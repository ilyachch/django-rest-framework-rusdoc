<!-- TRANSLATED by md-translate -->
# Tutorial 4: Authentication & Permissions

# Учебник 4: Аутентификация и разрешения

Currently our API doesn't have any restrictions on who can edit or delete code snippets. We'd like to have some more advanced behavior in order to make sure that:

В настоящее время наш API не имеет ограничений на то, кто может редактировать или удалять фрагменты кода. Мы хотели бы иметь более продвинутое поведение, чтобы убедиться в этом:

* Code snippets are always associated with a creator.
* Only authenticated users may create snippets.
* Only the creator of a snippet may update or delete it.
* Unauthenticated requests should have full read-only access.

* Фрагменты кода всегда связаны с создателем.
* Создавать сниппеты могут только авторизованные пользователи.
* Только создатель сниппета может обновлять или удалять его.
* Неаутентифицированные запросы должны иметь полный доступ только для чтения.

## Adding information to our model

## Добавление информации в нашу модель

We're going to make a couple of changes to our `Snippet` model class. First, let's add a couple of fields. One of those fields will be used to represent the user who created the code snippet. The other field will be used to store the highlighted HTML representation of the code.

Мы собираемся внести несколько изменений в наш класс модели `Snippet`. Во-первых, добавим пару полей. Одно из этих полей будет использоваться для представления пользователя, создавшего фрагмент кода. Другое поле будет использоваться для хранения выделенного HTML-представления кода.

Add the following two fields to the `Snippet` model in `models.py`.

Добавьте следующие два поля к модели `Snippet` в `models.py`.

```
owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
highlighted = models.TextField()
```

We'd also need to make sure that when the model is saved, that we populate the highlighted field, using the `pygments` code highlighting library.

Нам также нужно убедиться, что при сохранении модели мы заполним выделенное поле, используя библиотеку подсветки кода `pygments`.

We'll need some extra imports:

Нам понадобится дополнительный импорт:

```
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
```

And now we can add a `.save()` method to our model class:

И теперь мы можем добавить метод `.save()` в наш класс модели:

```
def save(self, *args, **kwargs):
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(self.language)
    linenos = 'table' if self.linenos else False
    options = {'title': self.title} if self.title else {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super().save(*args, **kwargs)
```

When that's all done we'll need to update our database tables. Normally we'd create a database migration in order to do that, but for the purposes of this tutorial, let's just delete the database and start again.

Когда все будет готово, нам нужно будет обновить таблицы нашей базы данных. Обычно для этого мы создаем миграцию базы данных, но для целей данного руководства давайте просто удалим базу данных и начнем все сначала.

```
rm -f db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

You might also want to create a few different users, to use for testing the API. The quickest way to do this will be with the `createsuperuser` command.

Возможно, вы также захотите создать несколько разных пользователей, чтобы использовать их для тестирования API. Быстрее всего это можно сделать с помощью команды `createsuperuser`.

```
python manage.py createsuperuser
```

## Adding endpoints for our User models

## Добавление конечных точек для наших моделей User

Now that we've got some users to work with, we'd better add representations of those users to our API. Creating a new serializer is easy. In `serializers.py` add:

Теперь, когда у нас есть несколько пользователей для работы, нам лучше добавить представления этих пользователей в наш API. Создать новый сериализатор очень просто. В `serializers.py` добавьте:

```
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
```

Because `'snippets'` is a *reverse* relationship on the User model, it will not be included by default when using the `ModelSerializer` class, so we needed to add an explicit field for it.

Поскольку `'snippets'' является *обратным* отношением на модели User, оно не будет включено по умолчанию при использовании класса `ModelSerializer'', поэтому нам нужно добавить явное поле для него.

We'll also add a couple of views to `views.py`. We'd like to just use read-only views for the user representations, so we'll use the `ListAPIView` and `RetrieveAPIView` generic class-based views.

Мы также добавим пару представлений в `views.py`. Мы хотим использовать представления только для чтения для пользовательских представлений, поэтому мы будем использовать представления `ListAPIView` и `RetrieveAPIView`, основанные на общих классах.

```
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Make sure to also import the `UserSerializer` class

Не забудьте также импортировать класс `UserSerializer`.

```
from snippets.serializers import UserSerializer
```

Finally we need to add those views into the API, by referencing them from the URL conf. Add the following to the patterns in `snippets/urls.py`.

Наконец, нам нужно добавить эти представления в API, ссылаясь на них из URL conf. Добавьте следующее к шаблонам в `snippets/urls.py`.

```
path('users/', views.UserList.as_view()),
path('users/<int:pk>/', views.UserDetail.as_view()),
```

## Associating Snippets with Users

## Ассоциирование сниппетов с пользователями

Right now, if we created a code snippet, there'd be no way of associating the user that created the snippet, with the snippet instance. The user isn't sent as part of the serialized representation, but is instead a property of the incoming request.

Сейчас, если мы создаем сниппет кода, нет возможности связать пользователя, создавшего сниппет, с экземпляром сниппета. Пользователь не передается как часть сериализованного представления, а является свойством входящего запроса.

The way we deal with that is by overriding a `.perform_create()` method on our snippet views, that allows us to modify how the instance save is managed, and handle any information that is implicit in the incoming request or requested URL.

Мы решаем эту проблему путем переопределения метода `.perform_create()` в наших представлениях фрагментов, что позволяет нам изменять способ сохранения экземпляра и обрабатывать любую информацию, которая подразумевается во входящем запросе или запрашиваемом URL.

On the `SnippetList` view class, add the following method:

В классе представления `SnippetList` добавьте следующий метод:

```
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

