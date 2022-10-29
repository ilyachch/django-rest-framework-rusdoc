## Built-in API documentation

## Встроенная документация API

---

**DEPRECATION NOTICE:** Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10. See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

** Уведомление об ископке: ** Использование схем на основе Coreapi было устарело с введением нативного генерации схем на основе OpenAPI по состоянию на основу Django Rest Framework v3.10.
См. Объявление [версия 3.10 выпуска] (../ Community/3.10-Annoument.md) для получения более подробной информации.

If you are looking for information regarding schemas, you might want to look at these updated resources:

Если вы ищете информацию о схемах, вы можете посмотреть на эти обновленные ресурсы:

1. [Schema](../api-guide/schemas.md)
2. [Documenting your API](../topics/documenting-your-api.md)

1. [Схема] (../ API-Guide/Schemas.md)
2. [документирование вашего API] (../ Темы/документирование-your-api.md)

---

The built-in API documentation includes:

Встроенная документация API включает в себя:

* Documentation of API endpoints.
* Automatically generated code samples for each of the available API client libraries.
* Support for API interaction.

* Документация конечных точек API.
* Автоматически сгенерированные образцы кода для каждой из доступных клиентских библиотек API.
* Поддержка взаимодействия API.

### Installation

### Монтаж

The `coreapi` library is required as a dependency for the API docs. Make sure
to install the latest version. The `Pygments` and `Markdown` libraries
are optional but recommended.

Библиотека Coreapi 'требуется в качестве зависимости для документов API.
Убедиться
Чтобы установить последнюю версию.
Библиотеки `pygments и` markdown`
дополнительные, но рекомендуются.

To install the API documentation, you'll need to include it in your project's URLconf:

Чтобы установить документацию API, вам нужно включить ее в UrlConf вашего проекта:

```
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='My API title'))
]
```


This will include two different views:

Это будет включать два разных просмотра:

* `/docs/` - The documentation page itself.
* `/docs/schema.js` - A JavaScript resource that exposes the API schema.

* `/docs/` - сама страница документации.
* `/docs/schema.js` - ресурс JavaScript, который разоблачает схему API.

---

**Note**: By default `include_docs_urls` configures the underlying `SchemaView` to generate *public* schemas.
This means that views will not be instantiated with a `request` instance. i.e. Inside the view `self.request` will be `None`.

** ПРИМЕЧАНИЕ **: По умолчанию `include_docs_urls` Конфигурирует базовую` schemaview` для генерации*public*схемы.
Это означает, что представления не будут создаваться с помощью экземпляра «запроса».
то есть внутри представления `self.request` будет« нет ».

To be compatible with this behaviour, methods (such as `get_serializer` or `get_serializer_class` etc.) which inspect `self.request` or, particularly, `self.request.user` may need to be adjusted to handle this case.

Чтобы быть совместимым с этим поведением, методы (такие как `get_serializer` или` get_serializer_class` и т. Д.), Которые осматривают `self.request` или, в частности,` self.request.user`, возможно, потребуется адаптировать для обработки этого случая.

You may ensure views are given a `request` instance by calling `include_docs_urls` with `public=False`:

Вы можете убедиться, что представлениям предоставляется экземпляр `request`, вызывая` include_docs_urls` с `public = false`:

```
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    # Generate schema with valid `request` instance:
    path('docs/', include_docs_urls(title='My API title', public=False))
]
```


---

### Documenting your views

### документирование ваших мнений

You can document your views by including docstrings that describe each of the available actions.
For example:

Вы можете документировать свои взгляды, включив Docstrings, которые описывают каждое из доступных действий.
Например:

```
class UserList(generics.ListAPIView):
    """
    Return a list of all the existing users.
    """
```


If a view supports multiple methods, you should split your documentation using `method:` style delimiters.

Если представление поддерживает несколько методов, вы должны разделить свою документацию, используя метод: `стиль делимитер.

