# Аутентификация

> Аутентификация должна быть подключаемой.
>
> &mdash; Jacob Kaplan-Moss, ["REST worst practices"][cite]

Аутентификация - механизм связывания входящего запроса с набором идентифицирующих учетных данных, таких как пользователь, от которого пришел запрос, или токен, которым он был подписан. Политики [разрешений][permission] и [регулирования][throttling] могут затем использовать эти учетные данные, чтобы определить, следует ли разрешить запрос.

REST framework предоставляет ряд схем аутентификации из коробки, а также позволяет реализовать собственные схемы.

Аутентификация всегда выполняется в самом начале представления, до того, как произойдут проверки разрешений и регулирования, а также до того, как будет разрешено выполнение любого другого кода.

Свойство `request.user` обычно устанавливается равным экземпляру класса `User` из пакета `contrib.auth`.

Свойство `request.auth` используется для любой дополнительной информации аутентификации, например, оно может использоваться для представления токена аутентификации, которым был подписан запрос.

---

**Примечание:** Не забывайте, что **аутентификация сама по себе не разрешает или не запрещает входящий запрос**, она просто определяет учетные данные, с которыми был сделан запрос.

Для получения информации о том, как настроить политики разрешений для вашего API, см. [Документация по разрешениям][permission].

---

## Как определяется аутентификация

Схемы аутентификации всегда определяются как список классов. REST framework будет пытаться аутентифицировать каждым классом в списке и установит `request.user` и` request.auth`, используя возвращаемое значение первого класса, который успешно выполнит аутентификацию.

Если ни один класс не выполнит аутентификацию, `request.user` будет установлен как экземпляр `django.contrib.auth.models.AnonymousUser`, а `request.auth` будет установлен как `None`.

Значение `request.user` и` request.auth` для неаутентифицированных запросов может быть изменено с помощью настроек `UNAUTHENTICATED_USER` и `UNAUTHENTICATED_TOKEN`.

## Установка схемы аутентификации

Схемы аутентификации по умолчанию могут быть установлены глобально, используя настройку `DEFAULT_AUTHENTICATION_CLASSES`. Например:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

Вы также можете установить схему аутентификации для каждого представления или набора представлений, используя представления на основе классов `APIView`.

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
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
```

Или, если вы используете декоратор `@api_view` с представлениями на основе функций.

```python
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
```

## Несанкционированные и запрещенные ответы

Когда неаутентифицированному запросу отказано в выполнении, могут быть подходящими два разных кода ошибки.

* [HTTP 401 Unauthorized][http401]
* [HTTP 403 Permission Denied][http403]

Ответы `HTTP 401` всегда должны включать заголовок `WWW-Authenticate`, который указывает клиенту, как пройти аутентификацию. Ответы `HTTP 403` не включают заголовок `WWW-Authenticate`.

Тип ответа, который будет использоваться, зависит от схемы аутентификации. Хотя может использоваться несколько схем аутентификации, только одна схема может использоваться для определения типа ответа. **Первый класс аутентификации, установленный в представлении, используется при определении типа ответа**.

Обратите внимание, что когда запрос может успешно пройти аутентификацию, но ему все равно будет отказано в разрешении на выполнение запроса, и в этом случае всегда будет использоваться ответ `403 Permission Denied`, независимо от схемы аутентификации.

## Конкретная конфигурация Apache mod_wsgi

Обратите внимание, что при развертывании на [Apache с использованием mod_wsgi][mod_wsgi_official] заголовок авторизации не передается в приложение WSGI по умолчанию, поскольку предполагается, что аутентификация будет выполняться Apache, а не на уровне приложения.

Если вы выполняете развертывание в Apache и используете любую аутентификацию, не основанную на сеансе, вам необходимо явно настроить mod_wsgi для передачи требуемых заголовков в приложение. Это можно сделать, указав директиву `WSGIPassAuthorization` в соответствующем контексте и установив для нее значение `'On'`.

```shell
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On
```

# Справочник по API

## BasicAuthentication

Эта схема аутентификации использует ["HTTP Basic Authentication"][basicauth], подписанную с использованием имени пользователя и пароля. "Basic Authentication" обычно подходит только для тестирования.

В случае успешной аутентификации `BasicAuthentication` предоставляет следующие учетные данные.

* `request.user` будет содержать объект класса `User`.
* `request.auth` будет содержать `None`.

Неаутентифицированные ответы, которым отказано в доступе, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком `WWW-Authenticate`. Например:

```shell
WWW-Authenticate: Basic realm="api"
```

---

**Примечание:** Если вы используете `BasicAuthentication` в производстве, вы должны убедиться, что ваш API доступен только через `https`. Вы также должны убедиться, что ваши клиенты API всегда будут повторно запрашивать имя пользователя и пароль при входе в систему и никогда не сохранят эти данные в постоянном хранилище.

---

## TokenAuthentication

Эта схема аутентификации использует простую схему аутентификации HTTP на основе токенов. Аутентификация по токену подходит для конфигураций клиент-сервер, таких как собственные настольные и мобильные клиенты.

Чтобы использовать схему `TokenAuthentication`, вам необходимо [настроить классы аутентификации](#setting-the-authentication-scheme), чтобы включить `TokenAuthentication`, и дополнительно включить `rest_framework.authtoken` в настройку `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

