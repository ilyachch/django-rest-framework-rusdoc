<!-- TRANSLATED by md-translate -->
---

source:

источник:

* viewsets.py

* Viewsets.py

---

# ViewSets

# Виды

> After routing has determined which controller to use for a request, your controller is responsible for making sense of the request and producing the appropriate output.
>
> — [Ruby on Rails Documentation](https://guides.rubyonrails.org/action_controller_overview.html)

> После того, как маршрутизация определила, какой контроллер использовать для запроса, ваш контроллер отвечает за понимание запроса и создание соответствующего вывода.
>
> - [Документация Ruby on Rails] (https://guides.rubyonrails.org/action_controller_overview.html)

Django REST framework allows you to combine the logic for a set of related views in a single class, called a `ViewSet`. In other frameworks you may also find conceptually similar implementations named something like 'Resources' or 'Controllers'.

Django Rest Framework позволяет объединить логику для набора связанных представлений в одном классе, называемом `viewset '.
В других структурах вы также можете найти концептуально похожие реализации, названные что -то вроде «ресурсов» или «контроллеров».

A `ViewSet` class is simply **a type of class-based View, that does not provide any method handlers** such as `.get()` or `.post()`, and instead provides actions such as `.list()` and `.create()`.

Класс `viewset`-это просто ** тип представления на основе класса, который не предоставляет каких-либо обработчиков метода **, таких как` .get () `или` .post () `, и вместо этого предоставляет такие действия, как`.
list () `и` .create () `.

The method handlers for a `ViewSet` are only bound to the corresponding actions at the point of finalizing the view, using the `.as_view()` method.

Обработчики метода для `viewset` связаны только с соответствующими действиями в точке завершения представления, используя метод` .as_view () `.

Typically, rather than explicitly registering the views in a viewset in the urlconf, you'll register the viewset with a router class, that automatically determines the urlconf for you.

Как правило, вместо того, чтобы явно регистрировать представления в счете Views в URLConf, вы зарегистрируете смесь просмотра с помощью класса маршрутизатора, который автоматически определяет URLConf для вас.

## Example

## Пример

Let's define a simple viewset that can be used to list or retrieve all the users in the system.

Давайте определим простой набор просмотра, который можно использовать для перечисления или извлечения всех пользователей в системе.

```
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

If we need to, we can bind this viewset into two separate views, like so:

Если нам нужно, мы можем связать этот сет с двумя отдельными представлениями, например, так:

```
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

Typically we wouldn't do this, but would instead register the viewset with a router, and allow the urlconf to be automatically generated.

Как правило, мы не делали этого, но вместо этого регистрируем визуальный набор с маршрутизатором и позволили бы автоматически генерировать URLConf.

```
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

Rather than writing your own viewsets, you'll often want to use the existing base classes that provide a default set of behavior. For example:

Вместо того, чтобы писать свои собственные виды, вы часто захотите использовать существующие базовые классы, которые обеспечивают набор поведения по умолчанию.
Например:

```
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

There are two main advantages of using a `ViewSet` class over using a `View` class.

Существует два основных преимущества использования класса `viewset` по сравнению с использованием класса` view '.

* Repeated logic can be combined into a single class. In the above example, we only need to specify the `queryset` once, and it'll be used across multiple views.
* By using routers, we no longer need to deal with wiring up the URL conf ourselves.

* Повторная логика может быть объединена в один класс.
В приведенном выше примере нам нужно указать только один раз один раз, и он будет использоваться в нескольких представлениях.
* Используя маршрутизаторы, нам больше не нужно иметь дело с проводкой URL Conf.

Both of these come with a trade-off. Using regular views and URL confs is more explicit and gives you more control. ViewSets are helpful if you want to get up and running quickly, or when you have a large API and you want to enforce a consistent URL configuration throughout.

Оба они поставляются с компромиссом.
Использование регулярных представлений и URL CONFS более четко и дает вам больше контроля.
Виды полезны, если вы хотите быстро встать и работать или когда у вас есть большой API, и вы хотите обеспечить постоянную конфигурацию URL -адреса повсюду.

## ViewSet actions

## viewset actions

The default routers included with REST framework will provide routes for a standard set of create/retrieve/update/destroy style actions, as shown below:

Маршрутизаторы по умолчанию, включенные в Framework REST, предоставят маршруты для стандартного набора действий CREATE/RESIED/UPDATE/Уничтожение стиля, как показано ниже:

```
class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
```

## Introspecting ViewSet actions

## интроспективные действия визуализации

During dispatch, the following attributes are available on the `ViewSet`.

Во время отправки следующие атрибуты доступны на `viewset '.

* `basename` - the base to use for the URL names that are created.
* `action` - the name of the current action (e.g., `list`, `create`).
* `detail` - boolean indicating if the current action is configured for a list or detail view.
* `suffix` - the display suffix for the viewset type - mirrors the `detail` attribute.
* `name` - the display name for the viewset. This argument is mutually exclusive to `suffix`.
* `description` - the display description for the individual view of a viewset.

* `baseName` - база для использования для созданных имен URL -адресов.
* `action` - имя текущего действия (например,` list`, `create`).
* `Detail` - Boolean, указывая, настроено ли текущее действие для представления списка или подробного описания.
* `Суффикс - суффикс дисплея для типа вида - отражает атрибут` detail`.
* `name` - отображаемое имя для ViewSet.
Этот аргумент взаимоисключает для `суффикс.
* `description` - Описание дисплея для индивидуального представления обзора.

You may inspect these attributes to adjust behavior based on the current action. For example, you could restrict permissions to everything except the `list` action similar to this:

Вы можете осмотреть эти атрибуты, чтобы настроить поведение на основе текущего действия.
Например, вы можете ограничить разрешения на все, кроме действия «List», аналогично этим:

```
def get_permissions(self):
    """
    Instantiates and returns the list of permissions that this view requires.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]
```

## Marking extra actions for routing

## отмечает дополнительные действия для маршрутизации

If you have ad-hoc methods that should be routable, you can mark them as such with the `@action` decorator. Like regular actions, extra actions may be intended for either a single object, or an entire collection. To indicate this, set the `detail` argument to `True` or `False`. The router will configure its URL patterns accordingly. e.g., the `DefaultRouter` will configure detail actions to contain `pk` in their URL patterns.

Если у вас есть специальные методы, которые должны быть направлены, вы можете пометить их как таковые с помощью декоратора `@action`.
Как и регулярные действия, дополнительные действия могут быть предназначены либо для одного объекта, либо для целой коллекции.
Чтобы указать это, установите аргумент «Detail» на `true` или` false '.
Маршрутизатор будет настраивать свои шаблоны URL -адреса соответственно.
Например, «Defaultrouter» будет настроить подробные действия, чтобы содержать «pk» в своих шаблонах URL.

A more complete example of extra actions:

Более полный пример дополнительных действий:

```
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
```

The `action` decorator will route `GET` requests by default, but may also accept other HTTP methods by setting the `methods` argument. For example:

Декоратор «действия» будет направлять запросы `get` по умолчанию, но также может принять другие методы HTTP, установив аргумент« Методы ».
Например:

```
@action(detail=True, methods=['post', 'delete'])
    def unset_password(self, request, pk=None):
       ...
```

The decorator allows you to override any viewset-level configuration such as `permission_classes`, `serializer_class`, `filter_backends`...:

Декоратор позволяет переопределить любую конфигурацию на уровне обзора, такую как `rescision_class`,` serializer_class`, `filter_backends` ...:

```
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
       ...
```

The two new actions will then be available at the urls `^users/{pk}/set_password/$` and `^users/{pk}/unset_password/$`. Use the `url_path` and `url_name` parameters to change the URL segment and the reverse URL name of the action.

Затем два новых действия будут доступны на URLS `^users/{pk}/set_password/$` и `^users/{pk}/unset_password/$`.
Используйте параметры `url_path` и` url_name`, чтобы изменить сегмент URL -адреса и имя обратного URL -адреса действия.

To view all extra actions, call the `.get_extra_actions()` method.

Чтобы просмотреть все дополнительные действия, вызовите метод `.get_extra_actions ()`.

### Routing additional HTTP methods for extra actions

### Маршрутизация дополнительных методов HTTP для дополнительных действий

Extra actions can map additional HTTP methods to separate `ViewSet` methods. For example, the above password set/unset methods could be consolidated into a single route. Note that additional mappings do not accept arguments.

Дополнительные действия могут сопоставить дополнительные методы HTTP для разделения методов `viewset.
Например, вышеуказанные методы установки паролей/нередовые могут быть объединены в один маршрут.
Обратите внимание, что дополнительные сопоставления не принимают аргументы.

```python
@action(detail=True, methods=['put'], name='Change Password')
    def password(self, request, pk=None):
        """Update the user's password."""
        ...

    @password.mapping.delete
    def delete_password(self, request, pk=None):
        """Delete the user's password."""
        ...
```

## Reversing action URLs

## Обращение URL -адресов действия

If you need to get the URL of an action, use the `.reverse_action()` method. This is a convenience wrapper for `reverse()`, automatically passing the view's `request` object and prepending the `url_name` with the `.basename` attribute.

Если вам нужно получить URL -адрес действия, используйте метод `.reverse_Action ()`.
Это удобная обертка для `reverse ()`, автоматически передавая объект View `request` и подготовка атрибута` url_name` с атрибутом `.basename.

Note that the `basename` is provided by the router during `ViewSet` registration. If you are not using a router, then you must provide the `basename` argument to the `.as_view()` method.

Обратите внимание, что `basename 'обеспечивается маршрутизатором во время регистрации` viewset.
Если вы не используете маршрутизатор, то вы должны предоставить аргумент `baseName` для метода` .as_view () `.

Using the example from the previous section:

Используя пример из предыдущего раздела:

```python
>>> view.reverse_action('set-password', args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

Alternatively, you can use the `url_name` attribute set by the `@action` decorator.

В качестве альтернативы, вы можете использовать атрибут `url_name`, установленную декоратором`@action`.

```python
>>> view.reverse_action(view.set_password.url_name, args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

The `url_name` argument for `.reverse_action()` should match the same argument to the `@action` decorator. Additionally, this method can be used to reverse the default actions, such as `list` and `create`.

Аргумент `url_name` для` .reverse_action () `должен соответствовать тому же аргументу с декоратором`@action`.
Кроме того, этот метод может использоваться для отмены действий по умолчанию, таких как «List» и `create`.

---

# API Reference

# Ссылка на API

## ViewSet

## Viewset

The `ViewSet` class inherits from `APIView`. You can use any of the standard attributes such as `permission_classes`, `authentication_classes` in order to control the API policy on the viewset.

Класс `viewset` наследует от` apiview`.
Вы можете использовать любой из стандартных атрибутов, таких как `rescision_classes`,` Authentication_classes`, чтобы управлять политикой API на сборе просмотра.

The `ViewSet` class does not provide any implementations of actions. In order to use a `ViewSet` class you'll override the class and define the action implementations explicitly.

Класс `ViewSet` не предоставляет никаких реализаций действий.
Чтобы использовать класс `viewset`, вы переопределяете класс и явно определите реализации действий.

## GenericViewSet

## genericviewset

The `GenericViewSet` class inherits from `GenericAPIView`, and provides the default set of `get_object`, `get_queryset` methods and other generic view base behavior, but does not include any actions by default.

Класс `genericViewSet` наследует от` genericApiview` и предоставляет набор по умолчанию `get_object`, методов` get_queryset` и другого базового поведения общего представления, но не включает никаких действий по умолчанию.

In order to use a `GenericViewSet` class you'll override the class and either mixin the required mixin classes, or define the action implementations explicitly.

Чтобы использовать класс `genericViewSet`, вы переопределите класс и либо смешивают требуемые классы микшина, либо явно определите реализации действий.

## ModelViewSet

## modelviewset

The `ModelViewSet` class inherits from `GenericAPIView` and includes implementations for various actions, by mixing in the behavior of the various mixin classes.

Класс `modelviewset` наследуется от` genericapiview` и включает реализации для различных действий, смешивая поведение различных классов микшина.

The actions provided by the `ModelViewSet` class are `.list()`, `.retrieve()`, `.create()`, `.update()`, `.partial_update()`, and `.destroy()`.

Действия, предусмотренные классом `modelViewSet`, являются` .list () `,` .retrieve () `,` .create () `,` .update () `,` .partial_update () `и` .destroy (
) `.

#### Example

#### Пример

Because `ModelViewSet` extends `GenericAPIView`, you'll normally need to provide at least the `queryset` and `serializer_class` attributes. For example:

Поскольку `modelviewset` Extens` genericapiview`, как правило, вам нужно предоставить хотя бы атрибуты `Queryset` и` serializer_class`.
Например:

```
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```

Note that you can use any of the standard attributes or method overrides provided by `GenericAPIView`. For example, to use a `ViewSet` that dynamically determines the queryset it should operate on, you might do something like this:

Обратите внимание, что вы можете использовать любой из стандартных атрибутов или переопределения метода, предоставленных `genericapiview`.
Например, чтобы использовать `viewset`, который динамически определяет запрос, который он должен работать, вы можете сделать что -то вроде этого:

```
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()
```

Note however that upon removal of the `queryset` property from your `ViewSet`, any associated [router](routers.md) will be unable to derive the basename of your Model automatically, and so you will have to specify the `basename` kwarg as part of your [router registration](routers.md).

Однако обратите внимание, что после удаления свойства `Queryset` из вашего` viewset`, любой связанный [router] (routers.md) не сможет автоматически вывести базовое имя вашей модели, и поэтому вам придется указать «базовое название».
Kwarg как часть вашей [Router Registration] (Routers.md).

Also note that although this class provides the complete set of create/list/retrieve/update/destroy actions by default, you can restrict the available operations by using the standard permission classes.

Также обратите внимание, что, хотя этот класс предоставляет полный набор действий CREATE/LIST/RETIVE/UPDATE/Уничтожение по умолчанию, вы можете ограничить доступные операции, используя стандартные классы разрешений.

## ReadOnlyModelViewSet

## readonlymodelviewset

The `ReadOnlyModelViewSet` class also inherits from `GenericAPIView`. As with `ModelViewSet` it also includes implementations for various actions, but unlike `ModelViewSet` only provides the 'read-only' actions, `.list()` and `.retrieve()`.

Класс `readonlymodelviewset` также наследует от` genericapiview`.
Как и в случае «ModelViewSet», он также включает реализации для различных действий, но в отличие от `modelViewSet` только предоставляет действия« только для чтения »,` .list () `и` .retrieve () `.

#### Example

#### Пример

As with `ModelViewSet`, you'll normally need to provide at least the `queryset` and `serializer_class` attributes. For example:

Как и в случае с `modelviewset`, вам обычно нужно предоставить хотя бы атрибуты` Queryset` и `serializer_class`.
Например:

```
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
```

Again, as with `ModelViewSet`, you can use any of the standard attributes and method overrides available to `GenericAPIView`.

Опять же, как и в случае `modelviewset`, вы можете использовать любой из стандартных атрибутов и переопределения методов, доступных для` genericapiview`.

# Custom ViewSet base classes

# Пользовательские базовые классы видовых сетей

You may need to provide custom `ViewSet` classes that do not have the full set of `ModelViewSet` actions, or that customize the behavior in some other way.

Возможно, вам потребуется предоставить пользовательские классы `viewset`, которые не имеют полного набора действий` modelViewSet` или которые настраивают поведение каким -либо другим способом.

## Example

## Пример

To create a base viewset class that provides `create`, `list` and `retrieve` operations, inherit from `GenericViewSet`, and mixin the required actions:

Чтобы создать базовый класс ViewSet, который предоставляет операции `create`,` list` и `retive`, наследуя от` genericviewset` и смешивайте требуемые действия:

```
from rest_framework import mixins

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass
```

By creating your own base `ViewSet` classes, you can provide common behavior that can be reused in multiple viewsets across your API.

Создавая свои собственные базовые классы `viewset`, вы можете обеспечить общее поведение, которое можно повторно использоваться в нескольких видах по всему вашему API.