```
class UserList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing users.

    post:
    Create a new user instance.
    """
```


When using viewsets, you should use the relevant action names as delimiters.

При использовании Spestions вы должны использовать соответствующие имена действий в качестве разделителей.

```
class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given user.

    list:
    Return a list of all the existing users.

    create:
    Create a new user instance.
    """
```


Custom actions on viewsets can also be documented in a similar way using the method names
as delimiters or by attaching the documentation to action mapping methods.

Пользовательские действия на видах также могут быть задокументированы аналогичным образом, используя имена методов
как разделители или подключив документацию к методам сопоставления действий.

```
class UserViewSet(viewsets.ModelViewset):
    ...

    @action(detail=False, methods=['get', 'post'])
    def some_action(self, request, *args, **kwargs):
        """
        get:
        A description of the get method on the custom action.

        post:
        A description of the post method on the custom action.
        """

    @some_action.mapping.put
    def put_some_action():
        """
        A description of the put method on the custom action.
        """
```


### `documentation` API Reference

### `documentation` api ссылка

The `rest_framework.documentation` module provides three helper functions to help configure the interactive API documentation, `include_docs_urls` (usage shown above), `get_docs_view` and `get_schemajs_view`.

Модуль `rest_framework.documentation` предоставляет три вспомогательные функции, чтобы помочь настроить интерактивную документацию API,` include_docs_urls` (использование, показанное выше), `get_docs_view` и` get_schemajs_view`.

`include_docs_urls` employs `get_docs_view` and `get_schemajs_view` to generate the url patterns for the documentation page and JavaScript resource that exposes the API schema respectively. They expose the following options for customisation. (`get_docs_view` and `get_schemajs_view` ultimately call `rest_frameworks.schemas.get_schema_view()`, see the Schemas docs for more options there.)

`include_docs_urls` использует` get_docs_view` и `get_schemajs_view` для создания шаблонов URL для страницы документации и ресурса JavaScript, который раскрывает схему API соответственно.
Они разоблачают следующие параметры для настройки.
(`get_docs_view` и` get_schemajs_view` в конечном итоге вызовите `rest_frameworks.schemas.get_schema_view ()`, см. Docs схемы для дополнительных параметров.)

#### `include_docs_urls`

#### `include_docs_urls`

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. Should the schema be considered *public*? If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES` May be used to pass custom permission classes to the `SchemaView`.
* `renderer_classes`: Default `None`. May be used to pass custom renderer classes to the `SchemaView`.

* `title`: по умолчанию` none `. Может использоваться для предоставления описательного заголовка для определения схемы.
* `description`: по умолчанию` none `. Может использоваться для предоставления описания определения схемы.
* `schema_url`: по умолчанию` none`. Может использоваться для прохождения канонического базового URL для схемы.
* `public`: по умолчанию` true`. Следует ли считать схему *публичной *? Если схема `true` генерируется без экземпляра« запроса », передаваемого в представления.
* `patterns`: по умолчанию` none `. Список URL -адресов для проверки при генерации схемы. Если будет использоваться URL CONF Project.
* `generator_class`: по умолчанию` rest_framework.schemas.schemagenerator`. Может использоваться для указания подкласса «схемагенератора», который должен быть передан в «SchemaView».
* `authentication_classes`: по умолчанию` api_settings.default_authentication_classes`. Может использоваться для передачи пользовательских классов аутентификации в `schemaview '.
* `rescision_class`: по умолчанию` api_settings.default_permission_classes` может использоваться для передачи пользовательских классов разрешений в `schemaview`.
* `renderer_classes`: по умолчанию` none`. Может использоваться для передачи пользовательских классов рендеринга в «SchemaView».

#### `get_docs_view`

