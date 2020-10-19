# Разрешения

> Сами по себе аутентификация или идентификация обычно недостаточны для получения доступа к информации или коду. Для этого объект, запрашивающий доступ, должен иметь авторизацию.
>
> — [Apple Developer Documentation][cite]

Вместе с [аутентификацией][authentication] и [регулированием][throttling] разрешения определяют, должен ли запрос быть предоставлен или запрещен доступ.

Проверки разрешений всегда выполняются в самом начале представления, прежде чем будет разрешено выполнение любого другого кода. Проверки разрешений обычно используют информацию аутентификации в свойствах `request.user` и `request.auth`, чтобы определить, следует ли выполнить входящий запрос.

Разрешения используются для предоставления или запрета доступа разным классам пользователей к разным частям API.

Самый простой стиль разрешения - разрешить доступ любому аутентифицированному пользователю и запретить доступ любому неаутентифицированному пользователю. Это соответствует классу `IsAuthenticated` в REST framework.

Чуть менее строгий стиль разрешений - разрешить полный доступ аутентифицированным пользователям, но разрешить доступ только для чтения неаутентифицированным пользователям. Это соответствует классу `IsAuthenticatedOrReadOnly` в REST framework.

## Как определяются разрешения

Разрешения в REST framework всегда определяются как список классов разрешений.

Перед запуском основной части представления проверяется каждое разрешение в списке. Если какая-либо проверка разрешений не удалась, будет возбуждено исключение `exceptions.PermissionDenied` или `exceptions.NotAuthenticated`, и основная часть представления не будет запущена.

Если проверка разрешений завершится неудачно, будет возвращен ответ `403 Forbidden` или `401 Unauthorized` в соответствии со следующими правилами:

* Запрос был успешно аутентифицирован, но в разрешении было отказано. *- будет возвращен ответ `HTTP 403 Forbidden`.*
* Запрос не был успешно аутентифицирован, а класс аутентификации с наивысшим приоритетом * не * использует заголовки `WWW-Authenticate`. *- будет возвращен ответ `HTTP 403 Forbidden`.*
* Запрос не был успешно аутентифицирован, а класс аутентификации с наивысшим приоритетом * использует * заголовки `WWW-Authenticate`. *- Будет возвращен ответ `HTTP 401 Unauthorized` с соответствующим заголовком `WWW-Authenticate`.*

## Разрешения на уровне объекта

Разрешения REST framework также поддерживают разрешение на уровне объекта. Разрешения на уровне объекта используются для определения того, следует ли разрешить пользователю действовать с конкретным объектом, который обычно является экземпляром модели.

Разрешения на уровне объекта выполняются общими представлениями инфраструктуры REST при вызове `.get_object()`. Как и в случае с разрешениями уровня представления, исключение `exceptions.PermissionDenied` будет вызвано, если пользователю не разрешено действовать с данным объектом.

Если вы пишете свои собственные представления и хотите принудительно применять разрешения на уровне объекта, или если вы переопределяете метод `get_object` в общем представлении, вам необходимо явно вызвать метод `.check_object_permissions (request, obj)` для представления в точке, в которой вы извлекли объект.

Это либо вызовет исключение `PermissionDenied`, либо `NotAuthenticated`, либо просто вернется, если представление имеет соответствующие разрешения.

Например:

```python
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
```

---

**Примечание:** За исключением `DjangoObjectPermissions`, предоставленные классы разрешений в `rest_framework.permissions` **не** реализуют методы, необходимые для проверки разрешений объекта.

