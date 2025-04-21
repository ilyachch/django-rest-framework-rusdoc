<!-- TRANSLATED by md-translate -->
# Browsable API

> Это глубоко ошибочный трюизм... что мы должны культивировать привычку думать о том, что мы делаем. Все обстоит с точностью до наоборот. Цивилизация развивается за счет увеличения числа важных операций, которые мы можем выполнять, не задумываясь о них.
>
> &mdash; [Альфред Норт Уайтхед](https://en.wikiquote.org/wiki/Alfred_North_Whitehead), Введение в математику (1911)

API может означать интерфейс прикладного _программирования_(Application _Programming_ Interface), но люди тоже должны уметь читать API; кто-то должен заниматься программированием. DRF поддерживает генерацию удобного для человека HTML-вывода для каждого ресурса при запросе формата `HTML`. Эти страницы позволяют легко просматривать ресурсы, а также содержат формы для отправки данных на ресурсы с помощью `POST`, `PUT` и `DELETE`.

## URLs

Если вы включите в вывод ресурсов полностью определенные URL, они будут "урлизованы" и сделаны кликабельными для удобства просмотра человеком. Для этого в пакет `rest_framework` включен помощник [`reverse`](../api-guide/reverse.md).

## Форматы

По умолчанию API возвращает формат, указанный в заголовках, который в случае браузера является HTML. Формат может быть указан с помощью `?format=` в запросе, так что вы можете просмотреть необработанный JSON-ответ в браузере, добавив `?format=json` к URL. Существуют полезные расширения для просмотра JSON в [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/) и [Chrome](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc).

## Аутентификация

Чтобы быстро добавить аутентификацию в Web-интерфейсе API, добавьте маршруты с именами `"login"` и `"logout"` в пространстве имен `"rest_framework"`. DRF предоставляет для этого маршруты по умолчанию, которые вы можете добавить в свой urlconf:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
```

## Настройка

Web-интерфейс API построен с использованием [Twitter's Bootstrap](https://getbootstrap.com/) (v 3.4.1), что позволяет легко настроить внешний вид и функциональность.

Чтобы настроить стиль по умолчанию, создайте шаблон `rest_framework/api.html`, который расширяет `rest_framework/base.html`. Например:

**templates/rest_framework/api.html**

```html
{% extends "rest_framework/base.html" %}

...  # Override blocks with required customizations
```

### Переопределение темы по умолчанию

Чтобы заменить тему по умолчанию, добавьте блок `bootstrap_theme` в ваш `api.html` и вставьте `ссылку` на нужный css-файл темы Bootstrap. Это полностью заменит включенную тему.

```html
{% block bootstrap_theme %}
    <link rel="stylesheet" href="/path/to/my/bootstrap.css" type="text/css">
{% endblock %}
```

Подходящие готовые темы для замены доступны на сайте [Bootswatch](https://bootswatch.com/). Чтобы использовать любую из тем Bootswatch, просто скачайте файл `bootstrap.min.css` этой темы, добавьте его в свой проект и замените тему по умолчанию, как описано выше. Убедитесь, что версия Bootstrap новой темы совпадает с версией темы по умолчанию.

Вы также можете изменить вариант навигационной панели, которая по умолчанию имеет значение `navbar-inverse`, с помощью блока `bootstrap_navbar_variant`. Пустой блок `{% block bootstrap_navbar_variant %}{% endblock %}` будет использовать оригинальный стиль навигационной панели Bootstrap.

Полный пример:

```html
{% extends "rest_framework/base.html" %}

{% block bootstrap_theme %}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@3.4.1/flatly/bootstrap.min.css" type="text/css">
{% endblock %}

{% block bootstrap_navbar_variant %}{% endblock %}
```

Для более специфических CSS-настроек, чем просто переопределение темы bootstrap по умолчанию, вы можете переопределить блок `style`.

---

![Cerulean theme](https://github.com/encode/django-rest-framework/raw/master/docs/img/cerulean.png)

*Скриншот темы "Cerulean"*

---

![Slate theme](https://github.com/encode/django-rest-framework/raw/master/docs/img/slate.png)

*Скриншот темы "Slate"*

---

### Пакеты сторонних разработчиков для настройки

Вы можете использовать сторонние пакеты для кастомизации, а не делать это самостоятельно. Вот 3 пакета для настройки API:

* [drf-restwind](https://github.com/youzarsiph/drf-restwind) - Современное переосмысление REST-фреймворка Django использует TailwindCSS и DaisyUI для создания гибких и настраиваемых решений пользовательского интерфейса с минимальными усилиями по кодированию.
* [drf-redesign](https://github.com/youzarsiph/drf-redesign) - Пакет для настройки API с помощью Bootstrap 5. Современный и элегантный дизайн, поддержка темного режима.
* [drf-material](https://github.com/youzarsiph/drf-material) - Материальный дизайн для Django REST Framework.

---

![API Root](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-rw-api-root.png)

![List View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-rw-list-view.png)

![Detail View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-rw-detail-view.png)

*Скриншоты drf-restwind*

---

![API Root](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-r-api-root.png)

![List View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-r-list-view.png)

![Detail View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-r-detail-view.png)

*Скриншоты drf-redesign*

---

![API Root](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-m-api-root.png)

![List View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-m-list-view.png)

![Detail View](https://github.com/encode/django-rest-framework/raw/master/docs/img/drf-m-detail-view.png)

*Скриншоты drf-material*

---

### Блоки

Все блоки, доступные в базовом шаблоне Web-интерфейса API, которые можно использовать в вашем `api.html`.

* `body` - Весь html-тег `<body>`.
* `bodyclass` - Атрибут класса для тега `<body>`, по умолчанию пустой.
* `bootstrap_theme` - CSS для темы Bootstrap.
* `bootstrap_navbar_variant` - CSS-класс для навигационной панели.
* `branding` - Раздел брендирования navbar, см. [Bootstrap components](https://getbootstrap.com/2.3.2/components.html#navbar).
* `breadcrumbs` - Ссылки, показывающие вложенность ресурсов, позволяющие пользователю вернуться к ним. Рекомендуется сохранять их, но их можно переопределить с помощью блока breadcrumbs.
* `script` - Файлы JavaScript для страницы.
* `style` - Таблицы стилей CSS для страницы.
* `title` - Заголовок страницы.
* `userlinks` - Список ссылок справа от заголовка, по умолчанию содержит ссылки на вход/выход. Чтобы добавить ссылки вместо замены, используйте `{{ block.super }}`, чтобы сохранить ссылки аутентификации.

#### Компоненты

Доступны все стандартные [Bootstrap-компоненты](https://getbootstrap.com/2.3.2/components.html).

#### Всплывающие подсказки

Web-интерфейс API использует компонент Bootstrap tooltips. Любой элемент с классом `js-tooltip` и атрибутом `title` имеет содержание заголовка, который будет отображать всплывающую подсказку при наведении.

### Шаблон для входа в систему

Чтобы добавить брендинг и настроить внешний вид шаблона входа в систему, создайте шаблон `login.html` и добавьте его в свой проект, например: `templates/rest_framework/login.html`. Шаблон должен расширяться от `rest_framework/login_base.html`.

Вы можете добавить название своего сайта или брендинг, включив блок брендинга:

```html
{% extends "rest_framework/login_base.html" %}

{% block branding %}
    <h3 style="margin: 0 0 20px;">My Site Name</h3>
{% endblock %}
```

Вы также можете настроить стиль, добавив блок `bootstrap_theme` или `style`, аналогичный `api.html`.

### Расширенная настройка

#### Контекст

Контекст, доступный шаблону:

* `allowed_methods` : Список методов, разрешенных ресурсу
* `api_settings` : Настройки API
* `available_formats` : Список форматов, разрешенных ресурсом
* `breadcrumblist` : Список ссылок, следующих по цепочке вложенных ресурсов
* `content` : Содержание ответа API
* `description` : Описание ресурса, сгенерированное из его docstring
* `name` : Название ресурса
* `post_form` : Экземпляр формы для использования POST-формой (если разрешено)
* `put_form` : Экземпляр формы для использования PUT-формой (если разрешено)
* `display_edit_forms` : Булево значение, указывающее, будут ли отображаться формы POST, PUT и PATCH.
* `request` : Объект запроса
* `response` : Объект ответа
* `version` : Версия Django REST Framework
* `view` : Представление, обрабатывающее запрос
* `FORMAT_PARAM` : Представление может принимать переопределение формата
* `METHOD_PARAM` : Представление может принимать переопределение метода

Вы можете переопределить метод `BrowsableAPIRenderer.get_context()`, чтобы настроить контекст, передаваемый в шаблон.

#### Неиспользование файла base.html

Для более продвинутой настройки, например, без основы Bootstrap или более тесной интеграции с остальным сайтом, вы можете просто убрать в `api.html` расширение `base.html`. Тогда содержание и возможности страницы будут зависеть только от вас.

#### Обработка `ChoiceField` с большим количеством элементов.

Когда в отношениях или `ChoiceField` слишком много элементов, рендеринг виджета, содержащего все варианты, может стать очень медленным, что приведет к плохой работе рендеринга Web-интерфейса API.

Самый простой вариант в этом случае - заменить виджет select на стандартный текстовый виджет. Например:

```python
author = serializers.HyperlinkedRelatedField(
    queryset=User.objects.all(),
    style={'base_template': 'input.html'}
)
```

#### Автозаполнение

Альтернативным, но более сложным вариантом будет замена виджета ввода виджетом автозаполнения, который будет загружать и отображать только подмножество доступных вариантов по мере необходимости. Если вам нужно сделать это, вам придется потрудиться, чтобы создать собственный HTML-шаблон автозаполнения.

Существует [множество пакетов для виджетов автозаполнения](https://www.djangopackages.com/grids/g/auto-complete/), например [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light), к которым вы можете обратиться. Обратите внимание, что вы не сможете просто включить эти компоненты в качестве стандартных виджетов, а должны будете явно написать HTML-шаблон. Это связано с тем, что REST framework 3.0 больше не поддерживает именованный аргумент `widget`, так как теперь он использует шаблонизацию HTML.
