# Tutorial 5: Relationships & Hyperlinked APIs

# Учебное пособие 5: Отношения и гиперссыщенные API

At the moment relationships within our API are represented by using primary keys.  In this part of the tutorial we'll improve the cohesion and discoverability of our API, by instead using hyperlinking for relationships.

На данный момент отношения в нашем API представлены с использованием первичных ключей.
В этой части учебника мы улучшаем сплоченность и обнаружение нашего API, вместо этого используя гиперлизму для отношений.

## Creating an endpoint for the root of our API

## Создание конечной точки для корня нашего API

Right now we have endpoints for 'snippets' and 'users', but we don't have a single entry point to our API.  To create one, we'll use a regular function-based view and the `@api_view` decorator we introduced earlier. In your `snippets/views.py` add:

Прямо сейчас у нас есть конечные точки для «фрагментов» и «пользователей», но у нас нет ни одной точки входа в наш API.
Чтобы создать один, мы будем использовать обычный представление на основе функций и декоратор `@api_view`, который мы представили ранее.
В ваших фрагментах/views.py` добавить:

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

Здесь следует заметить две вещи.
Во-первых, мы используем функцию REST Framework `обратно ', чтобы вернуть полностью квалифицированные URL-адреса;
Во -вторых, шаблоны URL идентифицируются по именам удобства, которые мы будем объявлять позже в наших фрагментах/urls.py.

## Creating an endpoint for the highlighted snippets

## Создание конечной точки для выделенных фрагментов

The other obvious thing that's still missing from our pastebin API is the code highlighting endpoints.

Другая очевидная вещь, которая все еще отсутствует в нашем API Pastebin, - это код, выделяющий конечные точки.

Unlike all our other API endpoints, we don't want to use JSON, but instead just present an HTML representation.  There are two styles of HTML renderer provided by REST framework, one for dealing with HTML rendered using templates, the other for dealing with pre-rendered HTML.  The second renderer is the one we'd like to use for this endpoint.

В отличие от всех других наших конечных точек API, мы не хотим использовать JSON, а вместо этого просто представляем HTML -представление.
Существует два стиля HTML-рендеринга, предоставленных Framework REST, один для работы с HTML-рендерингом с использованием шаблонов, другой для работы с предварительно предопределенным HTML.
Второй визуализатор - это тот, который мы хотели бы использовать для этой конечной точки.

The other thing we need to consider when creating the code highlight view is that there's no existing concrete generic view that we can use.  We're not returning an object instance, but instead a property of an object instance.

Другая вещь, которую мы должны рассмотреть при создании представления о выдвижении кода, заключается в том, что нет существующего конкретного общего представления, которое мы можем использовать.
Мы не возвращаем экземпляр объекта, а в свойство экземпляра объекта.

Instead of using a concrete generic view, we'll use the base class for representing instances, and create our own `.get()` method.  In your `snippets/views.py` add:

Вместо того, чтобы использовать конкретный общий вид, мы будем использовать базовый класс для представления экземпляров и создать наш собственный метод `.get ()`.
В ваших фрагментах/views.py` добавить:

```
from rest_framework import renderers

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
```


As usual we need to add the new views that we've created in to our URLconf.
We'll add a url pattern for our new API root in `snippets/urls.py`:

Как обычно, нам нужно добавить новые представления, которые мы создали в наш URLConf.
Мы добавим шаблон URL для нашего нового корня API в `Snippets/urls.py`:

```
path('', views.api_root),
```


And then add a url pattern for the snippet highlights:

А затем добавьте шаблон URL для фрагмента.

```
path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
```


## Hyperlinking our API

## Гиперсвязывание нашего API

Dealing with relationships between entities is one of the more challenging aspects of Web API design.  There are a number of different ways that we might choose to represent a relationship:

Работа с отношениями между сущностями является одним из наиболее сложных аспектов дизайна веб -API.
Есть ряд различных способов, которыми мы могли бы представлять отношения:

* Using primary keys.
* Using hyperlinking between entities.
* Using a unique identifying slug field on the related entity.
* Using the default string representation of the related entity.
* Nesting the related entity inside the parent representation.
* Some other custom representation.

* Использование первичных ключей.
* Использование гиперлизации между сущностями.
* Использование уникального идентифицирующего поля слизняка на смежной сущности.
* Использование представления строки по умолчанию соответствующей сущности.
* Вложение связанной сущности внутри родительского представления.
* Некоторое другое пользовательское представление.

REST framework supports all of these styles, and can apply them across forward or reverse relationships, or apply them across custom managers such as generic foreign keys.

Структура REST поддерживает все эти стили и может применять их через форвардные или обратные отношения или применять их для пользовательских менеджеров, таких как общие иностранные ключи.

In this case we'd like to use a hyperlinked style between entities.  In order to do so, we'll modify our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.

В этом случае мы хотели бы использовать гиперссывленный стиль между сущностями.
Для этого мы изменим наши сериалы, чтобы расширить `HyperlinkedModelserializer` вместо существующего` modelerializer '.

The `HyperlinkedModelSerializer` has the following differences from `ModelSerializer`:

