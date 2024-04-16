<!-- TRANSLATED by md-translate -->
# Документирование вашего API

> REST API должен тратить почти все свои усилия по описанию на определение типа(ов) носителей, используемых для представления ресурсов и управления состоянием приложения.
>
> - Рой Филдинг, [REST API должны быть гипертекстовыми](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

DRF предоставляет ряд различных вариантов документирования вашего API. Ниже приведен неполный список наиболее популярных из них.

## Пакеты сторонних разработчиков для поддержки OpenAPI

### drf-spectacular

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/) - это библиотека генерации схем [OpenAPI 3](https://openapis.org/) с явным акцентом на расширяемость, настраиваемость и генерацию клиентов. Это рекомендуемый способ генерации и представления схем OpenAPI.

Библиотека стремится извлечь как можно больше информации о схеме, предоставляя при этом декораторы и расширения для легкой настройки. Имеется явная поддержка [swagger-codegen](https://swagger.io/), [SwaggerUI](https://swagger.io/tools/swagger-ui/) и [Redoc](https://github.com/Rebilly/ReDoc), i18n, версионность, аутентификация, полиморфизм (динамические запросы и ответы), параметры запроса/пути/заголовка, документация и многое другое. Несколько популярных плагинов для DRF также поддерживаются "из коробки".

### drf-yasg

[drf-yasg](https://github.com/axnsan12/drf-yasg/) - это инструмент генерации [Swagger / OpenAPI 2](https://swagger.io/), реализованный без использования генерации схем, предоставляемой DRF.

Его цель - реализовать как можно больше спецификации [OpenAPI 2](https://openapis.org/) - вложенные схемы, именованные модели, тела ответов, валидаторы enum/pattern/min/max, параметры формы и др. - и генерировать документы, пригодные для использования с помощью инструментов генерации кода, таких как `swagger-codegen`.

Это также воплощается в очень полезном интерактивном средстве просмотра документации в виде `swagger-ui`:

![Скриншот - drf-yasg](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-yasg.png)

---

## Built-in OpenAPI schema generation (deprecated)

## Встроенная генерация схем OpenAPI (устаревшая)

**Уведомление о сокращении: Встроенная в REST framework поддержка генерации схем OpenAPI устарела в пользу сторонних пакетов, которые могут предоставить эту функциональность вместо нее. В качестве замены мы рекомендуем использовать пакет [drf-spectacular](#drf-spectacular).**.

Существует ряд пакетов, позволяющих генерировать HTML-страницы документации на основе схем OpenAPI.

Два популярных варианта - [Swagger UI](https://swagger.io/tools/swagger-ui/) и [ReDoc](https://github.com/Rebilly/ReDoc).

Оба требуют лишь указания местоположения статического файла схемы или динамической конечной точки `SchemaView`.

### Минимальный пример с Swagger UI

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

Сохраните его в папке templates под именем `swagger-ui.html`. Затем добавьте маршрут `TemplateView` в URL conf вашего проекта:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]
```

Расширенные возможности использования см. в [Swagger UI documentation](https://swagger.io/tools/swagger-ui/).

### Минимальный пример с ReDoc.

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

Сохраните его в папке шаблонов под именем `redoc.html`. Затем проложите маршрут `TemplateView` в URL conf вашего проекта:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
]
```

Расширенное использование см. в [документации ReDoc](https://github.com/Rebilly/ReDoc).

## Самоописывающиеся API

Web-интерфейс API, который предоставляет DRF, позволяет вашему API быть полностью самоописывающимся. Документация для каждой конечной точки API может быть предоставлена просто при посещении URL-адреса в браузере.

![Скриншот - API самоописания](https://github.com/encode/django-rest-framework/raw/master/docs/img/self-describing.png)

---

#### Установка заголовка

Заголовок, который используется в Web-интерфейсе API, генерируется из имени класса представления или имени функции. Любой суффикс `View` или `ViewSet` удаляется, а строка разделяется пробелами по прописным/строчным буквам или подчеркиваниям.

Например, представление `UserListView`, будет называться `User List`, когда будет представлено в Web-интерфейсе API.

При работе с наборами представлений к каждому сгенерированному представлению добавляется соответствующий суффикс. Например, набор представлений `UserViewSet` будет генерировать представления с именами `User List` и `User Instance`.

#### Установка описания

Описание в Web-интерфейсе API генерируется из docstring представления или набора представлений.

Если установлена библиотека python `Markdown`, то в docstring можно использовать [синтаксис markdown](https://daringfireball.net/projects/markdown/syntax), который будет преобразован в HTML в Web-интерфейсе API. Например:

```python
class AccountListView(views.APIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
```

Обратите внимание, что при использовании наборов представлений базовая строка документа используется для всех создаваемых представлений. Чтобы предоставить описания для каждого представления, например, для представлений list и retrieve, используйте секции docstring, как описано в [Schemas as documentation](../api-guide/schemas.md).

#### Метод `OPTIONS`.

API DRF также поддерживают программно доступные описания, используя HTTP-метод `OPTIONS`. Представление отвечает на запрос `OPTIONS` с метаданными, включающими название, описание и различные типы медиа, которые оно принимает и на которые отвечает.

При использовании общих представлений, любые запросы `OPTIONS` будут получать ответ с метаданными о любых доступных действиях `POST` или `PUT`, описывая, какие поля находятся в сериализаторе.

Вы можете изменить поведение ответа на `OPTIONS` запросы, переопределив метод представления `options` и/или предоставив пользовательский класс Metadata. Например:

```python
def options(self, request, *args, **kwargs):
    """
    Don't include the view description in OPTIONS responses.
    """
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    data.pop('description')
    return Response(data=data, status=status.HTTP_200_OK)
```

Более подробную информацию смотрите в [документации по метаданным](../api-guide/metadata.md).

---

## The hypermedia approach

## Гипермедийный подход

Чтобы быть полностью RESTful, API должен представлять свои доступные действия в виде гипермедийных элементов управления в ответах, которые он отправляет.

При таком подходе, вместо того, чтобы документировать доступные конечные точки API, описание концентрируется на *типах медиа*, которые используются. Доступные действия, которые могут быть предприняты на любом данном URL, не являются строго фиксированными, но вместо этого становятся доступными благодаря наличию элементов управления ссылками и формами в возвращаемом документе.

Чтобы реализовать гипермедийный API, вам необходимо выбрать подходящий тип медиа для API и реализовать пользовательский рендерер и парсер для этого типа медиа. Раздел документации [REST, Hypermedia & HATEOAS](rest-hypermedia-hateoas.md) содержит указатели на справочную литературу, а также ссылки на различные форматы гипермедиа.