---

**Примечание:** Не забудьте запустить `manage.py migrate` после изменения настроек. Приложение `rest_framework.authtoken` обеспечивает миграцию базы данных Django.

---

Вам также нужно будет создать токены для ваших пользователей.

```python
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

Для аутентификации клиентов ключ токена должен быть включен в HTTP-заголовок `Authorization`. Ключ должен иметь префикс в виде строкового литерала "Token" с пробелом, разделяющим две строки. Например:

```python
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

**Примечание:** Если вы хотите использовать другое ключевое слово в заголовке, например `Bearer`, просто создайте подкласс `TokenAuthentication` и установите переменную класса `keyword`.

---

В случае успешной аутентификации `TokenAuthentication` предоставляет следующие учетные данные.

* `request.user` будет содержать объект класса `User`.
* `request.auth` будет содержать объект класса `rest_framework.authtoken.models.Token`.

Неаутентифицированные ответы, которым отказано в разрешении, приведут к ответу `HTTP 401 Unauthorized` с соответствующим заголовком `WWW-Authenticate`. Например:

```shell
WWW-Authenticate: Token
```

Инструмент командной строки `curl` может быть полезен для тестирования API с аутентификацией токена. Например:

```shell
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

---

**Примечание:** Если вы используете `TokenAuthentication` в production среде, вы должны убедиться, что ваш API доступен только через `https`.

---

#### Генерирование токенов

##### Используя сигналы

Если вы хотите, чтобы у каждого пользователя был автоматически сгенерированный токен, вы можете просто поймать сигнал пользователя `post_save`.

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

Обратите внимание, что вам нужно убедиться, что вы поместили этот фрагмент кода в установленный модуль `models.py` или в другое место, которое будет импортировано Django при запуске.

Если вы уже создали несколько пользователей, вы можете сгенерировать токены для всех существующих пользователей следующим образом:

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

##### Открывая эндпоинт API

При использовании `TokenAuthentication` вы можете захотеть предоставить клиентам механизм для получения токена с учетом имени пользователя и пароля. REST framework предоставляет встроенное представление для обеспечения такого поведения. Чтобы использовать его, добавьте представление `obtain_auth_token` в ваш URLconf:

```python
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
```

Обратите внимание, что часть URL-адреса шаблона может быть любой, которую вы хотите использовать.

Представление `obtain_auth_token` вернет JSON ответ, когда действительные поля `username` и `password` будут отправлены в представление с использованием данных формы или JSON:

```python
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Обратите внимание, что представление по умолчанию `obtain_auth_token` явно использует запросы и ответы JSON, а не классы рендеринга и парсера по умолчанию в ваших настройках.

По умолчанию к представлению `obtain_auth_token` не применяются разрешения или регулирование. Если вы действительно хотите применить регулирование, вам необходимо переопределить класс представления и включить его с помощью атрибута `throttle_classes`.

Если вам нужна кастомная версия представления `obtain_auth_token`, вы можете сделать это, создав подкласс класса представления `ObtainAuthToken` и вместо этого используя его в своем url conf.

Например, вы можете вернуть дополнительную информацию о пользователе помимо значения `token`:

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

##### С помощью Django Admin

Также возможно создание токенов вручную через интерфейс администратора. В случае, если вы используете большую базу пользователей, мы рекомендуем вам обезьяно пропатчить класс `TokenAdmin`, чтобы настроить его под свои нужды, в частности, объявив поле `user` как `raw_field`.

