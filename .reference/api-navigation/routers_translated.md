<!-- TRANSLATED by md-translate -->
---

source:
    - routers.py

источник:
- routers.py

---

# Routers

# Маршрутизаторы

> Resource routing allows you to quickly declare all of the common routes for a given resourceful controller.  Instead of declaring separate routes for your index... a resourceful route declares them in a single line of code.
>
> &mdash; [Ruby on Rails Documentation](https://guides.rubyonrails.org/routing.html)

> Маршрутизация ресурсов позволяет быстро объявить все общие маршруты для данного находчивого контроллера.
Вместо того, чтобы объявлять отдельные маршруты для вашего индекса ... находчивый маршрут объявляет их в одной строке кода.
>
> & mdash;
[Документация Ruby on Rails] (https://guides.rubyonrails.org/routing.html)

Some Web frameworks such as Rails provide functionality for automatically determining how the URLs for an application should be mapped to the logic that deals with handling incoming requests.

Некоторые веб -структуры, такие как Rails, обеспечивают функциональность для автоматического определения того, как URL -адреса для приложения должны быть сопоставлены с логикой, которая занимается обработкой входящих запросов.

REST framework adds support for automatic URL routing to Django, and provides you with a simple, quick and consistent way of wiring your view logic to a set of URLs.

Framework REST добавляет поддержку автоматической маршрутизации URL -адреса Django и предоставляет вам простой, быстрый и последовательный способ подключения логики вашего представления к набору URL -адресов.

## Usage

## Применение

Here's an example of a simple URL conf, that uses `SimpleRouter`.

Вот пример простого URL Conf, который использует `simpleerouter '.

```
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```

There are two mandatory arguments to the `register()` method:

Существует два обязательных аргумента в методе `Register ()`:

* `prefix` - The URL prefix to use for this set of routes.
* `viewset` - The viewset class.

* `prefix` - префикс URL для использования для этого набора маршрутов.
* `ViewSet` - класс ViewSet.

Optionally, you may also specify an additional argument:

При желании вы также можете указать дополнительный аргумент:

* `basename` - The base to use for the URL names that are created.  If unset the basename will be automatically generated based on the `queryset` attribute of the viewset, if it has one.  Note that if the viewset does not include a `queryset` attribute then you must set `basename` when registering the viewset.

* `baseName` - база для использования для созданных имен URL -адресов.
Если unset, базовое имя будет автоматически сгенерировано на основе атрибута `Queryset` на сет, если оно имеет один.
Обратите внимание, что если набор View не включает атрибут `Queryset`, вы должны установить` baseName` при регистрации сбора просмотра.

The example above would generate the following URL patterns:

Приведенный выше пример будет генерировать следующие шаблоны URL:

* URL pattern: `^users/$`  Name: `'user-list'`
* URL pattern: `^users/{pk}/$`  Name: `'user-detail'`
* URL pattern: `^accounts/$`  Name: `'account-list'`
* URL pattern: `^accounts/{pk}/$`  Name: `'account-detail'`

* URL-шаблон: `^users/$` name: `'Пользовательский список
* URL-шаблон: `^users/{pk}/$` name: `'user-detail'
* URL-шаблон: `^Accounts/$` name: `'' list '' ''
* URL-шаблон: `^Accounts/{pk}/$` name: `'account-detail'

---

**Note**: The `basename` argument is used to specify the initial part of the view name pattern.  In the example above, that's the `user` or `account` part.

** Примечание **: аргумент `baseName` используется для указания начальной части шаблона имени представления.
В приведенном выше примере это часть `пользователь 'или` chounct'.

Typically you won't *need* to specify the `basename` argument, but if you have a viewset where you've defined a custom `get_queryset` method, then the viewset may not have a `.queryset` attribute set.  If you try to register that viewset you'll see an error like this:

Как правило, вам не нужно * указать аргумент `baseName`, но если у вас есть сетчатый набор, в котором вы определили пользовательский метод` get_queryset`, то набор ViewSet может не иметь набора атрибутов `.queryset`.
Если вы попытаетесь зарегистрировать этот вид просмотра, вы увидите такую ошибку:

```
'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```

This means you'll need to explicitly set the `basename` argument when registering the viewset, as it could not be automatically determined from the model name.

Это означает, что вам необходимо явно установить аргумент «BaseName» при регистрации сетчатого сбора, поскольку он не может быть автоматически определен из имени модели.

---

### Using `include` with routers

### с помощью `include` с маршрутизаторами

The `.urls` attribute on a router instance is simply a standard list of URL patterns. There are a number of different styles for how you can include these URLs.

Атрибут `.URLS` в экземпляре маршрутизатора является просто стандартным списком шаблонов URL.
Существует ряд различных стилей того, как вы можете включить эти URL -адреса.

For example, you can append `router.urls` to a list of existing views...

Например, вы можете добавить `router.urls` в список существующих представлений ...

```
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls
```

Alternatively you can use Django's `include` function, like so...

В качестве альтернативы вы можете использовать функцию Django `include`, как и ...

```
urlpatterns = [
    path('forgot-password', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```

You may use `include` with an application namespace:

Вы можете использовать `include` с пространством имен приложений:

```
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```

Or both an application and instance namespace:

Или как пространство имен приложения, и экземпляры:

```
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```

See Django's [URL namespaces docs](https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces) and the [`include` API reference](https://docs.djangoproject.com/en/4.0/ref/urls/#include) for more details.

См. Django [url-namespaces docs] (https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces) и [`` include` api reference] (https: //docs.djangoproject
.com/en/4.0/ref/urls/#включите) для более подробной информации.

---

**Note**: If using namespacing with hyperlinked serializers you'll also need to ensure that any `view_name` parameters
on the serializers correctly reflect the namespace. In the examples above you'd need to include a parameter such as
`view_name='app_name:user-detail'` for serializer fields hyperlinked to the user detail view.

** ПРИМЕЧАНИЕ **: Если вы используете пространство имен с помощью гиперссылки, вам также необходимо убедиться, что любые параметры `view_name`
На сериализаторах правильно отражает пространство имен.
В приведенных выше примерах вам необходимо включить параметр, такой как
`view_name = 'app_name: user-detail' для полей сериализатора, гиперссыщенных в представление с подробностями пользователя.

The automatic `view_name` generation uses a pattern like `%(model_name)-detail`. Unless your models names actually clash
you may be better off **not** namespacing your Django REST Framework views when using hyperlinked serializers.

В генерации Automatic `view_name` используется шаблон, такой как`%(model_name) -detail`.
Если имена ваших моделей фактически сталкиваются
Вам может быть лучше **, а не ** Имена рассылает ваши представления Django Rest Pramework при использовании гиперссыщенных сериалов.

---

### Routing for extra actions

### Маршрутизация для дополнительных действий

A viewset may [mark extra actions for routing](viewsets.md#marking-extra-actions-for-routing) by decorating a method with the `@action` decorator. These extra actions will be included in the generated routes. For example, given the `set_password` method on the `UserViewSet` class:

Взгляд может [отмечать дополнительные действия для маршрутизации] (Viewsets.md#Marking-Extra-Actions-For-Routing), украшая метод с помощью декоратора `@Action`.
Эти дополнительные действия будут включены в сгенерированные маршруты.
Например, с учетом метода `set_password` в классе` userviewset`:

```
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        ...
```

The following route would be generated:

Будет создан следующий маршрут:

* URL pattern: `^users/{pk}/set_password/$`
* URL name: `'user-set-password'`

* URL -шаблон: `^users/{pk}/set_password/$`
* Имя URL: `'Пользовательский наводка-пас-слова'

By default, the URL pattern is based on the method name, and the URL name is the combination of the `ViewSet.basename` and the hyphenated method name.
If you don't want to use the defaults for either of these values, you can instead provide the `url_path` and `url_name` arguments to the `@action` decorator.

По умолчанию шаблон URL основан на имени метода, а имя URL - это комбинация `viewset.basename` и имени по дефисам.
Если вы не хотите использовать по умолчанию по умолчанию для одного из этих значений, вы можете вместо этого предоставить аргументы `url_path` и` url_name` для декоратора `@action`.

For example, if you want to change the URL for our custom action to `^users/{pk}/change-password/$`, you could write:

Например, если вы хотите изменить URL для нашего пользовательского действия на `^users/{pk}/change-password/$`, вы можете написать:

```
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
            url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        ...
```

The above example would now generate the following URL pattern:

Приведенный выше пример теперь генерирует следующий шаблон URL:

* URL path: `^users/{pk}/change-password/$`
* URL name: `'user-change_password'`

* Путь URL: `^users/{pk}/change-password/$`
* Имя URL: `'user-change_password'

# API Guide

# Guide API

## SimpleRouter

## проще

This router includes routes for the standard set of `list`, `create`, `retrieve`, `update`, `partial_update` and `destroy` actions.  The viewset can also mark additional methods to be routed, using the `@action` decorator.

Этот маршрутизатор включает в себя маршруты для стандартного набора `list`,` create`, `retive`,` update`, `partial_update` и` dissult` of.
Viewset также может отмечать дополнительные методы, которые будут направлены, используя декоратор `@Action`.

<table border=1>
    <tr><th>URL Style</th><th>HTTP Method</th><th>Action</th><th>URL Name</th></tr>
    <tr><td rowspan=2>{prefix}/</td><td>GET</td><td>list</td><td rowspan=2>{basename}-list</td></tr></tr>
    <tr><td>POST</td><td>create</td></tr>
    <tr><td>{prefix}/{url_path}/</td><td>GET, or as specified by `methods` argument</td><td>`@action(detail=False)` decorated method</td><td>{basename}-{url_name}</td></tr>
    <tr><td rowspan=4>{prefix}/{lookup}/</td><td>GET</td><td>retrieve</td><td rowspan=4>{basename}-detail</td></tr></tr>
    <tr><td>PUT</td><td>update</td></tr>
    <tr><td>PATCH</td><td>partial_update</td></tr>
    <tr><td>DELETE</td><td>destroy</td></tr>
    <tr><td>{prefix}/{lookup}/{url_path}/</td><td>GET, or as specified by `methods` argument</td><td>`@action(detail=True)` decorated method</td><td>{basename}-{url_name}</td></tr>
</table>

By default the URLs created by `SimpleRouter` are appended with a trailing slash.
This behavior can be modified by setting the `trailing_slash` argument to `False` when instantiating the router.  For example:

По умолчанию URL -адреса, созданные `SimpleRouter
Такое поведение может быть изменено, установив аргумент `trailing_slash` на` false` при создании маршрутизатора.
Например:

```
router = SimpleRouter(trailing_slash=False)
```

Trailing slashes are conventional in Django, but are not used by default in some other frameworks such as Rails.  Which style you choose to use is largely a matter of preference, although some javascript frameworks may expect a particular routing style.

Тяжелые черты являются обычными в Django, но не используются по умолчанию в некоторых других рамках, таких как Rails.
Какой стиль вы выберете для использования, в значительной степени является предпочтением, хотя некоторые рамки JavaScript могут ожидать конкретного стиля маршрутизации.

The router will match lookup values containing any characters except slashes and period characters.  For a more restrictive (or lenient) lookup pattern, set the `lookup_value_regex` attribute on the viewset.  For example, you can limit the lookup to valid UUIDs:

Маршрутизатор будет соответствовать значениям поиска, содержащих любые символы, кроме сменных и периодических символов.
Для более ограничивающего (или снисходительного) шаблона поиска установите атрибут `lookup_value_regex` на сет.
Например, вы можете ограничить поиск достоверным UUIDS:

```
class MyModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_id'
    lookup_value_regex = '[0-9a-f]{32}'
```

## DefaultRouter

## defaultrouter

This router is similar to `SimpleRouter` as above, but additionally includes a default API root view, that returns a response containing hyperlinks to all the list views.  It also generates routes for optional `.json` style format suffixes.

Этот маршрутизатор похож на `simpleerouter ', как указано выше, но дополнительно включает в себя представление API по умолчанию, которое возвращает ответ, содержащий гиперссылки во все представления списка.
Он также генерирует маршруты для дополнительных суффиксов в стиле `.json`.

<table border=1>
    <tr><th>URL Style</th><th>HTTP Method</th><th>Action</th><th>URL Name</th></tr>
    <tr><td>[.format]</td><td>GET</td><td>automatically generated root view</td><td>api-root</td></tr></tr>
    <tr><td rowspan=2>{prefix}/[.format]</td><td>GET</td><td>list</td><td rowspan=2>{basename}-list</td></tr></tr>
    <tr><td>POST</td><td>create</td></tr>
    <tr><td>{prefix}/{url_path}/[.format]</td><td>GET, or as specified by `methods` argument</td><td>`@action(detail=False)` decorated method</td><td>{basename}-{url_name}</td></tr>
    <tr><td rowspan=4>{prefix}/{lookup}/[.format]</td><td>GET</td><td>retrieve</td><td rowspan=4>{basename}-detail</td></tr></tr>
    <tr><td>PUT</td><td>update</td></tr>
    <tr><td>PATCH</td><td>partial_update</td></tr>
    <tr><td>DELETE</td><td>destroy</td></tr>
    <tr><td>{prefix}/{lookup}/{url_path}/[.format]</td><td>GET, or as specified by `methods` argument</td><td>`@action(detail=True)` decorated method</td><td>{basename}-{url_name}</td></tr>
</table>

As with `SimpleRouter` the trailing slashes on the URL routes can be removed by setting the `trailing_slash` argument to `False` when instantiating the router.

Как и в случае с «простым», зацепленные удары на маршрутах URL могут быть удалены, установив аргумент `trailing_slash` на` false` при создании маршрутизатора.

```
router = DefaultRouter(trailing_slash=False)
```

# Custom Routers

# Пользовательские маршрутизаторы

Implementing a custom router isn't something you'd need to do very often, but it can be useful if you have specific requirements about how the URLs for your API are structured.  Doing so allows you to encapsulate the URL structure in a reusable way that ensures you don't have to write your URL patterns explicitly for each new view.

Реализация пользовательского маршрутизатора - это не то, что вам нужно делать очень часто, но это может быть полезно, если у вас есть конкретные требования к тому, как структурированы URL -адреса для вашего API.
Это позволяет вам инкапсулировать структуру URL многократным образом, что гарантирует, что вам не нужно явно писать ваши шаблоны URL для каждого нового представления.

The simplest way to implement a custom router is to subclass one of the existing router classes.  The `.routes` attribute is used to template the URL patterns that will be mapped to each viewset. The `.routes` attribute is a list of `Route` named tuples.

Самый простой способ реализации пользовательского маршрутизатора - это подкласс один из существующих классов маршрутизатора.
Атрибут.
Атрибут `.routes` - это список« маршрута »с именем.

The arguments to the `Route` named tuple are:

Аргументы в «Маршрут» с именем Tuple:

**url**: A string representing the URL to be routed.  May include the following format strings:

** url **: строка, представляющая URL, который будет направлен.
Может включать следующие строки формата:

* `{prefix}` - The URL prefix to use for this set of routes.
* `{lookup}` - The lookup field used to match against a single instance.
* `{trailing_slash}` - Either a '/' or an empty string, depending on the `trailing_slash` argument.

* `{prefix}` - Префикс URL для использования для этого набора маршрутов.
* `{Lookup}` - поле Lookup, используемое для совпадения с одним экземпляром.
* `{Tailing_Slash}` - либо a '/', либо пустая строка, в зависимости от аргумента `trailing_slash`.

**mapping**: A mapping of HTTP method names to the view methods

** Картирование **: отображение имен методов HTTP с методами просмотра

**name**: The name of the URL as used in `reverse` calls. May include the following format string:

** Имя **: Имя URL -адреса, используемое в `обратно вызовах.
Может включать следующую строку формата:

* `{basename}` - The base to use for the URL names that are created.

* `{baseName}` - база для использования для созданных имен URL -адресов.

**initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view.  Note that the `detail`, `basename`, and `suffix` arguments are reserved for viewset introspection and are also used by the browsable API to generate the view name and breadcrumb links.

** initkwargs **: Словарь любых дополнительных аргументов, которые следует передавать при создании взгляда.
Обратите внимание, что аргументы `detail`,` baseName 'и `суффикс предназначены для самоанализа ViewSet, а также используются API -файлом для просмотра для генерации имени просмотра и ссылок на хлебную крошку.

## Customizing dynamic routes

## Настройка динамических маршрутов

You can also customize how the `@action` decorator is routed. Include the `DynamicRoute` named tuple in the `.routes` list, setting the `detail` argument as appropriate for the list-based and detail-based routes. In addition to `detail`, the arguments to `DynamicRoute` are:

Вы также можете настроить, как маршрутизируется декоратор@action`.
Включите «DynamicRoute» с именем Tuple в список `.ROUTES
В дополнение к «Detail» аргументы в отношении «Dynamicroute»:

**url**: A string representing the URL to be routed. May include the same format strings as `Route`, and additionally accepts the `{url_path}` format string.

** url **: строка, представляющая URL, который будет направлен.
Может включать в себя те же строки формата, что и `route`, и дополнительно принимает строку формата` `{url_path}`.

**name**: The name of the URL as used in `reverse` calls. May include the following format strings:

** Имя **: Имя URL -адреса, используемое в `обратно вызовах.
Может включать следующие строки формата:

* `{basename}` - The base to use for the URL names that are created.
* `{url_name}` - The `url_name` provided to the `@action`.

* `{baseName}` - база для использования для созданных имен URL -адресов.
* `{url_name}` - `url_name` предоставлен для`@action`.

**initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view.

** initkwargs **: Словарь любых дополнительных аргументов, которые следует передавать при создании взгляда.

## Example

## Пример

The following example will only route to the `list` and `retrieve` actions, and does not use the trailing slash convention.

Следующий пример будет только перейти к действиям `list` и` reture

```
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class CustomReadOnlyRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
```

Let's take a look at the routes our `CustomReadOnlyRouter` would generate for a simple viewset.

Давайте посмотрим на маршруты, которые наши `CustomReadOnlyRouter

`views.py`:

`views.py`:

```
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=True)
    def group_names(self, request, pk=None):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])
```

`urls.py`:

`urls.py`:

```
router = CustomReadOnlyRouter()
router.register('users', UserViewSet)
urlpatterns = router.urls
```

The following mappings would be generated...

Следующие сопоставления будут сгенерированы ...

<table border=1>
    <tr><th>URL</th><th>HTTP Method</th><th>Action</th><th>URL Name</th></tr>
    <tr><td>/users</td><td>GET</td><td>list</td><td>user-list</td></tr>
    <tr><td>/users/{username}</td><td>GET</td><td>retrieve</td><td>user-detail</td></tr>
    <tr><td>/users/{username}/group_names</td><td>GET</td><td>group_names</td><td>user-group-names</td></tr>
</table>

For another example of setting the `.routes` attribute, see the source code for the `SimpleRouter` class.

Еще один пример настройки атрибута `.routes` см. В классе` simpleerouter '.

## Advanced custom routers

## расширенные пользовательские маршрутизаторы

If you want to provide totally custom behavior, you can override `BaseRouter` and override the `get_urls(self)` method.  The method should inspect the registered viewsets and return a list of URL patterns.  The registered prefix, viewset and basename tuples may be inspected by accessing the `self.registry` attribute.

Если вы хотите обеспечить абсолютно пользовательское поведение, вы можете переопределить «BASEROUTER» и переопределить метод `get_urls (self)`.
Метод должен осмотреть зарегистрированные виды и вернуть список шаблонов URL.
Зарегистрированный префикс, псевдоним и кортежи BaseName можно проверить, доступ к атрибуту `self.registry.

You may also want to override the `get_default_basename(self, viewset)` method, or else always explicitly set the `basename` argument when registering your viewsets with the router.

Вы также можете переопределить метод `get_default_basename (self, viewset)` или всегда явно устанавливает аргумент `baseName 'при регистрации ваших видов с помощью маршрутизатора.

# Third Party Packages

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## DRF Nested Routers

## вложенные маршрутизаторы DRF

The [drf-nested-routers package](https://github.com/alanjds/drf-nested-routers) provides routers and relationship fields for working with nested resources.

[Пакет DRF-nested-Routers] (https://github.com/alanjds/drf-nested-routers) предоставляет маршрутизаторы и поля взаимоотношений для работы с вложенными ресурсами.

## ModelRouter (wq.db.rest)

## modelrouter (wq.db.rest)

The [wq.db package](https://wq.io/wq.db) provides an advanced [ModelRouter](https://wq.io/docs/router) class (and singleton instance) that extends `DefaultRouter` with a `register_model()` API. Much like Django's `admin.site.register`, the only required argument to `rest.router.register_model` is a model class.  Reasonable defaults for a url prefix, serializer, and viewset will be inferred from the model and global configuration.

[WQ.DB Package] (https://wq.io/wq.db) предоставляет расширенный [modelrouter] (https://wq.io/docs/router) класс (и экземпляр Singleton), который расширяет `defaultrouter`
с `Register_model ()` api.
Подобно тому, как Django `admin.site.register`, единственный требуемый аргумент для` rest.router.register_model` - это модельный класс.
Разумные значения по умолчанию для префикса URL, сериализатора и сбора просмотра будут выведены из модели и глобальной конфигурации.

```
from wq.db import rest
from myapp.models import MyModel

rest.router.register_model(MyModel)
```

## DRF-extensions

## drf-extensions

The [`DRF-extensions` package](https://chibisov.github.io/drf-extensions/docs/) provides [routers](https://chibisov.github.io/drf-extensions/docs/#routers) for creating [nested viewsets](https://chibisov.github.io/drf-extensions/docs/#nested-routes), [collection level controllers](https://chibisov.github.io/drf-extensions/docs/#collection-level-controllers) with [customizable endpoint names](https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name).

[`` Drf-extensions` package] (https://chibisov.github.io/drf-extensions/docs/) предоставляет [routers] (https://chibisov.github.io/drf-extensions/docs/#routers
) для создания [вложенных видов] (https://chibisov.github.io/drf-extensions/docs/#nestestor-routes), [контроллеры уровня сбора] (https://chibisov.github.io/drf-extensions/
DOCS/#Коллекция на уровне управления) с [настраиваемыми именами конечных точек] (https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name).