Если вы хотите использовать предоставленные классы разрешений для проверки прав доступа к объектам, **вы должны** создать подклассы и реализовать метод `has_object_permission()`, описанный в разделе [_Custom permissions_](#custom-permissions) (ниже).

---

#### Ограничения разрешений на уровне объекта

По соображениям производительности общие представления не будут автоматически применять разрешения уровня объекта к каждому экземпляру в наборе запросов при возврате списка объектов.

Часто, когда вы используете разрешения на уровне объекта, вам также нужно [фильтровать набор запросов][filtering] соответствующим образом, чтобы гарантировать, что пользователи видят только те экземпляры, которые им разрешено просматривать.

## Установка политики разрешений

Политика разрешений по умолчанию может быть установлена ​​глобально с помощью параметра `DEFAULT_PERMISSION_CLASSES`. Например.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

Если не указано, по умолчанию этот параметр разрешает неограниченный доступ:

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.AllowAny',
]
```

Вы также можете установить политику аутентификации для каждого представления или набора представлений, используя представления на основе классов `APIView`.

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

Или, если вы используете декоратор `@api_view` с представлениями на основе функций.

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

__Примечание:__ когда вы устанавливаете новые классы разрешений через атрибут класса или декораторы, вы говорите представлению игнорировать список по умолчанию, установленный в файле __settings.py__.

При условии, что они наследуются от `rest_framework.permissions.BasePermission`, разрешения могут быть составлены с использованием стандартных побитовых операторов Python. Например, `IsAuthenticatedOrReadOnly` можно записать:

```python
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ExampleView(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

__Примечание:__ поддерживает `& (and)`, `| (или)` и `~ (не)`.

# Справочник по API

## AllowAny

Класс разрешений `AllowAny` разрешит неограниченный доступ **независимо от того, был ли запрос аутентифицирован или не аутентифицирован**.

Это разрешение не является строго обязательным, поскольку вы можете достичь того же результата, используя пустой список или кортеж для настройки разрешений, но вы можете найти полезным указать этот класс, потому что он делает намерение явным.

## IsAuthenticated

Класс разрешений `IsAuthenticated` откажет в разрешении любому неаутентифицированному пользователю и разрешит разрешение в противном случае.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только зарегистрированным пользователям.

## IsAdminUser

Класс разрешений `IsAdminUser` будет отказывать в разрешении любому пользователю, если только `user.is_staff` не равен `True`, и в этом случае разрешение будет разрешено.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только подмножеству доверенных администраторов.

## IsAuthenticatedOrReadOnly

`IsAuthenticatedOrReadOnly` позволит аутентифицированным пользователям выполнять любой запрос. Запросы для неавторизованных пользователей будут разрешены только в том случае, если метод запроса является одним из «безопасных» методов: `GET`, `HEAD` или `OPTIONS`.

Это разрешение подходит, если вы хотите, чтобы ваш API разрешал чтение анонимным пользователям и разрешал запись только аутентифицированным пользователям.

## DjangoModelPermissions

Этот класс разрешений связан со стандартным Django `django.contrib.auth` [разрешения модели][contribauth]. Это разрешение должно применяться только к представлениям, у которых установлено свойство `.queryset`. Авторизация будет предоставлена ​​только в том случае, если пользователь *аутентифицирован* и ему назначены *соответствующие разрешения модели*.

* Запросы `POST` требуют, чтобы у пользователя было право `add` на модель.
* Запросы `PUT` и `PATCH` требуют, чтобы у пользователя было право `change` модели.
* Запросы `DELETE` требуют, чтобы у пользователя было право `delete` модели.

Поведение по умолчанию также можно переопределить для поддержки разрешений настраиваемой модели. Например, вы можете захотеть включить разрешение модели `view` для запросов `GET`.

Чтобы использовать разрешения пользовательской модели, переопределите `DjangoModelPermissions` и установите свойство `.perms_map`. За подробностями обращайтесь к исходному коду.

#### Использование с представлениями, не содержащими атрибут `queryset`.

Если вы используете это разрешение с представлением, в котором используется переопределенный метод `get_queryset()`, то в представлении может не быть атрибута `queryset`. В этом случае мы предлагаем также пометить представление контрольным набором запросов, чтобы этот класс мог определить необходимые разрешения. Например:

```python
queryset = User.objects.none()  # Required for DjangoModelPermissions
```

## DjangoModelPermissionsOrAnonReadOnly

Подобно `DjangoModelPermissions`, но также позволяет неаутентифицированным пользователям иметь доступ только для чтения к API.

## DjangoObjectPermissions

Этот класс разрешений связан со стандартной [структурой разрешений объектов][objectpermissions] Django, которая разрешает разрешения для каждого объекта в моделях. Чтобы использовать этот класс разрешений, вам также необходимо добавить серверную часть разрешений, которая поддерживает разрешения на уровне объектов, например [django-guardian][guardian].

Как и в случае `DjangoModelPermissions`, это разрешение должно применяться только к представлениям, имеющим свойство `.queryset` или метод `.get_queryset()`. Авторизация будет предоставлена ​​только в том случае, если пользователь *аутентифицирован* и имеет *соответствующие разрешения для каждого объекта* и *соответствующие разрешения модели*.

* Запросы `POST` требуют, чтобы у пользователя было право `add` на объект модели.
* Запросы `PUT` и `PATCH` требуют, чтобы у пользователя было право `change` на объект модели.
* Запросы `DELETE` требуют, чтобы у пользователя было право `delete` на объект модели.

Обратите внимание, что `DjangoObjectPermissions` **не требует** пакета `django-guardian` и должен поддерживать другие серверные части объектного уровня одинаково хорошо.

Как и в случае с `DjangoModelPermissions`, вы можете использовать пользовательские разрешения модели, переопределив `DjangoObjectPermissions` и установив свойство `.perms_map`. За подробностями обращайтесь к исходному коду.

---

**Примечание**: Если вам нужны разрешения `view` на уровне объекта для запросов `GET`, `HEAD` и `OPTIONS` и вы используете django-guardian для своей серверной части разрешений на уровне объекта, вам следует рассмотреть возможность использования Класс `DjangoObjectPermissionsFilter`, предоставляемый [пакетом `djangorestframework-guardian`][django-rest-framework-guardian]. Это гарантирует, что конечные точки списка возвращают только результаты, включая объекты, для которых у пользователя есть соответствующие разрешения на просмотр.

---

# Пользовательские разрешения

Чтобы реализовать настраиваемое разрешение, переопределите `BasePermission` и реализуйте один или оба из следующих методов:

* `.has_permission(self, request, view)`
* `.has_object_permission(self, request, view, obj)`

Методы должны возвращать `True`, если запросу должен быть предоставлен доступ, и `False` в противном случае.

Если вам нужно проверить, является ли запрос операцией чтения или записи, вы должны проверить метод запроса на соответствие константе `SAFE_METHODS`, которая представляет собой кортеж, содержащий `'GET'`, `'OPTIONS'` и `'HEAD'`. Например:

```python
if request.method in permissions.SAFE_METHODS:
    # Check permissions for read-only request
else:
    # Check permissions for write request
```

---

**Примечание**: метод `has_object_permission` на уровне экземпляра будет вызываться только в том случае, если проверки `has_permission` на уровне представления уже прошли. Также обратите внимание, что для запуска проверок на уровне экземпляра код представления должен явно вызывать `.check_object_permissions(request, obj)`. Если вы используете общие представления, это будет сделано за вас по умолчанию. (Представления на основе функций должны будут явно проверять права доступа к объектам, вызывая `PermissionDenied` в случае ошибки.)

---

Пользовательские разрешения вызовут исключение `PermissionDenied`, если тест не пройден. Чтобы изменить сообщение об ошибке, связанное с исключением, реализуйте атрибут `message` непосредственно в вашем настраиваемом разрешении. В противном случае будет использован атрибут `default_detail` из `PermissionDenied`. Точно так же, чтобы изменить идентификатор кода, связанный с исключением, реализуйте атрибут `code` непосредственно в вашем настраиваемом разрешении - в противном случае будет использоваться атрибут` default_code` из `PermissionDenied`.

```python
from rest_framework import permissions

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
            ...
```

## Examples

Ниже приведен пример класса разрешений, который проверяет IP-адрес входящего запроса по списку блокировки и отклоняет запрос, если IP-адрес был заблокирован.

```python
from rest_framework import permissions

class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        return not blocked
```

Помимо глобальных разрешений, которые выполняются для всех входящих запросов, вы также можете создавать разрешения на уровне объекта, которые выполняются только для операций, влияющих на конкретный экземпляр объекта. Например:

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```

Обратите внимание, что общие представления будут проверять соответствующие разрешения на уровне объекта, но если вы пишете свои собственные настраиваемые представления, вам необходимо убедиться, что вы сами проверяете проверки разрешений на уровне объекта. Вы можете сделать это, вызвав `self.check_object_permissions(request, obj)` из представления, когда у вас есть экземпляр объекта. Этот вызов вызовет соответствующее исключение `APIException`, если какая-либо проверка разрешений на уровне объекта завершится неудачно, и в противном случае просто вернется.

Также обратите внимание, что общие представления будут проверять разрешения на уровне объекта только для представлений, которые получают один экземпляр модели. Если вам требуется фильтрация представлений списков на уровне объекта, вам необходимо отфильтровать набор запросов отдельно. см. [Документацию по фильтрации][filtering] для получения более подробной информации.

# Сторонние пакеты

Также доступны следующие сторонние пакеты.

## DRF - Access policy

Пакет [Django REST - Access policy][drf-access-policy] предоставляет способ определения сложных правил доступа в классах декларативных политик, которые прикреплены к наборам представлений или представлениям на основе функций. Политики определены в JSON в формате, аналогичном политикам `AWS Identity & Access Management`.

## Composed Permissions

Пакет [Composed Permissions][formed-permissions] предоставляет простой способ определения сложных и многоуровневых (с логическими операторами) объектов разрешений с использованием небольших и повторно используемых компонентов.

## REST Condition

Пакет [REST Condition][rest-condition] - еще одно расширение для создания сложных разрешений простым и удобным способом. Расширение позволяет комбинировать разрешения с логическими операторами.

## DRY Rest Permissions

Пакет [DRY Rest Permissions][dry-rest-permissions] предоставляет возможность определять различные разрешения для отдельных действий по умолчанию и настраиваемых действий. Этот пакет предназначен для приложений с разрешениями, производными от отношений, определенных в модели данных приложения. Он также поддерживает проверку разрешений, возвращаемую клиентскому приложению через сериализатор API. Кроме того, он поддерживает добавление разрешений к действиям по умолчанию и настраиваемым спискам, чтобы ограничить данные, которые они получают для каждого пользователя.

## Django Rest Framework Roles

Пакет [Django Rest Framework Roles][django-rest-framework-roles] упрощает параметризацию вашего API для разных типов пользователей.

## Django REST Framework API Key

Пакет [Django REST Framework API Key][djangorestframework-api-key] предоставляет классы разрешений, модели и помощников для добавления авторизации ключа API в ваш API. Его можно использовать для авторизации внутренних или сторонних серверных программ и служб (например, _machines_), у которых нет учетной записи пользователя. Ключи API надежно хранятся с использованием инфраструктуры хеширования паролей Django, и их можно просмотреть, отредактировать и отозвать в любое время в администраторе Django.

## Django Rest Framework Role Filters

Пакет [Django Rest Framework Role Filters][django-rest-framework-role-filters] обеспечивает простую фильтрацию по нескольким типам ролей.

## Django Rest Framework PSQ

Пакет [Django Rest Framework PSQ][drf-psq] - это расширение, обеспечивающее поддержку **классов разрешений** на основе действий, **класс_сериализатора** и **набора запросов** в зависимости от правил на основе разрешений.

[cite]: https://developer.apple.com/library/mac/#documentation/security/Conceptual/AuthenticationAndAuthorizationGuide/Authorization/Authorization.html
[authentication]: authentication.md
[throttling]: throttling.md
[filtering]: filtering.md
[contribauth]: https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions
[objectpermissions]: https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions
[guardian]: https://github.com/lukaszb/django-guardian
[filtering]: filtering.md
[composed-permissions]: https://github.com/niwibe/djangorestframework-composed-permissions
[rest-condition]: https://github.com/caxap/rest_condition
[dry-rest-permissions]: https://github.com/FJNR-inc/dry-rest-permissions
[django-rest-framework-roles]: https://github.com/computer-lab/django-rest-framework-roles
[djangorestframework-api-key]: https://florimondmanca.github.io/djangorestframework-api-key/
[django-rest-framework-role-filters]: https://github.com/allisson/django-rest-framework-role-filters
[django-rest-framework-guardian]: https://github.com/rpkilby/django-rest-framework-guardian
[drf-access-policy]: https://github.com/rsinger86/drf-access-policy
[drf-psq]: https://github.com/drf-psq/drf-psq