The `create()` method of our serializer will now be passed an additional `'owner'` field, along with the validated data from the request.

Теперь методу `create()` нашего сериализатора будет передано дополнительное поле `'owner'` вместе с подтвержденными данными из запроса.

## Updating our serializer

## Обновление нашего сериализатора

Now that snippets are associated with the user that created them, let's update our `SnippetSerializer` to reflect that. Add the following field to the serializer definition in `serializers.py`:

Теперь, когда сниппеты связаны с пользователем, который их создал, давайте обновим наш `SnippetSerializer`, чтобы отразить это. Добавьте следующее поле в определение сериализатора в `serializers.py`:

```
owner = serializers.ReadOnlyField(source='owner.username')
```

**Note**: Make sure you also add `'owner',` to the list of fields in the inner `Meta` class.

**Примечание**: Убедитесь, что вы также добавили `'owner',` в список полей во внутреннем классе `Meta`.

This field is doing something quite interesting. The `source` argument controls which attribute is used to populate a field, and can point at any attribute on the serialized instance. It can also take the dotted notation shown above, in which case it will traverse the given attributes, in a similar way as it is used with Django's template language.

В этой области происходит нечто весьма интересное. Аргумент `source` управляет тем, какой атрибут используется для заполнения поля, и может указывать на любой атрибут сериализованного экземпляра. Он также может принимать точечную нотацию, показанную выше, в этом случае он будет перебирать заданные атрибуты, подобно тому, как это используется в языке шаблонов Django.

The field we've added is the untyped `ReadOnlyField` class, in contrast to the other typed fields, such as `CharField`, `BooleanField` etc... The untyped `ReadOnlyField` is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used `CharField(read_only=True)` here.

Поле, которое мы добавили, представляет собой нетипизированный класс `ReadOnlyField`, в отличие от других типизированных полей, таких как `CharField`, `BooleanField` и т.д.. Нетипизированное `ReadOnlyField` всегда только для чтения, оно будет использоваться для сериализованных представлений, но не будет использоваться для обновления экземпляров модели при их десериализации. Мы могли бы также использовать здесь `CharField(read_only=True)`.

## Adding required permissions to views

## Добавление необходимых разрешений к представлениям

Now that code snippets are associated with users, we want to make sure that only authenticated users are able to create, update and delete code snippets.

Теперь, когда фрагменты кода связаны с пользователями, мы хотим убедиться, что только аутентифицированные пользователи могут создавать, обновлять и удалять фрагменты кода.

REST framework includes a number of permission classes that we can use to restrict who can access a given view. In this case the one we're looking for is `IsAuthenticatedOrReadOnly`, which will ensure that authenticated requests get read-write access, and unauthenticated requests get read-only access.

REST framework включает в себя ряд классов разрешений, которые мы можем использовать для ограничения доступа к определенному представлению. В данном случае нам нужен класс `IsAuthenticatedOrReadOnly`, который обеспечит аутентифицированным запросам доступ на чтение-запись, а неаутентифицированным - только на чтение.

First add the following import in the views module

Сначала добавьте следующий импорт в модуль views

```
from rest_framework import permissions
```

Then, add the following property to **both** the `SnippetList` and `SnippetDetail` view classes.

Затем добавьте следующее свойство к **обоим** классам представления `SnippetList` и `SnippetDetail`.

