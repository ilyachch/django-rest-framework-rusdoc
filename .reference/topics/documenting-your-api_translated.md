<!-- TRANSLATED by md-translate -->
# Documenting your API

# Документирование вашего API

> A REST API should spend almost all of its descriptive effort in defining the media type(s) used for representing resources and driving application state.
>
> — Roy Fielding, [REST APIs must be hypertext driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

> API REST должен тратить практически все свои описательные усилия на определение типа (ы) среды, используемых для представления ресурсов и состояния приложения.
>
>-Рой Филдинг, [REST API должны быть гипертектными управлением] (https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driened)

REST framework provides a range of different choices for documenting your API. The following is a non-exhaustive list of the most popular ones.

Framework REST предоставляет ряд различных вариантов документирования вашего API.
Ниже приведен неэкгартный список самых популярных.

## Third party packages for OpenAPI support

## Сторонние пакеты для поддержки OpenAPI

### drf-spectacular

### DRF-Spectacular

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) is an [OpenAPI 3](https://openapis.org/) schema generation library with explicit focus on extensibility, customizability and client generation. It is the recommended way for generating and presenting OpenAPI schemas.

[DRF-Spectacular] (https://github.com/tfranzel/drf-spectacular/)-это библиотека схемы [openapi 3] (https://openapis.org/) с явным фокусом на расширении, настраиваемости и генерации клиентов.
Анкет
Это рекомендуемый способ создания и представления схем OpenAPI.

The library aims to extract as much schema information as possible, while providing decorators and extensions for easy customization. There is explicit support for [swagger-codegen](https://swagger.io/), [SwaggerUI](https://swagger.io/tools/swagger-ui/) and [Redoc](https://github.com/Rebilly/ReDoc), i18n, versioning, authentication, polymorphism (dynamic requests and responses), query/path/header parameters, documentation and more. Several popular plugins for DRF are supported out-of-the-box as well.

Библиотека направлена на то, чтобы извлечь как можно больше информации о схеме, предоставляя декораторы и расширения для легкой настройки.
Существует явная поддержка [Swagger-codegen] (https://swagger.io/), [swaggerui] (https://swagger.io/tools/swager-ui/) и [redoc] (https: // github
.com/rebilly/redoc), i18n, управление версией, аутентификация, полиморфизм (динамические запросы и ответы), параметры запроса/путя/заголовка, документация и многое другое.
Несколько популярных плагинов для DRF также поддерживаются без ящика.

### drf-yasg

### drf-yasg

[drf-yasg](https://github.com/axnsan12/drf-yasg/) is a [Swagger / OpenAPI 2](https://swagger.io/) generation tool implemented without using the schema generation provided by Django Rest Framework.

[drf-yasg] (https://github.com/axnsan12/drf-yasg/)-это инструмент Generation [Swagger/OpenApi 2] (https://swagger.io/), реализованный без использования генерации схемы, предоставленной Django
Структура отдыха.

It aims to implement as much of the [OpenAPI 2](https://openapis.org/) specification as possible - nested schemas, named models, response bodies, enum/pattern/min/max validators, form parameters, etc. - and to generate documents usable with code generation tools like `swagger-codegen`.

Он направлен на реализацию как можно большую часть спецификации [openapi 2] (https://openapis.org/) - вложенные схемы, названные модели, тела ответов, enum/pattern/min/max valdators, параметры формы и т. Д. - - - - -
и для создания документов, используемых с помощью инструментов генерации кодов, таких как «Swagger-Codegen».

This also translates into a very useful interactive documentation viewer in the form of `swagger-ui`:

Это также приводит к очень полезному просмотру интерактивной документации в форме `swagger-ui`:

![Screenshot - drf-yasg](../img/drf-yasg.png)

! [Screenshot-DRF-YASG] (../ IMG/DRF-YASG.PNG)

---

## Built-in OpenAPI schema generation (deprecated)

## Встроенная генерация схемы OpenAPI (устарело)

**Deprecation notice: REST framework's built-in support for generating OpenAPI schemas is deprecated in favor of 3rd party packages that can provide this functionality instead. As replacement, we recommend using the [drf-spectacular](#drf-spectacular) package.**

** Уведомление об ископении: встроенная поддержка REST Framework для создания схем OpenAPI устарела в пользу сторонних пакетов, которые могут вместо этого предоставить эту функциональность.
В качестве замены мы рекомендуем использовать пакет [DRF-Spectacular] (#DRF-Spectacular). **

There are a number of packages available that allow you to generate HTML documentation pages from OpenAPI schemas.

Существует несколько пакетов, которые позволяют создавать HTML -страницы документации из схем OpenAPI.

Two popular options are [Swagger UI](https://swagger.io/tools/swagger-ui/) and [ReDoc](https://github.com/Rebilly/ReDoc).

Два популярных варианта-[Swagger UI] (https://swagger.io/tools/swagger-ui/) и [Redoc] (https://github.com/rebilly/redoc).

Both require little more than the location of your static schema file or dynamic `SchemaView` endpoint.

Оба требуют чуть больше, чем местоположение вашего файла статической схемы или динамической конечной точки `schemaview`.

### A minimal example with Swagger UI

### Минимальный пример с Swagger UI

Assuming you've followed the example from the schemas documentation for routing a dynamic `SchemaView`, a minimal Django template for using Swagger UI might be this:

Предполагая, что вы следовали примеру из документации с схемами для маршрутизации динамического «SchemaView», минимального шаблона Django для использования пользовательского интерфейса Swagger.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      type="text/css"
      href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css"
    />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
      const ui = SwaggerUIBundle({
        url: "{% url schema_url %}",
        dom_id: "#swagger-ui",
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset,
        ],
        layout: "BaseLayout",
        requestInterceptor: (request) => {
          request.headers["X-CSRFToken"] = "{{ csrf_token }}";
          return request;
        },
      });
    </script>
  </body>
</html>
```

Save this in your templates folder as `swagger-ui.html`. Then route a `TemplateView` in your project's URL conf:

Сохраните это в папке своих шаблонов как `swagger-ui.html`.
Затем маршрут `templateview` в URL Conf:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
```

See the [Swagger UI documentation](https://swagger.io/tools/swagger-ui/) for advanced usage.

Смотрите документацию [Swagger UI] (https://swagger.io/tools/swagger-ui/) для расширенного использования.

### A minimal example with ReDoc.

### Минимальный пример с Redoc.

Assuming you've followed the example from the schemas documentation for routing a dynamic `SchemaView`, a minimal Django template for using ReDoc might be this:

Предполагая, что вы следовали примеру из документации схемы для маршрутизации динамического «SchemaView», минимального шаблона Django для использования REDOC может быть следующим:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700"
      rel="stylesheet"
    />
    <!-- ReDoc doesn't change outer page styles -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url="{% url schema_url %}"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
  </body>
</html>
```

Save this in your templates folder as `redoc.html`. Then route a `TemplateView` in your project's URL conf:

Сохраните это в папке своих шаблонов как `redoc.html`.
Затем маршрут `templateview` в URL Conf:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]
```

See the [ReDoc documentation](https://github.com/Rebilly/ReDoc) for advanced usage.

См. [Redoc Documentation] (https://github.com/rebilly/redoc) для расширенного использования.

## Self describing APIs

## self -описание API

The browsable API that REST framework provides makes it possible for your API to be entirely self describing. The documentation for each API endpoint can be provided simply by visiting the URL in your browser.

Производимый API, который обеспечивает структуру REST, позволяет вашему API быть полностью самоопределенным.
Документация для каждой конечной точки API может быть предоставлена просто посещение URL -адреса в вашем браузере.

![Screenshot - Self describing API](../img/self-describing.png)

! [Screenshot - Самозапись API] (../ IMG/Self -Describing.png)

---

#### Setting the title

#### Установка заголовка

The title that is used in the browsable API is generated from the view class name or function name. Any trailing `View` or `ViewSet` suffix is stripped, and the string is whitespace separated on uppercase/lowercase boundaries or underscores.

Название, которое используется в API, используемом просмотром, генерируется из имени класса View или имени функции.
Любой суффикс `view` или` `wiedset` stucts's разделен, а строка отделен пробезой на верхних/нижних границах или нижних показателях.

For example, the view `UserListView`, will be named `User List` when presented in the browsable API.

Например, представление `userListView` будет называться« List », когда представлен в API -интерфейсе.

When working with viewsets, an appropriate suffix is appended to each generated view. For example, the view set `UserViewSet` will generate views named `User List` and `User Instance`.

При работе с видами подходящий суффикс добавляется к каждому сгенерированному представлению.
Например, набор View `userviewSet` будет генерировать представления с именем` list 'и `emessurant`.

#### Setting the description

#### Настройка описания

The description in the browsable API is generated from the docstring of the view or viewset.

Описание в API, подлежащем просмотру, генерируется в результате документации вида или сбора просмотра.

If the python `Markdown` library is installed, then [markdown syntax](https://daringfireball.net/projects/markdown/syntax) may be used in the docstring, and will be converted to HTML in the browsable API. For example:

Если библиотека Python `markdown` установлена, то [Sintax Markdown] (https://daringfireball.net/projects/markdown/syntax) может использоваться в Docstring и будет преобразована в HTML в API просмотра.
Например:

```
class AccountListView(views.APIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
```

Note that when using viewsets the basic docstring is used for all generated views. To provide descriptions for each view, such as for the list and retrieve views, use docstring sections as described in [Schemas as documentation: Examples](../api-guide/schemas.md#examples).

Обратите внимание, что при использовании видов базовый DocString используется для всех сгенерированных представлений.
Чтобы предоставить описания для каждого представления, например, для списка и получения представлений, используйте разделы DocString, как описано в [схемы в качестве документации: примеры] (../ API-Guide/Schemas.md#Примеры).

#### The `OPTIONS` method

#### Метод параметров `

REST framework APIs also support programmatically accessible descriptions, using the `OPTIONS` HTTP method. A view will respond to an `OPTIONS` request with metadata including the name, description, and the various media types it accepts and responds with.

API Framework Framework также поддерживают программно доступные описания, используя метод http `` `` `` `` `` `` `` `` метод.
Представление будет отвечать на запрос «Параметры» с метаданными, включая имя, описание и различные типы средств массовой информации, которые он принимает и отвечает.

When using the generic views, any `OPTIONS` requests will additionally respond with metadata regarding any `POST` or `PUT` actions available, describing which fields are on the serializer.

При использовании общих представлений любые запросы «опции» будут дополнительно отвечать метаданным, касающиеся любых доступных действий «post» или `put, описывая, какие поля находятся на сериализаторе.

You can modify the response behavior to `OPTIONS` requests by overriding the `options` view method and/or by providing a custom Metadata class. For example:

Вы можете изменить поведение ответа на запросы `Options ', переопределив метод« Опции »и/или, предоставляя пользовательский класс метаданных.
Например:

```
def options(self, request, *args, **kwargs):
    """
    Don't include the view description in OPTIONS responses.
    """
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    data.pop('description')
    return Response(data=data, status=status.HTTP_200_OK)
```

See [the Metadata docs](../api-guide/metadata.md) for more details.

См. [Документы метаданных] (../ api-guide/metadata.md) для получения более подробной информации.

---

## The hypermedia approach

## подход гипермедиа

To be fully RESTful an API should present its available actions as hypermedia controls in the responses that it sends.

Чтобы быть полностью спокойным, API должен представлять свои доступные действия, поскольку Hypermedia контролирует ответы, которые он посылает.

In this approach, rather than documenting the available API endpoints up front, the description instead concentrates on the *media types* that are used. The available actions that may be taken on any given URL are not strictly fixed, but are instead made available by the presence of link and form controls in the returned document.

При таком подходе вместо документирования доступных конечных точек API впереди, описание вместо этого концентрируется на * типах * носителя *, которые используются.
Доступные действия, которые могут быть предприняты на любой заданный URL -адрес, не являются строго фиксированными, но вместо этого предоставляются доступными путем наличия контроля ссылок и формы в возвращенном документе.

To implement a hypermedia API you'll need to decide on an appropriate media type for the API, and implement a custom renderer and parser for that media type. The [REST, Hypermedia & HATEOAS](rest-hypermedia-hateoas.md) section of the documentation includes pointers to background reading, as well as links to various hypermedia formats.

Чтобы внедрить API Hypermedia, вам необходимо определить соответствующий тип медиа для API, а также внедрить пользовательский рендерер и анализатор для этого типа носителя.
В разделе [REST, Hypermedia & HatoAS] (REST-Hypermedia-Hateoas.md) документация включает в себя указатели на фонах, а также ссылки на различные форматы гипермедиа.