`your_app/admin.py`:

```python
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

#### Используя команду Django manage.py

Начиная с версии 3.6.4 можно сгенерировать токен пользователя с помощью следующей команды:

```bash
./manage.py drf_create_token <username>
```

Эта команда вернет токен API для данного пользователя, создав его, если он не существует:

```bash
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

Если вы хотите перегенерировать токен (например, если он был взломан или случилась утечка), вы можете передать дополнительный параметр:

```bash
./manage.py drf_create_token -r <username>
```

## SessionAuthentication

В этой схеме аутентификации для аутентификации используется серверная часть сеанса Django по умолчанию. Аутентификация сеанса подходит для клиентов AJAX, которые работают в том же контексте сеанса, что и ваш веб-сайт.

В случае успешной аутентификации `SessionAuthentication` предоставляет следующие учетные данные.

* `request.user` будет содержать объект класса `User`.
* `request.auth` будет содержать `None`.

Неаутентифицированные ответы, которым отказано в разрешении, приведут к ответу `HTTP 403 Forbidden`.

Если вы используете API в стиле AJAX с `SessionAuthentication`, вам необходимо убедиться, что вы включили действительный токен CSRF для любых "небезопасных" вызовов HTTP-методов, таких как `PUT`, `PATCH`, `POST` или `DELETE` запросы. См. [Документацию Django CSRF][csrf-ajax] для получения более подробной информации.

**Предупреждение:** всегда используйте стандартное представление входа в систему Django при создании страниц входа. Это обеспечит надлежащую защиту ваших просмотров входа.

Проверка CSRF в REST framework работает несколько иначе, чем в стандартном Django из-за необходимости поддерживать как сеансовую, так и несессионную аутентификацию в одних и тех же представлениях. Это означает, что только аутентифицированные запросы требуют токенов CSRF, а анонимные запросы могут отправляться без токенов CSRF. Это поведение не подходит для представлений входа в систему, к которым всегда должна применяться проверка CSRF.

## RemoteUserAuthentication

Эта схема аутентификации позволяет вам делегировать аутентификацию вашему веб-серверу, который устанавливает переменную среды `REMOTE_USER`.

Чтобы использовать его, вы должны иметь `django.contrib.auth.backends.RemoteUserBackend` (или подкласс) в настройках `AUTHENTICATION_BACKENDS`. По умолчанию `RemoteUserBackend` создает объекты `User` для имен пользователей, которые еще не существуют. Чтобы изменить это и другое поведение, обратитесь к [документации Django](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/).

В случае успешной аутентификации `RemoteUserAuthentication` предоставляет следующие учетные данные:

* `request.user` будет содержать объект класса `User`.
* `request.auth` будет содержать `None`.

Обратитесь к документации вашего веб-сервера для получения информации о настройке метода аутентификации, например:

