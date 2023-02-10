<!-- TRANSLATED by md-translate -->
# Урок 6: Наборы представлений и маршрутизаторы

DRF включает абстракцию для работы с `ViewSets`, которая позволяет разработчику сосредоточиться на моделировании состояния и взаимодействий API, а построение URL-адресов оставить для автоматической обработки, основанной на общепринятых соглашениях.

Классы `ViewSet` - это почти то же самое, что и классы `View`, за исключением того, что они предоставляют такие операции, как `retrieve` или `update`, а не обработчики методов, таких как `get` или `put`.

Класс `ViewSet` привязывается к набору обработчиков методов только в последний момент, когда он инстанцируется в набор представлений, обычно с помощью класса `Router`, который обрабатывает сложности определения URL conf за вас.

## Рефакторинг для использования ViewSets

Давайте возьмем наш текущий набор представлений и рефакторим их в наборы представлений.

Прежде всего, давайте рефакторим наши классы `UserList` и `UserDetail` в один класс `UserViewSet`. Мы можем удалить два класса представлений и заменить их одним классом ViewSet:

```python
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Здесь мы использовали класс `ReadOnlyModelViewSet` для автоматического предоставления операций по умолчанию "только для чтения". Мы по-прежнему устанавливаем атрибуты `queryset` и `serializer_class` точно так же, как и при использовании обычных представлений, но нам больше не нужно предоставлять одну и ту же информацию двум отдельным классам.

Далее мы заменим классы представления `SnippetList`, `SnippetDetail` и `SnippetHighlight`. Мы можем удалить три предоставления и снова заменить их одним классом.

```python
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

На этот раз мы использовали класс `ModelViewSet`, чтобы получить полный набор операций чтения и записи по умолчанию.

Обратите внимание, что мы также использовали декоратор `@action` для создания пользовательского действия, названного `highlight`. Этот декоратор можно использовать для добавления любых пользовательских конечных точек, которые не вписываются в стандартный стиль `create`/`update`/`delete`.

Пользовательские действия, использующие декоратор `@action`, по умолчанию обрабатывают `GET` запросы. Мы можем использовать аргумент `methods`, если хотим получить действие, обрабатывающее `POST` запросы.

URL-адреса для пользовательских действий по умолчанию зависят от имени самого метода. Если вы хотите изменить способ построения URL, вы можете включить `url_path` в качестве именованного аргумента декоратора.

## Привязка наборов представлений к URL-адресам в явном виде

Методы обработчика привязываются к действиям только тогда, когда мы определяем URLConf. Чтобы увидеть, что происходит под капотом, давайте сначала явно создадим набор представлений из наших ViewSet.

В файле `snippets/urls.py` мы связываем наши классы `ViewSet` в набор конкретных представлений.

```python
from rest_framework import renderers

from snippets.views import api_root, SnippetViewSet, UserViewSet

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
```

Обратите внимание, как мы создаем несколько представлений из каждого класса `ViewSet`, связывая методы HTTP с необходимым действием для каждого представления.

Теперь, когда мы связали наши ресурсы в конкретные представления, мы можем зарегистрировать представления с помощью URL conf, как обычно.

```python
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
```

## Использование маршрутизаторов

Поскольку мы используем классы `ViewSet`, а не `View`, нам не нужно самим планировать URL conf. Соглашения о соединении ресурсов в представления и URL-адреса могут быть обработаны автоматически, с помощью класса `Router`. Все, что нам нужно сделать, это зарегистрировать соответствующие наборы представлений в маршрутизаторе, и пусть он сделает все остальное.

Вот наш переделанный файл `snippets/urls.py`.

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
```

Регистрация наборов представлений в маршрутизаторе аналогична предоставлению шаблона url. Мы включаем два аргумента - префикс URL для представлений и сам набор представлений.

Класс `DefaultRouter`, который мы используем, также автоматически создает для нас корневое представление API, поэтому мы можем удалить функцию `api_root` из нашего модуля `views`.

## Компромиссы между представлениями и наборами представлений

Использование наборов представлений может быть действительно полезной абстракцией. Она помогает обеспечить согласованность соглашений URL в вашем API, минимизирует объем кода, который вам нужно написать, и позволяет вам сосредоточиться на взаимодействии и представлениях, которые предоставляет ваш API, а не на специфике URL conf.

Но это не значит, что такой подход всегда правильный. Существует аналогичный набор компромиссов, которые необходимо учитывать при использовании представлений на основе классов вместо представлений на основе функций. Использование наборов представлений менее очевидно, чем создание представлений API по отдельности.
