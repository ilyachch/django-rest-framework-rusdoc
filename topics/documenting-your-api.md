<!-- TRANSLATED by md-translate -->

# Documenting your API

# Документирование вашего API

> A REST API should spend almost all of its descriptive effort in defining the media type(s) used for representing resources and driving application state.
>
> — Roy Fielding, [REST APIs must be hypertext driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

> API REST должен тратить почти все свои усилия по описанию на определение типа(ов) носителей, используемых для представления ресурсов и управления состоянием приложения.
>
> - Рой Филдинг, [REST API должны быть гипертекстовыми](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

REST framework provides a range of different choices for documenting your API. The following is a non-exhaustive list of the most popular ones.

Фреймворк REST предоставляет ряд различных вариантов документирования вашего API. Ниже приведен неполный список наиболее популярных из них.

## Third party packages for OpenAPI support

## Пакеты сторонних разработчиков для поддержки OpenAPI

### drf-spectacular

### drf-spectacular

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) is an [OpenAPI 3](https://openapis.org/) schema generation library with explicit focus on extensibility, customizability and client generation. It is the recommended way for generating and presenting OpenAPI schemas.

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) - это библиотека генерации схем [OpenAPI 3](https://openapis.org/) с явным акцентом на расширяемость, настраиваемость и генерацию клиентов. Это рекомендуемый способ генерации и представления схем OpenAPI.

The library aims to extract as much schema information as possible, while providing decorators and extensions for easy customization. There is explicit support for [swagger-codegen](https://swagger.io/), [SwaggerUI](https://swagger.io/tools/swagger-ui/) and [Redoc](https://github.com/Rebilly/ReDoc), i18n, versioning, authentication, polymorphism (dynamic requests and responses), query/path/header parameters, documentation and more. Several popular plugins for DRF are supported out-of-the-box as well.

Библиотека стремится извлечь как можно больше информации о схеме, предоставляя при этом декораторы и расширения для легкой настройки. Имеется явная поддержка [swagger-codegen](https://swagger.io/), [SwaggerUI](https://swagger.io/tools/swagger-ui/) и [Redoc](https://github.com/Rebilly/ReDoc), i18n, версионность, аутентификация, полиморфизм (динамические запросы и ответы), параметры запроса/пути/заголовка, документация и многое другое. Несколько популярных плагинов для DRF также поддерживаются "из коробки".

### drf-yasg

### drf-yasg

[drf-yasg](https://github.com/axnsan12/drf-yasg/) is a [Swagger / OpenAPI 2](https://swagger.io/) generation tool implemented without using the schema generation provided by Django Rest Framework.

[drf-yasg](https://github.com/axnsan12/drf-yasg/) - это инструмент генерации [Swagger / OpenAPI 2](https://swagger.io/), реализованный без использования генерации схем, предоставляемой Django Rest Framework.

It aims to implement as much of the [OpenAPI 2](https://openapis.org/) specification as possible - nested schemas, named models, response bodies, enum/pattern/min/max validators, form parameters, etc. - and to generate documents usable with code generation tools like `swagger-codegen`.

Его цель - реализовать как можно больше спецификации [OpenAPI 2](https://openapis.org/) - вложенные схемы, именованные модели, тела ответов, валидаторы enum/pattern/min/max, параметры формы и др. - и генерировать документы, пригодные для использования с помощью инструментов генерации кода, таких как `swagger-codegen`.

This also translates into a very useful interactive documentation viewer in the form of `swagger-ui`:

Это также воплощается в очень полезном интерактивном средстве просмотра документации в виде `swagger-ui`:

![Screenshot - drf-yasg](../img/drf-yasg.png)

![Скриншот - drf-yasg](../img/drf-yasg.png)

______________________________________________________________________

## Built-in OpenAPI schema generation (deprecated)

## Встроенная генерация схем OpenAPI (устаревшая)

**Deprecation notice: REST framework's built-in support for generating OpenAPI schemas is deprecated in favor of 3rd party packages that can provide this functionality instead. As replacement, we recommend using the [drf-spectacular](#drf-spectacular) package.**

**Уведомление о сокращении: Встроенная в REST framework поддержка генерации схем OpenAPI устарела в пользу сторонних пакетов, которые могут предоставить эту функциональность вместо нее. В качестве замены мы рекомендуем использовать пакет [drf-spectacular](#drf-spectacular).**.

There are a number of packages available that allow you to generate HTML documentation pages from OpenAPI schemas.

Существует ряд пакетов, позволяющих генерировать HTML-страницы документации на основе схем OpenAPI.

Two popular options are [Swagger UI](https://swagger.io/tools/swagger-ui/) and [ReDoc](https://github.com/Rebilly/ReDoc).

Два популярных варианта - [Swagger UI](https://swagger.io/tools/swagger-ui/) и [ReDoc](https://github.com/Rebilly/ReDoc).

Both require little more than the location of your static schema file or dynamic `SchemaView` endpoint.

Оба требуют лишь указания местоположения статического файла схемы или динамической конечной точки `SchemaView`.

### A minimal example with Swagger UI

### Минимальный пример с Swagger UI

Assuming you've followed the example from the schemas documentation for routing a dynamic `SchemaView`, a minimal Django template for using Swagger UI might be this:

Если предположить, что вы последовали примеру из документации по схемам для маршрутизации динамического `SchemaView`, минимальный шаблон Django для использования Swagger UI может быть таким:

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

Сохраните его в папке templates под именем `swagger-ui.html`. Затем проложите маршрут `TemplateView` в URL conf вашего проекта:

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

Расширенные возможности использования см. в [Swagger UI documentation](https://swagger.io/tools/swagger-ui/).

### A minimal example with ReDoc.

### Минимальный пример с ReDoc.

Assuming you've followed the example from the schemas documentation for routing a dynamic `SchemaView`, a minimal Django template for using ReDoc might be this:

Если предположить, что вы последовали примеру из документации по схемам для маршрутизации динамического `SchemaView`, минимальный шаблон Django для использования ReDoc может быть таким:

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

Сохраните его в папке шаблонов под именем `redoc.html`. Затем проложите маршрут `TemplateView` в URL conf вашего проекта:

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

Расширенное использование см. в [документации ReDoc](https://github.com/Rebilly/ReDoc).

## Self describing APIs

## Самоописывающиеся API

The browsable API that REST framework provides makes it possible for your API to be entirely self describing. The documentation for each API endpoint can be provided simply by visiting the URL in your browser.

Просматриваемый API, который предоставляет фреймворк REST, позволяет вашему API быть полностью самоописывающимся. Документация для каждой конечной точки API может быть предоставлена просто при посещении URL-адреса в браузере.

![Screenshot - Self describing API](../img/self-describing.png)

![Скриншот - API самоописания](../img/self-describing.png)

______________________________________________________________________

#### Setting the title

#### Установка заголовка

The title that is used in the browsable API is generated from the view class name or function name. Any trailing `View` or `ViewSet` suffix is stripped, and the string is whitespace separated on uppercase/lowercase boundaries or underscores.

Заголовок, который используется в просматриваемом API, генерируется из имени класса представления или имени функции. Любой суффикс `View` или `ViewSet` удаляется, а строка разделяется пробелами на прописные/строчные буквы или подчеркивания.

For example, the view `UserListView`, will be named `User List` when presented in the browsable API.

Например, представление `UserListView`, будет называться `User List`, когда будет представлено в просматриваемом API.

When working with viewsets, an appropriate suffix is appended to each generated view. For example, the view set `UserViewSet` will generate views named `User List` and `User Instance`.

При работе с наборами представлений к каждому сгенерированному представлению добавляется соответствующий суффикс. Например, набор представлений `UserViewSet` будет генерировать представления с именами `User List` и `User Instance`.

#### Setting the description

#### Установка описания

The description in the browsable API is generated from the docstring of the view or viewset.

Описание в просматриваемом API генерируется из docstring представления или набора представлений.

If the python `Markdown` library is installed, then [markdown syntax](https://daringfireball.net/projects/markdown/syntax) may be used in the docstring, and will be converted to HTML in the browsable API. For example:

Если установлена библиотека python `Markdown`, то в docstring можно использовать [markdown syntax](https://daringfireball.net/projects/markdown/syntax), который будет преобразован в HTML в просматриваемом API. Например:

```
class AccountListView(views.APIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
```

Note that when using viewsets the basic docstring is used for all generated views. To provide descriptions for each view, such as for the list and retrieve views, use docstring sections as described in [Schemas as documentation: Examples](../api-guide/schemas.md#examples).

Обратите внимание, что при использовании наборов представлений базовая строка документа используется для всех создаваемых представлений. Чтобы предоставить описания для каждого представления, например, для представлений list и retrieve, используйте секции docstring, как описано в [Schemas as documentation: Examples](../api-guide/schemas.md#examples).

#### The `OPTIONS` method

#### Метод `OPTIONS`.

REST framework APIs also support programmatically accessible descriptions, using the `OPTIONS` HTTP method. A view will respond to an `OPTIONS` request with metadata including the name, description, and the various media types it accepts and responds with.

API фреймворка REST также поддерживают программно доступные описания, используя HTTP-метод `OPTIONS`. Представление отвечает на запрос `OPTIONS` с метаданными, включающими название, описание и различные типы медиа, которые оно принимает и на которые отвечает.

When using the generic views, any `OPTIONS` requests will additionally respond with metadata regarding any `POST` or `PUT` actions available, describing which fields are on the serializer.

При использовании общих представлений, любые запросы `OPTIONS` будут дополнительно отвечать метаданными о любых доступных действиях `POST` или `PUT`, описывая, какие поля находятся в сериализаторе.

You can modify the response behavior to `OPTIONS` requests by overriding the `options` view method and/or by providing a custom Metadata class. For example:

Вы можете изменить поведение ответа на `OPTIONS` запросы, переопределив метод представления `options` и/или предоставив пользовательский класс Metadata. Например:

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

Более подробную информацию смотрите в [документации по метаданным](../api-guide/metadata.md).

______________________________________________________________________

## The hypermedia approach

## Гипермедийный подход

To be fully RESTful an API should present its available actions as hypermedia controls in the responses that it sends.

Чтобы быть полностью RESTful, API должен представлять свои доступные действия в виде гипермедийных элементов управления в ответах, которые он отправляет.

In this approach, rather than documenting the available API endpoints up front, the description instead concentrates on the *media types* that are used. The available actions that may be taken on any given URL are not strictly fixed, but are instead made available by the presence of link and form controls in the returned document.

При таком подходе, вместо того, чтобы документировать доступные конечные точки API, описание концентрируется на *типах медиа*, которые используются. Доступные действия, которые могут быть предприняты на любом данном URL, не являются строго фиксированными, но вместо этого становятся доступными благодаря наличию элементов управления ссылками и формами в возвращаемом документе.

To implement a hypermedia API you'll need to decide on an appropriate media type for the API, and implement a custom renderer and parser for that media type. The [REST, Hypermedia & HATEOAS](rest-hypermedia-hateoas.md) section of the documentation includes pointers to background reading, as well as links to various hypermedia formats.

Чтобы реализовать гипермедийный API, вам необходимо выбрать подходящий тип медиа для API и реализовать пользовательский рендерер и парсер для этого типа медиа. Раздел документации \[REST, Hypermedia & HATEOAS\] (rest-hypermedia-hateoas.md) содержит указатели на справочную литературу, а также ссылки на различные форматы гипермедиа.
