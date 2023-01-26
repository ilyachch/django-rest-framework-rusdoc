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

> Пространства имен - это одна отличная идея - давайте сделаем больше из них!
>
> - [дзен питона] [цитирует]

Configuration for REST framework is all namespaced inside a single Django setting, named `REST_FRAMEWORK`.

Конфигурация для Framework REST имеет все имена в одной настройке Django, именем `rest_framework`.

For example your project's `settings.py` file might include something like this:

Например, файл вашего проекта `settings.py` может включать что -то вроде этого:

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

Если вам нужно получить доступ к значениям настройки API Framework REST в вашем проекте, вам следует использовать объект `api_settings`.
Например.

```
from rest_framework.settings import api_settings

print(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
```

The `api_settings` object will check for any user-defined settings, and otherwise fall back to the default values. Any setting that uses string import paths to refer to a class will automatically import and return the referenced class, instead of the string literal.

Объект `api_settings` будет проверять любые пользовательские настройки и в противном случае вернется к значениям по умолчанию.
Любая настройка, которая использует пути импорта строки для обозначения класса, автоматически импортирует и возвращает ссылочный класс вместо буквального буква.

---

# API Reference

# Ссылка на API

## API policy settings

## Настройки политики API

*The following settings control the basic API policies, and are applied to every `APIView` class-based view, or `@api_view` function based view.*

*Следующие параметры управляют основными политиками API и применяются к каждому представлению на основе класса Apiview

#### DEFAULT_RENDERER_CLASSES

#### default_renderer_classes

A list or tuple of renderer classes, that determines the default set of renderers that may be used when returning a `Response` object.

Список или кортеж классов рендеринга, который определяет набор визуализаторов по умолчанию, который может использоваться при возвращении объекта `recsess '.

Default:

По умолчанию:

```
[
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]
```

#### DEFAULT_PARSER_CLASSES

#### default_parser_classes

A list or tuple of parser classes, that determines the default set of parsers used when accessing the `request.data` property.

Список или кортеж классов анализаторов, который определяет набор анализаторов по умолчанию, используемые при доступе к свойству equest.data`.

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

#### default_authentication_classes

A list or tuple of authentication classes, that determines the default set of authenticators used when accessing the `request.user` or `request.auth` properties.

Список или кортеж классов аутентификации, который определяет набор по умолчанию аутентикаторов, используемых при доступе к свойствам `request.user` или` request.auth`.

Default:

По умолчанию:

```
[
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication'
]
```

#### DEFAULT_PERMISSION_CLASSES

#### default_permission_classes

A list or tuple of permission classes, that determines the default set of permissions checked at the start of a view. Permission must be granted by every class in the list.

Список или кортеж классов разрешений, который определяет набор разрешений по умолчанию, проверяемых в начале представления.
Разрешение должно быть предоставлено каждому классу в списке.

Default:

По умолчанию:

```
[
    'rest_framework.permissions.AllowAny',
]
```

#### DEFAULT_THROTTLE_CLASSES

#### default_throttle_classes

A list or tuple of throttle classes, that determines the default set of throttles checked at the start of a view.

Список или кортеж классов дроссельной заслонки, который определяет набор дросселей по умолчанию, проверяемый в начале представления.

Default: `[]`

По умолчанию: `[]`

#### DEFAULT_CONTENT_NEGOTIATION_CLASS

#### default_content_negotiation_class

A content negotiation class, that determines how a renderer is selected for the response, given an incoming request.

Класс переговоров о контенте, который определяет, как отображается рендерера, учитывая входящий запрос.

Default: `'rest_framework.negotiation.DefaultContentNegotiation'`

По умолчанию: `'REST Framework.negotiation.defaultContent Переговоры»

#### DEFAULT_SCHEMA_CLASS

#### default_schema_class

A view inspector class that will be used for schema generation.

Класс инспекторов представления, который будет использоваться для генерации схемы.

Default: `'rest_framework.schemas.openapi.AutoSchema'`

По умолчанию: `rest_framework.schemas.openapi.autoschema '

---

## Generic view settings

## общие настройки просмотра

*The following settings control the behavior of the generic class-based views.*

*Следующие настройки управляют поведением общих представлений на основе классов.*

#### DEFAULT_FILTER_BACKENDS

#### default_filter_backends

A list of filter backend classes that should be used for generic filtering. If set to `None` then generic filtering is disabled.

Список классов бэкэнд фильтров, которые следует использовать для общей фильтрации.
Если установить на `none`, то общая фильтрация отключена.