```
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

## Adding login to the Browsable API

## Добавление входа в просматриваемый API

If you open a browser and navigate to the browsable API at the moment, you'll find that you're no longer able to create new code snippets. In order to do so we'd need to be able to login as a user.

Если вы откроете браузер и перейдете к просматриваемому API, то обнаружите, что больше не можете создавать новые фрагменты кода. Для этого нам нужно иметь возможность войти в систему как пользователь.

We can add a login view for use with the browsable API, by editing the URLconf in our project-level `urls.py` file.

Мы можем добавить представление входа для использования с просматриваемым API, отредактировав URLconf в нашем файле `urls.py` на уровне проекта.

Add the following import at the top of the file:

Добавьте следующий импорт в верхней части файла:

```
from django.urls import path, include
```

And, at the end of the file, add a pattern to include the login and logout views for the browsable API.

И в конце файла добавьте шаблон для включения представлений входа и выхода для просматриваемого API.

```
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
```

The `'api-auth/'` part of pattern can actually be whatever URL you want to use.

Часть шаблона `'api-auth/'` может быть любым URL, который вы хотите использовать.

Now if you open up the browser again and refresh the page you'll see a 'Login' link in the top right of the page. If you log in as one of the users you created earlier, you'll be able to create code snippets again.

Теперь, если вы снова откроете браузер и обновите страницу, вы увидите ссылку 'Login' в правом верхнем углу страницы. Если вы войдете в систему как один из пользователей, созданных ранее, вы снова сможете создавать фрагменты кода.

Once you've created a few code snippets, navigate to the '/users/' endpoint, and notice that the representation includes a list of the snippet ids that are associated with each user, in each user's 'snippets' field.

После создания нескольких фрагментов кода перейдите к конечной точке '/users/' и обратите внимание, что представление включает список идентификаторов фрагментов, связанных с каждым пользователем, в поле 'snippets' каждого пользователя.

## Object level permissions

## Разрешения на уровне объекта

Really we'd like all code snippets to be visible to anyone, but also make sure that only the user that created a code snippet is able to update or delete it.

Нам бы хотелось, чтобы все кодовые сниппеты были видны всем, но при этом чтобы только пользователь, создавший кодовый сниппет, мог его обновить или удалить.

To do that we're going to need to create a custom permission.

Для этого нам понадобится создать пользовательское разрешение.

In the snippets app, create a new file, `permissions.py`

В приложении snippets создайте новый файл `permissions.py`.

```
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
```

Now we can add that custom permission to our snippet instance endpoint, by editing the `permission_classes` property on the `SnippetDetail` view class:

Теперь мы можем добавить это пользовательское разрешение в конечную точку экземпляра сниппета, отредактировав свойство `permission_classes` в классе представления `SnippetDetail`:

```
permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
```

Make sure to also import the `IsOwnerOrReadOnly` class.

Не забудьте также импортировать класс `IsOwnerOrReadOnly`.

```
from snippets.permissions import IsOwnerOrReadOnly
```

Now, if you open a browser again, you find that the 'DELETE' and 'PUT' actions only appear on a snippet instance endpoint if you're logged in as the same user that created the code snippet.

Теперь, если вы снова откроете браузер, вы обнаружите, что действия 'DELETE' и 'PUT' появляются на конечной точке экземпляра сниппета, только если вы вошли в систему как тот же пользователь, который создал сниппет кода.

## Authenticating with the API

## Аутентификация в API

Because we now have a set of permissions on the API, we need to authenticate our requests to it if we want to edit any snippets. We haven't set up any [authentication classes](../api-guide/authentication.md), so the defaults are currently applied, which are `SessionAuthentication` and `BasicAuthentication`.

Поскольку теперь у нас есть набор прав доступа к API, нам нужно аутентифицировать наши запросы к нему, если мы хотим редактировать какие-либо сниппеты. Мы не установили никаких [классов аутентификации](../api-guide/authentication.md), поэтому сейчас применяются значения по умолчанию, а именно `SessionAuthentication` и `BasicAuthentication`.

When we interact with the API through the web browser, we can login, and the browser session will then provide the required authentication for the requests.

Когда мы взаимодействуем с API через веб-браузер, мы можем войти в систему, и тогда сессия браузера обеспечит необходимую аутентификацию для запросов.

If we're interacting with the API programmatically we need to explicitly provide the authentication credentials on each request.

Если мы взаимодействуем с API программно, нам необходимо явно предоставлять учетные данные аутентификации при каждом запросе.

If we try to create a snippet without authenticating, we'll get an error:

Если мы попытаемся создать сниппет без аутентификации, мы получим ошибку:

```
http POST http://127.0.0.1:8000/snippets/ code="print(123)"

{
    "detail": "Authentication credentials were not provided."
}
```

We can make a successful request by including the username and password of one of the users we created earlier.

Мы можем сделать успешный запрос, включив в него имя пользователя и пароль одного из пользователей, созданных нами ранее.

```
http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"

{
    "id": 1,
    "owner": "admin",
    "title": "foo",
    "code": "print(789)",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

## Summary

## Резюме

We've now got a fairly fine-grained set of permissions on our Web API, and end points for users of the system and for the code snippets that they have created.

Теперь у нас есть довольно тонкий набор разрешений для нашего Web API, а также конечные точки для пользователей системы и для созданных ими фрагментов кода.

In [part 5](5-relationships-and-hyperlinked-apis.md) of the tutorial we'll look at how we can tie everything together by creating an HTML endpoint for our highlighted snippets, and improve the cohesion of our API by using hyperlinking for the relationships within the system.

В [части 5](5-relationships-and-hyperlinked-apis.md) учебника мы рассмотрим, как мы можем связать все вместе, создав конечную точку HTML для наших выделенных фрагментов, и улучшить связность нашего API, используя гиперссылки для связей внутри системы.