* [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
* [NGINX (Restricting Access)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

# Пользовательская аутентификация

Чтобы реализовать настраиваемую схему аутентификации, создайте подкласс `BaseAuthentication` и переопределите метод `.authenticate(self, request)`. Метод должен возвращать кортеж (user, auth), если аутентификация прошла успешно, или `None` в противном случае.

В некоторых случаях вместо возврата `None` вы можете вызвать исключение `AuthenticationFailed` из метода `.authenticate()`.

Обычно вам следует придерживаться следующего подхода:

* Если аутентификация не была предпринята, верните `None`. Любые другие используемые схемы аутентификации по-прежнему будут проверяться.
* Если попытка аутентификации не удалась, вызовите исключение `AuthenticationFailed`. Ответ об ошибке будет возвращен немедленно, независимо от любых проверок разрешений и без проверки каких-либо других схем аутентификации.

Вы также *можете* переопределить метод `.authenticate_header(self, request)`. Если он реализован, он должен возвращать строку, которая будет использоваться в качестве значения заголовка `WWW-Authenticate` в ответе `HTTP 401 Unauthorized`.

Если метод `.authenticate_header()` не переопределен, схема аутентификации будет возвращать ответы `HTTP 403 Forbidden`, когда неаутентифицированному запросу отказано в доступе.

---

**Примечание:** Когда ваш пользовательский аутентификатор вызывается свойствами объекта запроса `.user` или `.auth`, вы можете увидеть `AttributeError`, повторно вызванный как `WrappedAttributeError`. Это необходимо для предотвращения подавления исходного исключения внешним доступом к свойству. Python не распознает, что `AttributeError` исходит от вашего пользовательского аутентификатора, и вместо этого будет предполагать, что объект запроса не имеет свойства `.user` или` .auth`. Эти ошибки должны быть исправлены или обработаны вашим аутентификатором иным образом.

---

## Пример

В следующем примере выполняется аутентификация любого входящего запроса от имени пользователя, заданного именем пользователя в настраиваемом заголовке запроса с именем `X-USERNAME`.

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

# Сторонние пакеты

Также доступны следующие сторонние пакеты.

## Django OAuth Toolkit

Пакет [Django OAuth Toolkit][django-oauth-toolkit] обеспечивает поддержку OAuth 2.0 и работает с Python 3.4+. Пакет поддерживается [Evonove][evonove] и использует превосходную [OAuthLib][oauthlib]. Пакет хорошо документирован, хорошо поддерживается и в настоящее время является нашим **рекомендуемым пакетом для поддержки OAuth 2.0**.

#### Уставнока и настройка

Установите пакет с помощью `pip`.

```bash
pip install django-oauth-toolkit
```

Добавьте пакет в свой `INSTALLED_APPS` и измените настройки вашего REST framework.

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

Дополнительные сведения см. в документации [Django REST framework - Начало работы][django-oauth-toolkit-Getting-started].

## Django REST framework OAuth

Пакет [Django REST framework OAuth][django-rest-framework-oauth] обеспечивает поддержку как OAuth1, так и OAuth2 для REST framework.

Этот пакет ранее был включен непосредственно в REST framework, но теперь поддерживается и поддерживается как сторонний пакет.

#### Installation & configuration

Установите пакет с помощью `pip`.

```bash
pip install djangorestframework-oauth
```

Подробнее о настройке и использовании см. документацию OAuth фреймворка Django REST для [аутентификации][django-rest-framework-oauth-authentication] и [permissions][django-rest-framework-oauth-permissions].

## JSON Web Token Аутентификация

JSON Web Token - это довольно новый стандарт, который можно использовать для аутентификации на основе токенов. В отличие от встроенной схемы `TokenAuthentication`, `JWT Authentication` не требует использования базы данных для проверки токена. Пакет для аутентификации JWT - это [djangorestframework-simplejwt][djangorestframework-simplejwt], который предоставляет некоторые функции, а также приложение с подключаемым черным списком токенов.

## HTTP-аутентификация Hawk

Библиотека [HawkREST][hawkrest] основана на библиотеке [Mohawk][mohawk], чтобы вы могли работать с подписанными запросами и ответами [Hawk][hawk] в вашем API. [Hawk][hawk] позволяет двум сторонам безопасно общаться друг с другом, используя сообщения, подписанные общим ключом. Он основан на [HTTP-аутентификации доступа MAC][mac] (который был основан на частях [OAuth 1.0][oauth-1.0a]).

## Аутентификация подписи HTTP

Подпись HTTP (в настоящее время это [проект IETF][http-signature-ietf-draft]) обеспечивает способ достижения аутентификации источника и целостности сообщений для сообщений HTTP. Подобно [схеме HTTP-подписи Amazon][amazon-http-signature], используемой многими ее службами, она разрешает аутентификацию без сохранения состояния по запросу. [Elvio Toccalino][etoccalino] поддерживает пакет [djangorestframework-httpsignature][djangorestframework-httpsignature] (устаревший), который обеспечивает простой в использовании механизм аутентификации подписи HTTP. Вы можете использовать обновленную версию вилки [djangorestframework-httpsignature][djangorestframework-httpsignature], то есть [drf-httpsig][drf-httpsig].

## Djoser

Библиотека [Djoser][djoser] предоставляет набор представлений для обработки основных действий, таких как регистрация, вход в систему, выход из системы, сброс пароля и активация учетной записи. Пакет работает с настраиваемой моделью пользователя и использует аутентификацию на основе токенов. Это готовая к использованию REST-реализация системы аутентификации Django.

## django-rest-auth / dj-rest-auth

Эта библиотека предоставляет набор конечных точек REST API для регистрации, аутентификации (включая аутентификацию в социальных сетях), сброса пароля, получения и обновления сведений о пользователях и т. Д. Имея эти конечные точки API, ваши клиентские приложения, такие как AngularJS, iOS, Android и другие может независимо общаться с вашим серверным сайтом Django через REST API для управления пользователями.

На данный момент существует два форка этого проекта.

* [Django-rest-auth][django-rest-auth] - оригинальный проект, [но сейчас не получает обновлений](https://github.com/Tivix/django-rest-auth/issues/568).
* [Dj-rest-auth][dj-rest-auth] - новейший форк библиотеки.

## django-rest-framework-social-oauth2

Библиотека [Django-rest-framework-social-oauth2][django-rest-framework-social-oauth2] предоставляет простой способ интеграции социальных плагинов (facebook, twitter, google и т. Д.) В вашу систему аутентификации и простую настройку oauth2. С помощью этой библиотеки вы сможете аутентифицировать пользователей на основе внешних токенов (например, токена доступа к facebook), преобразовывать эти токены во «внутренние» токены oauth2, а также использовать и генерировать токены oauth2 для аутентификации ваших пользователей.

## django-rest-knox

Библиотека [Django-rest-knox][django-rest-knox] предоставляет модели и представления для обработки аутентификации на основе токенов более безопасным и расширяемым способом, чем встроенная схема `TokenAuthentication` - с учетом одностраничных приложений и мобильных клиентов. Он предоставляет токены для каждого клиента и представления для их генерации, когда предоставляется какая-либо другая аутентификация (обычно базовая аутентификация), для удаления токена (обеспечивая принудительный выход из системы с сервера) и для удаления всех токенов (выходит из системы всех клиентов, в которые вошел пользователь).

## drfpasswordless

[drfpasswordless] [drfpasswordless] добавляет (Medium, Square Cash) поддержку без пароля к собственной схеме TokenAuthentication Django REST Framework. Пользователи входят в систему и регистрируются с помощью токена, отправленного в контактную точку, например, на адрес электронной почты или номер мобильного телефона.

[cite]: https://jacobian.org/writing/rest-worst-practices/
[http401]: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2
[http403]: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4
[basicauth]: https://tools.ietf.org/html/rfc2617
[permission]: permissions.md
[throttling]: throttling.md
[csrf-ajax]: https://docs.djangoproject.com/en/stable/ref/csrf/#ajax
[mod_wsgi_official]: https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html
[django-oauth-toolkit-getting-started]: https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html
[django-rest-framework-oauth]: https://jpadilla.github.io/django-rest-framework-oauth/
[django-rest-framework-oauth-authentication]: https://jpadilla.github.io/django-rest-framework-oauth/authentication/
[django-rest-framework-oauth-permissions]: https://jpadilla.github.io/django-rest-framework-oauth/permissions/
[juanriaza]: https://github.com/juanriaza
[djangorestframework-digestauth]: https://github.com/juanriaza/django-rest-framework-digestauth
[oauth-1.0a]: https://oauth.net/core/1.0a/
[django-oauth-toolkit]: https://github.com/evonove/django-oauth-toolkit
[evonove]: https://github.com/evonove/
[oauthlib]: https://github.com/idan/oauthlib
[djangorestframework-simplejwt]: https://github.com/davesque/django-rest-framework-simplejwt
[etoccalino]: https://github.com/etoccalino/
[djangorestframework-httpsignature]: https://github.com/etoccalino/django-rest-framework-httpsignature
[drf-httpsig]: https://github.com/ahknight/drf-httpsig
[amazon-http-signature]: https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
[http-signature-ietf-draft]: https://datatracker.ietf.org/doc/draft-cavage-http-signatures/
[hawkrest]: https://hawkrest.readthedocs.io/en/latest/
[hawk]: https://github.com/hueniverse/hawk
[mohawk]: https://mohawk.readthedocs.io/en/latest/
[mac]: https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05
[djoser]: https://github.com/sunscrapers/djoser
[django-rest-auth]: https://github.com/Tivix/django-rest-auth
[dj-rest-auth]: https://github.com/jazzband/dj-rest-auth
[django-rest-framework-social-oauth2]: https://github.com/PhilipGarnero/django-rest-framework-social-oauth2
[django-rest-knox]: https://github.com/James1345/django-rest-knox
[drfpasswordless]: https://github.com/aaronn/django-rest-framework-passwordless
