# Урок 4: Аутентификация и Разрешения

На данный момент наше API не имеет ограничений, на то, кто может изменять или удалять код сниппетов. Хотелось бы более продвинутого поведения, реализующего следующее:

1. Код сниппетов всегда связан с автором;
2. Только авторизованные пользователи могут создавать сниппеты.
3. Только создатель сниппета может его изменять и удалять.
4. Неавторизованные пользователи должны иметь полный доступ только на чтение.

## Расширение нашей модели

Мы собираемся внести несколько изменений в наш класс модели `Snippet`. Для начала, давайте добавим пару новых полей. Первое поле - связь с создавшим пользователем, второе - форматированная и подсвеченная HTML-версия кода сниппета.

Добавьте следующие поля в класс модели `Snippet`, который находится в `snippets/models.py`:

```python
owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
highlighted = models.TextField()
```

Так же мы должны заполнять новое поле подсвеченной версией кода. Для этого мы будем использовать библиотеку `pygments`.

Импортируем несколько новых пакетов:

```python
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
```

Теперь мы можем расширить метод `.save()` нашей модели:

```python
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
    super(Snippet, self).save(*args, **kwargs)
```

После того, как все будет готово, нам необходимо обновить нашу базу данных. Обычно, для этого мы используем миграции, но, в рамках обучения, мы удалим БД с миграциями и создадим заново.

```bash
rm -f db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

Также, есть смысл создать нескольких пользователей, чтобы протестировать наше API. Самый быстрый способ - использовать команду `createsuperuser`.

```bash
python manage.py createsuperuser
```

## Добавляем User в API

Теперь у нас есть несколько пользователей, с которыми можно работать. Добавим их в наше API. Создадим сериализатор для них. Добавляем в `snippets/serializers.py`:

```python
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
```

Поскольку `snippets` - обратная связь с моделью `User`, она не будет подключена по умолчанию при использовании класса `ModelSerializer`, поэтому мы должны добавить явное указание на это поле.

Так же мы добавим несколько представлений в `snippets/views.py`. Мы добавим представления только для чтения, поэтому мы используем встроенные представления классы `ListAPIView` и `RetrieveAPIView`.

```python
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Убедитесь, что вы подключили класс `UserSerializer`.

```python
from snippets.serializers import UserSerializer
```

Теперь нам необходимо добавить эти представления в API, определив их URL. Добавим следующие шаблоны в `snippets/urls.py`:


```python
path('users/', views.UserList.as_view()),
path('users/<int:pk>/', views.UserDetail.as_view()),
```

## Связываем сниппеты и пользователей

Сейчас, при создании сниппета, пользователь не будет связан с созданным сниппетом, поскольку пользователь не посылается, как часть сериализованного представления. Однако, он является частью входящего запроса (`request.user`).

Мы можем решить эту проблему переопределив метод `.perform_create()` нашего представления сниппета, который определяет то, как сохраняется наш объект и добавить любую информацию, которая неявно присутствует в нашем запросе или запрашиваемом URL.

Добавьте следующий метод в класс представления `SnippetList`:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

Теперь в метод `.create()` нашего сериализатора будет попадать дополнительное поле `owner`, содержащее объект пользователя, полученный из объекта запроса.

## Обновляем сериализатор

Теперь сниппеты связаны с создавшими их пользователями, давайте обновим `SnippetSerializer`. Добавьте следующее в `snippets/serializers.py`:

```python
owner = serializers.ReadOnlyField(source='owner.username')
```

Важно: Убедитесь, что вы добавили `'owner', ` в список полей в классе `Meta`.

Это поле делает интересую вещь. Изначальный аргумент указывает, какой атрибут используется для заполнения поля и может указывать на любой атрибут связанной модели. Можно использовать точечное описание, как описано выше, что позволит указать именно необходимый атрибут, как это делается в шаблонах Django.

