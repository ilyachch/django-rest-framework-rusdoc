<!-- TRANSLATED by md-translate -->
# Аутентификация

> Аутентификация должна быть подключаемой.
>
> - Джейкоб Каплан-Мосс, ["Худшие практики REST"](https://jacobian.org/writing/rest-worst-practices/)

Аутентификация - это механизм связывания входящего запроса с набором идентификационных данных, таких как пользователь, от которого пришел запрос, или токен, которым он был подписан. Политики [permission](permissions.md) и [throttling](throttling.md) могут затем использовать эти учетные данные, чтобы определить, должен ли запрос быть разрешен.

DRF предоставляет несколько схем аутентификации из коробки, а также позволяет реализовать пользовательские схемы.

Аутентификация всегда выполняется в самом начале представления, до того, как произойдет проверка разрешений и дросселирования, и до того, как будет разрешено выполнение любого другого кода.

Свойство `request.user` обычно устанавливается на экземпляр класса `User` пакета `contrib.auth`.

Свойство `request.auth` используется для любой дополнительной информации об аутентификации, например, оно может быть использовано для представления маркера аутентификации, которым был подписан запрос.

---

**Примечание:** Не забывайте, что **аутентификация сама по себе не разрешает и не запрещает входящий запрос**, она просто идентифицирует учетные данные, с которыми был сделан запрос.

Информацию о том, как настроить политику разрешений для вашего API, смотрите в документации [permissions](permissions.md).

---

## Как определяется аутентификация

Схемы аутентификации всегда определяются как список классов. DRF попытается выполнить аутентификацию с каждым классом в списке, и установит `request.user` и `request.auth`, используя возвращаемое значение первого класса, который успешно аутентифицируется.

Если ни один класс не выполнит аутентификацию, `request.user` будет установлен в экземпляр `django.contrib.auth.models.AnonymousUser`, а `request.auth` будет установлен в `None`.

Значение `request.user` и `request.auth` для неаутентифицированных запросов можно изменить с помощью параметров `UNAUTHENTICATED_USER` и `UNAUTHENTICATED_TOKEN`.

## Установка схемы аутентификации

Схемы аутентификации по умолчанию можно установить глобально, используя настройку `DEFAULT_AUTHENTICATION_CLASSES`. Например.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

Вы также можете установить схему аутентификации отдельно для каждого представления или каждого набора представлений, используя представления на основе класса `APIView`.

```python
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

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```python
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

## Неавторизованные и запрещенные ответы

Когда неаутентифицированному запросу отказано в разрешении, существует два различных кода ошибок, которые могут быть уместны.

* [HTTP 401 Unauthorized](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
* [HTTP 403 Permission Denied](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

Ответы HTTP 401 всегда должны содержать заголовок `WWW-Authenticate`, который указывает клиенту, как пройти аутентификацию. Ответы HTTP 403 не включают заголовок `WWW-Authenticate`.

Тип ответа, который будет использоваться, зависит от схемы аутентификации. Хотя может использоваться несколько схем аутентификации, для определения типа ответа может использоваться только одна схема. **Первый класс аутентификации, установленный для представления, используется при определении типа ответа**.

Обратите внимание, что когда запрос может успешно пройти аутентификацию, но при этом получить отказ в разрешении на выполнение запроса, в этом случае всегда будет использоваться ответ `403 Permission Denied`, независимо от схемы аутентификации.

## Специфическая конфигурация Apache mod_wsgi

Обратите внимание, что при развертывании на [Apache using mod_wsgi](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html) заголовок авторизации по умолчанию не передается приложению WSGI, так как предполагается, что аутентификация будет обрабатываться Apache, а не на уровне приложения.

Если вы развертываете на Apache и используете любую аутентификацию, не основанную на сеансах, вам необходимо явно настроить mod_wsgi для передачи необходимых заголовков приложению. Это можно сделать, указав директиву `WSGIPassAuthorization` в соответствующем контексте и установив ее в значение `'On'`.

```apache
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On
```

---

# API Reference

## BasicAuthentication

Эта схема аутентификации использует [HTTP Basic Authentication](https://tools.ietf.org/html/rfc2617), подписанную именем пользователя и паролем. Базовая аутентификация обычно подходит только для тестирования.

При успешной аутентификации `BasicAuthentication` предоставляет следующие учетные данные.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком WWW-Authenticate. Например:

```http
WWW-Authenticate: Basic realm="api"
```

**Примечание:** Если вы используете `BasicAuthentication` в реальном проекте, вы должны убедиться, что ваш API доступен только через `https`. Вы также должны убедиться, что клиенты вашего API всегда будут повторно запрашивать имя пользователя и пароль при входе в систему и никогда не будут сохранять эти данные в постоянном хранилище.

## TokenAuthentication

---

**Примечание:** Аутентификация с помощью токенов, предоставляемая DRF, является довольно простой реализацией.

Для реализации, которая позволяет использовать более одного токена на пользователя, имеет некоторые более жесткие детали реализации безопасности и поддерживает истечение срока действия токена, пожалуйста, обратитесь к стороннему пакету [Django REST Knox](https://github.com/James1345/django-rest-knox).

---

Эта схема аутентификации использует простую схему аутентификации HTTP на основе токенов. Токен-аутентификация подходит для клиент-серверных установок, таких как собственные настольные и мобильные клиенты.

Для использования схемы `TokenAuthentication` вам необходимо [настроить классы аутентификации](#setting-the-authentication-scheme), чтобы включить `TokenAuthentication`, и дополнительно включить `rest_framework.authtoken` в настройку `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

Обязательно запустите `manage.py migrate` после изменения настроек.

Приложение `rest_framework.authtoken` обеспечивает миграцию баз данных Django.

Вам также потребуется создать токены для своих пользователей.

```python
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

Для аутентификации клиентов ключ токена должен быть включен в HTTP-заголовок `Authorization`. Ключ должен иметь префикс в виде строкового литерала "Token", с пробелами, разделяющими эти две строки. Например:

```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

*Если вы хотите использовать другое ключевое слово в заголовке, например `Bearer`, просто создайте подкласс `TokenAuthentication` и установите переменную класса `keyword`.

При успешной аутентификации `TokenAuthentication` предоставляет следующие учетные данные.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет экземпляром `rest_framework.authtoken.models.Token`.

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком WWW-Authenticate. Например:

```http
WWW-Authenticate: Token
```

Инструмент командной строки `curl` может быть полезен для тестирования API с аутентификацией токенов. Например:

```http
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

---

**Примечание:** Если вы используете `TokenAuthentication` в реальном проекте, вы должны убедиться, что ваш API доступен только через `https`.

---

### Генерация токенов

#### С помощью сигналов

Если вы хотите, чтобы у каждого пользователя был автоматически сгенерированный Token, вы можете просто перехватить сигнал `post_save` пользователя.

```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

Обратите внимание, что вам нужно убедиться, что вы поместили этот фрагмент кода в установленный модуль `models.py` или в другое место, которое будет импортироваться Django при запуске.

Если вы уже создали несколько пользователей, вы можете сгенерировать токены для всех существующих пользователей следующим образом:

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

#### Посредством конечной точки API

При использовании `TokenAuthentication` вы можете захотеть предоставить клиентам механизм для получения токена, заданного именем пользователя и паролем. DRF предоставляет встроенное представление для обеспечения такого поведения. Чтобы использовать его, добавьте представление `obtain_auth_token` в URLconf:

```python
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
```

Обратите внимание, что URL часть шаблона может быть любой, которую вы хотите использовать.

Представление `obtain_auth_token` вернет ответ в формате JSON, если действительные поля `username` и `password` будут отправлены в представление с помощью данных формы или JSON:

```python
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Обратите внимание, что представление по умолчанию `obtain_auth_token` явно использует JSON запросы и ответы, а не использует классы рендерера и парсера по умолчанию в ваших настройках.

По умолчанию к представлению `obtain_auth_token` не применяется никаких разрешений или дросселирования. Если вы хотите применить дросселирование, вам нужно переопределить класс представления и включить их с помощью атрибута `throttle_classes`.

Если вам нужна настраиваемая версия представления `obtain_auth_token`, вы можете сделать это, создав подкласс класса представления `ObtainAuthToken` и используя его в url conf.

Например, вы можете возвращать дополнительную информацию о пользователе помимо значения `token`:

```python
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

И в вашем `urls.py`:

```python
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
```

#### С администратором Django

Токены также можно создавать вручную через интерфейс администратора. В случае, если вы используете большую базу пользователей, мы рекомендуем вам пропатчить класс `TokenAdmin`, чтобы настроить его под свои нужды, в частности, объявив поле `user` как `raw_field`.

`ваше_приложение/admin.py`:

```python
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

#### Использование команды Django manage.py

Начиная с версии 3.6.4 можно сгенерировать пользовательский токен с помощью следующей команды:

```bash
./manage.py drf_create_token <username>
```

эта команда вернет API-токен для данного пользователя, создав его, если он не существует:

```bash
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

Если вы хотите восстановить токен (например, если он был скомпрометирован или произошла утечка), вы можете передать дополнительный параметр:

```bash
./manage.py drf_create_token -r <username>
```

## SessionAuthentication

Эта схема аутентификации использует бэкенд сессий Django по умолчанию для аутентификации. Сеансовая аутентификация подходит для клиентов AJAX, которые работают в том же сеансовом контексте, что и ваш сайт.

При успешной аутентификации `SessionAuthentication` предоставляет следующие учетные данные.

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Ответы без аутентификации, которым отказано в разрешении, приведут к ответу `HTTP 403 Forbidden`.

Если вы используете API в стиле AJAX с `SessionAuthentication`, вам нужно убедиться, что вы включаете действительный CSRF токен для любых "небезопасных" вызовов HTTP методов, таких как `PUT`, `PATCH`, `POST` или `DELETE` запросы. Более подробную информацию смотрите в [Django CSRF documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

**Предупреждение**: Всегда используйте стандартное представление входа Django при создании страниц входа. Это обеспечит надлежащую защиту ваших представлений входа.

Проверка CSRF в DRF работает несколько иначе, чем в стандартном Django, из-за необходимости поддерживать как сеансовую, так и несеансовую аутентификацию для одних и тех же представлений. Это означает, что только аутентифицированные запросы требуют CSRF-токенов, а анонимные запросы могут быть отправлены без CSRF-токенов. Такое поведение не подходит для представлений входа в систему, к которым всегда должна применяться проверка CSRF.

## RemoteUserAuthentication

Эта схема аутентификации позволяет делегировать аутентификацию вашему веб-серверу, который устанавливает переменную окружения `REMOTE_USER`.

Чтобы использовать его, вы должны иметь `django.contrib.auth.backends.RemoteUserBackend` (или подкласс) в настройках `AUTHENTICATION_BACKENDS`. По умолчанию `RemoteUserBackend` создает объекты `User` для имен пользователей, которые еще не существуют. Чтобы изменить это и другое поведение, обратитесь к [документации Django](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

При успешной аутентификации `RemoteUserAuthentication` предоставляет следующие учетные данные:

* `request.user` будет экземпляром Django `User`.
* `request.auth` будет `None`.

Обратитесь к документации вашего веб-сервера за информацией о настройке метода аутентификации, например:

* [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
* [NGINX (ограничение доступа)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

# Пользовательская аутентификация

Чтобы реализовать собственную схему аутентификации, создайте подкласс `BaseAuthentication` и переопределите метод `.authenticate(self, request)`. Метод должен возвращать кортеж `(user, auth)`, если аутентификация прошла успешно, или `None` в противном случае.

В некоторых случаях вместо возврата `None` вы можете захотеть вызвать исключение `AuthenticationFailed` из метода `.authenticate()`.

Как правило, вам следует придерживаться следующего подхода:

* Если попытка аутентификации не была предпринята, верните `None`. Любые другие схемы аутентификации, которые также используются, будут проверены.
* Если попытка аутентификации была предпринята, но не удалась, вызовите исключение `AuthenticationFailed`. Ответ об ошибке будет возвращен немедленно, независимо от любых проверок разрешений и без проверки других схем аутентификации.

Вы *можете* также переопределить метод `.authenticate_header(self, request)`. Если он реализован, он должен возвращать строку, которая будет использоваться в качестве значения заголовка `WWW-Authenticate` в ответе `HTTP 401 Unauthorized`.

Если метод `.authenticate_header()` не переопределен, схема аутентификации будет возвращать ответы `HTTP 403 Forbidden`, когда неаутентифицированному запросу будет отказано в доступе.

---

**Примечание:** Когда ваш пользовательский аутентификатор вызывается свойствами `.user` или `.auth` объекта запроса, вы можете увидеть, как `AttributeError` повторно выбрасывается, как `WrappedAttributeError`. Это необходимо для того, чтобы исходное исключение не было подавлено доступом к внешнему свойству. Python не распознает, что `AttributeError` исходит от вашего пользовательского аутентификатора, и вместо этого будет считать, что объект запроса не имеет свойства `.user` или `.auth`. Эти ошибки должны быть исправлены или иным образом обработаны вашим аутентификатором.

---

## Пример

Следующий пример аутентифицирует любой входящий запрос как пользователя, указанного в имени пользователя в пользовательском заголовке запроса под названием 'X-USERNAME'.

```python
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

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## django-rest-knox

Библиотека [Django-rest-knox](https://github.com/James1345/django-rest-knox) предоставляет модели и представления для обработки аутентификации на основе токенов более безопасным и расширяемым способом, чем встроенная схема `TokenAuthentication` - с учетом одностраничных приложений и мобильных клиентов. Она предоставляет токены для каждого клиента, а также представления для их генерации при предоставлении другой аутентификации (обычно базовой), для удаления токена (обеспечивая принудительный выход с сервера) и для удаления всех токенов (выход из всех клиентов, в которые вошел пользователь).

## Django OAuth Toolkit

Пакет [Django OAuth Toolkit](https://github.com/evonove/django-oauth-toolkit) обеспечивает поддержку OAuth 2.0 и работает с Python 3.4+. Пакет поддерживается [jazzband](https://github.com/jazzband/) и использует превосходный [OAuthLib](https://github.com/idan/oauthlib). Пакет хорошо документирован, хорошо поддерживается и в настоящее время является нашим **рекомендованным пакетом для поддержки OAuth 2.0**.

### Установка и настройка

Установите с помощью `pip`.

```bash
pip install django-oauth-toolkit
```

Добавьте пакет в `INSTALLED_APPS` и измените настройки DRF.

```python
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

Более подробную информацию можно найти в документации [Django REST framework - Getting started](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html).

## Django REST framework OAuth

Пакет [Django REST framework OAuth](https://jpadilla.github.io/django-rest-framework-oauth/) обеспечивает поддержку OAuth1 и OAuth2 для DRF.

Ранее этот пакет был включен непосредственно в DRF, но теперь поддерживается и сопровождается как пакет стороннего разработчика.

### Установка и настройка

Установите пакет с помощью `pip`.

```bash
pip install djangorestframework-oauth
```

Подробнее о настройке и использовании смотрите документацию по OAuth фреймворку Django REST для [authentication](https://jpadilla.github.io/django-rest-framework-oauth/authentication/) и [permissions](https://jpadilla.github.io/django-rest-framework-oauth/permissions/).

## JSON Web Token Authentication

JSON Web Token - это довольно новый стандарт, который можно использовать для аутентификации на основе токенов. В отличие от встроенной схемы TokenAuthentication, аутентификация JWT не требует использования базы данных для проверки токена. Пакет для JWT-аутентификации - [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt), который предоставляет некоторые возможности, а также подключаемое приложение черного списка токенов.

## Аутентификация Hawk HTTP

Библиотека [HawkREST](https://hawkrest.readthedocs.io/en/latest/) основана на библиотеке [Mohawk](https://mohawk.readthedocs.io/en/latest/) и позволяет вам работать с подписанными запросами и ответами [Hawk](https://github.com/hueniverse/hawk) в вашем API. [Hawk](https://github.com/hueniverse/hawk) позволяет двум сторонам безопасно общаться друг с другом, используя сообщения, подписанные общим ключом. Она основана на [HTTP MAC аутентификации доступа](https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05) (которая была основана на части [OAuth 1.0](https://oauth.net/core/1.0a/)).

## Аутентификация посредством подписи HTTP

HTTP Signature (в настоящее время [проект IETF](https://datatracker.ietf.org/doc/draft-cavage-http-signatures/)) предоставляет способ аутентификации происхождения и проверки целостности сообщений HTTP. Подобно схеме [Amazon's HTTP Signature scheme](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), используемой многими сервисами компании, она допускает аутентификацию по каждому запросу без хранения состояния. [Elvio Toccalino](https://github.com/etoccalino/) поддерживает пакет [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) (устаревший), который предоставляет простой в использовании механизм аутентификации HTTP Signature. Вы можете использовать обновленную версию-форк [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature), которой является [drf-httpsig](https://github.com/ahknight/drf-httpsig).

## Djoser

[Djoser](https://github.com/sunscrapers/djoser) библиотека предоставляет набор представлений для обработки основных действий, таких как регистрация, вход, выход, сброс пароля и активация учетной записи. Пакет работает с пользовательской моделью пользователя и использует аутентификацию на основе токенов. Это готовая к использованию REST-реализация системы аутентификации Django.

## django-rest-auth / dj-rest-auth

Эта библиотека предоставляет набор конечных точек REST API для регистрации, аутентификации (включая аутентификацию в социальных сетях), сброса пароля, получения и обновления данных пользователя и т.д. Имея эти конечные точки API, ваши клиентские приложения, такие как AngularJS, iOS, Android и другие, могут самостоятельно общаться с вашим бэкендом Django через REST API для управления пользователями.

В настоящее время существует два форка этого проекта.

* [Django-rest-auth](https://github.com/Tivix/django-rest-auth) - оригинальный проект, [но в настоящее время не получает обновлений](https://github.com/Tivix/django-rest-auth/issues/568).
* [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth) - более новый форк проекта.

## drf-social-oauth2

[Drf-social-oauth2](https://github.com/wagnerdelima/drf-social-oauth2) - это фреймворк, который поможет вам аутентифицироваться у основных поставщиков социального oauth2, таких как Facebook, Google, Twitter, Orcid и др. Он генерирует токены в виде JWT с простой настройкой.

## drfpasswordless

[drfpasswordless](https://github.com/aaronn/django-rest-framework-passwordless) добавляет (по мотивам Medium, Square Cash) поддержку беспарольного входа в схему TokenAuthentication платформы DRF. Пользователи входят в систему и регистрируются с помощью токена, отправленного на контактную точку, например, адрес электронной почты или номер мобильного телефона.

## django-rest-authemail

[django-rest-authemail](https://github.com/celiao/django-rest-authemail) предоставляет RESTful API интерфейс для регистрации и аутентификации пользователей. Для аутентификации используются адреса электронной почты, а не имена пользователей. Доступны конечные точки API для регистрации, проверки электронной почты при регистрации, входа в систему, выхода из системы, сброса пароля, проверки сброса пароля, изменения электронной почты, проверки изменения электронной почты, изменения пароля и детализации пользователя. Полностью функциональный пример проекта и подробные инструкции прилагаются.

## Django-Rest-Durin

[Django-Rest-Durin](https://github.com/eshaan7/django-rest-durin) создана с идеей иметь одну библиотеку, которая делает аутентификацию токенов для нескольких Web/CLI/Mobile API клиентов через один интерфейс, но позволяет различную конфигурацию токенов для каждого API клиента, который потребляет API. Она обеспечивает поддержку нескольких токенов для каждого пользователя через пользовательские модели, представления, разрешения, которые работают с Django-Rest-Framework. Время истечения срока действия токена может быть разным для каждого API-клиента и настраивается через интерфейс администратора Django.

Более подробную информацию можно найти в [Документации](https://django-rest-durin.readthedocs.io/en/latest/index.html).