#### DEFAULT_PAGINATION_CLASS

#### default_pagination_class

The default class to use for queryset pagination. If set to `None`, pagination is disabled by default. See the pagination documentation for further guidance on [setting](pagination.md#setting-the-pagination-style) and [modifying](pagination.md#modifying-the-pagination-style) the pagination style.

Класс по умолчанию для использования для страниц Queryset.
Если установить на `none`, страдания отключена по умолчанию.
См. Документацию на странице для дальнейшего руководства по [настройке] (Pagination.md#в стиле настройки) и [модификация] (Pagination.md#модификация стиля плавания) в стиле страниц.

Default: `None`

По умолчанию: `none

#### PAGE_SIZE

#### РАЗМЕР СТРАНИЦЫ

The default page size to use for pagination. If set to `None`, pagination is disabled by default.

Размер страницы по умолчанию для использования для страницы.
Если установить на `none`, страдания отключена по умолчанию.

Default: `None`

По умолчанию: `none

### SEARCH_PARAM

### search_param

The name of a query parameter, which can be used to specify the search term used by `SearchFilter`.

Имя параметра запроса, который можно использовать для указания термина поиска, используемого `searchfilter`.

Default: `search`

По умолчанию: `search`

#### ORDERING_PARAM

#### ordering_param

The name of a query parameter, which can be used to specify the ordering of results returned by `OrderingFilter`.

Название параметра запроса, который можно использовать для указания упорядочения результатов, возвращаемых `orderingfilter '.

Default: `ordering`

По умолчанию: `Заказать

---

## Versioning settings

## Настройки управления версиями

#### DEFAULT_VERSION

#### default_version

The value that should be used for `request.version` when no versioning information is present.

Значение, которое следует использовать для `request.version`, когда информация об управлении версией не присутствует.

Default: `None`

По умолчанию: `none

#### ALLOWED_VERSIONS

#### Alling_versions

If set, this value will restrict the set of versions that may be returned by the versioning scheme, and will raise an error if the provided version if not in this set.

Если установлено, это значение ограничит набор версий, которые могут быть возвращены схемой версии, и вынесет ошибку, если предоставленная версия, если не в этом наборе.

Default: `None`

По умолчанию: `none

#### VERSION_PARAM

#### version_param

The string that should used for any versioning parameters, such as in the media type or URL query parameters.

Строка, которая должна использовать для любых параметров управления версией, например, в параметрах типа среды или параметров запроса URL.

Default: `'version'`

По умолчанию: `'версия' '

---

## Authentication settings

## Настройки аутентификации

*The following settings control the behavior of unauthenticated requests.*

*Следующие настройки контролируют поведение несаутонированных запросов.*

#### UNAUTHENTICATED_USER

#### unauthenticated_user

The class that should be used to initialize `request.user` for unauthenticated requests. (If removing authentication entirely, e.g. by removing `django.contrib.auth` from `INSTALLED_APPS`, set `UNAUTHENTICATED_USER` to `None`.)

Класс, который должен использоваться для инициализации `request.user` для несаутентированных запросов.
(Если полностью удалить аутентификацию, например, удалив `django.contrib.auth` из` stanted_apps`, установите `unauthenticated_user` none`.)

Default: `django.contrib.auth.models.AnonymousUser`

По умолчанию: `django.contrib.auth.models.anonymoususer`

#### UNAUTHENTICATED_TOKEN

#### unautenticated_token

The class that should be used to initialize `request.auth` for unauthenticated requests.

Класс, который должен использоваться для инициализации `request.auth` для несаутентированных запросов.

Default: `None`

По умолчанию: `none

---

## Test settings

## Настройки теста

*The following settings control the behavior of APIRequestFactory and APIClient*

*Следующие настройки контролируют поведение apirequestfactory и apiclient*

#### TEST_REQUEST_DEFAULT_FORMAT

#### test_request_default_format

The default format that should be used when making test requests.

Формат по умолчанию, который следует использовать при выполнении тестовых запросов.

This should match up with the format of one of the renderer classes in the `TEST_REQUEST_RENDERER_CLASSES` setting.

Это должно соответствовать формату одного из классов Renderer в настройке `test_request_renderer_classes`.

Default: `'multipart'`

По умолчанию: `'Multipart''

#### TEST_REQUEST_RENDERER_CLASSES

#### test_request_renderer_classes

The renderer classes that are supported when building test requests.

Классы рендерера, которые поддерживаются при строительстве запросов на тестирование.

The format of any of these renderer classes may be used when constructing a test request, for example: `client.post('/users', {'username': 'jamie'}, format='json')`

Формат любого из этих классов рендеринга может использоваться при построении запроса на тест, например: `client.post ('/users', {'username': 'Jamie'}, format = 'json')`

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

## управление генерацией схемы

#### SCHEMA_COERCE_PATH_PK

#### schema_coerce_path_pk

If set, this maps the `'pk'` identifier in the URL conf onto the actual field name when generating a schema path parameter. Typically this will be `'id'`. This gives a more suitable representation as "primary key" is an implementation detail, whereas "identifier" is a more general concept.

Если установлено, это отображает идентификатор «PK» в URL CONF на фактическое имя поля при создании параметра пути схемы.
Как правило, это будет «id».
Это дает более подходящее представление, поскольку «первичный ключ» является детализацией реализации, тогда как «идентификатор» является более общей концепцией.

Default: `True`

По умолчанию: `true

#### SCHEMA_COERCE_METHOD_NAMES

#### schema_coerce_method_names

If set, this is used to map internal viewset method names onto external action names used in the schema generation. This allows us to generate names that are more suitable for an external representation than those that are used internally in the codebase.

Если установлено, это используется для картирования имен методов внутренних видов на имена внешних действий, используемые в генерации схемы.
Это позволяет нам генерировать имена, которые более подходящие для внешнего представления, чем те, которые используются внутренне в кодовой базе.

Default: `{'retrieve': 'read', 'destroy': 'delete'}`

По умолчанию: `{'retive': 'reade', 'destroy': 'delete'}`

---

## Content type controls

## элементы управления типом контента

#### URL_FORMAT_OVERRIDE

#### url_format_override

The name of a URL parameter that may be used to override the default content negotiation `Accept` header behavior, by using a `format=…` query parameter in the request URL.

Имя параметра URL, который может использоваться для переопределения согласования контента по умолчанию `принять` поведение заголовка, с помощью `format =…` параметр запроса в URL -адресе запроса.

For example: `http://example.com/organizations/?format=csv`

Например: `http: //example.com/organizations/? Format = csv`

If the value of this setting is `None` then URL format overrides will be disabled.

Если значение этого настройки равна `none`, то переопределение формата URL -формата будет отключено.

Default: `'format'`

По умолчанию: `'format'

#### FORMAT_SUFFIX_KWARG

#### format_suffix_kwarg

The name of a parameter in the URL conf that may be used to provide a format suffix. This setting is applied when using `format_suffix_patterns` to include suffixed URL patterns.

Название параметра в конфузе URL, которое может использоваться для обеспечения суффикса формата.
Эта настройка применяется при использовании `format_suffix_patterns` для включения суффиксативных шаблонов URL -адресов.

For example: `http://example.com/organizations.csv/`

Например: `http: // Пример.com/Organizations.csv/`

Default: `'format'`

По умолчанию: `'format'

---

## Date and time formatting

## форматирование даты и времени

*The following settings are used to control how date and time representations may be parsed and rendered.*

*Следующие настройки используются для контроля того, как могут быть проанализированы и отображены представления даты и времени.*

#### DATETIME_FORMAT

#### datetime_format

A format string that should be used by default for rendering the output of `DateTimeField` serializer fields. If `None`, then `DateTimeField` serializer fields will return Python `datetime` objects, and the datetime encoding will be determined by the renderer.

Строка формата, которую следует использовать по умолчанию для визуализации вывода полей сериализатора DateTimefield`.
Если `none`, то поля сериализатора` dateTimefield` возвращают объекты Python `dateTime`, а кодирование DateTime будет определено рендерера.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любой из `none`,` 'iso-8601'' или python [strftime format] (https://docs.python.org/3/library/time.html#time.trftime) String.

Default: `'iso-8601'`

По умолчанию: `iso-8601' '

#### DATETIME_INPUT_FORMATS

#### datetime_input_formats

A list of format strings that should be used by default for parsing inputs to `DateTimeField` serializer fields.

Список строк формата, которые следует использовать по умолчанию для анализа входов в поля сериализатора DateTimefield`.

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть список, включая строку `'iso-8601'` или python [strftime format] (https://docs.python.org/3/library/time.html#time.strftime) строки.

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`

#### DATE_FORMAT

#### ФОРМАТ ДАТЫ

A format string that should be used by default for rendering the output of `DateField` serializer fields. If `None`, then `DateField` serializer fields will return Python `date` objects, and the date encoding will be determined by the renderer.

Строка формата, которую следует использовать по умолчанию для отображения вывода полей сериализатора `datefield.
Если `none`, то поля сериализатора` datefield 'вернет объекты Python `date', а кодирование даты будет определено рендерера.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любой из `none`,` 'iso-8601'' или python [strftime format] (https://docs.python.org/3/library/time.html#time.trftime) String.

Default: `'iso-8601'`

По умолчанию: `iso-8601' '

#### DATE_INPUT_FORMATS

#### date_input_formats

A list of format strings that should be used by default for parsing inputs to `DateField` serializer fields.

Список строк формата, которые следует использовать по умолчанию для анализа входов в поля сериализатора `datefield`.

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть список, включая строку `'iso-8601'` или python [strftime format] (https://docs.python.org/3/library/time.html#time.strftime) строки.

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`

#### TIME_FORMAT

#### time_format

A format string that should be used by default for rendering the output of `TimeField` serializer fields. If `None`, then `TimeField` serializer fields will return Python `time` objects, and the time encoding will be determined by the renderer.

Строка формата, которую следует использовать по умолчанию для отображения вывода полей сериализатора Timefield.
Если `none`, то поля сериализатора` timefield 'вернет объекты Python `time', а кодирование времени будет определено рендерера.

May be any of `None`, `'iso-8601'` or a Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) string.

Может быть любой из `none`,` 'iso-8601'' или python [strftime format] (https://docs.python.org/3/library/time.html#time.trftime) String.

Default: `'iso-8601'`

По умолчанию: `iso-8601' '

#### TIME_INPUT_FORMATS

#### time_input_formats

A list of format strings that should be used by default for parsing inputs to `TimeField` serializer fields.

Список строк формата, которые следует использовать по умолчанию для анализа входов в поля сериализатора «Timefield».

May be a list including the string `'iso-8601'` or Python [strftime format](https://docs.python.org/3/library/time.html#time.strftime) strings.

Может быть список, включая строку `'iso-8601'` или python [strftime format] (https://docs.python.org/3/library/time.html#time.strftime) строки.

Default: `['iso-8601']`

По умолчанию: `['iso-8601']`

---

## Encodings

## Кодирования

#### UNICODE_JSON

#### unicode_json

When set to `True`, JSON responses will allow unicode characters in responses. For example:

При установке на `true 'ответы JSON позволят символам Unicode в ответах.
Например:

```
{"unicode black star":"★"}
```

When set to `False`, JSON responses will escape non-ascii characters, like so:

При установке на `false 'ответы JSON избежат персонажей, не являющихся персонажами, например, так:

```
{"unicode black star":"\u2605"}
```

Both styles conform to [RFC 4627](https://www.ietf.org/rfc/rfc4627.txt), and are syntactically valid JSON. The unicode style is preferred as being more user-friendly when inspecting API responses.

Оба стиля соответствуют [RFC 4627] (https://www.ietf.org/rfc/rfc4627.txt) и являются синтаксически действительными JSON.
Стиль Unicode предпочтительнее как более удобный для пользователя при проверке ответов API.

Default: `True`

По умолчанию: `true

#### COMPACT_JSON

#### compact_json

When set to `True`, JSON responses will return compact representations, with no spacing after `':'` and `','` characters. For example:

При установке на `true 'ответы JSON будут возвращать компактные представления, без интернатов после`': '`и`', '`символов.
Например:

```
{"is_admin":false,"email":"jane@example"}
```

When set to `False`, JSON responses will return slightly more verbose representations, like so:

При установке на `false 'ответы JSON вернут немного более многословных представлений, например, так:

```
{"is_admin": false, "email": "jane@example"}
```

The default style is to return minified responses, in line with [Heroku's API design guidelines](https://github.com/interagent/http-api-design#keep-json-minified-in-all-responses).

Стиль по умолчанию заключается в том, чтобы вернуть минимизированные ответы, в соответствии с [Руководствами по проектированию API Heroku] (https://github.com/interagent/http-api-design#keep-json-minified-in-responses).

Default: `True`

По умолчанию: `true

#### STRICT_JSON

#### strict_json

When set to `True`, JSON rendering and parsing will only observe syntactically valid JSON, raising an exception for the extended float values (`nan`, `inf`, `-inf`) accepted by Python's `json` module. This is the recommended setting, as these values are not generally supported. e.g., neither Javascript's `JSON.Parse` nor PostgreSQL's JSON data type accept these values.

При установке на `true` рендеринг и анализ JSON будут соблюдать только синтаксически действительный JSON, поднимая исключение для расширенных значений поплавки (` nan`, `inf`,` -inf`), принятых модулем Python `json`.
Это рекомендуемый настройка, так как эти значения обычно не поддерживаются.
Например, ни `json.parse`, ни тип данных JSON's javaScript не принимают эти значения.

When set to `False`, JSON rendering and parsing will be permissive. However, these values are still invalid and will need to be specially handled in your code.

Когда установлено на `false`, рендеринг JSON и анализ будет разрешается.
Тем не менее, эти значения все еще являются недействительными и должны быть специально обработаны в вашем коде.

Default: `True`

По умолчанию: `true

#### COERCE_DECIMAL_TO_STRING

#### coerce_decimal_to_string

When returning decimal objects in API representations that do not support a native decimal type, it is normally best to return the value as a string. This avoids the loss of precision that occurs with binary floating point implementations.

При возврате десятичных объектов в представлениях API, которые не поддерживают нативного десятичного типа, обычно лучше всего вернуть значение как строку.
Это позволяет избежать потери точности, которая возникает с помощью бинарных реализаций с плавающей запятой.

When set to `True`, the serializer `DecimalField` class will return strings instead of `Decimal` objects. When set to `False`, serializers will return `Decimal` objects, which the default JSON encoder will return as floats.

При установке на `true` класс сериализатора` decimalfield` вернет строки вместо «десятичных» объектов.
Когда установлено в `false`, сериализаторы возвращают« десятичные »объекты, которые кодировщик JSON по умолчанию вернет как поплавок.

Default: `True`

По умолчанию: `true

---

## View names and descriptions

## Просмотреть имена и описания

**The following settings are used to generate the view names and descriptions, as used in responses to `OPTIONS` requests, and as used in the browsable API.**

** Следующие настройки используются для генерации имен и описаний представлений, как это используется в ответах на запросы `параметров ', и как используется в API -файле Brows. **

#### VIEW_NAME_FUNCTION

#### view_name_function

A string representing the function that should be used when generating view names.

Строка, представляющая функцию, которую следует использовать при генерации имен просмотра.

This should be a function with the following signature:

Это должно быть функцией со следующей подписью:

```
view_name(self)
```

* `self`: The view instance. Typically the name function would inspect the name of the class when generating a descriptive name, by accessing `self.__class__.__name__`.

* `self ': экземпляр просмотра.
Обычно функция имени проверяет имя класса при генерации описательного имени, доступа к `self .__ Class __.__ name__`.

If the view instance inherits `ViewSet`, it may have been initialized with several optional arguments:

Если экземпляр просмотра наследует `viewset`, он мог быть инициализирован несколькими дополнительными аргументами:

* `name`: A name explicitly provided to a view in the viewset. Typically, this value should be used as-is when provided.
* `suffix`: Text used when differentiating individual views in a viewset. This argument is mutually exclusive to `name`.
* `detail`: Boolean that differentiates an individual view in a viewset as either being a 'list' or 'detail' view.

* `name`: имя явно предоставлено для представления в счете.
Как правило, это значение следует использовать как есть, когда предоставляется.
* `Суффикс <: текст, используемый при дифференциации отдельных представлений в счете.
Этот аргумент взаимоисключающего для `name`.
* `Detail`: логический, который отличает индивидуальное представление в сфере просмотра как как« список »или« подробный ».

Default: `'rest_framework.views.get_view_name'`

По умолчанию: `'rest_framework.views.get_view_name'

#### VIEW_DESCRIPTION_FUNCTION

#### view_description_function

A string representing the function that should be used when generating view descriptions.

Строка, представляющая функцию, которую следует использовать при генерации описаний представлений.

This setting can be changed to support markup styles other than the default markdown. For example, you can use it to support `rst` markup in your view docstrings being output in the browsable API.

Этот параметр может быть изменен, чтобы поддержать стили разметки, кроме разметки по умолчанию.
Например, вы можете использовать его для поддержки `rst` recke в вашем просмотре DocStrings, выводящихся в API, доступный для просмотра.

This should be a function with the following signature:

Это должно быть функцией со следующей подписью:

```
view_description(self, html=False)
```

* `self`: The view instance. Typically the description function would inspect the docstring of the class when generating a description, by accessing `self.__class__.__doc__`
* `html`: A boolean indicating if HTML output is required. `True` when used in the browsable API, and `False` when used in generating `OPTIONS` responses.

* `self ': экземпляр просмотра.
Обычно функция описания проверяет Docstring класса при генерации описания, получив доступ к `self .__ Класс __.__ DOC__`
* `html`: булево, указывающее, требуется ли вывод HTML.
`True` при использовании в API -файлах для просмотра, и` false 'при использовании при генерации ответов `` ``.

If the view instance inherits `ViewSet`, it may have been initialized with several optional arguments:

Если экземпляр просмотра наследует `viewset`, он мог быть инициализирован несколькими дополнительными аргументами:

* `description`: A description explicitly provided to the view in the viewset. Typically, this is set by extra viewset `action`s, and should be used as-is.

* `description`: описание явно предоставлено для представления в счете.
Как правило, это устанавливается дополнительным Viewset `aection ', и следует использовать как есть.

Default: `'rest_framework.views.get_view_description'`

По умолчанию: `'rest_framework.views.get_view_description' '

## HTML Select Field cutoffs

## HTML Select Field Cutoffs

Global settings for [select field cutoffs for rendering relational fields](relations.md#select-field-cutoffs) in the browsable API.

Глобальные настройки для [выберите поля для рендеринга реляционных полей] (urtations.md#Select-Field-Cutoffs) в API-файлах.

#### HTML_SELECT_CUTOFF

#### html_select_cutoff

Global setting for the `html_cutoff` value. Must be an integer.

Глобальная настройка для значения `html_cutoff`.
Должно быть целое число.

Default: 1000

По умолчанию: 1000

#### HTML_SELECT_CUTOFF_TEXT

#### html_select_cutoff_text

A string representing a global setting for `html_cutoff_text`.

Строка, представляющая глобальную настройку для `html_cutoff_text`.

Default: `"More than {count} items..."`

По умолчанию: `" больше, чем {count} элементы ... "` `

---

## Miscellaneous settings

## Разные настройки

#### EXCEPTION_HANDLER

#### Exception_handler

A string representing the function that should be used when returning a response for any given exception. If the function returns `None`, a 500 error will be raised.

Строка, представляющая функцию, которая должна использоваться при возврате ответа для любого данного исключения.
Если функция возвращает `none`, будет выдвинута ошибка 500.

This setting can be changed to support error responses other than the default `{"detail": "Failure..."}` responses. For example, you can use it to provide API responses like `{"errors": [{"message": "Failure...", "code": ""} ...]}`.

Этот параметр может быть изменен, чтобы поддержать ответы на ошибку, кроме по умолчанию `{" detail ":" affice ... "}` Ответы.
Например, вы можете использовать его для предоставления ответов API, таких как `{" Ошибки ": [{" Message ":" отказ ... "," code ":" "} ...]}`.

This should be a function with the following signature:

Это должно быть функцией со следующей подписью:

```
exception_handler(exc, context)
```

* `exc`: The exception.

* `exc`: исключение.

Default: `'rest_framework.views.exception_handler'`

По умолчанию: `'rest_framework.views.exception_handler''

#### NON_FIELD_ERRORS_KEY

#### non_field_errors_key

A string representing the key that should be used for serializer errors that do not refer to a specific field, but are instead general errors.

Строка, представляющая ключ, который следует использовать для ошибок сериализатора, которые не относятся к конкретному полю, а вместо этого являются общими ошибками.

Default: `'non_field_errors'`

По умолчанию: `non_field_errors'`

#### URL_FIELD_NAME

#### url_field_name

A string representing the key that should be used for the URL fields generated by `HyperlinkedModelSerializer`.

Строка, представляющая ключ, который следует использовать для полей URL, сгенерированных `HyperlinkedModelserializer.

Default: `'url'`

По умолчанию: `url' '

#### NUM_PROXIES

#### num_proxies

An integer of 0 or more, that may be used to specify the number of application proxies that the API runs behind. This allows throttling to more accurately identify client IP addresses. If set to `None` then less strict IP matching will be used by the throttle classes.

Целое число 0 или более, которое может использоваться для указания количества прокси приложений, которые работает API.
Это позволяет дросселизму более точно идентифицировать IP -адреса клиента.
Если установить на `none`, то меньшее строгий сопоставление IP будет использоваться классами дроссельной заслонки.

Default: `None`

По умолчанию: `none