<!-- TRANSLATED by md-translate -->
# Возвращение URL-адресов

> Центральной особенностью, отличающей архитектурный стиль REST от других сетевых стилей, является его акцент на едином интерфейсе между компонентами.
>
> - Рой Филдинг, [Архитектурные стили и проектирование сетевых архитектур программного обеспечения](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5)

Как правило, лучше возвращать абсолютные URI из ваших Web API, например `http://example.com/foobar`, а не относительные URI, например `/foobar`.

Преимуществами этого являются:

* Это более четко выражено.
* Это требует меньше работы для ваших клиентов API.
* Нет двусмысленности относительно значения строки, когда она встречается в таких форматах, как JSON, которые не имеют собственного типа URI.
* Это упрощает такие вещи, как разметка HTML-представлений с гиперссылками.

DRF предоставляет две служебные функции для упрощения возврата абсолютных URI из вашего Web API.

Использовать их не обязательно, но если вы их используете, то самоописывающийся API сможет автоматически делать для вас гиперссылки на свой вывод, что значительно упростит просмотр API.

## reverse

**Сигнатура:** `reverse(viewname, *args, **kwargs)`.

Имеет такое же поведение, как [`django.urls.reverse`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse), за исключением того, что возвращает полностью определенный URL, используя запрос для определения хоста и порта.

Вы должны **включить запрос в качестве аргумента ключевого слова** в функцию, например:

```python
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

**Сигнатура:** `reverse_lazy(viewname, *args, **kwargs)`.

Имеет такое же поведение, как [`django.urls.reverse_lazy`](https://docs.djangoproject.com/en/stable/topics/http/urls/#reverse-lazy), за исключением того, что возвращает полностью определенный URL, используя запрос для определения хоста и порта.

Как и в случае с функцией `reverse`, вы должны **включить запрос в качестве аргумента ключевого слова** в функцию, например:

```python
api_root = reverse_lazy('api-root', request=request)
```
