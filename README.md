# Django REST framework

Django REST framework \(DRF\) - мощный и гибкий инструмент для построения Web API.

Вот несколько причин, чтобы использовать DRF:

* Крайне удобная для разработчиков [браузерная версия API](http://restframework.herokuapp.com/);
* Наличие пакетов для OAuth1a и OAuth2 авторизации;
* Сериализация, поддерживающая ORM и не-ORM источники данных;
* Возможность полной и детальной настройки - можно использовать обычные представления-функции, если вы не нуждаетесь в мощном функционале;
* Расширенная документация и [отличная поддержка сообщества](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework);
* Используется и пользуется уважением таких узнаваемых компаний, как [Mozilla](http://www.mozilla.org/en-US/about/), [Red Hat](https://www.redhat.com/), [Heroku](https://www.heroku.com/), [Eventbrite](https://www.eventbrite.co.uk/about/).

## Зависимости

У DRF следующие требования:

* Python \(2.7, 3.2, 3.3, 3.4, 3.5, 3.6\)
* Django \(1.8, 1.9, 1.10, 1.11\)

Данные пакеты не обязательны:

* [coreapi](https://www.gitbook.com/book/ilyachch/django-rest-framework-ru/edit#) \(1.32.0+\) - Schema generation support.
* [Markdown](http://pypi.python.org/pypi/Markdown/) \(2.1.0+\) - Markdown support for the browsable API.
* [django-filter](http://pypi.python.org/pypi/django-filter) \(1.0.1+\) - Filtering support.
* [django-crispy-forms](https://github.com/maraujop/django-crispy-forms) - Improved HTML display for filtering.
* [django-guardian](https://github.com/django-guardian/django-guardian) \(1.1.1+\) - Object level permissions support.

## Установка

Установите с помощью `pip`

```py
pip install djangorestframework
pip install markdown        # Опционально
pip install django-filter   # Опционально
```

или склонируйте проект с Guthub

```
git clone git@github.com:encode/django-rest-framework.git
```

Добавьте `'rest_framework'` в `INSTALLED_APPS`  в настройках:

```py
INSTALLED_APPS = (
    ...
    'rest_framework',
)
```

Если вы планируете использовать браузерную версию API, возможно, вы захотите добавить предстваления входа и выхода. Для этого добавьте следующее в корневой диспетчер URL:

```py
urlpatterns = [
    ...
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework'))
]
```

Важно помнить, что в качестве пути вы можете указать что угодно, однако подключить необходимо `rest_framework.urls` с указанием пространства имен `rest_framework`. Но в Django версии 1.9 и выше, пространство имен можно оставить пустым и DRF заполнит его за вас.

## Пример

Давайте рассмотрим небольшой пример использования DRF для построения основанного на моделях API.

Мы создадим API с возможностью чтения/записи и доступом к данным пользователей нашего проекта.

Любые глобальные настройки DRF описываются в словаре конфигурации `REST_FRAMEWORK`. Начните с того, что добавите следующее в `settings.py`:

```py
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}
```

Не забудьте добавить `'rest_framework'` в `INSTALLED_APPS`.

Теперь мы готовы к созданию собственного API.

Ниже представлен корневой диспетчер URL:

```py
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Сериализаторы описывают представление данных.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# Наборы представлений описывают поведение представлений.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Роутеры позволяют быстро и просто сконфигурировать адреса.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Привяжите конфигурацию URL, используя роутеры.
# Так же мы предоставляем URL для авторизации в браузере.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Теперь можно открыть API в вашем браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/), и увидеть ваше API `'users'`. Так же, если вы воспользуетесь кнопкой `'Login'` в верхнем правом углу и авторизуетесь, вы сможете добавлять, изменять и удалять пользователей из системы.

## Быстрый старт

Не можете дождаться, чтобы начать? Руководство по [быстрому старту](quick-start.md) - быстрейший способ.

## Руководство

Руководство проведет вас через все этапы настройки DRF. Это займет не очень много времени, однако вы получите полное понимание того, как все компоненты работают друг с другом и данное руководство крайне рекомендовано к прочтению.

1. [Сериализация](quick-start/serialization.md)
2. [Запросы-ответы](quick-start/request-response.md)
3. [Представления-классы](quick-start/class-based-views.md)
4. [Аутентификация/права доступа](quick-start/auth-and-perm.md)
5. [Отношения и связи](quick-start/relations-and-hypelinks.md)
6. [Наборы представлений и роутеры](quick-start/viewsets-and-routers.md)
7. [Схемы и клиентские библиотеки](quick-start/schemas-and-client-libs.md)

Так же есть пример работающего API законченного руководства для тестовых целей, [доступен здесь](http://restframework.herokuapp.com/).

## Навигатор по API

Навигатор по API - исчерпывающее руководство по всему функционалу, предоставляемому DRF.

* [Запросы](api-navigation/requests.md)
* [Ответы](api-navigation/responses.md)
* [Представления](api-navigation/views.md)
* [Общие представления](api-navigation/generic-views.md)
* [Viewsets](api-navigation/viewsets.md)
* [Маршрутизаторы](api-navigation/routers.md)
* [Парсеры](api-navigation/parsers.md)
* [Рендеры](api-navigation/renders.md)
* [Cериализаторы](api-navigation/serializers.md)
* [Serializer fields](http://www.django-rest-framework.org/api-guide/fields/)
* [Serializer relations](http://www.django-rest-framework.org/api-guide/relations/)
* [Validators](http://www.django-rest-framework.org/api-guide/validators/)
* [Authentication](http://www.django-rest-framework.org/api-guide/authentication/)
* [Permissions](http://www.django-rest-framework.org/api-guide/permissions/)
* [Throttling](http://www.django-rest-framework.org/api-guide/throttling/)
* [Filtering](http://www.django-rest-framework.org/api-guide/filtering/)
* [Pagination](http://www.django-rest-framework.org/api-guide/pagination/)
* [Versioning](http://www.django-rest-framework.org/api-guide/versioning/)
* [Content negotiation](http://www.django-rest-framework.org/api-guide/content-negotiation/)
* [Metadata](http://www.django-rest-framework.org/api-guide/metadata/)
* [Schemas](http://www.django-rest-framework.org/api-guide/schemas/)
* [Format suffixes](http://www.django-rest-framework.org/api-guide/format-suffixes/)
* [Returning URLs](http://www.django-rest-framework.org/api-guide/reverse/)
* [Exceptions](http://www.django-rest-framework.org/api-guide/exceptions/)
* [Status codes](http://www.django-rest-framework.org/api-guide/status-codes/)
* [Testing](http://www.django-rest-framework.org/api-guide/testing/)
* [Settings](http://www.django-rest-framework.org/api-guide/settings/)

## Статьи

Основные руководства для использующих DRF.

* [Documenting your API](http://www.django-rest-framework.org/topics/documenting-your-api/)
* [API Clients](http://www.django-rest-framework.org/topics/api-clients/)
* [Internationalization](http://www.django-rest-framework.org/topics/internationalization/)
* [AJAX, CSRF & CORS](http://www.django-rest-framework.org/topics/ajax-csrf-cors/)
* [HTML & Forms](http://www.django-rest-framework.org/topics/html-and-forms/)
* [Browser enhancements](http://www.django-rest-framework.org/topics/browser-enhancements/)
* [The Browsable API](http://www.django-rest-framework.org/topics/browsable-api/)
* [REST, Hypermedia & HATEOAS](http://www.django-rest-framework.org/topics/rest-hypermedia-hateoas/)
* [Third Party Packages](http://www.django-rest-framework.org/topics/third-party-packages/)
* [Tutorials and Resources](http://www.django-rest-framework.org/topics/tutorials-and-resources/)
* [Contributing to REST framework](http://www.django-rest-framework.org/topics/contributing/)
* [Project management](http://www.django-rest-framework.org/topics/project-management/)
* [3.0 Announcement](http://www.django-rest-framework.org/topics/3.0-announcement/)
* [3.1 Announcement](http://www.django-rest-framework.org/topics/3.1-announcement/)
* [3.2 Announcement](http://www.django-rest-framework.org/topics/3.2-announcement/)
* [3.3 Announcement](http://www.django-rest-framework.org/topics/3.3-announcement/)
* [3.4 Announcement](http://www.django-rest-framework.org/topics/3.4-announcement/)
* [3.5 Announcement](http://www.django-rest-framework.org/topics/3.5-announcement/)
* [3.6 Announcement](http://www.django-rest-framework.org/topics/3.6-announcement/)
* [Kickstarter Announcement](http://www.django-rest-framework.org/topics/kickstarter-announcement/)
* [Mozilla Grant](http://www.django-rest-framework.org/topics/mozilla-grant/)
* [Funding](http://www.django-rest-framework.org/topics/funding/)
* [Release Notes](http://www.django-rest-framework.org/topics/release-notes/)
* [Jobs](http://www.django-rest-framework.org/topics/jobs/)

## Разработка

Прочтите [руководство для разработчиков](http://www.django-rest-framework.org/topics/contributing/) для получения информации о том, как склонировать репозиторий, запустить набор тестов и отправить изменения обратно в DRF.

## Поддержка

Для поддержки обратитесь в [группу обсуждения DRF](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework) или создайте вопрос на StackOverflow с указанием тэга ['django-rest-framework'](http://stackoverflow.com/questions/tagged/django-rest-framework).

Для уведомления об обновлениях, подпишитесь на нас в [Twitter](https://twitter.com/_tomchristie).

## Безопасность

Если вы уверены, что нашли пробел в безопасности, пожалуйста, **не создавайте публичный баг-репорт!**

Отправьте описание проблемы по почте [rest-framework-security@googlegroups.com](mailto:rest-framework-security@googlegroups.com). Руководители проекта будут работать с вами для решения любых подобных проблем.

