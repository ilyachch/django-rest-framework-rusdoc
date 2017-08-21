# Урок 3: Представления-классы

Мы также можем написать наши представления API, используя представления-классы, а не представления-функции. Как мы далее убедимся это мощный паттерн, который позволяет многократно использовать общий функционал и соблюдать принцип DRY (Don't repeat youself).

## Применение представлений-классов к нашему API

Прежде всего перепишем наше корневое представление таким образом, чтобы оно использовало классы. Для этого нужно лишь немного изменить содержимое `views.py.`

```py
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """
    Перечисляет все сниппеты или создает новый сниппет.
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

Как видите, это было несложно. Результат не сильно отличается от того, что было раньше, но зато теперь мы добились лучшего разделения между разными HTTP методами. Нам также потребуется внести изменения в экземпляр представления в `views.py`.

```py
class SnippetDetail(APIView):
    """
    Извлекает, обновляет или удаляет экземпляр сниппета.
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

Выглядит неплохо! Опять же, это очень похоже на представления-функции. Нам потребуется немного изменить наш файл `urls.py`, так как теперь мы используем представления на основе классов.

```py
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Вот и все. Если Вы запустите сервер разработки, то все будет работать точно так же, как и до этого.

## Использование примесей 

Одно из главных приемуществ использования представлений-классов заключается в том, что такой подход без труда позволяет нам компоновать повторно используемые элементы логики. 

Операции create/retrieve/update/delete, которые мы использовали выше, будут аналогичными для любых представлений на основе API, которые мы создадим. Эти общие элементы всторены в классы примесей (mixin classes) REST framework.

Давайте посмотрим, как можно написать наши представления с помошью классов примесей. Снова откроем модуль `views.py`.

```py
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

Рассмотрим подробнее, что здесь произошло. Мы строим наше представление с помощью GenericAPIView и добавляем 
`ListModelMixin` и `CreateModelMixin`.

Базовый класс предоставялет основной функционал, в то время как классы примесей дают операции `.list()` и .`create()`. После этого мы явно привязываем методы `get` и `post` для соответствующих действий. Пока что все довольно просто.

```py
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

Мы снова используем класс `GenericAPIView` для основного функционала и добавляем примеси, чтобы получить доступ к операциям `.retrieve()`, `.update()` и `.destroy()`.

## Использование универсальных представлений-классов 

С помощью классов примесей мы переписали наши представления и немного оптимизировали код, но можно пойти еще дальше. REST framework включает набор универсальных представлений, с помощью которых можно еще сильнее сократить наш модуль views.py.

``` py
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

Как говорится "Краткость - сестра таланта". Мы без труда сократили наш код, чтобы он выглядел опрятно и читаемо в соответсвии с идеологией Django.

В [4 части](quick-start/auth-and-perm.md) руководства мы рассмотрим темы аутентификации и доступа для нашего API.