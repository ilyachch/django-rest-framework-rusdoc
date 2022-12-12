<!-- TRANSLATED by md-translate -->
---

source:
    - metadata.py

источник:
- Metadata.py

---

# Metadata

# Метаданные

> [The `OPTIONS`] method allows a client to determine the options and/or requirements associated with a resource, or the capabilities of a server, without implying a resource action or initiating a resource retrieval.
>
> &mdash; [RFC7231, Section 4.3.7.](https://tools.ietf.org/html/rfc7231#section-4.3.7)

> Метод [опции `] позволяет клиенту определять параметры и/или требования, связанные с ресурсом, или возможности сервера, не подразумевая действие ресурса или инициируя поиск ресурса.
>
> & mdash;
[RFC7231, раздел 4.3.7.] (Https://tools.ietf.org/html/rfc7231#section-4.3.7)

REST framework includes a configurable mechanism for determining how your API should respond to `OPTIONS` requests. This allows you to return API schema or other resource information.

Структура REST включает настраиваемый механизм для определения того, как ваш API должен отвечать на запросы «опции».
Это позволяет вернуть схему API или другую информацию о ресурсах.

There are not currently any widely adopted conventions for exactly what style of response should be returned for HTTP `OPTIONS` requests, so we provide an ad-hoc style that returns some useful information.

В настоящее время нет никаких широко принятых соглашений для того, какой именно стиль ответа должен быть возвращен для запросов http `‘ Options ', поэтому мы предоставляем специальный стиль, который возвращает некоторую полезную информацию.

Here's an example response that demonstrates the information that is returned by default.

Вот пример ответа, который демонстрирует информацию, которая возвращается по умолчанию.

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

Вы можете установить класс метаданных глобально, используя ключ настройки `'default_metadata_class'`

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

Пакет Framework Framework включает в себя только одну реализацию класса метаданных, названную `SimpleMetadata`.
Если вы хотите использовать альтернативный стиль, вам нужно будет внедрить пользовательский класс метаданных.

## Creating schema endpoints

## Создание конечных точек схемы

If you have specific requirements for creating schema endpoints that are accessed with regular `GET` requests, you might consider re-using the metadata API for doing so.

Если у вас есть конкретные требования для создания конечных точек схемы, доступных к регулярным запросам `get ', вы можете рассмотреть возможность повторного использования API метаданных для этого.

For example, the following additional route could be used on a viewset to provide a linkable schema endpoint.

Например, следующий дополнительный маршрут может быть использован на счете просмотра, чтобы обеспечить конечную точку схемы.

```
@action(methods=['GET'], detail=False)
def api_schema(self, request):
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    return Response(data)
```

There are a couple of reasons that you might choose to take this approach, including that `OPTIONS` responses [are not cacheable](https://www.mnot.net/blog/2012/10/29/NO_OPTIONS).

Есть несколько причин, по которым вы можете выбрать этот подход, в том числе ответы «опции» [не являются кэшированными] (https://www.mnot.net/blog/2012/10/29/no_options).

---

# Custom metadata classes

# Пользовательские классы метаданных

If you want to provide a custom metadata class you should override `BaseMetadata` and implement the `determine_metadata(self, request, view)` method.

Если вы хотите предоставить пользовательский класс метаданных, вы должны переопределить `basemetadata` и реализовать метод` desite_metadata (self, запрос, просмотр) ``.

Useful things that you might want to do could include returning schema information, using a format such as [JSON schema](https://json-schema.org/), or returning debug information to admin users.

Полезные вещи, которые вы, возможно, захотите сделать, могут включать возврату информации схемы, используя такой формат, как [JSON Schema] (https://json-schema.org/), или возвращая информация отладки пользователям администратора.

## Example

## Пример

The following class could be used to limit the information that is returned to `OPTIONS` requests.

Следующий класс может быть использован для ограничения информации, которая возвращается в запросы «параметры».

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

Затем настройте настройки, чтобы использовать этот пользовательский класс:

```
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'myproject.apps.core.MinimalMetadata'
}
```

# Third party packages

# Сторонние пакеты

The following third party packages provide additional metadata implementations.

Следующие сторонние пакеты предоставляют дополнительные реализации метаданных.

## DRF-schema-adapter

## drf-schema-adapter

[drf-schema-adapter](https://github.com/drf-forms/drf-schema-adapter) is a set of tools that makes it easier to provide schema information to frontend frameworks and libraries. It provides a metadata mixin as well as 2 metadata classes and several adapters suitable to generate [json-schema](https://json-schema.org/) as well as schema information readable by various libraries.

[DRF-SCHEMA-Adapter] (https://github.com/drf-forms/drf-schema-adapter)-это набор инструментов, которые облегчают предоставление информации схемы для фронтальных фреймворков и библиотек.
Он обеспечивает микшин метаданных, а также 2 класса метаданных и несколько адаптеров, подходящих для генерации [json-schema] (https://json-schema.org/), а также информацию о схеме, читаемой различными библиотеками.

You can also write your own adapter to work with your specific frontend.
If you wish to do so, it also provides an exporter that can export those schema information to json files.

Вы также можете написать свой собственный адаптер для работы с вашим конкретным фронтом.
Если вы хотите сделать это, он также предоставляет экспортеров, который может экспортировать информацию о схеме в файлы JSON.