# Django REST framework

Django REST framework - это мощный и гибкий инструментарий для создания веб API.

Некоторые причины, по которым вы можете выбрать Framework REST:

* [Web Browsable API](https://restframework.herokuapp.com/) - огромное удобство использования для ваших разработчиков.
* [Политики аутентификации](API-Guide/Authentication.md), включая пакеты для [OAuth1a] (API-Guide/Authentication/#django-rest-framework-oauth) и [OAuth2] (API-Guide/Authentication/#django-Oauth-toolkit).
* [Сериализация](API-Guide/Serializers.md), которая поддерживает как [ORM] (API-Guide/Serializers#ModelseRializer), так и [non-ORM](API-Guide/Serializers#Serializers) источники данных.
* Полностью настраиваемый - просто используйте [обычные представления-функции](API-Guide/Views#Function-Views), если вам не нужно [больше](API-Guide/Generic-Views.md) [мощных](API-Guide/Viewsets.md) [возможностей](API-Guide/Routers.md).
* Обширная документация и [великолепная поддержка сообщества](https://groups.google.com/forum/?fromGroups#!Forum/django-rest-framework).
* Используется и пользуется доверием международно признанным компаниям, включая [Mozilla](https://www.mozilla.org/en-us/about/), [Red Hat](https://www.redhat.com/), [heroku](https://www.heroku.com/) и [eventbrite](https://www.eventbrite.co.uk/about/).

## Требования

REST framework требует следующего:

* Python (3.6, 3.7, 3.8, 3.9, 3.10, 3.11)
* Django (2.2, 3.0, 3.1, 3.2, 4.0, 4.1)

Мы **настоятельно рекомендуем** и официально поддерживаем только последний патч-выпуск каждой серии Python и Django.

Следующие пакеты необязательны:

* [PyYAML](https://pypi.org/project/pyyaml/), [uritemplate](https://pypi.org/project/uritemplate/) (5.1+, 3.0.0+) - Поддержка генерации схем.
* [Markdown](https://pypi.org/project/markdown/) (3.0.0+) - поддержка Markdown для Web Browsable API.
* [Pygments](https://pypi.org/project/pygments/) (2.4.0+) - добавляет подстветку синтаксиса для Markdown.
* [django-filter](https://pypi.org/project/django-filter/) (1.0.1+) - поддержка фильтрации.
* [django-guardian](https://github.com/django-guardian/django-guardian) (1.1.1+) - Поддержка разрешений на уровне объекта.

## Установка

Установите, используя `pip`, включая любые дополнительные пакеты, которые вы хотите...

```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

... или клонируйте проект с GitHub.

```
git clone https://github.com/encode/django-rest-framework
```

Добавьте `'rest_framework'` в секцию `INSTALLED_APPS` ваших настроек.

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Если вы собираетесь использовать веб интерфейс API, вероятно, также захотите добавить представления для входа и выхода. Добавьте следующее в свой корневой `urls.py` файл.

```python
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls'))
]
```

Обратите внимание, что путь URL может быть любым.

## Пример

Давайте посмотрим на быстрый пример использования REST framework для создания простого API, основанного на модели.

Мы создадим API чтения-записи для доступа к информации о пользователях нашего проекта.

Любые глобальные настройки для API REST framework хранятся в одном словаре конфигурации с именем `REST_FRAMEWORK`. Начните с добавления следующего в свой модуль `settings.py`:

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

Мы готовы создать наш API. Вот кореневой модуль `urls.py` нашего проекта:

```python
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Сериализаторы определяют вид API.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# Наборы представлений (ViewSets) определяют поведение конечных точек.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Маршрутизаторы обеспечивают простой способ автоматического определения конфигурации URL.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Свяжите наше API с помощью автоматической маршрутизации URL.
# Кроме того, мы включаем URL-адреса входа для web интерфейса API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Теперь вы можете открыть API в своем браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/), и просмотреть свой новый API «Пользователи». Если вы воспользуетесь формой входа в верхнем правом углу, вы также сможете добавить, создавать и удалять пользователей из системы.

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

Для поддержки, пожалуйста, см. [группу обсуждения REST Framework](https://groups.google.com/forum/?fromGroups#!Forum/django-rest-framework), попробуйте канал `#restframe` на `irc.libera.chat`, или создайте вопрос на [Stack Overflow](https://stackoverflow.com/) с тэгом ['django-rest-framework'] (https://stackoverflow.com/questions/tagged/].

Для приоритетной поддержки, пожалуйста, зарегистрируйтесь на [профессиональный или премиальный спонсорский план](https://fund.django-rest-framework.org/topics/funding/).

## Безопасность

Если вы уверены, что нашли пробел в безопасности, пожалуйста, **не создавайте публичный баг-репорт!**

Отправьте описание проблемы по почте [security@djangoproject.com](mailto:security@djangoproject.com). Руководители проекта будут работать с вами для решения любых подобных проблем.

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
