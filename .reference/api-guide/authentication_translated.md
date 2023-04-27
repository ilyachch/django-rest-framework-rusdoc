<!-- TRANSLATED by md-translate -->
---

source:
    - authentication.py

источник:
- authentication.py

---

# Authentication

# Аутентификация

> Auth needs to be pluggable.
>
> &mdash; Jacob Kaplan-Moss, ["REST worst practices"](https://jacobian.org/writing/rest-worst-practices/)

> Auth должен быть подключаемым.
>
> &mdash; Джейкоб Каплан-Мосс, ["Худшие практики REST"](https://jacobian.org/writing/rest-worst-practices/)

Authentication is the mechanism of associating an incoming request with a set of identifying credentials, such as the user the request came from, or the token that it was signed with.  The [permission](permissions.md) and [throttling](throttling.md) policies can then use those credentials to determine if the request should be permitted.

Аутентификация - это механизм связывания входящего запроса с набором идентификационных данных, таких как пользователь, от которого пришел запрос, или токен, которым он был подписан.  Политики [permission](permissions.md) и [throttling](throttling.md) могут затем использовать эти учетные данные, чтобы определить, должен ли запрос быть разрешен.

REST framework provides several authentication schemes out of the box, and also allows you to implement custom schemes.

Фреймворк REST предоставляет несколько схем аутентификации из коробки, а также позволяет реализовать пользовательские схемы.

Authentication always runs at the very start of the view, before the permission and throttling checks occur, and before any other code is allowed to proceed.

Аутентификация всегда выполняется в самом начале представления, до того, как произойдет проверка разрешений и дросселирование, и до того, как будет разрешено выполнение любого другого кода.

The `request.user` property will typically be set to an instance of the `contrib.auth` package's `User` class.

Свойство `request.user` обычно устанавливается на экземпляр класса `User` пакета `contrib.auth`.

The `request.auth` property is used for any additional authentication information, for example, it may be used to represent an authentication token that the request was signed with.

Свойство `request.auth` используется для любой дополнительной информации об аутентификации, например, оно может быть использовано для представления маркера аутентификации, которым был подписан запрос.

---

**Note:** Don't forget that **authentication by itself won't allow or disallow an incoming request**, it simply identifies the credentials that the request was made with.

**Примечание:** Не забывайте, что **аутентификация сама по себе не разрешает и не запрещает входящий запрос**, она просто идентифицирует учетные данные, с которыми был сделан запрос.

For information on how to set up the permission policies for your API please see the [permissions documentation](permissions.md).

Информацию о том, как настроить политику разрешений для вашего API, смотрите в документации [permissions](permissions.md).

---

## How authentication is determined

## Как определяется аутентификация

The authentication schemes are always defined as a list of classes.  REST framework will attempt to authenticate with each class in the list, and will set `request.user` and `request.auth` using the return value of the first class that successfully authenticates.

Схемы аутентификации всегда определяются как список классов.  REST framework попытается аутентифицироваться с каждым классом в списке, и установит `request.user` и `request.auth`, используя возвращаемое значение первого класса, который успешно аутентифицируется.

If no class authenticates, `request.user` will be set to an instance of `django.contrib.auth.models.AnonymousUser`, and `request.auth` will be set to `None`.

Если ни один класс не аутентифицирует, `request.user` будет установлен в экземпляр `django.contrib.auth.models.AnonymousUser`, а `request.auth` будет установлен в `None`.

The value of `request.user` and `request.auth` for unauthenticated requests can be modified using the `UNAUTHENTICATED_USER` and `UNAUTHENTICATED_TOKEN` settings.

Значение `request.user` и `request.auth` для неаутентифицированных запросов можно изменить с помощью параметров `UNAUTHENTICATED_USER` и `UNAUTHENTICATED_TOKEN`.

## Setting the authentication scheme

## Установка схемы аутентификации

The default authentication schemes may be set globally, using the `DEFAULT_AUTHENTICATION_CLASSES` setting.  For example.

Схемы аутентификации по умолчанию можно установить глобально, используя параметр `DEFAULT_AUTHENTICATION_CLASSES`.  Например.

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

You can also set the authentication scheme on a per-view or per-viewset basis,
using the `APIView` class-based views.

Вы также можете установить схему аутентификации для каждого вида или каждого набора видов,
используя класс `APIView`, основанный на представлениях.

```
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
```

Or, if you're using the `@api_view` decorator with function based views.

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)
```

## Unauthorized and Forbidden responses

## Неавторизованные и запрещенные ответы

When an unauthenticated request is denied permission there are two different error codes that may be appropriate.

Когда неаутентифицированному запросу отказано в разрешении, существует два различных кода ошибок, которые могут быть уместны.

* [HTTP 401 Unauthorized](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
* [HTTP 403 Permission Denied](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

* [HTTP 401 Unauthorized](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
* [HTTP 403 Permission Denied](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

HTTP 401 responses must always include a `WWW-Authenticate` header, that instructs the client how to authenticate.  HTTP 403 responses do not include the `WWW-Authenticate` header.

Ответы HTTP 401 всегда должны содержать заголовок `WWW-Authenticate`, который указывает клиенту, как пройти аутентификацию.  Ответы HTTP 403 не включают заголовок `WWW-Authenticate`.

The kind of response that will be used depends on the authentication scheme.  Although multiple authentication schemes may be in use, only one scheme may be used to determine the type of response.  **The first authentication class set on the view is used when determining the type of response**.

Тип ответа, который будет использоваться, зависит от схемы аутентификации.  Хотя может использоваться несколько схем аутентификации, для определения типа ответа может использоваться только одна схема.  **Первый класс аутентификации, установленный в представлении, используется при определении типа ответа**.

Note that when a request may successfully authenticate, but still be denied permission to perform the request, in which case a `403 Permission Denied` response will always be used, regardless of the authentication scheme.

Обратите внимание, что когда запрос может успешно пройти аутентификацию, но при этом получить отказ в разрешении на выполнение запроса, в этом случае всегда будет использоваться ответ `403 Permission Denied`, независимо от схемы аутентификации.

## Apache mod_wsgi specific configuration

## Специфическая конфигурация Apache mod_wsgi

Note that if deploying to [Apache using mod_wsgi](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html), the authorization header is not passed through to a WSGI application by default, as it is assumed that authentication will be handled by Apache, rather than at an application level.

Обратите внимание, что при развертывании на [Apache using mod_wsgi](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html) заголовок авторизации по умолчанию не передается приложению WSGI, так как предполагается, что аутентификация будет обрабатываться Apache, а не на уровне приложения.

If you are deploying to Apache, and using any non-session based authentication, you will need to explicitly configure mod_wsgi to pass the required headers through to the application.  This can be done by specifying the `WSGIPassAuthorization` directive in the appropriate context and setting it to `'On'`.

Если вы развертываете на Apache и используете любую аутентификацию, не основанную на сеансах, вам необходимо явно настроить mod_wsgi для передачи необходимых заголовков приложению.  Это можно сделать, указав директиву `WSGIPassAuthorization` в соответствующем контексте и установив ее в значение `'On'`.

```
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On
```

---

# API Reference

# API Reference

## BasicAuthentication

## BasicAuthentication

This authentication scheme uses [HTTP Basic Authentication](https://tools.ietf.org/html/rfc2617), signed against a user's username and password.  Basic authentication is generally only appropriate for testing.

Эта схема аутентификации использует [HTTP Basic Authentication](https://tools.ietf.org/html/rfc2617), подписанную против имени пользователя и пароля.  Базовая аутентификация обычно подходит только для тестирования.

If successfully authenticated, `BasicAuthentication` provides the following credentials.

При успешной аутентификации `BasicAuthentication` предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Unauthenticated responses that are denied permission will result in an `HTTP 401 Unauthorized` response with an appropriate WWW-Authenticate header.  For example:

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком WWW-Authenticate.  Например:

```
WWW-Authenticate: Basic realm="api"
```

**Note:** If you use `BasicAuthentication` in production you must ensure that your API is only available over `https`.  You should also ensure that your API clients will always re-request the username and password at login, and will never store those details to persistent storage.

**Примечание:** Если вы используете `BasicAuthentication` в производстве, вы должны убедиться, что ваш API доступен только через `https`.  Вы также должны убедиться, что клиенты вашего API всегда будут повторно запрашивать имя пользователя и пароль при входе в систему и никогда не будут сохранять эти данные в постоянном хранилище.

## TokenAuthentication

## TokenAuthentication

---

**Note:** The token authentication provided by Django REST framework is a fairly simple implementation.

**Примечание:** Аутентификация с помощью токенов, предоставляемая REST-фреймворком Django, является довольно простой реализацией.

For an implementation which allows more than one token per user, has some tighter security implementation details, and supports token expiry, please see the [Django REST Knox](https://github.com/James1345/django-rest-knox) third party package.

Для реализации, которая позволяет использовать более одного токена на пользователя, имеет некоторые более жесткие детали реализации безопасности и поддерживает истечение срока действия токена, пожалуйста, обратитесь к стороннему пакету [Django REST Knox](https://github.com/James1345/django-rest-knox).

---

This authentication scheme uses a simple token-based HTTP Authentication scheme.  Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.

Эта схема аутентификации использует простую схему аутентификации HTTP на основе маркеров.  Токен-аутентификация подходит для клиент-серверных установок, таких как собственные настольные и мобильные клиенты.

To use the `TokenAuthentication` scheme you'll need to [configure the authentication classes](#setting-the-authentication-scheme) to include `TokenAuthentication`, and additionally include `rest_framework.authtoken` in your `INSTALLED_APPS` setting:

Для использования схемы `TokenAuthentication` вам необходимо [настроить классы аутентификации] (#setting-the-authentication-scheme), чтобы включить `TokenAuthentication`, и дополнительно включить `rest_framework.authtoken` в настройку `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

Make sure to run `manage.py migrate` after changing your settings.

Обязательно запустите `manage.py migrate` после изменения настроек.

The `rest_framework.authtoken` app provides Django database migrations.

Приложение `rest_framework.authtoken` обеспечивает миграцию баз данных Django.

You'll also need to create tokens for your users.

Вам также потребуется создать маркеры для своих пользователей.

```
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

For clients to authenticate, the token key should be included in the `Authorization` HTTP header.  The key should be prefixed by the string literal "Token", with whitespace separating the two strings.  For example:

Для аутентификации клиентов ключ токена должен быть включен в HTTP-заголовок `Authorization`.  Ключ должен иметь префикс в виде строкового литерала "Token", с пробелами, разделяющими эти две строки.  Например:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

_If you want to use a different keyword in the header, such as `Bearer`, simply subclass `TokenAuthentication` and set the `keyword` class variable._

*Если вы хотите использовать другое ключевое слово в заголовке, например `Bearer`, просто подкласс `TokenAuthentication` и установите переменную класса `keyword`.

If successfully authenticated, `TokenAuthentication` provides the following credentials.

При успешной аутентификации `TokenAuthentication` предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be a `rest_framework.authtoken.models.Token` instance.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет экземпляром `rest_framework.authtoken.models.Token`.

Unauthenticated responses that are denied permission will result in an `HTTP 401 Unauthorized` response with an appropriate WWW-Authenticate header.  For example:

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком WWW-Authenticate.  Например:

```
WWW-Authenticate: Token
```

The `curl` command line tool may be useful for testing token authenticated APIs.  For example:

Инструмент командной строки `curl` может быть полезен для тестирования API с аутентификацией токенов.  Например:

```
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

---

**Note:** If you use `TokenAuthentication` in production you must ensure that your API is only available over `https`.

**Примечание:** Если вы используете `TokenAuthentication` в производстве, вы должны убедиться, что ваш API доступен только через `https`.

---

### Generating Tokens

### Генерация токенов

#### By using signals

#### С помощью сигналов

If you want every user to have an automatically generated Token, you can simply catch the User's `post_save` signal.

Если вы хотите, чтобы у каждого пользователя был автоматически сгенерированный токен, вы можете просто перехватить сигнал `post_save` пользователя.

```
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

Note that you'll want to ensure you place this code snippet in an installed `models.py` module, or some other location that will be imported by Django on startup.

Обратите внимание, что вам нужно убедиться, что вы поместили этот фрагмент кода в установленный модуль `models.py` или в другое место, которое будет импортироваться Django при запуске.

If you've already created some users, you can generate tokens for all existing users like this:

Если вы уже создали несколько пользователей, вы можете сгенерировать токены для всех существующих пользователей следующим образом:

```
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

#### By exposing an api endpoint

#### Посредством раскрытия конечной точки api

When using `TokenAuthentication`, you may want to provide a mechanism for clients to obtain a token given the username and password.  REST framework provides a built-in view to provide this behavior.  To use it, add the `obtain_auth_token` view to your URLconf:

При использовании `TokenAuthentication` вы можете захотеть предоставить клиентам механизм для получения токена, заданного именем пользователя и паролем.  Фреймворк REST предоставляет встроенное представление для обеспечения такого поведения.  Чтобы использовать его, добавьте представление `obtain_auth_token` в URLconf:

```
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
```

Note that the URL part of the pattern can be whatever you want to use.

Обратите внимание, что URL часть шаблона может быть любой, которую вы хотите использовать.

The `obtain_auth_token` view will return a JSON response when valid `username` and `password` fields are POSTed to the view using form data or JSON:

Представление `obtain_auth_token` вернет ответ в формате JSON, когда действительные поля `имя пользователя` и `пароль` будут отправлены в представление с помощью данных формы или JSON:

```
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Note that the default `obtain_auth_token` view explicitly uses JSON requests and responses, rather than using default renderer and parser classes in your settings.

Обратите внимание, что представление по умолчанию `obtain_auth_token` явно использует JSON запросы и ответы, а не использует классы рендерера и парсера по умолчанию в ваших настройках.

By default, there are no permissions or throttling applied to the `obtain_auth_token` view. If you do wish to apply throttling you'll need to override the view class,
and include them using the `throttle_classes` attribute.

По умолчанию к представлению `obtain_auth_token` не применяется никаких разрешений или дросселирования. Если вы хотите применить дросселирование, вам нужно переопределить класс представления,
и включить их с помощью атрибута `throttle_classes`.

If you need a customized version of the `obtain_auth_token` view, you can do so by subclassing the `ObtainAuthToken` view class, and using that in your url conf instead.

Если вам нужна настраиваемая версия представления `obtain_auth_token`, вы можете сделать это, создав подкласс класса представления `ObtainAuthToken` и используя его в url conf.

For example, you may return additional user information beyond the `token` value:

Например, вы можете возвращать дополнительную информацию о пользователе помимо значения `token`:

```
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
```

And in your `urls.py`:

И в вашем `urls.py`:

```
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
```

#### With Django admin

#### С администратором Django

It is also possible to create Tokens manually through the admin interface. In case you are using a large user base, we recommend that you monkey patch the `TokenAdmin` class to customize it to your needs, more specifically by declaring the `user` field as `raw_field`.

Токены также можно создавать вручную через интерфейс администратора. В случае, если вы используете большую базу пользователей, мы рекомендуем вам внести обезьяньи исправления в класс `TokenAdmin`, чтобы настроить его под свои нужды, в частности, объявив поле `user` как `raw_field`.

`your_app/admin.py`:

`ваше_приложение/admin.py`:

```
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

#### Using Django manage.py command

#### Использование команды Django manage.py

Since version 3.6.4 it's possible to generate a user token using the following command:

Начиная с версии 3.6.4 можно сгенерировать пользовательский токен с помощью следующей команды:

```
./manage.py drf_create_token <username>
```

this command will return the API token for the given user, creating it if it doesn't exist:

эта команда вернет API-токен для данного пользователя, создав его, если он не существует:

```
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

In case you want to regenerate the token (for example if it has been compromised or leaked) you can pass an additional parameter:

Если вы хотите восстановить токен (например, если он был скомпрометирован или произошла утечка), вы можете передать дополнительный параметр:

```
./manage.py drf_create_token -r <username>
```

## SessionAuthentication

## SessionAuthentication

This authentication scheme uses Django's default session backend for authentication.  Session authentication is appropriate for AJAX clients that are running in the same session context as your website.

Эта схема аутентификации использует бэкенд сессий Django по умолчанию для аутентификации.  Сеансовая аутентификация подходит для клиентов AJAX, которые работают в том же сеансовом контексте, что и ваш сайт.

If successfully authenticated, `SessionAuthentication` provides the following credentials.

При успешной аутентификации `SessionAuthentication` предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Unauthenticated responses that are denied permission will result in an `HTTP 403 Forbidden` response.

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 403 Forbidden`.

If you're using an AJAX-style API with SessionAuthentication, you'll need to make sure you include a valid CSRF token for any "unsafe" HTTP method calls, such as `PUT`, `PATCH`, `POST` or `DELETE` requests.  See the [Django CSRF documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax) for more details.

Если вы используете API в стиле AJAX с SessionAuthentication, вам нужно убедиться, что вы включаете действительный CSRF токен для любых "небезопасных" вызовов HTTP методов, таких как `PUT`, `PATCH`, `POST` или `DELETE` запросы.  Более подробную информацию смотрите в [Django CSRF documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

**Warning**: Always use Django's standard login view when creating login pages. This will ensure your login views are properly protected.

**Предупреждение**: Всегда используйте стандартное представление входа Django при создании страниц входа. Это обеспечит надлежащую защиту ваших представлений входа.

CSRF validation in REST framework works slightly differently from standard Django due to the need to support both session and non-session based authentication to the same views. This means that only authenticated requests require CSRF tokens, and anonymous requests may be sent without CSRF tokens. This behavior is not suitable for login views, which should always have CSRF validation applied.

Проверка CSRF в REST-фреймворке работает несколько иначе, чем в стандартном Django, из-за необходимости поддерживать как сеансовую, так и несеансовую аутентификацию для одних и тех же представлений. Это означает, что только аутентифицированные запросы требуют CSRF-токенов, а анонимные запросы могут быть отправлены без CSRF-токенов. Такое поведение не подходит для представлений входа в систему, к которым всегда должна применяться проверка CSRF.

## RemoteUserAuthentication

## RemoteUserAuthentication

This authentication scheme allows you to delegate authentication to your web server, which sets the `REMOTE_USER`
environment variable.

Эта схема аутентификации позволяет вам делегировать аутентификацию вашему веб-серверу, который устанавливает `REMOTE_USER`.
переменную окружения.

To use it, you must have `django.contrib.auth.backends.RemoteUserBackend` (or a subclass) in your
`AUTHENTICATION_BACKENDS` setting. By default, `RemoteUserBackend` creates `User` objects for usernames that don't
already exist. To change this and other behavior, consult the
[Django documentation](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

Чтобы использовать его, вы должны иметь `django.contrib.auth.backends.RemoteUserBackend` (или его подкласс) в настройке
`AUTHENTICATION_BACKENDS`. По умолчанию `RemoteUserBackend` создает объекты `User` для имен пользователей, которые не
уже существуют. Чтобы изменить это и другое поведение, обратитесь к
[Django documentation](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

If successfully authenticated, `RemoteUserAuthentication` provides the following credentials:

При успешной аутентификации `RemoteUserAuthentication` предоставляет следующие учетные данные:

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Consult your web server's documentation for information about configuring an authentication method, for example:

Обратитесь к документации вашего веб-сервера за информацией о настройке метода аутентификации, например:

* [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
* [NGINX (Restricting Access)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

* [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
* [NGINX (ограничение доступа)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

# Custom authentication

# Пользовательская аутентификация

To implement a custom authentication scheme, subclass `BaseAuthentication` and override the `.authenticate(self, request)` method.  The method should return a two-tuple of `(user, auth)` if authentication succeeds, or `None` otherwise.

Чтобы реализовать собственную схему аутентификации, подкласс `BaseAuthentication` и переопределите метод `.authenticate(self, request)`.  Метод должен возвращать кортеж `(user, auth)`, если аутентификация прошла успешно, или `None` в противном случае.

In some circumstances instead of returning `None`, you may want to raise an `AuthenticationFailed` exception from the `.authenticate()` method.

В некоторых случаях вместо возврата `None` вы можете захотеть вызвать исключение `AuthenticationFailed` из метода `.authenticate()`.

Typically the approach you should take is:

Как правило, вам следует придерживаться следующего подхода:

* If authentication is not attempted, return `None`.  Any other authentication schemes also in use will still be checked.
* If authentication is attempted but fails, raise an `AuthenticationFailed` exception.  An error response will be returned immediately, regardless of any permissions checks, and without checking any other authentication schemes.

* Если попытка аутентификации не была предпринята, верните `None`.  Любые другие схемы аутентификации, которые также используются, будут проверены.
* Если попытка аутентификации была предпринята, но не удалась, вызовите исключение `AuthenticationFailed`.  Ответ об ошибке будет возвращен немедленно, независимо от любых проверок разрешений и без проверки других схем аутентификации.

You _may_ also override the `.authenticate_header(self, request)` method.  If implemented, it should return a string that will be used as the value of the `WWW-Authenticate` header in a `HTTP 401 Unauthorized` response.

Вы *можете* также переопределить метод `.authenticate_header(self, request)`.  Если он реализован, он должен возвращать строку, которая будет использоваться в качестве значения заголовка `WWW-Authenticate` в ответе `HTTP 401 Unauthorized`.

If the `.authenticate_header()` method is not overridden, the authentication scheme will return `HTTP 403 Forbidden` responses when an unauthenticated request is denied access.

Если метод `.authenticate_header()` не переопределен, схема аутентификации будет возвращать ответы `HTTP 403 Forbidden`, когда неаутентифицированному запросу будет отказано в доступе.

---

**Note:** When your custom authenticator is invoked by the request object's `.user` or `.auth` properties, you may see an `AttributeError` re-raised as a `WrappedAttributeError`. This is necessary to prevent the original exception from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from your custom authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. These errors should be fixed or otherwise handled by your authenticator.

**Примечание:** Когда ваш пользовательский аутентификатор вызывается свойствами `.user` или `.auth` объекта запроса, вы можете увидеть, как `AttributeError` перефразируется в `WrappedAttributeError`. Это необходимо для того, чтобы исходное исключение не было подавлено доступом к внешнему свойству. Python не распознает, что `AttributeError` исходит от вашего пользовательского аутентификатора, и вместо этого будет считать, что объект запроса не имеет свойства `.user` или `.auth`. Эти ошибки должны быть исправлены или иным образом обработаны вашим аутентификатором.

---

## Example

## Пример

The following example will authenticate any incoming request as the user given by the username in a custom request header named 'X-USERNAME'.

Следующий пример аутентифицирует любой входящий запрос как пользователя, указанного в имени пользователя в пользовательском заголовке запроса 'X-USERNAME'.

```
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
```

---

# Third party packages

# Пакеты сторонних производителей

The following third-party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## django-rest-knox

## django-rest-knox

[Django-rest-knox](https://github.com/James1345/django-rest-knox) library provides models and views to handle token-based authentication in a more secure and extensible way than the built-in TokenAuthentication scheme - with Single Page Applications and Mobile clients in mind. It provides per-client tokens, and views to generate them when provided some other authentication (usually basic authentication), to delete the token (providing a server enforced logout) and to delete all tokens (logs out all clients that a user is logged into).

Библиотека [Django-rest-knox](https://github.com/James1345/django-rest-knox) предоставляет модели и представления для обработки аутентификации на основе токенов более безопасным и расширяемым способом, чем встроенная схема TokenAuthentication - с учетом одностраничных приложений и мобильных клиентов. Она предоставляет токены для каждого клиента, а также представления для их генерации при предоставлении другой аутентификации (обычно базовой), для удаления токена (обеспечивая принудительный выход с сервера) и для удаления всех токенов (выход из всех клиентов, в которые вошел пользователь).

## Django OAuth Toolkit

## Django OAuth Toolkit

The [Django OAuth Toolkit](https://github.com/evonove/django-oauth-toolkit) package provides OAuth 2.0 support and works with Python 3.4+. The package is maintained by [jazzband](https://github.com/jazzband/) and uses the excellent [OAuthLib](https://github.com/idan/oauthlib).  The package is well documented, and well supported and is currently our **recommended package for OAuth 2.0 support**.

Пакет [Django OAuth Toolkit](https://github.com/evonove/django-oauth-toolkit) обеспечивает поддержку OAuth 2.0 и работает с Python 3.4+. Пакет поддерживается [jazzband](https://github.com/jazzband/) и использует превосходный [OAuthLib](https://github.com/idan/oauthlib).  Пакет хорошо документирован, хорошо поддерживается и в настоящее время является нашим **рекомендованным пакетом для поддержки OAuth 2.0**.

### Installation & configuration

### Установка и настройка

Install using `pip`.

Установите с помощью `pip`.

```
pip install django-oauth-toolkit
```

Add the package to your `INSTALLED_APPS` and modify your REST framework settings.

Добавьте пакет в `INSTALLED_APPS` и измените настройки фреймворка REST.

```
INSTALLED_APPS = [
    ...
    'oauth2_provider',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}
```

For more details see the [Django REST framework - Getting started](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html) documentation.

Более подробную информацию можно найти в документации [Django REST framework - Getting started](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html).

## Django REST framework OAuth

## Django REST framework OAuth

The [Django REST framework OAuth](https://jpadilla.github.io/django-rest-framework-oauth/) package provides both OAuth1 and OAuth2 support for REST framework.

Пакет [Django REST framework OAuth](https://jpadilla.github.io/django-rest-framework-oauth/) обеспечивает поддержку OAuth1 и OAuth2 для REST-фреймворка.

This package was previously included directly in the REST framework but is now supported and maintained as a third-party package.

Ранее этот пакет был включен непосредственно в REST framework, но теперь поддерживается и сопровождается как пакет стороннего разработчика.

### Installation & configuration

### Установка и настройка

Install the package using `pip`.

Установите пакет с помощью `pip`.

```
pip install djangorestframework-oauth
```

For details on configuration and usage see the Django REST framework OAuth documentation for [authentication](https://jpadilla.github.io/django-rest-framework-oauth/authentication/) and [permissions](https://jpadilla.github.io/django-rest-framework-oauth/permissions/).

Подробнее о настройке и использовании смотрите документацию по OAuth фреймворку Django REST для [authentication](https://jpadilla.github.io/django-rest-framework-oauth/authentication/) и [permissions](https://jpadilla.github.io/django-rest-framework-oauth/permissions/).

## JSON Web Token Authentication

## JSON Web Token Authentication

JSON Web Token is a fairly new standard which can be used for token-based authentication. Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) which provides some features as well as a pluggable token blacklist app.

JSON Web Token - это довольно новый стандарт, который можно использовать для аутентификации на основе токенов. В отличие от встроенной схемы TokenAuthentication, аутентификация JWT не требует использования базы данных для проверки токена. Пакет для JWT-аутентификации - [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt), который предоставляет некоторые возможности, а также подключаемое приложение черного списка токенов.

## Hawk HTTP Authentication

## Аутентификация Hawk HTTP

The [HawkREST](https://hawkrest.readthedocs.io/en/latest/) library builds on the [Mohawk](https://mohawk.readthedocs.io/en/latest/) library to let you work with [Hawk](https://github.com/hueniverse/hawk) signed requests and responses in your API. [Hawk](https://github.com/hueniverse/hawk) lets two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication](https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05) (which was based on parts of [OAuth 1.0](https://oauth.net/core/1.0a/)).

Библиотека [HawkREST](https://hawkrest.readthedocs.io/en/latest/) основана на библиотеке [Mohawk](https://mohawk.readthedocs.io/en/latest/) и позволяет вам работать с подписанными запросами и ответами [Hawk](https://github.com/hueniverse/hawk) в вашем API. [Hawk](https://github.com/hueniverse/hawk) позволяет двум сторонам безопасно общаться друг с другом, используя сообщения, подписанные общим ключом. Она основана на [HTTP MAC аутентификации доступа](https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05) (которая была основана на части [OAuth 1.0](https://oauth.net/core/1.0a/)).

## HTTP Signature Authentication

## Аутентификация подписи HTTP

HTTP Signature (currently a [IETF draft](https://datatracker.ietf.org/doc/draft-cavage-http-signatures/)) provides a way to achieve origin authentication and message integrity for HTTP messages. Similar to [Amazon's HTTP Signature scheme](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), used by many of its services, it permits stateless, per-request authentication. [Elvio Toccalino](https://github.com/etoccalino/) maintains the [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) (outdated) package which provides an easy-to-use HTTP Signature Authentication mechanism. You can use the updated fork version of [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature), which is [drf-httpsig](https://github.com/ahknight/drf-httpsig).

HTTP Signature (в настоящее время [проект IETF](https://datatracker.ietf.org/doc/draft-cavage-http-signatures/)) предоставляет способ достижения аутентификации происхождения и целостности сообщений HTTP. Подобно схеме [Amazon's HTTP Signature scheme](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), используемой многими сервисами компании, она допускает безэталонную аутентификацию по каждому запросу. [Elvio Toccalino](https://github.com/etoccalino/) поддерживает пакет [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) (устаревший), который предоставляет простой в использовании механизм аутентификации HTTP Signature. Вы можете использовать обновленную форковую версию [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature), которой является [drf-httpsig](https://github.com/ahknight/drf-httpsig).

## Djoser

## Джосер

[Djoser](https://github.com/sunscrapers/djoser) library provides a set of views to handle basic actions such as registration, login, logout, password reset and account activation. The package works with a custom user model and uses token-based authentication. This is a ready to use REST implementation of the Django authentication system.

[Djoser](https://github.com/sunscrapers/djoser) библиотека предоставляет набор представлений для обработки основных действий, таких как регистрация, вход в систему, выход из системы, сброс пароля и активация учетной записи. Пакет работает с пользовательской моделью пользователя и использует аутентификацию на основе токенов. Это готовая к использованию REST-реализация системы аутентификации Django.

## django-rest-auth / dj-rest-auth

## django-rest-auth / dj-rest-auth

This library provides a set of REST API endpoints for registration, authentication (including social media authentication), password reset, retrieve and update user details, etc. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for user management.

Эта библиотека предоставляет набор конечных точек REST API для регистрации, аутентификации (включая аутентификацию в социальных сетях), сброса пароля, получения и обновления данных пользователя и т.д. Имея эти конечные точки API, ваши клиентские приложения, такие как AngularJS, iOS, Android и другие, могут самостоятельно общаться с вашим бэкенд-сайтом Django через REST API для управления пользователями.

There are currently two forks of this project.

В настоящее время существует два форка этого проекта.

* [Django-rest-auth](https://github.com/Tivix/django-rest-auth) is the original project, [but is not currently receiving updates](https://github.com/Tivix/django-rest-auth/issues/568).
* [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth) is a newer fork of the project.

* [Django-rest-auth](https://github.com/Tivix/django-rest-auth) - оригинальный проект, [но в настоящее время не получает обновлений](https://github.com/Tivix/django-rest-auth/issues/568).
* [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth) - более новый форк проекта.

## drf-social-oauth2

## drf-social-oauth2

[Drf-social-oauth2](https://github.com/wagnerdelima/drf-social-oauth2) is a framework that helps you authenticate with major social oauth2 vendors, such as Facebook, Google, Twitter, Orcid, etc. It generates tokens in a JWTed way with an easy setup.

[Drf-social-oauth2](https://github.com/wagnerdelima/drf-social-oauth2) - это фреймворк, который поможет вам аутентифицироваться у основных поставщиков социального oauth2, таких как Facebook, Google, Twitter, Orcid и др. Он генерирует токены в виде JWT с простой настройкой.

## drfpasswordless

## drfpasswordless

[drfpasswordless](https://github.com/aaronn/django-rest-framework-passwordless) adds (Medium, Square Cash inspired) passwordless support to Django REST Framework's TokenAuthentication scheme. Users log in and sign up with a token sent to a contact point like an email address or a mobile number.

[drfpasswordless](https://github.com/aaronn/django-rest-framework-passwordless) добавляет (по мотивам Medium, Square Cash) поддержку беспарольного входа в схему TokenAuthentication платформы Django REST Framework. Пользователи входят в систему и регистрируются с помощью токена, отправленного на контактную точку, например, адрес электронной почты или номер мобильного телефона.

## django-rest-authemail

## django-rest-authemail

[django-rest-authemail](https://github.com/celiao/django-rest-authemail) provides a RESTful API interface for user signup and authentication. Email addresses are used for authentication, rather than usernames.  API endpoints are available for signup, signup email verification, login, logout, password reset, password reset verification, email change, email change verification, password change, and user detail.  A fully functional example project and detailed instructions are included.

[django-rest-authemail](https://github.com/celiao/django-rest-authemail) предоставляет RESTful API интерфейс для регистрации и аутентификации пользователей. Для аутентификации используются адреса электронной почты, а не имена пользователей.  Доступны конечные точки API для регистрации, проверки электронной почты при регистрации, входа в систему, выхода из системы, сброса пароля, проверки сброса пароля, изменения электронной почты, проверки изменения электронной почты, изменения пароля и детализации пользователя.  Полностью функциональный пример проекта и подробные инструкции прилагаются.

## Django-Rest-Durin

## Django-Rest-Durin

[Django-Rest-Durin](https://github.com/eshaan7/django-rest-durin) is built with the idea to have one library that does token auth for multiple Web/CLI/Mobile API clients via one interface but allows different token configuration for each API Client that consumes the API. It provides support for multiple tokens per user via custom models, views, permissions that work with Django-Rest-Framework. The token expiration time can be different per API client and is customizable via the Django Admin Interface.

[Django-Rest-Durin](https://github.com/eshaan7/django-rest-durin) создана с идеей иметь одну библиотеку, которая делает аутентификацию токенов для нескольких Web/CLI/Mobile API клиентов через один интерфейс, но позволяет различную конфигурацию токенов для каждого API клиента, который потребляет API. Она обеспечивает поддержку нескольких токенов для каждого пользователя через пользовательские модели, представления, разрешения, которые работают с Django-Rest-Framework. Время истечения срока действия токена может быть разным для каждого API-клиента и настраивается через интерфейс администратора Django.

More information can be found in the [Documentation](https://django-rest-durin.readthedocs.io/en/latest/index.html).

Более подробную информацию можно найти в [Документации](https://django-rest-durin.readthedocs.io/en/latest/index.html).