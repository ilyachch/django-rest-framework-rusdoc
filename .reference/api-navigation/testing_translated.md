<!-- TRANSLATED by md-translate -->
---

source:
    - test.py

источник:
- test.py

---

# Testing

# Тестирование

> Code without tests is broken as designed.
>
> &mdash; [Jacob Kaplan-Moss](https://jacobian.org/writing/django-apps-with-buildout/#s-create-a-test-wrapper)

> Код без тестов нарушается, как разработано.
>
> & mdash;
[Джейкоб Каплан-Мосс] (https://jacobian.org/writing/django-apps-with-buildout/#s-reate-a-test-wrapper)

REST framework includes a few helper classes that extend Django's existing test framework, and improve support for making API requests.

Структура REST включает в себя несколько вспомогательных классов, которые расширяют существующую тестовую структуру Django, и улучшают поддержку для выполнения запросов API.

# APIRequestFactory

# Apirequestfactory

Extends [Django's existing `RequestFactory` class](https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.client.RequestFactory).

Extends [Django's существующий `requestFactory` class] (https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.client.requestfactory).

## Creating test requests

## Создание тестовых запросов

The `APIRequestFactory` class supports an almost identical API to Django's standard `RequestFactory` class.  This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available.

Класс `apirequestfactory 'поддерживает почти идентичный API для стандартного класса Django` requestFactory'.
Это означает, что стандарт `.get ()`, `.post ()`, `.put ()`, `.patch ()`, `.delete ()`, `.head ()` и `.
() `Методы доступны.

```
from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
```

#### Using the `format` argument

#### с помощью аргумента `format`

Methods which create a request body, such as `post`, `put` and `patch`, include a `format` argument, which make it easy to generate requests using a content type other than multipart form data.  For example:

Методы, которые создают корпус запроса, такие как «post», `put` и` patch ', включают аргумент «формат», который позволяет легко генерировать запросы с использованием типа контента, кроме как многочисленных данных формы.
Например:

```
# Create a JSON POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')
```

By default the available formats are `'multipart'` and `'json'`.  For compatibility with Django's existing `RequestFactory` the default format is `'multipart'`.

По умолчанию доступные форматы: `'Multipart'` и`' json' '.
Для совместимости с существующим Django `requestFactory 'формат по умолчанию -`' Multipart '.

To support a wider set of request formats, or change the default format, [see the configuration section](#configuration).

Чтобы поддержать более широкий набор форматов запроса или изменить формат по умолчанию, [см. Раздел конфигурации] (#configuration).

#### Explicitly encoding the request body

#### явно кодируя корпус запроса

If you need to explicitly encode the request body, you can do so by setting the `content_type` flag.  For example:

Если вам нужно явно кодировать тело запроса, вы можете сделать это, установив флаг `content_type`.
Например:

```
request = factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')
```

#### PUT and PATCH with form data

#### положить и исправить данные

One difference worth noting between Django's `RequestFactory` and REST framework's `APIRequestFactory` is that multipart form data will be encoded for methods other than just `.post()`.

Одно отличие, которое стоит отметить между `QuequistFactory` и Framework's Framework Django, - это то, что многочисленные данные формы будут закодированы для других методов, отличных от` .post () `.

For example, using `APIRequestFactory`, you can make a form PUT request like so:

Например, используя `apirequestfactory`, вы можете сделать запрос на форму, как SO:

```
factory = APIRequestFactory()
request = factory.put('/notes/547/', {'title': 'remember to email dave'})
```

Using Django's `RequestFactory`, you'd need to explicitly encode the data yourself:

Используя Django `requestFactory`, вам нужно явно кодировать данные самостоятельно:

```
from django.test.client import encode_multipart, RequestFactory

factory = RequestFactory()
data = {'title': 'remember to email dave'}
content = encode_multipart('BoUnDaRyStRiNg', data)
content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
request = factory.put('/notes/547/', content, content_type=content_type)
```

## Forcing authentication

## принуждение аутентификации

When testing views directly using a request factory, it's often convenient to be able to directly authenticate the request, rather than having to construct the correct authentication credentials.

При тестировании представлений непосредственно с использованием завода запроса часто удобно иметь возможность напрямую аутентифицировать запрос, а не создавать правильные учетные данные аутентификации.

To forcibly authenticate a request, use the `force_authenticate()` method.

Чтобы насильно аутентифицировать запрос, используйте метод `force_authenticate ()`.

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

The signature for the method is `force_authenticate(request, user=None, token=None)`.  When making the call, either or both of the user and token may be set.

Подписью для метода является `force_authenticate (запрос, user = none, token = none)`.
При совершении вызова может быть установлен один или оба пользователя и токена.

For example, when forcibly authenticating using a token, you might do something like the following:

Например, при насильственном аутентификации с использованием токена вы можете сделать что -то вроде следующего:

```
user = User.objects.get(username='olivia')
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user, token=user.auth_token)
```

---

**Note**: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are re-using the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`](https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.refresh_from_db) between tests.

** ПРИМЕЧАНИЕ **: `force_authenticate` напрямую устанавливает` request.user` экземпляру `user`’ in-memory.
Если вы повторно используете один и тот же экземпляр `user` на нескольких тестах, которые обновляют сохраненное состояние` user`, вам может потребоваться позвонить [`refresh_from_db ()`] (https://docs.djangoproject.com/en/stable
/ref/models/instances/#django.db.models.model.refresh_from_db) между тестами.

---

**Note**: When using `APIRequestFactory`, the object that is returned is Django's standard `HttpRequest`, and not REST framework's `Request` object, which is only generated once the view is called.

** ПРИМЕЧАНИЕ **: При использовании `apirequestfactory` возвращаемый объект - это стандартный объект Django` httprequest`, а не объект REST Framework `request`, который генерируется только после того, как вид будет вызван.

This means that setting attributes directly on the request object may not always have the effect you expect.  For example, setting `.token` directly will have no effect, and setting `.user` directly will only work if session authentication is being used.

Это означает, что настройка атрибутов непосредственно на объект запроса не всегда может иметь эффект, который вы ожидаете.
Например, настройка `.token` напрямую не будет иметь эффекта, и настройка` .user` напрямую будет работать только в случае использования аутентификации сеанса.

```
# Request will only authenticate if `SessionAuthentication` is in use.
request = factory.get('/accounts/django-superstars/')
request.user = user
response = view(request)
```

---

## Forcing CSRF validation

## вынуждение проверки CSRF

By default, requests created with `APIRequestFactory` will not have CSRF validation applied when passed to a REST framework view.  If you need to explicitly turn CSRF validation on, you can do so by setting the `enforce_csrf_checks` flag when instantiating the factory.

По умолчанию запросы, созданные с помощью `apirequestfactory` не будут иметь проверку CSRF, применяются при передаче в представление структуры REST.
Если вам нужно явно включить валидацию CSRF, вы можете сделать это, установив флаг `reforce_csrf_checks` при создании завода.

```
factory = APIRequestFactory(enforce_csrf_checks=True)
```

---

**Note**: It's worth noting that Django's standard `RequestFactory` doesn't need to include this option, because when using regular Django the CSRF validation takes place in middleware, which is not run when testing views directly.  When using REST framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.

** ПРИМЕЧАНИЕ **: Стоит отметить, что стандартный `requestFactory 'Django не должен включать эту опцию, потому что при использовании обычного Django проверка CSRF происходит в промежуточном программном обеспечении, которое не выполняется при непосредственном тестировании видов.
При использовании Framework REST, проверка CSRF происходит внутри представления, поэтому заводская фабрика необходимо отключить проверки CSRF на уровне представления.

---

# APIClient

# Apiclient

Extends [Django's existing `Client` class](https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client).

Extends [Django's существующий `client` class] (https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client).

## Making requests

## Делать запросы

The `APIClient` class supports the same request interface as Django's standard `Client` class.  This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available.  For example:

Класс `apiclient` поддерживает тот же интерфейс запроса, что и стандартный класс Django` client`.
Это означает, что стандарт `.get ()`, `.post ()`, `.put ()`, `.patch ()`, `.delete ()`, `.head ()` и `.
() `Методы доступны.
Например:

```
from rest_framework.test import APIClient

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

To support a wider set of request formats, or change the default format, [see the configuration section](#configuration).

Чтобы поддержать более широкий набор форматов запроса или изменить формат по умолчанию, [см. Раздел конфигурации] (#configuration).

## Authenticating

## аутентификация

#### .login(**kwargs)

#### .login (** kwargs)

The `login` method functions exactly as it does with Django's regular `Client` class.  This allows you to authenticate requests against any views which include `SessionAuthentication`.

Метод `login` функционирует точно так же, как и с обычным классом Django` client '.
Это позволяет вам аутентифицировать запросы против любых представлений, которые включают «SessionAuthentication».

```
# Make all requests in the context of a logged in session.
client = APIClient()
client.login(username='lauren', password='secret')
```

To logout, call the `logout` method as usual.

Чтобы выходить из системы, вызовите метод `logout` как обычно.

```
# Log out
client.logout()
```

The `login` method is appropriate for testing APIs that use session authentication, for example web sites which include AJAX interaction with the API.

Метод `login` подходит для тестирования API, которые используют аутентификацию сеанса, например, веб -сайты, которые включают взаимодействие AJAX с API.

#### .credentials(**kwargs)

#### .credentials (** kwargs)

The `credentials` method can be used to set headers that will then be included on all subsequent requests by the test client.

Метод «учетных данных» можно использовать для установки заголовков, которые затем будут включены во все последующие запросы тестовым клиентом.

```
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Include an appropriate `Authorization:` header on all requests.
token = Token.objects.get(user__username='lauren')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```

Note that calling `credentials` a second time overwrites any existing credentials.  You can unset any existing credentials by calling the method with no arguments.

Обратите внимание, что вызов «учетных данных» во второй раз перезаписывает любые существующие учетные данные.
Вы можете не считать любые существующие учетные данные, вызывая метод без аргументов.

```
# Stop including any credentials
client.credentials()
```

The `credentials` method is appropriate for testing APIs that require authentication headers, such as basic authentication, OAuth1a and OAuth2 authentication, and simple token authentication schemes.

Метод «учетных данных» подходит для тестирования API, которые требуют заголовков аутентификации, таких как базовая аутентификация, аутентификация OAuth1a и OAuth2 и простые схемы аутентификации токенов.

#### .force_authenticate(user=None, token=None)

#### .force_authenticate (user = none, token = none)

Sometimes you may want to bypass authentication entirely and force all requests by the test client to be automatically treated as authenticated.

Иногда вы можете полностью обойти аутентификацию и заставлять все запросы тестовым клиентом автоматически рассматриваться как аутентификация.

This can be a useful shortcut if you're testing the API but don't want to have to construct valid authentication credentials in order to make test requests.

Это может быть полезным ярлыком, если вы тестируете API, но не хотите создавать допустимые учетные данные аутентификации, чтобы выполнить тестовые запросы.

```
user = User.objects.get(username='lauren')
client = APIClient()
client.force_authenticate(user=user)
```

To unauthenticate subsequent requests, call `force_authenticate` setting the user and/or token to `None`.

Чтобы не доставить последующие запросы, вызовите `force_authenticate` на установление пользователя и/или токена на` none`.

```
client.force_authenticate(user=None)
```

## CSRF validation

## Validation

By default CSRF validation is not applied when using `APIClient`.  If you need to explicitly enable CSRF validation, you can do so by setting the `enforce_csrf_checks` flag when instantiating the client.

По умолчанию валидация CSRF не применяется при использовании `apiclient`.
Если вам нужно явно включить проверку CSRF, вы можете сделать это, установив флаг `reforce_csrf_checks` при создании клиента.

```
client = APIClient(enforce_csrf_checks=True)
```

As usual CSRF validation will only apply to any session authenticated views.  This means CSRF validation will only occur if the client has been logged in by calling `login()`.

Как обычно, проверка CSRF будет применяться только к любым аутентированным представлениям сеанса.
Это означает, что проверка CSRF будет происходить только в том случае, если клиент был вошел в систему, вызывая `login ()`.

---

# RequestsClient

# Requestsclient

REST framework also includes a client for interacting with your application
using the popular Python library, `requests`. This may be useful if:

Структура REST также включает клиента для взаимодействия с вашим приложением
Используя популярную библиотеку Python, `запросы`.
Это может быть полезно, если:

* You are expecting to interface with the API primarily from another Python service,

* Вы ожидаете взаимодействовать с API в основном из другой услуги Python,

and want to test the service at the same level as the client will see.

и хочу проверить службу на том же уровне, что и клиент.

* You want to write tests in such a way that they can also be run against a staging or

* Вы хотите написать тесты таким образом, чтобы они также могли быть запущены против постановки или

live environment. (See "Live tests" below.)

живая среда.
(См. «Живые тесты» ниже.)

This exposes exactly the same interface as if you were using a requests session
directly.

Это раскрывает точно тот же интерфейс, что и если вы использовали сеанс запросов
напрямую.

```
from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('http://testserver/users/')
assert response.status_code == 200
```

Note that the requests client requires you to pass fully qualified URLs.

Обратите внимание, что клиент запроса требует, чтобы вы передали полностью квалифицированные URL -адреса.

## RequestsClient and working with the database

## RequestSclient и работа с базой данных

The `RequestsClient` class is useful if you want to write tests that solely interact with the service interface. This is a little stricter than using the standard Django test client, as it means that all interactions should be via the API.

Класс `requestsClient` полезен, если вы хотите написать тесты, которые взаимодействуют исключительно с интерфейсом службы.
Это немного строго, чем использование стандартного тестового клиента Django, поскольку это означает, что все взаимодействия должны быть через API.

If you're using `RequestsClient` you'll want to ensure that test setup, and results assertions are performed as regular API calls, rather than interacting with the database models directly. For example, rather than checking that `Customer.objects.count() == 3` you would list the customers endpoint, and ensure that it contains three records.

Если вы используете `requestsClient`, вы захотите убедиться, что настройка теста, а утверждения результатов выполняются в виде регулярных вызовов API, а не взаимодействовать с моделями базы данных напрямую.
Например, вместо того, чтобы проверять, что `customer.objects.count () == 3` вы перечислите конечную точку клиентов и убедитесь, что он содержит три записи.

## Headers & Authentication

## заголовки и аутентификация

Custom headers and authentication credentials can be provided in the same way
as [when using a standard `requests.Session` instance](https://requests.readthedocs.io/en/master/user/advanced/#session-objects).

Пользовательские заголовки и учетные данные аутентификации могут быть предоставлены таким же образом
как [при использовании стандартного `requests.session` ancement] (https://requests.readthedocs.io/en/master/user/advanced/#session-objects).

```
from requests.auth import HTTPBasicAuth

client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})
```

## CSRF

## csrf

If you're using `SessionAuthentication` then you'll need to include a CSRF token
for any `POST`, `PUT`, `PATCH` or `DELETE` requests.

Если вы используете `sessionAuthentication`, вам нужно будет включить токен CSRF
Для любых запросов `post`,` put`, `patch` или` delete '.

You can do so by following the same flow that a JavaScript based client would use.
First, make a `GET` request in order to obtain a CSRF token, then present that
token in the following request.

Вы можете сделать это, следуя тому же потоку, который использовал клиент на основе JavaScript.
Сначала сделайте запрос `get`, чтобы получить токен CSRF, а затем представьте, что
токен в следующем запросе.

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

With careful usage both the `RequestsClient` and the `CoreAPIClient` provide
the ability to write test cases that can run either in development, or be run
directly against your staging server or production environment.

При тщательном использовании как `requestsclient, и` coreapiclient
Возможность писать тестовые примеры, которые могут работать либо в разработке, либо запускаться
непосредственно против вашего проставочного сервера или производственной среды.

Using this style to create basic tests of a few core pieces of functionality is
a powerful way to validate your live service. Doing so may require some careful
attention to setup and teardown to ensure that the tests run in a way that they
do not directly affect customer data.

Использование этого стиля для создания основных тестов нескольких основных функций
Мощный способ подтвердить ваш живой сервис.
Это может потребовать некоторых осторожных
внимание к настройке и разрыв, чтобы гарантировать, что тесты работают так, как они
Не влияйте на данные клиента.

---

# CoreAPIClient

# Coreapiclient

The CoreAPIClient allows you to interact with your API using the Python
`coreapi` client library.

Coreapiclient позволяет вам взаимодействовать с вашим API с помощью Python
`Клиентская библиотека Coreapi.

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

## заголовки и аутентификация

Custom headers and authentication may be used with `CoreAPIClient` in a
similar way as with `RequestsClient`.

Пользовательские заголовки и аутентификация могут использоваться с `coreapiclient` в
Аналогично, как с `requestsclient`.

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

Структура REST включает в себя следующие классы тестового примера, которые отражают существующие [классы тестового примера Django] (https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes),
Но используйте `apiclient` вместо по умолчанию Django` client '.

* `APISimpleTestCase`
* `APITransactionTestCase`
* `APITestCase`
* `APILiveServerTestCase`

* `ApisimpleTestSact`
* `ApitransactionTestCase`
* `Apitestcase`
* `ApiliveSerVertStAcke`

## Example

## Пример

You can use any of REST framework's test case classes as you would for the regular Django test case classes.  The `self.client` attribute will be an `APIClient` instance.

Вы можете использовать любой из тестовых примеров REST Framework, как для обычных тестовых примеров Django.
Атрибутом `self.client` будет экземпляром` apiclient '.

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

# Urlpatternstestcase

REST framework also provides a test case class for isolating `urlpatterns` on a per-class basis. Note that this inherits from Django's `SimpleTestCase`, and will most likely need to be mixed with another test case class.

Структура REST также предоставляет тестовый класс для изоляции `urlPatterns 'для каждого класса.
Обратите внимание, что это наследует от «SimpleTestSteCase» Джанго, и, скорее всего, потребуется смешать с другим классом тестового примера.

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

При проверке достоверности испытательных ответов часто удобнее осмотреть данные, с которыми был создан ответ, а не осматривать полностью отображаемый ответ.

For example, it's easier to inspect `response.data`:

Например, легче проверить `recsom.data`:

```
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
```

Instead of inspecting the result of parsing `response.content`:

Вместо проверки результата анализа `response.content`:

```
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})
```

## Rendering responses

## redending ответы

If you're testing views directly using `APIRequestFactory`, the responses that are returned will not yet be rendered, as rendering of template responses is performed by Django's internal request-response cycle.  In order to access `response.content`, you'll first need to render the response.

Если вы тестируете представления непосредственно, используя `apirequestfactory`, возвращаемые ответы еще не будут отображаться, поскольку рендеринг ответов шаблонов выполняется в цикле внутреннего запроса-ответа Джанго.
Чтобы получить доступ к `response.content`, вам сначала необходимо привести ответ.

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

## Настройка формата по умолчанию

The default format used to make test requests may be set using the `TEST_REQUEST_DEFAULT_FORMAT` setting key.  For example, to always use JSON for test requests by default instead of standard multipart form requests, set the following in your `settings.py` file:

Формат по умолчанию, используемый для выполнения тестовых запросов, может быть установлен с использованием клавиши настройки `test_request_default_format`.
Например, чтобы всегда использовать JSON для тестовых запросов по умолчанию вместо стандартных запросов формы Multipart, установите следующее в вашем файле `futs.py`:

```
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

## Setting the available formats

## Установка доступных форматов

If you need to test requests using something other than multipart or json requests, you can do so by setting the `TEST_REQUEST_RENDERER_CLASSES` setting.

Если вам нужно тестировать запросы, используя что -то другое, кроме запросов Multipart или JSON, вы можете сделать это, установив настройку `test_request_renderer_classes`.

For example, to add support for using `format='html'` in test requests, you might have something like this in your `settings.py` file.

Например, чтобы добавить поддержку для использования `format = 'html'` в тестовых запросах, у вас может быть что -то подобное в вашем файле` futs.py.

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