`‘ HyperlinkedModelserializer` имеет следующие отличия от `modelerializer`:

* It does not include the `id` field by default.
* It includes a `url` field, using `HyperlinkedIdentityField`.
* Relationships use `HyperlinkedRelatedField`,
instead of `PrimaryKeyRelatedField`.

* Он не включает поле `id` по умолчанию.
* Он включает в себя полю `url` с использованием` hyperlinkedidentityfield`.
* Отношения используют `HyperlinkedRelatedField`,
Вместо «первичного Keyrelated».

We can easily re-write our existing serializers to use hyperlinking. In your `snippets/serializers.py` add:

Мы можем легко переписать наши существующие сериалы, чтобы использовать гиперлиз.
В ваших фрагментах/serializers.py` add:

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


Notice that we've also added a new `'highlight'` field.  This field is of the same type as the `url` field, except that it points to the `'snippet-highlight'` url pattern, instead of the `'snippet-detail'` url pattern.

Обратите внимание, что мы также добавили новое поле «Выделка».
Это поле имеет тот же тип, что и поле «URL», за исключением того, что оно указывает на URL-шаблон «фрагментов», вместо шаблона URL-адреса «фрагмент».

Because we've included format suffixed URLs such as `'.json'`, we also need to indicate on the `highlight` field that any format suffixed hyperlinks it returns should use the `'.html'` suffix.

Поскольку мы включили в суффиксы формата, такие как «» .json'`, мы также должны указать в поле `highting ', что любой формат суффикса, который он возвращает, должен использовать суффикс`' .html'`.

## Making sure our URL patterns are named

## Убедитесь, что наши шаблоны URL названы

If we're going to have a hyperlinked API, we need to make sure we name our URL patterns.  Let's take a look at which URL patterns we need to name.

Если у нас будет гиперссылка API, мы должны убедиться, что мы назваем наши шаблоны URL.
Давайте посмотрим, какие шаблоны URL мы должны назвать.

* The root of our API refers to `'user-list'` and `'snippet-list'`.
* Our snippet serializer includes a field that refers to `'snippet-highlight'`.
* Our user serializer includes a field that refers to `'snippet-detail'`.
* Our snippet and user serializers include `'url'` fields that by default will refer to `'{model_name}-detail'`, which in this case will be `'snippet-detail'` and `'user-detail'`.

* Корень нашего API относится к «пользовательскому списку» и «спине фрагмента».
* Наш фрагмент сериализатора включает в себя поле, которое относится к «фрагменту фрагмента».
* Наш пользовательский сериализатор включает в себя поле, которое относится к «фрагменту-детополосовой».
* Наши фрагменты и сериализаторы пользователей включают в себя поля «url'`», которые по умолчанию будут ссылаться на `'{model_name} -detail'', что в данном случае будет« фрагментной detail »и` '' user-detail '
Анкет

After adding all those names into our URLconf, our final `snippets/urls.py` file should look like this:

После добавления всех этих имен в наш UrlConf наш последний файл `Snippets/urls.py` должен выглядеть следующим образом:

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

## Добавление страниц

The list views for users and code snippets could end up returning quite a lot of instances, so really we'd like to make sure we paginate the results, and allow the API client to step through each of the individual pages.

Просмотры списков для пользователей и фрагментов кода могут в конечном итоге вернуть довольно много случаев, поэтому мы действительно хотели бы убедиться, что мы нанесли стравные результаты, и позволить клиенту API пройти через каждую из отдельных страниц.

We can change the default list style to use pagination, by modifying our `tutorial/settings.py` file slightly. Add the following setting:

Мы можем изменить стиль списка по умолчанию на использование страниц, слегка изменяя наш файл `turnial/settings.py`.
Добавьте следующую настройку:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```


Note that settings in REST framework are all namespaced into a single dictionary setting, named `REST_FRAMEWORK`, which helps keep them well separated from your other project settings.

Обратите внимание, что настройки в структуре REST расположены все имена в одну настройку словаря, названная `REST_FRAMEWORK`, что помогает им хорошо отделить от других настроек вашего проекта.

We could also customize the pagination style if we needed to, but in this case we'll just stick with the default.

Мы также могли бы настроить стиль страниц, если нам нужно, но в этом случае мы просто придерживаемся по умолчанию.

## Browsing the API

## Просмотр API

If we open a browser and navigate to the browsable API, you'll find that you can now work your way around the API simply by following links.

Если мы откроем браузер и перейдем к API, который можно просматривать, вы обнаружите, что теперь вы сможете пройти путь по API, просто следуя ссылкам.

You'll also be able to see the 'highlight' links on the snippet instances, that will take you to the highlighted code HTML representations.

Вы также сможете увидеть ссылки «выделения» на экземплярах фрагмента, которые приведут вас к выделенному коду HTML -представлениям.

In [part 6](6-viewsets-and-routers.md) of the tutorial we'll look at how we can use ViewSets and Routers to reduce the amount of code we need to build our API.

В [Часть 6] (6-й визит и routers.md) учебника мы рассмотрим, как мы можем использовать виды и маршрутизаторы, чтобы уменьшить количество кода, необходимого для создания нашего API.