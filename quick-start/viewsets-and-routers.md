# Урок 6: наборы представлений и маршрутизаторы

DRF включает в себя абстракцию для работы с наборами представлений(`ViewSets`), которая позволяет разработчику сконцентрироваться на моделировании состояния и взимодействии с API, а URL адреса сформировать автоматически, основываясь на общих соглашениях.

Наборы представлений - почти то же самое, что и классы представлений, только предоставляют они операции, такие как чтение или обновление, а не методы, такие как `GET` или `PUT`.

Класс набора представлений привязывается к обработчикам методов в момент создания и превращения в множество представлений, что обычно происходит в момент, когда класс `Router` обрабатывает и создает конфигурацию URL-ов для вас.
<!--A ViewSet class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a Router class which handles the complexities of defining the URL conf for you.-->

## Изменение для использования наборов представлений

Давайте возьмем наше множество представлений и переделаем их в набор представлений.

Для начала, давайте переделаем наши классы `UserList` и `UserDetail` в один `UserViewSet`. Мы можем убрать два представления и заменить их одним классом:

```python
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот набор представлений автоматически создает действия `list` и `detail`.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Здесь мы использовали класс `ReadOnlyModelViewSet` для обеспечения операций только на чтение. Мы по прежнему указываем запрос(`queryset`) и класс сериализатора, точно так же, как когда писали обычные предславления, но нам больше нет необходимости дублировать эту информацию в двух разных классах.

Теперь мы собираемся заменить классы `SnippetList`, `SnippetDetail` и `SnippetHighlight`. Мы можем убрать три представления и заменить их одним классом.

```python
from rest_framework.decorators import detail_route

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

На этот раз мы использовали класс `ModelViewSet` для того, чтобы получить набор стандартных операций чтения и записи.

Обратите внимание, что мы использовали декоратор `@detail_route`, чтобы создать собственную операцию, названную `highlight`. Этот декоратор используется для того, чтобы создать собственные конечные точки, которых нет среди стандартных операций создания/обновления/удаления.

Собственные действия, которые используют декоратор `@detail_route`, по умолчанию обрабатывают `GET` запрос. Мы можем использовать аргумент метода, если хотим, чтобы действие обрабатывало `POST` запросы.

URL адреса для собственных действий по умолчанию зависят от названия метода. Если вы хотите изменить правило, как URL должен быть создан, вы можете включить `url_path` как именованый аргумент декоратора.

## Явное связывание наборов представлений и URL адресов

Методы обработчика связываются с действиями когда мы определяем конфигурацию URL. Чтобы увидеть, что происходит под капотом, давайте сначала явно создадим множество представлений из нашего набора представлений(`ViewSet`).

В `snippet/urls.py` мы связываем наши классы `ViewSet` в множество конкретных представлений.

```python
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

Заметьте, как мы создаем множественные представления для каждого класса `ViewSet`, связывая методы с требуемыми действиями для каждого представления.

Теперь, связав наши ресурсы в конкретными представлениями, мы можем зарегистрировать их в конфигурации URL, как обычно.

```python
urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
])
```

## Используя маршрутизаторы

Поскольку мы используем наборы представлений(`ViewSet`), а не обычные представления-классы, мы, ыообще-то, можем не проектировать конфигурацию URL. Вся конфигурация может быть создана автоматически, используя класс `Router`. Все, что нам нужно, это зарегистрировать наборы форм с префиксом, остальное маршрутизатор сделаем сам за нас.

Вот наш новый, переписанный файл `snippets/urls.py`:

```python
from django.conf.urls import url, include
from snippets import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Регистрация наборов представлений в маршрутизаторе идентична созданию шаблонов URL адресов. Мы включаем два аргумента - URL префикс и, собственно, набор представлений.

Класс `DefaultRouter`, который мы используем, автоматически создает корень API, так что мы можем удалить метод `api_root` из модуля представлений.


## Компромис между представлениями и наборами представлений

Использование наборов представлений может быть очень полезной абстракцией. Это позволяет быть уверенным в том, что принцип построения API будет одинаков для всего вашего API, уменьшает количество необходимого кода и позволяет сконцентрироваться взаимодействии и представлении данных, а не на специфике конфигурации URL.

Однако, это не означает, что это всегда правильно. Бывают ситуации, когда использование представлений-функций более оправдано, чем использование представлений-классов. Так и с наборами представлений. Их использование менее явно, чем создание каждого отдельного представления.

В [уроке 7](schemas-and-client-libs.md) данного руководства мы посмотрим на то, как мы можем добавить схему API и взаимодействовать с API, используя клиентские библиотеки или командную строку.
