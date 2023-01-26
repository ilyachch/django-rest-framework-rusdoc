<!-- TRANSLATED by md-translate -->
---

source:

источник:

* schemas.py

* schemas.py

---

# Schemas

# Схемы

---

**DEPRECATION NOTICE:** Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10. See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

**УВЕДОМЛЕНИЕ О ДЕПРЕССИИ:** Использование схем на базе CoreAPI было отменено с введением генерации схем на базе OpenAPI в Django REST Framework v3.10. Более подробную информацию смотрите в [Version 3.10 Release Announcement](../community/3.10-announcement.md).

You are probably looking for [this page](../api-guide/schemas.md) if you want latest information regarding schemas.

Вы, вероятно, ищете [эту страницу](../api-guide/schemas.md), если вам нужна последняя информация о схемах.

---

> A machine-readable [schema] describes what resources are available via the API, what their URLs are, how they are represented and what operations they support.
>
> — Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

> Машиночитаемая [схема] описывает, какие ресурсы доступны через API, каковы их URL, как они представлены и какие операции они поддерживают.
>
> - Heroku, [JSON Schema for the Heroku Platform API](https://blog.heroku.com/archives/2014/1/8/json_schema_for_heroku_platform_api)

API schemas are a useful tool that allow for a range of use cases, including generating reference documentation, or driving dynamic client libraries that can interact with your API.

Схемы API - это полезный инструмент, который позволяет использовать их в различных случаях, включая создание справочной документации или создание динамических клиентских библиотек, которые могут взаимодействовать с вашим API.

## Install Core API & PyYAML

## Установите Core API и PyYAML

You'll need to install the `coreapi` package in order to add schema support for REST framework. You probably also want to install `pyyaml`, so that you can render the schema into the commonly used YAML-based OpenAPI format.

Вам необходимо установить пакет `coreapi`, чтобы добавить поддержку схем для REST framework. Возможно, вы также захотите установить `pyyaml`, чтобы можно было преобразовать схему в широко используемый формат OpenAPI на основе YAML.

```
pip install coreapi pyyaml
```

## Quickstart

## Быстрый старт

There are two different ways you can serve a schema description for your API.

Существует два различных способа предоставления описания схемы для вашего API.

### Generating a schema with the `generateschema` management command

### Генерация схемы с помощью команды управления `generateschema`.

To generate a static API schema, use the `generateschema` management command.

Чтобы создать статическую схему API, используйте команду управления `generateschema`.

```shell
$ python manage.py generateschema > schema.yml
```

Once you've generated a schema in this way you can annotate it with any additional information that cannot be automatically inferred by the schema generator.

После создания схемы таким образом вы можете аннотировать ее любой дополнительной информацией, которая не может быть автоматически выведена генератором схемы.

You might want to check your API schema into version control and update it with each new release, or serve the API schema from your site's static media.

Вы можете зарегистрировать схему API в системе контроля версий и обновлять ее с каждым новым релизом, или использовать схему API из статического медиа вашего сайта.

### Adding a view with `get_schema_view`

### Добавление представления с помощью `get_schema_view`

To add a dynamically generated schema view to your API, use `get_schema_view`.

Чтобы добавить динамически сгенерированное представление схемы в ваш API, используйте `get_schema_view`.

```python
from rest_framework.schemas import get_schema_view
from django.urls import path

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path('schema', schema_view),
    ...
]
```

See below [for more details](#the-get_schema_view-shortcut) on customizing a dynamically generated schema view.

Смотрите ниже [для более подробной информации](#the-get_schema_view-shortcut) о настройке динамически генерируемого представления схемы.

## Internal schema representation

## Внутреннее представление схемы

REST framework uses [Core API](https://www.coreapi.org/) in order to model schema information in a format-independent representation. This information can then be rendered into various different schema formats, or used to generate API documentation.

REST-фреймворк использует [Core API](https://www.coreapi.org/) для моделирования информации схемы в независимом от формата представлении. Затем эта информация может быть преобразована в различные форматы схем или использована для создания документации API.

When using Core API, a schema is represented as a `Document` which is the top-level container object for information about the API. Available API interactions are represented using `Link` objects. Each link includes a URL, HTTP method, and may include a list of `Field` instances, which describe any parameters that may be accepted by the API endpoint. The `Link` and `Field` instances may also include descriptions, that allow an API schema to be rendered into user documentation.

При использовании Core API схема представляется в виде `Document`, который является объектом-контейнером верхнего уровня для информации об API. Доступные взаимодействия API представлены с помощью объектов `Link`. Каждая ссылка включает URL, метод HTTP и может включать список экземпляров `Field`, которые описывают любые параметры, которые могут быть приняты конечной точкой API. Экземпляры `Link` и `Field` могут также включать описания, которые позволяют представить схему API в виде пользовательской документации.

Here's an example of an API description that includes a single `search` endpoint:

Вот пример описания API, включающего единственную конечную точку `search`:

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

In order to be presented in an HTTP response, the internal representation has to be rendered into the actual bytes that are used in the response.

Чтобы быть представленным в HTTP-ответе, внутреннее представление должно быть преобразовано в фактические байты, которые используются в ответе.

REST framework includes a few different renderers that you can use for encoding the API schema.

REST framework включает несколько различных рендерингов, которые можно использовать для кодирования схемы API.

* `renderers.OpenAPIRenderer` - Renders into YAML-based [OpenAPI](https://openapis.org/), the most widely used API schema format.
* `renderers.JSONOpenAPIRenderer` - Renders into JSON-based [OpenAPI](https://openapis.org/).
* `renderers.CoreJSONRenderer` - Renders into [Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding), a format designed for use with the `coreapi` client library.

* `renderers.OpenAPIRenderer` - Рендеринг в YAML-формат [OpenAPI](https://openapis.org/), наиболее широко используемый формат схемы API.
* `renderers.JSONOpenAPIRenderer` - Рендеринг в JSON-формат [OpenAPI](https://openapis.org/).
* `renderers.CoreJSONRenderer` - Рендеринг в [Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding), формат, разработанный для использования с клиентской библиотекой `coreapi`.

[Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding) is designed as a canonical format for use with Core API. REST framework includes a renderer class for handling this media type, which is available as `renderers.CoreJSONRenderer`.

[Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding) разработан как канонический формат для использования с Core API. REST framework включает класс рендерера для работы с этим типом медиа, который доступен как `renderers.CoreJSONRenderer`.

## Schemas vs Hypermedia

## Схемы против гипермедиа

It's worth pointing out here that Core API can also be used to model hypermedia responses, which present an alternative interaction style to API schemas.

Здесь стоит отметить, что Core API также можно использовать для моделирования гипермедийных ответов, которые представляют собой альтернативный стиль взаимодействия со схемами API.

With an API schema, the entire available interface is presented up-front as a single endpoint. Responses to individual API endpoints are then typically presented as plain data, without any further interactions contained in each response.

С помощью схемы API весь доступный интерфейс представляется заранее в виде одной конечной точки. Ответы на отдельные конечные точки API обычно представляются как обычные данные, без каких-либо дополнительных взаимодействий, содержащихся в каждом ответе.

With Hypermedia, the client is instead presented with a document containing both data and available interactions. Each interaction results in a new document, detailing both the current state and the available interactions.

При использовании гипермедиа клиент вместо этого получает документ, содержащий как данные, так и доступные взаимодействия. Каждое взаимодействие приводит к созданию нового документа, в котором подробно описывается как текущее состояние, так и доступные взаимодействия.

Further information and support on building Hypermedia APIs with REST framework is planned for a future version.

Дополнительная информация и поддержка по созданию гипермедийных API с помощью REST-фреймворка запланирована на будущую версию.

---

# Creating a schema

# Создание схемы

REST framework includes functionality for auto-generating a schema, or allows you to specify one explicitly.

REST-фреймворк включает функциональность для автоматической генерации схемы или позволяет указать ее в явном виде.

## Manual Schema Specification

## Ручная спецификация схемы

To manually specify a schema you create a Core API `Document`, similar to the example above.

Чтобы вручную указать схему, вы создаете Core API `Document`, подобно приведенному выше примеру.

```
schema = coreapi.Document(
    title='Flight Search API',
    content={
        ...
    }
)
```

## Automatic Schema Generation

## Автоматическая генерация схемы

Automatic schema generation is provided by the `SchemaGenerator` class.

Автоматическая генерация схемы обеспечивается классом `SchemaGenerator`.

`SchemaGenerator` processes a list of routed URL patterns and compiles the appropriately structured Core API Document.

`SchemaGenerator` обрабатывает список шаблонов маршрутизируемых URL и составляет соответствующим образом структурированный документ Core API.

Basic usage is just to provide the title for your schema and call `get_schema()`:

Базовое использование - это просто указать название вашей схемы и вызвать `get_schema()`:

```
generator = schemas.SchemaGenerator(title='Flight Search API')
schema = generator.get_schema()
```

## Per-View Schema Customisation

## Настройка схемы для каждого представления

By default, view introspection is performed by an `AutoSchema` instance accessible via the `schema` attribute on `APIView`. This provides the appropriate Core API `Link` object for the view, request method and path:

По умолчанию интроспекция представления выполняется экземпляром `AutoSchema`, доступным через атрибут `schema` на `APIView`. Он предоставляет соответствующий объект Core API `Link` для представления, метода запроса и пути:

```
auto_schema = view.schema
coreapi_link = auto_schema.get_link(...)
```

(In compiling the schema, `SchemaGenerator` calls `view.schema.get_link()` for each view, allowed method and path.)

(При компиляции схемы `SchemaGenerator` вызывает `view.schema.get_link()` для каждого представления, разрешенного метода и пути).

---

**Note**: For basic `APIView` subclasses, default introspection is essentially limited to the URL kwarg path parameters. For `GenericAPIView` subclasses, which includes all the provided class based views, `AutoSchema` will attempt to introspect serializer, pagination and filter fields, as well as provide richer path field descriptions. (The key hooks here are the relevant `GenericAPIView` attributes and methods: `get_serializer`, `pagination_class`, `filter_backends` and so on.)

**Примечание**: Для базовых подклассов `APIView` интроспекция по умолчанию ограничивается параметрами пути URL kwarg. Для подклассов `GenericAPIView`, которые включают все представления, основанные на классах, `AutoSchema` попытается проанализировать поля сериализатора, пагинации и фильтра, а также предоставить более богатые описания полей пути. (Ключевыми крючками здесь являются соответствующие атрибуты и методы `GenericAPIView`: `get_serializer`, `pagination_class`, `filter_backends` и так далее).

---

To customise the `Link` generation you may:

Чтобы настроить генерацию `Ссылки`, вы можете:

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
    ```This allows extension for the most common case without subclassing.
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
    ```This provides complete control over view introspection.
* Instantiate `ManualSchema` on your view, providing the Core API `Fields` for the view explicitly:
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
    ```This allows manually specifying the schema for some views whilst maintaining automatic generation elsewhere.

* Инстанцируйте `AutoSchema` на вашем представлении с помощью кванга `manual_fields`:
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
``Это позволяет расширить наиболее распространенный случай без подкласса.
* Предоставить подкласс ``AutoSchema`` с более сложной настройкой:
```
from rest_framework.views import APIView
from rest_framework.schemas import AutoSchema
class CustomSchema(AutoSchema):
def get_link(...):
# Реализуйте пользовательскую интроспекцию здесь (или в других подметодах)
class CustomView(APIView):
...
schema = CustomSchema()
``Это обеспечивает полный контроль над интроспекцией представления.
* Инстанцируйте `ManualSchema` на вашем представлении, явно предоставляя Core API `Fields` для представления:
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
``Это позволяет вручную указывать схему для некоторых представлений, сохраняя автоматическую генерацию в других местах.

You may disable schema generation for a view by setting `schema` to `None`:

Вы можете отключить генерацию схемы для представления, установив значение `schema` в `None`:

```
class CustomView(APIView):
        ...
        schema = None  # Will not appear in schema
```

This also applies to extra actions for `ViewSet`s:

Это также относится к дополнительным действиям для `ViewSet`:

```
class CustomViewSet(viewsets.ModelViewSet):

        @action(detail=True, schema=None)
        def extra_action(self, request, pk=None):
            ...
```

---

**Note**: For full details on `SchemaGenerator` plus the `AutoSchema` and `ManualSchema` descriptors see the [API Reference below](#api-reference).

**Примечание**: Полную информацию о `SchemaGenerator` и дескрипторах `AutoSchema` и `ManualSchema` смотрите в [API Reference below](#api-reference).

---

# Adding a schema view

# Добавление представления схемы

There are a few different ways to add a schema view to your API, depending on exactly what you need.

Существует несколько различных способов добавить представление схемы в ваш API, в зависимости от того, что именно вам нужно.

## The get_schema_view shortcut

## Ярлык get_schema_view

The simplest way to include a schema in your project is to use the `get_schema_view()` function.

Самый простой способ включить схему в ваш проект - использовать функцию `get_schema_view()`.

```
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="Server Monitoring API")

urlpatterns = [
    path('', schema_view),
    ...
]
```

Once the view has been added, you'll be able to make API requests to retrieve the auto-generated schema definition.

После добавления представления вы сможете делать API-запросы для получения автоматически сгенерированного определения схемы.

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

Аргументами для `get_schema_view()` являются:

#### `title`

#### `title`.

May be used to provide a descriptive title for the schema definition.

Может использоваться для предоставления описательного заголовка для определения схемы.

#### `url`

#### `url`.

May be used to pass a canonical URL for the schema.

Может использоваться для передачи канонического URL для схемы.

```
schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/'
)
```

#### `urlconf`

#### `urlconf`.

A string representing the import path to the URL conf that you want to generate an API schema for. This defaults to the value of Django's ROOT_URLCONF setting.

Строка, представляющая путь импорта к URL conf, для которого вы хотите сгенерировать схему API. По умолчанию это значение соответствует значению параметра ROOT_URLCONF в Django.

```
schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/',
    urlconf='myproject.urls'
)
```

#### `renderer_classes`

#### `renderer_classes`.

May be used to pass the set of renderer classes that can be used to render the API root endpoint.

Может использоваться для передачи набора классов рендеринга, которые могут быть использованы для рендеринга корневой конечной точки API.

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

#### `паттерны`.

List of url patterns to limit the schema introspection to. If you only want the `myproject.api` urls to be exposed in the schema:

Список шаблонов url для ограничения интроспекции схемы. Если вы хотите, чтобы в схеме отображались только урлы `myproject.api`:

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

#### `generator_class`.

May be used to specify a `SchemaGenerator` subclass to be passed to the `SchemaView`.

Может использоваться для указания подкласса `SchemaGenerator`, который будет передан в `SchemaView`.

#### `authentication_classes`

#### `authentication_classes`.

May be used to specify the list of authentication classes that will apply to the schema endpoint. Defaults to `settings.DEFAULT_AUTHENTICATION_CLASSES`

Может использоваться для указания списка классов аутентификации, которые будут применяться к конечной точке схемы. По умолчанию `settings.DEFAULT_AUTHENTICATION_CLASSES`.

#### `permission_classes`

#### `permission_classes`.

May be used to specify the list of permission classes that will apply to the schema endpoint. Defaults to `settings.DEFAULT_PERMISSION_CLASSES`

Может использоваться для указания списка классов разрешений, которые будут применяться к конечной точке схемы. По умолчанию `settings.DEFAULT_PERMISSION_CLASSES`.

## Using an explicit schema view

## Использование явного представления схемы

If you need a little more control than the `get_schema_view()` shortcut gives you, then you can use the `SchemaGenerator` class directly to auto-generate the `Document` instance, and to return that from a view.

Если вам нужно немного больше контроля, чем дает ярлык `get_schema_view()`, то вы можете использовать класс `SchemaGenerator` напрямую для автоматической генерации экземпляра `Document` и возврата его из представления.

This option gives you the flexibility of setting up the schema endpoint with whatever behaviour you want. For example, you can apply different permission, throttling, or authentication policies to the schema endpoint.

Эта опция дает вам гибкость в настройке конечной точки схемы с любым поведением, которое вы хотите. Например, вы можете применить к конечной точке схемы различные политики разрешений, дросселирования или аутентификации.

Here's an example of using `SchemaGenerator` together with a view to return the schema.

Вот пример использования `SchemaGenerator` вместе с представлением для возврата схемы.

**views.py:**

**views.py:**

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

**urls.py:**

```
urlpatterns = [
    path('', schema_view),
    ...
]
```

You can also serve different schemas to different users, depending on the permissions they have available. This approach can be used to ensure that unauthenticated requests are presented with a different schema to authenticated requests, or to ensure that different parts of the API are made visible to different users depending on their role.

Вы также можете обслуживать разные схемы для разных пользователей в зависимости от имеющихся у них разрешений. Этот подход можно использовать для того, чтобы неаутентифицированные запросы получали схему, отличную от схемы аутентифицированных запросов, или для того, чтобы разные части API были видны разным пользователям в зависимости от их роли.

In order to present a schema with endpoints filtered by user permissions, you need to pass the `request` argument to the `get_schema()` method, like so:

Чтобы представить схему с конечными точками, отфильтрованными по разрешениям пользователей, вам нужно передать аргумент `request` методу `get_schema()`, как показано ниже:

```
@api_view()
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bookings API')
    return response.Response(generator.get_schema(request=request))
```

## Explicit schema definition

## Явное определение схемы

An alternative to the auto-generated approach is to specify the API schema explicitly, by declaring a `Document` object in your codebase. Doing so is a little more work, but ensures that you have full control over the schema representation.

Альтернативой автогенерируемому подходу является явное указание схемы API путем объявления объекта `Document` в вашей кодовой базе. Это немного больше работы, но гарантирует, что у вас есть полный контроль над представлением схемы.

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

Одно из распространенных применений схем API - это использование их для создания страниц документации.

The schema generation in REST framework uses docstrings to automatically populate descriptions in the schema document.

Генерация схемы в REST framework использует docstrings для автоматического заполнения описаний в документе схемы.

These descriptions will be based on:

Эти описания будут основаны на:

* The corresponding method docstring if one exists.
* A named section within the class docstring, which can be either single line or multi-line.
* The class docstring.

* Соответствующая док-строка метода, если она существует.
* Именованный раздел в docstring класса, который может быть как однострочным, так и многострочным.
* Документальная строка класса.

## Examples

## Примеры

An `APIView`, with an explicit method docstring.

Вид `APIView`, с явным докстроком метода.

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

Набор `ViewSet`, с явным документом действия.

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

Общий вид с разделами в классе docstring, с использованием однострочного стиля.

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

Общий набор представлений с разделами в классе docstring, использующий многострочный стиль.

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

# API Reference

## SchemaGenerator

## SchemaGenerator

A class that walks a list of routed URL patterns, requests the schema for each view, and collates the resulting CoreAPI Document.

Класс, который просматривает список шаблонов URL, запрашивает схему для каждого представления и собирает результирующий документ CoreAPI.

Typically you'll instantiate `SchemaGenerator` with a single argument, like so:

Обычно вы создаете `SchemaGenerator` с одним аргументом, например, так:

```
generator = SchemaGenerator(title='Stock Prices API')
```

Arguments:

Аргументы:

* `title` **required** - The name of the API.
* `url` - The root URL of the API schema. This option is not required unless the schema is included under path prefix.
* `patterns` - A list of URLs to inspect when generating the schema. Defaults to the project's URL conf.
* `urlconf` - A URL conf module name to use when generating the schema. Defaults to `settings.ROOT_URLCONF`.

* `title` **required** - Название API.
* `url` - Корневой URL схемы API. Этот параметр не требуется, если схема не включена в префикс path.
* `patterns` - Список URL-адресов для проверки при генерации схемы. По умолчанию используется URL conf проекта.
* `urlconf` - Имя модуля URL conf для использования при генерации схемы. По умолчанию `settings.ROOT_URLCONF`.

### get_schema(self, request)

### get_schema(self, request)

Returns a `coreapi.Document` instance that represents the API schema.

Возвращает экземпляр `coreapi.Document`, который представляет схему API.

```
@api_view
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bookings API')
    return Response(generator.get_schema())
```

The `request` argument is optional, and may be used if you want to apply per-user permissions to the resulting schema generation.

Аргумент `request` является необязательным и может быть использован, если вы хотите применить разрешения для каждого пользователя к результирующей генерации схемы.

### get_links(self, request)

### get_links(self, request)

Return a nested dictionary containing all the links that should be included in the API schema.

Возвращает вложенный словарь, содержащий все ссылки, которые должны быть включены в схему API.

This is a good point to override if you want to modify the resulting structure of the generated schema, as you can build a new dictionary with a different layout.

Это хороший момент для переопределения, если вы хотите изменить результирующую структуру сгенерированной схемы, так как вы можете построить новый словарь с другим расположением.

## AutoSchema

## AutoSchema

A class that deals with introspection of individual views for schema generation.

Класс, который занимается интроспекцией отдельных представлений для генерации схемы.

`AutoSchema` is attached to `APIView` via the `schema` attribute.

`AutoSchema` прикрепляется к `APIView` через атрибут `chema`.

The `AutoSchema` constructor takes a single keyword argument `manual_fields`.

Конструктор `AutoSchema` принимает единственный аргумент ключевого слова `manual_fields`.

**`manual_fields`**: a `list` of `coreapi.Field` instances that will be added to the generated fields. Generated fields with a matching `name` will be overwritten.

**`manual_fields`**: `список` экземпляров `coreapi.Field`, которые будут добавлены к сгенерированным полям. Сгенерированные поля с совпадающим `именем` будут перезаписаны.

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

Для более продвинутой настройки подкласс `AutoSchema` позволяет настроить генерацию схемы.

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

Для переопределения доступны следующие методы.

### get_link(self, path, method, base_url)

### get_link(self, path, method, base_url)

Returns a `coreapi.Link` instance corresponding to the given view.

Возвращает экземпляр `coreapi.Link`, соответствующий данному представлению.

This is the main entry point. You can override this if you need to provide custom behaviors for particular views.

Это основная точка входа. Вы можете переопределить его, если вам нужно обеспечить пользовательское поведение для определенных представлений.

### get_description(self, path, method)

### get_description(self, path, method)

Returns a string to use as the link description. By default this is based on the view docstring as described in the "Schemas as Documentation" section above.

Возвращает строку для использования в качестве описания ссылки. По умолчанию она основывается на docstring представления, как описано в разделе "Схемы как документация" выше.

### get_encoding(self, path, method)

### get_encoding(self, path, method)

Returns a string to indicate the encoding for any request body, when interacting with the given view. Eg. `'application/json'`. May return a blank string for views that do not expect a request body.

Возвращает строку, указывающую кодировку для любого тела запроса при взаимодействии с данным представлением. Например, `'application/json'`. Может возвращать пустую строку для представлений, которые не ожидают тело запроса.

### get_path_fields(self, path, method):

### get_path_fields(self, path, method):

Return a list of `coreapi.Field()` instances. One for each path parameter in the URL.

Возвращает список экземпляров `coreapi.Field()`. По одному для каждого параметра пути в URL.

### get_serializer_fields(self, path, method)

### get_serializer_fields(self, path, method)

Return a list of `coreapi.Field()` instances. One for each field in the serializer class used by the view.

Возвращает список экземпляров `coreapi.Field()`. По одному для каждого поля в классе сериализатора, используемого представлением.

### get_pagination_fields(self, path, method)

### get_pagination_fields(self, path, method)

Return a list of `coreapi.Field()` instances, as returned by the `get_schema_fields()` method on any pagination class used by the view.

Возвращает список экземпляров `coreapi.Field()`, возвращенных методом `get_schema_fields()` любого класса пагинации, используемого представлением.

### get_filter_fields(self, path, method)

### get_filter_fields(self, path, method)

Return a list of `coreapi.Field()` instances, as returned by the `get_schema_fields()` method of any filter classes used by the view.

Возвращает список экземпляров `coreapi.Field()`, возвращенных методом `get_schema_fields()` любых классов фильтров, используемых представлением.

### get_manual_fields(self, path, method)

### get_manual_fields(self, path, method)

Return a list of `coreapi.Field()` instances to be added to or replace generated fields. Defaults to (optional) `manual_fields` passed to `AutoSchema` constructor.

Возвращает список экземпляров `coreapi.Field()`, которые будут добавлены к сгенерированным полям или заменят их. По умолчанию (необязательно) `manual_fields`, переданный в конструктор `AutoSchema`.

May be overridden to customise manual fields by `path` or `method`. For example, a per-method adjustment may look like this:

Может быть переопределена для настройки ручных полей по `пути` или `методу`. Например, настройка для каждого метода может выглядеть следующим образом:

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

### update_fields(fields, update_with)

Utility `staticmethod`. Encapsulates logic to add or replace fields from a list by `Field.name`. May be overridden to adjust replacement criteria.

Утилита `staticmethod`. Инкапсулирует логику добавления или замены полей из списка по `Field.name`. Может быть переопределен для настройки критериев замены.

## ManualSchema

## ManualSchema

Allows manually providing a list of `coreapi.Field` instances for the schema, plus an optional description.

Позволяет вручную предоставить список экземпляров `coreapi.Field` для схемы, плюс необязательное описание.

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

Конструктор `ManualSchema` принимает два аргумента:

**`fields`**: A list of `coreapi.Field` instances. Required.

**`fields`**: Список экземпляров `coreapi.Field`. Требуется.

**`description`**: A string description. Optional.

**`description`**: Строковое описание. Необязательно.

**`encoding`**: Default `None`. A string encoding, e.g `application/json`. Optional.

**`encoding`**: По умолчанию `None`. Строковая кодировка, например `application/json`. Необязательно.

---

## Core API

## Core API

This documentation gives a brief overview of the components within the `coreapi` package that are used to represent an API schema.

Эта документация дает краткий обзор компонентов пакета `coreapi`, которые используются для представления схемы API.

Note that these classes are imported from the `coreapi` package, rather than from the `rest_framework` package.

Обратите внимание, что эти классы импортируются из пакета `coreapi`, а не из пакета `rest_framework`.

### Document

### Документ

Represents a container for the API schema.

Представляет собой контейнер для схемы API.

#### `title`

#### `title`.

A name for the API.

Имя для API.

#### `url`

#### `url`.

A canonical URL for the API.

Канонический URL-адрес для API.

#### `content`

#### `content`.

A dictionary, containing the `Link` objects that the schema contains.

Словарь, содержащий объекты `Link`, которые содержит схема.

In order to provide more structure to the schema, the `content` dictionary may be nested, typically to a second level. For example:

Для обеспечения большей структуры схемы словарь `содержания` может быть вложенным, обычно до второго уровня. Например:

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

### Ссылка

Represents an individual API endpoint.

Представляет собой отдельную конечную точку API.

#### `url`

#### `url`.

The URL of the endpoint. May be a URI template, such as `/users/{username}/`.

URL конечной точки. Может быть шаблоном URI, например `/users/{username}/`.

#### `action`

#### `action`.

The HTTP method associated with the endpoint. Note that URLs that support more than one HTTP method, should correspond to a single `Link` for each.

Метод HTTP, связанный с конечной точкой. Обратите внимание, что URL, поддерживающие более одного метода HTTP, должны соответствовать одному `Link` для каждого из них.

#### `fields`

#### `fields`.

A list of `Field` instances, describing the available parameters on the input.

Список экземпляров `Field`, описывающих доступные параметры на входе.

#### `description`

#### `description`.

A short description of the meaning and intended usage of the endpoint.

Краткое описание значения и предполагаемого использования конечной точки.

### Field

### Поле

Represents a single input parameter on a given API endpoint.

Представляет один входной параметр на данной конечной точке API.

#### `name`

#### `name`.

A descriptive name for the input.

Описательное имя для входа.

#### `required`

#### `необходимо`

A boolean, indicated if the client is required to included a value, or if the parameter can be omitted.

Булево значение, указывающее, должен ли клиент включить значение, или параметр может быть опущен.

#### `location`

#### `локация`.

Determines how the information is encoded into the request. Should be one of the following strings:

Определяет, как информация будет закодирована в запросе. Должна быть одной из следующих строк:

**"path"**

**"путь "**

Included in a templated URI. For example a `url` value of `/products/{product_code}/` could be used together with a `"path"` field, to handle API inputs in a URL path such as `/products/slim-fit-jeans/`.

Включается в шаблонный URI. Например, значение `url` `/products/{product_code}/` может использоваться вместе с полем `"path"` для обработки входов API с URL-путем, например `/products/slim-fit-jeans/`.

These fields will normally correspond with [named arguments in the project URL conf](https://docs.djangoproject.com/en/stable/topics/http/urls/#named-groups).

Эти поля обычно соответствуют [именованным аргументам в URL conf проекта](https://docs.djangoproject.com/en/stable/topics/http/urls/#named-groups).

**"query"**

**"запрос "**

Included as a URL query parameter. For example `?search=sale`. Typically for `GET` requests.

Включается в качестве параметра запроса URL. Например, `?search=sale`. Обычно для запросов `GET`.

These fields will normally correspond with pagination and filtering controls on a view.

Эти поля обычно соответствуют элементам управления пагинацией и фильтрацией в представлении.

**"form"**

**"форма "**

Included in the request body, as a single item of a JSON object or HTML form. For example `{"colour": "blue", ...}`. Typically for `POST`, `PUT` and `PATCH` requests. Multiple `"form"` fields may be included on a single link.

Включается в тело запроса, как отдельный элемент объекта JSON или HTML-формы. Например, `{"color": "синий", ...}`. Обычно для запросов `POST`, `PUT` и `PATCH`. Несколько полей ``формы`` могут быть включены в одну ссылку.

These fields will normally correspond with serializer fields on a view.

Эти поля обычно соответствуют полям сериализатора в представлении.

**"body"**

**"тело "**

Included as the complete request body. Typically for `POST`, `PUT` and `PATCH` requests. No more than one `"body"` field may exist on a link. May not be used together with `"form"` fields.

Включается как полный корпус запроса. Обычно для запросов `POST`, `PUT` и `PATCH`. В ссылке может существовать не более одного поля ``тело``. Не может использоваться вместе с полями `"form"`.

These fields will normally correspond with views that use `ListSerializer` to validate the request input, or with file upload views.

Эти поля обычно соответствуют представлениям, которые используют `ListSerializer` для проверки ввода запроса, или представлениям загрузки файлов.

#### `encoding`

#### `encoding`.

**"application/json"**

**"application/json "**.

JSON encoded request content. Corresponds to views using `JSONParser`. Valid only if either one or more `location="form"` fields, or a single `location="body"` field is included on the `Link`.

Содержимое запроса в кодировке JSON. Соответствует представлениям, использующим `JSONParser`. Действителен, только если в `Link` включено одно или несколько полей `location="form"` или одно поле `location="body"`.

**"multipart/form-data"**

**"multipart/form-data "**.

Multipart encoded request content. Corresponds to views using `MultiPartParser`. Valid only if one or more `location="form"` fields is included on the `Link`.

Многокомпонентное кодированное содержимое запроса. Соответствует представлениям, использующим `MultiPartParser`. Действует, только если в `Link` включено одно или несколько полей `location="form"`.

**"application/x-www-form-urlencoded"**

** "application/x-www-form-urlencoded "**.

URL encoded request content. Corresponds to views using `FormParser`. Valid only if one or more `location="form"` fields is included on the `Link`.

URL-кодированное содержимое запроса. Соответствует представлениям, использующим `FormParser`. Действителен, только если в `Link` включено одно или несколько полей `location="form"`.

**"application/octet-stream"**

**"application/octet-stream "**.

Binary upload request content. Corresponds to views using `FileUploadParser`. Valid only if a `location="body"` field is included on the `Link`.

Содержимое двоичного запроса на выгрузку. Соответствует представлениям, использующим `FileUploadParser`. Действителен только в том случае, если в `Link` включено поле `location="body"`.

#### `description`

#### `description`.

A short description of the meaning and intended usage of the input field.

Краткое описание значения и предполагаемого использования поля ввода.

---

# Third party packages

# Пакеты сторонних производителей

## drf-yasg - Yet Another Swagger Generator

## drf-yasg - Yet Another Swagger Generator

[drf-yasg](https://github.com/axnsan12/drf-yasg/) generates [OpenAPI](https://openapis.org/) documents suitable for code generation - nested schemas, named models, response bodies, enum/pattern/min/max validators, form parameters, etc.

[drf-yasg](https://github.com/axnsan12/drf-yasg/) генерирует [OpenAPI](https://openapis.org/) документы, пригодные для генерации кода - вложенные схемы, именованные модели, тела ответов, валидаторы enum/pattern/min/max, параметры форм и т.д.

## drf-spectacular - Sane and flexible OpenAPI 3.0 schema generation for Django REST framework

## drf-spectacular - Разумная и гибкая генерация схем OpenAPI 3.0 для REST-фреймворка Django

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) is a [OpenAPI 3](https://openapis.org/) schema generation tool with explicit focus on extensibility, customizability and client generation. It's usage patterns are very similar to [drf-yasg](https://github.com/axnsan12/drf-yasg/).

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) - это инструмент генерации схем [OpenAPI 3](https://openapis.org/) с явным акцентом на расширяемость, настраиваемость и генерацию клиентов. Модели его использования очень похожи на [drf-yasg](https://github.com/axnsan12/drf-yasg/).