<!-- TRANSLATED by md-translate -->
# Согласование контента

> HTTP предусматривает несколько механизмов "согласования контента" - процесса выбора наилучшего представления для данного ответа при наличии нескольких представлений.
>
> - [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html), Fielding et al.

Согласование контента - это процесс выбора одного из нескольких возможных форматов ответа для возврата клиенту, основанный на предпочтениях клиента или сервера.

## Определение выбранного рендерера

DRF использует простой стиль согласования контента для определения того, какой формат данных должен быть возвращен клиенту, основываясь на доступных рендерерах, приоритетах каждого из них и заголовке клиента `Accept:`. Используемый стиль частично зависит от клиента, а частично от сервера.

1. Более конкретным типам носителей отдается предпочтение перед менее конкретными типами носителей.
2. Если несколько типов медиа имеют одинаковую специфичность, то предпочтение отдается на основе порядка рендеринга, настроенного для данного представления.

Например, при следующем заголовке `Accept`:

```
application/json; indent=4, application/json, application/yaml, text/html, */*
```

Приоритеты для каждого из указанных типов носителей будут следующими:

* ``application/json; indent=4``
* ``application/json``, ``application/yaml`` и ``text/html``
* `*/*`

Если запрашиваемое представление было настроено только с рендерерами для `YAML` и `HTML`, то DRF будет выбирать тот рендерер, который указан первым в списке `renderer_classes` или настройке `DEFAULT_RENDERER_CLASSES`.

Более подробную информацию о заголовке `HTTP Accept` смотрите в [RFC 2616] (https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html).

---

**Примечание**: Значения "q" не учитываются DRF при определении предпочтений. Использование значений "q" негативно влияет на кэширование, и, по мнению автора, это ненужный и слишком сложный подход к согласованию контента.

Это верный подход, поскольку спецификация HTTP намеренно не определяет, как сервер должен взвешивать предпочтения, основанные на сервере, против предпочтений, основанных на клиенте.

---

# Переговоры по пользовательскому контенту

Маловероятно, что вы захотите предоставить пользовательскую схему согласования контента для DRF, но вы можете сделать это при необходимости. Для реализации пользовательской схемы согласования контента переопределите `BaseContentNegotiation`.

Классы согласования контента DRF обрабатывают выбор как подходящего парсера для запроса, так и подходящего рендерера для ответа, поэтому вы должны реализовать оба метода `.select_parser(request, parsers)` и `.select_renderer(request, renderers, format_suffix)`.

Метод `select_parser()` должен вернуть один экземпляр парсера из списка доступных парсеров, или `None`, если ни один из парсеров не может обработать входящий запрос.

Метод `select_renderer()` должен возвращать кортеж из (экземпляр рендерера, тип медиа), либо вызывать исключение `NotAcceptable`.

## Пример

Ниже представлен пользовательский класс согласования контента, который игнорирует запрос клиента при выборе подходящего парсера или рендерера.

```python
from rest_framework.negotiation import BaseContentNegotiation

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)
```

## Указание согласования контента

Класс согласования контента по умолчанию можно установить глобально, используя настройку `DEFAULT_CONTENT_NEGOTIATION_CLASS`. Например, следующие настройки будут использовать наш пример класса `IgnoreClientContentNegotiation`.

```python
REST_FRAMEWORK = {
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'myapp.negotiation.IgnoreClientContentNegotiation',
}
```

Вы также можете указать согласование контента, используемое для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```python
from myapp.negotiation import IgnoreClientContentNegotiation
from rest_framework.response import Response
from rest_framework.views import APIView

class NoNegotiationView(APIView):
    """
    An example view that does not perform content negotiation.
    """
    content_negotiation_class = IgnoreClientContentNegotiation

    def get(self, request, format=None):
        return Response({
            'accepted media type': request.accepted_renderer.media_type
        })
```
