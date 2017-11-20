# Маршрутизаторы
> Ресурсный роутинг позволяет быстро объявлять все общие маршруты для заданного ресурсного контроллера. Вместо объявления отдельных маршрутов... ресурсный маршрут объявляет их одной строчкой кода.

— Документация Ruby on Rails

Некоторые веб фреймворки, как Rails, автоматически реализуют механизм логической свзяи URL'ов приложения с входящими запросами.
REST framework добавляет поддержку автоматического роутинга для Джанго, тем самым предоставляя пользователю простой и надежный способ написания логики представлении для набора URL.

## Использование
Ниже приводится пример простого URL conf с использованием `SimpleRouter`.
```python

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```
Метод `register()` должен включать два обязательных аргумента:
* `prefix` - префикс URL, использующийся с данным набором роутеров.
* `viewset` - класс viewset.

Опционально вы можете указать дополнительный аргумент:

* `base_name` - основа для использования с URL именами. Елси аргумент не указан, то базовое имя будет автоматически сгенерировано на основе атрибута queryset из viewset, при наличии такого. Обратите внимание, что если viewset не включает атрибут `queryset`, то вы должны использовать  `base_name` при регистрации viewset.

Пример выше генерирует следующие URL паттерны: 

* URL pattern: `^users/$` Name: `'user-list'`
* URL pattern: `^users/{pk}/$` Name: `'user-detail'`
* URL pattern: `^accounts/$` Name: `'account-list'`
* URL pattern: `^accounts/{pk}/$` Name: `'account-detail'`

**Примечание**: аргумент `base_name` используется для того, чтобы указать исходную часть паттерна имени представления. В примере выше это часть `user` или `account`.

Как правило вам не *требуется* указывать аргументы для `base_name`, но при наличии viewset, в котором вы кастомно определили метод `get_queryset`, viewset может не иметь списка атрибутов `.queryset`. Если вы попробуете зарегистрировать этот viewset, то увидите ошибку, наподобие этой.

```python

'base_name' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```
Это значит, что вам необходимо однозначно указать аргумент `base_name` при регистрации viewset, так как он не может автоматически определяться исходя из имени модели.

# Использование `include` с маршрутизаторами
Атрибут `.urls` экземпляра роутера всего навсего является стандартом списка URL паттернов. Существуют разные способы включения этих URL'ов.
Например, вы можете добавить `router.urls` к списку существующих представлений...

```python
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls
```
Помимо этого вы можете использовать функцию `include` Django, например...

```python

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^', include(router.urls)),
]

```

Пространства имен могут быть URL паттернами роутера

```python

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^api/', include(router.urls, namespace='api')),
]

```
При использовании пространства имен с гиперссылочными сериализаторами, вам также нужно удостовериться, что любой параметр `view_name` сериализаторов корректно отражает пространство имен. В примере выше вам потребовалось бы включить параметр `view_name='api:user-detail` для полей сериализатора, которые связаны гиперссылкой с отдельными представлениями пользователя.

## Дополнительные ссылки и действия

Любые методы viewset, используемые с декораторами `@detail_route` или `@list_route` также будут маршрутизированы. Например, при использовании данного метода на классе `UserViewSet`:

```python


from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import detail_route

class UserViewSet(ModelViewSet):
    ...

    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        ...
```
Дополнительно будет сгенерирован следующий URL паттерн:
* URL паттерн: `^users/{pk}/set_password/$` Имя: `'user-set-password'`
Если вы не хотите использовать стандартную генерацию URL для ваших кастомных действий, то  используйте параметр `url_path` для настройки.
Например, если вы хотите изменить URL для вашего кастомного действия на `^users/{pk}/change-password/$`, то можете написать следующее: 

```python
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import detail_route

class UserViewSet(ModelViewSet):
    ...

    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf], url_path='change-password')
    def set_password(self, request, pk=None):
        ...
```
Этот пример сгенерирует следующий URL паттерн:

* URL паттерн: `^users/{pk}/change-password/$` Имя: `'user-change-password'`
Если вы не хотите использовать стандартные имена для ваших кастомных действий, то можете использовать параметр `url_name` для настройки.

Например, если вы хотите изменить имя вашего кастомного действия на `'user-change-password'`, то можете написать следующее:

```python 
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import detail_route

class UserViewSet(ModelViewSet):
    ...

    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf], url_name='change-password')
    def set_password(self, request, pk=None):
        ...
```
Этот пример сгенерирует следующий URL паттерн:
*URL паттерн: `^users/{pk}/set_password/$` Имя: `'user-change-password'`

Вы также можете использовать параметр `url_path` и `url_name` вместе, чтобы дополнительно контролировать генерирование URL для кастомных представлений.
Для дополнительно информации смотри документацию viewset о создании [дополнительных действий для маршрутизатора](viewsets.md).

# Руководство API
## SimpleRouter
Этот роутер включает маршруты для стандартного набора действий  `list`, `create`, `retrieve`, `update`, `partial_update` и `destroy`. Viewset также может выделить дополнительные методы для маршрутизации, использя декораторы `@detail_route` или `@list_route`.

