<!-- TRANSLATED by md-translate -->
---

source:
    - permissions.py

источник:
- permissions.py

---

# Permissions

# Разрешения

> Authentication or identification by itself is not usually sufficient to gain access to information or code.  For that, the entity requesting access must have authorization.
>
> &mdash; [Apple Developer Documentation](https://developer.apple.com/library/mac/#documentation/security/Conceptual/AuthenticationAndAuthorizationGuide/Authorization/Authorization.html)

> Аутентификация или идентификация сами по себе обычно недостаточны для получения доступа к информации или коду.  Для этого субъект, запрашивающий доступ, должен иметь авторизацию.
>
> &mdash; [Apple Developer Documentation](https://developer.apple.com/library/mac/#documentation/security/Conceptual/AuthenticationAndAuthorizationGuide/Authorization/Authorization.html)

Together with [authentication](authentication.md) and [throttling](throttling.md), permissions determine whether a request should be granted or denied access.

Вместе с [authentication](authentication.md) и [throttling](throttling.md) разрешения определяют, следует ли предоставить или отказать в доступе запросу.

Permission checks are always run at the very start of the view, before any other code is allowed to proceed.  Permission checks will typically use the authentication information in the `request.user` and `request.auth` properties to determine if the incoming request should be permitted.

Проверка разрешений всегда выполняется в самом начале представления, до того, как будет разрешено выполнение любого другого кода.  Проверки разрешений обычно используют информацию об аутентификации в свойствах `request.user` и `request.auth`, чтобы определить, должен ли входящий запрос быть разрешен.

Permissions are used to grant or deny access for different classes of users to different parts of the API.

Разрешения используются для предоставления или запрета доступа различных классов пользователей к различным частям API.

The simplest style of permission would be to allow access to any authenticated user, and deny access to any unauthenticated user. This corresponds to the `IsAuthenticated` class in REST framework.

Самый простой стиль разрешения - разрешить доступ любому аутентифицированному пользователю и запретить доступ любому неаутентифицированному пользователю. Это соответствует классу `IsAuthenticated` в REST framework.

A slightly less strict style of permission would be to allow full access to authenticated users, but allow read-only access to unauthenticated users. This corresponds to the `IsAuthenticatedOrReadOnly` class in REST framework.

Несколько менее строгий стиль разрешения - разрешить полный доступ для аутентифицированных пользователей, но разрешить доступ только для чтения для неаутентифицированных пользователей. Это соответствует классу `IsAuthenticatedOrReadOnly` в REST framework.

## How permissions are determined

## Как определяются разрешения

Permissions in REST framework are always defined as a list of permission classes.

Разрешения в REST framework всегда определяются как список классов разрешений.

Before running the main body of the view each permission in the list is checked.
If any permission check fails, an `exceptions.PermissionDenied` or `exceptions.NotAuthenticated` exception will be raised, and the main body of the view will not run.

Перед запуском основной части представления проверяется каждое разрешение в списке.
Если проверка какого-либо разрешения не удалась, будет вызвано исключение `exceptions.PermissionDenied` или `exceptions.NotAuthenticated`, и основное тело представления не будет запущено.

When the permission checks fail, either a "403 Forbidden" or a "401 Unauthorized" response will be returned, according to the following rules:

Если проверка разрешения не сработала, будет возвращен ответ "403 Forbidden" или "401 Unauthorized", в соответствии со следующими правилами:

* The request was successfully authenticated, but permission was denied. _&mdash; An HTTP 403 Forbidden response will be returned._
* The request was not successfully authenticated, and the highest priority authentication class _does not_ use `WWW-Authenticate` headers. _&mdash; An HTTP 403 Forbidden response will be returned._
* The request was not successfully authenticated, and the highest priority authentication class _does_ use `WWW-Authenticate` headers. _&mdash; An HTTP 401 Unauthorized response, with an appropriate `WWW-Authenticate` header will be returned._

* Запрос был успешно аутентифицирован, но в разрешении было отказано. *&mdash; Будет возвращен ответ HTTP 403 Forbidden.
* Запрос не был успешно аутентифицирован, и класс аутентификации с наивысшим приоритетом *не использует заголовки `WWW-Authenticate`. *&mdash; Будет возвращен ответ HTTP 403 Forbidden.* *
* Запрос не был успешно аутентифицирован, и класс аутентификации с наивысшим приоритетом *не использует заголовки `WWW-Authenticate`. *&mdash; Будет возвращен ответ HTTP 401 Unauthorized с соответствующим заголовком `WWW-Authenticate`.

## Object level permissions

## Разрешения на уровне объекта

REST framework permissions also support object-level permissioning.  Object level permissions are used to determine if a user should be allowed to act on a particular object, which will typically be a model instance.

Разрешения фреймворка REST также поддерживают разрешение на уровне объекта.  Разрешения на уровне объекта используются для определения того, разрешено ли пользователю действовать с определенным объектом, который обычно является экземпляром модели.

Object level permissions are run by REST framework's generic views when `.get_object()` is called.
As with view level permissions, an `exceptions.PermissionDenied` exception will be raised if the user is not allowed to act on the given object.

Разрешения на уровне объекта запускаются общими представлениями REST framework при вызове `.get_object()`.
Как и в случае с разрешениями на уровне представления, исключение `exceptions.PermissionDenied` будет поднято, если пользователю не разрешено действовать с данным объектом.

If you're writing your own views and want to enforce object level permissions,
or if you override the `get_object` method on a generic view, then you'll need to explicitly call the `.check_object_permissions(request, obj)` method on the view at the point at which you've retrieved the object.

Если вы пишете собственные представления и хотите обеспечить разрешения на уровне объекта,
или если вы переопределите метод `get_object` в общем представлении, то вам нужно будет явно вызвать метод `.check_object_permissions(request, obj)` в представлении в тот момент, когда вы извлекли объект.

This will either raise a `PermissionDenied` or `NotAuthenticated` exception, or simply return if the view has the appropriate permissions.

Это либо вызовет исключение `PermissionDenied` или `NotAuthenticated`, либо просто вернет, если представление имеет соответствующие разрешения.

For example:

Например:

```
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
```

---

**Note**: With the exception of `DjangoObjectPermissions`, the provided
permission classes in `rest_framework.permissions` **do not** implement the
methods necessary to check object permissions.

**Примечание**: За исключением `DjangoObjectPermissions`, предоставленные
классы разрешений в `rest_framework.permissions` **не** реализуют
методы, необходимые для проверки объектных разрешений.

If you wish to use the provided permission classes in order to check object
permissions, **you must** subclass them and implement the
`has_object_permission()` method described in the [_Custom
permissions_](#custom-permissions) section (below).

Если вы хотите использовать предоставленные классы разрешений для проверки объекта
разрешения, **вы должны** подклассифицировать их и реализовать метод
метод `has_object_permission()`, описанный в разделе [*Custom
разрешения*](#custom-permissions) (ниже).

---

#### Limitations of object level permissions

#### Ограничения разрешений на уровне объекта

For performance reasons the generic views will not automatically apply object level permissions to each instance in a queryset when returning a list of objects.

По причинам производительности общие представления не будут автоматически применять разрешения на уровне объекта к каждому экземпляру в наборе запросов при возврате списка объектов.

Often when you're using object level permissions you'll also want to [filter the queryset](filtering.md) appropriately, to ensure that users only have visibility onto instances that they are permitted to view.

Часто при использовании разрешений на уровне объектов вы также хотите [фильтровать набор запросов] (filtering.md) соответствующим образом, чтобы убедиться, что пользователи имеют видимость только тех экземпляров, которые им разрешено просматривать.

Because the `get_object()` method is not called, object level permissions from the `has_object_permission()` method **are not applied** when creating objects. In order to restrict object creation you need to implement the permission check either in your Serializer class or override the `perform_create()` method of your ViewSet class.

Поскольку метод `get_object()` не вызывается, разрешения объектного уровня из метода `has_object_permission()` **не применяются** при создании объектов. Чтобы ограничить создание объектов, вам необходимо реализовать проверку разрешений либо в классе Serializer, либо переопределить метод `perform_create()` вашего класса ViewSet.

## Setting the permission policy

## Установка политики разрешений

The default permission policy may be set globally, using the `DEFAULT_PERMISSION_CLASSES` setting.  For example.

Политика разрешений по умолчанию может быть установлена глобально с помощью параметра `DEFAULT_PERMISSION_CLASSES`.  Например.

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

If not specified, this setting defaults to allowing unrestricted access:

Если этот параметр не указан, то по умолчанию он разрешает неограниченный доступ:

```
'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
]
```

You can also set the authentication policy on a per-view, or per-viewset basis,
using the `APIView` class-based views.

Вы также можете установить политику аутентификации на основе каждого просмотра или каждого набора просмотров,
используя представления на основе класса `APIView`.

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

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

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

**Примечание:** когда вы устанавливаете новые классы разрешений с помощью атрибута class или декораторов, вы говорите представлению игнорировать список по умолчанию, установленный в файле **settings.py**.

Provided they inherit from `rest_framework.permissions.BasePermission`, permissions can be composed using standard Python bitwise operators. For example, `IsAuthenticatedOrReadOnly` could be written:

При условии наследования от `rest_framework.permissions.BasePermission`, разрешения могут быть составлены с использованием стандартных побитовых операторов Python. Например, `IsAuthenticatedOrReadOnly` может быть записано:

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

**Примечание:** он поддерживает & (и), | (или) и ~ (не).

---

# API Reference

# API Reference

## AllowAny

## AllowAny

The `AllowAny` permission class will allow unrestricted access, **regardless of if the request was authenticated or unauthenticated**.

Класс разрешения `AllowAny` разрешает неограниченный доступ, **независимо от того, был ли запрос аутентифицирован или неаутентифицирован**.

This permission is not strictly required, since you can achieve the same result by using an empty list or tuple for the permissions setting, but you may find it useful to specify this class because it makes the intention explicit.

Это разрешение не является строго обязательным, поскольку вы можете достичь того же результата, используя пустой список или кортеж для установки разрешений, но вы можете посчитать полезным указать этот класс, поскольку он делает намерение явным.

## IsAuthenticated

## IsAuthenticated

The `IsAuthenticated` permission class will deny permission to any unauthenticated user, and allow permission otherwise.

Класс разрешения `IsAuthenticated` будет запрещать разрешение любому пользователю, не прошедшему аутентификацию, и разрешать в противном случае.

This permission is suitable if you want your API to only be accessible to registered users.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только зарегистрированным пользователям.

## IsAdminUser

## IsAdminUser

The `IsAdminUser` permission class will deny permission to any user, unless `user.is_staff` is `True` in which case permission will be allowed.

Класс разрешения `IsAdminUser` запрещает разрешение любому пользователю, если только `user.is_staff` не является `True`, в этом случае разрешение будет разрешено.

This permission is suitable if you want your API to only be accessible to a subset of trusted administrators.

Это разрешение подходит, если вы хотите, чтобы ваш API был доступен только подгруппе доверенных администраторов.

## IsAuthenticatedOrReadOnly

## IsAuthenticatedOrReadOnly

The `IsAuthenticatedOrReadOnly` will allow authenticated users to perform any request.  Requests for unauthenticated users will only be permitted if the request method is one of the "safe" methods; `GET`, `HEAD` or `OPTIONS`.

Параметр `IsAuthenticatedOrReadOnly` позволит аутентифицированным пользователям выполнять любые запросы.  Запросы для неаутентифицированных пользователей будут разрешены, только если метод запроса является одним из "безопасных" методов: `GET`, `HEAD` или `OPTIONS`.

This permission is suitable if you want to your API to allow read permissions to anonymous users, and only allow write permissions to authenticated users.

Это разрешение подходит, если вы хотите, чтобы ваш API разрешал разрешения на чтение анонимным пользователям и разрешал разрешения на запись только аутентифицированным пользователям.

## DjangoModelPermissions

## DjangoModelPermissions

This permission class ties into Django's standard `django.contrib.auth` [model permissions](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions).  This permission must only be applied to views that have a `.queryset` property or `get_queryset()` method. Authorization will only be granted if the user _is authenticated_ and has the _relevant model permissions_ assigned. The appropriate model is determined by checking `get_queryset().model` or `queryset.model`.

Этот класс разрешений связан со стандартными разрешениями Django `django.contrib.auth` [model permissions](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions).  Это разрешение должно применяться только к представлениям, имеющим свойство `.queryset` или метод `get_queryset()`. Авторизация будет предоставлена только в том случае, если пользователь *аутентифицирован* и имеет *соответствующие разрешения модели*. Соответствующая модель определяется путем проверки `get_queryset().model` или `queryset.model`.

* `GET` requests require the user to have the `view` or `change` permission on the model
* `POST` requests require the user to have the `add` permission on the model.
* `PUT` and `PATCH` requests require the user to have the `change` permission on the model.
* `DELETE` requests require the user to have the `delete` permission on the model.

* запросы `GET` требуют, чтобы пользователь имел права `view` или `change` на модель.
* `POST` запросы требуют от пользователя разрешения `add` на модель.
* запросы `PUT` и `PATCH` требуют от пользователя разрешения `изменить` модель.
* Запросы `DELETE` требуют от пользователя разрешения `delete` на модель.

The default behaviour can also be overridden to support custom model permissions.

Поведение по умолчанию также может быть переопределено для поддержки пользовательских разрешений модели.

To use custom model permissions, override `DjangoModelPermissions` and set the `.perms_map` property.  Refer to the source code for details.

Чтобы использовать пользовательские разрешения модели, переопределите `DjangoModelPermissions` и установите свойство `.perms_map`.  Подробности см. в исходном коде.

## DjangoModelPermissionsOrAnonReadOnly

## DjangoModelPermissionsOrAnonReadOnly

Similar to `DjangoModelPermissions`, but also allows unauthenticated users to have read-only access to the API.

Аналогичен `DjangoModelPermissions`, но также позволяет неаутентифицированным пользователям иметь доступ к API только для чтения.

## DjangoObjectPermissions

## DjangoObjectPermissions

This permission class ties into Django's standard [object permissions framework](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions) that allows per-object permissions on models.  In order to use this permission class, you'll also need to add a permission backend that supports object-level permissions, such as [django-guardian](https://github.com/lukaszb/django-guardian).

Этот класс разрешений связан со стандартным [object permissions framework](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions) Django, который позволяет устанавливать разрешения на модели на уровне объектов.  Чтобы использовать этот класс разрешений, вам также необходимо добавить бэкенд разрешений, который поддерживает разрешения на уровне объектов, например [django-guardian](https://github.com/lukaszb/django-guardian).

As with `DjangoModelPermissions`, this permission must only be applied to views that have a `.queryset` property or `.get_queryset()` method. Authorization will only be granted if the user _is authenticated_ and has the _relevant per-object permissions_ and _relevant model permissions_ assigned.

Как и `DjangoModelPermissions`, это разрешение должно применяться только к представлениям, имеющим свойство `.queryset` или метод `.get_queryset()`. Разрешение будет предоставлено только в том случае, если пользователь *аутентифицирован* и имеет *соответствующие разрешения на объект* и *соответствующие разрешения на модель*.

* `POST` requests require the user to have the `add` permission on the model instance.
* `PUT` and `PATCH` requests require the user to have the `change` permission on the model instance.
* `DELETE` requests require the user to have the `delete` permission on the model instance.

* `POST` запросы требуют, чтобы пользователь имел право `add` на экземпляр модели.
* Запросы `PUT` и `PATCH` требуют от пользователя разрешения `изменить` на экземпляре модели.
* Запросы `DELETE` требуют от пользователя разрешения `delete` на экземпляр модели.

Note that `DjangoObjectPermissions` **does not** require the `django-guardian` package, and should support other object-level backends equally well.

Обратите внимание, что `DjangoObjectPermissions` **не** требует пакета `django-guardian`, и должен одинаково хорошо поддерживать другие бэкенды объектного уровня.

As with `DjangoModelPermissions` you can use custom model permissions by overriding `DjangoObjectPermissions` and setting the `.perms_map` property.  Refer to the source code for details.

Как и в случае с `DjangoModelPermissions`, вы можете использовать пользовательские разрешения модели, переопределив `DjangoObjectPermissions` и установив свойство `.perms_map`.  Подробности смотрите в исходном коде.

---

**Note**: If you need object level `view` permissions for `GET`, `HEAD` and `OPTIONS` requests and are using django-guardian for your object-level permissions backend, you'll want to consider using the `DjangoObjectPermissionsFilter` class provided by the [`djangorestframework-guardian2` package](https://github.com/johnthagen/django-rest-framework-guardian2). It ensures that list endpoints only return results including objects for which the user has appropriate view permissions.

**Примечание**: Если вам нужны разрешения `view` на уровне объектов для запросов `GET`, `HEAD` и `OPTIONS` и вы используете django-guardian для бэкенда разрешений на уровне объектов, вам стоит рассмотреть возможность использования класса `DjangoObjectPermissionsFilter`, предоставляемого [пакетом `djangorestframework-guardian2`](https://github.com/johnthagen/django-rest-framework-guardian2). Он гарантирует, что конечные точки списка возвращают только те результаты, включающие объекты, для которых у пользователя есть соответствующие разрешения на просмотр.

---

# Custom permissions

# Пользовательские разрешения

To implement a custom permission, override `BasePermission` and implement either, or both, of the following methods:

Чтобы реализовать пользовательское разрешение, переопределите `BasePermission` и реализуйте один или оба из следующих методов:

* `.has_permission(self, request, view)`
* `.has_object_permission(self, request, view, obj)`

* `.has_permission(self, request, view)`
* `.has_object_permission(self, request, view, obj)`

The methods should return `True` if the request should be granted access, and `False` otherwise.

Методы должны возвращать `True`, если запрос должен получить доступ, и `False` в противном случае.

If you need to test if a request is a read operation or a write operation, you should check the request method against the constant `SAFE_METHODS`, which is a tuple containing `'GET'`, `'OPTIONS'` and `'HEAD'`.  For example:

Если вам нужно проверить, является ли запрос операцией чтения или записи, вы должны проверить метод запроса по константе `SAFE_METHODS`, которая представляет собой кортеж, содержащий `'GET'`, `'OPTIONS'` и `'HEAD'`.  Например:

```
if request.method in permissions.SAFE_METHODS:
    # Check permissions for read-only request
else:
    # Check permissions for write request
```

---

**Note**: The instance-level `has_object_permission` method will only be called if the view-level `has_permission` checks have already passed. Also note that in order for the instance-level checks to run, the view code should explicitly call `.check_object_permissions(request, obj)`. If you are using the generic views then this will be handled for you by default. (Function-based views will need to check object permissions explicitly, raising `PermissionDenied` on failure.)

**Примечание**: Метод `has_object_permission` на уровне экземпляра будет вызван только в том случае, если проверки `has_permission` на уровне представления уже прошли. Также обратите внимание, что для того, чтобы проверки на уровне экземпляра были выполнены, код представления должен явно вызвать `.check_object_permissions(request, obj)`. Если вы используете общие представления, то это будет сделано за вас по умолчанию. (Представления, основанные на функциях, должны будут проверять разрешения объектов явно, выдавая при неудаче сообщение `PermissionDenied`).

---

Custom permissions will raise a `PermissionDenied` exception if the test fails. To change the error message associated with the exception, implement a `message` attribute directly on your custom permission. Otherwise the `default_detail` attribute from `PermissionDenied` will be used. Similarly, to change the code identifier associated with the exception, implement a `code` attribute directly on your custom permission - otherwise the `default_code` attribute from `PermissionDenied` will be used.

Пользовательские разрешения вызовут исключение `PermissionDenied`, если тест не пройдет. Чтобы изменить сообщение об ошибке, связанное с исключением, реализуйте атрибут `message` непосредственно для вашего пользовательского разрешения. В противном случае будет использоваться атрибут `default_detail` из `PermissionDenied`. Аналогично, чтобы изменить идентификатор кода, связанный с исключением, реализуйте атрибут `code` непосредственно для вашего пользовательского разрешения - иначе будет использоваться атрибут `default_code` из `PermissionDenied`.

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

Ниже приведен пример класса разрешения, который проверяет IP-адрес входящего запроса по списку блокировки и отклоняет запрос, если IP-адрес был заблокирован.

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

As well as global permissions, that are run against all incoming requests, you can also create object-level permissions, that are only run against operations that affect a particular object instance.  For example:

Помимо глобальных разрешений, которые выполняются для всех входящих запросов, вы также можете создавать разрешения на уровне объекта, которые выполняются только для операций, затрагивающих конкретный экземпляр объекта.  Например:

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

Note that the generic views will check the appropriate object level permissions, but if you're writing your own custom views, you'll need to make sure you check the object level permission checks yourself.  You can do so by calling `self.check_object_permissions(request, obj)` from the view once you have the object instance.  This call will raise an appropriate `APIException` if any object-level permission checks fail, and will otherwise simply return.

Обратите внимание, что общие представления будут проверять соответствующие разрешения на уровне объекта, но если вы пишете свои собственные пользовательские представления, вам нужно убедиться, что вы сами проверяете разрешения на уровне объекта.  Вы можете сделать это, вызвав `self.check_object_permissions(request, obj)` из представления, когда у вас есть экземпляр объекта.  Этот вызов вызовет соответствующее исключение `APIException`, если проверка разрешений на уровне объекта завершится неудачей, а в противном случае просто вернется.

Also note that the generic views will only check the object-level permissions for views that retrieve a single model instance.  If you require object-level filtering of list views, you'll need to filter the queryset separately.  See the [filtering documentation](filtering.md) for more details.

Также обратите внимание, что общие представления будут проверять разрешения на уровне объекта только для представлений, которые получают один экземпляр модели.  Если вам требуется фильтрация представлений списка на уровне объектов, вам нужно будет фильтровать набор запросов отдельно.  Более подробную информацию смотрите в документации [filtering documentation](filtering.md).

# Overview of access restriction methods

# Обзор методов ограничения доступа

REST framework offers three different methods to customize access restrictions on a case-by-case basis. These apply in different scenarios and have different effects and limitations.

Структура REST предлагает три различных метода настройки ограничений доступа в каждом конкретном случае. Они применяются в разных сценариях и имеют различные эффекты и ограничения.

* `queryset`/`get_queryset()`: Limits the general visibility of existing objects from the database. The queryset limits which objects will be listed and which objects can be modified or deleted. The `get_queryset()` method can apply different querysets based on the current action.
* `permission_classes`/`get_permissions()`: General permission checks based on the current action, request and targeted object. Object level permissions can only be applied to retrieve, modify and deletion actions. Permission checks for list and create will be applied to the entire object type. (In case of list: subject to restrictions in the queryset.)
* `serializer_class`/`get_serializer()`: Instance level restrictions that apply to all objects on input and output. The serializer may have access to the request context. The `get_serializer()` method can apply different serializers based on the current action.

* `queryset`/`get_queryset()`: Ограничивает общую видимость существующих объектов из базы данных. Кверисет ограничивает, какие объекты будут отображаться в списке и какие объекты могут быть изменены или удалены. Метод `get_queryset()` может применять различные кверисеты в зависимости от текущего действия.
* `permission_classes`/`get_permissions()`: Общая проверка разрешений на основе текущего действия, запроса и целевого объекта. Разрешения на уровне объекта могут быть применены только к действиям получения, изменения и удаления. Проверки разрешений для list и create будут применены ко всему типу объекта. (В случае списка: с учетом ограничений в наборе запросов).
* `serializer_class`/`get_serializer()`: Ограничения на уровне экземпляра, которые применяются ко всем объектам на входе и выходе. Сериализатор может иметь доступ к контексту запроса. Метод `get_serializer()` может применять различные сериализаторы в зависимости от текущего действия.

The following table lists the access restriction methods and the level of control they offer over which actions.

В следующей таблице перечислены методы ограничения доступа и уровень контроля, который они обеспечивают, над какими действиями.

|                                    | `queryset` | `permission_classes` | `serializer_class` |
|------------------------------------|------------|----------------------|--------------------|
| Action: list                       | global     | global               | object-level*      |
| Action: create                     | no         | global               | object-level       |
| Action: retrieve                   | global     | object-level         | object-level       |
| Action: update                     | global     | object-level         | object-level       |
| Action: partial_update             | global     | object-level         | object-level       |
| Action: destroy                    | global     | object-level         | no                 |
| Can reference action in decision   | no**       | yes                  | no**               |
| Can reference request in decision  | no**       | yes                  | yes                |

| | | `queryset` | `permission_classes` | `serializer_class` | |
|------------------------------------|------------|----------------------|--------------------|
| Действие: список | глобальный | глобальный | объектный уровень* | |
| Действие: создать | нет | глобальный | объектный уровень |
| Действие: извлечь | глобальный | объектный уровень | объектного уровня | |
| Действие: обновить | глобальный | объектный уровень | объектно-уровневый | |
| Действие: partial_update | global | object-level | object-level | object-level |
| Действие: уничтожить | глобальный | объектный уровень | нет |
| Может ссылаться на действие в решении | нет** | да | нет** | да | нет** | да | да | нет** | нет
| Может ссылаться на запрос в решении | нет** | да | да | да | да.

* A Serializer class should not raise PermissionDenied in a list action, or the entire list would not be returned. <br>
 ** The `get_*()` methods have access to the current view and can return different Serializer or QuerySet instances based on the request or action.

* Класс Serializer не должен поднимать PermissionDenied в действии со списком, иначе весь список не будет возвращен. <br>
** Методы `get_*()` имеют доступ к текущему представлению и могут возвращать различные экземпляры Serializer или QuerySet в зависимости от запроса или действия.

---

# Third party packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF - Access Policy

## DRF - Политика доступа

The [Django REST - Access Policy](https://github.com/rsinger86/drf-access-policy) package provides a way to define complex access rules in declarative policy classes that are attached to view sets or function-based views. The policies are defined in JSON in a format similar to AWS' Identity & Access Management policies.

Пакет [Django REST - Access Policy](https://github.com/rsinger86/drf-access-policy) предоставляет способ определения сложных правил доступа в декларативных классах политик, которые прикрепляются к наборам представлений или представлениям на основе функций. Политики определяются в JSON в формате, аналогичном политикам AWS Identity & Access Management.

## Composed Permissions

## Составленные разрешения

The [Composed Permissions](https://github.com/niwibe/djangorestframework-composed-permissions) package provides a simple way to define complex and multi-depth (with logic operators) permission objects, using small and reusable components.

Пакет [Composed Permissions](https://github.com/niwibe/djangorestframework-composed-permissions) предоставляет простой способ определения сложных и многомерных (с логическими операторами) объектов разрешений, используя небольшие и многократно используемые компоненты.

## REST Condition

## Условие REST

The [REST Condition](https://github.com/caxap/rest_condition) package is another extension for building complex permissions in a simple and convenient way. The extension allows you to combine permissions with logical operators.

Пакет [REST Condition](https://github.com/caxap/rest_condition) - это еще одно расширение для построения сложных разрешений простым и удобным способом. Расширение позволяет комбинировать разрешения с логическими операторами.

## DRY Rest Permissions

## DRY Rest Permissions

The [DRY Rest Permissions](https://github.com/FJNR-inc/dry-rest-permissions) package provides the ability to define different permissions for individual default and custom actions. This package is made for apps with permissions that are derived from relationships defined in the app's data model. It also supports permission checks being returned to a client app through the API's serializer. Additionally it supports adding permissions to the default and custom list actions to restrict the data they retrieve per user.

Пакет [DRY Rest Permissions](https://github.com/FJNR-inc/dry-rest-permissions) предоставляет возможность определять различные разрешения для отдельных действий по умолчанию и пользовательских действий. Этот пакет предназначен для приложений с разрешениями, которые являются производными от отношений, определенных в модели данных приложения. Он также поддерживает проверку разрешений, возвращаемую клиентскому приложению через сериализатор API. Кроме того, он поддерживает добавление разрешений к действиям списка по умолчанию и пользовательским действиям списка для ограничения данных, которые они извлекают для каждого пользователя.

## Django Rest Framework Roles

## Роли Django Rest Framework

The [Django Rest Framework Roles](https://github.com/computer-lab/django-rest-framework-roles) package makes it easier to parameterize your API over multiple types of users.

Пакет [Django Rest Framework Roles](https://github.com/computer-lab/django-rest-framework-roles) облегчает параметризацию вашего API для нескольких типов пользователей.

## Rest Framework Roles

## Rest Framework Roles

The [Rest Framework Roles](https://github.com/Pithikos/rest-framework-roles) makes it super easy to protect views based on roles. Most importantly allows you to decouple accessibility logic from models and views in a clean human-readable way.

[Rest Framework Roles](https://github.com/Pithikos/rest-framework-roles) позволяет очень просто защитить представления на основе ролей. Самое главное - позволяет вам отделить логику доступности от моделей и представлений чистым человекочитаемым способом.

## Django REST Framework API Key

## Ключ API Django REST Framework

The [Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/) package provides permissions classes, models and helpers to add API key authorization to your API. It can be used to authorize internal or third-party backends and services (i.e. _machines_) which do not have a user account. API keys are stored securely using Django's password hashing infrastructure, and they can be viewed, edited and revoked at anytime in the Django admin.

Пакет [Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/) предоставляет классы разрешений, модели и помощники для добавления авторизации по API ключу в ваш API. Его можно использовать для авторизации внутренних или сторонних бэкендов и сервисов (т.е. *машин*), которые не имеют учетной записи пользователя. API ключи хранятся в безопасном месте с использованием инфраструктуры хэширования паролей Django, и их можно просматривать, редактировать и отзывать в любое время в админке Django.

## Django Rest Framework Role Filters

## Ролевые фильтры Django Rest Framework

The [Django Rest Framework Role Filters](https://github.com/allisson/django-rest-framework-role-filters) package provides simple filtering over multiple types of roles.

Пакет [Django Rest Framework Role Filters](https://github.com/allisson/django-rest-framework-role-filters) обеспечивает простую фильтрацию по нескольким типам ролей.

## Django Rest Framework PSQ

## Django Rest Framework PSQ

The [Django Rest Framework PSQ](https://github.com/drf-psq/drf-psq) package is an extension that gives support for having action-based **permission_classes**, **serializer_class**, and **queryset** dependent on permission-based rules.

Пакет [Django Rest Framework PSQ](https://github.com/drf-psq/drf-psq) - это расширение, которое предоставляет поддержку для того, чтобы основанные на действиях **permission_classes**, **serializer_class** и **queryset** зависели от правил, основанных на разрешениях.