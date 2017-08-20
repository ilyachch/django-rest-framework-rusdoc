# Быстрый старт {#quickstart}

Мы собираемся создать простое API, которое позволяло пользователям-администраторам просматривать и изменять пользователей и группы в системе.

## Настройки проекта

Создайте новый Django проект, названный `tutorial`, затем создайте новое приложение, названное `quickstart`.

```bash
# Создайте директорию проекта

mkdir tutorial
cd tutorial

# Создайте виртуальное окружение, чтобы изолировать установленные пакеты локально

virtualenv env
source env/bin/activate    # Для Windows используйте `env\Scripts\activate`

# Установите Django и Django REST framework в виртуальное окружение.
pip install django
pip install djangorestframework


# Создайте новый проект с одним приложением

django-admin.py startproject tutorial .    # Не забудьте последний символ '.'

cd tutorial
django-admin.py startapp quickstart
cd ..
```

Создайте базу данных:

```bash
python manage.py migrate
```

Так же необходимо создать начального пользователя `admin` с паролем `password123`. Потом мы авторизуем этого пользователя в нашем примере.

```bash
python manage.py createsuperuser
```

После того, как вы создали базу данных, начального пользователя и готовы продолжать, откройте директорию приложения и давайте уже начнем писать код.

## Сериализаторы

Для начала мы определим несколько сериализаторов. Создайте модуль `serializers.py`, расположенный в `tutorial/quickstart`, который мы будем использовать для представления наших данных.

```py
from django.contrib.auth.models import User, Group 
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = User
                fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Group
                fields = ('url', 'name')
```

Заметьте, мы используем ссылочные отношения в данном случае. Для этого мы используем `HyperlinkedModelSerializer`. Вы так же можете использовать первичный ключ или любые другие способы связи объектов, однако ссылочная связь считается более правильной при проектировании API.

## Представления {#views}

Теперь мы добавим несколько представлений. Откройте `tutorial/quickstart/views.py` и напишите:

```py
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```

Вместо того, чтобы писать большое количество представлений, мы группируем их в классы с общим поведением, называемые `ViewSet`.

Конечно, мы легко можем разбить их на отдельные представления, но зачем, если можно держать всю логику в одном месте, отлично организованно.

## URL-ы

Теперь давайте привяжем к нашему API URL-ы. Заходим в `tutorial/urls.py`:

```py
from django.conf.urls import url, include
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Поскольку мы используем наборы представлений \(`ViewSet`-ы\), мы можем автоматически сгенерировать конфигурацию URL-ов, просто зарегистрировав наборы представлений в классе `router`.

Опять же, если нам нужно больше контроля над URL-ами API, мы можем просто разбить это на обычные представления-классы и описать конфигурацию URL явно.

В конце мы подключаем стандартные представления авторизации и выхода из сессии для использования в браузерной версии API. Это опционально, однако очень удобно, если ваше API требует авторизации и вы хотите использовать браузерную версию API.

## Настройки {#settings}

Так же мы добавим несколько глобальных настроек. Мы включим постраничный вывод и предоставим доступ только пользователям-администраторам. модуль настроек находится в `tutorual/settings.py`.

```py
INSTALLED_APPS = (
    ...
    'rest_framework',
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE':10
}
```

Теперь мы закончили.

---

## Тестирование нашего API {#testing-our-api}

Теперь мы готовы протестировать наше API. Запустите сервер командой

```bash
python manage.py runserver
```

Теперь мы можем получить доступ к нашему API как из командной строки, используя утилиту `curl`...

```bash
bash: curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin"
        },
        {
            "email": "tom@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/2/",
            "username": "tom"
        }
    ]
}
```

или [httpie](https://github.com/jakubroztocil/httpie#installation)...

```bash
bash: http -a admin:password123 http://127.0.0.1:8000/users/

HTTP/1.1 200 OK
...
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://localhost:8000/users/1/",
            "username": "paul"
        },
        {
            "email": "tom@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/2/",
            "username": "tom"
        }
    ]
}
```

или вообще через браузер, открыв адрес [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)...

![](http://www.django-rest-framework.org/img/quickstart.png)

Если вы работаете через браузер, убедитесь, что вы авторизовались через меню в правом верхнем углу.

Это было легко=\)

Если вы хотите изучить, как все части DRF работают друг с другом, продолжайте читать [руководство](quick-start/serialization.md), или начните изучать путеводитель по API.

