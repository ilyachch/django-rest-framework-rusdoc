<!-- TRANSLATED by md-translate -->
# Метаданные

> [Метод `OPTIONS`] позволяет клиенту определить опции и/или требования, связанные с ресурсом, или возможности сервера, не подразумевая действия с ресурсом и не инициируя поиск ресурса.
>
> - [RFC7231, раздел 4.3.7.](https://tools.ietf.org/html/rfc7231#section-4.3.7)

DRF включает настраиваемый механизм для определения того, как ваш API должен отвечать на запросы `OPTIONS`. Это позволяет вам возвращать схему API или другую информацию о ресурсе.

В настоящее время не существует широко принятых соглашений о том, какой именно стиль ответа должен быть возвращен для HTTP `OPTIONS` запросов, поэтому мы предоставляем специальный стиль, который возвращает некоторую полезную информацию.

Вот пример ответа, который демонстрирует информацию, возвращаемую по умолчанию.

```http
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

## Установка схемы метаданных

Вы можете установить класс метаданных глобально, используя ключ настройки `'DEFAULT_METADATA_CLASS'`:

```python
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'
}
```

Или вы можете установить класс метаданных индивидуально для представления:

```python
class APIRoot(APIView):
    metadata_class = APIRootMetadata

    def get(self, request, format=None):
        return Response({
            ...
        })
```

Пакет DRF включает только одну реализацию класса метаданных, названную `SimpleMetadata`. Если вы хотите использовать альтернативный стиль, вам нужно будет реализовать собственный класс метаданных.

## Создание конечных точек схемы

Если у вас есть особые требования к созданию конечных точек схемы, доступ к которым осуществляется с помощью обычных запросов `GET`, вы можете рассмотреть возможность повторного использования API метаданных для этого.

Например, следующий дополнительный маршрут может быть использован в наборе представлений для обеспечения конечной точки схемы со ссылкой.

```python
@action(methods=['GET'], detail=False)
def api_schema(self, request):
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    return Response(data)
```

Есть несколько причин, по которым вы можете выбрать такой подход, включая то, что ответы `OPTIONS` [не подлежат кэшированию](https://www.mnot.net/blog/2012/10/29/NO_OPTIONS).

---

# Пользовательские классы метаданных

Если вы хотите предоставить собственный класс метаданных, вам следует переопределить `BaseMetadata` и реализовать метод `determine_metadata(self, request, view)`.

Полезные вещи, которые вы, возможно, захотите сделать, могут включать возврат информации о схеме, используя такой формат, как [JSON schema](https://json-schema.org/), или возврат отладочной информации для пользователей-администраторов.

## Пример

Следующий класс может быть использован для ограничения информации, возвращаемой на запросы `OPTIONS`.

```python
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

Затем настройте свои параметры для использования этого пользовательского класса:

```python
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'myproject.apps.core.MinimalMetadata'
}
```

# Пакеты сторонних производителей

Следующие пакеты сторонних производителей предоставляют дополнительные реализации метаданных.

## DRF-schema-adapter

[drf-schema-adapter](https://github.com/drf-forms/drf-schema-adapter) - это набор инструментов, облегчающих предоставление информации о схемах фронтенд-фреймворкам и библиотекам. Он предоставляет миксин метаданных, а также 2 класса метаданных и несколько адаптеров, подходящих для генерации [json-schema](https://json-schema.org/), а также информации о схемах, читаемой различными библиотеками.

Вы также можете написать свой собственный адаптер для работы с вашим конкретным фронтендом. Если вы захотите это сделать, он также предоставляет экспортер, который может экспортировать информацию о схеме в json-файлы.
