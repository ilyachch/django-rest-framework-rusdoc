# Кэширование

> У одной женщины было очень острое сознание, но почти не было памяти ... Она помнила достаточно, чтобы работать, и она много работала.
>
> - Lydia Davis

Кэширование в REST Framework хорошо работает с утилитами кеширования, предоставленными в Django.

## Использование кеша с apiview и viewsets

Django предоставляет [`method_decorator`][decorator] для использования декораторов с представлениями на основе классов. Его можно использовать с другими кэщтрующими декораторами, такими как [`cache_page`][page] и [` var_on_cookie`][cookie].

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
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

---

**Примечание:** Декоратор [`cache_page`][page] кэширует только ответы` GET` и `HEAD` со статусом 200.

---

[page]: https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache
[cookie]: https://docs.djangoproject.com/en/dev/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie
[decorator]: https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class
