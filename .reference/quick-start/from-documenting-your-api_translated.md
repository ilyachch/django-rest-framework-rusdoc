<!-- TRANSLATED by md-translate -->
## Built-in API documentation

## Встроенная документация по API

---

**DEPRECATION NOTICE:** Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10. See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

**УВЕДОМЛЕНИЕ О ДЕПРЕССИИ:** Использование схем на базе CoreAPI было отменено с введением генерации схем на базе OpenAPI в Django REST Framework v3.10. Более подробную информацию смотрите в [Version 3.10 Release Announcement](../community/3.10-announcement.md).

If you are looking for information regarding schemas, you might want to look at these updated resources:

Если вы ищете информацию о схемах, обратите внимание на эти обновленные ресурсы:

1. [Schema](../api-guide/schemas.md)
2. [Documenting your API](../topics/documenting-your-api.md)

1. [Schema](../api-guide/schemas.md)
2. [Документирование вашего API](../topics/documenting-your-api.md)

---

The built-in API documentation includes:

Встроенная документация по API включает:

* Documentation of API endpoints.
* Automatically generated code samples for each of the available API client libraries.
* Support for API interaction.

* Документирование конечных точек API.
* Автоматически генерируемые примеры кода для каждой из доступных клиентских библиотек API.
* Поддержка взаимодействия с API.

### Installation

### Установка

The `coreapi` library is required as a dependency for the API docs. Make sure to install the latest version. The `Pygments` and `Markdown` libraries are optional but recommended.

Библиотека `coreapi` требуется в качестве зависимости для документации по API. Обязательно установите последнюю версию. Библиотеки `Pygments` и `Markdown` являются необязательными, но рекомендуемыми.

To install the API documentation, you'll need to include it in your project's URLconf:

Чтобы установить документацию API, вам нужно включить ее в URLconf вашего проекта:

```
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='My API title'))
]
```

This will include two different views:

Это будет включать в себя два различных вида:

* `/docs/` - The documentation page itself.
* `/docs/schema.js` - A JavaScript resource that exposes the API schema.

* `/docs/` - Сама страница документации.
* `/docs/schema.js` - Ресурс JavaScript, раскрывающий схему API.

---

**Note**: By default `include_docs_urls` configures the underlying `SchemaView` to generate *public* schemas. This means that views will not be instantiated with a `request` instance. i.e. Inside the view `self.request` will be `None`.

**Примечание**: По умолчанию `include_docs_urls` настраивает лежащий в основе `SchemaView` на генерацию *публичных* схем. Это означает, что представления не будут инстанцироваться с экземпляром `request`. Т.е. внутри представления `self.request` будет `None`.

To be compatible with this behaviour, methods (such as `get_serializer` or `get_serializer_class` etc.) which inspect `self.request` or, particularly, `self.request.user` may need to be adjusted to handle this case.

Чтобы быть совместимыми с таким поведением, методы (такие как `get_serializer` или `get_serializer_class` и т.д.), которые проверяют `self.request` или, в частности, `self.request.user`, могут потребовать корректировки для обработки этого случая.

You may ensure views are given a `request` instance by calling `include_docs_urls` with `public=False`:

Вы можете обеспечить предоставление представлениям экземпляра `request`, вызвав `include_docs_urls` с `public=False`:

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

### Документирование ваших представлений

You can document your views by including docstrings that describe each of the available actions. For example:

Вы можете документировать свои представления, включив в них docstrings, описывающие каждое из доступных действий. Например:

```
class UserList(generics.ListAPIView):
    """
    Return a list of all the existing users.
    """
```

If a view supports multiple methods, you should split your documentation using `method:` style delimiters.

Если представление поддерживает несколько методов, вы должны разделить документацию, используя разделители в стиле `method:`.

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

При использовании наборов представлений следует использовать соответствующие имена действий в качестве разделителей.

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

Custom actions on viewsets can also be documented in a similar way using the method names as delimiters or by attaching the documentation to action mapping methods.

Пользовательские действия над наборами представлений также можно документировать подобным образом, используя имена методов в качестве разделителей или присоединяя документацию к методам отображения действий.

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

### `documentation` API Reference

The `rest_framework.documentation` module provides three helper functions to help configure the interactive API documentation, `include_docs_urls` (usage shown above), `get_docs_view` and `get_schemajs_view`.

Модуль `rest_framework.documentation` предоставляет три вспомогательные функции для настройки интерактивной документации API: `include_docs_urls` (использование показано выше), `get_docs_view` и `get_schemajs_view`.

