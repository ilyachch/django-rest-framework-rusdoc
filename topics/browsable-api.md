<!-- TRANSLATED by md-translate -->

# The Browsable API

# Browsable API

> It is a profoundly erroneous truism... that we should cultivate the habit of thinking of what we are doing. The precise opposite is the case. Civilization advances by extending the number of important operations which we can perform without thinking about them.
>
> — [Alfred North Whitehead](https://en.wikiquote.org/wiki/Alfred_North_Whitehead), An Introduction to Mathematics (1911)

> Это глубоко ошибочный трюизм... что мы должны культивировать привычку думать о том, что мы делаем. Дело обстоит прямо противоположным образом. Цивилизация развивается благодаря расширению числа важных операций, которые мы можем выполнять, не задумываясь о них.
>
> - \[Альфред Норт Уайтхед\] (https://en.wikiquote.org/wiki/Alfred_North_Whitehead), Введение в математику (1911)

API may stand for Application *Programming* Interface, but humans have to be able to read the APIs, too; someone has to do the programming. Django REST Framework supports generating human-friendly HTML output for each resource when the `HTML` format is requested. These pages allow for easy browsing of resources, as well as forms for submitting data to the resources using `POST`, `PUT`, and `DELETE`.

API может означать интерфейс прикладного *программирования*, но люди тоже должны уметь читать API; кто-то должен заниматься программированием. Django REST Framework поддерживает генерацию удобного для человека HTML вывода для каждого ресурса, когда запрашивается формат `HTML`. Эти страницы позволяют легко просматривать ресурсы, а также формы для отправки данных на ресурсы с помощью `POST`, `PUT` и `DELETE`.

## URLs

## URLs

If you include fully-qualified URLs in your resource output, they will be 'urlized' and made clickable for easy browsing by humans. The `rest_framework` package includes a [`reverse`](../api-guide/reverse.md) helper for this purpose.

Если вы включите полные URL-адреса в вывод ресурсов, они будут "урлизованы" и станут кликабельными для удобного просмотра людьми. Для этого в пакет `rest_framework` включен помощник [`reverse`](../api-guide/reverse.md).

## Formats

## Форматы

By default, the API will return the format specified by the headers, which in the case of the browser is HTML. The format can be specified using `?format=` in the request, so you can look at the raw JSON response in a browser by adding `?format=json` to the URL. There are helpful extensions for viewing JSON in [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/) and [Chrome](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc).

По умолчанию API возвращает формат, указанный в заголовках, который в случае браузера является HTML. Формат может быть указан с помощью `?format=` в запросе, поэтому вы можете просмотреть необработанный JSON-ответ в браузере, добавив `?format=json` к URL. Существуют полезные расширения для просмотра JSON в [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/) и [Chrome](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc).

## Customizing

## Настройка

The browsable API is built with [Twitter's Bootstrap](https://getbootstrap.com/) (v 3.4.1), making it easy to customize the look-and-feel.

Просматриваемый API построен с использованием [Twitter's Bootstrap](https://getbootstrap.com/) (v 3.4.1), что позволяет легко настраивать внешний вид.

To customize the default style, create a template called `rest_framework/api.html` that extends from `rest_framework/base.html`. For example:

Чтобы настроить стиль по умолчанию, создайте шаблон `rest_framework/api.html`, который расширяется от `rest_framework/base.html`. Например:

**templates/rest_framework/api.html**

**templates/rest_framework/api.html**

```
{% extends "rest_framework/base.html" %}

...  # Override blocks with required customizations
```

### Overriding the default theme

### Переопределение темы по умолчанию

To replace the default theme, add a `bootstrap_theme` block to your `api.html` and insert a `link` to the desired Bootstrap theme css file. This will completely replace the included theme.

Чтобы заменить тему по умолчанию, добавьте блок `bootstrap_theme` в ваш `api.html` и вставьте `ссылку` на нужный css-файл темы Bootstrap. Это полностью заменит включенную тему.

```
{% block bootstrap_theme %}
    <link rel="stylesheet" href="/path/to/my/bootstrap.css" type="text/css">
{% endblock %}
```

Suitable pre-made replacement themes are available at [Bootswatch](https://bootswatch.com/). To use any of the Bootswatch themes, simply download the theme's `bootstrap.min.css` file, add it to your project, and replace the default one as described above. Make sure that the Bootstrap version of the new theme matches that of the default theme.

Подходящие готовые темы для замены доступны на сайте [Bootswatch](https://bootswatch.com/). Чтобы использовать любую из тем Bootswatch, просто скачайте файл `bootstrap.min.css` этой темы, добавьте его в свой проект и замените тему по умолчанию, как описано выше. Убедитесь, что версия Bootstrap новой темы совпадает с версией темы по умолчанию.

You can also change the navbar variant, which by default is `navbar-inverse`, using the `bootstrap_navbar_variant` block. The empty `{% block bootstrap_navbar_variant %}{% endblock %}` will use the original Bootstrap navbar style.

Вы также можете изменить вариант navbar, который по умолчанию является `navbar-inverse`, используя блок `bootstrap_navbar_variant`. Пустой блок `{% block bootstrap_navbar_variant %}{% endblock %}` будет использовать оригинальный стиль навигационной панели Bootstrap.

Full example:

Полный пример:

```
{% extends "rest_framework/base.html" %}

{% block bootstrap_theme %}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@3.4.1/flatly/bootstrap.min.css" type="text/css">
{% endblock %}

{% block bootstrap_navbar_variant %}{% endblock %}
```

For more specific CSS tweaks than simply overriding the default bootstrap theme you can override the `style` block.

Для более специфических настроек CSS, чем просто переопределение темы bootstrap по умолчанию, вы можете переопределить блок `style`.

______________________________________________________________________

![Cerulean theme](../img/cerulean.png)

![Cerulean theme](../img/cerulean.png)

*Screenshot of the bootswatch 'Cerulean' theme*

\*Скриншот загрузочной темы "Cerulean".

______________________________________________________________________

![Slate theme](../img/slate.png)

![Тема Slate](../img/slate.png)

*Screenshot of the bootswatch 'Slate' theme*

*Скриншот темы bootswatch 'Slate'*.

______________________________________________________________________

### Blocks

### Блоки

All of the blocks available in the browsable API base template that can be used in your `api.html`.

Все блоки, доступные в просматриваемом базовом шаблоне API, которые можно использовать в вашем `api.html`.

- `body` - The entire html `<body>`.

- `bodyclass` - Class attribute for the `<body>` tag, empty by default.

- `bootstrap_theme` - CSS for the Bootstrap theme.

- `bootstrap_navbar_variant` - CSS class for the navbar.

- `branding` - Branding section of the navbar, see [Bootstrap components](https://getbootstrap.com/2.3.2/components.html#navbar).

- `breadcrumbs` - Links showing resource nesting, allowing the user to go back up the resources. It's recommended to preserve these, but they can be overridden using the breadcrumbs block.

- `script` - JavaScript files for the page.

- `style` - CSS stylesheets for the page.

- `title` - Title of the page.

- `userlinks` - This is a list of links on the right of the header, by default containing login/logout links. To add links instead of replace, use `{{ block.super }}` to preserve the authentication links.

- `body` - Весь html `<body>`.

- `bodyclass` - Атрибут класса для тега `<body>`, по умолчанию пустой.

- `bootstrap_theme` - CSS для темы Bootstrap.

- `bootstrap_navbar_variant` - CSS класс для навигационной панели.

- `branding` - Раздел брендинга navbar, см. [Bootstrap components](https://getbootstrap.com/2.3.2/components.html#navbar).

- `хлебные крошки` - Ссылки, показывающие вложенность ресурсов, позволяющие пользователю вернуться назад по ресурсам. Рекомендуется сохранять их, но их можно переопределить с помощью блока хлебных крошек.

- `script` - файлы JavaScript для страницы.

- `style` - Таблицы стилей CSS для страницы.

- `title` - Заголовок страницы.

- `userlinks` - Список ссылок справа от заголовка, по умолчанию содержит ссылки для входа/выхода. Чтобы добавить ссылки вместо замены, используйте `{{ block.super }}`, чтобы сохранить ссылки авторизации.

#### Components

#### Компоненты

All of the standard [Bootstrap components](https://getbootstrap.com/2.3.2/components.html) are available.

Доступны все стандартные [Bootstrap-компоненты](https://getbootstrap.com/2.3.2/components.html).

#### Tooltips

#### Всплывающие подсказки

The browsable API makes use of the Bootstrap tooltips component. Any element with the `js-tooltip` class and a `title` attribute has that title content will display a tooltip on hover events.

API с возможностью просмотра использует компонент всплывающих подсказок Bootstrap. Любой элемент с классом `js-tooltip` и атрибутом `title` имеет содержание заголовка, который будет отображать всплывающую подсказку при наведении.

### Login Template

### Шаблон входа в систему

To add branding and customize the look-and-feel of the login template, create a template called `login.html` and add it to your project, eg: `templates/rest_framework/login.html`. The template should extend from `rest_framework/login_base.html`.

Чтобы добавить брендинг и настроить внешний вид шаблона входа, создайте шаблон `login.html` и добавьте его в свой проект, например: `templates/rest_framework/login.html`. Шаблон должен расширяться от `rest_framework/login_base.html`.

You can add your site name or branding by including the branding block:

Вы можете добавить название своего сайта или брендинг, включив блок брендинга:

```
{% extends "rest_framework/login_base.html" %}

{% block branding %}
    <h3 style="margin: 0 0 20px;">My Site Name</h3>
{% endblock %}
```

You can also customize the style by adding the `bootstrap_theme` or `style` block similar to `api.html`.

Вы также можете настроить стиль, добавив блок `bootstrap_theme` или `style`, аналогичный `api.html`.

### Advanced Customization

### Расширенная настройка

#### Context

#### Контекст

The context that's available to the template:

Контекст, доступный шаблону:

- `allowed_methods` : A list of methods allowed by the resource

- `api_settings` : The API settings

- `available_formats` : A list of formats allowed by the resource

- `breadcrumblist` : The list of links following the chain of nested resources

- `content` : The content of the API response

- `description` : The description of the resource, generated from its docstring

- `name` : The name of the resource

- `post_form` : A form instance for use by the POST form (if allowed)

- `put_form` : A form instance for use by the PUT form (if allowed)

- `display_edit_forms` : A boolean indicating whether or not POST, PUT and PATCH forms will be displayed

- `request` : The request object

- `response` : The response object

- `version` : The version of Django REST Framework

- `view` : The view handling the request

- `FORMAT_PARAM` : The view can accept a format override

- `METHOD_PARAM` : The view can accept a method override

- `allowed_methods` : Список методов, разрешенных ресурсу

- `api_settings` : Настройки API

- `available_formats` : Список форматов, разрешенных ресурсом

- `breadcrumblist` : Список ссылок, следующих за цепочкой вложенных ресурсов.

- `content` : Содержание ответа API

- `description` : Описание ресурса, сгенерированное из его doc-строки.

- `name` : Название ресурса

- `post_form` : Экземпляр формы для использования POST-формой (если разрешено)

- `put_form` : Экземпляр формы для использования формой PUT (если разрешено)

- `display_edit_forms` : Булево значение, указывающее, будут ли отображаться формы POST, PUT и PATCH.

- `request` : Объект запроса

- `response` : Объект ответа

- `version` : Версия Django REST Framework

- `view` : Представление, обрабатывающее запрос.

- `FORMAT_PARAM` : Представление может принимать переопределение формата

- `METHOD_PARAM` : Представление может принимать переопределение метода

You can override the `BrowsableAPIRenderer.get_context()` method to customise the context that gets passed to the template.

Вы можете переопределить метод `BrowsableAPIRenderer.get_context()`, чтобы настроить контекст, передаваемый шаблону.

#### Not using base.html

#### Не используется файл base.html

For more advanced customization, such as not having a Bootstrap basis or tighter integration with the rest of your site, you can simply choose not to have `api.html` extend `base.html`. Then the page content and capabilities are entirely up to you.

Для более продвинутой настройки, например, без основы Bootstrap или более тесной интеграции с остальной частью вашего сайта, вы можете просто не использовать `api.html` и `base.html`. Тогда содержание и возможности страницы будут полностью зависеть от вас.

#### Handling `ChoiceField` with large numbers of items.

#### Обработка `ChoiceField` с большим количеством элементов.

When a relationship or `ChoiceField` has too many items, rendering the widget containing all the options can become very slow, and cause the browsable API rendering to perform poorly.

Когда отношения или `ChoiceField` имеют слишком много элементов, рендеринг виджета, содержащего все опции, может стать очень медленным и привести к плохой работе рендеринга API с возможностью просмотра.

The simplest option in this case is to replace the select input with a standard text input. For example:

Самый простой вариант в этом случае - заменить вход select на стандартный текстовый вход. Например:

```
author = serializers.HyperlinkedRelatedField(
    queryset=User.objects.all(),
    style={'base_template': 'input.html'}
)
```

#### Autocomplete

#### Автозаполнение

An alternative, but more complex option would be to replace the input with an autocomplete widget, that only loads and renders a subset of the available options as needed. If you need to do this you'll need to do some work to build a custom autocomplete HTML template yourself.

Альтернативным, но более сложным вариантом может быть замена ввода виджетом автозаполнения, который загружает и отображает только подмножество доступных вариантов по мере необходимости. Если вам нужно сделать это, вам придется поработать над созданием собственного HTML-шаблона автозаполнения.

There are [a variety of packages for autocomplete widgets](https://www.djangopackages.com/grids/g/auto-complete/), such as [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light), that you may want to refer to. Note that you will not be able to simply include these components as standard widgets, but will need to write the HTML template explicitly. This is because REST framework 3.0 no longer supports the `widget` keyword argument since it now uses templated HTML generation.

Существует [множество пакетов для виджетов автозаполнения](https://www.djangopackages.com/grids/g/auto-complete/), например [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light), к которым вы можете обратиться. Обратите внимание, что вы не сможете просто включить эти компоненты в качестве стандартных виджетов, а должны будете написать HTML-шаблон в явном виде. Это связано с тем, что REST framework 3.0 больше не поддерживает аргумент ключевого слова `widget`, поскольку теперь он использует шаблонизированную генерацию HTML.

______________________________________________________________________
