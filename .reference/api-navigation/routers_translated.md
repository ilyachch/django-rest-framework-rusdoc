<!-- TRANSLATED by md-translate -->
---

source:

источник:

* routers.py

* routers.py

---

# Routers

# Маршрутизаторы

> Resource routing allows you to quickly declare all of the common routes for a given resourceful controller. Instead of declaring separate routes for your index... a resourceful route declares them in a single line of code.
>
> — [Ruby on Rails Documentation][cite]

> Маршрутизация ресурсов позволяет быстро объявить все общие маршруты для данного ресурсного контроллера. Вместо объявления отдельных маршрутов для вашего индекса... ресурсный маршрут объявляет их в одной строке кода.
>
> - [Документация Ruby on Rails][cite]

Some Web frameworks such as Rails provide functionality for automatically determining how the URLs for an application should be mapped to the logic that deals with handling incoming requests.

Некоторые веб-фреймворки, такие как Rails, предоставляют функциональность для автоматического определения того, как URL-адреса приложения должны быть сопоставлены с логикой, которая занимается обработкой входящих запросов.

REST framework adds support for automatic URL routing to Django, and provides you with a simple, quick and consistent way of wiring your view logic to a set of URLs.

Фреймворк REST добавляет в Django поддержку автоматической маршрутизации URL и предоставляет вам простой, быстрый и последовательный способ подключения логики представления к набору URL.

## Usage

## Использование

Here's an example of a simple URL conf, that uses `SimpleRouter`.

Вот пример простого URL conf, который использует `SimpleRouter`.

```
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```

There are two mandatory arguments to the `register()` method:

У метода `register()` есть два обязательных аргумента:

* `prefix` - The URL prefix to use for this set of routes.
* `viewset` - The viewset class.

* `prefix` - Префикс URL, который будет использоваться для этого набора маршрутов.
* ``viewset`` - Класс набора представлений.

Optionally, you may also specify an additional argument:

По желанию вы можете указать дополнительный аргумент:

* `basename` - The base to use for the URL names that are created. If unset the basename will be automatically generated based on the `queryset` attribute of the viewset, if it has one. Note that if the viewset does not include a `queryset` attribute then you must set `basename` when registering the viewset.

* `basename` - Основа, которую следует использовать для создаваемых имен URL. Если значение не задано, то базовое имя будет автоматически генерироваться на основе атрибута `queryset` набора представлений, если он есть. Обратите внимание, что если набор представлений не включает атрибут `queryset`, то вы должны установить `basename` при регистрации набора представлений.

The example above would generate the following URL patterns:

В приведенном выше примере будут сгенерированы следующие шаблоны URL:

* URL pattern: `^users/$` Name: `'user-list'`
* URL pattern: `^users/{pk}/$` Name: `'user-detail'`
* URL pattern: `^accounts/$` Name: `'account-list'`
* URL pattern: `^accounts/{pk}/$` Name: `'account-detail'`

* Шаблон URL: `^users/$` Имя: `'user-list'`
* Шаблон URL: `^users/{pk}/$` Имя: `'user-detail'`
* Шаблон URL: `^accounts/$` Имя: `'account-list'`
* Шаблон URL: `^accounts/{pk}/$` Имя: `'account-detail'`

---

**Note**: The `basename` argument is used to specify the initial part of the view name pattern. In the example above, that's the `user` or `account` part.

**Примечание**: Аргумент `basename` используется для указания начальной части шаблона имени представления. В приведенном выше примере это часть `user` или `account`.

Typically you won't *need* to specify the `basename` argument, but if you have a viewset where you've defined a custom `get_queryset` method, then the viewset may not have a `.queryset` attribute set. If you try to register that viewset you'll see an error like this:

Обычно вам не нужно указывать аргумент `basename`, но если у вас есть набор представлений, в котором вы определили пользовательский метод `get_queryset`, то набор представлений может не иметь атрибута `.queryset`. Если вы попытаетесь зарегистрировать этот набор представлений, вы увидите ошибку, подобную этой:

```
'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```

This means you'll need to explicitly set the `basename` argument when registering the viewset, as it could not be automatically determined from the model name.

Это означает, что вам нужно будет явно задать аргумент `basename` при регистрации набора представлений, поскольку он не может быть автоматически определен из имени модели.

---

### Using `include` with routers

### Использование `include` с маршрутизаторами

The `.urls` attribute on a router instance is simply a standard list of URL patterns. There are a number of different styles for how you can include these URLs.

Атрибут `.urls` экземпляра маршрутизатора - это просто стандартный список шаблонов URL. Существует несколько различных стилей для включения этих URL.

For example, you can append `router.urls` to a list of existing views...

Например, вы можете добавить `router.urls` к списку существующих представлений...

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

В качестве альтернативы вы можете использовать функцию Django `include`, например, так...

