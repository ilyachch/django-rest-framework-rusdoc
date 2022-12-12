<!-- TRANSLATED by md-translate -->
# Tutorial 6: ViewSets & Routers

# Учебное пособие 6: виды и маршрутизаторы

REST framework includes an abstraction for dealing with `ViewSets`, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

Структура REST включает в себя абстракцию для борьбы с «видами», которая позволяет разработчику сосредоточиться на моделировании состояния и взаимодействия API и оставляет обработку URL -конструкции автоматически, основываясь на общих конвенциях.

`ViewSet` classes are almost the same thing as `View` classes, except that they provide operations such as `retrieve`, or `update`, and not method handlers such as `get` or `put`.

‘Классы Viewset` почти то же самое, что и классы` view ', за исключением того, что они предоставляют такие операции, как «reture», или «Обновление», а не обработчики методов, такие как «get» или «put».

A `ViewSet` class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a `Router` class which handles the complexities of defining the URL conf for you.

Класс `ViewSet` связан только с набором обработчиков метода в последний момент, когда он создается в набор представления, обычно с использованием класса« маршрутизатор », который обрабатывает сложности определения конфуза URL для вас.

## Refactoring to use ViewSets

## Рефакторинг использования видах.

Let's take our current set of views, and refactor them into view sets.

Давайте возьмем наш текущий набор просмотров и рефактируем их в виде наборов.

First of all let's refactor our `UserList` and `UserDetail` views into a single `UserViewSet`.  We can remove the two views, and replace them with a single class:

Прежде всего, давайте рефактируем наши представления `userlist` и` userdetail
Мы можем удалить два представления и заменить их одним классом:

```
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```


Here we've used the `ReadOnlyModelViewSet` class to automatically provide the default 'read-only' operations.  We're still setting the `queryset` and `serializer_class` attributes exactly as we did when we were using regular views, but we no longer need to provide the same information to two separate classes.

Здесь мы использовали класс `readonlymodelviewset` для автоматического предоставления операций по умолчанию« только для чтения ».
Мы по -прежнему устанавливаем атрибуты `Queryset` и` serializer_class` точно так же, как мы делали, когда использовали обычные представления, но нам больше не нужно предоставлять одну и ту же информацию для двух отдельных классов.

Next we're going to replace the `SnippetList`, `SnippetDetail` and `SnippetHighlight` view classes.  We can remove the three views, and again replace them with a single class.

Далее мы собираемся заменить классы SnippetList`, `SnippetDetail` и` snippethighlight '.
Мы можем удалить три представления и снова заменить их одним классом.

```
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
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

На этот раз мы использовали класс «ModelViewSet», чтобы получить полный набор операций чтения и записи по умолчанию.

Notice that we've also used the `@action` decorator to create a custom action, named `highlight`.  This decorator can be used to add any custom endpoints that don't fit into the standard `create`/`update`/`delete` style.

Обратите внимание, что мы также использовали декоратор `@Action` для создания пользовательского действия с именем` highting '.
Этот декоратор можно использовать для добавления любых пользовательских конечных точек, которые не вписываются в стандартный стиль `create`/` invembent`/`delete`.

Custom actions which use the `@action` decorator will respond to `GET` requests by default.  We can use the `methods` argument if we wanted an action that responded to `POST` requests.

Пользовательские действия, которые используют декоратор `@action`, будут отвечать на запросы` get` по умолчанию.
Мы можем использовать аргумент «Методы», если мы хотели действие, которое ответило на запросы «post».

The URLs for custom actions by default depend on the method name itself. If you want to change the way url should be constructed, you can include `url_path` as a decorator keyword argument.

URL -адреса для пользовательских действий по умолчанию зависят от самого имени метода.
Если вы хотите изменить способ, которым должен быть построен URL -адрес, вы можете включить `url_path` как аргумент ключевого слова декоратора.

## Binding ViewSets to URLs explicitly

## Переплет виды с URL -адресами явно

The handler methods only get bound to the actions when we define the URLConf.
To see what's going on under the hood let's first explicitly create a set of views from our ViewSets.

Методы обработчика связаны только с действиями только тогда, когда мы определяем URLConf.
Чтобы увидеть, что происходит под капюшоном, давайте сначала явно создадим набор просмотров из наших видов.

In the `snippets/urls.py` file we bind our `ViewSet` classes into a set of concrete views.

В файле `Snippets/urls.py` мы связываем наши классы` viewset` в набор конкретных представлений.

```
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

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


Notice how we're creating multiple views from each `ViewSet` class, by binding the http methods to the required action for each view.

Обратите внимание, как мы создаем несколько представлений из каждого класса `viewset`, связывая методы HTTP с необходимым действием для каждого представления.

Now that we've bound our resources into concrete views, we can register the views with the URL conf as usual.

Теперь, когда мы связали наши ресурсы с конкретными видами, мы можем зарегистрировать представления с URL Conf, как обычно.

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

Because we're using `ViewSet` classes rather than `View` classes, we actually don't need to design the URL conf ourselves.  The conventions for wiring up resources into views and urls can be handled automatically, using a `Router` class.  All we need to do is register the appropriate view sets with a router, and let it do the rest.

Поскольку мы используем классы `viewset`, а не классы« View », нам на самом деле не нужно разрабатывать сами URL Conf.
Конвенции для подключения ресурсов в представления и URL -адреса могут быть обработаны автоматически, используя класс «маршрутизатора».
Все, что нам нужно сделать, это зарегистрировать соответствующие наборы представлений с помощью маршрутизатора, а остальное сделает все остальное.

Here's our re-wired `snippets/urls.py` file.

Вот наш переосмысленный файл `Snippets/urls.py`.

```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet,basename="snippet")
router.register(r'users', views.UserViewSet,basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
```


Registering the viewsets with the router is similar to providing a urlpattern.  We include two arguments - the URL prefix for the views, and the viewset itself.

Регистрация просмотров с помощью маршрутизатора аналогична предоставлению urlpattern.
Мы включаем два аргумента - префикс URL для представлений, и сам обзор.

The `DefaultRouter` class we're using also automatically creates the API root view for us, so we can now delete the `api_root` method from our `views` module.

Класс `defaultrouter, который мы используем, также автоматически создает для нас представление API, поэтому мы можем теперь удалить метод` api_root` из нашего модуля `siews`.

## Trade-offs between views vs viewsets

## компромиссы между просмотрами и видами.

Using viewsets can be a really useful abstraction.  It helps ensure that URL conventions will be consistent across your API, minimizes the amount of code you need to write, and allows you to concentrate on the interactions and representations your API provides rather than the specifics of the URL conf.

Использование видов может быть действительно полезной абстракцией.
Это помогает гарантировать, что URL -конвенции будут согласованы по вашему API, сводят к минимуму количество кода, необходимого для написания, и позволяет вам сосредоточиться на взаимодействиях и представлениях, которые предоставляет ваш API, а не на специфику URL Conf.

That doesn't mean it's always the right approach to take.  There's a similar set of trade-offs to consider as when using class-based views instead of function based views.  Using viewsets is less explicit than building your views individually.

Это не значит, что это всегда правильный подход.
Существует аналогичный набор компромиссов, которые следует учитывать, как при использовании представлений на основе классов вместо представлений на основе функций.
Использование видов менее четко, чем создание ваших взглядов индивидуально.
