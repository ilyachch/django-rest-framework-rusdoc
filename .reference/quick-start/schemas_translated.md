<!-- TRANSLATED by md-translate -->
source: schemas.py

Источник: Schemas.py

# Schemas

# Схемы

---

**DEPRECATION NOTICE:** Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10. See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

** Уведомление об ископке: ** Использование схем на основе Coreapi было устарело с введением нативного генерации схем на основе OpenAPI по состоянию на основу Django Rest Framework v3.10.
См. Объявление [версия 3.10 выпуска] (../ Community/3.10-Annoument.md) для получения более подробной информации.

You are probably looking for [this page](../api-guide/schemas.md) if you want latest information regarding schemas.

Вы, вероятно, ищете [эту страницу] (../ API-Guide/Schemas.md), если вы хотите последнюю информацию о схемах.

---

> A machine-readable [schema] describes what resources are available via the API, what their URLs are, how they are represented and what operations they support.
>
> &mdash; Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

> Машино читаемый [схема] описывает, какие ресурсы доступны через API, каковы их URL-адреса, как они представлены и какие операции они поддерживают.
>
> & mdash;
Heroku, [JSON Schema для API платформы Heroku] (https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

API schemas are a useful tool that allow for a range of use cases, including
generating reference documentation, or driving dynamic client libraries that
can interact with your API.

Схемы API являются полезным инструментом, который позволяет использовать ряд вариантов использования, включая
генерирование эталонной документации или динамического клиентского библиотек, которые
может взаимодействовать с вашим API.

## Install Core API & PyYAML

## Установите Core API и Pyyaml

You'll need to install the `coreapi` package in order to add schema support
for REST framework. You probably also want to install `pyyaml`, so that you
can render the schema into the commonly used YAML-based OpenAPI format.

Вам нужно будет установить пакет `coreapi`, чтобы добавить поддержку схемы
Для структуры отдыха.
Вы, вероятно, также хотите установить `pyyaml`, чтобы вы
может привести схему в широко используемый формат OpenAPI на основе YAML.

```
pip install coreapi pyyaml
```


## Quickstart

## Быстрый старт

There are two different ways you can serve a schema description for your API.

Есть два разных способа, которыми вы можете обслуживать описание схемы для вашего API.

### Generating a schema with the `generateschema` management command

### генерирование схемы с командой управления ‘Generateschema`

To generate a static API schema, use the `generateschema` management command.

Чтобы сгенерировать статическую схему API, используйте команду управления Generateschema`.

```shell
$ python manage.py generateschema > schema.yml
```


Once you've generated a schema in this way you can annotate it with any
additional information that cannot be automatically inferred by the schema
generator.

После того, как вы создали схему таким образом, вы можете аннотировать ее любым
Дополнительная информация, которая не может быть автоматически выведена с помощью схемы
генератор.

You might want to check your API schema into version control and update it
with each new release, or serve the API schema from your site's static media.

Вы можете захотеть проверить свою схему API в управлении версиями и обновить ее
С каждым новым выпуском или обслуживайте схему API из статических средств массовой информации вашего сайта.

### Adding a view with `get_schema_view`

### Добавление представления с `get_schema_view`

To add a dynamically generated schema view to your API, use `get_schema_view`.

Чтобы добавить динамически сгенерированное представление схемы в свой API, используйте `get_schema_view`.

```python
from rest_framework.schemas import get_schema_view
from django.urls import path

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path('schema', schema_view),
    ...
]
```


See below [for more details](#the-get_schema_view-shortcut) on customizing a
dynamically generated schema view.

См. Ниже [для более подробной информации] (#the-get_schema_view-shortcut) на настройке
Динамически сгенерированное представление схемы.

## Internal schema representation

## представление внутренней схемы

REST framework uses [Core API](https://www.coreapi.org/) in order to model schema information in
a format-independent representation. This information can then be rendered
into various different schema formats, or used to generate API documentation.

Framework Rest Framework использует [Core API] (https://www.coreapi.org/) для моделирования информации о схеме в
Формат-независимое представление.
Эта информация может быть сделана
в различные форматы схемы или используются для генерации документации API.

When using Core API, a schema is represented as a `Document` which is the
top-level container object for information about the API. Available API
interactions are represented using `Link` objects. Each link includes a URL,
HTTP method, and may include a list of `Field` instances, which describe any
parameters that may be accepted by the API endpoint. The `Link` and `Field`
instances may also include descriptions, that allow an API schema to be
rendered into user documentation.

При использовании Core API схема представлена как «документ», который является
Контейнерный объект верхнего уровня для получения информации об API.
Доступный API
Взаимодействия представлены с использованием объектов `link`.
Каждая ссылка включает URL,
Метод http и может включать список экземпляров `field`, которые описывают любые
параметры, которые могут быть приняты конечной точкой API.
`Link` и` field`
экземпляры могут также включать описания, которые позволяют схеме API
Введен в пользовательскую документацию.

Here's an example of an API description that includes a single `search`
endpoint:

Вот пример описания API, который включает в себя один `search '
конечная точка:

