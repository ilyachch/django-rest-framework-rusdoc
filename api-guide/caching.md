<!-- TRANSLATED by md-translate -->
# Кэширование

> У одной женщины было очень острое сознание, но почти не было памяти... Она помнила достаточно, чтобы работать, и она много работала.
>
> * Лидия Дэвис

Кэширование в DRF хорошо работает с утилитами кэширования, предоставляемыми в Django.

---

## Использование кэша с apiview и наборами представлений

Django предоставляет [`method_decorator`](https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/#decorating-the-class) для использования декораторов с представлениями, основанными на классах. Его можно использовать с другими декораторами кэша, такими как [`cache_page`](https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache), [`vary_on_cookie`](https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie) и [`vary_on_headers`](https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.vary.vary_on_headers).

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            "user_feed": request.user.get_user_feed(),
        }
        return Response(content)


class ProfileView(APIView):
    # With auth: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        content = {
            "user_feed": request.user.get_user_feed(),
        }
        return Response(content)


class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        content = {
            "title": "Post title",
            "body": "Post content",
        }
        return Response(content)
```

## Использование кэша с декоратором @api_view

При использовании декоратора `@api_view` декораторы кэша, основанные на методах, такие как [`cache_page`](https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache), [`vary_on_cookie`](https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie) и [`vary_on_headers`](https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.vary.vary_on_headers) могут быть вызваны напрямую.

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response


@cache_page(60 * 15)
@vary_on_cookie
@api_view(["GET"])
def get_user_list(request):
    content = {"user_feed": request.user.get_user_feed()}
    return Response(content)
```

---

**Обратите внимание:** Декоратор [`cache_page`](https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache) кэширует только ответы `GET` и `HEAD` со статусом 200.

---
