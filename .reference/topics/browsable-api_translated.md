<!-- TRANSLATED by md-translate -->
# The Browsable API

# API для просмотра

> It is a profoundly erroneous truism... that we should cultivate the habit of thinking of what we are doing.  The precise opposite is the case.  Civilization advances by extending the number of important operations which we can perform without thinking about them.
>
> &mdash; [Alfred North Whitehead](https://en.wikiquote.org/wiki/Alfred_North_Whitehead), An Introduction to Mathematics (1911)

> Это глубоко ошибочный трюизм ... что мы должны развивать привычку думать о том, что мы делаем.
Точная противоположность имеет место.
Цивилизация продвигается, расширяя количество важных операций, которые мы можем выполнить, не задумываясь о них.
>
> & mdash;
[Альфред Норт -Уайтхед] (https://en.wikiquote.org/wiki/alfred_north_whitehead), введение в математику (1911)

API may stand for Application *Programming* Interface, but humans have to be able to read the APIs, too; someone has to do the programming.  Django REST Framework supports generating human-friendly HTML output for each resource when the `HTML` format is requested.  These pages allow for easy browsing of resources, as well as forms for submitting data to the resources using `POST`, `PUT`, and `DELETE`.

API может соответствовать приложению * Программирование * интерфейс, но люди тоже должны читать API;
Кто -то должен сделать программирование.
Django Rest Framework поддерживает генерацию HTML-вывода для человека для каждого ресурса, когда запрошен формат `html`.
Эти страницы позволяют легко просматривать ресурсы, а также формы для отправки данных в ресурсы с использованием «post», «put» и «Delete».

## URLs

## URLS

If you include fully-qualified URLs in your resource output, they will be 'urlized' and made clickable for easy browsing by humans.  The `rest_framework` package includes a [`reverse`](../api-guide/reverse.md) helper for this purpose.

Если вы включите полностью квалифицированные URL-адреса в свой вывод ресурса, они будут «наклейки» и сделаны кликбельными для легкого просмотра людьми.
Пакет `rest_framework` включает в себя помощник [` reverse`] (../ api-guide/reample.md) для этой цели.

## Formats

## форматы

By default, the API will return the format specified by the headers, which in the case of the browser is HTML.  The format can be specified using `?format=` in the request, so you can look at the raw JSON response in a browser by adding `?format=json` to the URL.  There are helpful extensions for viewing JSON in [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/) and [Chrome](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc).

По умолчанию API вернет формат, указанный заголовками, который в случае браузера является HTML.
Формат может быть указан с помощью `? Format =` в запросе, поэтому вы можете посмотреть на ответ Raw JSON в браузере, добавив `? Format = json` в URL.
Есть полезные расширения для просмотра JSON в [Firefox] (https://addons.mozilla.org/en-us/firefox/addon/jsonview/) и [chrome] (https://chrome.google.com/webstore/
Деталь/chklaanhfefbnpoihckbnefhakgolnmc).

## Customizing

## Настройка

The browsable API is built with [Twitter's Bootstrap](https://getbootstrap.com/) (v 3.3.5), making it easy to customize the look-and-feel.

API Browsable построен с помощью Bootstrap [witter] (https://getbootstrap.com/) (v 3.3.5), что облегчает настройку внешнего вида.

To customize the default style, create a template called `rest_framework/api.html` that extends from `rest_framework/base.html`.  For example:

Чтобы настроить стиль по умолчанию, создайте шаблон под названием `rest_framework/api.html`, который простирается от` rest_framework/base.html`.
Например:

**templates/rest_framework/api.html**

** шаблоны/rest_framework/api.html **

```
{% extends "rest_framework/base.html" %}

...  # Override blocks with required customizations
```

### Overriding the default theme

### Переоценка тема по умолчанию

To replace the default theme, add a `bootstrap_theme` block to your `api.html` and insert a `link` to the desired Bootstrap theme css file.  This will completely replace the included theme.

Чтобы заменить тему по умолчанию, добавьте блок `bootstrap_theme` в свой a api.html` и вставьте` ссылку в нужную файл CSS -файла Bootstrap.
Это полностью заменит включенную тему.

```
{% block bootstrap_theme %}
    <link rel="stylesheet" href="/path/to/my/bootstrap.css" type="text/css">
{% endblock %}
```

Suitable pre-made replacement themes are available at [Bootswatch](https://bootswatch.com/).  To use any of the Bootswatch themes, simply download the theme's `bootstrap.min.css` file, add it to your project, and replace the default one as described above.

Подходящие предварительные темы замены доступны по адресу [bootswatch] (https://bootswatch.com/).
Чтобы использовать любую из тем Bootswatch, просто загрузите файл темы `bootstrap.min.css

You can also change the navbar variant, which by default is `navbar-inverse`, using the `bootstrap_navbar_variant` block.  The empty `{% block bootstrap_navbar_variant %}{% endblock %}` will use the original Bootstrap navbar style.

Вы также можете изменить вариант Navbar, который по умолчанию является `navbar-enverse`, используя блок` bootstrap_navbar_variant`.
Пустое `{ % block bootstrap_navbar_variant %} { % endblock %}` будет использовать оригинальный стиль Navbar Bootstrap.

Full example:

Полный пример:

```
{% extends "rest_framework/base.html" %}

{% block bootstrap_theme %}
    <link rel="stylesheet" href="https://bootswatch.com/flatly/bootstrap.min.css" type="text/css">
{% endblock %}

{% block bootstrap_navbar_variant %}{% endblock %}
```

For more specific CSS tweaks than simply overriding the default bootstrap theme you can override the `style` block.

Для более конкретных настроек CSS, чем просто переопределение темы начальной загрузки по умолчанию, вы можете переопределить блок `style '.

---

![Cerulean theme](../img/cerulean.png)

! [Церулеанская тема] (../ img/cerulean.png)

*Screenshot of the bootswatch 'Cerulean' theme*

*Скриншот темы Bootswatch 'Cerulean'*

---

![Slate theme](../img/slate.png)

! [Slate Theme] (../ img/slate.png)

*Screenshot of the bootswatch 'Slate' theme*

*Снимок экрана из темы Bootswatch 'Slate'*

---

### Blocks

### блоки

All of the blocks available in the browsable API base template that can be used in your `api.html`.

Все блоки, доступные в базовом шаблоне API, которые можно использовать в вашем api.html`.

* `body`                       - The entire html `<body>`.
* `bodyclass`                  - Class attribute for the `<body>` tag, empty by default.
* `bootstrap_theme`            - CSS for the Bootstrap theme.
* `bootstrap_navbar_variant`   - CSS class for the navbar.
* `branding`                   - Branding section of the navbar, see [Bootstrap components](https://getbootstrap.com/2.3.2/components.html#navbar).
* `breadcrumbs`                - Links showing resource nesting, allowing the user to go back up the resources.  It's recommended to preserve these, but they can be overridden using the breadcrumbs block.
* `script`                     - JavaScript files for the page.
* `style`                      - CSS stylesheets for the page.
* `title`                      - Title of the page.
* `userlinks`                  - This is a list of links on the right of the header, by default containing login/logout links.  To add links instead of replace, use `{{ block.super }}` to preserve the authentication links.

* `body` - весь html` <body> `.
* `bodyclass` - атрибут класса для` <<body> `Tag, по умолчанию пусто.
* `bootstrap_theme` - CSS для темы начальной загрузки.
* `bootstrap_navbar_variant` - css class для Navbar.
* `Branding` - раздел брендинга Navbar, см.
* `Shantcrumbs` - ссылки, показывающие всасывание ресурсов, что позволяет пользователю вернуть ресурсы.
Рекомендуется сохранить их, но они могут быть переопределены с помощью блока хлебных крошек.
* `script` - файлы JavaScript для страницы.
* `style` - CSS StyleShips для страницы.
* `title` - заголовок страницы.
* `userLinks` - это список ссылок справа от заголовка, по умолчанию, содержащим ссылки в систему/вход в систему.
Чтобы добавить ссылки вместо замены, используйте `{{block.super}}`, чтобы сохранить ссылки аутентификации.

#### Components

#### Составные части

All of the standard [Bootstrap components](https://getbootstrap.com/2.3.2/components.html) are available.

Все стандартные [Bootstrap Components] (https://getbootstrap.com/2.3.2/components.html) доступны.

#### Tooltips

#### Потиски инструментов

The browsable API makes use of the Bootstrap tooltips component.  Any element with the `js-tooltip` class and a `title` attribute has that title content will display a tooltip on hover events.

API Browsable использует компонент подсказки Bootstrap Tools.
В любом элементе с классом `js-tooltip` и атрибутом« title »есть этот контент заголовка, отображает подсказку на событиях Hover.

### Login Template

### Шаблон входа в систему

To add branding and customize the look-and-feel of the login template, create a template called `login.html` and add it to your project, eg: `templates/rest_framework/login.html`.  The template should extend from `rest_framework/login_base.html`.

Чтобы добавить брендинг и настроить внешний вид шаблона входа в систему, создайте шаблон под названием `login.html` и добавьте его в свой проект, например:` Templates/rest_framework/login.html`.
Шаблон должен простираться от `rest_framework/login_base.html`.

You can add your site name or branding by including the branding block:

Вы можете добавить название своего сайта или брендинг, включив блок брендинга:

```
{% extends "rest_framework/login_base.html" %}

{% block branding %}
    <h3 style="margin: 0 0 20px;">My Site Name</h3>
{% endblock %}
```

You can also customize the style by adding the `bootstrap_theme` or `style` block similar to `api.html`.

Вы также можете настроить стиль, добавив блок `bootstrap_theme` или` style`, похожий на `api.html`.

### Advanced Customization

### расширенная настройка

#### Context

#### Контекст

The context that's available to the template:

Контекст, который доступен для шаблона:

* `allowed_methods`     : A list of methods allowed by the resource
* `api_settings`        : The API settings
* `available_formats`   : A list of formats allowed by the resource
* `breadcrumblist`      : The list of links following the chain of nested resources
* `content`             : The content of the API response
* `description`         : The description of the resource, generated from its docstring
* `name`                : The name of the resource
* `post_form`           : A form instance for use by the POST form (if allowed)
* `put_form`            : A form instance for use by the PUT form (if allowed)
* `display_edit_forms`  : A boolean indicating whether or not POST, PUT and PATCH forms will be displayed
* `request`             : The request object
* `response`            : The response object
* `version`             : The version of Django REST Framework
* `view`                : The view handling the request
* `FORMAT_PARAM`        : The view can accept a format override
* `METHOD_PARAM`        : The view can accept a method override

* `Alling_methods`: список методов, разрешенных ресурсом
* `api_settings`: настройки API
* `Доступно_FORMATS`: список форматов, разрешенных ресурсом
* `Drancrumblist`: список ссылок, следуя цепочке вложенных ресурсов
* `content`: содержание ответа API
* `description`: описание ресурса, сгенерированное из его доктора
* `name`: имя ресурса
* `post_form`: экземпляр формы для использования в форме Post (если разрешено)
* `put_form`: экземпляр формы для использования формой PUT (если разрешено)
* `display_edit_forms`: булево, указывающая, будут ли отображаться формы публикации, положения и исправлений
* `request`: объект запроса
* `response`: объект ответа
* `version`: версия Django Rest Framework
* `view`: представление обрабатывает запрос
* `Format_param`: представление может принять переопределение формата
* `Method_param`: представление может принять переопределение метода

You can override the `BrowsableAPIRenderer.get_context()` method to customise the context that gets passed to the template.

Вы можете переопределить метод `browsableApirenderer.get_context ()` для настройки контекста, который передается в шаблон.

#### Not using base.html

#### не использует base.html

For more advanced customization, such as not having a Bootstrap basis or tighter integration with the rest of your site, you can simply choose not to have `api.html` extend `base.html`.  Then the page content and capabilities are entirely up to you.

Для более продвинутой настройки, такой как отсутствие начальной базы или более жесткой интеграции с остальной частью вашего сайта, вы можете просто выбрать, чтобы не иметь `api.html` Extend` base.html`.
Тогда контент и возможности страницы полностью зависит от вас.

#### Handling `ChoiceField` with large numbers of items.

#### Обработка `Choicefield` с большим количеством предметов.

When a relationship or `ChoiceField` has too many items, rendering the widget containing all the options can become very slow, and cause the browsable API rendering to perform poorly.

Когда отношения или «Choicefield» имеют слишком много элементов, визуализация, содержащая все варианты, может стать очень медленным и привести к тому, что рендеринг API просмотра работает плохо.

The simplest option in this case is to replace the select input with a standard text input. For example:

Самый простой вариант в этом случае - заменить ввод выбора стандартным текстовым вводом.
Например:

```
author = serializers.HyperlinkedRelatedField(
    queryset=User.objects.all(),
    style={'base_template': 'input.html'}
)
```

#### Autocomplete

#### Автозаполнение

An alternative, but more complex option would be to replace the input with an autocomplete widget, that only loads and renders a subset of the available options as needed. If you need to do this you'll need to do some work to build a custom autocomplete HTML template yourself.

Альтернативой, но более сложным вариантом будет заменить вход на виджет автозаполнения, который загружает только и делает подмножество доступных параметров по мере необходимости.
Если вам нужно это сделать, вам нужно сделать некоторую работу, чтобы самостоятельно создать пользовательский шаблон HTML автозаполнения.

There are [a variety of packages for autocomplete widgets](https://www.djangopackages.com/grids/g/auto-complete/), such as [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light), that you may want to refer to. Note that you will not be able to simply include these components as standard widgets, but will need to write the HTML template explicitly. This is because REST framework 3.0 no longer supports the `widget` keyword argument since it now uses templated HTML generation.

Существует [различные пакеты для автоматических виджетов] (https://www.djangopackages.com/grids/g/auto-complete/), такие как [django-autocomplete-light] (https://github.com/
yourlabs/django-autocoplete-light), на который вы можете обратиться.
Обратите внимание, что вы не сможете просто включить эти компоненты в качестве стандартных виджетов, но вам нужно будет явно написать шаблон HTML.
Это связано с тем, что Framework REST 3.0 больше не поддерживает аргумент ключевого слова «виджета», поскольку теперь он использует шаблонную HTML -генерацию.

---