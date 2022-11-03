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
> — Джейкоб Каплан-Мосс, [«Худшие практики REST»] (https://jacobian.org/writing/rest-worst-practices/)

Authentication is the mechanism of associating an incoming request with a set of identifying credentials, such as the user the request came from, or the token that it was signed with.  The [permission](permissions.md) and [throttling](throttling.md) policies can then use those credentials to determine if the request should be permitted.

Проверка подлинности — это механизм связывания входящего запроса с набором идентифицирующих учетных данных, таких как пользователь, от которого пришел запрос, или маркер, с помощью которого он был подписан.  Политики [permission](permissions.md) и [throttling](throttling.md) могут затем использовать эти учетные данные, чтобы определить, следует ли разрешить запрос.

REST framework provides several authentication schemes out of the box, and also allows you to implement custom schemes.

REST framework предоставляет несколько схем проверки подлинности из коробки, а также позволяет реализовывать пользовательские схемы.

Authentication always runs at the very start of the view, before the permission and throttling checks occur, and before any other code is allowed to proceed.

Проверка подлинности всегда выполняется в самом начале представления, до того, как произойдут проверки разрешений и регулирования, а также до того, как будет разрешено выполнение любого другого кода.

The `request.user` property will typically be set to an instance of the `contrib.auth` package's `User` class.

Свойству 'request.user' обычно присваивается экземпляр класса 'User' пакета 'contrib.auth'.

The `request.auth` property is used for any additional authentication information, for example, it may be used to represent an authentication token that the request was signed with.

Свойство 'request.auth' используется для любых дополнительных сведений о проверке подлинности, например, оно может использоваться для представления маркера проверки подлинности, которым был подписан запрос.

---

**Note:** Don't forget that **authentication by itself won't allow or disallow an incoming request**, it simply identifies the credentials that the request was made with.

**Примечание:** Не забывайте, что **аутентификация сама по себе не разрешает или запрещает входящий запрос**, она просто идентифицирует учетные данные, с которыми был сделан запрос.

For information on how to set up the permission policies for your API please see the [permissions documentation](permissions.md).

Сведения о настройке политик разрешений для API см. в разделе [документация по разрешениям](permissions.md).

---

## How authentication is determined

## Как определяется проверка подлинности

The authentication schemes are always defined as a list of classes.  REST framework will attempt to authenticate with each class in the list, and will set `request.user` and `request.auth` using the return value of the first class that successfully authenticates.

Схемы проверки подлинности всегда определяются как список классов.  Платформа REST попытается аутентифицироваться с каждым классом в списке и установит 'request.user' и 'request.auth', используя возвращаемое значение первого класса, который успешно аутентифицируется.

If no class authenticates, `request.user` will be set to an instance of `django.contrib.auth.models.AnonymousUser`, and `request.auth` will be set to `None`.

Если класс не аутентифицируется, для параметра 'request.user' будет установлен экземпляр 'django.contrib.auth.models.AnonymousUser', а для 'request.auth' будет установлено значение 'None'.

The value of `request.user` and `request.auth` for unauthenticated requests can be modified using the `UNAUTHENTICATED_USER` and `UNAUTHENTICATED_TOKEN` settings.

Значение 'request.user' и 'request.auth' для запросов, не прошедших проверку подлинности, можно изменить с помощью настроек 'UNAUTHENTICATED_USER' и 'UNAUTHENTICATED_TOKEN'.

## Setting the authentication scheme

## Настройка схемы проверки подлинности

The default authentication schemes may be set globally, using the `DEFAULT_AUTHENTICATION_CLASSES` setting.  For example.

Схемы аутентификации по умолчанию могут быть установлены глобально, используя параметр «DEFAULT_AUTHENTICATION_CLASSES».  Например.

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

Можно также задать схему проверки подлинности для каждого представления или набора представлений.
с использованием представлений на основе классов 'APIView'.

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

Или, если вы используете декоратор «@api_view» с функциональными представлениями.

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

## Несанкционированные и запрещенные ответы

When an unauthenticated request is denied permission there are two different error codes that may be appropriate.

Если запросу, не прошедшему проверку подлинности, отказано в разрешении, могут потребоваться два разных кода ошибки.

* [HTTP 401 Unauthorized](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
* [HTTP 403 Permission Denied](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

* [HTTP 401 Неавторизованный](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
* [Отказано в разрешении HTTP 403](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

HTTP 401 responses must always include a `WWW-Authenticate` header, that instructs the client how to authenticate.  HTTP 403 responses do not include the `WWW-Authenticate` header.

Ответы HTTP 401 всегда должны содержать заголовок 'WWW-Authenticate', который инструктирует клиента о том, как аутентифицироваться.  Ответы HTTP 403 не содержат заголовка 'WWW-Authenticate'.

The kind of response that will be used depends on the authentication scheme.  Although multiple authentication schemes may be in use, only one scheme may be used to determine the type of response.  **The first authentication class set on the view is used when determining the type of response**.

Тип ответа, который будет использоваться, зависит от схемы проверки подлинности.  Хотя может использоваться несколько схем проверки подлинности, для определения типа ответа может использоваться только одна схема.  **Первый класс аутентификации, заданный в представлении, используется при определении типа ответа**.

Note that when a request may successfully authenticate, but still be denied permission to perform the request, in which case a `403 Permission Denied` response will always be used, regardless of the authentication scheme.

Обратите внимание, что когда запрос может успешно аутентифицировать, но все же будет отказано в разрешении на выполнение запроса, и в этом случае ответ «403 разрешение отказано» всегда будет использоваться, независимо от схемы аутентификации.

## Apache mod_wsgi specific configuration

## Apache MOD_WSGI Специальная конфигурация

Note that if deploying to [Apache using mod_wsgi](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html), the authorization header is not passed through to a WSGI application by default, as it is assumed that authentication will be handled by Apache, rather than at an application level.

Обратите внимание, что при развертывании в [apache с использованием mod_wsgi] (https://modwsgi.readthedocs.io/en/develop/configuration-directives/wsgipassauthorization.html), заголовок авторизации не передается в приложение WSGI по умолчанию, как это, как это
предполагается, что аутентификация будет обрабатываться Apache, а не на уровне приложения.

If you are deploying to Apache, and using any non-session based authentication, you will need to explicitly configure mod_wsgi to pass the required headers through to the application.  This can be done by specifying the `WSGIPassAuthorization` directive in the appropriate context and setting it to `'On'`.

Если вы развернете в Apache и используете какую-либо не сессию аутентификацию, вам необходимо будет явно настроить MOD_WSGI, чтобы передать необходимые заголовки в приложение.
Это может быть сделано путем указания директивы `wsgipassauthorization` в соответствующем контексте и установив ее на« на ».

```
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On
```

---

# API Reference

# Ссылка на API

## BasicAuthentication

## Basicauthentication

This authentication scheme uses [HTTP Basic Authentication](https://tools.ietf.org/html/rfc2617), signed against a user's username and password.  Basic authentication is generally only appropriate for testing.

В этой схеме аутентификации используется [http basic аутентификация] (https://tools.ietf.org/html/rfc2617), подписанная против имени пользователя и пароля пользователя.
Основная аутентификация, как правило, подходит только для тестирования.

If successfully authenticated, `BasicAuthentication` provides the following credentials.

Если успешно аутентифицируется, «Basicauthentication» предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляр Django` user '.
* `request.auth` будет« нет ».

Unauthenticated responses that are denied permission will result in an `HTTP 401 Unauthorized` response with an appropriate WWW-Authenticate header.  For example:

Несанкционированные ответы, которые будут отказаны в разрешении, приведут к ответам `http 401 unaultorized` с соответствующим заголовком www-authentitic.
Например:

```
WWW-Authenticate: Basic realm="api"
```

**Note:** If you use `BasicAuthentication` in production you must ensure that your API is only available over `https`.  You should also ensure that your API clients will always re-request the username and password at login, and will never store those details to persistent storage.

** ПРИМЕЧАНИЕ: ** Если вы используете `basicauthentication` в производстве, вы должны убедиться, что ваш API доступен только для` https`.
Вы также должны убедиться, что ваши клиенты API всегда будут пересматривать имя пользователя и пароль в Login, и никогда не сохранят эти данные для постоянного хранения.

## TokenAuthentication

## tokenauthentication

---

**Note:** The token authentication provided by Django REST framework is a fairly simple implementation.

** ПРИМЕЧАНИЕ: ** Аутентификация токена, предоставленная Django Rest Framework, является довольно простой реализацией.

For an implementation which allows more than one token per user, has some tighter security implementation details, and supports token expiry, please see the [Django REST Knox](https://github.com/James1345/django-rest-knox) third party package.

Для реализации, которая позволяет более одного токена на одного пользователя, имеет некоторые более жесткие детали реализации безопасности и поддерживает срок действия токена, см.
Партийный пакет.

---

This authentication scheme uses a simple token-based HTTP Authentication scheme.  Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.

Эта схема аутентификации использует простую схему аутентификации HTTP на основе токенов.
Аутентификация токена подходит для настройки клиентских серверов, таких как натуральные настольные и мобильные клиенты.

To use the `TokenAuthentication` scheme you'll need to [configure the authentication classes](#setting-the-authentication-scheme) to include `TokenAuthentication`, and additionally include `rest_framework.authtoken` in your `INSTALLED_APPS` setting:

Чтобы использовать схему `tokenauthentication`, которая вам нужно [настраивать классы аутентификации] (#Настройка Authentication-Scheme), чтобы включить` tokenauthentication` и дополнительно включите `rest_framework.authtoken` в свою настройку` stasted_apps`:

```
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

Make sure to run `manage.py migrate` after changing your settings.

Обязательно запустите `Manage.py Migrate` после изменения ваших настроек.

The `rest_framework.authtoken` app provides Django database migrations.

Приложение `rest_framework.authtoken`s предоставляет миграции базы данных Django.

You'll also need to create tokens for your users.

Вам также нужно создать токены для ваших пользователей.

```
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

For clients to authenticate, the token key should be included in the `Authorization` HTTP header.  The key should be prefixed by the string literal "Token", with whitespace separating the two strings.  For example:

Для клиентов для аутентификации ключ токена должен быть включен в заголовок HTTP «Авторизация».
Ключ должен быть префикс строк, буквального «токена», с пробелом, разделяющим две строки.
Например:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

*If you want to use a different keyword in the header, such as `Bearer`, simply subclass `TokenAuthentication` and set the `keyword` class variable.*

*Если вы хотите использовать другое ключевое слово в заголовке, например, «Bearer», просто подкласс `tokenauthentication` и установите переменную класса ключевого слова.**

If successfully authenticated, `TokenAuthentication` provides the following credentials.

Если успешно аутентифицируется, «Tokenauthentication» предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be a `rest_framework.authtoken.models.Token` instance.

* `request.user` будет экземпляр Django` user '.
* `request.auth` будет экземпляр` rest_framework.authtoken.models.token`.

Unauthenticated responses that are denied permission will result in an `HTTP 401 Unauthorized` response with an appropriate WWW-Authenticate header.  For example:

Несанкционированные ответы, которые будут отказаны в разрешении, приведут к ответам `http 401 unaultorized` с соответствующим заголовком www-authentitic.
Например:

```
WWW-Authenticate: Token
```

The `curl` command line tool may be useful for testing token authenticated APIs.  For example:

Инструмент командной строки `curl` может быть полезен для тестирования API -интерфейсов токена.
Например:

```
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

---

**Note:** If you use `TokenAuthentication` in production you must ensure that your API is only available over `https`.

** ПРИМЕЧАНИЕ: ** Если вы используете `tokenauthentication` в производстве, вы должны убедиться, что ваш API доступен только для` https`.

---

### Generating Tokens

### Генерация токенов

#### By using signals

#### с помощью сигналов

If you want every user to have an automatically generated Token, you can simply catch the User's `post_save` signal.

Если вы хотите, чтобы у каждого пользователя был автоматически сгенерированный токен, вы можете просто поймать сигнал пользователя `post_save`.

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

Обратите внимание, что вы захотите убедиться, что вы разместите этот фрагмент кода в установленном модуле `models.py` или в каком -либо другом месте, которое будет импортировано Django при запуске.

If you've already created some users, you can generate tokens for all existing users like this:

Если вы уже создали некоторых пользователей, вы можете генерировать токены для всех существующих пользователей, как это:

```
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

#### By exposing an api endpoint

####, разоблачив конечную точку API

When using `TokenAuthentication`, you may want to provide a mechanism for clients to obtain a token given the username and password.  REST framework provides a built-in view to provide this behaviour.  To use it, add the `obtain_auth_token` view to your URLconf:

При использовании «tokenauthentication» вы можете предоставить клиентам механизм для получения токена с учетом имени пользователя и пароля.
Структура REST обеспечивает встроенное представление для обеспечения такого поведения.
Чтобы использовать его, добавьте представление `eave_auth_token` в свой urlconf:

```
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
```

Note that the URL part of the pattern can be whatever you want to use.

Обратите внимание, что URL часть шаблона может быть тем, что вы хотите использовать.

The `obtain_auth_token` view will return a JSON response when valid `username` and `password` fields are POSTed to the view using form data or JSON:

Представление `eave_auth_token` вернет ответ JSON, когда поля` inerername 'и `password' размещаются в представлении, используя данные формы или JSON:

```
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Note that the default `obtain_auth_token` view explicitly uses JSON requests and responses, rather than using default renderer and parser classes in your settings.

Обратите внимание, что представление по умолчанию `eave_auth_token` явно использует запросы и ответы JSON, а не использование рендеринга по умолчанию и классов анализатора в ваших настройках.

By default, there are no permissions or throttling applied to the  `obtain_auth_token` view. If you do wish to apply to throttle you'll need to override the view class,
and include them using the `throttle_classes` attribute.

По умолчанию нет разрешений или дросселя, применяемых к представлению `eave_auth_token`.
Если вы хотите подать заявку на дроссельную заслонку, вам нужно переопределить класс View,
и включите их, используя атрибут `throttle_classes`.

If you need a customized version of the `obtain_auth_token` view, you can do so by subclassing the `ObtainAuthToken` view class, and using that in your url conf instead.

Если вам нужна индивидуальная версия представления `eave_auth_token`, вы можете сделать это путем подкласса класса представления` Quectionauthtoken`, и вместо этого используя его в URL Conf.

For example, you may return additional user information beyond the `token` value:

Например, вы можете вернуть дополнительную информацию пользователя за пределами значения `token`:

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

#### с администратором Django

It is also possible to create Tokens manually through the admin interface. In case you are using a large user base, we recommend that you monkey patch the `TokenAdmin` class customize it to your needs, more specifically by declaring the `user` field as `raw_field`.

Также возможно создавать токены вручную через интерфейс администратора.
Если вы используете большую пользовательскую базу, мы рекомендуем вам обезьянуть исправить класс TokenAdmin`, более конкретно, объявив поле «пользователь» как `raw_field`.

`your_app/admin.py`:

`your_app/admin.py`:

```
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

#### Using Django manage.py command

#### с помощью команды django Manage.py

Since version 3.6.4 it's possible to generate a user token using the following command:

Поскольку версия 3.6.4 можно сгенерировать токен пользователя, используя следующую команду:

```
./manage.py drf_create_token <username>
```

this command will return the API token for the given user, creating it if it doesn't exist:

Эта команда вернет токен API для данного пользователя, создавая его, если ее не существует:

```
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

In case you want to regenerate the token (for example if it has been compromised or leaked) you can pass an additional parameter:

Если вы хотите восстановить токен (например, если он был скомпрометирован или просочился), вы можете передать дополнительный параметр:

```
./manage.py drf_create_token -r <username>
```

## SessionAuthentication

## sessionAuthentication

This authentication scheme uses Django's default session backend for authentication.  Session authentication is appropriate for AJAX clients that are running in the same session context as your website.

Эта схема аутентификации использует бэкэнд сеанса Django по умолчанию для аутентификации.
Аутентификация сеанса подходит для клиентов AJAX, которые работают в том же контексте сеанса, что и ваш сайт.

If successfully authenticated, `SessionAuthentication` provides the following credentials.

Если успешно аутентифицируется, «SessionAuthentication» предоставляет следующие учетные данные.

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляр Django` user '.
* `request.auth` будет« нет ».

Unauthenticated responses that are denied permission will result in an `HTTP 403 Forbidden` response.

Ответы на неавентичинку, которые отказано в разрешении, приведут к ответу `http 403.

If you're using an AJAX-style API with SessionAuthentication, you'll need to make sure you include a valid CSRF token for any "unsafe" HTTP method calls, such as `PUT`, `PATCH`, `POST` or `DELETE` requests.  See the [Django CSRF documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax) for more details.

Если вы используете API в стиле AJAX с SessionAuthentication, вам нужно убедиться, что вы включите действительный токен CSRF для любых вызовов «небезопасно» HTTP, таких как «Put», `patch ',` post` или `
Удалить запросы.
См. Документацию [Django CSRF] (https://docs.djangoproject.com/en/stable/ref/csrf/#ajax) для получения более подробной информации.

**Warning**: Always use Django's standard login view when creating login pages. This will ensure your login views are properly protected.

** ПРЕДУПРЕЖДЕНИЕ **: Всегда используйте стандартное представление Django в логине при создании страниц входа в систему.
Это гарантирует, что ваши виды входа будут должным образом защищены.

CSRF validation in REST framework works slightly differently from standard Django due to the need to support both session and non-session based authentication to the same views. This means that only authenticated requests require CSRF tokens, and anonymous requests may be sent without CSRF tokens. This behaviour is not suitable for login views, which should always have CSRF validation applied.

Валидация CSRF в структуре REST работает немного иначе, чем стандартный Django из-за необходимости поддержки как сеанс, так и не сессий, на основе аутентификации с одинаковыми представлениями.
Это означает, что только аутентифицированные запросы требуют токенов CSRF, а анонимные запросы могут быть отправлены без токенов CSRF.
Такое поведение не подходит для просмотров входа в систему, которые всегда должны иметь валидацию CSRF.

## RemoteUserAuthentication

## remoteUserauthentication

This authentication scheme allows you to delegate authentication to your web server, which sets the `REMOTE_USER`
environment variable.

Эта схема аутентификации позволяет делегировать аутентификацию на ваш веб -сервер, который устанавливает `remote_user`
переменная среды.

To use it, you must have `django.contrib.auth.backends.RemoteUserBackend` (or a subclass) in your
`AUTHENTICATION_BACKENDS` setting. By default, `RemoteUserBackend` creates `User` objects for usernames that don't
already exist. To change this and other behaviour, consult the
[Django documentation](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

Чтобы использовать его, вы должны иметь `django.contrib.auth.backends.remoteuserbackend` (или подкласс) в вашем
`Authentication_backends` Установка.
По умолчанию, `remoteUserbackend` создает объекты пользователя для имен пользователей, которые не
уже существует.
Чтобы изменить это и другое поведение, проконсультируйтесь
[Документация Django] (https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

If successfully authenticated, `RemoteUserAuthentication` provides the following credentials:

Если успешно аутентифицируется, `remoteUserauthentication 'предоставляет следующие учетные данные:

* `request.user` will be a Django `User` instance.
* `request.auth` will be `None`.

* `request.user` будет экземпляр Django` user '.
* `request.auth` будет« нет ».

Consult your web server's documentation for information about configuring an authentication method, e.g.:

Проконсультируйтесь с документацией вашего веб -сервера для получения информации о настройке метода аутентификации, например:

* [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
* [NGINX (Restricting Access)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

* [Apache Authentication How-at-ale] (https://httpd.apache.org/docs/2.4/howto/auth.html)
* [Nginx (ограничение доступа)] (https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

# Custom authentication

# Пользовательская аутентификация

To implement a custom authentication scheme, subclass `BaseAuthentication` and override the `.authenticate(self, request)` method.  The method should return a two-tuple of `(user, auth)` if authentication succeeds, or `None` otherwise.

Чтобы внедрить пользовательскую схему аутентификации, подкласс `baseauthentication 'и переопределить метод`. Authenticate (self, запрос) `.
Метод должен вернуть двухверенный из `(пользователь, auth)` Если аутентификация добивается успеха, или иначе `none.

In some circumstances instead of returning `None`, you may want to raise an `AuthenticationFailed` exception from the `.authenticate()` method.

В некоторых обстоятельствах вместо того, чтобы вернуть «нет», вы можете поднять исключение «аутентификации» из метода `.Authenticate ()`.

Typically the approach you should take is:

Как правило, подход, который вы должны использовать:

* If authentication is not attempted, return `None`.  Any other authentication schemes also in use will still be checked.
* If authentication is attempted but fails, raise an `AuthenticationFailed` exception.  An error response will be returned immediately, regardless of any permissions checks, and without checking any other authentication schemes.

* Если аутентификация не предпринимается, верните `none`.
Любые другие схемы аутентификации, также используемые, все еще будут проверены.
* Если аутентификация предпринимается, но не удается, поднимите исключение «аутентификация».
Ответ об ошибке будет возвращен немедленно, независимо от каких -либо проверок разрешений, и без проверки любых других схем аутентификации.

You *may* also override the `.authenticate_header(self, request)` method.  If implemented, it should return a string that will be used as the value of the `WWW-Authenticate` header in a `HTTP 401 Unauthorized` response.

Вы * можете * также переопределить метод `.Authenticate_header (self, запрос)`.
В случае реализации он должен вернуть строку, которая будет использоваться в качестве значения заголовка `www-authenticate` в ответе` http 401 unauthorized`.

If the `.authenticate_header()` method is not overridden, the authentication scheme will return `HTTP 403 Forbidden` responses when an unauthenticated request is denied access.

Если метод `.AuthentIcate_Header ()` не переопределен, схема аутентификации вернет `http 403 FORBIDE -ответы, когда неавтоцированный запрос будет отклонен доступом.

---

**Note:** When your custom authenticator is invoked by the request object's `.user` or `.auth` properties, you may see an `AttributeError` re-raised as a `WrappedAttributeError`. This is necessary to prevent the original exception from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from your custom authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. These errors should be fixed or otherwise handled by your authenticator.

** ПРИМЕЧАНИЕ: ** Когда ваш пользовательский аутентификатор используется свойствами объекта запроса `.user` или`.
Это необходимо, чтобы предотвратить подавление первоначального исключения из -за доступа внешнего свойства.
Python не признает, что `attributeRror` происходит от вашего пользовательского аутентификатора и вместо этого предполагает, что объект запроса не имеет свойства` .user` или `.Auth`.
Эти ошибки должны быть исправлены или иным образом обработаны вашим аутентификатором.

---

## Example

## Пример

The following example will authenticate any incoming request as the user given by the username in a custom request header named 'X-USERNAME'.

В следующем примере будет аутентифицирует любой входящий запрос в качестве пользователя, предоставленного именем пользователя в пользовательском заголовке запроса с именем «x-username».

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

# Сторонние пакеты

The following third-party packages are also available.

Следующие сторонние пакеты также доступны.

## django-rest-knox

## django-rest-knox

[Django-rest-knox](https://github.com/James1345/django-rest-knox) library provides models and views to handle token-based authentication in a more secure and extensible way than the built-in TokenAuthentication scheme - with Single Page Applications and Mobile clients in mind. It provides per-client tokens, and views to generate them when provided some other authentication (usually basic authentication), to delete the token (providing a server enforced logout) and to delete all tokens (logs out all clients that a user is logged into).

[Django-rest-knox] (https://github.com/james1345/django-rest-knox).
С учетом одностраничных приложений и мобильных клиентов.
Он предоставляет токены для клиента и представления для их генерирования при предоставлении какой-либо другой аутентификации (обычно базовой аутентификации), для удаления токена (предоставление обеспеченного выхода на сервер) и удаления всех токенов (входит в систему всех клиентов, которые пользователь вошел в
)

## Django OAuth Toolkit

## django oauth toolkit

The [Django OAuth Toolkit](https://github.com/evonove/django-oauth-toolkit) package provides OAuth 2.0 support and works with Python 3.4+. The package is maintained by [jazzband](https://github.com/jazzband/) and uses the excellent [OAuthLib](https://github.com/idan/oauthlib).  The package is well documented, and well supported and is currently our **recommended package for OAuth 2.0 support**.

Пакет [https://github.com/evonove/django-oauth-toolkit) обеспечивает поддержку и работает с Python 3.4+.
Пакет поддерживается [jazzband] (https://github.com/jazzband/) и использует превосходную [oauthlib] (https://github.com/idan/oauthlib).
Пакет хорошо задокументирован и хорошо поддерживается и в настоящее время является нашим ** рекомендуемым пакетом для поддержки OAuth 2.0 **.

### Installation & configuration

### Установка и конфигурация

Install using `pip`.

Установите, используя `pip`.

```
pip install django-oauth-toolkit
```

Add the package to your `INSTALLED_APPS` and modify your REST framework settings.

Добавьте пакет в свой `stasted_apps` и измените настройки платформы REST.

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

Более подробную информацию см. В рамках REST-Framework [django REST] (https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html).

## Django REST framework OAuth

## Django Rest Framework oauth

The [Django REST framework OAuth](https://jpadilla.github.io/django-rest-framework-oauth/) package provides both OAuth1 and OAuth2 support for REST framework.

[Django Rest Framework OAuth] (https://jpadilla.github.io/django-rest-framework-oauth/) обеспечивает поддержку как OAuth1, так и OAuth2 для структуры REST.

This package was previously included directly in the REST framework but is now supported and maintained as a third-party package.

Этот пакет ранее был включен непосредственно в рамки REST, но теперь поддерживается и поддерживается в качестве стороннего пакета.

### Installation & configuration

### Установка и конфигурация

Install the package using `pip`.

Установите пакет, используя `pip`.

```
pip install djangorestframework-oauth
```

For details on configuration and usage see the Django REST framework OAuth documentation for [authentication](https://jpadilla.github.io/django-rest-framework-oauth/authentication/) and [permissions](https://jpadilla.github.io/django-rest-framework-oauth/permissions/).

Для получения подробной информации о конфигурации и использовании см. В рамках Django Rest Documentwork OAuth для [аутентификации] (https://jpadilla.github.io/django-rest-framework-oauth/authentication/) и [разрешения] (https: // jpadilla.
github.io/django-rest-framework-oauth/permissions/).

## JSON Web Token Authentication

## json -аутентификация веб -токена

JSON Web Token is a fairly new standard which can be used for token-based authentication. Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) which provides some features as well as a pluggable token blacklist app.

JSON Web Token-это довольно новый стандарт, который можно использовать для аутентификации на основе токенов.
В отличие от встроенной схемы Tokenauthentication, аутентификации JWT не нужно использовать базу данных для проверки токена.
Пакет для аутентификации JWT-это [djangestframework-simplejwt] (https://github.com/davesque/django-rest-framework-simplejwt), которое предоставляет некоторые функции, а также приложение для черного списка для подкоров.

## Hawk HTTP Authentication

## http http

The [HawkREST](https://hawkrest.readthedocs.io/en/latest/) library builds on the [Mohawk](https://mohawk.readthedocs.io/en/latest/) library to let you work with [Hawk](https://github.com/hueniverse/hawk) signed requests and responses in your API. [Hawk](https://github.com/hueniverse/hawk) lets two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication](https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05) (which was based on parts of [OAuth 1.0](https://oauth.net/core/1.0a/)).

[Hawkrest] (https://hawkrest.readthedocs.io/en/latest/) Библиотека строится на библиотеке [https://mohawk.readthedocs.io/en/latest/), чтобы позволить вам работать с [[
Hawk] (https://github.com/hueniverse/hawk) Подписанные запросы и ответы в вашем API.
[Hawk] (https://github.com/hueniverse/hawk) позволяет двум сторонам надежно общаться друг с другом, используя сообщения, подписанные общим ключом.
Он основан на [http mac access atultication] (https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05) (который был основан на частях [OAuth 1.0] (https
: //oauth.net/core/1.0a/)).

## HTTP Signature Authentication

## http -подписи аутентификация

HTTP Signature (currently a [IETF draft](https://datatracker.ietf.org/doc/draft-cavage-http-signatures/)) provides a way to achieve origin authentication and message integrity for HTTP messages. Similar to [Amazon's HTTP Signature scheme](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), used by many of its services, it permits stateless, per-request authentication. [Elvio Toccalino](https://github.com/etoccalino/) maintains the [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) (outdated) package which provides an easy to use HTTP Signature Authentication mechanism. You can use the updated fork version of [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature), which is [drf-httpsig](https://github.com/ahknight/drf-httpsig).

Подпись HTTP (в настоящее время A [IETF DRAFT] (https://datatracker.ietf.org/doc/draft-cavage-http-signatures/)) предоставляет способ достичь аутентификации происхождения и целостности сообщений для HTTP-сообщений.
Подобно [схеме подписи HTTP Amazon] (https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), используемое многими его услугами, он позволяет без гражданства, Per-Request
аутентификация.
[Elvio toccalino] (https://github.com/etoccalino/) поддерживает [djangestframework-httpsignature] (https://github.com/etoccalino/django-rest-framework-httpsignature) (устаревший), который обеспечивает легкий пакет
использовать механизм аутентификации HTTP.
Вы можете использовать обновленную версию вилки [djangorestframework-httpsignature] (https://github.com/etoccalino/django-rest-framework-httpsignature), то есть [drf-httpsig] (https://github.com/ahknight
/drf-httpsig).

## Djoser

## Джозер

[Djoser](https://github.com/sunscrapers/djoser) library provides a set of views to handle basic actions such as registration, login, logout, password reset and account activation. The package works with a custom user model and uses token-based authentication. This is ready to use REST implementation of the Django authentication system.

[Djoser] (https://github.com/sunscrapers/djoser) предоставляет набор представлений для обработки основных действий, таких как регистрация, вход, вход в систему, сброс пароля и активация учетной записи.
Пакет работает с пользовательской моделью пользователя и использует аутентификацию на основе токков.
Это готово использовать реализацию отдыха системы аутентификации Django.

## django-rest-auth / dj-rest-auth

## django-rest-auth / dj-rest-auth

This library provides a set of REST API endpoints for registration, authentication (including social media authentication), password reset, retrieve and update user details, etc. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for user management.

Эта библиотека предоставляет набор конечных точек API REST для регистрации, аутентификации (включая аутентификацию в социальных сетях), сброс пароля, получение и обновление данных пользователя и т. Д. Имея эти конечные точки API, ваши клиентские приложения, такие как AngularJS, iOS, Android и другие
Можно общаться с вашим бэкэнд -сайтом Django независимо через API REST для управления пользователями.

There are currently two forks of this project.

В настоящее время есть две вилки этого проекта.

* [Django-rest-auth](https://github.com/Tivix/django-rest-auth) is the original project, [but is not currently receiving updates](https://github.com/Tivix/django-rest-auth/issues/568).
* [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth) is a newer fork of the project.

* [Django-rest-auth] (https://github.com/tivix/django-rest-auth) является оригинальным проектом, [но в настоящее время не получает обновления] (https://github.com/tivix/django
-Rest-auth/проблемы/568).
* [DJ-Rest-auth] (https://github.com/jazzband/dj-rest-auth)-более новая вилка проекта.

## drf-social-oauth2

## drf-social-oauth2

[Drf-social-oauth2](https://github.com/wagnerdelima/drf-social-oauth2) is a framework that helps you authenticate with major social oauth2 vendors, such as Facebook, Google, Twitter, Orcid, etc. It generates tokens in a JWTed way with an easy setup.

[Drf-social-oauth2] (https://github.com/wagnerdelima/drf-social-oauth2)-это структура, которая помогает вам аутентифицировать с крупными поставщиками Social OAuth2, такими как Facebook, Google, Twitter, Orcid и т. Д.
генерирует токены с помощью простой настройки.

## drfpasswordless

## drfpasswordless

[drfpasswordless](https://github.com/aaronn/django-rest-framework-passwordless) adds (Medium, Square Cash inspired) passwordless support to Django REST Framework's TokenAuthentication scheme. Users log in and sign up with a token sent to a contact point like an email address or a mobile number.

[drfpasswordless] (https://github.com/aaronn/django-rest-framework-passwordless) добавляет (средние, квадратные наличные) поддержка без пароля в схему Tokenauthentication Django Rest.
Пользователи входят в систему и регистрируются с токеном, отправленным на контактную точку, такую как адрес электронной почты или номер мобильного телефона.

## django-rest-authemail

## django-rest-authemail

[django-rest-authemail](https://github.com/celiao/django-rest-authemail) provides a RESTful API interface for user signup and authentication. Email addresses are used for authentication, rather than usernames.  API endpoints are available for signup, signup email verification, login, logout, password reset, password reset verification, email change, email change verification, password change, and user detail.  A fully functional example project and detailed instructions are included.

[django-rest-authemail] (https://github.com/celiao/django-rest-authemail) предоставляет интерфейс API Restful для регистрации и аутентификации пользователя.
Адреса электронной почты используются для аутентификации, а не имена пользователей.
Конечные точки API доступны для регистрации, проверки электронной почты, входа в систему, входа в систему, сброса пароля, проверки сброса пароля, изменения электронной почты, проверки изменения электронной почты, изменения пароля и данных пользователя.
Полностью функциональный пример проекта и подробные инструкции включены.

## Django-Rest-Durin

## django-rest-durin

[Django-Rest-Durin](https://github.com/eshaan7/django-rest-durin) is built with the idea to have one library that does token auth for multiple Web/CLI/Mobile API clients via one interface but allows different token configuration for each API Client that consumes the API. It provides support for multiple tokens per user via custom models, views, permissions that work with Django-Rest-Framework. The token expiration time can be different per API client and is customizable via the Django Admin Interface.

[Django-rest-durin] (https://github.com/eshaan7/django-rest-durin) создан с идеей иметь одну библиотеку, которая делает токен Auth для нескольких клиентов Web/CLI/Mobile API через один интерфейс, но но
Позволяет различной конфигурации токена для каждого клиента API, который потребляет API.
Он обеспечивает поддержку нескольких токенов на одного пользователя через пользовательские модели, представления, разрешения, которые работают с Django-Rest-Framework.
Время истечения срока действия токена может быть другим в соответствии с клиентом API и настраивается через интерфейс администратора Django.

More information can be found in the [Documentation](https://django-rest-durin.readthedocs.io/en/latest/index.html).

Более подробную информацию можно найти в [документации] (https://django-rest-durin.readthedocs.io/en/latest/index.html).