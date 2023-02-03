<!-- TRANSLATED by md-translate -->
---

source:

источник:

* reverse.py

* reverse.py

---

# Returning URLs

# Возвращение URL-адресов

> The central feature that distinguishes the REST architectural style from other network-based styles is its emphasis on a uniform interface between components.
>
> — Roy Fielding, [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5)

> Центральной особенностью, отличающей архитектурный стиль REST от других сетевых стилей, является его акцент на едином интерфейсе между компонентами.
>
> - Рой Филдинг, [Архитектурные стили и проектирование сетевых архитектур программного обеспечения](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5)

As a rule, it's probably better practice to return absolute URIs from your Web APIs, such as `http://example.com/foobar`, rather than returning relative URIs, such as `/foobar`.

Как правило, лучше возвращать абсолютные URI из ваших Web API, например `http://example.com/foobar`, а не относительные URI, например `/foobar`.

The advantages of doing so are:

Преимуществами этого являются:

* It's more explicit.
* It leaves less work for your API clients.
* There's no ambiguity about the meaning of the string when it's found in representations such as JSON that do not have a native URI type.
* It makes it easy to do things like markup HTML representations with hyperlinks.

* Это более четко выражено.
* Это оставляет меньше работы для ваших клиентов API.
* Нет двусмысленности относительно значения строки, когда она встречается в таких представлениях, как JSON, которые не имеют собственного типа URI.
* Это упрощает такие вещи, как разметка HTML-представлений с гиперссылками.

REST framework provides two utility functions to make it more simple to return absolute URIs from your Web API.

Фреймворк REST предоставляет две служебные функции для упрощения возврата абсолютных URI из вашего Web API.

There's no requirement for you to use them, but if you do then the self-describing API will be able to automatically hyperlink its output for you, which makes browsing the API much easier.

Использовать их не обязательно, но если вы их используете, то самоописывающийся API сможет автоматически делать для вас гиперссылки на свой вывод, что значительно упростит просмотр API.

## reverse

## реверс

**Signature:** `reverse(viewname, *args, **kwargs)`

**Значение:** `reverse(viewname, *args, **kwargs)`.

Has the same behavior as [`django.urls.reverse`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse), except that it returns a fully qualified URL, using the request to determine the host and port.

Имеет такое же поведение, как [`django.urls.reverse`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse), за исключением того, что возвращает полностью определенный URL, используя запрос для определения хоста и порта.

You should **include the request as a keyword argument** to the function, for example:

Вы должны **включить запрос в качестве аргумента ключевого слова** в функцию, например:

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

## reverse_lazy

**Signature:** `reverse_lazy(viewname, *args, **kwargs)`

**Значение:** `reverse_lazy(viewname, *args, **kwargs)`.

Has the same behavior as [`django.urls.reverse_lazy`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse-lazy), except that it returns a fully qualified URL, using the request to determine the host and port.

Имеет такое же поведение, как [`django.urls.reverse_lazy`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse-lazy), за исключением того, что возвращает полностью определенный URL, используя запрос для определения хоста и порта.

As with the `reverse` function, you should **include the request as a keyword argument** to the function, for example:

Как и в случае с функцией `reverse`, вы должны **включить запрос в качестве аргумента ключевого слова** в функцию, например:

```
api_root = reverse_lazy('api-root', request=request)
```