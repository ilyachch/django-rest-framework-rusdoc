<!-- TRANSLATED by md-translate -->
# Тестирование

> Код без тестов сломан по умолчанию.
>
> - [Джейкоб Каплан-Мосс](https://jacobian.org/writing/django-apps-with-buildout/#s-create-a-test-wrapper)

DRF включает несколько вспомогательных классов, которые расширяют существующую тестовую структуру Django и улучшают поддержку выполнения API-запросов.

# APIRequestFactory

Расширяет [существующий в Django класс `RequestFactory`](https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.client.RequestFactory).

## Создание тестовых запросов

Класс `APIRequestFactory` поддерживает почти такой же API, как и стандартный класс Django `RequestFactory`. Это означает, что все стандартные методы `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` и `.options()` доступны.

```python
from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})

# Using the standard RequestFactory API to encode JSON data
request = factory.post('/notes/', {'title': 'new idea'}, content_type='application/json')
```

#### Использование аргумента `format`

Методы, создающие тело запроса, такие как `post`, `put` и `patch`, включают аргумент `format`, который позволяет легко генерировать запросы с использованием широкого набора форматов запросов.  При использовании этого аргумента фабрика выберет соответствующий рендерер и его сконфигурированный `content_type`.  Например:

```python
# Create a JSON POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')
```

По умолчанию доступны форматы `'multipart'` и `'json'`. Для совместимости с существующей в Django `RequestFactory` по умолчанию используется формат `'multipart'`.

Чтобы поддерживать более широкий набор форматов запросов или изменить формат по умолчанию, [см. раздел конфигурации](#Конфигурация).

#### Явное кодирование тела запроса

Если вам нужно явно закодировать тело запроса, вы можете сделать это, установив флаг `content_type`. Например:

```python
request = factory.post('/notes/', yaml.dump({'title': 'new idea'}), content_type='application/yaml')
```

#### PUT и PATCH с данными формы

Стоит отметить одно отличие между `RequestFactory` Django и `APIRequestFactory` DRF в том, что данные многочастной формы будут закодированы для методов, отличных от `.post()`.

Например, используя `APIRequestFactory`, вы можете сделать запрос формы PUT следующим образом:

```python
factory = APIRequestFactory()
request = factory.put('/notes/547/', {'title': 'remember to email dave'})
```

Используя `RequestFactory` от Django, вам придется явно кодировать данные самостоятельно:

```python
from django.test.client import encode_multipart, RequestFactory

factory = RequestFactory()
data = {'title': 'remember to email dave'}
content = encode_multipart('BoUnDaRyStRiNg', data)
content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
request = factory.put('/notes/547/', content, content_type=content_type)
```

## Принудительная аутентификация

При тестировании представлений непосредственно с помощью фабрики запросов часто бывает удобно иметь возможность напрямую аутентифицировать запрос, а не создавать правильные учетные данные для аутентификации.

Чтобы принудительно аутентифицировать запрос, используйте метод `force_authenticate()`.

```python
from rest_framework.test import force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='olivia')
view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
response = view(request)
```

Сигнатура для метода - `force_authenticate(request, user=None, token=None)`. При выполнении вызова может быть задан пользователь и токен или оба.

Например, при принудительной аутентификации с помощью токена вы можете сделать что-то вроде следующего:

```python
user = User.objects.get(username='olivia')
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user, token=user.auth_token)
```

---

**Примечание**: `force_authenticate` напрямую устанавливает `request.user` в экземпляр `user` в памяти. Если вы повторно используете один и тот же экземпляр `user` в нескольких тестах, которые обновляют сохраненное состояние `user`, вам может понадобиться вызывать [`refresh_from_db()`](https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.refresh_from_db) между тестами.

---

**Примечание**: При использовании `APIRequestFactory`, возвращаемый объект - это стандартный `HttpRequest` Django, а не объект `Request` DRF, который генерируется только после вызова представления.

Это означает, что установка атрибутов непосредственно на объект запроса не всегда может иметь ожидаемый эффект. Например, установка `.token` напрямую не будет иметь никакого эффекта, а установка `.user` напрямую будет работать только при использовании сеансовой аутентификации.

```python
# Request will only authenticate if `SessionAuthentication` is in use.
request = factory.get('/accounts/django-superstars/')
request.user = user
response = view(request)
```

---

## Принудительная проверка CSRF

По умолчанию запросы, созданные с помощью `APIRequestFactory`, не будут проходить проверку CSRF при передаче в представление DRF. Если вам необходимо явно включить проверку CSRF, вы можете сделать это, установив флаг `enforce_csrf_checks` при инстанцировании фабрики.

```python
factory = APIRequestFactory(enforce_csrf_checks=True)
```

---

**Примечание**: Стоит отметить, что стандартная фабрика запросов Django `RequestFactory` не должна включать эту опцию, потому что при использовании обычного Django проверка CSRF происходит в промежуточном ПО, которое не запускается при тестировании представлений напрямую. При использовании DRF проверка CSRF происходит внутри представления, поэтому в фабрике запросов необходимо отключить проверку CSRF на уровне представления.

---

# APIClient

Расширяет [существующий в Django класс `Client`](https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client).

## Выполнение запросов

Класс `APIClient` поддерживает тот же интерфейс запросов, что и стандартный класс Django `Client`. Это означает, что стандартные методы `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` и `.options()` доступны. Например:

```python
from rest_framework.test import APIClient

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

Чтобы поддерживать более широкий набор форматов запросов или изменить формат по умолчанию, [см. раздел конфигурации](#Конфигурация).

## Аутентификация

#### .login(**kwargs)

Метод `login` функционирует точно так же, как и в обычном классе Django `Client`. Это позволяет вам аутентифицировать запросы к любым представлениям, которые включают `SessionAuthentication`.

```python
# Make all requests in the context of a logged in session.
client = APIClient()
client.login(username='lauren', password='secret')
```

Чтобы выйти из системы, вызовите метод `logout`, как обычно.

```python
# Log out
client.logout()
```

Метод `login` подходит для тестирования API, использующих сеансовую аутентификацию, например, веб-сайтов, включающих AJAX-взаимодействие с API.

#### .credentials(**kwargs)

Метод `credentials` можно использовать для установки заголовков, которые затем будут включены во все последующие запросы тестового клиента.

```python
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Include an appropriate `Authorization:` header on all requests.
token = Token.objects.get(user__username='lauren')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```

Обратите внимание, что вызов `credentials` во второй раз перезаписывает все существующие учетные данные. Вы можете удалить все существующие учетные данные, вызвав метод без аргументов.

```python
# Stop including any credentials
client.credentials()
```

Метод `credentials` подходит для тестирования API, требующих заголовков аутентификации, таких как базовая аутентификация, аутентификация OAuth1a и OAuth2, а также простые схемы аутентификации токенов.

#### .force_authenticate(user=None, token=None)

Иногда вы можете захотеть полностью обойти аутентификацию и заставить все запросы тестового клиента автоматически рассматриваться как аутентифицированные.

Это может быть полезным сокращением, если вы тестируете API, но не хотите создавать действительные учетные данные аутентификации для выполнения тестовых запросов.

```python
user = User.objects.get(username='lauren')
client = APIClient()
client.force_authenticate(user=user)
```

Чтобы не аутентифицировать последующие запросы, вызовите `force_authenticate`, установив для пользователя и/или токена значение `None`.

```python
client.force_authenticate(user=None)
```

## Проверка CSRF

По умолчанию проверка CSRF не применяется при использовании `APIClient`. Если вам необходимо явно включить проверку CSRF, вы можете сделать это, установив флаг `enforce_csrf_checks` при инстанцировании клиента.

```python
client = APIClient(enforce_csrf_checks=True)
```

Обычно, проверка CSRF будет применяться только к любым аутентифицированным в сеансе представлениям. Это означает, что проверка CSRF будет происходить только в том случае, если клиент вошел в систему, вызвав `login()`.

---

# RequestsClient

DRF также включает клиент для взаимодействия с вашим приложением с помощью популярной библиотеки Python, `requests`. Это может быть полезно, если:

* Вы предполагаете взаимодействовать с API в основном из другого сервиса Python и хотите протестировать сервис на том же уровне, который будет видеть клиент.
* Вы хотите написать тесты таким образом, чтобы их можно было запускать в среде постановки или в реальном времени. (См. раздел "Живые тесты" ниже).

Это предоставляет точно такой же интерфейс, как если бы вы использовали сессию запросов напрямую.

```python
from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('http://testserver/users/')
assert response.status_code == 200
```

Обратите внимание, что клиент запросов требует передачи полностью определенных URL-адресов.

## RequestsClient и работа с базой данных

Класс `RequestsClient` полезен, если вы хотите написать тесты, которые взаимодействуют только с интерфейсом сервиса. Это немного строже, чем использование стандартного тестового клиента Django, поскольку это означает, что все взаимодействия должны осуществляться через API.

Если вы используете `RequestsClient`, вам нужно убедиться, что установка тестов и утверждения результатов выполняются как обычные вызовы API, а не взаимодействуют с моделями базы данных напрямую. Например, вместо того чтобы проверять, что `Customer.objects.count() == 3`, вы должны перечислить конечную точку `customers` и убедиться, что она содержит три записи.

## Заголовки и аутентификация

Пользовательские заголовки и учетные данные аутентификации могут быть предоставлены так же, как и [при использовании стандартного экземпляра `requests.Session`](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects).

```python
from requests.auth import HTTPBasicAuth

client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})
```

## CSRF

Если вы используете `SessionAuthentication`, то вам необходимо включить CSRF-токен для любых запросов `POST`, `PUT`, `PATCH` или `DELETE`.

Вы можете сделать это, следуя той же схеме, которую использует клиент на базе JavaScript. Сначала сделайте запрос `GET`, чтобы получить маркер CSRF, а затем цкажите этот токен в следующем запросе.

Например...

```python
client = RequestsClient()

