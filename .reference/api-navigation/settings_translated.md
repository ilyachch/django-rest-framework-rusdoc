<!-- TRANSLATED by md-translate -->
---

source:

источник:

* settings.py

* settings.py

---

# Settings

# Настройки

> Namespaces are one honking great idea - let's do more of those!
>
> — [The Zen of Python][cite]

> Пространства имен - это отличная идея - давайте делать их больше!
>
> - [The Zen of Python][cite]

Configuration for REST framework is all namespaced inside a single Django setting, named `REST_FRAMEWORK`.

Конфигурация для фреймворка REST находится в едином пространстве имен в настройках Django под названием `REST_FRAMEWORK`.

For example your project's `settings.py` file might include something like this:

Например, файл `settings.py` вашего проекта может содержать что-то вроде этого:

```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

## Accessing settings

## Доступ к настройкам

If you need to access the values of REST framework's API settings in your project, you should use the `api_settings` object. For example.

Если вам необходимо получить доступ к значениям настроек API фреймворка REST в вашем проекте, вам следует использовать объект `api_settings`. Например.

```
from rest_framework.settings import api_settings

print(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
```

The `api_settings` object will check for any user-defined settings, and otherwise fall back to the default values. Any setting that uses string import paths to refer to a class will automatically import and return the referenced class, instead of the string literal.

Объект `api_settings` будет проверять наличие любых пользовательских настроек и в противном случае возвращаться к значениям по умолчанию. Любая настройка, использующая строковые пути импорта для ссылки на класс, будет автоматически импортировать и возвращать класс, на который ссылается, вместо строкового литерала.

---

# API Reference

# API Reference

## API policy settings

## Настройки политики API

*The following settings control the basic API policies, and are applied to every `APIView` class-based view, or `@api_view` function based view.*

*Следующие настройки управляют основными политиками API и применяются к каждому представлению `APIView` на основе класса или `@api_view` на основе функции.*

#### DEFAULT_RENDERER_CLASSES

#### DEFAULT_RENDERER_CLASSES

A list or tuple of renderer classes, that determines the default set of renderers that may be used when returning a `Response` object.

Список или кортеж классов рендереров, определяющий набор рендереров по умолчанию, которые могут быть использованы при возврате объекта `Response`.

Default:

По умолчанию:

```
[
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]
```

#### DEFAULT_PARSER_CLASSES

#### DEFAULT_PARSER_CLASSES

A list or tuple of parser classes, that determines the default set of parsers used when accessing the `request.data` property.

Список или кортеж классов парсеров, определяющий набор парсеров по умолчанию, используемых при обращении к свойству `request.data`.

Default:

По умолчанию:

```
[
    'rest_framework.parsers.JSONParser',
    'rest_framework.parsers.FormParser',
    'rest_framework.parsers.MultiPartParser'
]
```

#### DEFAULT_AUTHENTICATION_CLASSES

#### DEFAULT_AUTHENTICATION_CLASSES

A list or tuple of authentication classes, that determines the default set of authenticators used when accessing the `request.user` or `request.auth` properties.

Список или кортеж классов аутентификации, определяющий набор аутентификаторов по умолчанию, используемых при обращении к свойствам `request.user` или `request.auth`.

Default:

По умолчанию:

```
[
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication'
]
```

#### DEFAULT_PERMISSION_CLASSES

#### DEFAULT_PERMISSION_CLASSES

A list or tuple of permission classes, that determines the default set of permissions checked at the start of a view. Permission must be granted by every class in the list.

Список или кортеж классов разрешений, который определяет набор разрешений по умолчанию, проверяемых при запуске представления. Разрешение должно быть предоставлено каждым классом в списке.

Default:

По умолчанию:

```
[
    'rest_framework.permissions.AllowAny',
]
```

#### DEFAULT_THROTTLE_CLASSES

#### DEFAULT_THROTTLE_CLASSES

A list or tuple of throttle classes, that determines the default set of throttles checked at the start of a view.

Список или кортеж классов дросселей, который определяет набор дросселей по умолчанию, проверяемых при запуске представления.

Default: `[]`

По умолчанию: `[]`.

#### DEFAULT_CONTENT_NEGOTIATION_CLASS

#### DEFAULT_CONTENT_NEGOTIATION_CLASS

A content negotiation class, that determines how a renderer is selected for the response, given an incoming request.

Класс согласования содержимого, который определяет, как выбирается рендерер для ответа, учитывая входящий запрос.

Default: `'rest_framework.negotiation.DefaultContentNegotiation'`

По умолчанию: `'rest_framework.negotiation.DefaultContentNegotiation'`.

#### DEFAULT_SCHEMA_CLASS

#### DEFAULT_SCHEMA_CLASS

A view inspector class that will be used for schema generation.

Класс инспектора представлений, который будет использоваться для генерации схемы.

Default: `'rest_framework.schemas.openapi.AutoSchema'`

По умолчанию: `'rest_framework.schemas.openapi.AutoSchema'`.

---

## Generic view settings

## Общие настройки представления

*The following settings control the behavior of the generic class-based views.*

* Следующие настройки управляют поведением общих представлений на основе классов.

#### DEFAULT_FILTER_BACKENDS

#### DEFAULT_FILTER_BACKENDS

A list of filter backend classes that should be used for generic filtering. If set to `None` then generic filtering is disabled.

Список классов бэкенда фильтра, которые должны использоваться для общей фильтрации. Если установлено значение `None`, то общая фильтрация отключена.

#### DEFAULT_PAGINATION_CLASS

#### DEFAULT_PAGINATION_CLASS

The default class to use for queryset pagination. If set to `None`, pagination is disabled by default. See the pagination documentation for further guidance on [setting](pagination.md#setting-the-pagination-style) and [modifying](pagination.md#modifying-the-pagination-style) the pagination style.

Класс по умолчанию, используемый для пагинации наборов запросов. Если установлено значение `None`, пагинация по умолчанию отключена. Дополнительное руководство по [установке](pagination.md#setting-the-pagination-style) и [изменению](pagination.md#modifying-the-pagination-style) стиля пагинации см. в документации по пагинации.

Default: `None`

По умолчанию: `Нет`

#### PAGE_SIZE

#### PAGE_SIZE

The default page size to use for pagination. If set to `None`, pagination is disabled by default.

Размер страницы по умолчанию, используемый для пагинации. Если установлено значение `None`, то по умолчанию пагинация отключена.

Default: `None`

По умолчанию: `Нет`

### SEARCH_PARAM

### SEARCH_PARAM

The name of a query parameter, which can be used to specify the search term used by `SearchFilter`.

Имя параметра запроса, который может быть использован для указания поискового термина, используемого `SearchFilter`.

Default: `search`

По умолчанию: `search`.

#### ORDERING_PARAM

#### ORDERING_PARAM

The name of a query parameter, which can be used to specify the ordering of results returned by `OrderingFilter`.

Имя параметра запроса, который может быть использован для указания упорядочения результатов, возвращаемых `OrderingFilter`.

Default: `ordering`

По умолчанию: `заказ`.

---

## Versioning settings

## Настройки версий

#### DEFAULT_VERSION

#### DEFAULT_VERSION

The value that should be used for `request.version` when no versioning information is present.

Значение, которое должно использоваться для `request.version`, когда информация о версиях отсутствует.

Default: `None`

По умолчанию: `Нет`

#### ALLOWED_VERSIONS

#### ALLOWED_VERSIONS

If set, this value will restrict the set of versions that may be returned by the versioning scheme, and will raise an error if the provided version if not in this set.

Если задано, это значение ограничивает набор версий, которые могут быть возвращены схемой версий, и вызывает ошибку, если предоставленная версия не входит в этот набор.

Default: `None`

По умолчанию: `Нет`

#### VERSION_PARAM

#### VERSION_PARAM

The string that should used for any versioning parameters, such as in the media type or URL query parameters.

Строка, которая должна использоваться для любых параметров версионирования, например, в типе медиа или параметрах запроса URL.

Default: `'version'`

По умолчанию: ``версия``.

---

## Authentication settings

## Настройки аутентификации

*The following settings control the behavior of unauthenticated requests.*

* Следующие настройки управляют поведением неаутентифицированных запросов.*

#### UNAUTHENTICATED_USER

#### UNAUTHENTICATED_USER

The class that should be used to initialize `request.user` for unauthenticated requests. (If removing authentication entirely, e.g. by removing `django.contrib.auth` from `INSTALLED_APPS`, set `UNAUTHENTICATED_USER` to `None`.)

Класс, который должен использоваться для инициализации `request.user` для неаутентифицированных запросов. (Если аутентификация полностью удалена, например, путем удаления `django.contrib.auth` из `INSTALLED_APPS`, установите `UNAUTHENTICATED_USER` в `None`).

Default: `django.contrib.auth.models.AnonymousUser`

По умолчанию: `django.contrib.auth.models.AnonymousUser`.

#### UNAUTHENTICATED_TOKEN

#### UNAUTHENTICATED_TOKEN

The class that should be used to initialize `request.auth` for unauthenticated requests.

Класс, который должен использоваться для инициализации `request.auth` для неаутентифицированных запросов.

Default: `None`

По умолчанию: `Нет`

---

## Test settings

## Настройки теста

*The following settings control the behavior of APIRequestFactory and APIClient*

* Следующие настройки управляют поведением APIRequestFactory и APIClient*.

#### TEST_REQUEST_DEFAULT_FORMAT

#### TEST_REQUEST_DEFAULT_FORMAT

The default format that should be used when making test requests.

Формат по умолчанию, который следует использовать при составлении тестовых запросов.

This should match up with the format of one of the renderer classes in the `TEST_REQUEST_RENDERER_CLASSES` setting.

Он должен совпадать с форматом одного из классов рендереров в настройке `TEST_REQUEST_RENDERER_CLASSES`.

Default: `'multipart'`

По умолчанию: `'multipart'`.

#### TEST_REQUEST_RENDERER_CLASSES

#### TEST_REQUEST_RENDERER_CLASSES

The renderer classes that are supported when building test requests.

Классы рендереров, которые поддерживаются при построении тестовых запросов.

The format of any of these renderer classes may be used when constructing a test request, for example: `client.post('/users', {'username': 'jamie'}, format='json')`

Формат любого из этих классов рендереров может быть использован при построении тестового запроса, например: `client.post('/users', {'username': 'jamie'}, format='json')`.

Default:

По умолчанию:

```
[
    'rest_framework.renderers.MultiPartRenderer',
    'rest_framework.renderers.JSONRenderer'
]
```

---

## Schema generation controls

## Элементы управления генерацией схемы

#### SCHEMA_COERCE_PATH_PK

#### SCHEMA_COERCE_PATH_PK

If set, this maps the `'pk'` identifier in the URL conf onto the actual field name when generating a schema path parameter. Typically this will be `'id'`. This gives a more suitable representation as "primary key" is an implementation detail, whereas "identifier" is a more general concept.

Если задано, то при генерации параметра пути к схеме идентификатор `'pk'` в URL conf сопоставляется с реальным именем поля. Обычно это `'id'`. Это дает более подходящее представление, поскольку "первичный ключ" - это деталь реализации, тогда как "идентификатор" - более общая концепция.

Default: `True`

По умолчанию: `True`

#### SCHEMA_COERCE_METHOD_NAMES

#### SCHEMA_COERCE_METHOD_NAMES

If set, this is used to map internal viewset method names onto external action names used in the schema generation. This allows us to generate names that are more suitable for an external representation than those that are used internally in the codebase.

Если установлено, это используется для сопоставления внутренних имен методов набора представлений с именами внешних действий, используемых при генерации схемы. Это позволяет нам генерировать имена, более подходящие для внешнего представления, чем те, которые используются внутри кодовой базы.

Default: `{'retrieve': 'read', 'destroy': 'delete'}`

По умолчанию: `{'retrieve': 'read', 'destroy': 'delete'}`

---

## Content type controls

## Контроль типа содержимого

#### URL_FORMAT_OVERRIDE

#### URL_FORMAT_OVERRIDE

The name of a URL parameter that may be used to override the default content negotiation `Accept` header behavior, by using a `format=…` query parameter in the request URL.

Имя параметра URL, который можно использовать для переопределения стандартного поведения заголовка согласования содержимого `Accept`, используя параметр запроса `format=...` в URL запроса.

For example: `http://example.com/organizations/?format=csv`

Например: `http://example.com/organizations/?format=csv`

If the value of this setting is `None` then URL format overrides will be disabled.

Если значение этого параметра равно `None`, то переопределение формата URL будет отключено.

Default: `'format'`

По умолчанию: ``формат``.

#### FORMAT_SUFFIX_KWARG

#### FORMAT_SUFFIX_KWARG

The name of a parameter in the URL conf that may be used to provide a format suffix. This setting is applied when using `format_suffix_patterns` to include suffixed URL patterns.

Имя параметра в URL conf, который может быть использован для обеспечения суффикса формата. Этот параметр применяется при использовании `format_suffix_patterns` для включения суффиксных шаблонов URL.

For example: `http://example.com/organizations.csv/`

Например: `http://example.com/organizations.csv/`

Default: `'format'`

По умолчанию: ``формат``.

---

## Date and time formatting

## Форматирование даты и времени

*The following settings are used to control how date and time representations may be parsed and rendered.*

* Следующие параметры используются для управления тем, как представления даты и времени могут быть разобраны и отображены.*

#### DATETIME_FORMAT

#### DATETIME_FORMAT

A format string that should be used by default for rendering the output of `DateTimeField` serializer fields. If `None`, then `DateTimeField` serializer fields will return Python `datetime` objects, and the datetime encoding will be determined by the renderer.

Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора `DateTimeField`. Если `None`, то поля сериализатора `DateTimeField` будут возвращать объекты Python `datetime`, а кодировка времени будет определяться рендерером.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любым из `None`, `'iso-8601'` или строкой Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `'iso-8601'`

По умолчанию: `'iso-8601'`.

#### DATETIME_INPUT_FORMATS

#### DATETIME_INPUT_FORMATS

A list of format strings that should be used by default for parsing inputs to `DateTimeField` serializer fields.

Список форматных строк, которые должны использоваться по умолчанию при разборе входных данных для полей сериализатора `DateTimeField`.

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть списком, включающим строку `'iso-8601'` или строки Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`.

#### DATE_FORMAT

#### DATE_FORMAT

A format string that should be used by default for rendering the output of `DateField` serializer fields. If `None`, then `DateField` serializer fields will return Python `date` objects, and the date encoding will be determined by the renderer.

Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора `DateField`. Если `None`, то поля сериализатора `DateField` будут возвращать объекты Python `date`, а кодировка даты будет определяться рендерером.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любым из `None`, `'iso-8601'` или строкой Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `'iso-8601'`

По умолчанию: `'iso-8601'`.

#### DATE_INPUT_FORMATS

#### DATE_INPUT_FORMATS

A list of format strings that should be used by default for parsing inputs to `DateField` serializer fields.

Список форматных строк, которые должны использоваться по умолчанию при разборе входных данных для полей сериализатора `DateField`.

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть списком, включающим строку `'iso-8601'` или строки Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`.

#### TIME_FORMAT

#### TIME_FORMAT

A format string that should be used by default for rendering the output of `TimeField` serializer fields. If `None`, then `TimeField` serializer fields will return Python `time` objects, and the time encoding will be determined by the renderer.

Строка формата, которая должна использоваться по умолчанию для вывода полей сериализатора `TimeField`. Если `None`, то поля сериализатора `TimeField` будут возвращать объекты Python `time`, а кодировка времени будет определяться рендерером.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любым из `None`, `'iso-8601'` или строкой Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `'iso-8601'`

По умолчанию: `'iso-8601'`.

#### TIME_INPUT_FORMATS

#### TIME_INPUT_FORMATS

A list of format strings that should be used by default for parsing inputs to `TimeField` serializer fields.

Список форматных строк, которые должны использоваться по умолчанию при разборе входных данных для полей сериализатора `TimeField`.

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть списком, включающим строку `'iso-8601'` или строки Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime).

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`.

---

## Encodings

## Кодировки

#### UNICODE_JSON

#### UNICODE_JSON

When set to `True`, JSON responses will allow unicode characters in responses. For example:

Если установлено значение `True`, ответы JSON будут разрешать использование символов юникода в ответах. Например:

```
{"unicode black star":"★"}
```

When set to `False`, JSON responses will escape non-ascii characters, like so:

Если установлено значение `False`, в ответах JSON будут экранироваться неасксиальные символы, как показано ниже:

```
{"unicode black star":"\u2605"}
```

Both styles conform to [RFC 4627](https://www.ietf.org/rfc/rfc4627.txt), and are syntactically valid JSON. The unicode style is preferred as being more user-friendly when inspecting API responses.

Оба стиля соответствуют [RFC 4627] (https://www.ietf.org/rfc/rfc4627.txt) и являются синтаксически правильным JSON. Стиль unicode предпочтительнее, так как он более удобен при проверке ответов API.

Default: `True`

По умолчанию: `True`

#### COMPACT_JSON

#### COMPACT_JSON

When set to `True`, JSON responses will return compact representations, with no spacing after `':'` and `','` characters. For example:

Если установлено значение `True`, ответы JSON будут возвращать компактные представления, без пробелов после символов `':'` и `','`. Например:

```
{"is_admin":false,"email":"jane@example"}
```

When set to `False`, JSON responses will return slightly more verbose representations, like so:

Если установлено значение `False`, ответы JSON будут возвращать более подробное представление, как показано ниже:

```
{"is_admin": false, "email": "jane@example"}
```

The default style is to return minified responses, in line with [Heroku's API design guidelines](https://github.com/interagent/http-api-design#keep-json-minified-in-all-responses).

По умолчанию возвращаются минифицированные ответы, в соответствии с [Heroku's API design guidelines](https://github.com/interagent/http-api-design#keep-json-minified-in-all-responses).

Default: `True`

По умолчанию: `True`

#### STRICT_JSON

#### STRICT_JSON

When set to `True`, JSON rendering and parsing will only observe syntactically valid JSON, raising an exception for the extended float values (`nan`, `inf`, `-inf`) accepted by Python's `json` module. This is the recommended setting, as these values are not generally supported. e.g., neither Javascript's `JSON.Parse` nor PostgreSQL's JSON data type accept these values.

Если установлено значение `True`, при рендеринге и разборе JSON будет использоваться только синтаксически правильный JSON, создавая исключение для расширенных значений float (`nan`, `inf`, `inf`), принимаемых модулем Python `json`. Это рекомендуемая настройка, так как эти значения обычно не поддерживаются. Например, ни Javascript `JSON.Parse`, ни PostgreSQL тип данных JSON не принимают эти значения.

When set to `False`, JSON rendering and parsing will be permissive. However, these values are still invalid and will need to be specially handled in your code.

Если установлено значение `False`, рендеринг и парсинг JSON будут разрешительными. Однако эти значения все еще недействительны и должны быть специально обработаны в вашем коде.

Default: `True`

По умолчанию: `True`

#### COERCE_DECIMAL_TO_STRING

#### COERCE_DECIMAL_TO_STRING

When returning decimal objects in API representations that do not support a native decimal type, it is normally best to return the value as a string. This avoids the loss of precision that occurs with binary floating point implementations.

При возврате десятичных объектов в представлениях API, которые не поддерживают собственный десятичный тип, обычно лучше всего возвращать значение в виде строки. Это позволяет избежать потери точности, которая происходит при двоичной реализации с плавающей запятой.

When set to `True`, the serializer `DecimalField` class will return strings instead of `Decimal` objects. When set to `False`, serializers will return `Decimal` objects, which the default JSON encoder will return as floats.

Если установлено значение `True`, сериализатор класса `DecimalField` будет возвращать строки вместо объектов `Decimal`. Если установлено значение `False`, сериализаторы будут возвращать объекты `Decimal`, которые кодировщик JSON по умолчанию будет возвращать как float.

Default: `True`

По умолчанию: `True`

---

## View names and descriptions

## Названия и описания видов

**The following settings are used to generate the view names and descriptions, as used in responses to `OPTIONS` requests, and as used in the browsable API.**

**Следующие настройки используются для создания названий и описаний представлений, которые используются в ответах на запросы `OPTIONS` и в API для просмотра.**.

#### VIEW_NAME_FUNCTION

#### VIEW_NAME_FUNCTION

A string representing the function that should be used when generating view names.

Строка, представляющая функцию, которая должна использоваться при генерации имен представлений.

This should be a function with the following signature:

Это должна быть функция со следующей сигнатурой:

```
view_name(self)
```

* `self`: The view instance. Typically the name function would inspect the name of the class when generating a descriptive name, by accessing `self.__class__.__name__`.

* `self`: Экземпляр представления. Обычно функция name проверяет имя класса при генерации описательного имени, обращаясь к `self.__class__.__name__`.

If the view instance inherits `ViewSet`, it may have been initialized with several optional arguments:

Если экземпляр представления наследует `ViewSet`, он может быть инициализирован с несколькими необязательными аргументами:

* `name`: A name explicitly provided to a view in the viewset. Typically, this value should be used as-is when provided.
* `suffix`: Text used when differentiating individual views in a viewset. This argument is mutually exclusive to `name`.
* `detail`: Boolean that differentiates an individual view in a viewset as either being a 'list' or 'detail' view.

* `name`: Имя, явно предоставленное представлению в наборе представлений. Обычно это значение должно использоваться как есть, если оно предоставлено.
* ``суффикс``: Текст, используемый для различения отдельных представлений в наборе представлений. Этот аргумент является взаимоисключающим с `name`.
* `detail`: Булево значение, отличающее индивидуальное представление в наборе представлений как "список" или "подробное представление".

Default: `'rest_framework.views.get_view_name'`

По умолчанию: `'rest_framework.views.get_view_name'`.

#### VIEW_DESCRIPTION_FUNCTION

#### VIEW_DESCRIPTION_FUNCTION

A string representing the function that should be used when generating view descriptions.

Строка, представляющая функцию, которая должна использоваться при генерации описаний представлений.

This setting can be changed to support markup styles other than the default markdown. For example, you can use it to support `rst` markup in your view docstrings being output in the browsable API.

Этот параметр может быть изменен для поддержки стилей разметки, отличных от стандартного markdown. Например, вы можете использовать его для поддержки разметки `rst` в ваших документах представления, выводимых в просматриваемом API.

This should be a function with the following signature:

Это должна быть функция со следующей сигнатурой:

```
view_description(self, html=False)
```

* `self`: The view instance. Typically the description function would inspect the docstring of the class when generating a description, by accessing `self.__class__.__doc__`
* `html`: A boolean indicating if HTML output is required. `True` when used in the browsable API, and `False` when used in generating `OPTIONS` responses.

* `self`: Экземпляр представления. Обычно функция описания проверяет строку документа класса при генерации описания, обращаясь к `self.__class__.__doc__`.
* `html`: Булево значение, указывающее, требуется ли вывод HTML. `True` используется в API для просмотра, а `False` - при генерации ответов `OPTIONS`.

If the view instance inherits `ViewSet`, it may have been initialized with several optional arguments:

Если экземпляр представления наследует `ViewSet`, он может быть инициализирован с несколькими необязательными аргументами:

* `description`: A description explicitly provided to the view in the viewset. Typically, this is set by extra viewset `action`s, and should be used as-is.

* `description`: Описание, явно предоставленное представлению в наборе представлений. Обычно оно устанавливается дополнительными ``действиями`` набора представлений и должно использоваться как есть.

Default: `'rest_framework.views.get_view_description'`

По умолчанию: `'rest_framework.views.get_view_description'`.

## HTML Select Field cutoffs

## HTML Select Field cutoffs

Global settings for [select field cutoffs for rendering relational fields](relations.md#select-field-cutoffs) in the browsable API.

Глобальные настройки для [select field cutoffs for rendering relational fields](relations.md#select-field-cutoffs) в browsable API.

#### HTML_SELECT_CUTOFF

#### HTML_SELECT_CUTOFF

Global setting for the `html_cutoff` value. Must be an integer.

Глобальная настройка для значения `html_cutoff`. Должно быть целое число.

Default: 1000

По умолчанию: 1000

#### HTML_SELECT_CUTOFF_TEXT

#### HTML_SELECT_CUTOFF_TEXT

A string representing a global setting for `html_cutoff_text`.

Строка, представляющая глобальную настройку для `html_cutoff_text`.

Default: `"More than {count} items..."`

По умолчанию: `"Более {count} элементов..."`.

---

## Miscellaneous settings

## Разные настройки

#### EXCEPTION_HANDLER

#### EXCEPTION_HANDLER

A string representing the function that should be used when returning a response for any given exception. If the function returns `None`, a 500 error will be raised.

Строка, представляющая функцию, которая должна быть использована при возврате ответа для любого данного исключения. Если функция возвращает `None`, будет выдана ошибка 500.

This setting can be changed to support error responses other than the default `{"detail": "Failure..."}` responses. For example, you can use it to provide API responses like `{"errors": [{"message": "Failure...", "code": ""} ...]}`.

Этот параметр может быть изменен для поддержки ответов на ошибки, отличных от ответов по умолчанию `{"detail": "Сбой..."}} ответов. Например, вы можете использовать его для предоставления ответов API типа `{"errors": [{"message": "Failure...", "code": ""} ...]}``.

This should be a function with the following signature:

Это должна быть функция со следующей сигнатурой:

```
exception_handler(exc, context)
```

* `exc`: The exception.

* ``exc``: Исключение.

Default: `'rest_framework.views.exception_handler'`

По умолчанию: `'rest_framework.views.exception_handler'`.

#### NON_FIELD_ERRORS_KEY

#### NON_FIELD_ERRORS_KEY

A string representing the key that should be used for serializer errors that do not refer to a specific field, but are instead general errors.

Строка, представляющая ключ, который следует использовать для ошибок сериализатора, которые не относятся к конкретному полю, а являются общими ошибками.

Default: `'non_field_errors'`

По умолчанию: `'non_field_errors'`.

#### URL_FIELD_NAME

#### URL_FIELD_NAME

A string representing the key that should be used for the URL fields generated by `HyperlinkedModelSerializer`.

Строка, представляющая ключ, который должен использоваться для полей URL, генерируемых `HyperlinkedModelSerializer`.

Default: `'url'`

По умолчанию: `'url'`

#### NUM_PROXIES

#### NUM_PROXIES

An integer of 0 or more, that may be used to specify the number of application proxies that the API runs behind. This allows throttling to more accurately identify client IP addresses. If set to `None` then less strict IP matching will be used by the throttle classes.

Целое число, равное 0 или более, которое может использоваться для указания количества прокси-серверов приложений, за которыми работает API. Это позволяет дросселированию более точно определять IP-адреса клиентов. Если установлено значение `None`, то классы дросселирования будут использовать менее строгое сопоставление IP-адресов.

Default: `None`

По умолчанию: `Нет`