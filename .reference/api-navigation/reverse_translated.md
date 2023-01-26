<!-- TRANSLATED by md-translate -->
---

source:

источник:

* reverse.py

* reverse.py

---

# Returning URLs

# Возвращающие URL -адреса

> The central feature that distinguishes the REST architectural style from other network-based styles is its emphasis on a uniform interface between components.
>
> — Roy Fielding, [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5)

> Центральной особенностью, которая отличает в основе архитектурного стиля остального от других стилей сети, является его акцент на едином интерфейсе между компонентами.
>
>-Рой Филдинг, [Архитектурные стили и дизайн сетевых программных архитектур] (https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5)

As a rule, it's probably better practice to return absolute URIs from your Web APIs, such as `http://example.com/foobar`, rather than returning relative URIs, such as `/foobar`.

Как правило, вероятно, лучше вернуть абсолютные URI из ваших веб -API, таких как `http: // example.com/foobar`, а не возвращение относительных URI, таких как«/foobar ».

The advantages of doing so are:

Преимущества этого:

* It's more explicit.
* It leaves less work for your API clients.
* There's no ambiguity about the meaning of the string when it's found in representations such as JSON that do not have a native URI type.
* It makes it easy to do things like markup HTML representations with hyperlinks.

* Это более ясно.
* Это оставляет меньше работы для ваших клиентов API.
* Нет никакой двусмысленности в отношении значения строки, когда она находится в таких представлениях, как JSON, у которых нет нативного типа URI.
* Это позволяет легко делать такие вещи, как разметка HTML -представления с гиперссылками.

REST framework provides two utility functions to make it more simple to return absolute URIs from your Web API.

Framework REST предоставляет две утилиты, чтобы сделать его более простым для возврата абсолютных URI из вашего веб -API.

There's no requirement for you to use them, but if you do then the self-describing API will be able to automatically hyperlink its output for you, which makes browsing the API much easier.

Вам не требуется их использовать, но если вы это сделаете, то API самоописания сможет автоматически гиперссыпать для вас результаты, что значительно облегчает просмотр API.

## reverse

## задний ход

**Signature:** `reverse(viewname, *args, **kwargs)`

** Подпись: ** `reverse (viewName,*args, ** kwargs)`

Has the same behavior as [`django.urls.reverse`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse), except that it returns a fully qualified URL, using the request to determine the host and port.

Имеет то же поведение, что и [`django.urls.reverse`] (https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse), за исключением того, что он возвращает полностью квалифицированный URL, используя
запрос на определение хоста и порта.

You should **include the request as a keyword argument** to the function, for example:

Вы должны ** включить запрос в качестве аргумента ключевого слова ** в функцию, например:

```
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.timezone import now

class APIRootView(APIView):
    def get(self, request):
        year = now().year
        data = {
            ...
            'year-summary-url': reverse('year-summary', args=[year], request=request)
        }
        return Response(data)
```

## reverse_lazy

## reample_lazy

**Signature:** `reverse_lazy(viewname, *args, **kwargs)`

** Подпись: ** `reverse_lazy (viewname,*args, ** kwargs)`

Has the same behavior as [`django.urls.reverse_lazy`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse-lazy), except that it returns a fully qualified URL, using the request to determine the host and port.

Имеет то же поведение, что и [`django.urls.reverse_lazy`] (https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse-lazy), за исключением того, что он возвращает полностью квалифицированный URL,
Использование запроса для определения хоста и порта.

As with the `reverse` function, you should **include the request as a keyword argument** to the function, for example:

Как и в случае с функцией `обратно, вы должны ** включить запрос как аргумент ключевого слова ** к функции, например:

```
api_root = reverse_lazy('api-root', request=request)
```