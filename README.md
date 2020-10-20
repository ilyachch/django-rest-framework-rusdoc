# Django REST framework

Django REST framework \(DRF\) - мощный и гибкий инструмент для построения Web API.

Вот несколько причин, чтобы использовать DRF:

* Крайне удобная для разработчиков [браузерная версия API](http://restframework.herokuapp.com/);
* Наличие пакетов для OAuth1a и OAuth2 авторизации;
* Сериализация, поддерживающая ORM и не-ORM источники данных;
* Возможность полной и детальной настройки - можно использовать обычные представления-функции, если вы не нуждаетесь в мощном функционале;
* Расширенная документация и [отличная поддержка сообщества](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework);
* Используется и пользуется уважением таких узнаваемых компаний, как [Mozilla](http://www.mozilla.org/en-US/about/), [Red Hat](https://www.redhat.com/), [Heroku](https://www.heroku.com/), [Eventbrite](https://www.eventbrite.co.uk/about/).

Существует пример API для тестирования, который доступен здесь [доступно здесь][sandbox].

## Зависимости

У DRF следующие требования:

* Python \(3.5, 3.6, 3.7\)
* Django \(1.11, 2.0, 2.1, 2.2\)

Мы **настоятельно рекомендуем** и официально поддерживаем только последние версии патчей для каждой серии Python и Django.

## Установка

Установите с помощью `pip`

```bash
    pip install djangorestframework
```

Добавьте `'rest_framework'` в `INSTALLED_APPS`  в настройках:

```python
    INSTALLED_APPS = (
        ...
        'rest_framework',
    )
```

## Пример

Давайте рассмотрим краткий пример использования инфраструктуры REST для создания простого API на основе модели для доступа к пользователям и группам.

Создайте новый проект:

```bash
pip install django
pip install djangorestframework
django-admin startproject example .
./manage.py migrate
./manage.py createsuperuser
```

Теперь отредактируйте модуль `example/urls.py` в вашем проекте:

```python
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Сериализаторы описывают представление данных.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

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

Мы также хотели бы настроить несколько параметров для нашего API.

Добавьте следующее к вашему `settings.py` модулю:

```python
INSTALLED_APPS = [
    ...  # Убедитесь, что здесь включены установленные по умолчанию приложения.
    'rest_framework',
]

REST_FRAMEWORK = {
    # Используйте стандартные Django  `django.contrib.auth` разрешения,
    # или разрешите доступ только для чтения для неаутентифицированных пользователей.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

Вот и все, мы закончили!

```bash
./manage.py runserver
```

Теперь можно открыть API в вашем браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/), и увидеть ваше API `'users'`. Так же, если вы воспользуетесь кнопкой `'Login'` в верхнем правом углу и авторизуетесь, вы сможете добавлять, изменять и удалять пользователей из системы.

Вы также можете взаимодействовать с API с помощью инструментов командной строки, таких как curl. Например, чтобы вывести конечную точку пользователей:

```bash
$ curl -H 'Accept: application/json; indent=4' -u admin:password http://127.0.0.1:8000/users/
[
    {
        "url": "http://127.0.0.1:8000/users/1/",
        "username": "admin",
        "email": "admin@example.com",
        "is_staff": true,
    }
]
```

Или создать нового пользователя:

```bash
$ curl -X POST -d username=new -d email=new@example.com -d is_staff=false -H 'Accept: application/json; indent=4' -u admin:password http://127.0.0.1:8000/users/
{
    "url": "http://127.0.0.1:8000/users/2/",
    "username": "new",
    "email": "new@example.com",
    "is_staff": false,
}
```

## Быстрый старт

Не можете дождаться, чтобы начать? Руководство по [быстрому старту](quick-start.md) - быстрейший способ.

## Руководство

Руководство проведет вас через все этапы настройки DRF. Это займет не очень много времени, однако вы получите полное понимание того, как все компоненты работают друг с другом и данное руководство крайне рекомендовано к прочтению.

1. [Сериализация](quick-start/serialization.md)
2. [Запросы-ответы](quick-start/request-response.md)
3. [Представления-классы](quick-start/class-based-views.md)
4. [Аутентификация/права доступа](quick-start/auth-and-perm.md)
5. [Отношения и связи](quick-start/relations-and-hyperlinks.md)
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
* [Поля сериализатора](api-navigation/fields.md)
* [Отношения сериализатора](api-navigation/relations.md)
* [Валидаторы](api-navigation/validators.md)
* [Аутентификация](api-navigation/authentication.md)
* [Разрешения](api-navigation/permissions.md)
* [Кэширование](api-navigation/caching.md)
* [Дросселирование (Регулирование)](api-navigation/throttling.md)
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

* [Documenting your API](https://www.django-rest-framework.org/topics/documenting-your-api/)
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

## Разработка

Прочтите [руководство для разработчиков](http://www.django-rest-framework.org/topics/contributing/) для получения информации о том, как склонировать репозиторий, запустить набор тестов и отправить изменения обратно в DRF.

## Поддержка

Для поддержки обратитесь в [группу обсуждения DRF](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework) или создайте вопрос на StackOverflow с указанием тэга ['django-rest-framework'](http://stackoverflow.com/questions/tagged/django-rest-framework).

Для уведомления об обновлениях, подпишитесь на нас в [Twitter](https://twitter.com/_tomchristie).

## Безопасность

Если вы уверены, что нашли пробел в безопасности, пожалуйста, **не создавайте публичный баг-репорт!**

Отправьте описание проблемы по почте [rest-framework-security@googlegroups.com](mailto:rest-framework-security@googlegroups.com). Руководители проекта будут работать с вами для решения любых подобных проблем.

-------------------
## Авторы перевода

* [Ilya Chichak](https://github.com/ilyachch/)

## Помощь в переводе
* [https://github.com/pymq](https://github.com/pymq)
* [https://github.com/rufatpro](https://github.com/rufatpro)
* [Dmitry Plaxunov](https://github.com/fojetin)

Пожалуйста, открывая Pull Request, указывайте меня в качестве ревьюера, так я буду узнавать об этом моментально.

Спасибо всем за помощь в переводе!

Перевод производится с помощью утилиты [md_docs-trans-app](https://github.com/ilyachch/md_docs-trans-app)

[sandbox]: https://restframework.herokuapp.com/
