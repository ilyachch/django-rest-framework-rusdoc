<!-- TRANSLATED by md-translate -->
---

source:

источник:

* test.py

* test.py

---

# Testing

# Тестирование

> Code without tests is broken as designed.
>
> — [Jacob Kaplan-Moss][cite]

> Код без тестов сломан, как и было задумано.
>
> - [Джейкоб Каплан-Мосс][cite]

REST framework includes a few helper classes that extend Django's existing test framework, and improve support for making API requests.

Фреймворк REST включает несколько вспомогательных классов, которые расширяют существующую тестовую структуру Django и улучшают поддержку выполнения API-запросов.

# APIRequestFactory

# APIRequestFactory

Extends [Django's existing `RequestFactory` class][requestfactory].

Расширяет [существующий в Django класс `RequestFactory`][requestfactory].

## Creating test requests

## Создание тестовых запросов

The `APIRequestFactory` class supports an almost identical API to Django's standard `RequestFactory` class. This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available.

Класс `APIRequestFactory` поддерживает почти такой же API, как и стандартный класс Django `RequestFactory`. Это означает, что все стандартные методы `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` и `.options()` доступны.

```
from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
```

#### Using the `format` argument

#### Использование аргумента `формат`

Methods which create a request body, such as `post`, `put` and `patch`, include a `format` argument, which make it easy to generate requests using a content type other than multipart form data. For example:

Методы, создающие тело запроса, такие как `post`, `put` и `patch`, включают аргумент `формат`, что облегчает генерацию запросов, использующих тип содержимого, отличный от многокомпонентных данных формы. Например:

```
# Create a JSON POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')
```

By default the available formats are `'multipart'` and `'json'`. For compatibility with Django's existing `RequestFactory` the default format is `'multipart'`.

По умолчанию доступны форматы `'multipart'' и `'json''. Для совместимости с существующей в Django `RequestFactory` по умолчанию используется формат `'multipart'`.

To support a wider set of request formats, or change the default format, [see the configuration section](#configuration).

Чтобы поддерживать более широкий набор форматов запросов или изменить формат по умолчанию, [см. раздел конфигурации](#configuration).

#### Explicitly encoding the request body

#### Явное кодирование тела запроса

If you need to explicitly encode the request body, you can do so by setting the `content_type` flag. For example:

Если вам нужно явно закодировать тело запроса, вы можете сделать это, установив флаг `content_type`. Например:

```
request = factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')
```

#### PUT and PATCH with form data

#### PUT и PATCH с данными формы

One difference worth noting between Django's `RequestFactory` and REST framework's `APIRequestFactory` is that multipart form data will be encoded for methods other than just `.post()`.

Стоит отметить одно отличие между `RequestFactory` Django и `APIRequestFactory` фреймворка REST в том, что данные многочастной формы будут закодированы для методов, отличных от `.post()`.

For example, using `APIRequestFactory`, you can make a form PUT request like so:

Например, используя `APIRequestFactory`, вы можете сделать запрос формы PUT следующим образом:

```
factory = APIRequestFactory()
request = factory.put('/notes/547/', {'title': 'remember to email dave'})
```

Using Django's `RequestFactory`, you'd need to explicitly encode the data yourself:

Используя `RequestFactory` от Django, вам придется явно кодировать данные самостоятельно:

```
from django.test.client import encode_multipart, RequestFactory

factory = RequestFactory()
data = {'title': 'remember to email dave'}
content = encode_multipart('BoUnDaRyStRiNg', data)
content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
request = factory.put('/notes/547/', content, content_type=content_type)
```

## Forcing authentication

## Принудительная аутентификация

When testing views directly using a request factory, it's often convenient to be able to directly authenticate the request, rather than having to construct the correct authentication credentials.

При тестировании представлений непосредственно с помощью фабрики запросов часто бывает удобно иметь возможность напрямую аутентифицировать запрос, а не создавать правильные учетные данные для аутентификации.

To forcibly authenticate a request, use the `force_authenticate()` method.

Чтобы принудительно аутентифицировать запрос, используйте метод `force_authenticate()`.

```
from rest_framework.test import force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='olivia')
view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
response = view(request)
```

The signature for the method is `force_authenticate(request, user=None, token=None)`. When making the call, either or both of the user and token may be set.

Подпись для метода - `force_authenticate(request, user=None, token=None)`. При выполнении вызова может быть задан пользователь и токен или оба.

For example, when forcibly authenticating using a token, you might do something like the following:

Например, при принудительной аутентификации с помощью маркера вы можете сделать что-то вроде следующего:

```
user = User.objects.get(username='olivia')
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user, token=user.auth_token)
```

---

**Note**: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are re-using the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`](https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.refresh_from_db) between tests.

**Примечание**: `force_authenticate` напрямую устанавливает `request.user` в экземпляр `user` в памяти. Если вы повторно используете один и тот же экземпляр `user` в нескольких тестах, которые обновляют сохраненное состояние `user`, вам может понадобиться вызывать [`refresh_from_db()`](https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.refresh_from_db) между тестами.

---

**Note**: When using `APIRequestFactory`, the object that is returned is Django's standard `HttpRequest`, and not REST framework's `Request` object, which is only generated once the view is called.

**Примечание**: При использовании `APIRequestFactory`, возвращаемый объект - это стандартный `HttpRequest` Django, а не объект `Request` фреймворка REST, который генерируется только после вызова представления.

This means that setting attributes directly on the request object may not always have the effect you expect. For example, setting `.token` directly will have no effect, and setting `.user` directly will only work if session authentication is being used.

Это означает, что установка атрибутов непосредственно на объект запроса не всегда может иметь ожидаемый эффект. Например, установка `.token` напрямую не будет иметь никакого эффекта, а установка `.user` напрямую будет работать только при использовании сеансовой аутентификации.

```
# Request will only authenticate if `SessionAuthentication` is in use.
request = factory.get('/accounts/django-superstars/')
request.user = user
response = view(request)
```

---

## Forcing CSRF validation

## Принудительная проверка CSRF

By default, requests created with `APIRequestFactory` will not have CSRF validation applied when passed to a REST framework view. If you need to explicitly turn CSRF validation on, you can do so by setting the `enforce_csrf_checks` flag when instantiating the factory.

По умолчанию запросы, созданные с помощью `APIRequestFactory`, не будут проходить проверку CSRF при передаче в представление REST-фреймворка. Если вам необходимо явно включить проверку CSRF, вы можете сделать это, установив флаг `enforce_csrf_checks` при инстанцировании фабрики.

```
factory = APIRequestFactory(enforce_csrf_checks=True)
```

---

**Note**: It's worth noting that Django's standard `RequestFactory` doesn't need to include this option, because when using regular Django the CSRF validation takes place in middleware, which is not run when testing views directly. When using REST framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.

**Примечание**: Стоит отметить, что стандартная фабрика запросов Django `RequestFactory` не должна включать эту опцию, потому что при использовании обычного Django проверка CSRF происходит в промежуточном ПО, которое не запускается при тестировании представлений напрямую. При использовании фреймворка REST проверка CSRF происходит внутри представления, поэтому в фабрике запросов необходимо отключить проверку CSRF на уровне представления.

---

# APIClient

# APIClient

Extends [Django's existing `Client` class](https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client).

Расширяет [существующий в Django класс `Client`] (https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client).

## Making requests

## Выполнение запросов

The `APIClient` class supports the same request interface as Django's standard `Client` class. This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available. For example:

Класс `APIClient` поддерживает тот же интерфейс запросов, что и стандартный класс Django `Client`. Это означает, что стандартные методы `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` и `.options()` доступны. Например:

```
from rest_framework.test import APIClient

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

To support a wider set of request formats, or change the default format, [see the configuration section](#configuration).

Чтобы поддерживать более широкий набор форматов запросов или изменить формат по умолчанию, [см. раздел конфигурации](#configuration).

## Authenticating

## Аутентификация

#### .login(**kwargs)

#### .login(**kwargs)

The `login` method functions exactly as it does with Django's regular `Client` class. This allows you to authenticate requests against any views which include `SessionAuthentication`.

Метод `login` функционирует точно так же, как и в обычном классе Django `Client`. Это позволяет вам аутентифицировать запросы к любым представлениям, которые включают `SessionAuthentication`.

```
# Make all requests in the context of a logged in session.
client = APIClient()
client.login(username='lauren', password='secret')
```

To logout, call the `logout` method as usual.

Чтобы выйти из системы, вызовите метод `logout`, как обычно.

```
# Log out
client.logout()
```

The `login` method is appropriate for testing APIs that use session authentication, for example web sites which include AJAX interaction with the API.

Метод `login` подходит для тестирования API, использующих сеансовую аутентификацию, например, веб-сайтов, включающих AJAX-взаимодействие с API.

#### .credentials(**kwargs)

#### .credentials(**kwargs)

The `credentials` method can be used to set headers that will then be included on all subsequent requests by the test client.

Метод `credentials` можно использовать для установки заголовков, которые затем будут включены во все последующие запросы тестового клиента.

```
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Include an appropriate `Authorization:` header on all requests.
token = Token.objects.get(user__username='lauren')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```

Note that calling `credentials` a second time overwrites any existing credentials. You can unset any existing credentials by calling the method with no arguments.

Обратите внимание, что вызов `credentials` во второй раз перезаписывает все существующие учетные данные. Вы можете удалить все существующие учетные данные, вызвав метод без аргументов.

```
# Stop including any credentials
client.credentials()
```

The `credentials` method is appropriate for testing APIs that require authentication headers, such as basic authentication, OAuth1a and OAuth2 authentication, and simple token authentication schemes.

Метод `credentials` подходит для тестирования API, требующих заголовков аутентификации, таких как базовая аутентификация, аутентификация OAuth1a и OAuth2, а также простые схемы аутентификации токенов.

#### .force_authenticate(user=None, token=None)

#### .force_authenticate(user=None, token=None)

Sometimes you may want to bypass authentication entirely and force all requests by the test client to be automatically treated as authenticated.

Иногда вы можете захотеть полностью обойти аутентификацию и заставить все запросы тестового клиента автоматически рассматриваться как аутентифицированные.

This can be a useful shortcut if you're testing the API but don't want to have to construct valid authentication credentials in order to make test requests.

Это может быть полезным сокращением, если вы тестируете API, но не хотите создавать действительные учетные данные аутентификации для выполнения тестовых запросов.

```
user = User.objects.get(username='lauren')
client = APIClient()
client.force_authenticate(user=user)
```

To unauthenticate subsequent requests, call `force_authenticate` setting the user and/or token to `None`.

Чтобы не аутентифицировать последующие запросы, вызовите `force_authenticate`, установив для пользователя и/или токена значение `None`.

```
client.force_authenticate(user=None)
```

## CSRF validation

## Проверка CSRF

By default CSRF validation is not applied when using `APIClient`. If you need to explicitly enable CSRF validation, you can do so by setting the `enforce_csrf_checks` flag when instantiating the client.

По умолчанию проверка CSRF не применяется при использовании `APIClient`. Если вам необходимо явно включить проверку CSRF, вы можете сделать это, установив флаг `enforce_csrf_checks` при инстанцировании клиента.

```
client = APIClient(enforce_csrf_checks=True)
```

As usual CSRF validation will only apply to any session authenticated views. This means CSRF validation will only occur if the client has been logged in by calling `login()`.

Как обычно, проверка CSRF будет применяться только к любым аутентифицированным в сеансе представлениям. Это означает, что проверка CSRF будет происходить только в том случае, если клиент вошел в систему, вызвав `login()`.

---

# RequestsClient

# RequestsClient

REST framework also includes a client for interacting with your application using the popular Python library, `requests`. This may be useful if:

REST framework также включает клиент для взаимодействия с вашим приложением с помощью популярной библиотеки Python, `requests`. Это может быть полезно, если:

* You are expecting to interface with the API primarily from another Python service, and want to test the service at the same level as the client will see.
* You want to write tests in such a way that they can also be run against a staging or live environment. (See "Live tests" below.)

* Вы предполагаете взаимодействовать с API в основном из другого сервиса Python и хотите протестировать сервис на том же уровне, который будет видеть клиент.
* Вы хотите написать тесты таким образом, чтобы их можно было запускать в среде постановки или в реальном времени. (См. раздел "Живые тесты" ниже).

This exposes exactly the same interface as if you were using a requests session directly.

Это предоставляет точно такой же интерфейс, как если бы вы использовали сессию запросов напрямую.

```
from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('http://testserver/users/')
assert response.status_code == 200
```

Note that the requests client requires you to pass fully qualified URLs.

Обратите внимание, что клиент запросов требует передачи полностью определенных URL-адресов.

## RequestsClient and working with the database

## RequestsClient и работа с базой данных

The `RequestsClient` class is useful if you want to write tests that solely interact with the service interface. This is a little stricter than using the standard Django test client, as it means that all interactions should be via the API.

Класс `RequestsClient` полезен, если вы хотите написать тесты, которые взаимодействуют только с интерфейсом сервиса. Это немного строже, чем использование стандартного тестового клиента Django, поскольку это означает, что все взаимодействия должны осуществляться через API.

If you're using `RequestsClient` you'll want to ensure that test setup, and results assertions are performed as regular API calls, rather than interacting with the database models directly. For example, rather than checking that `Customer.objects.count() == 3` you would list the customers endpoint, and ensure that it contains three records.

Если вы используете `RequestsClient`, вам нужно убедиться, что установка тестов и утверждения результатов выполняются как обычные вызовы API, а не взаимодействуют с моделями базы данных напрямую. Например, вместо того чтобы проверять, что `Customer.objects.count() == 3`, вы должны перечислить конечную точку customers и убедиться, что она содержит три записи.

## Headers & Authentication

## Заголовки и аутентификация

Custom headers and authentication credentials can be provided in the same way as [when using a standard `requests.Session` instance](https://requests.readthedocs.io/en/master/user/advanced/#session-objects).

Пользовательские заголовки и учетные данные аутентификации могут быть предоставлены так же, как и [при использовании стандартного экземпляра `requests.Session`] (https://requests.readthedocs.io/en/master/user/advanced/#session-objects).

```
from requests.auth import HTTPBasicAuth

client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})
```

## CSRF

## CSRF

If you're using `SessionAuthentication` then you'll need to include a CSRF token for any `POST`, `PUT`, `PATCH` or `DELETE` requests.

Если вы используете `SessionAuthentication`, то вам необходимо включить CSRF-токен для любых запросов `POST`, `PUT`, `PATCH` или `DELETE`.

You can do so by following the same flow that a JavaScript based client would use. First, make a `GET` request in order to obtain a CSRF token, then present that token in the following request.

Вы можете сделать это, следуя той же схеме, которую использует клиент на базе JavaScript. Сначала сделайте запрос `GET`, чтобы получить маркер CSRF, а затем представьте этот маркер в следующем запросе.

For example...

Например...

```
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

## Live tests

## Живые тесты

With careful usage both the `RequestsClient` and the `CoreAPIClient` provide the ability to write test cases that can run either in development, or be run directly against your staging server or production environment.

При тщательном использовании и `RequestsClient`, и `CoreAPIClient` дают возможность писать тестовые примеры, которые можно запускать как в процессе разработки, так и непосредственно на сервере постановки или в производственной среде.

Using this style to create basic tests of a few core pieces of functionality is a powerful way to validate your live service. Doing so may require some careful attention to setup and teardown to ensure that the tests run in a way that they do not directly affect customer data.

Использование этого стиля для создания базовых тестов нескольких основных частей функциональности является мощным способом проверки вашего живого сервиса. Это может потребовать некоторого внимания к настройке и демонтажу, чтобы убедиться, что тесты выполняются таким образом, что они не влияют непосредственно на данные клиента.

---

# CoreAPIClient

# CoreAPIClient

The CoreAPIClient allows you to interact with your API using the Python `coreapi` client library.

CoreAPIClient позволяет вам взаимодействовать с API с помощью клиентской библиотеки Python `coreapi`.

```
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

## Headers & Authentication

## Заголовки и аутентификация

Custom headers and authentication may be used with `CoreAPIClient` in a similar way as with `RequestsClient`.

Пользовательские заголовки и аутентификация могут использоваться с `CoreAPIClient` так же, как и с `RequestsClient`.

```
from requests.auth import HTTPBasicAuth

client = CoreAPIClient()
client.session.auth = HTTPBasicAuth('user', 'pass')
client.session.headers.update({'x-test': 'true'})
```

---

# API Test cases

# Тестовые случаи API

REST framework includes the following test case classes, that mirror the existing [Django's test case classes](https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes), but use `APIClient` instead of Django's default `Client`.

Фреймворк REST включает следующие классы тестовых примеров, которые являются зеркальным отражением существующих [Django's test case classes](https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes), но используют `APIClient` вместо Django's default `Client`.

* `APISimpleTestCase`
* `APITransactionTestCase`
* `APITestCase`
* `APILiveServerTestCase`

* `APISimpleTestCase`.
* `APITransactionTestCase`
* `APITestCase`
* `APILiveServerTestCase`

## Example

## Пример

You can use any of REST framework's test case classes as you would for the regular Django test case classes. The `self.client` attribute will be an `APIClient` instance.

Вы можете использовать любой из классов тестовых примеров фреймворка REST так же, как и обычные классы тестовых примеров Django. Атрибутом `self.client` будет экземпляр `APIClient`.

```
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

# URLPatternsTestCase

REST framework also provides a test case class for isolating `urlpatterns` on a per-class basis. Note that this inherits from Django's `SimpleTestCase`, and will most likely need to be mixed with another test case class.

REST framework также предоставляет класс тестовых примеров для изоляции `urlpatterns` на основе каждого класса. Обратите внимание, что он наследуется от Django `SimpleTestCase`, и, скорее всего, его придется смешивать с другим классом тестовых примеров.

## Example

## Пример

```
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

# Testing responses

# Тестирование ответов

## Checking the response data

## Проверка данных ответа

When checking the validity of test responses it's often more convenient to inspect the data that the response was created with, rather than inspecting the fully rendered response.

При проверке достоверности тестовых ответов часто удобнее проверять данные, на основе которых был создан ответ, чем проверять полностью отрисованный ответ.

For example, it's easier to inspect `response.data`:

Например, проще проверить `response.data`:

```
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
```

Instead of inspecting the result of parsing `response.content`:

Вместо того чтобы проверять результат разбора `response.content`:

```
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})
```

## Rendering responses

## Ответы на рендеринг

If you're testing views directly using `APIRequestFactory`, the responses that are returned will not yet be rendered, as rendering of template responses is performed by Django's internal request-response cycle. In order to access `response.content`, you'll first need to render the response.

Если вы тестируете представления напрямую, используя `APIRequestFactory`, возвращаемые ответы еще не будут отрисованы, поскольку отрисовка ответов шаблона выполняется внутренним циклом запроса-ответа Django. Чтобы получить доступ к `response.content`, вам сначала нужно отрендерить ответ.

```
view = UserDetail.as_view()
request = factory.get('/users/4')
response = view(request, pk='4')
response.render()  # Cannot access `response.content` without this.
self.assertEqual(response.content, '{"username": "lauren", "id": 4}')
```

---

# Configuration

# Конфигурация

## Setting the default format

## Установка формата по умолчанию

The default format used to make test requests may be set using the `TEST_REQUEST_DEFAULT_FORMAT` setting key. For example, to always use JSON for test requests by default instead of standard multipart form requests, set the following in your `settings.py` file:

Формат по умолчанию, используемый для выполнения тестовых запросов, можно установить с помощью ключа настройки `TEST_REQUEST_DEFAULT_FORMAT`. Например, чтобы всегда использовать JSON для тестовых запросов по умолчанию вместо стандартных многочастных запросов, установите следующее в файле `settings.py`:

```
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

## Setting the available formats

## Установка доступных форматов

If you need to test requests using something other than multipart or json requests, you can do so by setting the `TEST_REQUEST_RENDERER_CLASSES` setting.

Если вам нужно протестировать запросы, использующие не многочастичные или json-запросы, вы можете сделать это, установив параметр `TEST_REQUEST_RENDERER_CLASSES`.

For example, to add support for using `format='html'` in test requests, you might have something like this in your `settings.py` file.

Например, чтобы добавить поддержку использования `format='html'` в тестовых запросах, в файле `settings.py` можно сделать что-то вроде этого.

```
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}
```