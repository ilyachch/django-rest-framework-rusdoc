<!-- TRANSLATED by md-translate -->
# Caching

# Кэширование

> A certain woman had a very sharp consciousness but almost no memory ... She remembered enough to work, and she worked hard.
>
> * Lydia Davis

> У одной женщины было очень острое сознание, но почти не было памяти... Она помнила достаточно, чтобы работать, и она много работала.
>
> * Лидия Дэвис

Caching in REST Framework works well with the cache utilities provided in Django.

Кэширование в REST Framework хорошо работает с утилитами кэширования, предоставляемыми в Django.

---

## Using cache with apiview and viewsets

## Использование кэша с apiview и наборами представлений

Django provides a [`method_decorator`](https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class) to use decorators with class based views. This can be used with other cache decorators such as [`cache_page`](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache), [`vary_on_cookie`](https://docs.djangoproject.com/en/dev/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie) and [`vary_on_headers`](https://docs.djangoproject.com/en/dev/topics/http/decorators/#django.views.decorators.vary.vary_on_headers).

Django предоставляет [`method_decorator`](https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class) для использования декораторов с представлениями, основанными на классах. Его можно использовать с другими декораторами кэша, такими как [`cache_page`](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache), [`vary_on_cookie`](https://docs.djangoproject.com/en/dev/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie) и [`vary_on_headers`](https://docs.djangoproject.com/en/dev/topics/http/decorators/#django.views.decorators.vary.vary_on_headers).

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)


class ProfileView(APIView):
    # With auth: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)


class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        content = {
            'title': 'Post title',
            'body': 'Post content'
        }
        return Response(content)
```

**NOTE:** The [`cache_page`](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache) decorator only caches the `GET` and `HEAD` responses with status 200.

**NOTE:** Декоратор [`cache_page`](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache) кэширует только ответы `GET` и `HEAD` со статусом 200.