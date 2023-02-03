<!-- TRANSLATED by md-translate -->
---

source:

источник:

* schemas

* схемы

---

# Schema

# Schema

> A machine-readable [schema] describes what resources are available via the API, what their URLs are, how they are represented and what operations they support.
>
> — Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

> Машиночитаемая [схема] описывает, какие ресурсы доступны через API, каковы их URL, как они представлены и какие операции они поддерживают.
>
> - Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

---

**Deprecation notice:**

**Уведомление о сокращении:**

REST framework's built-in support for generating OpenAPI schemas is **deprecated** in favor of 3rd party packages that can provide this functionality instead. The built-in support will be moved into a separate package and then subsequently retired over the next releases.

Встроенная в REST framework поддержка генерации схем OpenAPI **утрачена** в пользу сторонних пакетов, которые могут предоставить эту функциональность вместо нее. Встроенная поддержка будет перенесена в отдельный пакет, а затем в последующих релизах будет удалена.

As a full-fledged replacement, we recommend the [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html) package. It has extensive support for generating OpenAPI 3 schemas from REST framework APIs, with both automatic and customisable options available. For further information please refer to [Documenting your API](../topics/documenting-your-api.md#drf-spectacular).

В качестве полноценной замены мы рекомендуем пакет [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html). Он обладает широкой поддержкой генерации схем OpenAPI 3 из API REST-фреймворка, причем доступны как автоматические, так и настраиваемые опции. За дополнительной информацией обращайтесь к [Documenting your API](../topics/documenting-your-api.md#drf-spectacular).

---

API schemas are a useful tool that allow for a range of use cases, including generating reference documentation, or driving dynamic client libraries that can interact with your API.

Схемы API - это полезный инструмент, который позволяет использовать их в различных случаях, включая создание справочной документации или создание динамических клиентских библиотек, которые могут взаимодействовать с вашим API.

Django REST Framework provides support for automatic generation of [OpenAPI](https://github.com/OAI/OpenAPI-Specification) schemas.

Django REST Framework обеспечивает поддержку автоматической генерации схем [OpenAPI](https://github.com/OAI/OpenAPI-Specification).

## Overview

## Обзор

Schema generation has several moving parts. It's worth having an overview:

Генерация схемы состоит из нескольких движущихся частей. Стоит сделать обзор:

* `SchemaGenerator` is a top-level class that is responsible for walking your configured URL patterns, finding `APIView` subclasses, enquiring for their schema representation, and compiling the final schema object.
* `AutoSchema` encapsulates all the details necessary for per-view schema introspection. Is attached to each view via the `schema` attribute. You subclass `AutoSchema` in order to customize your schema.
* The `generateschema` management command allows you to generate a static schema offline.
* Alternatively, you can route `SchemaView` to dynamically generate and serve your schema.
* `settings.DEFAULT_SCHEMA_CLASS` allows you to specify an `AutoSchema` subclass to serve as your project's default.

* `SchemaGenerator` - это класс верхнего уровня, который отвечает за поиск шаблонов URL, нахождение подклассов `APIView`, запрос их представления схемы и компиляцию конечного объекта схемы.
* `AutoSchema` инкапсулирует все детали, необходимые для интроспекции схемы для каждого представления. Прикрепляется к каждому представлению через атрибут `schema`. Вы подклассифицируете `AutoSchema` для того, чтобы настроить свою схему.
* Команда управления `generateschema` позволяет вам генерировать статическую схему в автономном режиме.
* Альтернативно, вы можете направить `SchemaView` для динамической генерации и обслуживания вашей схемы.
* `settings.DEFAULT_SCHEMA_CLASS` позволяет вам указать подкласс `AutoSchema`, который будет использоваться по умолчанию в вашем проекте.

The following sections explain more.

В следующих разделах рассказывается подробнее.

## Generating an OpenAPI Schema

## Генерация схемы OpenAPI

### Install dependencies

### Установите зависимости

```
pip install pyyaml uritemplate
```

* `pyyaml` is used to generate schema into YAML-based OpenAPI format.
* `uritemplate` is used internally to get parameters in path.

* `pyyaml` используется для генерации схемы в формат OpenAPI на основе YAML.
* `uritemplate` используется для получения параметров в пути.

### Generating a static schema with the `generateschema` management command

### Генерация статической схемы с помощью команды управления `generateschema`.

If your schema is static, you can use the `generateschema` management command:

Если ваша схема статична, вы можете использовать команду управления `generateschema`:

```bash
./manage.py generateschema --file openapi-schema.yml
```

Once you've generated a schema in this way you can annotate it with any additional information that cannot be automatically inferred by the schema generator.

После создания схемы таким образом вы можете аннотировать ее любой дополнительной информацией, которая не может быть автоматически выведена генератором схемы.

You might want to check your API schema into version control and update it with each new release, or serve the API schema from your site's static media.

Вы можете зарегистрировать схему API в системе контроля версий и обновлять ее с каждым новым релизом, или использовать схему API из статического медиа вашего сайта.

### Generating a dynamic schema with `SchemaView`

### Генерация динамической схемы с помощью `SchemaView`.

If you require a dynamic schema, because foreign key choices depend on database values, for example, you can route a `SchemaView` that will generate and serve your schema on demand.

Если вам нужна динамическая схема, например, потому что выбор внешнего ключа зависит от значений базы данных, вы можете создать `SchemaView`, который будет генерировать и обслуживать вашу схему по требованию.

To route a `SchemaView`, use the `get_schema_view()` helper.

Для маршрутизации `SchemaView` используйте помощник `get_schema_view()`.

In `urls.py`:

В `urls.py`:

```python
from rest_framework.schemas import get_schema_view

urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    # ...
]
```

#### `get_schema_view()`

#### `get_schema_view()`.

The `get_schema_view()` helper takes the following keyword arguments:

Помощник `get_schema_view()` принимает следующие аргументы ключевых слов:

* `title`: May be used to provide a descriptive title for the schema definition.
* `description`: Longer descriptive text.
* `version`: The version of the API.
* `url`: May be used to pass a canonical base URL for the schema.
    ```
    schema_view = get_schema_view(
          title='Server Monitoring API',
          url='https://www.example.org/api/'
      )
    ```
* `urlconf`: A string representing the import path to the URL conf that you want to generate an API schema for. This defaults to the value of Django's `ROOT_URLCONF` setting.
    ```
    schema_view = get_schema_view(
          title='Server Monitoring API',
          url='https://www.example.org/api/',
          urlconf='myproject.urls'
      )
    ```
* `patterns`: List of url patterns to limit the schema introspection to. If you only want the `myproject.api` urls to be exposed in the schema:
    ```
    schema_url_patterns = [
          path('api/', include('myproject.api.urls')),
      ]
    
      schema_view = get_schema_view(
          title='Server Monitoring API',
          url='https://www.example.org/api/',
          patterns=schema_url_patterns,
      )
    ```
* `public`: May be used to specify if schema should bypass views permissions. Default to False
* `generator_class`: May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.
* `authentication_classes`: May be used to specify the list of authentication classes that will apply to the schema endpoint. Defaults to `settings.DEFAULT_AUTHENTICATION_CLASSES`
* `permission_classes`: May be used to specify the list of permission classes that will apply to the schema endpoint. Defaults to `settings.DEFAULT_PERMISSION_CLASSES`.
* `renderer_classes`: May be used to pass the set of renderer classes that can be used to render the API root endpoint.

* `title`: [...]
[...]  [...]
[...]  [...]
[...]  [...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]  [...]  [...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]  [...]  [...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]  [...]  [...]
[...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]

## SchemaGenerator

## SchemaGenerator

**Schema-level customization**

**Настройка на уровне схемы**

```python
from rest_framework.schemas.openapi import SchemaGenerator
```

`SchemaGenerator` is a class that walks a list of routed URL patterns, requests the schema for each view and collates the resulting OpenAPI schema.

`SchemaGenerator` - это класс, который просматривает список шаблонов URL, запрашивает схему для каждого представления и собирает результирующую схему OpenAPI.

Typically you won't need to instantiate `SchemaGenerator` yourself, but you can do so like so:

Обычно вам не нужно самостоятельно создавать `SchemaGenerator`, но вы можете сделать это следующим образом:

```
generator = SchemaGenerator(title='Stock Prices API')
```

Arguments:

Аргументы:

* `title` **required**: The name of the API.
* `description`: Longer descriptive text.
* `version`: The version of the API. Defaults to `0.1.0`.
* `url`: The root URL of the API schema. This option is not required unless the schema is included under path prefix.
* `patterns`: A list of URLs to inspect when generating the schema. Defaults to the project's URL conf.
* `urlconf`: A URL conf module name to use when generating the schema. Defaults to `settings.ROOT_URLCONF`.

* ``заголовок`` **обязательно**: Название API.
* `description`: Более длинный описательный текст.
* `version`: Версия API. По умолчанию `0.1.0`.
* `url`: Корневой URL схемы API. Этот параметр не требуется, если схема не включена в префикс path.
* `patterns`: Список URL-адресов для проверки при генерации схемы. По умолчанию используется URL conf проекта.
* `urlconf`: Имя модуля URL conf для использования при генерации схемы. По умолчанию `settings.ROOT_URLCONF`.

In order to customize the top-level schema, subclass `rest_framework.schemas.openapi.SchemaGenerator` and provide your subclass as an argument to the `generateschema` command or `get_schema_view()` helper function.

Чтобы настроить схему верхнего уровня, подкласс `rest_framework.schemas.openapi.SchemaGenerator` и предоставьте свой подкласс в качестве аргумента команде `generateschema` или вспомогательной функции `get_schema_view()`.

### get_schema(self, request=None, public=False)

### get_schema(self, request=None, public=False)

Returns a dictionary that represents the OpenAPI schema:

Возвращает словарь, представляющий схему OpenAPI:

```
generator = SchemaGenerator(title='Stock Prices API')
schema = generator.get_schema()
```

The `request` argument is optional, and may be used if you want to apply per-user permissions to the resulting schema generation.

Аргумент `request` является необязательным и может быть использован, если вы хотите применить разрешения для каждого пользователя к результирующей генерации схемы.

This is a good point to override if you want to customize the generated dictionary For example you might wish to add terms of service to the [top-level `info` object](https://swagger.io/specification/#infoObject):

Например, вы можете добавить условия обслуживания в [объект верхнего уровня `info`](https://swagger.io/specification/#infoObject):

```
class TOSSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema["info"]["termsOfService"] = "https://example.com/tos.html"
        return schema
```

## AutoSchema

## AutoSchema

**Per-View Customization**

**Настройка для каждого вида**

```python
from rest_framework.schemas.openapi import AutoSchema
```

By default, view introspection is performed by an `AutoSchema` instance accessible via the `schema` attribute on `APIView`.

По умолчанию интроспекция представления выполняется экземпляром `AutoSchema`, доступным через атрибут `schema` на `APIView`.

```
auto_schema = some_view.schema
```

`AutoSchema` provides the OpenAPI elements needed for each view, request method and path:

`AutoSchema` предоставляет элементы OpenAPI, необходимые для каждого представления, метода запроса и пути:

* A list of [OpenAPI components](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject). In DRF terms these are mappings of serializers that describe request and response bodies.
* The appropriate [OpenAPI operation object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject) that describes the endpoint, including path and query parameters for pagination, filtering, and so on.

* Список [компонентов OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject). В терминах DRF это отображения сериализаторов, которые описывают тела запроса и ответа.
* Соответствующий [объект операции OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject), описывающий конечную точку, включая путь и параметры запроса для пагинации, фильтрации и так далее.

```python
components = auto_schema.get_components(...)
operation = auto_schema.get_operation(...)
```

In compiling the schema, `SchemaGenerator` calls `get_components()` and `get_operation()` for each view, allowed method, and path.

При компиляции схемы `SchemaGenerator` вызывает `get_components()` и `get_operation()` для каждого представления, разрешенного метода и пути.

---

**Note**: The automatic introspection of components, and many operation parameters relies on the relevant attributes and methods of `GenericAPIView`: `get_serializer()`, `pagination_class`, `filter_backends`, etc. For basic `APIView` subclasses, default introspection is essentially limited to the URL kwarg path parameters for this reason.

**Примечание**: Автоматическая интроспекция компонентов и многих параметров операций опирается на соответствующие атрибуты и методы `GenericAPIView`: `get_serializer()`, `pagination_class`, `filter_backends` и т.д. По этой причине для базовых подклассов `APIView` интроспекция по умолчанию ограничивается параметрами пути URL kwarg.

---

`AutoSchema` encapsulates the view introspection needed for schema generation. Because of this all the schema generation logic is kept in a single place, rather than being spread around the already extensive view, serializer and field APIs.

`AutoSchema` инкапсулирует интроспекцию представления, необходимую для генерации схемы. Благодаря этому вся логика генерации схемы хранится в одном месте, а не распределяется по уже существующим API представления, сериализатора и полей.

Keeping with this pattern, try not to let schema logic leak into your own views, serializers, or fields when customizing the schema generation. You might be tempted to do something like this:

Следуя этому шаблону, старайтесь не допускать утечки логики схемы в ваши собственные представления, сериализаторы или поля при настройке генерации схемы. У вас может возникнуть соблазн сделать что-то вроде этого:

```python
class CustomSchema(AutoSchema):
    """
    AutoSchema subclass using schema_extra_info on the view.
    """
    ...

class CustomView(APIView):
    schema = CustomSchema()
    schema_extra_info = ... some extra info ...
```

Here, the `AutoSchema` subclass goes looking for `schema_extra_info` on the view. This is *OK* (it doesn't actually hurt) but it means you'll end up with your schema logic spread out in a number of different places.

Здесь подкласс `AutoSchema` ищет `schema_extra_info` в представлении. Это *OK* (на самом деле это не вредит), но это означает, что в итоге вы получите логику схемы, разбросанную по разным местам.

Instead try to subclass `AutoSchema` such that the `extra_info` doesn't leak out into the view:

Вместо этого попробуйте подкласс `AutoSchema`, чтобы `extra_info` не просачивалась в представление:

```python
class BaseSchema(AutoSchema):
    """
    AutoSchema subclass that knows how to use extra_info.
    """
    ...

class CustomSchema(BaseSchema):
    extra_info = ... some extra info ...

class CustomView(APIView):
    schema = CustomSchema()
```

This style is slightly more verbose but maintains the encapsulation of the schema related code. It's more *cohesive* in the *parlance*. It'll keep the rest of your API code more tidy.

Этот стиль немного более многословен, но сохраняет инкапсуляцию кода, связанного со схемой. Он более *целостный* в *парламенте*. Это сделает остальной код вашего API более аккуратным.

If an option applies to many view classes, rather than creating a specific subclass per-view, you may find it more convenient to allow specifying the option as an `__init__()` kwarg to your base `AutoSchema` subclass:

Если опция применяется ко многим классам представлений, вместо того, чтобы создавать отдельный подкласс для каждого представления, вам может показаться более удобным разрешить указывать опцию как `__init__()` kwarg для вашего базового подкласса `AutoSchema`:

```python
class CustomSchema(BaseSchema):
    def __init__(self, **kwargs):
        # store extra_info for later
        self.extra_info = kwargs.pop("extra_info")
        super().__init__(**kwargs)

class CustomView(APIView):
    schema = CustomSchema(
        extra_info=... some extra info ...
    )
```

This saves you having to create a custom subclass per-view for a commonly used option.

Это избавит вас от необходимости создавать собственный подкласс для каждого вида для часто используемой опции.

Not all `AutoSchema` methods expose related `__init__()` kwargs, but those for the more commonly needed options do.

Не все методы `AutoSchema` раскрывают соответствующие ключи `__init__()`, но для наиболее часто используемых опций они есть.

### `AutoSchema` methods

### `Автосхема` методы

#### `get_components()`

#### `get_components()`.

Generates the OpenAPI components that describe request and response bodies, deriving their properties from the serializer.

Генерирует компоненты OpenAPI, описывающие тела запросов и ответов, получая их свойства от сериализатора.

Returns a dictionary mapping the component name to the generated representation. By default this has just a single pair but you may override `get_components()` to return multiple pairs if your view uses multiple serializers.

Возвращает словарь, отображающий имя компонента на сгенерированное представление. По умолчанию он содержит только одну пару, но вы можете переопределить `get_components()`, чтобы вернуть несколько пар, если ваше представление использует несколько сериализаторов.

#### `get_component_name()`

#### `get_component_name()`.

Computes the component's name from the serializer.

Вычисляет имя компонента из сериализатора.

You may see warnings if your API has duplicate component names. If so you can override `get_component_name()` or pass the `component_name` `__init__()` kwarg (see below) to provide different names.

Вы можете увидеть предупреждения, если в вашем API есть дублирующиеся имена компонентов. В этом случае вы можете переопределить `get_component_name()` или передать `component_name` `__init__()` kwarg (см. ниже), чтобы обеспечить разные имена.

#### `get_reference()`

#### `get_reference()`.

Returns a reference to the serializer component. This may be useful if you override `get_schema()`.

Возвращает ссылку на компонент сериализатора. Это может быть полезно, если вы переопределите `get_schema()`.

#### `map_serializer()`

#### `map_serializer()`.

Maps serializers to their OpenAPI representations.

Сопоставляет сериализаторы с их представлениями OpenAPI.

Most serializers should conform to the standard OpenAPI `object` type, but you may wish to override `map_serializer()` in order to customize this or other serializer-level fields.

Большинство сериализаторов должны соответствовать стандартному типу OpenAPI `object`, но вы можете переопределить `map_serializer()`, чтобы настроить это или другие поля на уровне сериализатора.

#### `map_field()`

#### `map_field()`.

Maps individual serializer fields to their schema representation. The base implementation will handle the default fields that Django REST Framework provides.

Сопоставляет отдельные поля сериализатора с их схемным представлением. Базовая реализация будет работать с полями по умолчанию, которые предоставляет Django REST Framework.

For `SerializerMethodField` instances, for which the schema is unknown, or custom field subclasses you should override `map_field()` to generate the correct schema:

Для экземпляров `SerializerMethodField`, для которых схема неизвестна, или подклассов пользовательских полей следует переопределить `map_field()`, чтобы сгенерировать правильную схему:

```python
class CustomSchema(AutoSchema):
    """Extension of ``AutoSchema`` to add support for custom field schemas."""

    def map_field(self, field):
        # Handle SerializerMethodFields or custom fields here...
        # ...
        return super().map_field(field)
```

Authors of third-party packages should aim to provide an `AutoSchema` subclass, and a mixin, overriding `map_field()` so that users can easily generate schemas for their custom fields.

Авторы сторонних пакетов должны стремиться предоставить подкласс `AutoSchema` и миксин, переопределяющий `map_field()`, чтобы пользователи могли легко генерировать схемы для своих пользовательских полей.

#### `get_tags()`

#### `get_tags()`.

OpenAPI groups operations by tags. By default tags taken from the first path segment of the routed URL. For example, a URL like `/users/{id}/` will generate the tag `users`.

OpenAPI группирует операции по тегам. По умолчанию теги берутся из первого сегмента пути маршрутизируемого URL. Например, URL типа `/users/{id}/` будет генерировать тег `users`.

You can pass an `__init__()` kwarg to manually specify tags (see below), or override `get_tags()` to provide custom logic.

Вы можете передать кварг `__init__()`, чтобы вручную указать теги (см. ниже), или переопределить `get_tags()`, чтобы обеспечить пользовательскую логику.

#### `get_operation()`

#### `get_operation()`.

Returns the [OpenAPI operation object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject) that describes the endpoint, including path and query parameters for pagination, filtering, and so on.

Возвращает [объект операции OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject), описывающий конечную точку, включая путь и параметры запроса для пагинации, фильтрации и так далее.

Together with `get_components()`, this is the main entry point to the view introspection.

Вместе с `get_components()` это основная точка входа в интроспекцию представления.

#### `get_operation_id()`

#### `get_operation_id()`.

There must be a unique [operationid](openapi-operationid) for each operation. By default the `operationId` is deduced from the model name, serializer name or view name. The operationId looks like "listItems", "retrieveItem", "updateItem", etc. The `operationId` is camelCase by convention.

Для каждой операции должен быть уникальный [operationid] (openapi-operationid). По умолчанию `operationId` выводится из имени модели, имени сериализатора или имени представления. OperationId выглядит как "listItems", "retrieveItem", "updateItem" и т.д. По соглашению `operationId` используется camelCase.

#### `get_operation_id_base()`

#### `get_operation_id_base()`.

If you have several views with the same model name, you may see duplicate operationIds.

Если у вас есть несколько представлений с одинаковым именем модели, вы можете увидеть дублирующиеся идентификаторы операций.

In order to work around this, you can override `get_operation_id_base()` to provide a different base for name part of the ID.

Чтобы обойти это, вы можете переопределить `get_operation_id_base()`, чтобы предоставить другую базу для именной части ID.

#### `get_serializer()`

#### `get_serializer()`.

If the view has implemented `get_serializer()`, returns the result.

Если представление реализовало `get_serializer()`, возвращает результат.

#### `get_request_serializer()`

#### `get_request_serializer()`.

By default returns `get_serializer()` but can be overridden to differentiate between request and response objects.

По умолчанию возвращает `get_serializer()`, но может быть переопределен для различения объектов запроса и ответа.

#### `get_response_serializer()`

#### `get_response_serializer()`.

By default returns `get_serializer()` but can be overridden to differentiate between request and response objects.

По умолчанию возвращает `get_serializer()`, но может быть переопределен для различения объектов запроса и ответа.

### `AutoSchema.__init__()` kwargs

### `AutoSchema.__init__()` kwargs

`AutoSchema` provides a number of `__init__()` kwargs that can be used for common customizations, if the default generated values are not appropriate.

`AutoSchema` предоставляет ряд каргов `__init__()`, которые могут быть использованы для общей настройки, если сгенерированные по умолчанию значения не подходят.

The available kwargs are:

Доступные значения kwargs следующие:

* `tags`: Specify a list of tags.
* `component_name`: Specify the component name.
* `operation_id_base`: Specify the resource-name part of operation IDs.

* `tags`: Укажите список тегов.
* `component_name`: Укажите имя компонента.
* `operation_id_base`: Укажите часть имени ресурса в идентификаторах операций.

You pass the kwargs when declaring the `AutoSchema` instance on your view:

Вы передаете kwargs при объявлении экземпляра `AutoSchema` в вашем представлении:

```
class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    schema = AutoSchema(
        tags=['Pets'],
        component_name='Pet',
        operation_id_base='Pet',
    )
    ...
```

Assuming a `Pet` model and `PetSerializer` serializer, the kwargs in this example are probably not needed. Often, though, you'll need to pass the kwargs if you have multiple view targeting the same model, or have multiple views with identically named serializers.

Предполагая модель `Pet` и сериализатор `PetSerializer`, kwargs в этом примере, вероятно, не нужны. Однако, часто вам придется передавать kwargs, если у вас есть несколько представлений, нацеленных на одну и ту же модель, или несколько представлений с одинаковыми именами сериализаторов.

If your views have related customizations that are needed frequently, you can create a base `AutoSchema` subclass for your project that takes additional `__init__()` kwargs to save subclassing `AutoSchema` for each view.

Если ваши представления имеют связанные настройки, которые часто требуются, вы можете создать базовый подкласс `AutoSchema` для вашего проекта, который принимает дополнительные `__init__()` kwargs, чтобы избежать подклассификации `AutoSchema` для каждого представления.