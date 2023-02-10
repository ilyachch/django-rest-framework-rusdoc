<!-- TRANSLATED by md-translate -->
# Быстрый старт

Мы собираемся создать простой API, который позволит пользователям-администраторам просматривать и редактировать пользователей и группы в системе.

## Настройка проекта

Создайте новый проект Django под названием `tutorial`, затем создайте новое приложение под названием `quickstart`.

```bash
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

Схема проекта должна выглядеть следующим образом:

```bash
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

Может показаться необычным, что приложение было создано в каталоге проекта. Использование пространства имен проекта позволяет избежать столкновения имен с внешними модулями (эта тема выходит за рамки данного краткого руководства).

Теперь синхронизируйте вашу базу данных в первый раз:

```bash
python manage.py migrate
```

Мы также создадим начального пользователя с именем `admin` и паролем. Мы будем аутентифицироваться под этим пользователем позже в нашем примере.

```bash
python manage.py createsuperuser --username admin --email admin@example.com
```

После того как вы настроили базу данных и создали начального пользователя, откройте каталог приложения и приступайте к кодированию...

## Сериализаторы

Сначала мы определим некоторые сериализаторы. Давайте создадим новый модуль `tutorial/quickstart/serializers.py`, который мы будем использовать для представления данных.

```python
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

Обратите внимание, что в данном случае мы используем гиперсвязанные отношения с помощью `HyperlinkedModelSerializer`. Вы также можете использовать первичный ключ и различные другие отношения, но гиперсвязь - это хороший дизайн RESTful.

## Представления

Хорошо, теперь нам нужно написать несколько представлений. Откройте `tutorial/quickstart/views.py` и начните печатать.

```python
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

Вместо того чтобы писать несколько представлений, мы объединяем все общее поведение в классы, называемые `ViewSets`.

При необходимости мы можем легко разбить их на отдельные представления, но использование наборов представлений позволяет хорошо организовать логику представления, а также сделать ее очень лаконичной.

## URL-адреса

Хорошо, теперь давайте подключим URL API. Переходим к `tutorial/urls.py`...

```python
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

Поскольку мы используем наборы представлений вместо представлений, мы можем автоматически генерировать URL conf для нашего API, просто зарегистрировав наборы представлений в классе маршрутизатора.

Опять же, если нам нужен больший контроль над URL API, мы можем просто вернуться к использованию обычных представлений на основе классов и явного написания URL conf.

Наконец, мы включаем представления входа и выхода по умолчанию для использования с просматриваемым API. Это необязательно, но полезно, если ваш API требует аутентификации, а вы хотите использовать просматриваемый API.

## Пагинация

Пагинация позволяет вам контролировать количество возвращаемых объектов на странице. Чтобы включить ее, добавьте следующие строки в `tutorial/settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Настройки

Добавьте `'rest_framework'` в `INSTALLED_APPS`. Модуль настроек будет находиться в `tutorial/settings.py`.

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Хорошо, мы закончили.

---

## Тестирование нашего API

Теперь мы готовы протестировать созданный нами API. Давайте запустим сервер из командной строки.

```bash
python manage.py runserver
```

Теперь мы можем получить доступ к нашему API как из командной строки, так и с помощью таких инструментов, как `curl`...

```bash
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

Или используя [httpie](https://httpie.io/docs#installation), инструмент командной строки...

```bash
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

Или непосредственно через браузер, перейдя по URL `http://127.0.0.1:8000/users/`...

![Изображение быстрого запуска](https://github.com/encode/django-rest-framework/raw/master/docs/img/quickstart.png)

Если вы работаете через браузер, обязательно войдите в систему, используя элемент управления в правом верхнем углу.

Отлично, это было легко!

Если вы хотите получить более глубокое понимание того, как REST-фреймворк работает вместе, перейдите к [учебнику](tutorial/1-serialization.md) или начните просматривать [руководство по API](api-guide/requests.md).
