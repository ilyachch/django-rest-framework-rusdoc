<!-- TRANSLATED by md-translate -->
---

source:
    - negotiation.py

источник:
- Durniation.py

---

# Content negotiation

# Переговоры о контенте

> HTTP has provisions for several mechanisms for "content negotiation" - the process of selecting the best representation for a given response when there are multiple representations available.
>
> &mdash; [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html), Fielding et al.

> У HTTP есть положения для нескольких механизмов «согласования контента» - процесса выбора наилучшего представления для данного ответа, когда есть несколько доступных представлений.
>
> & mdash;
[RFC 2616] (https://www.w3.org/protocols/rfc2616/rfc2616-sec12.html), Fielding et al.

Content negotiation is the process of selecting one of multiple possible representations to return to a client, based on client or server preferences.

Соглашение о контенте - это процесс выбора одного из множества возможных представлений для возвращения клиенту, основанного на предпочтениях клиента или сервера.

## Determining the accepted renderer

## Определение принятого рендерера

REST framework uses a simple style of content negotiation to determine which media type should be returned to a client, based on the available renderers, the priorities of each of those renderers, and the client's `Accept:` header.  The style used is partly client-driven, and partly server-driven.

Framework REST использует простой стиль переговоров о контенте, чтобы определить, какой тип носителя должен быть возвращен клиенту, на основе доступных визуализаторов, приоритетов каждого из этих визуализаторов и ‘Принять:` `` заголовок.
Используемый стиль частично управляется клиентом и частично управляется сервером.

1. More specific media types are given preference to less specific media types.
2. If multiple media types have the same specificity, then preference is given to based on the ordering of the renderers configured for the given view.

1. Более конкретные типы носителей получают предпочтение менее конкретным типам носителей.
2. Если несколько типов носителей имеют одинаковую специфичность, то предпочтение дается на основе упорядочения рендеристов, настроенных для данного представления.

For example, given the following `Accept` header:

Например, учитывая следующий заголовок `Принять

```
application/json; indent=4, application/json, application/yaml, text/html, */*
```

The priorities for each of the given media types would be:

Приоритеты для каждого из данных типов средств массовой информации будут:

* `application/json; indent=4`
* `application/json`, `application/yaml` and `text/html`
* `*/*`

* `Приложение/json;
adpent = 4`
* `application/json`,` application/yaml` и `text/html`
*`*/*`

If the requested view was only configured with renderers for `YAML` and `HTML`, then REST framework would select whichever renderer was listed first in the `renderer_classes` list or `DEFAULT_RENDERER_CLASSES` setting.

Если запрошенное представление было настроено только с рендерингами для `yaml` и` html`, то Framework REST выберет, какой рендеринг был первым указан в списке `renderer_classes 'или` default_renderer_classes`.

For more information on the `HTTP Accept` header, see [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)

Для получения дополнительной информации о заголовке `http Accept` см.

---

**Note**: "q" values are not taken into account by REST framework when determining preference.  The use of "q" values negatively impacts caching, and in the author's opinion they are an unnecessary and overcomplicated approach to content negotiation.

** ПРИМЕЧАНИЕ **: «Q» значения не учитываются структурой REST при определении предпочтений.
Использование ценностей «Q» негативно влияет на кэширование, и, по мнению автора, они являются ненужным и чрезмерным подходом к переговорам о контенте.

This is a valid approach as the HTTP spec deliberately underspecifies how a server should weight server-based preferences against client-based preferences.

Это действительный подход, так как спецификация HTTP умышленно подчеркивает, как сервер должен весоть сервер на основе предпочтений на основе клиента.

---

# Custom content negotiation

# Пользовательские переговоры о контенте

It's unlikely that you'll want to provide a custom content negotiation scheme for REST framework, but you can do so if needed.  To implement a custom content negotiation scheme override `BaseContentNegotiation`.

Маловероятно, что вы захотите предоставить пользовательскую схему согласования контента для структуры REST, но вы можете сделать это, если это необходимо.
Для реализации пользовательской схемы согласования контента переопределить «BaseContentNegotiation».

REST framework's content negotiation classes handle selection of both the appropriate parser for the request, and the appropriate renderer for the response, so you should implement both the `.select_parser(request, parsers)` and `.select_renderer(request, renderers, format_suffix)` methods.

Классы переговоров по переговорам по контенту REST обрабатывают выбор как соответствующего анализатора для запроса, так и соответствующего рендерера для ответа, поэтому вы должны реализовать как `.select_parser (request, parsers)` и `.select_renderer (запрос, рендеринги, format_suffix)
`Методы.

The `select_parser()` method should return one of the parser instances from the list of available parsers, or `None` if none of the parsers can handle the incoming request.

Метод `select_parser ()` должен вернуть один из экземпляров анализатора из списка доступных анализаторов или `none`, если ни один из парсеров не может обрабатывать входящий запрос.

The `select_renderer()` method should return a two-tuple of (renderer instance, media type), or raise a `NotAcceptable` exception.

Метод `select_renderer ()` должен вернуть двухверенный (экземпляр рендеринга, тип носителя) или поднять исключение `notecpectable '.

## Example

## Пример

The following is a custom content negotiation class which ignores the client
request when selecting the appropriate parser or renderer.

Ниже приведен класс переговоров по индивидуальному заказу, который игнорирует клиента
Запрос при выборе соответствующего анализатора или рендеринга.

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

## Установка переговоров по контенту

The default content negotiation class may be set globally, using the `DEFAULT_CONTENT_NEGOTIATION_CLASS` setting.  For example, the following settings would use our example `IgnoreClientContentNegotiation` class.

Класс согласования контента по умолчанию может быть установлен по всему миру, используя параметр `default_content_negotiation_class`.
Например, в следующих настройках будет использован наш пример `engoreclientContentnegotiation` класса.

```
REST_FRAMEWORK = {
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'myapp.negotiation.IgnoreClientContentNegotiation',
}
```

You can also set the content negotiation used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить согласование контента, используемое для индивидуального представления, или Viewset, используя на основе классов представлений `Apiview.

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
