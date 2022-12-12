<!-- TRANSLATED by md-translate -->
# Tutorial 3: Class-based Views

# Учебное пособие 3: Просмотры на основе класса

We can also write our API views using class-based views, rather than function based views. As we'll see this is a powerful pattern that allows us to reuse common functionality, and helps us keep our code [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

Мы также можем написать наши представления API, используя представления на основе классов, а не представления на основе функций.
Как мы увидим, это мощный шаблон, который позволяет нам повторно использовать общую функциональность и помогает нам сохранить наш код [сухой] (https://en.wikipedia.org/wiki/don%27t_repeat_yourself).

## Rewriting our API using class-based views

## Переписывание нашего API с использованием классовых представлений

We'll start by rewriting the root view as a class-based view. All this involves is a little bit of refactoring of `views.py`.

Мы начнем с переписывания корневого представления в качестве классового представления.
Все это включает в себя немного рефакторинга `views.py`.

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

So far, so good. It looks pretty similar to the previous case, but we've got better separation between the different HTTP methods. We'll also need to update the instance view in `views.py`.

Все идет нормально.
Это выглядит довольно похоже на предыдущий случай, но у нас лучшее разделение между различными методами HTTP.
Нам также нужно обновить представление экземпляра в `views.py`.

```
class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

That's looking good. Again, it's still pretty similar to the function based view right now.

Это выглядит хорошо.
Опять же, сейчас это все еще очень похоже на представление на основе функций.

We'll also need to refactor our `snippets/urls.py` slightly now that we're using class-based views.

Нам также нужно рефакторировать наши фрагменты/urls.py`, теперь, когда мы используем представления на основе классов.

```
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Okay, we're done. If you run the development server everything should be working just as before.

Хорошо, мы закончили.
Если вы запускаете сервер разработки, все должно работать так же, как и раньше.

## Using mixins

## Использование Mixins

One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behavior.

Одна из больших побед в использовании классовых представлений заключается в том, что он позволяет нам легко составлять многократные биты поведения.

The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behavior are implemented in REST framework's mixin classes.

Операции Create/Retive/Update/Delete, которые мы использовали до сих пор, будут очень похожи для любых видов API, поддерживаемых моделью, которые мы создаем.
Эти кусочки общего поведения реализованы в классах микшина REST Framework.

Let's take a look at how we can compose the views by using the mixin classes. Here's our `views.py` module again.

Давайте посмотрим, как мы можем составить представление, используя классы Mixin.
Вот наш модуль `views.py` снова.

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

We'll take a moment to examine exactly what's happening here. We're building our view using `GenericAPIView`, and adding in `ListModelMixin` and `CreateModelMixin`.

Мы потратим минутку, чтобы изучить именно то, что здесь происходит.
Мы создаем наш взгляд, используя `genericapiview` и добавляем` listmodelmixin` и `createmodelmixin`.

The base class provides the core functionality, and the mixin classes provide the `.list()` and `.create()` actions. We're then explicitly binding the `get` and `post` methods to the appropriate actions. Simple enough stuff so far.

Базовый класс обеспечивает основную функциональность, а классы Mixin обеспечивают действия `.list ()` и `.create ()`.
Затем мы явно связываем методы «get» и «post» с соответствующими действиями.
Достаточно простые вещи до сих пор.

```
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

Pretty similar. Again we're using the `GenericAPIView` class to provide the core functionality, and adding in mixins to provide the `.retrieve()`, `.update()` and `.destroy()` actions.

Довольно похожий.
Опять же, мы используем класс `genericapiview`, чтобы обеспечить основную функциональность, и добавляем в микшины для предоставления действий` .retrive () `,` .update () `и` .destroy () `.

## Using generic class-based views

## Использование общих просмотров на основе классов

Using the mixin classes we've rewritten the views to use slightly less code than before, but we can go one step further. REST framework provides a set of already mixed-in generic views that we can use to trim down our `views.py` module even more.

Используя классы Mixin, мы переписали представления, чтобы использовать чуть меньше кода, чем раньше, но мы можем пойти на один шаг вперед.
Framework REST обеспечивает набор уже смешанных общих видов, которые мы можем использовать для обрезки нашего `views.py`-модуля еще больше.

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

Wow, that's pretty concise. We've gotten a huge amount for free, and our code looks like good, clean, idiomatic Django.

Вау, это довольно кратко.
Мы получили огромное количество бесплатно, и наш код выглядит как хороший, чистый, идиоматический Джанго.

Next we'll move onto [part 4 of the tutorial](4-authentication-and-permissions.md), where we'll take a look at how we can deal with authentication and permissions for our API.

Затем мы перейдем к [Часть 4 Учебного пособия] (4-Authentication и Permissions.md), где мы посмотрим, как мы можем справиться с аутентификацией и разрешениями для нашего API.