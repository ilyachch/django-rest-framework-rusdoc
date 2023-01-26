<!-- TRANSLATED by md-translate -->
# Tutorial 5: Relationships & Hyperlinked APIs

# Учебник 5: Отношения и API с гиперссылками

At the moment relationships within our API are represented by using primary keys. In this part of the tutorial we'll improve the cohesion and discoverability of our API, by instead using hyperlinking for relationships.

В настоящее время отношения в нашем API представлены с помощью первичных ключей. В этой части учебника мы улучшим связность и открываемость нашего API, используя вместо этого гиперссылки для отношений.

## Creating an endpoint for the root of our API

## Создание конечной точки для корня нашего API

Right now we have endpoints for 'snippets' and 'users', but we don't have a single entry point to our API. To create one, we'll use a regular function-based view and the `@api_view` decorator we introduced earlier. In your `snippets/views.py` add:

Сейчас у нас есть конечные точки для "сниппетов" и "пользователей", но у нас нет единой точки входа в наш API. Чтобы создать ее, мы воспользуемся обычным представлением на основе функций и декоратором `@api_view`, который мы представили ранее. В вашем `snippets/views.py` добавьте:

```
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

Two things should be noticed here. First, we're using REST framework's `reverse` function in order to return fully-qualified URLs; second, URL patterns are identified by convenience names that we will declare later on in our `snippets/urls.py`.

Здесь следует отметить два момента. Во-первых, мы используем функцию `reverse` фреймворка REST, чтобы вернуть полностью квалифицированные URL; во-вторых, шаблоны URL идентифицируются удобными именами, которые мы объявим позже в нашем `snippets/urls.py`.

## Creating an endpoint for the highlighted snippets

## Создание конечной точки для выделенных фрагментов

The other obvious thing that's still missing from our pastebin API is the code highlighting endpoints.

Другая очевидная вещь, которой все еще не хватает в нашем API pastebin, - это конечные точки подсветки кода.

Unlike all our other API endpoints, we don't want to use JSON, but instead just present an HTML representation. There are two styles of HTML renderer provided by REST framework, one for dealing with HTML rendered using templates, the other for dealing with pre-rendered HTML. The second renderer is the one we'd like to use for this endpoint.

В отличие от всех других конечных точек API, мы не хотим использовать JSON, а вместо этого просто представим HTML-представление. Существует два стиля рендеринга HTML, предоставляемых REST framework: один для работы с HTML, созданным с помощью шаблонов, другой для работы с предварительно созданным HTML. Для этой конечной точки мы хотим использовать второй рендерер.

The other thing we need to consider when creating the code highlight view is that there's no existing concrete generic view that we can use. We're not returning an object instance, but instead a property of an object instance.

Другая вещь, которую мы должны учитывать при создании представления подсветки кода, заключается в том, что нет существующего конкретного общего представления, которое мы могли бы использовать. Мы возвращаем не экземпляр объекта, а свойство экземпляра объекта.

Instead of using a concrete generic view, we'll use the base class for representing instances, and create our own `.get()` method. In your `snippets/views.py` add:

Вместо того чтобы использовать конкретное общее представление, мы будем использовать базовый класс для представления экземпляров и создадим свой собственный метод `.get()`. В вашем `snippets/views.py` добавьте:

```
from rest_framework import renderers

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```

As usual we need to add the new views that we've created in to our URLconf. We'll add a url pattern for our new API root in `snippets/urls.py`:

Как обычно, нам нужно добавить новые представления, которые мы создали, в нашу URLconf. Мы добавим шаблон url для нашего нового корня API в `snippets/urls.py`:

```
path('', views.api_root),
```

And then add a url pattern for the snippet highlights:

А затем добавьте шаблон url для выделения фрагментов:

```
path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
```

## Hyperlinking our API

## Гиперссылка на наш API

Dealing with relationships between entities is one of the more challenging aspects of Web API design. There are a number of different ways that we might choose to represent a relationship:

Работа с отношениями между сущностями - один из самых сложных аспектов разработки Web API. Существует множество различных способов, которые мы можем выбрать для представления отношений:

* Using primary keys.
* Using hyperlinking between entities.
* Using a unique identifying slug field on the related entity.
* Using the default string representation of the related entity.
* Nesting the related entity inside the parent representation.
* Some other custom representation.

* Использование первичных ключей.
* Использование гиперссылок между сущностями.
* Использование уникального идентифицирующего поля slug в связанной сущности.
* Использование стандартного строкового представления связанной сущности.
* Вложение связанной сущности в родительское представление.
* Другое пользовательское представление.

REST framework supports all of these styles, and can apply them across forward or reverse relationships, or apply them across custom managers such as generic foreign keys.

Структура REST поддерживает все эти стили и может применять их к прямым или обратным отношениям, или применять их к пользовательским менеджерам, таким как общие внешние ключи.

In this case we'd like to use a hyperlinked style between entities. In order to do so, we'll modify our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.

В данном случае мы хотели бы использовать стиль гиперссылки между сущностями. Для этого мы изменим наши сериализаторы, чтобы расширить `HyperlinkedModelSerializer` вместо существующего `ModelSerializer`.

The `HyperlinkedModelSerializer` has the following differences from `ModelSerializer`:

`HyperlinkedModelSerializer` имеет следующие отличия от `ModelSerializer`:

* It does not include the `id` field by default.
* It includes a `url` field, using `HyperlinkedIdentityField`.
* Relationships use `HyperlinkedRelatedField`, instead of `PrimaryKeyRelatedField`.

* По умолчанию он не включает поле `id`.
* Оно включает поле `url`, используя `HyperlinkedIdentityField`.
* Отношения используют `HyperlinkedRelatedField`, вместо `PrimaryKeyRelatedField`.

We can easily re-write our existing serializers to use hyperlinking. In your `snippets/serializers.py` add:

Мы можем легко переписать наши существующие сериализаторы для использования гиперссылок. В вашем `snippets/serializers.py` добавьте:

```
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