# Obtain a CSRF token.
response = client.get('http://testserver/homepage/')
assert response.status_code == 200
csrftoken = response.cookies['csrftoken']

# Interact with the API.
response = client.post('http://testserver/organisations/', json={
    'name': 'MegaCorp',
    'status': 'active'
}, headers={'X-CSRFToken': csrftoken})
assert response.status_code == 200
```

## Живые тесты

При тщательном использовании и `RequestsClient`, и `CoreAPIClient` дают возможность писать тесты, которые можно запускать как в процессе разработки, так и непосредственно на build сервере или в production среде.

Использование этого стиля для создания базовых тестов нескольких основных частей функциональности является мощным способом проверки вашего живого сервиса. Это может потребовать некоторого внимания к `setup` и `teardown`, чтобы убедиться, что тесты выполняются таким образом, что они не влияют непосредственно на данные клиентов.

---

# CoreAPIClient

`CoreAPIClient` позволяет вам взаимодействовать с API с помощью клиентской библиотеки Python `coreapi`.

```python
# Fetch the API schema
client = CoreAPIClient()
schema = client.get('http://testserver/schema/')

# Create a new organisation
params = {'name': 'MegaCorp', 'status': 'active'}
client.action(schema, ['organisations', 'create'], params)

# Ensure that the organisation exists in the listing
data = client.action(schema, ['organisations', 'list'])
assert(len(data) == 1)
assert(data == [{'name': 'MegaCorp', 'status': 'active'}])
```

## Заголовки и аутентификация

Пользовательские заголовки и аутентификация могут использоваться с `CoreAPIClient` так же, как и с `RequestsClient`.

```python
from requests.auth import HTTPBasicAuth

