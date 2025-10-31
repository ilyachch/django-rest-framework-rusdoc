<!-- TRANSLATED by md-translate -->
# Урок 5: Отношения и API с гиперссылками

В настоящее время отношения в нашем API представлены с помощью первичных ключей. В этой части учебника мы улучшим связность и наглядность нашего API, используя вместо этого гиперссылки для отношений.

## Создание конечной точки для корня нашего API

Сейчас у нас есть конечные точки для "сниппетов" и "пользователей", но у нас нет единой точки входа в наш API. Чтобы создать ее, мы воспользуемся обычным представлением на основе функций и декоратором `@api_view`, который мы представили ранее. В вашем `snippets/views.py` добавьте:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format)
        }
    )
```

Здесь следует отметить два момента. Во-первых, мы используем функцию DRF `reverse`, чтобы вернуть полностью квалифицированные URL; во-вторых, шаблоны URL идентифицируются удобными именами, которые мы объявим позже в нашем `snippets/urls.py`.

## Создание конечной точки для подсвеченных фрагментов

Другая очевидная вещь, которой все еще не хватает в нашем API pastebin, — это конечные точки подсветки кода.

В отличие от всех других конечных точек API, мы не хотим использовать JSON, а вместо этого просто представим HTML-представление. Существует два способа рендеринга HTML, предоставляемых DRF: один для работы с HTML, созданным с помощью шаблонов, другой для работы с предварительно созданным HTML. Для этой конечной точки мы хотим использовать второй рендерер.

Другая вещь, которую мы должны учитывать при создании представления подсветки кода, заключается в том, что нет существующего конкретного общего представления, которое мы могли бы использовать. Мы возвращаем не экземпляр объекта, а свойство экземпляра объекта.

Вместо того чтобы использовать конкретное общее представление, мы будем использовать базовый класс для представления экземпляров и создадим свой собственный метод `.get()`. В вашем `snippets/views.py` добавьте:

```python
from rest_framework import renderers

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```

Как обычно, нам нужно добавить новые представления, которые мы создали, в наш URLconf. Мы добавим шаблон url для нашего нового корня API в `snippets/urls.py`:

```python
path('', views.api_root),
```

А затем добавьте шаблон url для выделения фрагмента:

```python
path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
```

## Гиперссылка на наш API

Работа с отношениями между сущностями - один из самых сложных аспектов разработки Web API. Существует множество различных способов, которые мы можем выбрать для отображения отношений:

* Использование первичных ключей.
* Использование гиперссылок между сущностями.
* Использование уникального идентифицирующего поля slug в связанной сущности.
* Использование стандартного строкового представления связанной сущности.
* Вложение связанной сущности в родительское представление.
* Другое пользовательское представление.

DRF поддерживает все эти стили и может применять их к прямым или обратным отношениям, или применять их к пользовательским менеджерам, таким как общие внешние ключи.

В данном случае мы хотели бы использовать гиперссылки между сущностями. Для этого мы изменим наши сериализаторы, чтобы расширить `HyperlinkedModelSerializer` вместо существующего `ModelSerializer`.

`HyperlinkedModelSerializer` имеет следующие отличия от `ModelSerializer`:

* По умолчанию он не включает поле `id`.
* Он включает поле `url`, используя `HyperlinkedIdentityField`.
* Отношения используют `HyperlinkedRelatedField`, вместо `PrimaryKeyRelatedField`.

Мы можем легко переписать наши существующие сериализаторы для использования гиперссылок. В вашем `snippets/serializers.py` добавьте:

```python
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = [
            'url',
            'id',
            'highlight',
            'owner',
            'title',
            'code',
            'linenos',
            'language',
            'style',
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'snippets',
        ]
```

Обратите внимание, что мы также добавили новое поле `'highlight'`. Это поле того же типа, что и поле `url`, за исключением того, что оно указывает на шаблон url `'snippet-highlight'`, а не на шаблон url `'snippet-detail'`.

Поскольку мы включили URL с суффиксом формата, например, `'.json'`, нам также необходимо указать полю `highlight`, что все гиперссылки с суффиксом формата, которые оно возвращает, должны использовать суффикс `'.html'`.

---

**Обратите внимание:**

Когда вы вручную создаете экземпляры этих сериализаторов внутри своих представлений (например, в `SnippetDetail` или `SnippetList`), вы **обязательно должны** передать `context={'request': request}`, чтобы сериализатор знал, как создавать абсолютные URL-адреса. Например, вместо:

```python
serializer = SnippetSerializer(snippet)
```

Вы должны написать:

```python
serializer = SnippetSerializer(snippet, context={'request': request})
```

Если ваше представление является подклассом `GenericAPIView`, вы можете использовать `get_serializer_context()` в качестве вспомогательного метода.

---

## Убедитесь, что наши шаблоны URL названы

Если мы собираемся иметь API с гиперссылками, нам нужно убедиться, что мы назвали наши шаблоны URL. Давайте рассмотрим, какие шаблоны URL нам нужно назвать.

* Корень нашего API ссылается на `'user-list'` и `'snippet-list'`.
* Наш сериализатор сниппетов включает поле, которое ссылается на `'snippet-highlight'`.
* Наш сериализатор пользователей включает поле, которое ссылается на `'snippet-detail'`.
* Наши сериализаторы сниппетов и пользователей включают поля `'url'`, которые по умолчанию ссылаются на `'{model_name}-detail'`, что в данном случае будет `'snippet-detail'` и `'user-detail'`.

После добавления всех этих имен в нашу URLconf, наш файл `snippets/urls.py` должен выглядеть следующим образом:

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path(
        '',
        views.api_root,
    ),
    path(
        'snippets/',
        views.SnippetList.as_view(),
        name='snippet-list',
        ),
    path(
        'snippets/<int:pk>/',
        views.SnippetDetail.as_view(),
        name='snippet-detail',
    ),
    path(
        'snippets/<int:pk>/highlight/',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight',
    ),
    path(
        'users/',
        views.UserList.as_view(),
        name='user-list',
    ),
    path(
        'users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail',
    )
])
```

## Добавление пагинации

Представления списка для пользователей и фрагментов кода могут в конечном итоге возвращать довольно много экземпляров, поэтому на самом деле мы хотели бы убедиться, что мы постранично отображаем результаты, и позволить клиенту API пройтись по каждой отдельной странице.

Мы можем изменить тип списка по умолчанию на использование пагинации, слегка изменив наш файл `tutorial/settings.py`. Добавьте следующую настройку:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Обратите внимание, что все настройки DRF разнесены по именам в один словарь с именем `REST_FRAMEWORK`, что позволяет отделить их от других настроек проекта.

При необходимости мы также можем настроить стиль пагинации, но в данном случае мы будем придерживаться стиля по умолчанию.

## Просмотр API

Если мы откроем браузер и перейдем к API с возможностью просмотра, вы увидите, что теперь вы можете работать с API, просто переходя по ссылкам.

Вы также сможете увидеть ссылки "highlight" на экземплярах сниппетов, которые приведут вас к HTML-представлениям выделенного кода.

В [части 6](6-viewsets-and-routers.md) учебника мы рассмотрим, как мы можем использовать ViewSets и Routers для уменьшения количества кода, необходимого для создания нашего API.
