<!-- TRANSLATED by md-translate -->
# Учебник 3: Представления на основе классов

Мы также можем писать наши представления API, используя представления на основе классов, а не на основе функций. Как мы увидим, это мощный паттерн, который позволяет нам повторно использовать общую функциональность и помогает нам сохранить наш код [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

## Переписывание нашего API с использованием представлений на основе классов

Мы начнем с того, что перепишем корневое представление как представление на основе классов. Все, что для этого нужно, это немного подправить `views.py`.

```python
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

Пока все хорошо. Это выглядит довольно похоже на предыдущий случай, но мы получили лучшее разделение между различными HTTP-методами. Нам также потребуется обновить представление экземпляра в `views.py`.

```python
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

Выглядит неплохо. Опять же, сейчас это все еще очень похоже на представление на основе функций.

Нам также придется немного подрефакторить наш `snippets/urls.py` теперь, когда мы используем представления на основе классов.

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Хорошо, мы закончили. Если вы запустите сервер разработки, все должно работать как прежде.

## Использование миксинов

Одним из главных преимуществ использования представлений на основе классов является то, что они позволяют нам легко комбинировать многократно используемые фрагменты поведения.

Операции create/retrieve/update/delete, которые мы использовали до сих пор, будут довольно похожими для всех создаваемых нами представлений API, основанных на моделях. Эти части общего поведения реализованы в классах-миксинах REST framework.

Давайте рассмотрим, как мы можем компоновать представления с помощью классов миксинов. Вот наш модуль `views.py`.

```python
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

Сейчас мы рассмотрим, что именно здесь происходит. Мы создаем наше представление, используя `GenericAPIView`, и добавляем `ListModelMixin` и `CreateModelMixin`.

Базовый класс обеспечивает основную функциональность, а классы-миксины предоставляют действия `.list()` и `.create()`. Затем мы явно привязываем методы `get` и `post` к соответствующим действиям. Пока все достаточно просто.

```python
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

Довольно похоже. Мы снова используем класс `GenericAPIView` для обеспечения основной функциональности, и добавляем миксины для обеспечения действий `.retrieve()`, `.update()` и `.destroy()`.

## Использование общих представлений на основе классов

Используя классы-миксины, мы переписали представления, чтобы использовать немного меньше кода, чем раньше, но мы можем пойти еще на один шаг дальше. Фреймворк REST предоставляет набор уже скомбинированных общих представлений, которые мы можем использовать, чтобы еще больше сократить наш модуль `views.py`.

```python
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

Ух ты, как лаконично. Мы получили огромное количество функционала бесплатно, и наш код выглядит как хороший, чистый, идиоматический Django.

Далее мы перейдем к [уроку 4](4-authentication-and-permissions.md), где мы рассмотрим, как мы можем работать с аутентификацией и разрешениями для нашего API.
