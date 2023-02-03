<!-- TRANSLATED by md-translate -->
---

source:

источник:

* metadata.py

* metadata.py

---

# Metadata

# Метаданные

> [The `OPTIONS`] method allows a client to determine the options and/or requirements associated with a resource, or the capabilities of a server, without implying a resource action or initiating a resource retrieval.
>
> — [RFC7231, Section 4.3.7.](https://tools.ietf.org/html/rfc7231#section-4.3.7)

> [Метод `OPTIONS`] позволяет клиенту определить опции и/или требования, связанные с ресурсом, или возможности сервера, не подразумевая действия с ресурсом и не инициируя поиск ресурса.
>
> - [RFC7231, раздел 4.3.7.](https://tools.ietf.org/html/rfc7231#section-4.3.7)

REST framework includes a configurable mechanism for determining how your API should respond to `OPTIONS` requests. This allows you to return API schema or other resource information.

Фреймворк REST включает настраиваемый механизм для определения того, как ваш API должен отвечать на запросы `OPTIONS`. Это позволяет вам возвращать схему API или другую информацию о ресурсе.

There are not currently any widely adopted conventions for exactly what style of response should be returned for HTTP `OPTIONS` requests, so we provide an ad-hoc style that returns some useful information.

В настоящее время не существует широко принятых соглашений о том, какой именно стиль ответа должен быть возвращен для HTTP `OPTIONS` запросов, поэтому мы предоставляем специальный стиль, который возвращает некоторую полезную информацию.

Here's an example response that demonstrates the information that is returned by default.

Вот пример ответа, который демонстрирует информацию, возвращаемую по умолчанию.

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json

{
    "name": "To Do List",
    "description": "List existing 'To Do' items, or create a new item.",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "note": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "title",
                "max_length": 100
            }
        }
    }
}
```

## Setting the metadata scheme

## Установка схемы метаданных

You can set the metadata class globally using the `'DEFAULT_METADATA_CLASS'` settings key:

Вы можете установить класс метаданных глобально, используя ключ настройки `'DEFAULT_METADATA_CLASS'`:

```
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'
}
```

Or you can set the metadata class individually for a view:

Или вы можете установить класс метаданных индивидуально для представления:

```
class APIRoot(APIView):
    metadata_class = APIRootMetadata

    def get(self, request, format=None):
        return Response({
            ...
        })
```

The REST framework package only includes a single metadata class implementation, named `SimpleMetadata`. If you want to use an alternative style you'll need to implement a custom metadata class.

Пакет REST framework включает только одну реализацию класса метаданных, названную `SimpleMetadata`. Если вы хотите использовать альтернативный стиль, вам нужно будет реализовать собственный класс метаданных.

## Creating schema endpoints

## Создание конечных точек схемы

If you have specific requirements for creating schema endpoints that are accessed with regular `GET` requests, you might consider re-using the metadata API for doing so.

Если у вас есть особые требования к созданию конечных точек схемы, доступ к которым осуществляется с помощью обычных запросов `GET`, вы можете рассмотреть возможность повторного использования API метаданных для этого.

For example, the following additional route could be used on a viewset to provide a linkable schema endpoint.

Например, следующий дополнительный маршрут может быть использован в наборе представлений для обеспечения конечной точки схемы со ссылкой.

```python
@action(methods=['GET'], detail=False)
def api_schema(self, request):
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    return Response(data)
```

There are a couple of reasons that you might choose to take this approach, including that `OPTIONS` responses [are not cacheable](https://www.mnot.net/blog/2012/10/29/NO_OPTIONS).

Есть несколько причин, по которым вы можете выбрать такой подход, включая то, что ответы `OPTIONS` [не подлежат кэшированию] (https://www.mnot.net/blog/2012/10/29/NO_OPTIONS).

---

# Custom metadata classes

# Пользовательские классы метаданных

If you want to provide a custom metadata class you should override `BaseMetadata` and implement the `determine_metadata(self, request, view)` method.

Если вы хотите предоставить собственный класс метаданных, вам следует переопределить `BaseMetadata` и реализовать метод `determine_metadata(self, request, view)`.

Useful things that you might want to do could include returning schema information, using a format such as [JSON schema](https://json-schema.org/), or returning debug information to admin users.

Полезные вещи, которые вы, возможно, захотите сделать, могут включать возврат информации о схеме, используя такой формат, как [JSON schema](https://json-schema.org/), или возврат отладочной информации для пользователей-администраторов.

## Example

## Пример

The following class could be used to limit the information that is returned to `OPTIONS` requests.

Следующий класс может быть использован для ограничения информации, возвращаемой на запросы `OPTIONS`.

```
class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description()
        }
```

Then configure your settings to use this custom class:

Затем настройте свои параметры для использования этого пользовательского класса:

```
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'myproject.apps.core.MinimalMetadata'
}
```

# Third party packages

# Пакеты сторонних производителей

The following third party packages provide additional metadata implementations.

Следующие пакеты сторонних производителей предоставляют дополнительные реализации метаданных.

## DRF-schema-adapter

## DRF-schema-adapter

[drf-schema-adapter](https://github.com/drf-forms/drf-schema-adapter) is a set of tools that makes it easier to provide schema information to frontend frameworks and libraries. It provides a metadata mixin as well as 2 metadata classes and several adapters suitable to generate [json-schema](https://json-schema.org/) as well as schema information readable by various libraries.

[drf-schema-adapter](https://github.com/drf-forms/drf-schema-adapter) - это набор инструментов, облегчающих предоставление информации о схемах фронтенд-фреймворкам и библиотекам. Он предоставляет миксин метаданных, а также 2 класса метаданных и несколько адаптеров, подходящих для генерации [json-schema](https://json-schema.org/), а также информации о схемах, читаемой различными библиотеками.

You can also write your own adapter to work with your specific frontend. If you wish to do so, it also provides an exporter that can export those schema information to json files.

Вы также можете написать свой собственный адаптер для работы с вашим конкретным фронтендом. Если вы захотите это сделать, он также предоставляет экспортер, который может экспортировать информацию о схеме в json-файлы.