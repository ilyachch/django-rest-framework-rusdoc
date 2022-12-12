<!-- TRANSLATED by md-translate -->
---

source:
    - fields.py

источник:
- fields.py

---

# Serializer fields

# Поля сериализатора

> Each field in a Form class is responsible not only for validating data, but also for "cleaning" it &mdash; normalizing it to a consistent format.
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data)

> Каждое поле в классе формы отвечает не только за проверку данных, но и за «очистку» IT & mdash;
Нормализация его в согласованном формате.
>
> & mdash;
[Документация Django] (https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.form.cleaned_data)

Serializer fields handle converting between primitive values and internal datatypes.  They also deal with validating input values, as well as retrieving and setting the values from their parent objects.

Поля сериализатора обрабатывают преобразование между примитивными значениями и внутренними датами данных.
Они также имеют дело с подтверждением входных значений, а также получением и установкой значений из своих родительских объектов.

---

**Note:** The serializer fields are declared in `fields.py`, but by convention you should import them using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.

** ПРИМЕЧАНИЕ.

---

## Core arguments

## Основные аргументы

Each serializer field class constructor takes at least these arguments.  Some Field classes take additional, field-specific arguments, but the following should always be accepted:

Каждый конструктор класса поля сериализатора принимает как минимум эти аргументы.
Некоторые полевые классы принимают дополнительные, специфичные для поля аргументы, но всегда следует принимать следующее:

### `read_only`

### `read_only`

Read-only fields are included in the API output, but should not be included in the input during create or update operations. Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.

Поля только для чтения включены в вывод API, но не должны быть включены в вход во время операций создания или обновления.
Любые поля «read_only», которые неправильно включены в вход сериализатора, будут игнорироваться.

Set this to `True` to ensure that the field is used when serializing a representation, but is not used when creating or updating an instance during deserialization.

Установите это на «true», чтобы убедиться, что поле используется при сериализации представления, но не используется при создании или обновлении экземпляра во время десериализации.

Defaults to `False`

По умолчанию «ложь»

### `write_only`

### `write_only`

Set this to `True` to ensure that the field may be used when updating or creating an instance, but is not included when serializing the representation.

Установите это на `true`, чтобы убедиться, что поле может использоваться при обновлении или создании экземпляра, но не включено при сериализации представления.

Defaults to `False`

По умолчанию «ложь»

### `required`

### `Обязательный

Normally an error will be raised if a field is not supplied during deserialization.
Set to false if this field is not required to be present during deserialization.

Обычно ошибка будет вызвана, если поле не будет поставляется во время десериализации.
Установите FALSE, если это поле не требуется присутствовать во время десериализации.

Setting this to `False` also allows the object attribute or dictionary key to be omitted from output when serializing the instance. If the key is not present it will simply not be included in the output representation.

Установка этого на `false` также позволяет атрибуту объекта или клавиша словаря быть опущены из вывода при сериализации экземпляра.
Если ключ отсутствует, он просто не будет включен в выходное представление.

Defaults to `True`. If you're using [Model Serializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) default value will be `False` if you have specified `blank=True` or `default` or `null=True` at your field in your `Model`.

По умолчанию «истинно».
Если вы используете [Model Serializer] (https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) значение по умолчанию будет `false`, если вы указали` blank = true
`default` или` null = true` в вашем поле в вашем `model '.

### `default`

### `default`

If set, this gives the default value that will be used for the field if no input value is supplied. If not set the default behaviour is to not populate the attribute at all.

Если установлено, это дает значение по умолчанию, которое будет использоваться для поля, если входное значение не будет предоставлено.
Если не установить поведение по умолчанию, вообще не заполняет атрибут вообще.

The `default` is not applied during partial update operations. In the partial update case only fields that are provided in the incoming data will have a validated value returned.

«По умолчанию» не применяется во время операций с частичным обновлением.
В случае частичного обновления только поля, представленные в входящих данных, будут иметь подтвержденное значение.

May be set to a function or other callable, in which case the value will be evaluated each time it is used. When called, it will receive no arguments. If the callable has a `requires_context = True` attribute, then the serializer field will be passed as an argument.

Может быть установлен на функцию или другую вызов, и в этом случае значение будет оцениваться каждый раз, когда оно будет использоваться.
При вызове он не будет получать аргументов.
Если Callable имеет атрибут `tress_context = true`, то поле сериализатора будет передаваться в качестве аргумента.

For example:

Например:

```
class CurrentUserDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user
```

When serializing the instance, default will be used if the object attribute or dictionary key is not present in the instance.

При сериализации экземпляра будет использоваться по умолчанию, если атрибут объекта или клавиша словаря отсутствует в экземпляре.

Note that setting a `default` value implies that the field is not required. Including both the `default` and `required` keyword arguments is invalid and will raise an error.

Обратите внимание, что настройка значения «по умолчанию» подразумевает, что поле не требуется.
Включение как аргументы ключевых слов как `default, так и` `требуется`, является недействительным и вынесет ошибку.

### `allow_null`

### `allow_null`

Normally an error will be raised if `None` is passed to a serializer field. Set this keyword argument to `True` if `None` should be considered a valid value.

Обычно ошибка будет вызвана, если `none` передается в поле сериализатора.
Установите этот аргумент ключевого слова в `true`, если` none `следует считать допустимым значением.

Note that, without an explicit `default`, setting this argument to `True` will imply a `default` value of `null` for serialization output, but does not imply a default for input deserialization.

Обратите внимание, что без явного «по умолчанию» установление этого аргумента на `true` будет подразумевать значение« дефолт »` null` для вывода сериализации, но не подразумевает дефолт для входной десериализации.

Defaults to `False`

По умолчанию «ложь»

### `source`

### `source`

The name of the attribute that will be used to populate the field.  May be a method that only takes a `self` argument, such as `URLField(source='get_absolute_url')`, or may use dotted notation to traverse attributes, such as `EmailField(source='user.email')`.

Название атрибута, которое будет использоваться для заполнения поля.
Может быть метод, который принимает только аргумент «самостоятельно», такой как `urlfield (source = 'get_absolute_url')`, или может использовать пунктирную нотацию для атрибутов Traverse, таких как `emailfield (source = 'user.email')`.

When serializing fields with dotted notation, it may be necessary to provide a `default` value if any object is not present or is empty during attribute traversal. Beware of possible n+1 problems when using source attribute if you are accessing a relational orm model. For example:

При сериализации полей с пунктирной нотацией может потребоваться предоставить значение «по умолчанию», если какой -либо объект не присутствует или не пуст во время обхода атрибута.
Остерегайтесь возможных задач n+1 при использовании атрибута источника, если вы обращаетесь к реляционной модели ORM.
Например:

```
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField(source="user.email")
```