```
urlpatterns = [
    path('forgot-password', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```

You may use `include` with an application namespace:

Вы можете использовать `include` с пространством имен приложения:

```
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```

Or both an application and instance namespace:

Или как пространство имен приложения и экземпляра:

```
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```

See Django's [URL namespaces docs](https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces) and the [`include` API reference](https://docs.djangoproject.com/en/4.0/ref/urls/#include) for more details.

Более подробную информацию смотрите в документации Django [URL namespaces docs](https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces) и в [`include` API reference](https://docs.djangoproject.com/en/4.0/ref/urls/#include).

---

**Note**: If using namespacing with hyperlinked serializers you'll also need to ensure that any `view_name` parameters on the serializers correctly reflect the namespace. In the examples above you'd need to include a parameter such as `view_name='app_name:user-detail'` for serializer fields hyperlinked to the user detail view.

**Примечание**: При использовании пространства имен с гиперссылками в сериализаторах вам также необходимо убедиться, что любые параметры `view_name` в сериализаторах правильно отражают пространство имен. В примерах выше вам нужно будет включить параметр типа `view_name='app_name:user-detail'` для полей сериализатора, гиперссылка на представление подробных данных пользователя.

The automatic `view_name` generation uses a pattern like `%(model_name)-detail`. Unless your models names actually clash you may be better off **not** namespacing your Django REST Framework views when using hyperlinked serializers.

Для автоматического создания `имени_вида` используется шаблон типа `%(имя_модели)-detail`. Если только имена ваших моделей не противоречат друг другу, вам, возможно, будет лучше ***не **расставлять имена в представлениях Django REST Framework при использовании сериализаторов с гиперссылками.

---

### Routing for extra actions

### Маршрутизация для дополнительных действий

A viewset may [mark extra actions for routing](viewsets.md#marking-extra-actions-for-routing) by decorating a method with the `@action` decorator. These extra actions will be included in the generated routes. For example, given the `set_password` method on the `UserViewSet` class:

Набор представлений может [пометить дополнительные действия для маршрутизации] (viewsets.md#marking-extra-actions-for-routing), украсив метод декоратором `@action`. Эти дополнительные действия будут включены в сгенерированные маршруты. Например, дан метод `set_password` для класса `UserViewSet`:

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

* Шаблон URL: `^users/{pk}/set_password/$`
* Имя URL: `'user-set-password'`.

By default, the URL pattern is based on the method name, and the URL name is the combination of the `ViewSet.basename` and the hyphenated method name. If you don't want to use the defaults for either of these values, you can instead provide the `url_path` and `url_name` arguments to the `@action` decorator.

По умолчанию шаблон URL основан на имени метода, а имя URL представляет собой комбинацию `ViewSet.basename` и имени метода через дефис. Если вы не хотите использовать значения по умолчанию, вы можете указать аргументы `url_path` и `url_name` в декораторе `@action`.

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

Приведенный выше пример теперь будет генерировать следующий шаблон URL:

* URL path: `^users/{pk}/change-password/$`
* URL name: `'user-change_password'`

* URL путь: `^users/{pk}/change-password/$`
* Имя URL: `'user-change_password'`.

# API Guide

# Руководство по API

## SimpleRouter

## SimpleRouter

This router includes routes for the standard set of `list`, `create`, `retrieve`, `update`, `partial_update` and `destroy` actions. The viewset can also mark additional methods to be routed, using the `@action` decorator.

Этот маршрутизатор включает маршруты для стандартного набора действий `list`, `create`, `retrieve`, `update`, `partial_update` и `destroy`. Набор представлений также может отметить дополнительные методы для маршрутизации, используя декоратор `@action`.

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

By default the URLs created by `SimpleRouter` are appended with a trailing slash. This behavior can be modified by setting the `trailing_slash` argument to `False` when instantiating the router. For example:

По умолчанию URL, создаваемые `SimpleRouter`, дополняются косой чертой. Это поведение можно изменить, установив аргумент `trailing_slash` в `False` при инстанцировании маршрутизатора. Например:

```
router = SimpleRouter(trailing_slash=False)
```

Trailing slashes are conventional in Django, but are not used by default in some other frameworks such as Rails. Which style you choose to use is largely a matter of preference, although some javascript frameworks may expect a particular routing style.

В Django косые черты являются традиционными, но не используются по умолчанию в некоторых других фреймворках, таких как Rails. Какой стиль использовать - это в основном вопрос предпочтений, хотя некоторые javascript-фреймворки могут ожидать определенного стиля маршрутизации.

The router will match lookup values containing any characters except slashes and period characters. For a more restrictive (or lenient) lookup pattern, set the `lookup_value_regex` attribute on the viewset. For example, you can limit the lookup to valid UUIDs:

Маршрутизатор будет сопоставлять значения поиска, содержащие любые символы, кроме косой черты и точки. Для более строгого (или мягкого) шаблона поиска установите атрибут `lookup_value_regex` для набора представлений. Например, вы можете ограничить поиск действительными UUID:

```
class MyModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_id'
    lookup_value_regex = '[0-9a-f]{32}'
```

## DefaultRouter

## DefaultRouter

This router is similar to `SimpleRouter` as above, but additionally includes a default API root view, that returns a response containing hyperlinks to all the list views. It also generates routes for optional `.json` style format suffixes.

Этот маршрутизатор похож на `SimpleRouter`, но дополнительно включает корневое представление API по умолчанию, которое возвращает ответ, содержащий гиперссылки на все представления списка. Он также генерирует маршруты для необязательных суффиксов формата `.json`.

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

Как и в `SimpleRouter`, косые черты в маршрутах URL могут быть удалены путем установки аргумента `trailing_slash` в `False` при инстанцировании маршрутизатора.

```
router = DefaultRouter(trailing_slash=False)
```

# Custom Routers

# Пользовательские маршрутизаторы

Implementing a custom router isn't something you'd need to do very often, but it can be useful if you have specific requirements about how the URLs for your API are structured. Doing so allows you to encapsulate the URL structure in a reusable way that ensures you don't have to write your URL patterns explicitly for each new view.

Реализация пользовательского маршрутизатора - это не то, что вам нужно делать очень часто, но это может быть полезно, если у вас есть особые требования к структуре URL для вашего API. Это позволит вам инкапсулировать структуру URL в многократно используемый способ, который гарантирует, что вам не придется писать шаблоны URL в явном виде для каждого нового представления.

The simplest way to implement a custom router is to subclass one of the existing router classes. The `.routes` attribute is used to template the URL patterns that will be mapped to each viewset. The `.routes` attribute is a list of `Route` named tuples.

Самый простой способ реализации пользовательского маршрутизатора - это подкласс одного из существующих классов маршрутизаторов. Атрибут `.routes` используется для шаблонизации шаблонов URL, которые будут сопоставлены с каждым набором представлений. Атрибут `.routes` представляет собой список кортежей с именем `Route`.

The arguments to the `Route` named tuple are:

Аргументами кортежа с именем `Route` являются:

**url**: A string representing the URL to be routed. May include the following format strings:

**url**: Строка, представляющая URL, который должен быть маршрутизирован. Может включать следующие строки формата:

* `{prefix}` - The URL prefix to use for this set of routes.
* `{lookup}` - The lookup field used to match against a single instance.
* `{trailing_slash}` - Either a '/' or an empty string, depending on the `trailing_slash` argument.

* `{prefix}` - Префикс URL, который будет использоваться для этого набора маршрутов.
* `{lookup}` - Поле поиска, используемое для сопоставления с одним экземпляром.
* `{trailing_slash}` - Либо '/', либо пустая строка, в зависимости от аргумента `trailing_slash`.

**mapping**: A mapping of HTTP method names to the view methods

**картография**: Сопоставление имен методов HTTP с методами представления

**name**: The name of the URL as used in `reverse` calls. May include the following format string:

**имя**: Имя URL, используемое в вызовах `reverse`. Может включать следующую строку формата:

* `{basename}` - The base to use for the URL names that are created.

* `{basename}` - Основа, которую следует использовать для создаваемых имен URL.

**initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view. Note that the `detail`, `basename`, and `suffix` arguments are reserved for viewset introspection and are also used by the browsable API to generate the view name and breadcrumb links.

**initkwargs**: Словарь дополнительных аргументов, которые должны быть переданы при инстанцировании представления. Обратите внимание, что аргументы `detail`, `basename` и `suffix` зарезервированы для интроспекции набора представлений и также используются API просмотра для генерации имени представления и ссылок на хлебные крошки.

## Customizing dynamic routes

## Настройка динамических маршрутов

You can also customize how the `@action` decorator is routed. Include the `DynamicRoute` named tuple in the `.routes` list, setting the `detail` argument as appropriate for the list-based and detail-based routes. In addition to `detail`, the arguments to `DynamicRoute` are:

Вы также можете настроить способ маршрутизации декоратора `@action`. Включите кортеж с именем `DynamicRoute` в список `.routes`, установив аргумент `detail` в соответствии с требованиями для маршрутов на основе списка и на основе деталей. В дополнение к `detail`, аргументами `DynamicRoute` являются:

**url**: A string representing the URL to be routed. May include the same format strings as `Route`, and additionally accepts the `{url_path}` format string.

**url**: Строка, представляющая URL, который должен быть маршрутизирован. Может включать те же строки формата, что и `Route`, и дополнительно принимает строку формата `{url_path}`.

**name**: The name of the URL as used in `reverse` calls. May include the following format strings:

**имя**: Имя URL, используемое в вызовах `reverse`. Может включать следующие строки формата:

* `{basename}` - The base to use for the URL names that are created.
* `{url_name}` - The `url_name` provided to the `@action`.

* `{basename}` - Основа, которую следует использовать для создаваемых имен URL.
* `{url_name}` - `имя URL`, предоставляемое `@action`.

**initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view.

**initkwargs**: Словарь любых дополнительных аргументов, которые должны быть переданы при инстанцировании представления.

## Example

## Пример

The following example will only route to the `list` and `retrieve` actions, and does not use the trailing slash convention.

Следующий пример маршрутизирует только действия `list` и `retrieve` и не использует соглашение о косой черте.

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

Давайте посмотрим на маршруты, которые наш `CustomReadOnlyRouter` будет генерировать для простого набора представлений.

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

Будут созданы следующие отображения...

<table border=1>
    <tr><th>URL</th><th>HTTP Method</th><th>Action</th><th>URL Name</th></tr>
    <tr><td>/users</td><td>GET</td><td>list</td><td>user-list</td></tr>
    <tr><td>/users/{username}</td><td>GET</td><td>retrieve</td><td>user-detail</td></tr>
    <tr><td>/users/{username}/group_names</td><td>GET</td><td>group_names</td><td>user-group-names</td></tr>
</table>

For another example of setting the `.routes` attribute, see the source code for the `SimpleRouter` class.

Другой пример установки атрибута `.routes` приведен в исходном коде класса `SimpleRouter`.

## Advanced custom routers

## Расширенные пользовательские маршрутизаторы

If you want to provide totally custom behavior, you can override `BaseRouter` and override the `get_urls(self)` method. The method should inspect the registered viewsets and return a list of URL patterns. The registered prefix, viewset and basename tuples may be inspected by accessing the `self.registry` attribute.

Если вы хотите обеспечить полностью пользовательское поведение, вы можете переопределить `BaseRouter` и переопределить метод `get_urls(self)`. Метод должен проверить зарегистрированные наборы представлений и вернуть список шаблонов URL. Зарегистрированные кортежи префикса, набора представлений и базового имени можно проверить, обратившись к атрибуту `self.registry`.

You may also want to override the `get_default_basename(self, viewset)` method, or else always explicitly set the `basename` argument when registering your viewsets with the router.

Вы также можете переопределить метод `get_default_basename(self, viewset)` или всегда явно задавать аргумент `basename` при регистрации ваших наборов представлений в маршрутизаторе.

# Third Party Packages

# Сторонние пакеты

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF Nested Routers

## Вложенные маршрутизаторы DRF

The [drf-nested-routers package](https://github.com/alanjds/drf-nested-routers) provides routers and relationship fields for working with nested resources.

Пакет [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) предоставляет маршрутизаторы и поля отношений для работы с вложенными ресурсами.

## ModelRouter (wq.db.rest)

## ModelRouter (wq.db.rest)

The [wq.db package](https://wq.io/wq.db) provides an advanced [ModelRouter](https://wq.io/docs/router) class (and singleton instance) that extends `DefaultRouter` with a `register_model()` API. Much like Django's `admin.site.register`, the only required argument to `rest.router.register_model` is a model class. Reasonable defaults for a url prefix, serializer, and viewset will be inferred from the model and global configuration.

Пакет [wq.db](https://wq.io/wq.db) предоставляет расширенный класс [ModelRouter](https://wq.io/docs/router) (и экземпляр синглтона), который расширяет `DefaultRouter` с API `register_model()`. Подобно Django's `admin.site.register`, единственным необходимым аргументом для `rest.router.register_model` является класс модели. Разумные значения по умолчанию для префикса url, сериализатора и набора представлений будут определяться из модели и глобальной конфигурации.

```
from wq.db import rest
from myapp.models import MyModel

rest.router.register_model(MyModel)
```

## DRF-extensions

## DRF-extensions

The [`DRF-extensions` package](https://chibisov.github.io/drf-extensions/docs/) provides [routers](https://chibisov.github.io/drf-extensions/docs/#routers) for creating [nested viewsets](https://chibisov.github.io/drf-extensions/docs/#nested-routes), [collection level controllers](https://chibisov.github.io/drf-extensions/docs/#collection-level-controllers) with [customizable endpoint names](https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name).

Пакет [`DRF-extensions`](https://chibisov.github.io/drf-extensions/docs/) предоставляет [маршрутизаторы](https://chibisov.github.io/drf-extensions/docs/#routers) для создания [вложенных наборов представлений](https://chibisov.github.io/drf-extensions/docs/#nested-routes), [контроллеров уровня коллекции](https://chibisov.github.io/drf-extensions/docs/#collection-level-controllers) с [настраиваемыми именами конечных точек](https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name).