`include_docs_urls` employs `get_docs_view` and `get_schemajs_view` to generate the url patterns for the documentation page and JavaScript resource that exposes the API schema respectively. They expose the following options for customisation. (`get_docs_view` and `get_schemajs_view` ultimately call `rest_frameworks.schemas.get_schema_view()`, see the Schemas docs for more options there.)

`include_docs_urls` использует `get_docs_view` и `get_schemajs_view` для генерации шаблонов url для страницы документации и JavaScript ресурса, который раскрывает схему API соответственно. Они предоставляют следующие опции для настройки. (`get_docs_view` и `get_schemajs_view` в конечном итоге вызывают `rest_frameworks.schemas.get_schema_view()`, дополнительные опции см. в документации по схемам).

#### `include_docs_urls`

#### `include_docs_urls`.

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. Should the schema be considered *public*? If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES` May be used to pass custom permission classes to the `SchemaView`.
* `renderer_classes`: Default `None`. May be used to pass custom renderer classes to the `SchemaView`.

* `title`: D [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]  [...]
[...]  [...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]
[...]  [...]  [...]

#### `get_docs_view`

#### `get_docs_view`.

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES`. May be used to pass custom permission classes to the `SchemaView`.
* `renderer_classes`: Default `None`. May be used to pass custom renderer classes to the `SchemaView`. If `None` the `SchemaView` will be configured with `DocumentationRenderer` and `CoreJSONRenderer` renderers, corresponding to the (default) `html` and `corejson` formats.

* `title`: D [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]  [...]

#### `get_schemajs_view`

#### `get_schemajs_view`.

* `title`: Default `None`. May be used to provide a descriptive title for the schema definition.
* `description`: Default `None`. May be used to provide a description for the schema definition.
* `schema_url`: Default `None`. May be used to pass a canonical base URL for the schema.
* `public`: Default `True`. If `True` schema is generated without a `request` instance being passed to views.
* `patterns`: Default `None`. A list of URLs to inspect when generating the schema. If `None` project's URL conf will be used.
* `generator_class`: Default `rest_framework.schemas.SchemaGenerator`. May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: Default `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. May be used to pass custom authentication classes to the `SchemaView`.
* `permission_classes`: Default `api_settings.DEFAULT_PERMISSION_CLASSES` May be used to pass custom permission classes to the `SchemaView`.

* `title`: По умолчанию `None`. Может использоваться для предоставления описательного заголовка для определения схемы.
* `description`: По умолчанию `None`. Может использоваться для описания определения схемы.
* `schema_url`: По умолчанию `None`. Может использоваться для передачи канонического базового URL для схемы.
* `public`: По умолчанию `True`. Если `True`, схема генерируется без передачи экземпляра `request` в представления.
* `patterns`: По умолчанию `None`. Список URL, которые необходимо проверять при генерации схемы. Если `None`, то будет использоваться URL conf проекта.
* `generator_class`: По умолчанию `rest_framework.schemas.SchemaGenerator`. Может быть использован для указания подкласса `SchemaGenerator`, который будет передан в `SchemaView`.
* `authentication_classes`: По умолчанию `api_settings.DEFAULT_AUTHENTICATION_CLASSES`. Может использоваться для передачи пользовательских классов аутентификации в `SchemaView`.
* `permission_classes`: По умолчанию `api_settings.DEFAULT_PERMISSION_CLASSES` Может использоваться для передачи пользовательских классов разрешений в `SchemaView`.

### Customising code samples

### Настройка примеров кода

The built-in API documentation includes automatically generated code samples for each of the available API client libraries.

Встроенная документация по API включает автоматически сгенерированные примеры кода для каждой из доступных клиентских библиотек API.

You may customise these samples by subclassing `DocumentationRenderer`, setting `languages` to the list of languages you wish to support:

Вы можете настроить эти примеры, создав подкласс `DocumentationRenderer`, установив `languages` в список языков, которые вы хотите поддерживать:

```
from rest_framework.renderers import DocumentationRenderer


class CustomRenderer(DocumentationRenderer):
    languages = ['ruby', 'go']
```

For each language you need to provide an `intro` template, detailing installation instructions and such, plus a generic template for making API requests, that can be filled with individual request details. See the [templates for the bundled languages](https://github.com/encode/django-rest-framework/tree/master/rest_framework/templates/rest_framework/docs/langs) for examples.

Для каждого языка необходимо предоставить шаблон `intro`, в котором подробно описаны инструкции по установке и т.п., а также общий шаблон для выполнения запросов API, который может быть заполнен индивидуальными деталями запроса. Примеры смотрите в [шаблонах для поставляемых языков](https://github.com/encode/django-rest-framework/tree/master/rest_framework/templates/rest_framework/docs/langs).

---