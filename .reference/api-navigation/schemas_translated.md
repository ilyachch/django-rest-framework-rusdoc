<!-- TRANSLATED by md-translate -->
---

source:

источник:

* schemas

* Схемы

---

# Schema

# Схема

> A machine-readable [schema] describes what resources are available via the API, what their URLs are, how they are represented and what operations they support.
>
> — Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

> Машино читаемый [схема] описывает, какие ресурсы доступны через API, каковы их URL-адреса, как они представлены и какие операции они поддерживают.
>
> - Heroku, [json схема для API платформы Heroku] (https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

---

**Deprecation notice:**

** Уведомление об испаке: **

REST framework's built-in support for generating OpenAPI schemas is **deprecated** in favor of 3rd party packages that can provide this functionality instead. The built-in support will be moved into a separate package and then subsequently retired over the next releases.

Встроенная поддержка REST Framework для создания схем OpenAPI ** устарела ** в пользу сторонних пакетов, которые могут предоставить эту функциональность.
Встроенная поддержка будет перемещена в отдельную упаковку, а затем впоследствии вышла на пенсию в следующих выпусках.

As a full-fledged replacement, we recommend the [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html) package. It has extensive support for generating OpenAPI 3 schemas from REST framework APIs, with both automatic and customisable options available. For further information please refer to [Documenting your API](../topics/documenting-your-api.md#drf-spectacular).

В качестве полноценной замены мы рекомендуем [DRF-Spectacular] (https://drf-spectacular.readthedocs.io/en/latest/readme.html).
Он обладает обширной поддержкой для создания схем OpenAPI 3 из API -интерфейсов REST Framework, с автоматическими и настраиваемыми параметрами.
Для получения дополнительной информации, пожалуйста, обратитесь к [документирование вашего API] (../ темы/документирование-your-api.md#drf-spectacular).

---

API schemas are a useful tool that allow for a range of use cases, including generating reference documentation, or driving dynamic client libraries that can interact with your API.

Схемы API являются полезным инструментом, который позволяет использовать ряд вариантов использования, включая генерацию эталонной документации или динамические библиотеки клиента, которые могут взаимодействовать с вашим API.

Django REST Framework provides support for automatic generation of [OpenAPI](https://github.com/OAI/OpenAPI-Specification) schemas.

Django Rest Framework обеспечивает поддержку автоматической генерации [OpenAPI] (https://github.com/oai/openapi-спецификации) схем.

## Overview

## Обзор

Schema generation has several moving parts. It's worth having an overview:

У поколения схемы есть несколько движущихся частей.
Стоит иметь обзор:

* `SchemaGenerator` is a top-level class that is responsible for walking your configured URL patterns, finding `APIView` subclasses, enquiring for their schema representation, and compiling the final schema object.
* `AutoSchema` encapsulates all the details necessary for per-view schema introspection. Is attached to each view via the `schema` attribute. You subclass `AutoSchema` in order to customize your schema.
* The `generateschema` management command allows you to generate a static schema offline.
* Alternatively, you can route `SchemaView` to dynamically generate and serve your schema.
* `settings.DEFAULT_SCHEMA_CLASS` allows you to specify an `AutoSchema` subclass to serve as your project's default.

* `Schemagenerator`-это класс верхнего уровня, который отвечает за ходьбу ваших настроенных шаблонов URL, поиск подклассов` apiview`, запроса на представление схемы и составление конечного объекта схемы.
* `Autoschema` включает в себя все детали, необходимые для самоанализации схемой на просмотр.
Прикреплен к каждому представлению через атрибут «Схема».
Вы подкласс `autoschema`, чтобы настроить свою схему.
* Команда управления ‘Generateschema позволяет создавать статическую схему в автономном режиме.
* В качестве альтернативы вы можете направить `schemaview` для динамического генерирования и обслуживать свою схему.
* `sutres.default_schema_class` позволяет указать подкласс` autoschema`, который служит дефолтом вашего проекта.

The following sections explain more.

Следующие разделы объясняют больше.

## Generating an OpenAPI Schema

## генерирование схемы OpenAPI

### Install dependencies

### Установить зависимости

```
pip install pyyaml uritemplate
```

* `pyyaml` is used to generate schema into YAML-based OpenAPI format.
* `uritemplate` is used internally to get parameters in path.

* `pyyaml` используется для создания схемы в формат OpenAPI на основе YAML.
* `urtemplate` используется внутри, чтобы получить параметры в пути.

### Generating a static schema with the `generateschema` management command

### генерирование статической схемы с командой управления `Generateschema`

If your schema is static, you can use the `generateschema` management command:

Если ваша схема статическая, вы можете использовать команду управления `Generateschema`:

```bash
./manage.py generateschema --file openapi-schema.yml
```

Once you've generated a schema in this way you can annotate it with any additional information that cannot be automatically inferred by the schema generator.

После того, как вы сгенерировали схему таким образом, вы можете аннотировать ее с помощью любой дополнительной информации, которая не может быть автоматически выводит генератор схемы.

You might want to check your API schema into version control and update it with each new release, or serve the API schema from your site's static media.

Возможно, вы захотите проверить свою схему API в управлении версиями и обновить ее с каждым новым выпуском или обслуживать схему API с статических носителей вашего сайта.

### Generating a dynamic schema with `SchemaView`

### генерирование динамической схемы с `schemaview`

If you require a dynamic schema, because foreign key choices depend on database values, for example, you can route a `SchemaView` that will generate and serve your schema on demand.

Если вам нужна динамическая схема, потому что выбор иностранных ключей зависит от значений базы данных, например, вы можете направить «SchemaView», которая будет генерировать и обслуживать вашу схему по требованию.

To route a `SchemaView`, use the `get_schema_view()` helper.

Чтобы направить `schemaview`, используйте hale` get_schema_view () `helper.

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

#### `get_schema_view ()`

The `get_schema_view()` helper takes the following keyword arguments:

`Get_schema_view ()` helper принимает следующие аргументы ключевого слова:

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

* `title`: может использоваться для предоставления описательного заголовка для определения схемы.
* `description`: более длительный описательный текст.
* `версия`: версия API.
* `url`: может использоваться для прохождения канонического базового URL для схемы.
`` `
schema_view = get_schema_view (
title = 'Server Monitoring API',
url = 'https: //www.example.org/api/'
)
`` `
* `urlConf`: строка, представляющая путь импорта в конфункт URL, для которого вы хотите создать схему API.
Это по умолчанию значения настройки Django `root_urlconf`.
`` `
schema_view = get_schema_view (
title = 'Server Monitoring API',
url = 'https: //www.example.org/api/',
urlConf = 'myProject.urls'
)
`` `
* `Паттерны`: Список шаблонов URL, чтобы ограничить самоанализ схемы.
Если вы хотите, чтобы URL -адреса `myproject.api` были разоблачены в схеме:
`` `
schema_url_patterns = [
Path ('api/', include ('myproject.api.urls')),
]
schema_view = get_schema_view (
title = 'Server Monitoring API',
url = 'https: //www.example.org/api/',
Patterns = schema_url_patterns,
)
`` `
* `public`: может использоваться для указания, следует ли обходить разрешения на представления.
По умолчанию в False
* `generator_class`: может использоваться для указания подкласса« Schemagenerator », который должен быть передан в` schemaview '.
* `authentication_classes`: может использоваться для указания списка классов аутентификации, которые будут применяться к конечной точке схемы.
По умолчанию `sutres.default_authentication_classes`
* `rescision_classes`: может использоваться для указания списка классов разрешений, которые будут применяться к конечной точке схемы.
По умолчанию `sutres.default_permission_classes`.
* `renderer_classes`: может использоваться для прохождения набора классов рендеринга, которые можно использовать для визуализации конечной точки корня API.

## SchemaGenerator

## схемагенератор

**Schema-level customization**

** Настройка уровня схемы **

```python
from rest_framework.schemas.openapi import SchemaGenerator
```

`SchemaGenerator` is a class that walks a list of routed URL patterns, requests the schema for each view and collates the resulting OpenAPI schema.

`Schemagenerator` - это класс, который проходит список направленных шаблонов URL, запрашивает схему для каждого представления и сопоставляет результирующую схему OpenAPI.

Typically you won't need to instantiate `SchemaGenerator` yourself, but you can do so like so:

Как правило, вам не нужно будет создавать экземпляр «Schemagerator» самостоятельно, но вы можете сделать это так:

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

*`title` ** обязательно **: имя API.
* `description`: более длительный описательный текст.
* `версия`: версия API.
По умолчанию до `0,1,0`.
* `url`: корневой URL схемы API.
Эта опция не требуется, если схема не включена в префикс пути.
* `шаблоны`: список URL -адресов для проверки при генерации схемы.
По умолчанию в URL Conf.
* `urlConf`: имя модуля URL Conf для использования при генерации схемы.
По умолчанию на settings.root_urlconf`.

In order to customize the top-level schema, subclass `rest_framework.schemas.openapi.SchemaGenerator` and provide your subclass as an argument to the `generateschema` command or `get_schema_view()` helper function.

Чтобы настроить схему верхнего уровня, подкласс `rest_framework.schemas.openapi.schemagenerator` и предоставьте свой подкласс в качестве аргумента команды` Generateschema 'или `get_schema_view ()` remerper-функция.

### get_schema(self, request=None, public=False)

### get_schema (self, request = none, public = false)

Returns a dictionary that represents the OpenAPI schema:

Возвращает словарь, который представляет схему OpenAPI:

```
generator = SchemaGenerator(title='Stock Prices API')
schema = generator.get_schema()
```

The `request` argument is optional, and may be used if you want to apply per-user permissions to the resulting schema generation.

Аргумент `request` является необязательным и может использоваться, если вы хотите применить разрешения на использования для получения полученной схемы.

This is a good point to override if you want to customize the generated dictionary For example you might wish to add terms of service to the [top-level `info` object](https://swagger.io/specification/#infoObject):

Это хороший момент, чтобы переопределить, если вы хотите настроить сгенерированный словарь, например, вы можете добавить Условия обслуживания к [Object info 'Object] [https://swagger.io/speciation/#infoobject)
:

```
class TOSSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema["info"]["termsOfService"] = "https://example.com/tos.html"
        return schema
```

## AutoSchema

## Autoschema

**Per-View Customization**

** Настройка для просмотра **

```python
from rest_framework.schemas.openapi import AutoSchema
```

By default, view introspection is performed by an `AutoSchema` instance accessible via the `schema` attribute on `APIView`.

По умолчанию интроспекция просмотра выполняется экземпляром `autoschema`, доступным через атрибут« схема »на` apiview`.

```
auto_schema = some_view.schema
```

`AutoSchema` provides the OpenAPI elements needed for each view, request method and path:

`Autoschema` предоставляет элементы OpenAPI, необходимые для каждого представления, метода запроса и пути:

* A list of [OpenAPI components](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject). In DRF terms these are mappings of serializers that describe request and response bodies.
* The appropriate [OpenAPI operation object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject) that describes the endpoint, including path and query parameters for pagination, filtering, and so on.

* Список [openAPI Components] (https://github.com/oai/openapi-peciation/blob/master/versions/3.0.2.md#componentsObject).
С точки зрения DRF это отображения сериалов, которые описывают запросы и ответные тела.
* Соответствующий [OpenAPI Operation Object] (https://github.com/oai/openapi-preciation/blob/master/versions/3.0.2.md#operationObject), описывающая конечную точку, включая параметры пути и запроса для страдания страданиям,
фильтрация и так далее.

```python
components = auto_schema.get_components(...)
operation = auto_schema.get_operation(...)
```

In compiling the schema, `SchemaGenerator` calls `get_components()` and `get_operation()` for each view, allowed method, and path.

При составлении схемы «Schemagenerator» вызывает `get_components ()` и `get_operation ()` для каждого представления, разрешенного метода и пути.

---

**Note**: The automatic introspection of components, and many operation parameters relies on the relevant attributes and methods of `GenericAPIView`: `get_serializer()`, `pagination_class`, `filter_backends`, etc. For basic `APIView` subclasses, default introspection is essentially limited to the URL kwarg path parameters for this reason.

** ПРИМЕЧАНИЕ **: Автоматическое самоанализ компонентов, и многие параметры операции основаны на соответствующих атрибутах и методах `genericapiview`:` get_serializer () `,` pagination_class`, `filter_backends` и т. Д.
, по умолчанию самоанализ по существу ограничено параметрами пути URL Kwarg по этой причине.

---

`AutoSchema` encapsulates the view introspection needed for schema generation. Because of this all the schema generation logic is kept in a single place, rather than being spread around the already extensive view, serializer and field APIs.

`Autoschema` -инкапсулирует представление самоанализ, необходимое для генерации схемы.
Из -за этого вся логика генерации схемы хранится в одном месте, а не распространяется вокруг и без того обширного обзора, сериализатора и полевых API.

Keeping with this pattern, try not to let schema logic leak into your own views, serializers, or fields when customizing the schema generation. You might be tempted to do something like this:

В соответствии с этой моделью, постарайтесь не позволять логике схемы протекать в свои собственные взгляды, сериалы или поля при настройке генерации схемы.
У вас может быть соблазн сделать что -то вроде этого:

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

Здесь подкласс `autoschema` идет в поисках` schema_extra_info` на представление.
Это * ОК * (на самом деле это не больно), но это означает, что вы получите логику схемы, распространяющуюся в ряде разных мест.

Instead try to subclass `AutoSchema` such that the `extra_info` doesn't leak out into the view:

Вместо этого попробуйте подкласс «Autoschema», так что `exuct_info` не протекает в представление:

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

Этот стиль немного более условно, но поддерживает инкапсуляцию кода, связанного с схемой.
Это больше *сплоченного *в *языке *.
Это сохранит остальную часть вашего кода API более аккуратным.

If an option applies to many view classes, rather than creating a specific subclass per-view, you may find it more convenient to allow specifying the option as an `__init__()` kwarg to your base `AutoSchema` subclass:

Если вариант применяется ко многим классам просмотра, вместо того, чтобы создавать конкретный подкласс для каждого просмотра, вы можете найти более удобным, чтобы позволить указать опцию в качестве подкласса `__init __ ()` kwarg для вашего базового подкласса `autoschema`

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

Это экономит вам необходимость создания пользовательского подкласса для обзора для обще используемого опции.

Not all `AutoSchema` methods expose related `__init__()` kwargs, but those for the more commonly needed options do.

Не все методы Autoschema` подвергают связанного `__init __ ()` kwargs, но методы для более часто необходимых вариантов делают.

### `AutoSchema` methods

### `Autoschema` Методы

#### `get_components()`

#### `get_components ()`

Generates the OpenAPI components that describe request and response bodies, deriving their properties from the serializer.

Генерирует компоненты OpenAPI, которые описывают тела запроса и реагирования, выводя их свойства из сериализатора.

Returns a dictionary mapping the component name to the generated representation. By default this has just a single pair but you may override `get_components()` to return multiple pairs if your view uses multiple serializers.

Возвращает словарь, отображающий имя компонента в сгенерированное представление.
По умолчанию у этого есть только одна пара, но вы можете переопределить `get_components ()`, чтобы вернуть несколько пар, если в вашем представлении используются несколько сериализаторов.

#### `get_component_name()`

#### `get_component_name ()`

Computes the component's name from the serializer.

Вычисляет имя компонента из сериализатора.

You may see warnings if your API has duplicate component names. If so you can override `get_component_name()` or pass the `component_name` `__init__()` kwarg (see below) to provide different names.

Вы можете увидеть предупреждения, если у вашего API есть дублирующие имена компонентов.
Если это так, вы можете переопределить `get_component_name ()` или пройти `component_name`` __init __ () `kwarg (см. Ниже), чтобы предоставить разные имена.

#### `get_reference()`

#### `get_reference ()`

Returns a reference to the serializer component. This may be useful if you override `get_schema()`.

Возвращает ссылку на компонент сериализатора.
Это может быть полезно, если вы переопределяете `get_schema ()`.

#### `map_serializer()`

#### `map_serializer ()`

Maps serializers to their OpenAPI representations.

Карты сериализаторов на их представления OpenAPI.

Most serializers should conform to the standard OpenAPI `object` type, but you may wish to override `map_serializer()` in order to customize this or other serializer-level fields.

Большинство сериалов должны соответствовать стандартному типу OpenAPI `Object`, но вы можете переопределить` map_serializer () `, чтобы настроить эти или другие поля уровня сериализатора.

#### `map_field()`

#### `map_field ()`

Maps individual serializer fields to their schema representation. The base implementation will handle the default fields that Django REST Framework provides.

Карты отдельных полей сериализатора с представлением схемы.
Базовая реализация будет обрабатывать поля по умолчанию, которые предоставляет структура Django REST.

For `SerializerMethodField` instances, for which the schema is unknown, or custom field subclasses you should override `map_field()` to generate the correct schema:

Для экземпляров `serializermethodfield`, для которых схема неизвестна, или подклассы пользовательских поля, вы должны переопределить` map_field () `для создания правильной схемы:

```python
class CustomSchema(AutoSchema):
    """Extension of ``AutoSchema`` to add support for custom field schemas."""

    def map_field(self, field):
        # Handle SerializerMethodFields or custom fields here...
        # ...
        return super().map_field(field)
```

Authors of third-party packages should aim to provide an `AutoSchema` subclass, and a mixin, overriding `map_field()` so that users can easily generate schemas for their custom fields.

Авторы сторонних пакетов должны быть направлены на предоставление подкласса Autoschema` и микшина, переоценивая `map_field ()`, чтобы пользователи могли легко генерировать схемы для своих пользовательских полей.

#### `get_tags()`

#### `get_tags ()`

OpenAPI groups operations by tags. By default tags taken from the first path segment of the routed URL. For example, a URL like `/users/{id}/` will generate the tag `users`.

OpenAPI Groups Operations по тегам.
По умолчанию теги, взятые из первого сегмента пути маршрутированного URL.
Например, URL -адрес, подобный `/users/{id}/`, генерирует тег `users`.

You can pass an `__init__()` kwarg to manually specify tags (see below), or override `get_tags()` to provide custom logic.

Вы можете передать `__init __ ()` kwarg, чтобы вручную указать теги (см. Ниже) или переопределить `get_tags ()`, чтобы предоставить пользовательскую логику.

#### `get_operation()`

#### `get_operation ()`

Returns the [OpenAPI operation object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject) that describes the endpoint, including path and query parameters for pagination, filtering, and so on.

Возвращает объект операции OpenAPI] (https://github.com/oai/openapi speciation/blob/master/versions/3.0.2.md#operationObject), описывающий конечную точку, включая параметры пути и запроса для страданий, фильтрации
, и так далее.

Together with `get_components()`, this is the main entry point to the view introspection.

Вместе с `get_components ()` это основная точка входа в представление.

#### `get_operation_id()`

#### `get_operation_id ()`

There must be a unique [operationid](openapi-operationid) for each operation. By default the `operationId` is deduced from the model name, serializer name or view name. The operationId looks like "listItems", "retrieveItem", "updateItem", etc. The `operationId` is camelCase by convention.

Для каждой операции должен быть уникальный [OperationId] (OpenAPI-OperationId).
По умолчанию `OperationId` выводится из имени модели, имени сериализатора или имени просмотра.
OperationID выглядит как «ListItems», «retiveItem», «UpdateItem» и т. Д.

#### `get_operation_id_base()`

#### `get_operation_id_base ()`

If you have several views with the same model name, you may see duplicate operationIds.

Если у вас есть несколько просмотров с тем же именем модели, вы можете увидеть дублирующие операции.

In order to work around this, you can override `get_operation_id_base()` to provide a different base for name part of the ID.

Чтобы обойти это, вы можете переопределить `get_operation_id_base ()`, чтобы предоставить другую основу для имени части идентификатора.

#### `get_serializer()`

#### `get_serializer ()`

If the view has implemented `get_serializer()`, returns the result.

Если представление реализовано `get_serializer ()`, возвращает результат.

#### `get_request_serializer()`

#### `get_request_serializer ()`

By default returns `get_serializer()` but can be overridden to differentiate between request and response objects.

По умолчанию возвращает `get_serializer ()`, но может быть переоборудован, чтобы различать объекты запроса и ответа.

#### `get_response_serializer()`

#### `get_response_serializer ()`

By default returns `get_serializer()` but can be overridden to differentiate between request and response objects.

По умолчанию возвращает `get_serializer ()`, но может быть переоборудован, чтобы различать объекты запроса и ответа.

### `AutoSchema.__init__()` kwargs

### `autoschema .__ init __ ()` kwargs

`AutoSchema` provides a number of `__init__()` kwargs that can be used for common customizations, if the default generated values are not appropriate.

`Autoschema` предоставляет` __init __ () `kwargs, которые можно использовать для общих настройки, если значения, сгенерированные по умолчанию, не подходят.

The available kwargs are:

Доступные Kwargs:

* `tags`: Specify a list of tags.
* `component_name`: Specify the component name.
* `operation_id_base`: Specify the resource-name part of operation IDs.

* `Tags`: укажите список тегов.
* `component_name`: указать имя компонента.
* `Operation_ID_BASE`: укажите ресурсную часть идентификатора операций.

You pass the kwargs when declaring the `AutoSchema` instance on your view:

Вы передаете Kwargs при объявлении экземпляра Autoschema` на своем взгляде:

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

Предполагая, что модель «ПЭТ» и сериализатор «Petserializer» Kwargs в этом примере, вероятно, не нужны.
Часто, однако, вам нужно пройти Kwargs, если у вас есть несколько представлений, нацеленных на одну и ту же модель, или у вас есть несколько представлений с одинаково именованными сериализаторами.

If your views have related customizations that are needed frequently, you can create a base `AutoSchema` subclass for your project that takes additional `__init__()` kwargs to save subclassing `AutoSchema` for each view.

Если в ваших представлениях есть связанные настройки, которые часто необходимы, вы можете создавать базовый подкласс `autoschema` для вашего проекта, который принимает дополнительный` __init __ () `kwargs, чтобы сохранить подкласс` autoschema` для каждого представления.