<!-- TRANSLATED by md-translate -->
# Django REST framework

![Logo by Jake 'Sid' Smith](https://github.com/encode/django-rest-framework/raw/master/docs/img/logo.png)

Django REST framework - это мощный и гибкий набор инструментов для создания Web API.

Некоторые причины, по которым вы можете захотеть использовать REST framework:

* [Просматриваемый API](https://restframework.herokuapp.com/) - огромный выигрыш в удобстве использования для ваших разработчиков.
* [Политики аутентификации](api-guide/authentication.md), включая пакеты для [OAuth1a][oauth1-section] и [OAuth2][oauth2-section].
* [Сериализация](api-guide/serializers.md), поддерживающая как [ORM][modelserializer-section], так и [non-ORM][api-guide/serializers#serializers] источники данных.
* Настраивается все - просто используйте [обычные представления на основе функций](api-guide/views#function-based-views), если вам не нужны [более](api-guide/generic-views.md) [мощные][viewsets][features][routers].
* Обширная документация и [отличная поддержка сообщества](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework).
* Используется и пользуется доверием всемирно известных компаний, включая [Mozilla](https://www.mozilla.org/en-us/about/), [Red Hat](https://www.redhat.com/), [Heroku](https://www.heroku.com/) и [Eventbrite](https://www.eventbrite.co.uk/about/).

---

## Требования

REST framework требует следующего:

* Python (3.6, 3.7, 3.8, 3.9, 3.10, 3.11)
* Django (2.2, 3.0, 3.1, 3.2, 4.0, 4.1)

Мы **настоятельно рекомендуем** и официально поддерживаем только последние выпуски патчей каждой версии Python и Django.

Следующие пакеты являются необязательными:

* [PyYAML](https://pypi.org/project/pyyaml/), [uritemplate](https://pypi.org/project/uritemplate/) (5.1+, 3.0.0+) - Поддержка генерации схем.
* [Markdown](https://pypi.org/project/markdown/) (3.0.0+) - Поддержка Markdown для просматриваемого API.
* [Pygments](https://pypi.org/project/pygments/) (2.4.0+) - Добавление подсветки синтаксиса в обработку Markdown.
* [django-filter](https://pypi.org/project/django-filter/) (1.0.1+) - Поддержка фильтрации.
* [django-guardian](https://github.com/django-guardian/django-guardian) (1.1.1+) - Поддержка разрешений на уровне объектов.

## Установка

Установите с помощью `pip`, включая все дополнительные пакеты, которые вы хотите...

```bash
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

...или клонируйте проект с github.

```bash
git clone https://github.com/encode/django-rest-framework
```

Добавьте `'rest_framework'` в настройку `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Если вы планируете использовать просматриваемый API, вы, вероятно, также захотите добавить представления входа и выхода из системы REST framework. Добавьте следующее в ваш корневой файл `urls.py`.

```python
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls'))
]
```

Обратите внимание, что путь URL может быть любым, какой вы захотите.

## Пример

Давайте рассмотрим быстрый пример использования REST-фреймворка для создания простого API с поддержкой модели.

Мы создадим API с функцией чтения-записи для доступа к информации о пользователях нашего проекта.

Все глобальные настройки для API REST-фреймворка хранятся в одном конфигурационном словаре с именем `REST_FRAMEWORK`. Начните с добавления следующих параметров в модуль `settings.py`:

```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

Не забудьте убедиться, что вы также добавили `rest_framework` в `INSTALLED_APPS`.

Теперь мы готовы к созданию нашего API. Вот корневой модуль нашего проекта `urls.py`:

```python
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Теперь вы можете открыть API в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/) и просмотреть новых "пользователей" API. Если вы используете элемент управления входом в систему в правом верхнем углу, вы также сможете добавлять, создавать и удалять пользователей из системы.

## Быстрый старт

Не можете дождаться начала работы? Руководство [quickstart](quick-start.md) - это самый быстрый способ начать работу и создавать API с помощью REST framework.

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

Смотрите [руководство для разработчиков][https://www.django-rest-framework.org/community/contributing/] для получения информации о том, как клонировать репозиторий, запустить набор тестов и внести изменения в REST Framework.

## Поддержка

За поддержкой обращайтесь в [REST framework discussion group](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework), попробуйте использовать канал `#restframework` на `irc.libera.chat`, или задайте вопрос на [Stack Overflow](https://stackoverflow.com/), обязательно указав тег ['django-rest-framework'](https://stackoverflow.com/questions/tagged/django-rest-framework).

Для получения приоритетной поддержки подпишитесь на [профессиональный или премиум спонсорский план](https://fund.django-rest-framework.org/topics/funding/).

## Безопасность

Вопросы безопасности решаются под руководством [Django security team](https://www.djangoproject.com/foundation/teams/#security-team).

**Пожалуйста, сообщайте о проблемах безопасности по электронной почте security@djangoproject.com**.

После этого сопровождающие проекта будут работать с вами над решением любых вопросов, если потребуется, до обнародования информации.

---
## Авторы перевода

* [Ilya Chichak](https://github.com/ilyachch/)

## Помощь в переводе
* [https://github.com/pymq](https://github.com/pymq)
* [https://github.com/rufatpro](https://github.com/rufatpro)
* [Dmitry Plaxunov](https://github.com/fojetin)

Спасибо всем за помощь в переводе!

Перевод производится с помощью утилиты [md_docs-trans-app](https://github.com/ilyachch/md_docs-trans-app)