client = CoreAPIClient()
client.session.auth = HTTPBasicAuth('user', 'pass')
client.session.headers.update({'x-test': 'true'})
```

---

# Тесты API

DRF включает следующие классы тестов, которые являются зеркальным отражением существующих [Django's test case classes](https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes), но используют `APIClient` вместо Django's default `Client`.

* `APISimpleTestCase`.
* `APITransactionTestCase`
* `APITestCase`
* `APILiveServerTestCase`

## Пример

Вы можете использовать любой из классов тестов DRF так же, как и обычные классы тестов Django. Атрибутом `self.client` будет экземпляр `APIClient`.

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myproject.apps.core.models import Account

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
```

---

# URLPatternsTestCase

DRF также предоставляет класс тестов для изоляции `urlpatterns` на основе каждого класса. Обратите внимание, что он наследуется от Django `SimpleTestCase`, и, скорее всего, его придется смешивать с другим классом тестов.

## Пример

```python
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
```

---

# Тестирование ответов

## Проверка данных ответа

При проверке достоверности тестовых ответов часто удобнее проверять данные, на основе которых был создан ответ, чем проверять полностью отрисованный ответ.

Например, проще проверить `response.data`:

```python
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
```

Вместо того чтобы проверять результат разбора `response.content`:

```python
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})
```

## Ответы на рендеринг

Если вы тестируете представления напрямую, используя `APIRequestFactory`, возвращаемые ответы еще не будут отрендерены, поскольку рендеринг ответов шаблона выполняется внутренним циклом запроса-ответа Django. Чтобы получить доступ к `response.content`, вам сначала нужно отрендерить ответ.

```python
view = UserDetail.as_view()
request = factory.get('/users/4')
response = view(request, pk='4')
response.render()  # Cannot access `response.content` without this.
self.assertEqual(response.content, '{"username": "lauren", "id": 4}')
```

---

# Конфигурация

## Установка формата по умолчанию

Формат по умолчанию, используемый для выполнения тестовых запросов, можно установить с помощью ключа настройки `TEST_REQUEST_DEFAULT_FORMAT`. Например, чтобы всегда использовать JSON для тестовых запросов по умолчанию вместо стандартных multipart form запросов, установите следующее в файле `settings.py`:

```python
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

## Установка доступных форматов

Если вам нужно протестировать запросы, использующие не многочастичные или json-запросы, вы можете сделать это, установив параметр `TEST_REQUEST_RENDERER_CLASSES`.

Например, чтобы добавить поддержку использования `format='html'` в тестовых запросах, в файле `settings.py` можно сделать что-то вроде этого.

```python
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}
```