<style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
    .tg .tg-yw4l{vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-yw4l">URL Style</th>
    <th class="tg-yw4l">Метод HTTP </th>
    <th class="tg-yw4l">Действие</th>
    <th class="tg-yw4l">Имя URL</th>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="2">{prefix}/</td>
    <td class="tg-yw4l">GET</td>
    <td class="tg-yw4l">list</td>
    <td class="tg-yw4l" rowspan="2">{basename}-list</td>
  </tr>
  <tr>
    <td class="tg-yw4l">POST</td>
    <td class="tg-yw4l">create</td>
  </tr>
  <tr>
    <td class="tg-yw4l">{prefix}/{lookup}/</td>
    <td class="tg-yw4l">GET, или как указано в аргументах `методов`</td>
    <td class="tg-yw4l">метод декоратор `@list_route`</td>
    <td class="tg-yw4l">{basename}-{methodname}</td>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="4">{prefix}/{lookup}/{methodname}/</td>
    <td class="tg-yw4l">GET</td>
    <td class="tg-yw4l">retrieve</td>
    <td class="tg-yw4l" rowspan="4">{basename}-detail</td>
  </tr>
  <tr>
    <td class="tg-yw4l">PUT</td>
    <td class="tg-yw4l">update</td>
  </tr>
  <tr>
    <td class="tg-yw4l">PATCH</td>
    <td class="tg-yw4l">partial_update</td>
  </tr>
  <tr>
    <td class="tg-yw4l">DELETE</td>
    <td class="tg-yw4l">destroy</td>
  </tr>
  <tr>
    <td class="tg-yw4l">{prefix}/{lookup}/{methodname}/</td>
    <td class="tg-yw4l">GET, или как указано в аргументах `методов`</td>
    <td class="tg-yw4l">метод декоратор `@detail_route`</td>
    <td class="tg-yw4l">{basename}-{methodname}</td>
  </tr>
</table>

По умолчанию URL'ы, созданные `SimpleRouter` замыкаются слешем. Это поведение можно изменить, поставив `False` в настройке аргумента `trailing_slash` при инициализации роутера. Например:

```python


router = SimpleRouter(trailing_slash=False)
```
Замыкающие слеши очень удобны в Джанго, но они не используются по умолчанию в некоторых других фреймворка, таких как Rails. Что использовать - остается на ваше усмотрение, но некоторые javascript фреймоврки могут ожидать особого стиля роутеров.

Роутер будет сопоставлять значения lookup, содержащие любые символы, кроме слешей и знаков препинания. Для более жетского (или наоборот, менее требовательного) паттерна поиска пропишите атбрибут `lookup_value_regex` в viewset. Например, вы можете ограничить поиски валидными UUID:

```python
class MyModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_id'
    lookup_value_regex = '[0-9a-f]{32}'
```

## DefaultRouter
Этот роутер похож на `SimpleRouter`, который мы рассматривали выше, но помимо этого дополнительно включает корневое представление API, которое возвращает ответ, содержащий гиперссылки ко всем представлениям списка. Он также генерирует роутеры для опционального стиля в формате `.json`.

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
.tg .tg-yw4l{vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-yw4l">URL Style</th>
    <th class="tg-yw4l">Метод HTTP </th>
    <th class="tg-yw4l">Действие</th>
    <th class="tg-yw4l">Имя URL</th>
  </tr>
  <tr>
    <td class="tg-yw4l">[.format]</td>
    <td class="tg-yw4l">GET</td>
    <td class="tg-yw4l">автоматически генерирует корневое представление</td>
    <td class="tg-yw4l">api-root</td>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="2">{prefix}/[.format]</td>
    <td class="tg-yw4l">GET</td>
    <td class="tg-yw4l">list</td>
    <td class="tg-yw4l" rowspan="2">{basename}-list</td>
  </tr>
  <tr>
    <td class="tg-yw4l">POST</td>
    <td class="tg-yw4l">create</td>
  </tr>
  <tr>
    <td class="tg-yw4l">{prefix}/{methodname}/[.format]</td>
    <td class="tg-yw4l">GET, или как указано в аргументах `методов`</td>
    <td class="tg-yw4l">метод декоратор `@list_route`</td>
    <td class="tg-yw4l">{basename}-{methodname}</td>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="4">{prefix}/{lookup}/[.format]</td>
    <td class="tg-yw4l">GET</td>
    <td class="tg-yw4l">retrieve</td>
    <td class="tg-yw4l" rowspan="4">{basename}-detail</td>
  </tr>
  <tr>
    <td class="tg-yw4l">PUT</td>
    <td class="tg-yw4l">update</td>
  </tr>
  <tr>
    <td class="tg-yw4l">PATCH</td>
    <td class="tg-yw4l">partial_update</td>
  </tr>
  <tr>
    <td class="tg-yw4l">DELETE</td>
    <td class="tg-yw4l">destroy</td>
  </tr>
  <tr>
    <td class="tg-yw4l">{prefix}/{lookup}/{methodname}/[.format]</td>
    <td class="tg-yw4l">GET, или как указано в аргументах `методов`</td>
    <td class="tg-yw4l">метод декоратор `@detail_route`</td>
    <td class="tg-yw4l">{basename}-{methodname}</td>
  </tr>
</table>

Как и в случае с `SimpleRouter`, закрывающие слеши путей URL можно удалить, установив значение `False` в настройке `trailing_slash` при инициализации роутера.

```python
router = DefaultRouter(trailing_slash=False)
```

# Кастомные роутеры
Вам редко понадобится применять кастомный роутер, но он может быть полезен, если у вас есть особые требования к структуре URL вашего API. Это позволит вам инкапсулировать структуру URL для повтороного использования, т.е. вам не придется отдельно писать URL паттерны для каждого нового представления.
Самый простой способ применения кастомного роутера это образовать подласс от одного из существующих классов роутера. Атрибут `.routes ` используется для шаблонизирования URL паттернов, которые будут отображаться для каждого viewset. Атрибут `.routes` это список, который содержит именованные кортежи (namedtuple) `Route`.
Аргументы именованных кортежей `Route`:

**url**: Строка, которая представляет URL для маршрутизации. Может включать следующие форматирующие строки:

* `{prefix}` - префикс URL, который будет использоваться с набором путей.
* `{lookup}` - поле поиска, которое используется для сопоставления с единичным экземпляром.
* `{trailing_slash}` - либо '/' или пустая строка, в зависимости от аргумента `trailing_slash`.

**mapping**: отображение имен методов HTTP для методов представления
**name**: Имя URL, используемое в `reverse` вызовах. Может включать следующую форматирующую строку:

* `{basename}` - основа, которая используется с создающимися URL именами.

**initkwargs**: Словарь любого дополнительного аргумена, который должен передаваться при инициализации представления. Заметьте, что аргумент `suffix` зарезервирован для определения типа viewset и используется при создании имени представления и навигационных цепочек.

# Кастомизация динамических путей

Вы также можете кастомизировать маршрутизацию декораторов `@list_route` и `@detail_route`. Чтобы маршрутизировать их внесите именованные кортежи`DynamicListRoute` и/или `DynamicDetailRoute` в списке `.routes list.`.
Аргументы `DynamicListRoute` и `DynamicDetailRoute`:

**url**: Строка, которая представляет URL для маршрутизации. Может включать те же форматирующие строки, как и `Route` и дополнительно принимает форматирующие строки `{methodname}` и `{methodnamehyphen}`.

**name**:  Имя URL, используемое в `reverse` вызовах. Может включать следующие форматирующие строки: `{basename}`, `{methodname}` и `{methodnamehyphen}`.

**initkwargs**:  Словарь любого дополнительного аргумена, который должен передаваться при инициализации представления.

## Пример
Слеюущий пример будет маршрутизировать только действия `list` и `retrieve` и не использует закрывающие слеши.

```python

from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class CustomReadOnlyRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodnamehyphen}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]
```

Давайте посмотрим на пути, которые наш `CustomReadOnlyRouter` сгенерирует для простого viewset.
`views.py`:

```python
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @detail_route()
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
Будет сгенерирован следующий маппинг...

| URL                           | HTTP Method | Action      | URL Name         |
|-------------------------------|-------------|-------------|------------------|
| /users                        | GET         | list        | user-list        |
| /users/{username}             | GET         | retrieve    | user-detail      |
| /users/{username}/group-names | GET         | group_names | user-group-names |


Для другого примера настроек атрибута `.routes` см код источника класса `SimpleRouter`.

## Продвинутые кастомные роутеры
Если вы хотите обеспечить полностью настраивомое поведение, то можете переписать `BaseRouter` и метод `get_urls(self)`. Метод должен инспетировать зарегистрированные viewsets и вернуть список URL паттернов. К зарегистрированным кортежам базовых имен, префиксов и viewset можно получить доступ через атрибут `self.registry`.
Также вы можете переписать метод `get_default_base_name(self, viewset)` или же всегда явно прописывать аргумент `base_name` при регистрации viewsets в роутере.


# Сторонние пакеты
Также доступны следующие пакеты.

##DRF Nested Routers

Пакет [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) активирует вложенные ресурсы в роутере и связанных полях.



##ModelRouter (wq.db.rest)
Пакет [wq.db](https://wq.io/wq.db) предоставляет продвинутый класс `ModelRouter` (и экземпляр singelton), который добавляет API `register_model()` к `DefaultRouter`. Как и в `admin.site.register`, единственный обязательный аргумент для `rest.router.register_model` это класс модели. Разумные значения по умолчанию для префикса URL, сериализатора и представлений будут получены из модели и глобальной конфигурации.

```python

from wq.db import rest
from myapp.models import MyModel

rest.router.register_model(MyModel)
```

## DRF-расширения
Пакет [DRF-расширений](http://chibisov.github.io/drf-extensions/docs/) предоставляет маршруты для создания вложенных viewsets, контроллеров уровня сбора данных и настраиваемых имен конечных точек.
