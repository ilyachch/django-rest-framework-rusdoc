<!-- TRANSLATED by md-translate -->
# Quickstart

# Быстрый старт

We're going to create a simple API to allow admin users to view and edit the users and groups in the system.

Мы собираемся создать простой API, чтобы позволить пользователям администратора просматривать и редактировать пользователей и группы в системе.

## Project setup

## Настройка проекта

Create a new Django project named `tutorial`, then start a new app called `quickstart`.

Создайте новый проект Django под названием `turniory ', затем запустите новое приложение под названием` QuickStart`.

```
# Create the project directory
mkdir tutorial
cd tutorial

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin startapp quickstart
cd ..
```

The project layout should look like:

Макет проекта должен выглядеть как:

```
$ pwd
<some path>/tutorial
$ find .
.
./tutorial
./tutorial/asgi.py
./tutorial/__init__.py
./tutorial/quickstart
./tutorial/quickstart/migrations
./tutorial/quickstart/migrations/__init__.py
./tutorial/quickstart/models.py
./tutorial/quickstart/__init__.py
./tutorial/quickstart/apps.py
./tutorial/quickstart/admin.py
./tutorial/quickstart/tests.py
./tutorial/quickstart/views.py
./tutorial/settings.py
./tutorial/urls.py
./tutorial/wsgi.py
./env
./env/...
./manage.py
```

It may look unusual that the application has been created within the project directory. Using the project's namespace avoids name clashes with external modules (a topic that goes outside the scope of the quickstart).

Может показаться необычным, что приложение было создано в каталоге проекта.
Использование пространства имен проекта позволяет избежать столкновений именовать с помощью внешних модулей (тема, которая выходит за рамки QuickStart).

Now sync your database for the first time:

Теперь синхронизируйте вашу базу данных впервые:

```
python manage.py migrate
```

We'll also create an initial user named `admin` with a password. We'll authenticate as that user later in our example.

Мы также создадим первоначального пользователя с именем `Admin` с паролем.
Мы аутентифицируем как этот пользователь позже в нашем примере.

```
python manage.py createsuperuser --username admin --email admin@example.com
```

Once you've set up a database and the initial user is created and ready to go, open up the app's directory and we'll get coding...

После того, как вы настроите базу данных и начальный пользователь создан и готов к работе, откройте каталог приложения, и мы получим кодирование ...

## Serializers

## serializers

First up we're going to define some serializers. Let's create a new module named `tutorial/quickstart/serializers.py` that we'll use for our data representations.

Во -первых, мы собираемся определить несколько сериалов.
Давайте создадим новый модуль с именем `turnerial/Quickstart/serializers.py`, который мы будем использовать для наших представлений данных.

```
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
```

Notice that we're using hyperlinked relations in this case with `HyperlinkedModelSerializer`. You can also use primary key and various other relationships, but hyperlinking is good RESTful design.

Обратите внимание, что в этом случае мы используем гиперсвязанные отношения с `HyperlinkedModelserializer '.
Вы также можете использовать первичный ключ и различные другие отношения, но гиперлизирование - это хороший дизайн.

## Views

## Просмотры

Right, we'd better write some views then. Open `tutorial/quickstart/views.py` and get typing.

Правильно, нам лучше написать некоторые представления тогда.
Откройте `Tutorial/QuickStart/Views.py` и получите набор печати.

```
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
```

Rather than write multiple views we're grouping together all the common behavior into classes called `ViewSets`.

Вместо того, чтобы писать несколько просмотров, мы объединяем все общее поведение в классы под названием «Просмотр».

We can easily break these down into individual views if we need to, but using viewsets keeps the view logic nicely organized as well as being very concise.

Мы можем легко разбить их на отдельные представления, если нам нужно, но использование видов сохраняет логику просмотра хорошо организованной, а также очень краткой.

## URLs

## URLS

Okay, now let's wire up the API URLs. On to `tutorial/urls.py`...

Хорошо, теперь давайте подключим URL -адреса API.
На `turning/urls.py` ...

```
from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
```

Because we're using viewsets instead of views, we can automatically generate the URL conf for our API, by simply registering the viewsets with a router class.

Поскольку мы используем виды вместо представлений, мы можем автоматически генерировать URL CONF для нашего API, просто зарегистрировав виды с помощью класса маршрутизатора.

Again, if we need more control over the API URLs we can simply drop down to using regular class-based views, and writing the URL conf explicitly.

Опять же, если нам нужно больше контроля над URL-адресами API, мы можем просто спуститься до использования регулярных представлений на основе классов и явно написать URL Conf.

Finally, we're including default login and logout views for use with the browsable API. That's optional, but useful if your API requires authentication and you want to use the browsable API.

Наконец, мы включаем вход по умолчанию и виды входа в систему для использования с API -файлом.
Это необязательно, но полезно, если ваш API требует аутентификации, и вы хотите использовать API, который можно найти.

## Pagination

## Парень

Pagination allows you to control how many objects per page are returned. To enable it add the following lines to `tutorial/settings.py`

Парень позволяет вам контролировать, сколько объектов на страницу возвращается.
Чтобы включить его добавить следующие строки в `turning/settings.py`

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Settings

## Настройки

Add `'rest_framework'` to `INSTALLED_APPS`. The settings module will be in `tutorial/settings.py`

Добавьте `'rest_framework' 'в` insted_apps`.
Модуль «Настройки» будет в `turnerial/settings.py`

```
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Okay, we're done.

Хорошо, мы закончили.

---

## Testing our API

## тестирование нашего API

We're now ready to test the API we've built. Let's fire up the server from the command line.

Теперь мы готовы проверить API, который мы построили.
Давайте запустим сервер из командной строки.

```
python manage.py runserver
```

We can now access our API, both from the command-line, using tools like `curl`...

Теперь мы можем получить доступ к нашему API, как из командной строки, используя такие инструменты, как «curl» ...

```
bash: curl -u admin -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/users/
Enter host password for user 'admin':
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin",
            "email": "admin@example.com",
            "groups": []
        }
    ]
}
```

Or using the [httpie](https://httpie.io/docs#installation), command line tool...

Или с помощью [httpie] (https://httpie.io/docs#installation), инструмент командной строки ...

```
bash: http -a admin http://127.0.0.1:8000/users/
http: password for admin@127.0.0.1:8000::
$HTTP/1.1 200 OK
...
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin"
        }
    ]
}
```

Or directly through the browser, by going to the URL `http://127.0.0.1:8000/users/`...

Или прямо через браузер, перейдя на URL `http: //127.0.0.1: 8000/users/` ...

![Quick start image](../img/quickstart.png)

! [Quick Start Image] (../ img/Quickstart.png)

If you're working through the browser, make sure to login using the control in the top right corner.

Если вы работаете через браузер, обязательно входите в систему, используя элемент управления в правом верхнем углу.

Great, that was easy!

Отлично, это было легко!

If you want to get a more in depth understanding of how REST framework fits together head on over to [the tutorial](1-serialization.md), or start browsing the [API guide](../api-guide/requests.md).

Если вы хотите получить более глубокое понимание того, как структура REST объединяется, отправляйтесь в [The Tutorial] (1-Serialization.md), или начните просматривать [Руководство по API] (../ API-Guide/запросы.
MD).