Поле, которое мы только что добавили, связывается объектом класса `ReadOnlyField`, что отличается от остальных полей, таких, как `CharField`, `BooleanField` и т.д. Данное поле - всегда read-only, и будет использоваться для представления данных, но не для изменения, когда объект будет десериализован. Так же мы можем заменить это поле на `CharField(read_only=True)`. 

## Добавляем разрешения в представления

Теперь, когда сниппеты связаны с пользователями, мы хотим быть уверены, что только авторизованные пользователи могут создавать, изменять и удалять сниппеты.

DRF включает большое число классов доступа, которые мы можем использовать, чтобы определять, кто может получить доступ к данному представлению. В данному случае нам подходит `IsAuthenticatedOrReadOnly`, который разрешит чтение/запись для авторизованных пользователей и только чтение для анонимных.

Для начала, добавьте следующее в `snippets/views.py`:

```python
from rest_framework import permissions
```
Затем, добавьте следующее свойство в классы `SnippetList` и `SnippetDetail` в том же модуле.

```python
permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
```

## Добавление авторизации в браузерную версию API

Если вы откроете браузер и зайдете на браузерную версию API сейчас, вы увидите, что мы больше не можете создавать сниппеты. Для того, чтобы получить такую возможность, нам необходимо авторизоваться.

Мы можем добавить представление авторизации, изменив корневой диспетчер URL-ов.

Добавьте следующее в `urls.py`:

```python
from django.urls import path, include
```

А так же в конец этого же модуля допишите:

```python
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
```

Часть шаблона `'api-auth/'` может быть любым URL-адресом, который вы хотите использовать.

Сейчас, если вы обновите страницу, вы увидите ссылку `Login` в правом верхнем углу. Войдя под одном из пользователей, что вы создали ранее, вы получите доступ к созданию сниппетов.

Создав несколько сниппетов и перейдся к ресурсу `'/users/'`, можно заметить, что представление включает в себя список сниппетов, id которых связаны с каждым пользователем, в поле `'snippets'`.

## Доступ на уровне объектов

Вообще, мы хотим, чтобы сниппеты были доступны все для чтения, однако мы хотим, чтобы только создатель сниппета мог редактировать или удалять его.

Для того, чтобы это сделать, мы напишем собственный класс доступа.

В приложении `snippets` создайте модуль `permissions.py` со следующим содержимым:

```python
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

Теперь мы можем добавить собственные права доступа ресурсу сниппета, добавив свойство `permission_classes` класса-представления `SnippetDetail`:

```python
permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
```

Убедитесь, что подключили класс `IsOwnerOrReadOnly`.

```python
from snippets.permissions import IsOwnerOrReadOnly
```

Сейчас, если вы опять откроете браузер, вы увидите кнопки `DELETE` и `PUT`, если будете авторизованы под тем же пользователем, что создал сниппет.


## Авторизация с помощью API

Поскольку сейчас у нас есть разделение прав доступа к API, мы должны аутентифицировать запросы, если мы хотим изменять сниппеты. Мы не указали аутентификационных классов, поэтому по умолчанию подключены `SessionAuthentication` и `BasicAuthentication`.

Когда мы взаимодействуем с API через браузер, мы можем авторизоваться и сессия браузера будет предоставлять авторизационные данные в запросы.

Если мы работаем с API программно, мы должны явно указывать авторизационные данные в каждом запросе.

Если мы попробуем создать сниппет без авторизации, мы получим ошибку:

```bash
http POST http://127.0.0.1:8000/snippets/ code="print(123)"

{
    "detail": "Authentication credentials were not provided."
}
```

Мы можем выполнить запрос, включив имя пользователя и пароль одного из наших пользователей.

```bash
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

## Итого

Теперь у нас есть набор прав доступа к нашему API и ресурс пользователей, а так же связь пользователей и сниппетов, которые они создали.

В [5 уроке](relations-and-hyperlinks.md) этого руководства мы посмотрим, как связать все вместе, создав HTML ресурс для наших подсвеченных сниппетов у улучшить связанность нашего API, использовать ссылки в связях.