#### `get_docs_view`

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES`. May be used to pass custom permission classes to the `SchemaView`.
* `renderer_classes`: Default `None`. May be used to pass custom renderer classes to the `SchemaView`. If `None` the `SchemaView` will be configured with `DocumentationRenderer` and `CoreJSONRenderer` renderers, corresponding to the (default) `html` and `corejson` formats.

* `title`: по умолчанию` none `. Может использоваться для предоставления описательного заголовка для определения схемы.
* `description`: по умолчанию` none `. Может использоваться для предоставления описания определения схемы.
* `schema_url`: по умолчанию` none`. Может использоваться для прохождения канонического базового URL для схемы.
* `public`: по умолчанию` true`. Если схема `true` генерируется без экземпляра« запроса », передаваемого в представления.
* `patterns`: по умолчанию` none `. Список URL -адресов для проверки при генерации схемы. Если будет использоваться URL CONF Project.
* `generator_class`: по умолчанию` rest_framework.schemas.schemagenerator`. Может использоваться для указания подкласса «схемагенератора», который должен быть передан в «SchemaView».
* `authentication_classes`: по умолчанию` api_settings.default_authentication_classes`. Может использоваться для передачи пользовательских классов аутентификации в `schemaview '.
* `rescision_class`: по умолчанию` api_settings.default_permission_class`. Может использоваться для передачи пользовательских классов разрешений в `schemaview '.
* `renderer_classes`: по умолчанию` none`. Может использоваться для передачи пользовательских классов рендеринга в «SchemaView». Если `none` `schemaview` будет настроен с` рендеристами `DocumentationRenderer` и` corejsonRenderer`, соответствующих форматам (по умолчанию) `html` и` corejson`.

#### `get_schemajs_view`

#### `get_schemajs_view`

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES` May be used to pass custom permission classes to the `SchemaView`.

* `title`: по умолчанию` none `.
Может использоваться для предоставления описательного заголовка для определения схемы.
* `description`: по умолчанию` none `.
Может использоваться для предоставления описания определения схемы.
* `schema_url`: по умолчанию` none`.
Может использоваться для прохождения канонического базового URL для схемы.
* `public`: по умолчанию` true`.
Если схема `true` генерируется без экземпляра« запроса », передаваемого в представления.
* `patterns`: по умолчанию` none `.
Список URL -адресов для проверки при генерации схемы.
Если будет использоваться URL CONF Project.
* `generator_class`: по умолчанию` rest_framework.schemas.schemagenerator`.
Может использоваться для указания подкласса «схемагенератора», который должен быть передан в «SchemaView».
* `authentication_classes`: по умолчанию` api_settings.default_authentication_classes`.
Может использоваться для передачи пользовательских классов аутентификации в `schemaview '.
* `rescision_class`: по умолчанию` api_settings.default_permission_classes` может использоваться для передачи пользовательских классов разрешений в `schemaview`.

### Customising code samples

### Настройка образцов кода

The built-in API documentation includes automatically generated code samples for
each of the available API client libraries.

Встроенная документация API включает в себя автоматически сгенерированные образцы кода для
Каждая из доступных клиентских библиотек API.

You may customise these samples by subclassing `DocumentationRenderer`, setting
`languages` to the list of languages you wish to support:

Вы можете настроить эти образцы путем подкласса `documentrenderer`, настройки
«Языки» в список языков, которые вы хотите поддержать:

```
from rest_framework.renderers import DocumentationRenderer


class CustomRenderer(DocumentationRenderer):
    languages = ['ruby', 'go']
```


For each language you need to provide an `intro` template, detailing installation instructions and such,
plus a generic template for making API requests, that can be filled with individual request details.
See the [templates for the bundled languages](https://github.com/encode/django-rest-framework/tree/master/rest_framework/templates/rest_framework/docs/langs) for examples.

Для каждого языка вам необходимо предоставить шаблон «вступления», детализацию инструкций по установке и тому подобное,
Кроме того, общий шаблон для выполнения запросов API, который может быть заполнен индивидуальными данными запроса.
См.

---