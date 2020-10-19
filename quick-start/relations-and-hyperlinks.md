# Урок 5: Отношения и ссылочные связи

На данный момент отношения в нашем API представлены первичными ключами. В этой части руководства мы улучшим связанность и наглядность нашего API, используя ссылочные связи.

## Создание корневой точки входа для API

На данный момент мы имеем точки входа для `snippets` и `users`, но у нас нет единой точки входа для API. Для ее создания мы используем обычную функцию-представление с декоратором `@api_view`, который мы видели раньше. Добавьте в `snippets/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
```

Обратите внимание на две вещи. Во-первых, мы используем функцию `reverse()` из состава DRF, чтобы вернуть полностью сформированные URL-ы. Во-вторых, шаблоны URL определены с помощью удобных имен, которые мы опишем позднее в `snippets/urls.py`.

## Создание конечной точки для подсвеченных сниппетов

Еще одна очевидная вешь для нашего API, которая не реализована - конечная точка для подсвеченного кода.

В отличие от наших других конечных точек, мы не хотим использовать здесь JSON, а, наоборот, хотим выводить HTML. Есть 2 стиля вывода HTML, реализованых в DRF: одна для рендеринга HTML, другая - для вывода предварительно срендеренного HTML. Мы будем использовать второй способ.

Следующая вещь, которую мы должны рассмотреть, когда создаем подсвеченный код - у нас нет конкретного встроенного представления, которое мы можем использовать. Мы не возвращаем экземпляр, а должны возвращать свойство объекта.

Вместо того, чтобы использовать встроенное представление, мы создадим базовый класс для представления объектов и определим собственный метод `.get()`. Добавьте в ваш `snippets/views.py`:

```python
from rest_framework import renderers
from rest_framework.response import Response

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```

Как и всегда, мы должны добавить наши новые представления в конфигурацию URL-ов. Добавьте шаблон URL-а в `snippets/urls.py`:

```python
path('', views.api_root),
```

А затем добавьте шаблон URL-адреса для выделения фрагмента:

```python
path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
```

## Связывание ссылками нашего API

Работа с отношениями между сущностями является одним из наиболее сложных аспектов проектирования API. Существует несколько разных способов, которые мы могли бы выбрать для представления отношения:

- использование первичных ключей;
- использование ссылок между сущностями;
- используя уникальные поля в связанных сущностях;
- используя стандартные строковые представления связанных сущностей;
- вкладывания связанных сущностей внутрь родительских;
- какая-то своя реализация.

DRF реализует все эти способы и может применять их как к прямым, так и к обратным связям или применять их к собственным менеджерам объектов, какие как встроенные внешние ключи.

В данном случае мы будем использовать ссылочные связи между сущностями. Для этого мы изменим наши сериализаторы, указав `HyperlinkedModelSerializer` в качестве родительского класса, вместо `ModelSerializer`.

Отличие класса `HyperlinkedModelSerializer` от класса `ModelSerializer` заключается в следующем: 

- по умолчанию он не включает в себя поле первичного ключа;
- он включае в себя поле адреса, используя `HyperlinkedIdentityField`;
- связи используют `HyperlinkedRelatedField` вместо `PrimaryKeyRelatedField`;

Мы можем просто переписать наши существующие сериализаторы для использования ссылок. Измените ваш `snippets/serializers.py`:

```python
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
```

Обратите внимание, что мы также добавили поле `highlight`. Это поле - того же типа, что и поле `url`, за исключением того, что указывает на шаблон URL `'snippet-highlight'`, вместо шаблона`'snippet-detail'`.

Поскольку мы включили указатели формата в шаблоны URL, такие как `'.json'`, нам необходимо пометить поле подсвеченного кода, как возвращающее `'.html'` в любом случае, вне зависимости от того, что было запрошено.

## Убеждаемся, что наши шаблоны URL названы

Если мы собираемся использовать ссылочно связанный API, мы должны убедиться, что шаблоны URL у нас названы. Давайте посмотрим, какие шаблоны URL мы должны назвать. Если мы собираемся иметь API с гиперссылками, нам нужно убедиться, что мы даем имена нашим шаблонам URL. Давайте посмотрим, какие шаблоны URL нам нужно назвать.

* Корень нашего API ссылается на `'user-list'` и `'snippet-list'`.
* Наш сериализатор сниппета включает поле, которое ссылается на `'snippet-highlight'`.
* Сериализатор пользователя включает поле, которое ссылается на `'snippet-detail'`.
* Наши сериализаторы сниппетов и пользователей содержат `'url'` поле, которое ссылается на `'{название_модели}-detail'`, которое, в нашем случае будет `'snippet-detail'` и `'user-detail'`.
* После добавления всех этих имен в нашу конфигурацию URL, `snippets/urls.py` должен выглядеть вот так:

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/',
        views.SnippetList.as_view(),
        name='snippet-list'),
    path('snippets/<int:pk>/',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    path('users/',
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail')
])
```

## Добавляем постраничный вывод

Представления, возвращающие список пользователей и сниппетов кода могут разростись и отдавать огромное количество объектов, поэтому, неплохо было бы включить постраничный вывод результатов и разрешить клиентам проходить по ним с помощью отдельных страниц.

Мы можем изменить стандартное поведение, изменив `settings.py`. Добавьте следующую настройку:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Помните, все настройки DRF находятся в одном словаре с названием `'REST_FRAMEWORK'`, что позволяет их отделить от остальных настроек проекта.

Так же мы можем настроить стиль постраничного вывода, но в данном случае мы воспользуемся стандартными настройками.

## Просмотр API

Если мы откроем браузер и перейдем в браузерную версию API, мы увидим, что теперь мы можем "гулять" по API, пользуясь ссылками.

Так же мы можем увидеть ссылки `'highlight'` у объектов сниппетов, которые будут возвращать вам HTML представление подсвеченного кода.

В [6 уроке](viewsets-and-routers.md) этого руководства мы посмотрим, как можно использовать наборы представлений(`ViewSets`) и матршрутизаторы (`Routers`), чтобы уменьшить количество кода, необходимого для построения API. 
