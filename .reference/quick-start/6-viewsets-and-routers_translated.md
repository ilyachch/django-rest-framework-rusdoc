<!-- TRANSLATED by md-translate -->
# Tutorial 6: ViewSets & Routers

# Учебник 6: Наборы представлений и маршрутизаторы

REST framework includes an abstraction for dealing with `ViewSets`, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

REST framework включает абстракцию для работы с `ViewSets`, которая позволяет разработчику сосредоточиться на моделировании состояния и взаимодействий API, а построение URL-адресов оставить для автоматической обработки, основанной на общепринятых соглашениях.

`ViewSet` classes are almost the same thing as `View` classes, except that they provide operations such as `retrieve`, or `update`, and not method handlers such as `get` or `put`.

Классы `ViewSet` - это почти то же самое, что и классы `View`, за исключением того, что они предоставляют такие операции, как `retrieve` или `update`, а не обработчики методов, таких как `get` или `put`.

A `ViewSet` class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a `Router` class which handles the complexities of defining the URL conf for you.

Класс `ViewSet` привязывается к набору обработчиков методов только в последний момент, когда он инстанцируется в набор представлений, обычно с помощью класса `Router`, который обрабатывает сложности определения URL conf за вас.

## Refactoring to use ViewSets

## Рефакторинг для использования ViewSets

Let's take our current set of views, and refactor them into view sets.

Давайте возьмем наш текущий набор представлений и рефакторим их в наборы представлений.

First of all let's refactor our `UserList` and `UserDetail` classes into a single `UserViewSet` class. We can remove the two view classes, and replace them with a single ViewSet class:

Прежде всего, давайте рефакторим наши классы `UserList` и `UserDetail` в один класс `UserViewSet`. Мы можем удалить два класса представлений и заменить их одним классом ViewSet:

```
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Here we've used the `ReadOnlyModelViewSet` class to automatically provide the default 'read-only' operations. We're still setting the `queryset` and `serializer_class` attributes exactly as we did when we were using regular views, but we no longer need to provide the same information to two separate classes.

Здесь мы использовали класс `ReadOnlyModelViewSet` для автоматического предоставления операций по умолчанию "только для чтения". Мы по-прежнему устанавливаем атрибуты `queryset` и `serializer_class` точно так же, как и при использовании обычных представлений, но нам больше не нужно предоставлять одну и ту же информацию двум отдельным классам.

Next we're going to replace the `SnippetList`, `SnippetDetail` and `SnippetHighlight` view classes. We can remove the three views, and again replace them with a single class.

Далее мы заменим классы представления `SnippetList`, `SnippetDetail` и `SnippetHighlight`. Мы можем удалить три вида и снова заменить их одним классом.

```
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

This time we've used the `ModelViewSet` class in order to get the complete set of default read and write operations.

На этот раз мы использовали класс `ModelViewSet`, чтобы получить полный набор операций чтения и записи по умолчанию.

Notice that we've also used the `@action` decorator to create a custom action, named `highlight`. This decorator can be used to add any custom endpoints that don't fit into the standard `create`/`update`/`delete` style.

Обратите внимание, что мы также использовали декоратор `@action` для создания пользовательского действия, названного `highlight`. Этот декоратор можно использовать для добавления любых пользовательских конечных точек, которые не вписываются в стандартный стиль `create`/`update`/`delete`.

Custom actions which use the `@action` decorator will respond to `GET` requests by default. We can use the `methods` argument if we wanted an action that responded to `POST` requests.

Пользовательские действия, использующие декоратор `@action`, по умолчанию отвечают на запросы `GET`. Мы можем использовать аргумент `methods`, если хотим получить действие, отвечающее на `POST` запросы.

The URLs for custom actions by default depend on the method name itself. If you want to change the way url should be constructed, you can include `url_path` as a decorator keyword argument.

URL-адреса для пользовательских действий по умолчанию зависят от имени самого метода. Если вы хотите изменить способ построения URL, вы можете включить `url_path` в качестве аргумента ключевого слова декоратора.

## Binding ViewSets to URLs explicitly

## Привязка наборов представлений к URL-адресам в явном виде

The handler methods only get bound to the actions when we define the URLConf. To see what's going on under the hood let's first explicitly create a set of views from our ViewSets.

Методы обработчика привязываются к действиям только тогда, когда мы определяем URLConf. Чтобы увидеть, что происходит под капотом, давайте сначала явно создадим набор представлений из наших ViewSet.

In the `snippets/urls.py` file we bind our `ViewSet` classes into a set of concrete views.

В файле `snippets/urls.py` мы связываем наши классы `ViewSet` в набор конкретных представлений.

```
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

Notice how we're creating multiple views from each `ViewSet` class, by binding the HTTP methods to the required action for each view.

Обратите внимание, как мы создаем несколько представлений из каждого класса `ViewSet`, связывая методы HTTP с необходимым действием для каждого представления.

Now that we've bound our resources into concrete views, we can register the views with the URL conf as usual.

Теперь, когда мы связали наши ресурсы в конкретные представления, мы можем зарегистрировать представления с помощью URL conf, как обычно.

```
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
```

## Using Routers

## Использование маршрутизаторов

Because we're using `ViewSet` classes rather than `View` classes, we actually don't need to design the URL conf ourselves. The conventions for wiring up resources into views and urls can be handled automatically, using a `Router` class. All we need to do is register the appropriate view sets with a router, and let it do the rest.

Поскольку мы используем классы `ViewSet`, а не `View`, нам не нужно самим разрабатывать URL conf. Соглашения о соединении ресурсов в представления и урлы могут быть обработаны автоматически, с помощью класса `Router`. Все, что нам нужно сделать, это зарегистрировать соответствующие наборы представлений в маршрутизаторе, и пусть он сделает все остальное.

Here's our re-wired `snippets/urls.py` file.

Вот наш переделанный файл `snippets/urls.py`.

```
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

Registering the ViewSets with the router is similar to providing a urlpattern. We include two arguments - the URL prefix for the views, and the view set itself.

Регистрация наборов представлений в маршрутизаторе аналогична предоставлению шаблона url. Мы включаем два аргумента - префикс URL для представлений и сам набор представлений.

The `DefaultRouter` class we're using also automatically creates the API root view for us, so we can now delete the `api_root` function from our `views` module.

Класс `DefaultRouter`, который мы используем, также автоматически создает для нас корневое представление API, поэтому мы можем удалить функцию `api_root` из нашего модуля `views`.

## Trade-offs between views vs ViewSets

## Компромиссы между представлениями и наборами представлений

Using ViewSets can be a really useful abstraction. It helps ensure that URL conventions will be consistent across your API, minimizes the amount of code you need to write, and allows you to concentrate on the interactions and representations your API provides rather than the specifics of the URL conf.

Использование ViewSets может быть действительно полезной абстракцией. Она помогает обеспечить согласованность соглашений URL в вашем API, минимизирует объем кода, который вам нужно написать, и позволяет вам сосредоточиться на взаимодействии и представлениях, которые предоставляет ваш API, а не на специфике URL conf.

That doesn't mean it's always the right approach to take. There's a similar set of trade-offs to consider as when using class-based views instead of function-based views. Using ViewSets is less explicit than building your API views individually.

Но это не значит, что такой подход всегда правильный. Существует аналогичный набор компромиссов, которые необходимо учитывать при использовании представлений на основе классов вместо представлений на основе функций. Использование наборов представлений менее очевидно, чем создание представлений API по отдельности.