```
coreapi.Document(
    title='Flight Search API',
    url='https://api.example.org/',
    content={
        'search': coreapi.Link(
            url='/search/',
            action='get',
            fields=[
                coreapi.Field(
                    name='from',
                    required=True,
                    location='query',
                    description='City name or airport code.'
                ),
                coreapi.Field(
                    name='to',
                    required=True,
                    location='query',
                    description='City name or airport code.'
                ),
                coreapi.Field(
                    name='date',
                    required=True,
                    location='query',
                    description='Flight date in "YYYY-MM-DD" format.'
                )
            ],
            description='Return flight availability and prices.'
        )
    }
)
```


## Schema output formats

## Форматы вывода схемы

In order to be presented in an HTTP response, the internal representation
has to be rendered into the actual bytes that are used in the response.

Чтобы быть представленным в ответе HTTP, внутреннее представление
должен быть представлен в фактических байтах, которые используются в ответе.

REST framework includes a few different renderers that you can use for
encoding the API schema.

Структура REST включает в себя несколько различных рендереров, для которых вы можете использовать
Кодирование схемы API.

* `renderers.OpenAPIRenderer` - Renders into YAML-based [OpenAPI](https://openapis.org/), the most widely used API schema format.
* `renderers.JSONOpenAPIRenderer` - Renders into JSON-based [OpenAPI](https://openapis.org/).
* `renderers.CoreJSONRenderer` - Renders into [Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding), a format designed for

* `redererers.openapirenderer` - рендеринг в YAML [openApi] (https://openapis.org/), наиболее широко используемый формат схемы API.
* `redererers.jsonopenapirenderer` - renders в json на основе [openapi] (https://openapis.org/).
* `redererers.corejsonrenderer`-рендеринг в [Core JSON] (https://www.coreapi.org/speciation/encoding/#core-json-encoding), формат, предназначенный для

use with the `coreapi` client library.

Используйте с клиентской библиотекой `coreapi.

[Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding) is designed as a canonical format for use with Core API.
REST framework includes a renderer class for handling this media type, which
is available as `renderers.CoreJSONRenderer`.

[Core JSON] (https://www.coreapi.org/speciation/encoding/#core-json-encoding) разработан в качестве канонического формата для использования с Core API.
Структура REST включает в себя класс рендеринга для обработки этого типа медиа, который
доступен в качестве `рендеров.corejsonrenderer`.

## Schemas vs Hypermedia

## схемы против гипермедиа

It's worth pointing out here that Core API can also be used to model hypermedia
responses, which present an alternative interaction style to API schemas.

Здесь стоит отметить, что Core API также можно использовать для моделирования гипермедиа
Ответы, которые представляют альтернативный стиль взаимодействия с схемами API.

With an API schema, the entire available interface is presented up-front
as a single endpoint. Responses to individual API endpoints are then typically
presented as plain data, without any further interactions contained in each
response.

С помощью схемы API весь доступный интерфейс представлен в первую очередь
как единственная конечная точка.
Ответы на отдельные конечные точки API, как правило, обычно
представлены в виде простых данных, без каких -либо дальнейших взаимодействий, содержащихся в каждом
отклик.

With Hypermedia, the client is instead presented with a document containing
both data and available interactions. Each interaction results in a new
document, detailing both the current state and the available interactions.

С гипермедиа клиенту вместо этого представлен документ, содержащий
как данные, так и доступные взаимодействия.
Каждое взаимодействие приводит к новому
Документ, подробно описывая как текущее состояние, так и доступные взаимодействия.

Further information and support on building Hypermedia APIs with REST framework
is planned for a future version.

Дополнительная информация и поддержка по созданию API гипермедиа с структурой REST
запланировано на будущую версию.

---

# Creating a schema

# Создание схемы

REST framework includes functionality for auto-generating a schema,
or allows you to specify one explicitly.

Структура REST включает в себя функциональность для автоматического генерации схемы,
или позволяет вам явно указать.

## Manual Schema Specification

## Спецификация схемы ручной работы

To manually specify a schema you create a Core API `Document`, similar to the
example above.

Чтобы вручную указать схему, вы создаете основной API `Document`, аналогичный
Пример выше.

```
schema = coreapi.Document(
    title='Flight Search API',
    content={
        ...
    }
)
```


## Automatic Schema Generation

## Автоматическая схема.

Automatic schema generation is provided by the `SchemaGenerator` class.

Автоматическая генерация схемы обеспечивается классом схемагенератора.

`SchemaGenerator` processes a list of routed URL patterns and compiles the
appropriately structured Core API Document.

`Schemagenerator'
соответствующим образом структурированный ядро документ API.

Basic usage is just to provide the title for your schema and call
`get_schema()`:

Основное использование - это просто предоставить заголовок для вашей схемы и звонить
`get_schema ()`:

```
generator = schemas.SchemaGenerator(title='Flight Search API')
schema = generator.get_schema()
```


## Per-View Schema Customisation

## настройка схемы для просмотра

By default, view introspection is performed by an `AutoSchema` instance
accessible via the `schema` attribute on `APIView`. This provides the
appropriate Core API `Link` object for the view, request method and path:

По умолчанию, интроспекция просмотра выполняется экземпляром `autoschema`
Доступно через атрибут «Схема» на `apiview`.
Это обеспечивает
Соответствующий Core API `link` объект для представления, метода запроса и пути:

```
auto_schema = view.schema
coreapi_link = auto_schema.get_link(...)
```


(In compiling the schema, `SchemaGenerator` calls `view.schema.get_link()` for
each view, allowed method and path.)

(При составлении схемы, `schemagenerator 'вызывает` view.schema.get_link () `for
Каждый вид, разрешенный метод и путь.)

---

**Note**: For basic `APIView` subclasses, default introspection is essentially
limited to the URL kwarg path parameters. For `GenericAPIView`
subclasses, which includes all the provided class based views, `AutoSchema` will
attempt to introspect serializer, pagination and filter fields, as well as
provide richer path field descriptions. (The key hooks here are the relevant
`GenericAPIView` attributes and methods: `get_serializer`, `pagination_class`,
`filter_backends` and so on.)

** ПРИМЕЧАНИЕ **: Для базовых подклассов `Apiview`, по существу самоанализ по умолчанию
Ограничено параметрами пути URL Kwarg.
Для `genericapiview`
Подклассы, которые включают все предоставленные классовые представления, `autoschema
попытка индивидуально сериализатора, полей лиц и фильтрации, а также
Предоставьте более богатые описания поля пути.
(Ключевые крючки здесь являются соответствующими
`Genericapiview` Атрибуты и методы:` get_serializer`, `pagination_class`,
`filter_backends` и так далее.)

---

To customise the `Link` generation you may:

Чтобы настроить поколение «ссылка», вы можете:

* Instantiate `AutoSchema` on your view with the `manual_fields` kwarg:
    ```
    from rest_framework.views import APIView
      from rest_framework.schemas import AutoSchema

      class CustomView(APIView):
          ...
          schema = AutoSchema(
              manual_fields=[
                  coreapi.Field("extra_field", ...),
              ]
          )
    ```
    This allows extension for the most common case without subclassing.
* Provide an `AutoSchema` subclass with more complex customisation:
    ```
    from rest_framework.views import APIView
      from rest_framework.schemas import AutoSchema

      class CustomSchema(AutoSchema):
          def get_link(...):
              # Implement custom introspection here (or in other sub-methods)

      class CustomView(APIView):
          ...
          schema = CustomSchema()
    ```
    This provides complete control over view introspection.
* Instantiate `ManualSchema` on your view, providing the Core API `Fields` for
the view explicitly:
    ```
    from rest_framework.views import APIView
      from rest_framework.schemas import ManualSchema

      class CustomView(APIView):
          ...
          schema = ManualSchema(fields=[
              coreapi.Field(
                  "first_field",
                  required=True,
                  location="path",
                  schema=coreschema.String()
              ),
              coreapi.Field(
                  "second_field",
                  required=True,
                  location="path",
                  schema=coreschema.String()
              ),
          ])
    ```
    This allows manually specifying the schema for some views whilst maintaining
      automatic generation elsewhere.

* Создание `autoschema` на вашем представлении с помощью` manual_fields` kwarg:
`` `
от rest_framework.views import apiview
от rest_framework.schemas import autoschema
класс CustomView (ApiView):
...
схема = Autoschema (
manual_fields = [
coreapi.field ("Extra_field", ...),
]
)
`` `
Это позволяет расширить для наиболее распространенного случая без подкласса.
* Предоставьте подкласс Autoschema` с более сложной настройкой:
`` `
от rest_framework.views import apiview
от rest_framework.schemas import autoschema
класс Customschema (Autoschema):
def get_link (...):
# Реализуйте пользовательскую самоанализ здесь (или в других подметодах)
класс CustomView (ApiView):
...
schema = customschema ()
`` `
Это обеспечивает полный контроль над интопбцией.
* Создание `hanualschema` на вашем взгляде, предоставляя основной API` fields` для
представление явно:
`` `
от rest_framework.views import apiview
от rest_framework.schemas Импорт Руководство
класс CustomView (ApiView):
...
Schema = Руководство (Fields = [
coreapi.field (
"First_field",
Требуется = true,
местоположение = "Путь",
schema = coreschema.string ()
),
coreapi.field (
"Second_field",
Требуется = true,
местоположение = "Путь",
schema = coreschema.string ()
),
])
`` `
Это позволяет вручную указать схему для некоторых представлений, сохраняя при этом сохранять
Автоматическое поколение в другом месте.

You may disable schema generation for a view by setting `schema` to `None`:

Вы можете отключить генерацию схемы для представления, установив «схему» на «нет»:

```
class CustomView(APIView):
        ...
        schema = None  # Will not appear in schema
```


This also applies to extra actions for `ViewSet`s:

Это также относится к дополнительным действиям для `viewset`s:

```
class CustomViewSet(viewsets.ModelViewSet):

        @action(detail=True, schema=None)
        def extra_action(self, request, pk=None):
            ...
```


---

**Note**: For full details on `SchemaGenerator` plus the `AutoSchema` and
`ManualSchema` descriptors see the [API Reference below](#api-reference).

** ПРИМЕЧАНИЕ **: для получения полной информации о `Schemagenerator` плюс` autoschema` и
`DENAUALSCHEMA 'Дескрипторы см. [Ссылка на API ниже] (#api-reference).

---

# Adding a schema view

# Добавление представления схемы

There are a few different ways to add a schema view to your API, depending on
exactly what you need.

Есть несколько разных способов добавить представление схемы в ваш API, в зависимости от
именно то, что вам нужно.

## The get_schema_view shortcut

## get_schema_view

The simplest way to include a schema in your project is to use the
`get_schema_view()` function.

Самый простой способ включить схему в ваш проект - использовать
`get_schema_view ()` Функция.

```
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="Server Monitoring API")

urlpatterns = [
    path('', schema_view),
    ...
]
```


Once the view has been added, you'll be able to make API requests to retrieve
the auto-generated schema definition.

Как только представление будет добавлено, вы сможете сделать запросы API, чтобы получить
Автопогенерированное определение схемы.

```
$ http http://127.0.0.1:8000/ Accept:application/coreapi+json
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/vnd.coreapi+json

{
    "_meta": {
        "title": "Server Monitoring API"
    },
    "_type": "document",
    ...
}
```


The arguments to `get_schema_view()` are:

Аргументы к `get_schema_view ()` являются:

#### `title`

#### `title`

May be used to provide a descriptive title for the schema definition.

Может использоваться для предоставления описательного заголовка для определения схемы.

#### `url`

#### `url`

May be used to pass a canonical URL for the schema.

Может использоваться для прохождения канонического URL для схемы.

```
schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/'
)
```


#### `urlconf`

#### `urlconf`

A string representing the import path to the URL conf that you want
to generate an API schema for. This defaults to the value of Django's
ROOT_URLCONF setting.

Строка, представляющая путь импорта в конфункт URL, который вы хотите
Чтобы генерировать схему API для.
Это по умолчанию ценности Джанго
Настройка ROOT_URLCONF.

```
schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/',
    urlconf='myproject.urls'
)
```


#### `renderer_classes`

#### `renderer_classes`

May be used to pass the set of renderer classes that can be used to render the API root endpoint.

Может использоваться для прохождения набора классов рендеринга, которые можно использовать для визуализации конечной точки корня API.

```
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer

schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/',
    renderer_classes=[JSONOpenAPIRenderer]
)
```


#### `patterns`

#### `patterns`

List of url patterns to limit the schema introspection to. If you only want the `myproject.api` urls
to be exposed in the schema:

Список моделей URL, чтобы ограничить самоанализ схемы.
Если вы хотите только URL -адреса `myProject.api`
быть выставленным в схеме:

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


#### `generator_class`

#### `Generator_class`

May be used to specify a `SchemaGenerator` subclass to be passed to the
`SchemaView`.

Может использоваться для указания подкласса «схемагенератор»
`Schemaview`.

#### `authentication_classes`

#### `outentication_classes`

May be used to specify the list of authentication classes that will apply to the schema endpoint.
Defaults to `settings.DEFAULT_AUTHENTICATION_CLASSES`

Может использоваться для указания списка классов аутентификации, которые будут применяться к конечной точке схемы.
По умолчанию `sutres.default_authentication_classes`

#### `permission_classes`

#### `rescision_classes`

May be used to specify the list of permission classes that will apply to the schema endpoint.
Defaults to `settings.DEFAULT_PERMISSION_CLASSES`

Может использоваться для указания списка классов разрешений, которые будут применяться к конечной точке схемы.
По умолчанию `sutres.default_permission_classes`

## Using an explicit schema view

## Использование явного представления схемы

If you need a little more control than the `get_schema_view()` shortcut gives you,
then you can use the `SchemaGenerator` class directly to auto-generate the
`Document` instance, and to return that from a view.

Если вам нужно немного больше управления, чем `get_schema_view ()`
Затем вы можете использовать класс «схемагенератор» непосредственно для автоматического генерации
`Экземпляр документа и вернуть его из представления.

This option gives you the flexibility of setting up the schema endpoint
with whatever behaviour you want. For example, you can apply different
permission, throttling, or authentication policies to the schema endpoint.

Эта опция дает вам гибкость настройки конечной точки схемы
с любым поведением, которое вы хотите.
Например, вы можете применить разные
Политика разрешения, дросселирование или аутентификация в конечную точку схемы.

Here's an example of using `SchemaGenerator` together with a view to
return the schema.

Вот пример использования `schemagerator 'вместе с видом на
вернуть схему.

**views.py:**

** views.py: **

```
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import renderers, response, schemas

generator = schemas.SchemaGenerator(title='Bookings API')

@api_view()
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    schema = generator.get_schema(request)
    return response.Response(schema)
```


**urls.py:**

** urls.py: **

```
urlpatterns = [
    path('', schema_view),
    ...
]
```


You can also serve different schemas to different users, depending on the
permissions they have available. This approach can be used to ensure that
unauthenticated requests are presented with a different schema to
authenticated requests, or to ensure that different parts of the API are
made visible to different users depending on their role.

Вы также можете обслуживать разные схемы для разных пользователей, в зависимости от
разрешения у них есть.
Этот подход может быть использован для обеспечения того, чтобы
Несанкционированные запросы представлены с другой схемой для
аутентифицированные запросы или для обеспечения того, чтобы различные части API были
Сделано видимым для разных пользователей в зависимости от их роли.

In order to present a schema with endpoints filtered by user permissions,
you need to pass the `request` argument to the `get_schema()` method, like so:

Чтобы представить схему с конечными точками, отфильтрованными разрешениями пользователей,
Вам нужно передать аргумент `request` на метод` get_schema () `, например, так:

```
@api_view()
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bookings API')
    return response.Response(generator.get_schema(request=request))
```


## Explicit schema definition

## Определение явного схемы

An alternative to the auto-generated approach is to specify the API schema
explicitly, by declaring a `Document` object in your codebase. Doing so is a
little more work, but ensures that you have full control over the schema
representation.

Альтернативой подходу к автоматическому генерации является указание схемы API
Явно, объявив объект «документ» в вашей кодовой базе.
Это
Немного больше работы, но гарантирует, что вы имеете полный контроль над схемой
представление.

```
import coreapi
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import renderers, response

schema = coreapi.Document(
    title='Bookings API',
    content={
        ...
    }
)

@api_view()
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    return response.Response(schema)
```


---

# Schemas as documentation

# Схемы как документация

One common usage of API schemas is to use them to build documentation pages.

Одним из распространенных схем API является использование их для создания страниц документации.

The schema generation in REST framework uses docstrings to automatically
populate descriptions in the schema document.

Генерация схемы в рамках REST использует DocStrings для автоматического
Заполняют описания в документе схемы.

These descriptions will be based on:

Эти описания будут основаны на:

* The corresponding method docstring if one exists.
* A named section within the class docstring, which can be either single line or multi-line.
* The class docstring.

* Соответствующий метод, если он существует.
* Именованный раздел в классе Docstring, который может быть либо одной линией, либо многострочной.
* Класс Docstring.

## Examples

## Примеры

An `APIView`, with an explicit method docstring.

`Apiview` с явным методом Docstring.

```
class ListUsernames(APIView):
    def get(self, request):
        """
        Return a list of all user names in the system.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```


A `ViewSet`, with an explicit action docstring.

`Viewset ', с явным действием Docstring.

```
class ListUsernames(ViewSet):
    def list(self, request):
        """
        Return a list of all user names in the system.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```


A generic view with sections in the class docstring, using single-line style.

Общий вид с разделами в классе Docstring, используя однострочный стиль.

```
class UserList(generics.ListCreateAPIView):
    """
    get: List all the users.
    post: Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
```


A generic viewset with sections in the class docstring, using multi-line style.

Общий обзор с разделами в классе Docstring, используя многострочный стиль.

```
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    retrieve:
    Return a user instance.

    list:
    Return all users, ordered by most recently joined.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
```


---

# API Reference

# Ссылка на API

## SchemaGenerator

## схемагенератор

A class that walks a list of routed URL patterns, requests the schema for each view,
and collates the resulting CoreAPI Document.

Класс, который проходит список направленных шаблонов URL -адреса, запрашивает схему для каждого представления,
и сопоставляет результирующий документ Coreapi.

Typically you'll instantiate `SchemaGenerator` with a single argument, like so:

Как правило, вы создаете экземпляр «Schemagerator» одним аргументом, как так:

```
generator = SchemaGenerator(title='Stock Prices API')
```


Arguments:

Аргументы:

* `title` **required** - The name of the API.
* `url` - The root URL of the API schema. This option is not required unless the schema is included under path prefix.
* `patterns` - A list of URLs to inspect when generating the schema. Defaults to the project's URL conf.
* `urlconf` - A URL conf module name to use when generating the schema. Defaults to `settings.ROOT_URLCONF`.

*`title` ** обязательно ** - Имя API.
* `url` - корневой URL схемы API.
Эта опция не требуется, если схема не включена в префикс пути.
* `patterns` - список URL -адресов для проверки при генерации схемы.
По умолчанию в URL Conf.
* `urlConf` - Имя модуля CONF URL для использования при генерации схемы.
По умолчанию на settings.root_urlconf`.

### get_schema(self, request)

### get_schema (Self, запрос)

Returns a `coreapi.Document` instance that represents the API schema.

Возвращает экземпляр `coreapi.document`, который представляет схему API.

```
@api_view
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bookings API')
    return Response(generator.get_schema())
```


The `request` argument is optional, and may be used if you want to apply per-user
permissions to the resulting schema generation.

Аргумент `request` является необязательным и может использоваться, если вы хотите применить пользователя
Разрешения к получению генерации схемы.

### get_links(self, request)

### get_links (Self, запрос)

Return a nested dictionary containing all the links that should be included in the API schema.

Верните вложенный словарь, содержащий все ссылки, которые должны быть включены в схему API.

This is a good point to override if you want to modify the resulting structure of the generated schema,
as you can build a new dictionary with a different layout.

Это хороший момент для переопределения, если вы хотите изменить полученную структуру сгенерированной схемы,
Как вы можете построить новый словарь с другой планировкой.

## AutoSchema

## Autoschema

A class that deals with introspection of individual views for schema generation.

Класс, который касается самоанализации отдельных взглядов для генерации схемы.

`AutoSchema` is attached to `APIView` via the `schema` attribute.

`Autoschema` прикреплен к` apiview` через атрибут `schema.

The `AutoSchema` constructor takes a single keyword argument  `manual_fields`.

Конструктор `autoschema` принимает один аргумент ключевого слова` manual_fields`.

**`manual_fields`**: a `list` of `coreapi.Field` instances that will be added to
the generated fields. Generated fields with a matching `name` will be overwritten.

** `manual_fields` **: a` list` из экземпляров `coreapi.field`, которые будут добавлены в
сгенерированные поля.
Сгенерированные поля с соответствующим `именем будут перезаписаны.

```
class CustomView(APIView):
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "my_extra_field",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
    ])
```


For more advanced customisation subclass `AutoSchema` to customise schema generation.

Для более продвинутой настройки подкласса `autoschema` для настройки генерации схемы.

```
class CustomViewSchema(AutoSchema):
    """
    Overrides `get_link()` to provide Custom Behavior X
    """

    def get_link(self, path, method, base_url):
        link = super().get_link(path, method, base_url)
        # Do something to customize link here...
        return link

class MyView(APIView):
  schema = CustomViewSchema()
```


The following methods are available to override.

Следующие методы доступны для переопределения.

### get_link(self, path, method, base_url)

### get_link (self, path, method, base_url)

Returns a `coreapi.Link` instance corresponding to the given view.

Возвращает экземпляр `coreapi.link`, соответствующий данному представлению.

This is the main entry point.
You can override this if you need to provide custom behaviors for particular views.

Это основная точка входа.
Вы можете переопределить это, если вам нужно предоставить пользовательское поведение для определенных представлений.

### get_description(self, path, method)

### get_description (self, path, method)

Returns a string to use as the link description. By default this is based on the
view docstring as described in the "Schemas as Documentation" section above.

Возвращает строку для использования в качестве описания ссылки.
По умолчанию это основано на
Посмотреть Docstring, как описано в разделе «Схемы как документация» выше.

### get_encoding(self, path, method)

### get_encoding (self, path, method)

Returns a string to indicate the encoding for any request body, when interacting
with the given view. Eg. `'application/json'`. May return a blank string for views
that do not expect a request body.

Возвращает строку, чтобы указать кодирование для любого корпуса запроса при взаимодействии
с данным представлением.
Например.
`'Приложение/json''.
Может вернуть пустую строку для просмотров
Это не ожидает запрашивающего органа.

### get_path_fields(self, path, method):

### get_path_fields (self, path, method):

Return a list of `coreapi.Field()` instances. One for each path parameter in the URL.

Верните список экземпляров `coreapi.field ()`.
Один для каждого параметра пути в URL.

### get_serializer_fields(self, path, method)

### get_serializer_fields (self, path, method)

Return a list of `coreapi.Field()` instances. One for each field in the serializer class used by the view.

Верните список экземпляров `coreapi.field ()`.
Один для каждого поля в классе сериализатора, используемого видом.

### get_pagination_fields(self, path, method)

### get_pagination_fields (self, path, method)

Return a list of `coreapi.Field()` instances, as returned by the `get_schema_fields()` method on any pagination class used by the view.

Верните список экземпляров `coreapi.field ()`, как возвращается методом `get_schema_fields ()` на любом классе страниц, используемом представлением.

### get_filter_fields(self, path, method)

### get_filter_fields (self, path, method)

Return a list of `coreapi.Field()` instances, as returned by the `get_schema_fields()` method of any filter classes used by the view.

Верните список экземпляров `coreapi.field ()`, как возвращается методом `get_schema_fields ()` любых классов фильтров, используемых представлением.

### get_manual_fields(self, path, method)

### get_manual_fields (self, path, method)

Return a list of `coreapi.Field()` instances to be added to or replace generated fields. Defaults to (optional) `manual_fields` passed to `AutoSchema` constructor.

Верните список экземпляров `coreapi.field ()`, которые должны быть добавлены в сгенерированные поля или заменить.
По умолчанию (необязательно) `manual_fields` передал конструктору Autoschema`.

May be overridden to customise manual fields by `path` or `method`. For example, a per-method adjustment may look like this:

Может быть отменен на настройку ручных полей с помощью `path` или` method '.
Например, регулировка на метод может выглядеть так:

```python
def get_manual_fields(self, path, method):
    """Example adding per-method fields."""

    extra_fields = []
    if method=='GET':
        extra_fields = # ... list of extra fields for GET ...
    if method=='POST':
        extra_fields = # ... list of extra fields for POST ...

    manual_fields = super().get_manual_fields(path, method)
    return manual_fields + extra_fields
```


### update_fields(fields, update_with)

### update_fields (fields, update_with)

Utility `staticmethod`. Encapsulates logic to add or replace fields from a list
by `Field.name`. May be overridden to adjust replacement criteria.

Утилита `staticmethod`.
Инкапсулирует логику для добавления или замены полей из списка
по `field.name`.
Может быть отменен, чтобы настроить критерии замены.

## ManualSchema

## Руководство

Allows manually providing a list of `coreapi.Field` instances for the schema,
plus an optional description.

Позволяет вручную предоставлять список экземпляров `coreapi.field` для схемы,
плюс дополнительное описание.

```
class MyView(APIView):
  schema = ManualSchema(fields=[
        coreapi.Field(
            "first_field",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "second_field",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
    ]
  )
```


The `ManualSchema` constructor takes two arguments:

Конструктор `Руководящий ручный конструктор принимает два аргумента:

**`fields`**: A list of `coreapi.Field` instances. Required.

** `fields` **: список экземпляров` coreapi.field`.
Необходимый.

**`description`**: A string description. Optional.

** `description` **: описание строки.
По желанию.

**`encoding`**: Default `None`. A string encoding, e.g `application/json`. Optional.

** `кодирование <**: по умолчанию` none `.
Строка кодирования, например, приложение/json`.
По желанию.

---

## Core API

## Core API

This documentation gives a brief overview of the components within the `coreapi`
package that are used to represent an API schema.

Эта документация дает краткий обзор компонентов в «Coreapi»
пакет, который используется для представления схемы API.

Note that these classes are imported from the `coreapi` package, rather than
from the `rest_framework` package.

Обратите внимание, что эти классы импортируются из пакета Coreapi, а не
из пакета `rest_framework`.

### Document

### документ

Represents a container for the API schema.

Представляет контейнер для схемы API.

#### `title`

#### `title`

A name for the API.

Имя для API.

#### `url`

#### `url`

A canonical URL for the API.

Канонический URL для API.

#### `content`

#### `content`

A dictionary, containing the `Link` objects that the schema contains.

Словарь, содержащий объекты `link`, которые содержит схема.

In order to provide more structure to the schema, the `content` dictionary
may be nested, typically to a second level. For example:

Чтобы обеспечить большую структуру для схемы, словарь «контент»
может быть вложенным, обычно на второй уровень.
Например:

```
content={
    "bookings": {
        "list": Link(...),
        "create": Link(...),
        ...
    },
    "venues": {
        "list": Link(...),
        ...
    },
    ...
}
```


### Link

### Ссылка на сайт

Represents an individual API endpoint.

Представляет отдельную конечную точку API.

#### `url`

#### `url`

The URL of the endpoint. May be a URI template, such as `/users/{username}/`.

URL -адрес конечной точки.
Может быть шаблон URI, такой как `/users/{username}/`.

#### `action`

#### `action`

The HTTP method associated with the endpoint. Note that URLs that support
more than one HTTP method, should correspond to a single `Link` for each.

Метод HTTP, связанный с конечной точкой.
Обратите внимание, что URL -адреса, которые поддерживают
Более одного метода HTTP должно соответствовать одному `ссылке 'для каждого.

#### `fields`

#### `Fields`

A list of `Field` instances, describing the available parameters on the input.

Список экземпляров «полевых», описывающих доступные параметры на входе.

#### `description`

#### `description`

A short description of the meaning and intended usage of the endpoint.

Краткое описание значения и предполагаемого использования конечной точки.

### Field

### Поле

Represents a single input parameter on a given API endpoint.

Представляет один входной параметр в данной конечной точке API.

#### `name`

#### `name`

A descriptive name for the input.

Описательное имя для ввода.

#### `required`

#### `Обязательный

A boolean, indicated if the client is required to included a value, or if
the parameter can be omitted.

Логический, указанный, если клиент должен включать значение или если
параметр может быть опущен.

#### `location`

#### `location`

Determines how the information is encoded into the request. Should be one of
the following strings:

Определяет, как информация кодируется в запросе.
Должен быть один из
Следующие строки:

**"path"**

**"дорожка"**

Included in a templated URI. For example a `url` value of `/products/{product_code}/` could be used together with a `"path"` field, to handle API inputs in a URL path such as `/products/slim-fit-jeans/`.

Включено в шаблон URI.
Например, значение `url``/products/{product_code}/`может быть использовано вместе с полем` "" "` `для обработки входов API в пути URL, такого как`/products/slim-jeans/
`.

These fields will normally correspond with [named arguments in the project URL conf](https://docs.djangoproject.com/en/stable/topics/http/urls/#named-groups).

Эти поля обычно соответствуют [названным аргументам в проекте URL Conf] (https://docs.djangoproject.com/en/stable/topics/http/urls/#named-groups).

**"query"**

**"запрос"**

Included as a URL query parameter. For example `?search=sale`. Typically for `GET` requests.

Включено в качестве параметра запроса URL.
Например, `? SEARK = SALE`.
Обычно для запросов `get '.

These fields will normally correspond with pagination and filtering controls on a view.

Эти поля обычно соответствуют элементам управления на странице и фильтрации.

**"form"**

**"форма"**

Included in the request body, as a single item of a JSON object or HTML form. For example `{"colour": "blue", ...}`. Typically for `POST`, `PUT` and `PATCH` requests. Multiple `"form"` fields may be included on a single link.

Включено в тело запроса, как единый элемент объекта JSON или HTML -формы.
Например, `{" Color ":" Blue ", ...}`.
Обычно для `post`,` put 'и `patch' запросы.
Несколько полей «Форма» могут быть включены по одной ссылке.

These fields will normally correspond with serializer fields on a view.

Эти поля обычно соответствуют полям сериализатора на представлении.

**"body"**

**"тело"**

Included as the complete request body. Typically for `POST`, `PUT` and `PATCH` requests. No more than one `"body"` field may exist on a link. May not be used together with `"form"` fields.

Включено в качестве полного органа запроса.
Обычно для `post`,` put 'и `patch' запросы.
Не более одного «тела» поля может существовать на ссылке.
Не может использоваться вместе с `« формой »поля.

These fields will normally correspond with views that use `ListSerializer` to validate the request input, or with file upload views.

Эти поля обычно соответствуют представлениям, которые используют `listSerializer` для проверки ввода запроса или с представлениями загрузки файлов.

#### `encoding`

#### `Кодирование

**"application/json"**

** "Приложение/json" **

JSON encoded request content. Corresponds to views using `JSONParser`.
Valid only if either one or more `location="form"` fields, or a single
`location="body"` field is included on the `Link`.

JSON, закодированный запрос, содержание запроса.
Соответствует представлениям с использованием `jsonParser`.
Действительно только если одно или несколько `location =" form "` fields или один
`location =" body "` Поле включено в `link '.

**"multipart/form-data"**

** "Multipart/Form-Data" **

Multipart encoded request content. Corresponds to views using `MultiPartParser`.
Valid only if one or more `location="form"` fields is included on the `Link`.

Кодированный содержимый многопорт содержимого.
Соответствует представлениям с использованием `multiplarperser.
Действительно только если одно или несколько `location =" form "` `Поля включены в` link '.

**"application/x-www-form-urlencoded"**

** "Приложение/X-WWW-Form-Urlencoded" **

URL encoded request content. Corresponds to views using `FormParser`. Valid
only if one or more `location="form"` fields is included on the `Link`.

URL -кодированный запрос содержимое.
Соответствует представлениям с использованием `FormParser '.
Действительный
Только если одно или несколько `location =" form "` fields включено в `link '.

**"application/octet-stream"**

** "Приложение/октет-поток" **

Binary upload request content. Corresponds to views using `FileUploadParser`.
Valid only if a `location="body"` field is included on the `Link`.

Содержание запроса на загрузку бинарной загрузки.
Соответствует представлениям с использованием `fileuploadParser`.
Действительно только в том случае, если поля `location =" body "включено в` link '.

#### `description`

#### `description`

A short description of the meaning and intended usage of the input field.

Краткое описание значения и предполагаемого использования поля ввода.

---

# Third party packages

# Сторонние пакеты

## drf-yasg - Yet Another Swagger Generator

## drf -yasg - еще один генератор Swagger

[drf-yasg](https://github.com/axnsan12/drf-yasg/) generates [OpenAPI](https://openapis.org/) documents suitable for code generation - nested schemas,
named models, response bodies, enum/pattern/min/max validators, form parameters, etc.

[drf-yasg] (https://github.com/axnsan12/drf-yasg/) генерирует [openapi] (https://openapis.org/) Документы, подходящие для генерации кода-вложенные схемы,
Названные модели, тела отклика, enum/pattern/min/max valdators, параметры формы и т. Д.

## drf-spectacular - Sane and flexible OpenAPI 3.0 schema generation for Django REST framework

## DRF -Spectacular - SANE и Гибкая генерация схемы OpenAPI 3.0 для Django Rest Framework

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) is a [OpenAPI 3](https://openapis.org/) schema generation tool with explicit focus on extensibility,
customizability and client generation. It's usage patterns are very similar to [drf-yasg](https://github.com/axnsan12/drf-yasg/).

[DRF-Spectacular] (https://github.com/tfranzel/drf-spectacular/)-это инструмент [openapi 3] (https://openapis.org/) схемы с явным фокусом на расширенности,
настраиваемость и генерация клиентов.
Это модели использования очень похожи на [DRF-YASG] (https://github.com/axnsan12/drf-yasg/).