Notice that we've also added a new `'highlight'` field. This field is of the same type as the `url` field, except that it points to the `'snippet-highlight'` url pattern, instead of the `'snippet-detail'` url pattern.

Обратите внимание, что мы также добавили новое поле `'highlight''. Это поле того же типа, что и поле `url`, за исключением того, что оно указывает на шаблон url `'snippet-highlight'`, а не на шаблон url `'snippet-detail'`.

Because we've included format suffixed URLs such as `'.json'`, we also need to indicate on the `highlight` field that any format suffixed hyperlinks it returns should use the `'.html'` suffix.

Поскольку мы включили URL с суффиксом формата, например, ``.json``, нам также необходимо указать полю ``highlight``, что все гиперссылки с суффиксом формата, которые оно возвращает, должны использовать суффикс ``.html``.

## Making sure our URL patterns are named

## Убедитесь, что наши шаблоны URL названы

If we're going to have a hyperlinked API, we need to make sure we name our URL patterns. Let's take a look at which URL patterns we need to name.

Если мы собираемся иметь API с гиперссылками, нам нужно убедиться, что мы назвали наши шаблоны URL. Давайте рассмотрим, какие шаблоны URL нам нужно назвать.

* The root of our API refers to `'user-list'` and `'snippet-list'`.
* Our snippet serializer includes a field that refers to `'snippet-highlight'`.
* Our user serializer includes a field that refers to `'snippet-detail'`.
* Our snippet and user serializers include `'url'` fields that by default will refer to `'{model_name}-detail'`, which in this case will be `'snippet-detail'` and `'user-detail'`.

* Корень нашего API ссылается на `'user-list'` и `'snippet-list'`.
* Наш сериализатор сниппетов включает поле, которое ссылается на `'snippet-highlight'`.
* Наш сериализатор пользователей включает поле, которое ссылается на `'snippet-detail'`.
* Наши сериализаторы сниппетов и пользователей включают поля `'url'`, которые по умолчанию ссылаются на `'{model_name}-detail'`, что в данном случае будет `'snippet-detail'` и `'user-detail'`.

After adding all those names into our URLconf, our final `snippets/urls.py` file should look like this:

После добавления всех этих имен в нашу URLconf, наш окончательный файл `snippets/urls.py` должен выглядеть следующим образом:

```
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

## Adding pagination

## Добавление пагинации

The list views for users and code snippets could end up returning quite a lot of instances, so really we'd like to make sure we paginate the results, and allow the API client to step through each of the individual pages.

Представления списка для пользователей и фрагментов кода могут в конечном итоге возвращать довольно много экземпляров, поэтому на самом деле мы хотели бы убедиться, что мы постранично отображаем результаты, и позволить клиенту API пройтись по каждой отдельной странице.

We can change the default list style to use pagination, by modifying our `tutorial/settings.py` file slightly. Add the following setting:

Мы можем изменить стиль списка по умолчанию на использование пагинации, слегка изменив наш файл `tutorial/settings.py`. Добавьте следующую настройку:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Note that settings in REST framework are all namespaced into a single dictionary setting, named `REST_FRAMEWORK`, which helps keep them well separated from your other project settings.

Обратите внимание, что все настройки REST framework разнесены по именам в один словарь с именем `REST_FRAMEWORK`, что позволяет отделить их от других настроек проекта.

We could also customize the pagination style if we needed to, but in this case we'll just stick with the default.

При необходимости мы также можем настроить стиль пагинации, но в данном случае мы будем придерживаться стиля по умолчанию.

## Browsing the API

## Просмотр API

If we open a browser and navigate to the browsable API, you'll find that you can now work your way around the API simply by following links.

Если мы откроем браузер и перейдем к API с возможностью просмотра, вы увидите, что теперь вы можете работать с API, просто переходя по ссылкам.

You'll also be able to see the 'highlight' links on the snippet instances, that will take you to the highlighted code HTML representations.

Вы также сможете увидеть ссылки "highlight" на экземплярах сниппетов, которые приведут вас к HTML-представлениям выделенного кода.

In [part 6](6-viewsets-and-routers.md) of the tutorial we'll look at how we can use ViewSets and Routers to reduce the amount of code we need to build our API.

В [части 6](6-viewsets-and-routers.md) учебника мы рассмотрим, как мы можем использовать ViewSets и Routers для уменьшения количества кода, необходимого для создания нашего API.