would require user object to be fetched from database when it is not prefetched. If that is not wanted, be sure to be using `prefetch_related` and `select_related` methods appropriately. For more information about the methods refer to [django documentation](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

потребует, чтобы пользовательский объект был извлечен из базы данных, когда он не будет предварительно выбран.
Если это не нужно, обязательно используйте методы `prefetch_related` и` select_related` соответственно.
Для получения дополнительной информации о методах см.

The value `source='*'` has a special meaning, and is used to indicate that the entire object should be passed through to the field.  This can be useful for creating nested representations, or for fields which require access to the complete object in order to determine the output representation.

Значение `source = '*'` имеет особое значение и используется, чтобы указать, что весь объект должен быть передан в поле.
Это может быть полезно для создания вложенных представлений или для полей, которые требуют доступа к полному объекту, чтобы определить выходное представление.

Defaults to the name of the field.

По умолчанию на имя поля.

### `validators`

### `validators`

A list of validator functions which should be applied to the incoming field input, and which either raise a validation error or simply return. Validator functions should typically raise `serializers.ValidationError`, but Django's built-in `ValidationError` is also supported for compatibility with validators defined in the Django codebase or third party Django packages.

Список функций валидатора, которые должны применяться к входу входящего поля и которые либо вызывают ошибку проверки, либо просто возвращаются.
Функции валидатора, как правило, должны повышать `serializers.validationError`, но встроенный Django« ValidationError »также поддерживается для совместимости с валидаторами, определенными в кодовой базе Django или сторонних пакетах Django.

### `error_messages`

### `error_messages`

A dictionary of error codes to error messages.

Словарь кодов ошибок в сообщениях об ошибках.

### `label`

### `label`

A short text string that may be used as the name of the field in HTML form fields or other descriptive elements.

Короткая текстовая строка, которая может использоваться в качестве имени поля в полевых полях HTML или других описательных элементах.

### `help_text`

### `help_text`

A text string that may be used as a description of the field in HTML form fields or other descriptive elements.

Текстовая строка, которая может использоваться в качестве описания поля в полевых полях HTML или других описательных элементов.

### `initial`

### `initial`

A value that should be used for pre-populating the value of HTML form fields. You may pass a callable to it, just as
you may do with any regular Django `Field`:

Значение, которое следует использовать для предварительной пополнения значения полей формы HTML.
Вы можете передать ему призыв, так же как
Вы можете делать с любым обычным Django `field`:

```
import datetime
from rest_framework import serializers
class ExampleSerializer(serializers.Serializer):
    day = serializers.DateField(initial=datetime.date.today)
```

### `style`

### `style`

A dictionary of key-value pairs that can be used to control how renderers should render the field.

Словарь пар клавишных значений, которые можно использовать для контроля того, как рендерины должны отображать поле.

Two examples here are `'input_type'` and `'base_template'`:

Два примера здесь являются `input_type'` и` 'base_template'::

```
# Use <input type="password"> for the input.
password = serializers.CharField(
    style={'input_type': 'password'}
)

# Use a radio input instead of a select input.
color_channel = serializers.ChoiceField(
    choices=['red', 'green', 'blue'],
    style={'base_template': 'radio.html'}
)
```

For more details see the [HTML & Forms](../topics/html-and-forms.md) documentation.

Для получения более подробной информации см. Документацию [HTML & Forms] (../ Темы/html-and-forms.md).

---

# Boolean fields

# Логические поля

## BooleanField

## Booleanfield

A boolean representation.

Логическое представление.

When using HTML encoded form input be aware that omitting a value will always be treated as setting a field to `False`, even if it has a `default=True` option specified. This is because HTML checkbox inputs represent the unchecked state by omitting the value, so REST framework treats omission as if it is an empty checkbox input.

При использовании кодируемой HTML -входной формы. Имейте в виду, что пропущение значения всегда будет рассматриваться как настройка поля для `false`, даже если оно имеет указанную опцию` default = true`.
Это связано с тем, что входы флажков HTML представляют собой неверное состояние, пропуская значение, поэтому структура REST рассматривает упущение, как будто это пустой вход флажок.

Note that Django 2.1 removed the `blank` kwarg from `models.BooleanField`.
Prior to Django 2.1 `models.BooleanField` fields were always `blank=True`. Thus
since Django 2.1 default `serializers.BooleanField` instances will be generated
without the `required` kwarg (i.e. equivalent to `required=True`) whereas with
previous versions of Django, default `BooleanField` instances will be generated
with a `required=False` option.  If you want to control this behaviour manually,
explicitly declare the `BooleanField` on the serializer class, or use the
`extra_kwargs` option to set the `required` flag.

Обратите внимание, что Django 2.1 удалил `blank` kwarg из` models.booleanfield`.
До Django 2.1 `models.booleanfield` Поля всегда были` blank = true`.
Таким образом
Поскольку Django 2.1 по умолчанию `serializers.booleanfield 'будут созданы экземпляры
Без `rekecle` kwarg (т.е. эквивалент `required = true`), тогда как с
Предыдущие версии Django, по умолчанию `booleanfield 'будут сгенерированы
с опцией `required = false.
Если вы хотите контролировать это поведение вручную,
явно объявите «Booleanfield» на классе сериализатора или используйте
`exuction_kwargs` опция, чтобы установить флаг` required`.

Corresponds to `django.db.models.fields.BooleanField`.

Соответствует `django.db.models.fields.booleanfield`.

**Signature:** `BooleanField()`

** Подпись: ** `booleanfield ()`

---

# String fields

# Строковые поля

## CharField

## Чарфилд

A text representation. Optionally validates the text to be shorter than `max_length` and longer than `min_length`.

Текстовое представление.
При желании проверяет текст, который будет короче, чем `max_length` и длиннее, чем` min_length`.

Corresponds to `django.db.models.fields.CharField` or `django.db.models.fields.TextField`.

Соответствует `django.db.models.fields.charfield` или` django.db.models.fields.textfield`.

**Signature:** `CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`

** Подпись: ** `charfield (max_length = none, min_length = none, alluct_blank = false, trim_whitespace = true)`

* `max_length` - Validates that the input contains no more than this number of characters.
* `min_length` - Validates that the input contains no fewer than this number of characters.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `trim_whitespace` - If set to `True` then leading and trailing whitespace is trimmed. Defaults to `True`.

* `max_length` - подтверждает, что ввод содержит не больше, чем это количество символов.
* `min_length` - подтверждает, что вход содержит не меньше, чем это количество символов.
* `allow_blank` - если установлено в` true`, то пустая строка должна считаться допустимым значением.
Если установить на `false`, то пустая строка считается недействительной и вынесет ошибку проверки.
По умолчанию «ложь».
* `trim_whitespace` - если установлено на` true`, то ведущий и следующий пробел обрезан.
По умолчанию «истинно».

The `allow_null` option is also available for string fields, although its usage is discouraged in favor of `allow_blank`. It is valid to set both `allow_blank=True` and `allow_null=True`, but doing so means that there will be two differing types of empty value permissible for string representations, which can lead to data inconsistencies and subtle application bugs.

Опция `alluct_null` также доступна для строковых полей, хотя его использование не рекомендуется в пользу` alluct_blank`.
Обратно установить как `alluct_blank = true`, так и` alluct_null = true`, но это означает, что будут иметь два различных типа пустого значения, допустимых для представлений строк, что может привести к несоответствиям данных и тонким ошибкам приложения.

## EmailField

## emailfield

A text representation, validates the text to be a valid e-mail address.

Текстовое представление, подтверждает текст действительным адресом электронной почты.

Corresponds to `django.db.models.fields.EmailField`

Соответствует `django.db.models.fields.emailfield`

**Signature:** `EmailField(max_length=None, min_length=None, allow_blank=False)`

** Подпись: ** `emailfield (max_length = none, min_length = none, allow_blank = false)`

## RegexField

## Regexfield

A text representation, that validates the given value matches against a certain regular expression.

Текстовое представление, которое подтверждает заданное значение, сочетается с определенным регулярным выражением.

Corresponds to `django.forms.fields.RegexField`.

Соответствует `django.forms.fields.regexfield`.

**Signature:** `RegexField(regex, max_length=None, min_length=None, allow_blank=False)`

** Подпись: ** `regexfield (regex, max_length = none, min_length = none, alluct_blank = false)`

The mandatory `regex` argument may either be a string, or a compiled python regular expression object.

Обязательный аргумент `regex` может быть либо строкой, либо составленным объектом регулярного выражения Python.

Uses Django's `django.core.validators.RegexValidator` for validation.

Использует Django's `django.core.validators.regexvalidator` для проверки.

## SlugField

## Slugfield

A `RegexField` that validates the input against the pattern `[a-zA-Z0-9_-]+`.

`Regexfield`, который проверяет вход в отношении шаблона` [a-za-z0-9 _-]+`.

Corresponds to `django.db.models.fields.SlugField`.

Соответствует `django.db.models.fields.slugfield`.

**Signature:** `SlugField(max_length=50, min_length=None, allow_blank=False)`

** Подпись: ** `slugfield (max_length = 50, min_length = none, allow_blank = false)`

## URLField

## Урлфилд

A `RegexField` that validates the input against a URL matching pattern. Expects fully qualified URLs of the form `http://<host>/<path>`.

`Regexfield`, который проверяет вход в соответствии с шаблоном соответствия URL -адреса.
Ожидает полностью квалифицированные URL -адреса формы `http: // <host>/<thpe>`.

Corresponds to `django.db.models.fields.URLField`.  Uses Django's `django.core.validators.URLValidator` for validation.

Соответствует `django.db.models.fields.urlfield`.
Использует Django's `django.core.validators.urlvalidator` для проверки.

**Signature:** `URLField(max_length=200, min_length=None, allow_blank=False)`

** Подпись: ** `urlfield (max_length = 200, min_length = none, allow_blank = false)`

## UUIDField

## Uuidfield

A field that ensures the input is a valid UUID string. The `to_internal_value` method will return a `uuid.UUID` instance. On output the field will return a string in the canonical hyphenated format, for example:

Поле, которое обеспечивает входную строку.
Метод `to_internal_value` вернет экземпляр` uuid.uuid`.
На выводе поле возвращает строку в каноническом формате дефисации, например:

```
"de305d54-75b4-431b-adb2-eb6b9e546013"
```

**Signature:** `UUIDField(format='hex_verbose')`

** подпись: ** `uuidfield (format = 'hex_verbose')`

* `format`: Determines the representation format of the uuid value
    - `'hex_verbose'` - The canonical hex representation, including hyphens: `"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`
    - `'hex'` - The compact hex representation of the UUID, not including hyphens: `"5ce0e9a55ffa654bcee01238041fb31a"`
    - `'int'` - A 128 bit integer representation of the UUID: `"123456789012312313134124512351145145114"`
    - `'urn'` - RFC 4122 URN representation of the UUID: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`

* `format`: определяет формат представления значения UUID
-`` hex_verbose'`-каноническое представление шестнадцатеристики, в том числе дефисы: `" 5ce0e9a5-5ffa-654b-cee0-1238041fb31a "` ``
- `'hex'` - компактное шестигранное представление UUID, не считая дефиса:` "5ce0e9a55ffa654bcee01238041fb31a" `` `` `` `` `` `` `` `
- `'int'` - 128 -битное целочисленное представление UUID:` "123456789012312313134124512351145145114" `
-`'urn'`-RFC 4122 URN представление UUID:` "Урн: UUID: 5CE0E9A5-5FFA-654B-CEE0-1238041FB31A" ``

Changing the `format` parameters only affects representation values. All formats are accepted by `to_internal_value`

Изменение параметров «формата» влияет только на значения представления.
Все форматы принимаются `to_internal_value`

## FilePathField

## FilePathfield

A field whose choices are limited to the filenames in a certain directory on the filesystem

Поле, чей выбор ограничен именами файлов в определенном каталоге в файловой системе

Corresponds to `django.forms.fields.FilePathField`.

Соответствует `django.forms.fields.filepathfield`.

**Signature:** `FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`

** Подпись: ** `filePathfield (path, match = none, recurisive = false, alluct_files = true, allow_folders = false, требуется = нет, ** kwargs)`

* `path` - The absolute filesystem path to a directory from which this FilePathField should get its choice.
* `match` - A regular expression, as a string, that FilePathField will use to filter filenames.
* `recursive` - Specifies whether all subdirectories of path should be included.  Default is `False`.
* `allow_files` - Specifies whether files in the specified location should be included. Default is `True`. Either this or `allow_folders` must be `True`.
* `allow_folders` - Specifies whether folders in the specified location should be included. Default is `False`. Either this or `allow_files` must be `True`.

* `path` - путь абсолютной файловой системы к каталогу, из которого этот FilePathfield должен получить свой выбор.
* `match` - регулярное выражение в качестве строки, которое FilePathfield будет использовать для фильтрации имен файлов.
* `recurisive` - указывает, должны ли все подкатарии пути быть включены.
По умолчанию `false`.
* `allow_files` - указывает, должны ли файлы в указанном месте быть включены.
По умолчанию `true '.
Либо это, либо `allow_folders` должен быть` true`.
* `allow_folders` - указывает, должны ли папки в указанном месте быть включены.
По умолчанию `false`.
Либо это, либо `allow_files` должен быть` true`.

## IPAddressField

## iPaddressfield

A field that ensures the input is a valid IPv4 or IPv6 string.

Поле, которое гарантирует входной строки IPv4 или IPv6.

Corresponds to `django.forms.fields.IPAddressField` and `django.forms.fields.GenericIPAddressField`.

Соответствует `django.forms.fields.ipaddressfield` и` django.forms.fields.genericipaddressfield`.

**Signature**: `IPAddressField(protocol='both', unpack_ipv4=False, **options)`

** Подпись **: `iPaddressfield (protocol = 'оба', unpack_ipv4 = false, ** параметры)`

* `protocol` Limits valid inputs to the specified protocol. Accepted values are 'both' (default), 'IPv4' or 'IPv6'. Matching is case insensitive.
* `unpack_ipv4` Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option is enabled that address would be unpacked to 192.0.2.1. Default is disabled. Can only be used when protocol is set to 'both'.

* `Protocol` ограничивает допустимые входы в указанный протокол.
Принятые значения - «оба» (по умолчанию), «IPv4» или «IPv6».
Сопоставление нечувствительно.
* `unpack_ipv4` распаковывать IPv4, отображенные адреса, такие как :: ffff: 192.0.2.1.
Если эта опция включена, адрес будет распакован до 192.0.2.1.
По умолчанию отключено.
Может использоваться только тогда, когда протокол установлен на «оба».

---

# Numeric fields

# Числовые поля

## IntegerField

## integerfield

An integer representation.

Целочисленное представление.

Corresponds to `django.db.models.fields.IntegerField`, `django.db.models.fields.SmallIntegerField`, `django.db.models.fields.PositiveIntegerField` and `django.db.models.fields.PositiveSmallIntegerField`.

Соответствует `django.db.models.fields.integerfield`,` django.db.models.fields.smallintegerfield`, `django.db.models.fields.positiveintegerfield` и` django.db.models.fields.

**Signature**: `IntegerField(max_value=None, min_value=None)`

** подпись **: `integerfield (max_value = none, min_value = none)`

* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.

* `max_value` подтверждает, что предоставленное число не больше, чем это значение.
* `min_value` подтверждает, что предоставленное число не меньше, чем это значение.

## FloatField

## floatfield

A floating point representation.

Плавающее представление.

Corresponds to `django.db.models.fields.FloatField`.

Соответствует `django.db.models.fields.floatfield`.

**Signature**: `FloatField(max_value=None, min_value=None)`

** подпись **: `floatfield (max_value = none, min_value = none)`

* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.

* `max_value` подтверждает, что предоставленное число не больше, чем это значение.
* `min_value` подтверждает, что предоставленное число не меньше, чем это значение.

## DecimalField

## Decimalfield

A decimal representation, represented in Python by a `Decimal` instance.

Десятичное представление, представленное на питоне экземпляром «десятичный».

Corresponds to `django.db.models.fields.DecimalField`.

Соответствует `django.db.models.fields.decimalfield`.

**Signature**: `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`

** подпись **: `decimalfield (max_digits, decimal_places, coerce_to_string = none, max_value = none, min_value = none)`

* `max_digits` The maximum number of digits allowed in the number. It must be either `None` or an integer greater than or equal to `decimal_places`.
* `decimal_places` The number of decimal places to store with the number.
* `coerce_to_string` Set to `True` if string values should be returned for the representation, or `False` if `Decimal` objects should be returned. Defaults to the same value as the `COERCE_DECIMAL_TO_STRING` settings key, which will be `True` unless overridden. If `Decimal` objects are returned by the serializer, then the final output format will be determined by the renderer. Note that setting `localize` will force the value to `True`.
* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.
* `localize` Set to `True` to enable localization of input and output based on the current locale. This will also force `coerce_to_string` to `True`. Defaults to `False`. Note that data formatting is enabled if you have set `USE_L10N=True` in your settings file.
* `rounding` Sets the rounding mode used when quantising to the configured precision. Valid values are [`decimal` module rounding modes](https://docs.python.org/3/library/decimal.html#rounding-modes). Defaults to `None`.

* `max_digits` Максимальное количество цифр, разрешенное в номере.
Это должно быть либо `none`, либо целое число, больше, чем или равно` decimal_places`.
* `decimal_places` Количество десятичных знаков для хранения с номером.
* `coerce_to_string` Установите в` true`, если строковые значения должны быть возвращены для представления, или `false`, если следует возвращать объекты` decimal '.
По умолчанию к тому же значению, что и клавиша настройки `coerce_decimal_to_string
Если объекты «десятичные» возвращаются сериализатором, то окончательный выходной формат будет определяться рендерером.
Обратите внимание, что настройка `localize` приведет к значению` true '.
* `max_value` подтверждает, что предоставленное число не больше, чем это значение.
* `min_value` подтверждает, что предоставленное число не меньше, чем это значение.
* `Localize` установите в` true`, чтобы включить локализацию ввода и вывода на основе текущей локали.
Это также заставит `coerce_to_string` к` true`.
По умолчанию «ложь».
Обратите внимание, что форматирование данных включено, если вы установили `use_l10n = true` в файле настроек.
* `Rounding` Устанавливает режим округления, используемый при количественном определении до настроенной точности.
Допустимыми значениями являются [`` decimal 'модуль режимы округления] (https://docs.python.org/3/library/decimal.html#rounding-dodes).
По умолчанию «нет».

#### Example usage

#### Пример использования

To validate numbers up to 999 with a resolution of 2 decimal places, you would use:

Чтобы проверить числа до 999 с разрешением из 2 десятичных знаков, вы будете использовать:

```
serializers.DecimalField(max_digits=5, decimal_places=2)
```

And to validate numbers up to anything less than one billion with a resolution of 10 decimal places:

И подтвердить цифры до чего -либо меньше одного миллиарда с разрешением 10 десятичных знаков:

```
serializers.DecimalField(max_digits=19, decimal_places=10)
```

---

# Date and time fields

# Поля даты и времени

## DateTimeField

## datetimefield

A date and time representation.

Дата и временное представление.

Corresponds to `django.db.models.fields.DateTimeField`.

Соответствует `django.db.models.fields.datetimefield`.

**Signature:** `DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)`

** Подпись: ** `dateTimefield (format = api_settings.datetime_format, input_formats = none, default_timezone = none)`

* `format` - A string representing the output format. If not specified, this defaults to the same value as the `DATETIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `datetime` objects should be returned by `to_representation`. In this case the datetime encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date.  If not specified, the `DATETIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.
* `default_timezone` - A `tzinfo` subclass (`zoneinfo` or `pytz`) prepresenting the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone). If `USE_TZ` is disabled, then datetime objects will be naive.

* `format` - строка, представляющая выходной формат.
Если не указано, это по умолчанию к тому же значению, что и клавиша настройки `datetime_format`, которая будет` 'iso-8601' », если не установлено.
Настройка на строку формата указывает на то, что возвращаемые значения `to_representation` должны быть принуждены к выводу строки.
Строки формата описаны ниже.
Установка этого значения на «Нет» указывает на то, что объекты Python `datetime` должны возвращаться` to_representation`.
В этом случае кодирование DateTime будет определена рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут использоваться для анализа даты.
Если не указано, будет использоваться настройка `datetime_input_formats`, которая по умолчанию по умолчанию« ['iso-8601'] `.
* `default_timezone` - a` tzinfo` subclass (`ZoneInfo` или` pytz`) предварительно презентации часового пояс.
Если не указано, и настройка `use_tz` включена, это по умолчанию [текущий часовой застрой] (https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and----
текущее время).
Если `use_tz` отключен, то объекты DateTime будут наивными.

#### `DateTimeField` format strings.

#### `DateTimefield` формат строки.

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style datetimes should be used. (eg `'2013-01-29T12:34:56.000000Z'`)

Строки формата могут быть либо [python strftime formats] (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат или специальную строку `'iso
-8601'`, что указывает на то, что [ISO 8601] (https://www.w3.org/tr/note-datetime) Стиль должен использоваться.
(Например, 2013-01-29t12: 34: 56.000000Z' ')

When a value of `None` is used for the format `datetime` objects will be returned by `to_representation` and the final output representation will determined by the renderer class.

Когда значение «Нет» используется для объектов формата `datetime`, будет возвращено` to_representation`, а конечное представление вывода будет определена классом рендеринга.

#### `auto_now` and `auto_now_add` model fields.

#### `auto_now` и` auto_now_add` поля модели.

When using `ModelSerializer` or `HyperlinkedModelSerializer`, note that any model fields with `auto_now=True` or `auto_now_add=True` will use serializer fields that are `read_only=True` by default.

При использовании `modelerializer` или` HyperlinkedModelserializer. Обратите внимание, что любые поля модели с `auto_now = true` или` auto_now_add = true` будут использовать поля сериализатора, которые являются `read_only = true` по умолчанию.

If you want to override this behavior, you'll need to declare the `DateTimeField` explicitly on the serializer.  For example:

Если вы хотите переопределить это поведение, вам нужно явно объявить «DateTimefield» на сериализаторе.
Например:

```
class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField()

    class Meta:
        model = Comment
```

## DateField

## datefield

A date representation.

Представление даты.

Corresponds to `django.db.models.fields.DateField`

Соответствует `django.db.models.fields.datefield`

**Signature:** `DateField(format=api_settings.DATE_FORMAT, input_formats=None)`

** Подпись: ** `datefield (format = api_settings.date_format, input_formats = none)`

* `format` - A string representing the output format.  If not specified, this defaults to the same value as the `DATE_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `date` objects should be returned by `to_representation`. In this case the date encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date.  If not specified, the `DATE_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.

* `format` - строка, представляющая выходной формат.
Если не указано, это по умолчанию к тому же значению, что и клавиша настройки `date_format`, которая будет` 'iso-8601'.
Настройка на строку формата указывает на то, что возвращаемые значения `to_representation` должны быть принуждены к выводу строки.
Строки формата описаны ниже.
Установка этого значения на «Нет» указывает на то, что объекты Python `date 'должны возвращаться` to_representation`.
В этом случае кодирование даты будет определяться рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут использоваться для анализа даты.
Если не указано, будет использоваться настройка `date_input_formats`, которая по умолчанию по умолчанию` ['iso-8601'] `.

#### `DateField` format strings

#### `strings format strings datefield`

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style dates should be used. (eg `'2013-01-29'`)

Строки формата могут быть либо [python strftime formats] (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат или специальную строку `'iso
-8601'`, что указывает на то, что [ISO 8601] (https://www.w3.org/tr/note-datetime) Следует использовать даты стиля.
(Например, 2013-01-29' ')

## TimeField

## Timefield

A time representation.

Репрезентация времени.

Corresponds to `django.db.models.fields.TimeField`

Соответствует `django.db.models.fields.timefield`

**Signature:** `TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`

** Подпись: ** `timefield (format = api_settings.time_format, input_formats = none)`

* `format` - A string representing the output format.  If not specified, this defaults to the same value as the `TIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `time` objects should be returned by `to_representation`. In this case the time encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date.  If not specified, the `TIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.

* `format` - строка, представляющая выходной формат.
Если не указано, это по умолчанию к тому же значению, что и клавиша настройки `time_format`, которая будет` 'iso-8601'.
Настройка на строку формата указывает на то, что возвращаемые значения `to_representation` должны быть принуждены к выводу строки.
Строки формата описаны ниже.
Установка этого значения на «Нет» указывает на то, что объекты Python `time` должны возвращаться` to_representation`.
В этом случае кодирование времени будет определяться рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут использоваться для анализа даты.
Если не указано, будет использоваться настройка `time_input_formats`, что по умолчанию по умолчанию« ['iso-8601'] `.

#### `TimeField` format strings

#### `timefield` strings формата формата

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style times should be used. (eg `'12:34:56.000000'`)

Строки формата могут быть либо [python strftime formats] (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат или специальную строку `'iso
-8601'`, что указывает на то, что [iso 8601] (https://www.w3.org/tr/note-datetime)
(например, `'12: 34: 56.000000'`)

## DurationField

## Durationfield

A Duration representation.
Corresponds to `django.db.models.fields.DurationField`

Продолжительное представление.
Соответствует `django.db.models.fields.durationfield`

The `validated_data` for these fields will contain a `datetime.timedelta` instance.
The representation is a string following this format `'[DD] [HH:[MM:]]ss[.uuuuuu]'`.

Для этих полей `valyated_data` будет содержать экземпляр` datetime.timedelta`.
Репрезентация представляет собой строку, следующую за этим форматом `'[dd] [HH: [MM:]] SS [.uuuuuuu]'`.

**Signature:** `DurationField(max_value=None, min_value=None)`

** Подпись: ** `durationfield (max_value = none, min_value = none)`

* `max_value` Validate that the duration provided is no greater than this value.
* `min_value` Validate that the duration provided is no less than this value.

* `max_value` подтверждает, что предоставленная продолжительность не больше этого значения.
* `min_value` подтверждает, что предоставленная продолжительность не меньше, чем это значение.

---

# Choice selection fields

# Поля выбора

## ChoiceField

## Choicefield

A field that can accept a value out of a limited set of choices.

Поле, которое может принять значение из ограниченного набора вариантов.

Used by `ModelSerializer` to automatically generate fields if the corresponding model field includes a `choices=…` argument.

Используется `modelseRializer` для автоматического генерации полей, если соответствующее поле модели включает в себя аргумент` shocates =… `.

**Signature:** `ChoiceField(choices)`

** Подпись: ** `Choicefield (выбор)`

* `choices` - A list of valid values, or a list of `(key, display_name)` tuples.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Can be used to ensure that automatically generated ChoiceFields with very large possible selections do not prevent a template from rendering. Defaults to `None`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `Choices` - список допустимых значений или список` (key, display_name) `cuples.
* `allow_blank` - если установлено в` true`, то пустая строка должна считаться допустимым значением.
Если установить на `false`, то пустая строка считается недействительной и вынесет ошибку проверки.
По умолчанию «ложь».
* `html_cutoff` - Если установлено, это будет максимальное количество вариантов, которые будут отображаться с помощью HTML Select Dlop Down.
Может использоваться для обеспечения автоматического генерируемого выбора, с очень большими возможными выборами не предотвращают рендеринг шаблона.
По умолчанию «нет».
* `html_cutoff_text` - Если установлено, это отобразит текстовый индикатор, если максимальное количество элементов было отсечено в выберите HTML Select.
По умолчанию `" больше, чем {count} элементы… "` `

Both the `allow_blank` and `allow_null` are valid options on `ChoiceField`, although it is highly recommended that you only use one and not both. `allow_blank` should be preferred for textual choices, and `allow_null` should be preferred for numeric or other non-textual choices.

И `alluck_blank`, и` alluct_null` являются допустимыми параметрами на `Choicefield`, хотя настоятельно рекомендуется использовать только один, а не оба.
`alluct_blank` должен быть предпочтительным для текстового выбора, а` alluct_null` должен быть предпочтительным для числовых или других не текстовых вариантов.

## MultipleChoiceField

## Multiplechoicefield

A field that can accept a set of zero, one or many values, chosen from a limited set of choices. Takes a single mandatory argument. `to_internal_value` returns a `set` containing the selected values.

Поле, которое может принять набор нуля, одного или многих значений, выбранных из ограниченного набора вариантов.
Берет один обязательный аргумент.
`to_internal_value` возвращает` set`, содержащий выбранные значения.

**Signature:** `MultipleChoiceField(choices)`

** Подпись: ** `multiplechoicefield (выбор)`

* `choices` - A list of valid values, or a list of `(key, display_name)` tuples.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Can be used to ensure that automatically generated ChoiceFields with very large possible selections do not prevent a template from rendering. Defaults to `None`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `Choices` - список допустимых значений или список` (key, display_name) `cuples.
* `allow_blank` - если установлено в` true`, то пустая строка должна считаться допустимым значением.
Если установить на `false`, то пустая строка считается недействительной и вынесет ошибку проверки.
По умолчанию «ложь».
* `html_cutoff` - Если установлено, это будет максимальное количество вариантов, которые будут отображаться с помощью HTML Select Dlop Down.
Может использоваться для обеспечения автоматического генерируемого выбора, с очень большими возможными выборами не предотвращают рендеринг шаблона.
По умолчанию «нет».
* `html_cutoff_text` - Если установлено, это отобразит текстовый индикатор, если максимальное количество элементов было отсечено в выберите HTML Select.
По умолчанию `" больше, чем {count} элементы… "` `

As with `ChoiceField`, both the `allow_blank` and `allow_null` options are valid, although it is highly recommended that you only use one and not both. `allow_blank` should be preferred for textual choices, and `allow_null` should be preferred for numeric or other non-textual choices.

Как и в случае с `Choicefield`, как параметры` alluct_blank`, так и `alluct_null` действительны, хотя настоятельно рекомендуется использовать только один, а не оба.
`alluct_blank` должен быть предпочтительным для текстового выбора, а` alluct_null` должен быть предпочтительным для числовых или других не текстовых вариантов.

---

# File upload fields

# Поля загрузки файла

#### Parsers and file uploads.

#### Парсеры и загрузки файлов.

The `FileField` and `ImageField` classes are only suitable for use with `MultiPartParser` or `FileUploadParser`. Most parsers, such as e.g. JSON don't support file uploads.
Django's regular [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS) are used for handling uploaded files.

Классы `filefield` и` Imagefield` подходят только для использования с `multiparparser` или` fileuploadParser`.
Большинство анализаторов, например, например,
JSON не поддерживает загрузки файлов.
Регулярные Django [file_upload_handlers] (https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-file_upload_handlers) используются для обработки загруженных файлов.

## FileField

## filefield

A file representation.  Performs Django's standard FileField validation.

Представление файла.
Выполняет стандартную проверку FileField Django.

Corresponds to `django.forms.fields.FileField`.

Соответствует `django.forms.fields.filefield`.

**Signature:** `FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

** Подпись: ** `filefield (max_length = none, alluct_empty_file = false, use_url = uploaded_files_use_url)`

* `max_length` - Designates the maximum length for the file name.
* `allow_empty_file` - Designates if empty files are allowed.
* `use_url` - If set to `True` then URL string values will be used for the output representation. If set to `False` then filename string values will be used for the output representation. Defaults to the value of the `UPLOADED_FILES_USE_URL` settings key, which is `True` unless set otherwise.

* `max_length` - обозначает максимальную длину для имени файла.
* `allow_empty_file` - назначает, разрешены ли пустые файлы.
* `use_url` - если установлено в` true`, то значения строки URL будут использоваться для выходного представления.
Если установлено в `false`, то для выходного представления будут использоваться значения строковых файлов.
По умолчанию значения клавиши настроек `uploaded_files_use_url`, которая является` true`, если не установлено иное.

## ImageField

## Imagefield

An image representation. Validates the uploaded file content as matching a known image format.

Представление изображения.
Проверяет загруженный содержимое файла в качестве сопоставления известного формата изображения.

Corresponds to `django.forms.fields.ImageField`.

Соответствует `django.forms.fields.imagefield`.

**Signature:** `ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

** Подпись: ** `Imagefield (max_length = none, alluct_empty_file = false, use_url = uploaded_files_use_url)`

* `max_length` - Designates the maximum length for the file name.
* `allow_empty_file` - Designates if empty files are allowed.
* `use_url` - If set to `True` then URL string values will be used for the output representation. If set to `False` then filename string values will be used for the output representation. Defaults to the value of the `UPLOADED_FILES_USE_URL` settings key, which is `True` unless set otherwise.

* `max_length` - обозначает максимальную длину для имени файла.
* `allow_empty_file` - назначает, разрешены ли пустые файлы.
* `use_url` - если установлено в` true`, то значения строки URL будут использоваться для выходного представления.
Если установлено в `false`, то для выходного представления будут использоваться значения строковых файлов.
По умолчанию значения клавиши настроек `uploaded_files_use_url`, которая является` true`, если не установлено иное.

Requires either the `Pillow` package or `PIL` package.  The `Pillow` package is recommended, as `PIL` is no longer actively maintained.

Требуется либо пакет «подушки», либо пакет «PIL».
Рекомендуется пакет «подушки», так как «PIL» больше не поддерживается.

---

# Composite fields

# Составные поля

## ListField

## Listfield

A field class that validates a list of objects.

Полевой класс, который проверяет список объектов.

**Signature**: `ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)`

** Подпись **: `listfield (child = <a_field_instance>, allow_empty = true, min_length = none, max_length = none)`

* `child` - A field instance that should be used for validating the objects in the list. If this argument is not provided then objects in the list will not be validated.
* `allow_empty` - Designates if empty lists are allowed.
* `min_length` - Validates that the list contains no fewer than this number of elements.
* `max_length` - Validates that the list contains no more than this number of elements.

* `Child` - экземпляр поля, который следует использовать для проверки объектов в списке.
Если этот аргумент не предоставлен, то объекты в списке не будут подтверждены.
* `allow_empty` - назначает, разрешены ли пустые списки.
* `min_length` - подтверждает, что список содержит не меньше, чем это количество элементов.
* `max_length` - подтверждает, что список содержит не больше этого количества элементов.

For example, to validate a list of integers you might use something like the following:

Например, чтобы проверить список целых чисел, вы можете использовать что -то вроде следующего:

```
scores = serializers.ListField(
   child=serializers.IntegerField(min_value=0, max_value=100)
)
```

The `ListField` class also supports a declarative style that allows you to write reusable list field classes.

Класс `Listfield` также поддерживает декларативный стиль, который позволяет вам писать многократные полевые классы Listable.

```
class StringListField(serializers.ListField):
    child = serializers.CharField()
```

We can now reuse our custom `StringListField` class throughout our application, without having to provide a `child` argument to it.

Теперь мы можем повторно использовать наш пользовательский класс `stringlistfield` на протяжении всего нашего приложения, не предоставляя ему аргумент« ребенка ».

## DictField

## dictfield

A field class that validates a dictionary of objects. The keys in `DictField` are always assumed to be string values.

Полевой класс, который проверяет словарь объектов.
Ключи в «dictfield» всегда предполагается, что это строковые значения.

**Signature**: `DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

** Подпись **: `dictfield (child = <a_field_instance>, ally_empty = true)`

* `child` - A field instance that should be used for validating the values in the dictionary. If this argument is not provided then values in the mapping will not be validated.
* `allow_empty` - Designates if empty dictionaries are allowed.

* `Child` - экземпляр поля, который следует использовать для проверки значений в словаре.
Если этот аргумент не предоставлен, то значения в отображении не будут подтверждены.
* `allow_empty` - обозначает, разрешены ли пустые словаря.

For example, to create a field that validates a mapping of strings to strings, you would write something like this:

Например, чтобы создать поле, которое проверяет отображение строк на строки, вы бы написали что -то вроде этого:

```
document = DictField(child=CharField())
```

You can also use the declarative style, as with `ListField`. For example:

Вы также можете использовать декларативный стиль, как с `listfield`.
Например:

```
class DocumentField(DictField):
    child = CharField()
```

## HStoreField

## hstorefield

A preconfigured `DictField` that is compatible with Django's postgres `HStoreField`.

Предварительно настроенный «dictfield», который совместим с постгресом Джанго «hstorefield».

**Signature**: `HStoreField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

** Подпись **: `hstorefield (child = <a_field_instance>, ally_empty = true)`

* `child` - A field instance that is used for validating the values in the dictionary. The default child field accepts both empty strings and null values.
* `allow_empty` - Designates if empty dictionaries are allowed.

* `Child` - экземпляр поля, который используется для проверки значений в словаре.
Детское поле по умолчанию принимает как пустые строки, так и нулевые значения.
* `allow_empty` - обозначает, разрешены ли пустые словаря.

Note that the child field **must** be an instance of `CharField`, as the hstore extension stores values as strings.

Обратите внимание, что детское поле ** должно ** быть экземпляром `charfield`, так как расширение Hstore сохраняет значения в виде строк.

## JSONField

## jsonfield

A field class that validates that the incoming data structure consists of valid JSON primitives. In its alternate binary mode, it will represent and validate JSON-encoded binary strings.

Полевой класс, который подтверждает, что входящая структура данных состоит из действительных примитивов JSON.
В своем альтернативном двоичном режиме он будет представлять и проверять кодируемые JSON бинарные строки.

**Signature**: `JSONField(binary, encoder)`

** подпись **: `jsonfield (бинарный, энкодер)`

* `binary` - If set to `True` then the field will output and validate a JSON encoded string, rather than a primitive data structure. Defaults to `False`.
* `encoder` - Use this JSON encoder to serialize input object. Defaults to `None`.

* `Binary` - если установлено в` true`, то поле выведет и проверяет строку, закодированную JSON, а не примитивную структуру данных.
По умолчанию «ложь».
* `encoder` - Используйте этот энкодер JSON для сериализации входного объекта.
По умолчанию «нет».

---

# Miscellaneous fields

# Разные поля

## ReadOnlyField

## readonlyfield

A field class that simply returns the value of the field without modification.

Полевой класс, который просто возвращает значение поля без модификации.

This field is used by default with `ModelSerializer` when including field names that relate to an attribute rather than a model field.

Это поле используется по умолчанию с `moderializer` при включении имен поля, которые относятся к атрибуту, а не по поле модели.

**Signature**: `ReadOnlyField()`

** Подпись **: `readonlyfield ()`

For example, if `has_expired` was a property on the `Account` model, then the following serializer would automatically generate it as a `ReadOnlyField`:

Например, если `has_expired` был свойством на модели` choucchting`, то следующий сериализатор автоматически генерирует его как `readonlyfield`:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'has_expired']
```

## HiddenField

## Hiddenfield

A field class that does not take a value based on user input, but instead takes its value from a default value or callable.

Полевой класс, который не принимает значение на основе пользовательского ввода, но вместо этого берет свое значение из значения по умолчанию или Callable.

**Signature**: `HiddenField()`

** подпись **: `hiddenfield ()`

For example, to include a field that always provides the current time as part of the serializer validated data, you would use the following:

Например, чтобы включить поле, которое всегда предоставляет текущее время как часть проверенных данных сериализатора, вы будете использовать следующее:

```
modified = serializers.HiddenField(default=timezone.now)
```

The `HiddenField` class is usually only needed if you have some validation that needs to run based on some pre-provided field values, but you do not want to expose all of those fields to the end user.

Класс «Hiddenfield» обычно требуется только в том случае, если у вас есть некоторая проверка, которая должна работать на основе некоторых предварительно предоставленных значений поля, но вы не хотите выставлять все эти поля конечному пользователю.

For further examples on `HiddenField` see the [validators](validators.md) documentation.

Для дальнейших примеров на `hiddenfield` см. Документацию [validators] (validators.md).

## ModelField

## modelfield

A generic field that can be tied to any arbitrary model field. The `ModelField` class delegates the task of serialization/deserialization to its associated model field.  This field can be used to create serializer fields for custom model fields, without having to create a new custom serializer field.

Общее поле, которое может быть связано с любым произвольным полем модели.
Класс `modelfield` делегирует задачу сериализации/десериализации в связанное с ним поле модели.
Это поле можно использовать для создания полей сериализатора для пользовательских полей модели, без необходимости создания нового пользовательского поля сериализатора.

This field is used by `ModelSerializer` to correspond to custom model field classes.

Это поле используется `modelseRializer` для соответствия пользовательским классам поля модели.

**Signature:** `ModelField(model_field=<Django ModelField instance>)`

** Подпись: ** `modelfield (model_field = <django modelfield экземпляр>)`

The `ModelField` class is generally intended for internal use, but can be used by your API if needed.  In order to properly instantiate a `ModelField`, it must be passed a field that is attached to an instantiated model.  For example: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`

Класс `modelfield` обычно предназначен для внутреннего использования, но может использоваться вашим API, если это необходимо.
Чтобы должным образом создать экземпляр «Modelfield», его необходимо пройти поле, которое прикреплено к созданной модели.
Например: `modelfield (model_field = mymodel () ._ meta.get_field ('custom_field'))`

## SerializerMethodField

## serializermethodfield

This is a read-only field. It gets its value by calling a method on the serializer class it is attached to. It can be used to add any sort of data to the serialized representation of your object.

Это поле только для чтения.
Он получает свое значение, вызывая метод в классе сериализатора, к которому он прикреплен.
Его можно использовать для добавления любых данных к сериализованному представлению вашего объекта.

**Signature**: `SerializerMethodField(method_name=None)`

** подпись **: `serializermethodfield (method_name = none)`

* `method_name` - The name of the method on the serializer to be called. If not included this defaults to `get_<field_name>`.

* `method_name` - Имя метода на сериализаторе, который будет вызван.
Если не включить эти значения по умолчанию, чтобы `get_ <field_name>`.

The serializer method referred to by the `method_name` argument should accept a single argument (in addition to `self`), which is the object being serialized. It should return whatever you want to be included in the serialized representation of the object. For example:

Метод сериализатора, упомянутый аргументом `method_name`, должен принять единый аргумент (в дополнение к« self »), который является сериализованным объектом.
Он должен вернуть все, что вы хотите, чтобы быть включенным в сериализованное представление объекта.
Например:

```
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
```

---

# Custom fields

# Настраиваемые поля

If you want to create a custom field, you'll need to subclass `Field` and then override either one or both of the `.to_representation()` and `.to_internal_value()` methods.  These two methods are used to convert between the initial datatype, and a primitive, serializable datatype. Primitive datatypes will typically be any of a number, string, boolean, `date`/`time`/`datetime` or `None`. They may also be any list or dictionary like object that only contains other primitive objects. Other types might be supported, depending on the renderer that you are using.

Если вы хотите создать пользовательское поле, вам нужно будет подкласс «Field», а затем переопределить один или оба из методов `.to_representation ()` и `.to_internal_value ()`.
Эти два метода используются для преобразования между исходным датом и примитивным сериализуемым данных.
Примитивными данными дата, как правило, являются любым числом, строкой, логическим, `date`/` time`/`datetime` или` none`.
Они также могут быть любым списком или словарным объектом, который содержит только другие примитивные объекты.
Другие типы могут быть поддержаны, в зависимости от рендеринга, который вы используете.

The `.to_representation()` method is called to convert the initial datatype into a primitive, serializable datatype.

Метод `.to_representation ()` вызывается для преобразования начального дата в примитивный, сериализуемый данных.

The `.to_internal_value()` method is called to restore a primitive datatype into its internal python representation. This method should raise a `serializers.ValidationError` if the data is invalid.

Метод `.to_internal_value ()` вызывается для восстановления примитивного данных в своем внутреннем представлении Python.
Этот метод должен поднять `serializers.validationError`, если данные недействительны.

## Examples

## Примеры

### A Basic Custom Field

### Основное пользовательское поле

Let's look at an example of serializing a class that represents an RGB color value:

Давайте посмотрим на пример сериализации класса, который представляет значение цвета RGB:

```
class Color:
    """
    A color represented in the RGB colorspace.
    """
    def __init__(self, red, green, blue):
        assert(red >= 0 and green >= 0 and blue >= 0)
        assert(red < 256 and green < 256 and blue < 256)
        self.red, self.green, self.blue = red, green, blue

class ColorField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, value):
        return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)

    def to_internal_value(self, data):
        data = data.strip('rgb(').rstrip(')')
        red, green, blue = [int(col) for col in data.split(',')]
        return Color(red, green, blue)
```

By default field values are treated as mapping to an attribute on the object.  If you need to customize how the field value is accessed and set you need to override `.get_attribute()` and/or `.get_value()`.

По умолчанию значения поля рассматриваются как сопоставление с атрибутом на объекте.
Если вам нужно настроить, как доступ к значению поля и установлено, вам нужно переопределить `.get_attribute ()` и/или `.get_value ()`.

As an example, let's create a field that can be used to represent the class name of the object being serialized:

В качестве примера, давайте создадим поле, которое можно использовать для представления имени класса сериализованного объекта:

```
class ClassNameField(serializers.Field):
    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        return value.__class__.__name__
```

### Raising validation errors

### повышение ошибок проверки

Our `ColorField` class above currently does not perform any data validation.
To indicate invalid data, we should raise a `serializers.ValidationError`, like so:

Наш класс «Colorfield» выше в настоящее время не выполняет никакой проверки данных.
Чтобы указать неверные данные, мы должны поднять «serializers.validationError», как так:

```
def to_internal_value(self, data):
    if not isinstance(data, str):
        msg = 'Incorrect type. Expected a string, but got %s'
        raise ValidationError(msg % type(data).__name__)

    if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
        raise ValidationError('Incorrect format. Expected `rgb(#,#,#)`.')

    data = data.strip('rgb(').rstrip(')')
    red, green, blue = [int(col) for col in data.split(',')]

    if any([col > 255 or col < 0 for col in (red, green, blue)]):
        raise ValidationError('Value out of range. Must be between 0 and 255.')

    return Color(red, green, blue)
```

The `.fail()` method is a shortcut for raising `ValidationError` that takes a message string from the `error_messages` dictionary. For example:

Метод `.fail ()` - это ярлык для повышения `valyationError
Например:

```
default_error_messages = {
    'incorrect_type': 'Incorrect type. Expected a string, but got {input_type}',
    'incorrect_format': 'Incorrect format. Expected `rgb(#,#,#)`.',
    'out_of_range': 'Value out of range. Must be between 0 and 255.'
}

def to_internal_value(self, data):
    if not isinstance(data, str):
        self.fail('incorrect_type', input_type=type(data).__name__)

    if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
        self.fail('incorrect_format')

    data = data.strip('rgb(').rstrip(')')
    red, green, blue = [int(col) for col in data.split(',')]

    if any([col > 255 or col < 0 for col in (red, green, blue)]):
        self.fail('out_of_range')

    return Color(red, green, blue)
```

This style keeps your error messages cleaner and more separated from your code, and should be preferred.

Этот стиль сохраняет ваши сообщения об ошибках чище и более отделенным от вашего кода, и должен быть предпочтительным.

### Using `source='*'`

### с помощью `source = '*'` `

Here we'll take an example of a *flat* `DataPoint` model with `x_coordinate` and `y_coordinate` attributes.

Здесь мы возьмем пример модели * ровной * `DataPoint` с атрибутами` x_coordination` и `y_coordinate`.

```
class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()
```

Using a custom field and `source='*'` we can provide a nested representation of
the coordinate pair:

Использование пользовательского поля и `source = '*' Мы можем предоставить вложенное представление
Координатная пара:

```
class CoordinateField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "x": value.x_coordinate,
            "y": value.y_coordinate
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "x_coordinate": data["x"],
            "y_coordinate": data["y"],
        }
        return ret


class DataPointSerializer(serializers.ModelSerializer):
    coordinates = CoordinateField(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']
```

Note that this example doesn't handle validation. Partly for that reason, in a
real project, the coordinate nesting might be better handled with a nested serializer
using `source='*'`, with two `IntegerField` instances, each with their own `source`
pointing to the relevant field.

Обратите внимание, что этот пример не обрабатывает проверку.
Частично по этой причине, в
Настоящий проект, координатное гнездование может быть лучше обработано с вложенным сериализатором
Использование `source = '*'`, с двумя экземплярами `integerfield`, каждый со своим собственным« источником »
указывая на соответствующее поле.

The key points from the example, though, are:

Ключевыми моментами из примера, однако, являются:

* `to_representation` is passed the entire `DataPoint` object and must map from that

* `to_representation` передается весь объект DataPoint 'и должен отобразить из этого

to the desired output.

к желаемому выводу.

```
>>> instance = DataPoint(label='Example', x_coordinate=1, y_coordinate=2)
    >>> out_serializer = DataPointSerializer(instance)
    >>> out_serializer.data
    ReturnDict([('label', 'Example'), ('coordinates', {'x': 1, 'y': 2})])
```

* Unless our field is to be read-only, `to_internal_value` must map back to a dict

* Если наше поле должно быть только для чтения, `to_internal_value

suitable for updating our target object. With `source='*'`, the return from
`to_internal_value` will update the root validated data dictionary, rather than a single key.

Подходит для обновления нашего целевого объекта.
С `source = '*'` return от
`TO_INTERNAL_VALUE` будет обновлять версированный корневой словарь данных, а не один ключ.

```
>>> data = {
    ...     "label": "Second Example",
    ...     "coordinates": {
    ...         "x": 3,
    ...         "y": 4,
    ...     }
    ... }
    >>> in_serializer = DataPointSerializer(data=data)
    >>> in_serializer.is_valid()
    True
    >>> in_serializer.validated_data
    OrderedDict([('label', 'Second Example'),
                 ('y_coordinate', 4),
                 ('x_coordinate', 3)])
```

For completeness lets do the same thing again but with the nested serializer
approach suggested above:

Для полноты давайте снова сделаем то же самое, но с вложенным сериализатором
Подход предложено выше:

```
class NestedCoordinateSerializer(serializers.Serializer):
    x = serializers.IntegerField(source='x_coordinate')
    y = serializers.IntegerField(source='y_coordinate')


class DataPointSerializer(serializers.ModelSerializer):
    coordinates = NestedCoordinateSerializer(source='*')

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']
```

Here the mapping between the target and source attribute pairs (`x` and
`x_coordinate`, `y` and `y_coordinate`) is handled in the `IntegerField`
declarations. It's our `NestedCoordinateSerializer` that takes `source='*'`.

Здесь отображение между парами атрибутов цели и источника (`x` и
`x_coordinate`,` y` и `y_coordinate`) обрабатывается в` integerfield`
декларации.
Это наш `nestedCoordinateSerializer`, который принимает` source = '*' `.

Our new `DataPointSerializer` exhibits the same behaviour as the custom field
approach.

Наш новый `DataPointSerializer` демонстрирует то же поведение, что и на пользовательском поле
подход.

Serializing:

Сериализация:

```
>>> out_serializer = DataPointSerializer(instance)
>>> out_serializer.data
ReturnDict([('label', 'testing'),
            ('coordinates', OrderedDict([('x', 1), ('y', 2)]))])
```

Deserializing:

Десериализация:

```
>>> in_serializer = DataPointSerializer(data=data)
>>> in_serializer.is_valid()
True
>>> in_serializer.validated_data
OrderedDict([('label', 'still testing'),
             ('x_coordinate', 3),
             ('y_coordinate', 4)])
```

But we also get the built-in validation for free:

Но мы также получаем встроенную проверку бесплатно:

```
>>> invalid_data = {
...     "label": "still testing",
...     "coordinates": {
...         "x": 'a',
...         "y": 'b',
...     }
... }
>>> invalid_serializer = DataPointSerializer(data=invalid_data)
>>> invalid_serializer.is_valid()
False
>>> invalid_serializer.errors
ReturnDict([('coordinates',
             {'x': ['A valid integer is required.'],
              'y': ['A valid integer is required.']})])
```

For this reason, the nested serializer approach would be the first to try. You
would use the custom field approach when the nested serializer becomes infeasible
or overly complex.

По этой причине подход вложенного сериализатора будет первым, кто попробовал.
Ты
Использует пользовательский полевой подход, когда вложенный сериализатор становится невозможным
или слишком сложный.

# Third party packages

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## DRF Compound Fields

## СООБЩЕНИЯ

The [drf-compound-fields](https://drf-compound-fields.readthedocs.io) package provides "compound" serializer fields, such as lists of simple values, which can be described by other fields rather than serializers with the `many=True` option. Also provided are fields for typed dictionaries and values that can be either a specific type or a list of items of that type.

Пакет [drf-compound-fields] (https://drf-compound-fields.readthedocs.io) предоставляет «составные» поля сериализатора, такие как списки простых значений, которые могут быть описаны другими полями, а не сериализаторами с
`mary = true` вариант.
Также приведены поля для напечатанных словарей и значений, которые могут быть либо определенным типом, либо списком элементов такого типа.

## DRF Extra Fields

## Дополнительные поля DRF

The [drf-extra-fields](https://github.com/Hipo/drf-extra-fields) package provides extra serializer fields for REST framework, including `Base64ImageField` and `PointField` classes.

Пакет [https://github.com/hipo/drf-extra-fields) (https://github.com/hipo/drf-extra-fields), включая классы `base64imagefield` и` pointfield`.

## djangorestframework-recursive

## djangorestframework-recursive

the [djangorestframework-recursive](https://github.com/heywbj/django-rest-framework-recursive) package provides a `RecursiveField` for serializing and deserializing recursive structures

[djangorestframework-recurive] (https://github.com/heywbj/django-rest-framework-recurisive) предоставляет «рекурсивное поле» для сериализации и детериализации рекурсивных структур

## django-rest-framework-gis

## django-rest-framework-gis

The [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) package provides geographic addons for django rest framework like a  `GeometryField` field and a GeoJSON serializer.

Пакет [django-rest-framework-gis] (https://github.com/djangonauts/django-rest-framework-gis) предоставляет географические дополнения для структуры REST Django, таких как сериализатор Geometryfield` и сериализатор Geojson.

## django-rest-framework-hstore

## django-rest-framework-hstore

The [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) package provides an `HStoreField` to support [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` model field.

В пакете [django-rest-framework-hstore] (https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `hstorefield` для поддержки [django-hstore] (https://github.com
/djangonauts/django-hstore) `Dictionaryfield's Model Field.