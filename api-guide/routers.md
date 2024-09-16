<!-- TRANSLATED by md-translate -->
---

источник:
- routers.py

---

# Маршрутизаторы

> Маршрутизация ресурсов позволяет быстро объявить все общие маршруты для данного ресурсного контроллера. Вместо объявления отдельных маршрутов для вашего индекса... ресурсный маршрут объявляет их в одной строке кода.
>
> &mdash; [Ruby on Rails Documentation](https://guides.rubyonrails.org/routing.html)

Некоторые веб-фреймворки, такие как Rails, предоставляют функциональность для автоматического определения того, как URL-адреса приложения должны быть сопоставлены с логикой, которая занимается обработкой входящих запросов.

DRF добавляет в Django поддержку автоматической маршрутизации URL и предоставляет вам простой, быстрый и последовательный способ подключения логики представления к набору URL.

## Использование

Вот пример простого URL conf, который использует `SimpleRouter`.

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```

У метода `register()` есть два обязательных аргумента:

* `prefix` - Префикс URL, который будет использоваться для этого набора маршрутов.
* `viewset` - Класс набора представлений.

По желанию вы можете указать дополнительный аргумент:

* `basename` - Основа, которую следует использовать для создаваемых имен URL. Если значение не задано, то базовое имя будет автоматически генерироваться на основе атрибута `queryset` набора представлений, если он есть. Обратите внимание, что если набор представлений не включает атрибут `queryset`, то вы должны установить `basename` при регистрации набора представлений.

В приведенном выше примере будут сгенерированы следующие шаблоны URL:

* Шаблон URL: `^users/$` Имя: `'user-list'`
* Шаблон URL: `^users/{pk}/$` Имя: `'user-detail'`
* Шаблон URL: `^accounts/$` Имя: `'account-list'`
* Шаблон URL: `^accounts/{pk}/$` Имя: `'account-detail'`

---

**Примечание**: Аргумент `basename` используется для указания начальной части шаблона имени представления. В приведенном выше примере это часть `user` или `account`.

Обычно вам не нужно указывать аргумент `basename`, но если у вас есть набор представлений, в котором вы определили пользовательский метод `get_queryset`, то набор представлений может не иметь атрибута `.queryset`. Если вы попытаетесь зарегистрировать этот набор представлений, вы увидите ошибку, подобную этой:

```text
'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```

Это означает, что вам нужно будет явно задать аргумент `basename` при регистрации набора представлений, поскольку он не может быть автоматически определен из имени модели.

---

### Использование `include` с маршрутизаторами

Атрибут `.urls` экземпляра маршрутизатора - это просто стандартный список шаблонов URL. Существует несколько различных стилей для включения этих URL.

Например, вы можете добавить `router.urls` к списку существующих представлений...

```python
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls
```

В качестве альтернативы вы можете использовать функцию Django `include`, например, так...

```python
urlpatterns = [
    path('forgot-password', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```

Вы можете использовать `include` с пространством имен приложения:

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```

Или как пространство имен приложения и экземпляра:

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```

Более подробную информацию смотрите в документации Django [URL namespaces docs](https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces) и в [`include` API reference](https://docs.djangoproject.com/en/4.0/ref/urls/#include).

---

**Примечание**: При использовании пространства имен с гиперссылками в сериализаторах вам также необходимо убедиться, что любые параметры `view_name` в сериализаторах правильно отражают пространство имен. В примерах выше вам нужно будет включить параметр типа `view_name='app_name:user-detail'` для полей сериализатора, гиперссылка на представление подробных данных пользователя.

Для автоматического создания `view_name` используется шаблон типа `%(имя_модели)-detail`. Если только имена ваших моделей не противоречат друг другу, вам, возможно, будет лучше **не** расставлять имена в представлениях DRF при использовании сериализаторов с гиперссылками.

---

### Маршрутизация для дополнительных действий

Набор представлений может [пометить дополнительные действия для маршрутизации](viewsets.md#добавление-дополнительных-действий-в-маршрутизацию), украсив метод декоратором `@action`. Эти дополнительные действия будут включены в сгенерированные маршруты. Например, дан метод `set_password` для класса `UserViewSet`:

```python
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        ...
```

Будет создан следующий маршрут:

* Шаблон URL: `^users/{pk}/set_password/$`
* Имя URL: `'user-set-password'`.

По умолчанию шаблон URL основан на имени метода, а имя URL представляет собой комбинацию `ViewSet.basename` и имени метода через дефис. Если вы не хотите использовать значения по умолчанию, вы можете указать аргументы `url_path` и `url_name` в декораторе `@action`.

Например, если вы хотите изменить URL для нашего пользовательского действия на `^users/{pk}/change-password/$`, вы можете написать:

```python
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
            url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        ...
```

Приведенный выше пример теперь будет генерировать следующий шаблон URL:

* URL путь: `^users/{pk}/change-password/$`
* Имя URL: `'user-change_password'`.

### Использование Django `path()` с маршрутизаторами

По умолчанию URL, создаваемые маршрутизаторами, используют регулярные выражения. Это поведение можно изменить, установив аргумент `use_regex_path` в `False` при инстанцировании маршрутизатора, в этом случае будут использоваться [преобразователи путей](https://docs.djangoproject.com/en/2.0/releases/2.0/#simplified-url-routing-syntax). Например:

```python
router = SimpleRouter(use_regex_path=False)
```

Маршрутизатор будет соответствовать значениям поиска, содержащим любые символы, кроме косой черты и точки. Чтобы получить более строгий (или более мягкий) шаблон поиска, установите атрибут `lookup_value_regex` в наборе представлений или `lookup_value_converter` при использовании конвертеров путей. Например, вы можете ограничить поиск допустимыми UUID:

```python
class MyModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_id'
    lookup_value_regex = '[0-9a-f]{32}'

class MyPathModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_uuid'
    lookup_value_converter = 'uuid'
```

Обратите внимание, что преобразователи путей будут использоваться для всех URL, зарегистрированных в маршрутизаторе, включая действия набора представлений.

# Руководство по API

## SimpleRouter

Этот маршрутизатор включает маршруты для стандартного набора действий `list`, `create`, `retrieve`, `update`, `partial_update` и `destroy`. Набор представлений также может отметить дополнительные методы для маршрутизации, используя декоратор `@action`.

| URL Style                     | HTTP Method                                | Action                                     | URL Name              |
| ----------------------------- | ------------------------------------------ | ------------------------------------------ | --------------------- |
| {prefix}/                     | GET                                        | list                                       | {basename}-list       |
|                               | POST                                       | create                                     |                       |
| {prefix}/{url_path}/          | GET, или как указано в аргументе `methods` | метод с декоратором `@action(detail=False)`| {basename}-{url_name} |
| {prefix}/{lookup}/            | GET                                        | retrieve                                   | {basename}-detail     |
|                               | PUT                                        | update                                     |                       |
|                               | PATCH                                      | partial_update                             |                       |
|                               | DELETE                                     | destroy                                    |                       |
| {prefix}/{lookup}/{url_path}/ | GET, или как указано в аргументе `methods` | метод с декоратором `@action(detail=True)` | {basename}-{url_name} |

По умолчанию URL, создаваемые `SimpleRouter`, дополняются косой чертой. Это поведение можно изменить, установив аргумент `trailing_slash` в `False` при инстанцировании маршрутизатора. Например:

```python
router = SimpleRouter(trailing_slash=False)
```

## DefaultRouter

Этот маршрутизатор похож на `SimpleRouter`, но дополнительно включает корневое представление API по умолчанию, которое возвращает ответ, содержащий гиперссылки на все представления списка. Он также генерирует маршруты для необязательных суффиксов формата `.json`.

| URL Style                              | HTTP Method                                | Action                                               | URL Name              |
| -------------------------------------- | ------------------------------------------ | ---------------------------------------------------- | --------------------- |
| [.format]                              | GET                                        | автоматически сгенерированное корневое представление | api-root              |
| {prefix}/[.format]                     | GET                                        | list                                                 | {basename}-list       |
|                                        | POST                                       | create                                               |                       |
| {prefix}/{url_path}/[.format]          | GET, или как указано в аргументе `methods` | метод с декоратором `@action(detail=False)`          | {basename}-{url_name} |
| {prefix}/{lookup}/[.format]            | GET                                        | retrieve                                             | {basename}-detail     |
|                                        | PUT                                        | update                                               |                       |
|                                        | PATCH                                      | partial_update                                       |                       |
|                                        | DELETE                                     | destroy                                              |                       |
| {prefix}/{lookup}/{url_path}/[.format] | GET, или как указано в аргументе `methods` | метод с декоратором `@action(detail=True)`           | {basename}-{url_name} |

Как и в `SimpleRouter`, косые черты в маршрутах URL могут быть удалены путем установки аргумента `trailing_slash` в `False` при инстанцировании маршрутизатора.

```python
router = DefaultRouter(trailing_slash=False)
```

# Пользовательские маршрутизаторы

Реализация пользовательского маршрутизатора - это не то, что вам нужно делать очень часто, но это может быть полезно, если у вас есть особые требования к структуре URL для вашего API. Это позволит вам инкапсулировать структуру URL в многократно используемый способ, который гарантирует, что вам не придется писать шаблоны URL в явном виде для каждого нового представления.

Самый простой способ реализации пользовательского маршрутизатора - это подкласс одного из существующих классов маршрутизаторов. Атрибут `.routes` используется для шаблонизации шаблонов URL, которые будут сопоставлены с каждым набором представлений. Атрибут `.routes` представляет собой список кортежей с именем `Route`.

Аргументами кортежа с именем `Route` являются:

**url**: Строка, представляющая URL, который должен быть маршрутизирован. Может включать следующие строки формата:

* `{prefix}` - Префикс URL, который будет использоваться для этого набора маршрутов.
* `{lookup}` - Поле поиска, используемое для сопоставления с одним экземпляром.
* `{trailing_slash}` - Либо '/', либо пустая строка, в зависимости от аргумента `trailing_slash`.

**mapping**: Сопоставление имен методов HTTP с методами представления

**name**: Имя URL, используемое в вызовах `reverse`. Может включать следующую строку формата:

* `{basename}` - Основа, которую следует использовать для создаваемых имен URL.

**initkwargs**: Словарь дополнительных аргументов, которые должны быть переданы при инстанцировании представления. Обратите внимание, что аргументы `detail`, `basename` и `suffix` зарезервированы для интроспекции набора представлений и также используются API просмотра для генерации имени представления и ссылок на хлебные крошки.

## Настройка динамических маршрутов

Вы также можете настроить способ маршрутизации декоратора `@action`. Включите кортеж с именем `DynamicRoute` в список `.routes`, установив аргумент `detail` в соответствии с требованиями для маршрутов на основе списка и на основе деталей. В дополнение к `detail`, аргументами `DynamicRoute` являются:

**url**: Строка, представляющая URL, который должен быть маршрутизирован. Может включать те же строки формата, что и `Route`, и дополнительно принимает строку формата `{url_path}`.

**name**: Имя URL, используемое в вызовах `reverse`. Может включать следующие строки формата:

* `{basename}` - Основа, которую следует использовать для создаваемых имен URL.
* `{url_name}` - `имя URL`, предоставляемое `@action`.

**initkwargs**: Словарь любых дополнительных аргументов, которые должны быть переданы при инстанцировании представления.

## Пример

Следующий пример маршрутизирует только действия `list` и `retrieve` и не использует соглашение о косой черте.

```python
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

Давайте посмотрим на маршруты, которые наш `CustomReadOnlyRouter` будет генерировать для простого набора представлений.

`views.py`:

```python
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

```python
router = CustomReadOnlyRouter()
router.register('users', UserViewSet)
urlpatterns = router.urls
```

Будут созданы следующие отображения...

| URL                           | HTTP Method | Action      | URL Name         |
| ----------------------------- | ----------- | ----------- | ---------------- |
| /users                        | GET         | list        | user-list        |
| /users/{username}             | GET         | retrieve    | user-detail      |
| /users/{username}/group_names | GET         | group_names | user-group-names |

Другой пример установки атрибута `.routes` приведен в исходном коде класса `SimpleRouter`.

## Расширенные пользовательские маршрутизаторы

Если вы хотите обеспечить полностью пользовательское поведение, вы можете переопределить `BaseRouter` и переопределить метод `get_urls(self)`. Метод должен проверить зарегистрированные наборы представлений и вернуть список шаблонов URL. Зарегистрированные кортежи префикса, набора представлений и базового имени можно проверить, обратившись к атрибуту `self.registry`.

Вы также можете переопределить метод `get_default_basename(self, viewset)` или всегда явно задавать аргумент `basename` при регистрации ваших наборов представлений в маршрутизаторе.

# Сторонние пакеты

Также доступны следующие пакеты сторонних производителей.

## DRF Nested Routers

Пакет [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) предоставляет маршрутизаторы и поля отношений для работы с вложенными ресурсами.

## ModelRouter (wq.db.rest)

Пакет [wq.db](https://wq.io/wq.db) предоставляет расширенный класс [ModelRouter](https://wq.io/docs/router) (и экземпляр синглтона), который расширяет `DefaultRouter` с API `register_model()`. Подобно Django's `admin.site.register`, единственным необходимым аргументом для `rest.router.register_model` является класс модели. Разумные значения по умолчанию для префикса url, сериализатора и набора представлений будут определяться из модели и глобальной конфигурации.

```python
from wq.db import rest
from myapp.models import MyModel

rest.router.register_model(MyModel)
```

## DRF-extensions

Пакет [`DRF-extensions`](https://chibisov.github.io/drf-extensions/docs/) предоставляет [маршрутизаторы](https://chibisov.github.io/drf-extensions/docs/#routers) для создания [вложенных наборов представлений](https://chibisov.github.io/drf-extensions/docs/#nested-routes), [контроллеров уровня коллекции](https://chibisov.github.io/drf-extensions/docs/#collection-level-controllers) с [настраиваемыми именами конечных точек](https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name).
