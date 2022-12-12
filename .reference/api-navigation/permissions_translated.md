<!-- TRANSLATED by md-translate -->
---

source:

источник:

* permissions.py

* Permissions.py

---

# Permissions

# Разрешения

> Authentication or identification by itself is not usually sufficient to gain access to information or code. For that, the entity requesting access must have authorization.
>
> — [Apple Developer Documentation](https://developer.apple.com/library/mac/#documentation/security/Conceptual/AuthenticationAndAuthorizationGuide/Authorization/Authorization.html)

> Аутентификация или идентификация сама по себе обычно недостаточно для получения доступа к информации или коду.
Для этого объект, запрашивающий доступ, должен иметь разрешение.
>
> - [Документация Apple Developer] (https://developer.apple.com/library/mac/#documentation/security/conceptual/authenticationandAuthorizationguide/authorization/authorization.html)

Together with [authentication](authentication.md) and [throttling](throttling.md), permissions determine whether a request should be granted or denied access.

Вместе с [аутентификацией] (аутентификация.md) и [Throttling] (Throttling.md) разрешения определяют, должен ли запрос быть предоставлен или отказ в доступе.

Permission checks are always run at the very start of the view, before any other code is allowed to proceed. Permission checks will typically use the authentication information in the `request.user` and `request.auth` properties to determine if the incoming request should be permitted.

Проверки разрешений всегда выполняются с самого начала представления, прежде чем любой другой код будет разрешен.
Проверки разрешений обычно используют информацию о аутентификации в свойствах `request.user` и` request.auth`, чтобы определить, должен ли входящий запрос быть разрешен.

Permissions are used to grant or deny access for different classes of users to different parts of the API.

Разрешения используются для предоставления или отказа в доступе для различных классов пользователей в разные части API.

The simplest style of permission would be to allow access to any authenticated user, and deny access to any unauthenticated user. This corresponds to the `IsAuthenticated` class in REST framework.

Самый простой стиль разрешения - разрешить доступ к любому аутентифицированному пользователю и отказать в доступе к любому несанкционированному пользователю.
Это соответствует классу `isauthenticated` в рамках REST.

A slightly less strict style of permission would be to allow full access to authenticated users, but allow read-only access to unauthenticated users. This corresponds to the `IsAuthenticatedOrReadOnly` class in REST framework.

Немного менее строгий стиль разрешения заключается в том, чтобы позволить полный доступ к аутентифицированным пользователям, но предоставление доступ к чтению только для пользователей.
Это соответствует классу `isauthenticatedordeReadonly` в рамках REST.

## How permissions are determined

## Как определяются разрешения

Permissions in REST framework are always defined as a list of permission classes.

Разрешения в структуре REST всегда определяются как список классов разрешений.

Before running the main body of the view each permission in the list is checked. If any permission check fails, an `exceptions.PermissionDenied` or `exceptions.NotAuthenticated` exception will be raised, and the main body of the view will not run.

Перед запуском основного тела представления каждое разрешение в списке проверяется.
Если какая -либо проверка разрешений не удастся, будет поднято исключение `exceptions.permissionedied` или` exceptions.notauthenticated`, а основная часть представления не будет работать.

When the permission checks fail, either a "403 Forbidden" or a "401 Unauthorized" response will be returned, according to the following rules:

Когда проверки разрешения не сняты, либо «запрещен» 403, либо «401 несанкционированный» ответ будет возвращен в соответствии со следующими правилами:

* The request was successfully authenticated, but permission was denied. *— An HTTP 403 Forbidden response will be returned.*
* The request was not successfully authenticated, and the highest priority authentication class *does not* use `WWW-Authenticate` headers. *— An HTTP 403 Forbidden response will be returned.*
* The request was not successfully authenticated, and the highest priority authentication class *does* use `WWW-Authenticate` headers. *— An HTTP 401 Unauthorized response, with an appropriate `WWW-Authenticate` header will be returned.*

* Запрос был успешно аутентифицирован, но разрешение было отклонено.
* - Запретный ответ HTTP 403 будет возвращен.*
* Запрос не был успешно аутентифицирован, а самый высокий класс аутентификации * не использует `www-authenticate` заголовков.
* - Запретный ответ HTTP 403 будет возвращен.*
* Запрос не был успешно аутентифицирован, и самый высокий класс аутентификации * с наивысшим приоритетом * использует заголовки www-authenticate`.
*-Несанкционированный ответ HTTP 401 с соответствующим заголовком `www-authenticate` будет возвращен.*

## Object level permissions

## разрешения уровня объекта

REST framework permissions also support object-level permissioning. Object level permissions are used to determine if a user should be allowed to act on a particular object, which will typically be a model instance.

Разрешения на основе REST также поддерживают разрешение на уровне объекта.
Разрешения на уровне объектов используются для определения того, разрешено ли пользователю действовать на конкретный объект, который обычно будет экземпляром модели.

Object level permissions are run by REST framework's generic views when `.get_object()` is called. As with view level permissions, an `exceptions.PermissionDenied` exception will be raised if the user is not allowed to act on the given object.

Разрешения на уровне объектов выполняются общими представлениями REST Framework, когда называется `.get_object ()`.
Как и в случае с разрешениями на уровень просмотра, исключение `exceptions.permissionDiened` будет повышено, если пользователю не разрешается действовать на данном объекте.

If you're writing your own views and want to enforce object level permissions, or if you override the `get_object` method on a generic view, then you'll need to explicitly call the `.check_object_permissions(request, obj)` method on the view at the point at which you've retrieved the object.

Если вы пишете свои собственные представления и хотите обеспечить разрешения на уровень объектов, или если вы переопределяете метод `get_object` в общем представлении, вам нужно явно вызвать метод.
Вид в точке, в котором вы взяли объект.

This will either raise a `PermissionDenied` or `NotAuthenticated` exception, or simply return if the view has the appropriate permissions.

Это либо поднимет исключение «разрешение» или «нет», либо просто вернется, если представление имеет соответствующие разрешения.

For example:

Например:

```
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
```

---

**Note**: With the exception of `DjangoObjectPermissions`, the provided permission classes in `rest_framework.permissions` **do not** implement the methods necessary to check object permissions.

** ПРИМЕЧАНИЕ **: За исключением `djangoobjectpermissions`, предоставленные классы разрешений в` rest_framework.permissions` ** Не ** реализуйте методы, необходимые для проверки разрешений объекта.

If you wish to use the provided permission classes in order to check object permissions, **you must** subclass them and implement the `has_object_permission()` method described in the [*Custom permissions*](#custom-permissions) section (below).

Если вы хотите использовать предоставленные классы разрешений, чтобы проверить разрешения объекта, ** вы должны ** подкласс и реализовать метод `has_object_permission ()`, описанный в разделе [*Пользовательские разрешения*] (#custom-permissions) (
ниже).

---

#### Limitations of object level permissions

#### Ограничения разрешений на уровень объекта

For performance reasons the generic views will not automatically apply object level permissions to each instance in a queryset when returning a list of objects.

По причинам производительности общие представления не будут автоматически применять разрешения на уровень объекта к каждому экземпляру в запросе при возврате списка объектов.

Often when you're using object level permissions you'll also want to [filter the queryset](filtering.md) appropriately, to ensure that users only have visibility onto instances that they are permitted to view.

Часто, когда вы используете разрешения на уровень объекта, вы также захотите [отфильтровать Queryset] (Filtering.md) соответствующим образом, чтобы убедиться, что пользователи имеют видимость только на случаи, которые им разрешено просмотреть.

Because the `get_object()` method is not called, object level permissions from the `has_object_permission()` method **are not applied** when creating objects. In order to restrict object creation you need to implement the permission check either in your Serializer class or override the `perform_create()` method of your ViewSet class.

Поскольку метод `get_object ()` не вызывается, разрешения уровня объекта из метода `has_object_permission ()` ** не применяются ** при создании объектов.
Чтобы ограничить создание объектов, вам необходимо реализовать проверку разрешений в своем классе сериализатора или переопределить метод `recement_create ()` `` `метод вашего класса Viewset.

## Setting the permission policy

## Установка политики разрешения

The default permission policy may be set globally, using the `DEFAULT_PERMISSION_CLASSES` setting. For example.

Политика разрешения по умолчанию может быть установлена по всему миру, используя настройку `default_permission_classes`.
Например.

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

If not specified, this setting defaults to allowing unrestricted access:

Если не указано, этот настройка по умолчанию разрешает неограниченный доступ:

```
'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
]
```

You can also set the authentication policy on a per-view, or per-viewset basis, using the `APIView` class-based views.

Вы также можете установить политику аутентификации на основе для каждого вида или на основе для на расстоянии, используя представления на основе класса Apiview`.

```
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

Or, if you're using the `@api_view` decorator with function based views.

Или, если вы используете декоратор `@api_view` с видами на основе функций.

```
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

**Note:** when you set new permission classes via the class attribute or decorators you're telling the view to ignore the default list set in the **settings.py** file.

** ПРИМЕЧАНИЕ. ** Когда вы устанавливаете новые классы разрешений через атрибут класса или декораторы.

Provided they inherit from `rest_framework.permissions.BasePermission`, permissions can be composed using standard Python bitwise operators. For example, `IsAuthenticatedOrReadOnly` could be written:

При условии, что они наследуют от `rest_framework.permissions.basepermission`, разрешения могут быть составлены с использованием стандартных операторов Python Bitwise.
Например, можно было бы написать: `isauthatecutedOrreadonly`:

```
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

**Note:** it supports & (and), | (or) and ~ (not).

** ПРИМЕЧАНИЕ: ** Он поддерживает и (и), |
(или) и ~ (нет).

---

# API Reference

# Ссылка на API

## AllowAny

## Allowany

The `AllowAny` permission class will allow unrestricted access, **regardless of if the request was authenticated or unauthenticated**.

Класс разрешений «разрешить» разрешит неограниченный доступ, ** независимо от того, был ли запрос аутентифицирован или неавентентирован **.

This permission is not strictly required, since you can achieve the same result by using an empty list or tuple for the permissions setting, but you may find it useful to specify this class because it makes the intention explicit.

Это разрешение не требуется строго, поскольку вы можете достичь того же результата, используя пустой список или кортеж для настройки разрешений, но вы можете найти полезным для указания этого класса, поскольку оно делает намерение явным.

## IsAuthenticated

## isauthenticated

The `IsAuthenticated` permission class will deny permission to any unauthenticated user, and allow permission otherwise.

Класс разрешений `isauthenticated` отрицает разрешение любому неавтотимированному пользователю и в противном случае разрешает разрешение.

This permission is suitable if you want your API to only be accessible to registered users.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только для зарегистрированных пользователей.

## IsAdminUser

## Исадминусер

The `IsAdminUser` permission class will deny permission to any user, unless `user.is_staff` is `True` in which case permission will be allowed.

Класс разрешений `isadminuser` будет отрицать разрешение любому пользователю, если только` user.is_staff` не является `true`, в этом случае разрешение будет разрешено.

This permission is suitable if you want your API to only be accessible to a subset of trusted administrators.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только для подмножества надежных администраторов.

## IsAuthenticatedOrReadOnly

## isauthenticatedOrreadonly

The `IsAuthenticatedOrReadOnly` will allow authenticated users to perform any request. Requests for unauthorised users will only be permitted if the request method is one of the "safe" methods; `GET`, `HEAD` or `OPTIONS`.

`IsauthenticatedOrreadonly` позволит пользователям аутентифицированного выполнения любого запроса.
Запросы на несанкционированных пользователей будут разрешены только в том случае, если метод запроса является одним из «безопасных» методов;
`Get ',` head' или `options '.

This permission is suitable if you want to your API to allow read permissions to anonymous users, and only allow write permissions to authenticated users.

Это разрешение подходит, если вы хотите, чтобы ваш API разрешил разрешения на чтение анонимным пользователям, и разрешают только разрешения на запись для аутентификации пользователей.

## DjangoModelPermissions

## djangomodelpermissions

This permission class ties into Django's standard `django.contrib.auth` [model permissions](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions). This permission must only be applied to views that have a `.queryset` property or `get_queryset()` method. Authorization will only be granted if the user *is authenticated* and has the *relevant model permissions* assigned. The appropriate model is determined by checking `get_queryset().model` or `queryset.model`.

Этот класс разрешений связывается с стандартом Django `django.contrib.auth` [Model Perforces] (https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions).
Это разрешение должно применяться только к представлениям, которые имеют свойство `.queryset` или метод` get_queryset () `.
Авторизация будет предоставлена только в том случае, если пользователь * аутентифицирован * и имеет * соответствующие разрешения модели * назначены.
Соответствующая модель определяется путем проверки `get_queryset (). Model` или` Queryset.model`.

* `POST` requests require the user to have the `add` permission on the model.
* `PUT` and `PATCH` requests require the user to have the `change` permission on the model.
* `DELETE` requests require the user to have the `delete` permission on the model.

* `Запросы post` требуют, чтобы пользователь имел разрешение` добавить `на модели.
* `` Put` и `запросы Patch` требуют, чтобы пользователь имел разрешение на изменение" на модели.
* `Запросы Delete` требуют, чтобы пользователь имел разрешение` delete` на модели.

The default behavior can also be overridden to support custom model permissions. For example, you might want to include a `view` model permission for `GET` requests.

Поведение по умолчанию также может быть переопределено для поддержки пользовательских разрешений модели.
Например, вы можете включить разрешение на модель View` для запросов `get '.

To use custom model permissions, override `DjangoModelPermissions` and set the `.perms_map` property. Refer to the source code for details.

Чтобы использовать пользовательские разрешения модели, переопределите `djangomodelpermissions` и установите свойство` .perms_map`.
Обратитесь к исходному коду для деталей.

## DjangoModelPermissionsOrAnonReadOnly

## djangomodelpermissionsoranOnreadonly

Similar to `DjangoModelPermissions`, but also allows unauthenticated users to have read-only access to the API.

Подобно «djangodelpermissions», но также позволяет неаутентированным пользователям иметь доступ только для чтения к API.

## DjangoObjectPermissions

## djangoobjectpermissions

This permission class ties into Django's standard [object permissions framework](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions) that allows per-object permissions on models. In order to use this permission class, you'll also need to add a permission backend that supports object-level permissions, such as [django-guardian](https://github.com/lukaszb/django-guardian).

Этот класс разрешений связан с стандартом Django [Framework разрешения объекта] (https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions), что позволяет pers-lepject разрешения на модели.
Чтобы использовать этот класс разрешений, вам также необходимо добавить бэкэнд разрешения, который поддерживает разрешения на уровне объектов, такие как [django-guardian] (https://github.com/lukaszb/django-guardian).

As with `DjangoModelPermissions`, this permission must only be applied to views that have a `.queryset` property or `.get_queryset()` method. Authorization will only be granted if the user *is authenticated* and has the *relevant per-object permissions* and *relevant model permissions* assigned.

Как и в случае с `djangomodelpermissions`, это разрешение должно применяться только к представлениям, которые имеют свойство` .Queryset` или `.get_queryset ()` метод.
Авторизация будет предоставлена только в том случае, если пользователь * аутентифицирован * и имеет * соответствующие разрешения на каждое объект * и * соответствующие разрешения модели * назначены.

* `POST` requests require the user to have the `add` permission on the model instance.
* `PUT` and `PATCH` requests require the user to have the `change` permission on the model instance.
* `DELETE` requests require the user to have the `delete` permission on the model instance.

* `Запросы post` требуют, чтобы пользователь имел разрешение` добавить `на экземпляре модели.
* `` Put` и `запросы Patch` требуют, чтобы пользователь имел разрешение` readment 'в экземпляре модели.
* `Запросы Delete` требуют, чтобы пользователь имел разрешение` delete` в экземпляре модели.

Note that `DjangoObjectPermissions` **does not** require the `django-guardian` package, and should support other object-level backends equally well.

Обратите внимание, что `djangoobjectpermissions` ** не требует пакета« django-guardian »и должен поддерживать другие бэкэнды на уровне объекта в равной степени.

As with `DjangoModelPermissions` you can use custom model permissions by overriding `DjangoObjectPermissions` and setting the `.perms_map` property. Refer to the source code for details.

Как и в случае с `djangomodelpermissions`, вы можете использовать пользовательские разрешения модели, переопределяя« djangoobjectpermissions »и установив свойство` .perms_map`.
Обратитесь к исходному коду для деталей.

---

**Note**: If you need object level `view` permissions for `GET`, `HEAD` and `OPTIONS` requests and are using django-guardian for your object-level permissions backend, you'll want to consider using the `DjangoObjectPermissionsFilter` class provided by the [`djangorestframework-guardian` package](https://github.com/rpkilby/django-rest-framework-guardian). It ensures that list endpoints only return results including objects for which the user has appropriate view permissions.

** Примечание **: Если вам нужны уровень объекта `wiew` разрешения для запросов` get`, `have` и` `` и используют Django-Guardian для вашего бэкэнда разрешений на уровне объекта, вам захотите рассмотреть возможность использования
`Djangoobjectpermissionsfilter` класс, предоставленный [` `djangorestframework-guardian` package] (https://github.com/rpkilby/django-rest-framework-guardian).
Это гарантирует, что списки конечных точек возвращают только результаты, включая объекты, для которых пользователь имеет соответствующие разрешения на представление.

---

# Custom permissions

# Пользовательские разрешения

To implement a custom permission, override `BasePermission` and implement either, or both, of the following methods:

Чтобы реализовать пользовательское разрешение, переопределить `basepemission` и реализовать либо или обоих следующих методов:

* `.has_permission(self, request, view)`
* `.has_object_permission(self, request, view, obj)`

* `.has_permission (self, запрос, просмотр)`
* `.has_object_permission (Self, запрос, просмотр, obj)`

The methods should return `True` if the request should be granted access, and `False` otherwise.

Методы должны вернуть `true`, если запрос должен быть предоставлен доступ, и в противном случае« false ».

If you need to test if a request is a read operation or a write operation, you should check the request method against the constant `SAFE_METHODS`, which is a tuple containing `'GET'`, `'OPTIONS'` and `'HEAD'`. For example:

Если вам нужно проверить, является ли запрос операцией чтения или операцией записи, вам следует проверить метод запроса на постоянный `safe_methods`, который является кортежом, содержащим` 'get'`, `' aptions 'и` ’Head
'.
Например:

```
if request.method in permissions.SAFE_METHODS:
    # Check permissions for read-only request
else:
    # Check permissions for write request
```

---

**Note**: The instance-level `has_object_permission` method will only be called if the view-level `has_permission` checks have already passed. Also note that in order for the instance-level checks to run, the view code should explicitly call `.check_object_permissions(request, obj)`. If you are using the generic views then this will be handled for you by default. (Function-based views will need to check object permissions explicitly, raising `PermissionDenied` on failure.)

** Примечание **: метод уровня экземпляра `has_object_permission` будет вызван только если проверки на уровне представления` has_permission` уже прошли.
Также обратите внимание, что для запуска проверки на уровне экземпляра код представления должен явно вызовать `.check_object_permissions (запрос, OBJ)`.
Если вы используете общие представления, это будет обрабатываться для вас по умолчанию.
(Основанные на функциях представления должны будут явно проверять разрешения объекта, повышая `разрешение на сбой.)

---

Custom permissions will raise a `PermissionDenied` exception if the test fails. To change the error message associated with the exception, implement a `message` attribute directly on your custom permission. Otherwise the `default_detail` attribute from `PermissionDenied` will be used. Similarly, to change the code identifier associated with the exception, implement a `code` attribute directly on your custom permission - otherwise the `default_code` attribute from `PermissionDenied` will be used.

Пользовательские разрешения приведут к исключению `romissiondenied`, если тест не удастся.
Чтобы изменить сообщение об ошибке, связанное с исключением, реализуйте атрибут «Сообщение» непосредственно в своем пользовательском разрешении.
В противном случае будет использоваться атрибут `default_detail
Аналогичным образом, чтобы изменить идентификатор кода, связанный с исключением, реализуйте атрибут «кода» непосредственно на вашем пользовательском разрешении - в противном случае будет использоваться атрибут `default_code` от` romsissionDied`.

```
from rest_framework import permissions

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
         ...
```

## Examples

## Примеры

The following is an example of a permission class that checks the incoming request's IP address against a blocklist, and denies the request if the IP has been blocked.

Ниже приведен пример класса разрешений, который проверяет IP -адрес входящего запроса по сравнению с блоком -списком, и отрицает запрос, если IP был заблокирован.

```
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

As well as global permissions, that are run against all incoming requests, you can also create object-level permissions, that are only run against operations that affect a particular object instance. For example:

Помимо глобальных разрешений, которые выполняются против всех входящих запросов, вы также можете создавать разрешения на уровне объектов, которые выполняются только против операций, которые влияют на конкретный экземпляр объекта.
Например:

```
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

Note that the generic views will check the appropriate object level permissions, but if you're writing your own custom views, you'll need to make sure you check the object level permission checks yourself. You can do so by calling `self.check_object_permissions(request, obj)` from the view once you have the object instance. This call will raise an appropriate `APIException` if any object-level permission checks fail, and will otherwise simply return.

Обратите внимание, что общие представления будут проверять соответствующие разрешения на уровень объекта, но если вы пишете свои собственные представления, вам нужно убедиться, что вы проверяете сами проверять разрешение на уровне объекта.
Вы можете сделать это, вызывая `self.check_object_permissions (запрос, obj)` из представления, как только у вас есть экземпляр объекта.
Этот вызов поднимет соответствующий `apiexception`, если какие-либо проверки на уровне объекта не удастся, и в противном случае просто вернется.

Also note that the generic views will only check the object-level permissions for views that retrieve a single model instance. If you require object-level filtering of list views, you'll need to filter the queryset separately. See the [filtering documentation](filtering.md) for more details.

Также обратите внимание, что общие представления будут проверять разрешения на уровне объекта только для представлений, которые получают один экземпляр модели.
Если вам требуется фильтрация на уровне объекта представлений списков, вам нужно отфильтровать запрос отдельно.
См. Документацию [Фильтрация] (Filtering.md) для получения более подробной информации.

# Overview of access restriction methods

# Обзор методов ограничения доступа

REST framework offers three different methods to customize access restrictions on a case-by-case basis. These apply in different scenarios and have different effects and limitations.

Framework REST предлагает три различных метода для настройки ограничений доступа в каждом конкретном случае.
Они применяются в разных сценариях и имеют разные эффекты и ограничения.

* `queryset`/`get_queryset()`: Limits the general visibility of existing objects from the database. The queryset limits which objects will be listed and which objects can be modified or deleted. The `get_queryset()` method can apply different querysets based on the current action.
* `permission_classes`/`get_permissions()`: General permission checks based on the current action, request and targeted object. Object level permissions can only be applied to retrieve, modify and deletion actions. Permission checks for list and create will be applied to the entire object type. (In case of list: subject to restrictions in the queryset.)
* `serializer_class`/`get_serializer()`: Instance level restrictions that apply to all objects on input and output. The serializer may have access to the request context. The `get_serializer()` method can apply different serializers based on the current action.

* `Queryset`/` get_queryset () `: ограничивает общую видимость существующих объектов из базы данных.
Ограничение запроса, которые будут перечислены объекты и какие объекты могут быть изменены или удалены.
Метод `get_queryset ()` может применять различные запросы на основе текущего действия.
* `rescision_class`/` get_permissions () `: Общие проверки разрешений на основе текущего действия, запроса и целевого объекта.
Разрешения на уровне объектов могут применяться только для извлечения, изменения и удаления действий.
Проверка разрешений на список и создание будет применяться ко всему типу объекта.
(В случае списка: с учетом ограничений в запросе.)
* `serializer_class`/` get_serializer () `: Ограничения уровня экземпляра, которые применяются ко всем объектам при вводе и выводе.
Сериализатор может иметь доступ к контексту запроса.
Метод `get_serializer ()` может применять различные сериализаторы на основе текущего действия.

The following table lists the access restriction methods and the level of control they offer over which actions.

В следующей таблице перечислены методы ограничения доступа и уровень контроля, который они предлагают, на каких действиях.

|                                   | `queryset` | `permission_classes` | `serializer_class` |
| --------------------------------- | ---------- | -------------------- | ------------------ |
| Action: list                      | global     | global               | object-level*     |
| Action: create                    | no         | global               | object-level       |
| Action: retrieve                  | global     | object-level         | object-level       |
| Action: update                    | global     | object-level         | object-level       |
| Action: partial_update            | global     | object-level         | object-level       |
| Action: destroy                   | global     | object-level         | no                 |
| Can reference action in decision  | no**     | yes                  | no**             |
| Can reference request in decision | no**     | yes                  | yes                |

|
|
`Queryset` |
`разрешение_классес '|
`serializer_class` |
|
--------------------------------- |
---------- |
-------------------- |
------------------ |
|
Действие: список |
глобальный |
глобальный |
Уровень объекта* |
|
Действие: Создать |
Нет |
глобальный |
Уровень объекта |
|
Действие: Получить |
глобальный |
Уровень объекта |
Уровень объекта |
|
Действие: обновление |
глобальный |
Уровень объекта |
Уровень объекта |
|
Действие: partial_update |
глобальный |
Уровень объекта |
Уровень объекта |
|
Действие: уничтожить |
глобальный |
Уровень объекта |
Нет |
|
Может ссылаться на действие в решении |
Нет ** |
Да |
Нет ** |
|
Может ссылаться на запрос в решении |
Нет ** |
Да |
Да |

* A Serializer class should not raise PermissionDenied in a list action, or the entire list would not be returned. <br> ** The `get_*()` methods have access to the current view and can return different Serializer or QuerySet instances based on the request or action.

* Класс сериализатора не должен повышать разрешение в действии списка, иначе весь список не будет возвращен.
<br> ** Методы `get _*()` имеют доступ к текущему представлению и могут возвращать различные экземпляры сериализатора или запроса на основе запроса или действия.

---

# Third party packages

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## DRF - Access Policy

## DRF - Политика доступа

The [Django REST - Access Policy](https://github.com/rsinger86/drf-access-policy) package provides a way to define complex access rules in declarative policy classes that are attached to view sets or function-based views. The policies are defined in JSON in a format similar to AWS' Identity & Access Management policies.

Пакет [Django REST-Политика доступа] (https://github.com/rsinger86/drf-access-policy) предоставляет способ определить правила сложного доступа в классах декларативной политики, которые прикреплены для просмотра наборов или представлений на основе функций.
Политики определены в JSON в формате, аналогичном политике управления идентификацией и доступом AWS.

## Composed Permissions

## Составленные разрешения

The [Composed Permissions](https://github.com/niwibe/djangorestframework-composed-permissions) package provides a simple way to define complex and multi-depth (with logic operators) permission objects, using small and reusable components.

[Составленные разрешения] (https://github.com/niwibe/djangorestframe-composed-permissions) предоставляет простой способ определения сложных и многократных (с логическими операторами) разрешениями, использующими небольшие и многократные компоненты.

## REST Condition

## Условие отдыха

The [REST Condition](https://github.com/caxap/rest_condition) package is another extension for building complex permissions in a simple and convenient way. The extension allows you to combine permissions with logical operators.

Пакет [Условие REST] (https://github.com/caxap/rest_condition) является еще одним расширением для создания комплексных разрешений простым и удобным способом.
Расширение позволяет вам объединять разрешения с логическими операторами.

## DRY Rest Permissions

## Разрешения на сухую отдыха

The [DRY Rest Permissions](https://github.com/FJNR-inc/dry-rest-permissions) package provides the ability to define different permissions for individual default and custom actions. This package is made for apps with permissions that are derived from relationships defined in the app's data model. It also supports permission checks being returned to a client app through the API's serializer. Additionally it supports adding permissions to the default and custom list actions to restrict the data they retrieve per user.

Пакет [Dry Restressions] (https://github.com/fjnr-inc/dry-rest-permissions) дает возможность определять различные разрешения для отдельных действий по умолчанию и пользовательских действий.
Этот пакет создан для приложений с разрешениями, которые получены из отношений, определенных в модели данных приложения.
Он также поддерживает проверки разрешений, возвращающихся в клиентское приложение через сериализатор API.
Кроме того, он поддерживает добавление разрешений к действиям по умолчанию и пользовательским списку для ограничения данных, которые они получают на пользователя.

## Django Rest Framework Roles

## Django Rest Framework роли

The [Django Rest Framework Roles](https://github.com/computer-lab/django-rest-framework-roles) package makes it easier to parameterize your API over multiple types of users.

Пакет [https://github.com/computer-lab/django-rest-framework-roles) (https://github.com/computer-lab/django-rest-framework

## Rest Framework Roles

## REST Framework Роли

The [Rest Framework Roles](https://github.com/Pithikos/rest-framework-roles) makes it super easy to protect views based on roles. Most importantly allows you to decouple accessibility logic from models and views in a clean human-readable way.

[Роли REST Framework] (https://github.com/pithikos/rest-framework-doles) делает очень легко защищать представления на основе ролей.
Самое главное, что позволяет вам отделить логику доступности от моделей и видов чистым человеком.

## Django REST Framework API Key

## Django Rest Framework API -ключ

The [Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/) package provides permissions classes, models and helpers to add API key authorization to your API. It can be used to authorize internal or third-party backends and services (i.e. *machines*) which do not have a user account. API keys are stored securely using Django's password hashing infrastructure, and they can be viewed, edited and revoked at anytime in the Django admin.

[Https://florimondmanca.github.io/djangestframeworkwork-api-key/) предоставляет классы, модели и помощники, модели и помощники для добавления авторизации API в ваш API.
Он может быть использован для авторизации внутренних или сторонних бэкэндов и услуг (то есть *машины *), которые не имеют учетной записи пользователя.
Ключи API надежно хранятся с использованием инфраструктуры пароля Django, и их можно просмотреть, отредактировать и отозвать в любое время в администраторе Django.

## Django Rest Framework Role Filters

## Django Rest Framework Role Filters

The [Django Rest Framework Role Filters](https://github.com/allisson/django-rest-framework-role-filters) package provides simple filtering over multiple types of roles.

Пакет [https://github.com/allisson/django-rest-role-filters) (https://github.com/allisson/django-rest-framework-role-filters) предоставляет простую фильтрацию по нескольким типам ролей.

## Django Rest Framework PSQ

## Django Rest Framework PSQ

The [Django Rest Framework PSQ](https://github.com/drf-psq/drf-psq) package is an extension that gives support for having action-based **permission_classes**, **serializer_class**, and **queryset** dependent on permission-based rules.

Пакет [https://github.com/drf-psq/drf-psq) [https://github.com/drf-psq/drf-psq)-это расширение, которое дает поддержку для наличия на основе действий ** разрешение_классы **, ** serializer_class ** и*
*queryset ** в зависимости от правил, основанных на разрешениях.