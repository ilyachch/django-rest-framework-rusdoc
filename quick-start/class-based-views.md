# Урок 3: Представления-классы

Мы также можем написать наши представления API, используя представления-классы, а не представления-функции. Как мы далее убедимся, это мощный паттерн, который позволяет многократно использовать общий функционал и соблюдать принцип [DRY](https://ru.wikipedia.org/wiki/Don%E2%80%99t_repeat_yourself) (Don't repeat youself).

## Переписываем наш API используя предствления-классы

Начнем с того, что перепишем основные предсталения, как представления-классы. Придется переписать `snippets/views.py`.

```py
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

Наше представление выглядит очень похоже на его предыдущее состояние, однако у нас теперь более наглядное разделение используемых HTTP методов. Теперь нужно обновить представление, отвечающее за представление конкретного объекта.

```py
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

Это по преднему очень похоже на предыдущее состояние.

Так же нам необходимо обновить `snippets/urls.py`, поскольку мы теперь используем представления классы.

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

Теперь, если вы запустите сервер, все должно работать точно, как раньше.

## Используем примеси

Одним из решающих преимуществ предсталений-классов является возможность выделять переиспользуемые элементы.

Операции создания/просмотра/изменения/удаления, которые мы используем, по сути, одинаковы для всех представлений. Эти операции реализованы в классах-примесях DRF.

Приведем пример того, как мы можем создать представление используя классы-примеси. Ниже представлен обновленный `snippets/views.py`:

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

Давайте рассмотрим, что сейчас произошло. Мы создаем наше представление, используя класс `GenericAPIView` и добавляя классы-примеси `ListModelMixin` и `CreateModelMixin`.

Базовый класс реализует основной функционал, а классы-примеси реаллизуют методы `.list()` и `.create()`. Затем мы явно привязываем методы `GET` и `POST` к предоставляемым методам. Достаточно просто.

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

Здесь мы поступили подобным образом. Снова использовали базовый класс `GenericAPIView` и добавили примеси, реализующие методы `.retrieve()`, `.update()` и `.destroy()`.

## Используем встроенные представления-классы

Используя встроенные классы-примеси мы переписали представления, используя очень мало кода, по сравнению с предыдущими реализациями, однако мы можем зайти еще дальше. DRF предоставляет набор классов, в которых уже содержатся примеси, которые мы можем использовать, чтобы сократить модуль `snippets/views.py` еще сильнее.

```py
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

Вот теперь это выглядит достаточно лаконично. Мы получили очень много функционала не прикладывая усилий. 

В [4 уроке](quick-start/auth-and-perm.md) этого руководства мы рассмотрим вопросы авторизации и прав доступа к нашему API.
