<!-- TRANSLATED by md-translate -->
---

source:

источник:

* negotiation.py

* negotiation.py

---

# Content negotiation

# Переговоры по содержанию

> HTTP has provisions for several mechanisms for "content negotiation" - the process of selecting the best representation for a given response when there are multiple representations available.
>
> — [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html), Fielding et al.

> HTTP предусматривает несколько механизмов "согласования содержания" - процесс выбора наилучшего представления для данного ответа при наличии нескольких представлений.
>
> - [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html), Fielding et al.

Content negotiation is the process of selecting one of multiple possible representations to return to a client, based on client or server preferences.

Согласование содержимого - это процесс выбора одного из нескольких возможных представлений для возврата клиенту, основанный на предпочтениях клиента или сервера.

## Determining the accepted renderer

## Определение принятого рендерера

REST framework uses a simple style of content negotiation to determine which media type should be returned to a client, based on the available renderers, the priorities of each of those renderers, and the client's `Accept:` header. The style used is partly client-driven, and partly server-driven.

Фреймворк REST использует простой стиль согласования контента для определения того, какой тип медиа должен быть возвращен клиенту, основываясь на доступных рендерерах, приоритетах каждого из них и заголовке клиента `Accept:`. Используемый стиль частично зависит от клиента, а частично от сервера.

1. More specific media types are given preference to less specific media types.
2. If multiple media types have the same specificity, then preference is given to based on the ordering of the renderers configured for the given view.

1. Более конкретным типам носителей отдается предпочтение перед менее конкретными типами носителей.
2. Если несколько типов медиа имеют одинаковую специфичность, то предпочтение отдается на основе порядка рендеринга, настроенного для данного представления.

For example, given the following `Accept` header:

Например, при следующем заголовке `Accept`:

```
application/json; indent=4, application/json, application/yaml, text/html, */*
```

The priorities for each of the given media types would be:

Приоритеты для каждого из указанных типов носителей будут следующими:

* `application/json; indent=4`
* `application/json`, `application/yaml` and `text/html`
* `*/*`

* ``application/json; indent=4``
* ``application/json``, ``application/yaml`` и ``text/html``
* `*/*`

If the requested view was only configured with renderers for `YAML` and `HTML`, then REST framework would select whichever renderer was listed first in the `renderer_classes` list or `DEFAULT_RENDERER_CLASSES` setting.

Если запрашиваемое представление было настроено только с рендерерами для `YAML` и `HTML`, то REST framework будет выбирать тот рендерер, который указан первым в списке `renderer_classes` или настройке `DEFAULT_RENDERER_CLASSES`.

For more information on the `HTTP Accept` header, see [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)

Более подробную информацию о заголовке `HTTP Accept` смотрите в [RFC 2616] (https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html).

---

**Note**: "q" values are not taken into account by REST framework when determining preference. The use of "q" values negatively impacts caching, and in the author's opinion they are an unnecessary and overcomplicated approach to content negotiation.

**Примечание**: Значения "q" не учитываются REST-фреймворком при определении предпочтений. Использование значений "q" негативно влияет на кэширование, и, по мнению автора, это ненужный и слишком сложный подход к согласованию контента.

This is a valid approach as the HTTP spec deliberately underspecifies how a server should weight server-based preferences against client-based preferences.

Это правильный подход, поскольку спецификация HTTP намеренно не определяет, как сервер должен взвешивать предпочтения, основанные на сервере, против предпочтений, основанных на клиенте.

---

# Custom content negotiation

# Переговоры по пользовательскому контенту

It's unlikely that you'll want to provide a custom content negotiation scheme for REST framework, but you can do so if needed. To implement a custom content negotiation scheme override `BaseContentNegotiation`.

Маловероятно, что вы захотите предоставить пользовательскую схему согласования содержимого для REST-фреймворка, но вы можете сделать это при необходимости. Для реализации пользовательской схемы согласования контента переопределите `BaseContentNegotiation`.

REST framework's content negotiation classes handle selection of both the appropriate parser for the request, and the appropriate renderer for the response, so you should implement both the `.select_parser(request, parsers)` and `.select_renderer(request, renderers, format_suffix)` methods.

Классы согласования контента фреймворка REST обрабатывают выбор как подходящего парсера для запроса, так и подходящего рендерера для ответа, поэтому вы должны реализовать оба метода `.select_parser(request, parsers)` и `.select_renderer(request, renderers, format_suffix)`.

The `select_parser()` method should return one of the parser instances from the list of available parsers, or `None` if none of the parsers can handle the incoming request.

Метод `select_parser()` должен вернуть один из экземпляров парсера из списка доступных парсеров, или `None`, если ни один из парсеров не может обработать входящий запрос.

The `select_renderer()` method should return a two-tuple of (renderer instance, media type), or raise a `NotAcceptable` exception.

Метод `select_renderer()` должен возвращать кортеж из (экземпляр рендерера, тип медиа), либо вызывать исключение `NotAcceptable`.

## Example

## Пример

The following is a custom content negotiation class which ignores the client request when selecting the appropriate parser or renderer.

Ниже представлен пользовательский класс согласования содержимого, который игнорирует запрос клиента при выборе подходящего парсера или рендерера.

```
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

## Setting the content negotiation

## Установка согласования содержания

The default content negotiation class may be set globally, using the `DEFAULT_CONTENT_NEGOTIATION_CLASS` setting. For example, the following settings would use our example `IgnoreClientContentNegotiation` class.

Класс согласования содержимого по умолчанию можно установить глобально, используя параметр `DEFAULT_CONTENT_NEGOTIATION_CLASS`. Например, следующие настройки будут использовать наш пример класса `IgnoreClientContentNegotiation`.

```
REST_FRAMEWORK = {
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'myapp.negotiation.IgnoreClientContentNegotiation',
}
```

You can also set the content negotiation used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить согласование содержимого, используемое для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```
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