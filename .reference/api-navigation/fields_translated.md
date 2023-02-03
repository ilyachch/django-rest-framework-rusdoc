<!-- TRANSLATED by md-translate -->
---

source:

источник:

* fields.py

* fields.py

---

# Serializer fields

# Поля сериализатора

> Each field in a Form class is responsible not only for validating data, but also for "cleaning" it — normalizing it to a consistent format.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data)

> Каждое поле в классе Form отвечает не только за проверку данных, но и за их "очистку" - нормализацию до согласованного формата.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data)

Serializer fields handle converting between primitive values and internal datatypes. They also deal with validating input values, as well as retrieving and setting the values from their parent objects.

Поля сериализатора обрабатывают преобразование между примитивными значениями и внутренними типами данных. Они также занимаются проверкой входных значений, а также получением и установкой значений из своих родительских объектов.

---

**Note:** The serializer fields are declared in `fields.py`, but by convention you should import them using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.

**Примечание:** Поля сериализатора объявляются в `fields.py`, но по соглашению вы должны импортировать их с помощью `from rest_framework import serializers` и ссылаться на поля как `serializers.<FieldName>`.

---

## Core arguments

## Основные аргументы

Each serializer field class constructor takes at least these arguments. Some Field classes take additional, field-specific arguments, but the following should always be accepted:

Каждый конструктор класса поля сериализатора принимает как минимум эти аргументы. Некоторые классы Field принимают дополнительные, специфические для поля аргументы, но следующие должны приниматься всегда:

### `read_only`

### `read_only`

Read-only fields are included in the API output, but should not be included in the input during create or update operations. Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.

Поля, доступные только для чтения, включаются в вывод API, но не должны включаться в ввод при операциях создания или обновления. Любые поля "только для чтения", которые неправильно включены во входные данные сериализатора, будут проигнорированы.

Set this to `True` to ensure that the field is used when serializing a representation, but is not used when creating or updating an instance during deserialization.

Установите значение `True`, чтобы гарантировать, что поле используется при сериализации представления, но не используется при создании или обновлении экземпляра во время десериализации.

Defaults to `False`

По умолчанию `False`.

### `write_only`

### `write_only`

Set this to `True` to ensure that the field may be used when updating or creating an instance, but is not included when serializing the representation.

Установите значение `True`, чтобы гарантировать, что поле может использоваться при обновлении или создании экземпляра, но не будет включено при сериализации представления.

Defaults to `False`

По умолчанию `False`.

### `required`

### `обязательно`

Normally an error will be raised if a field is not supplied during deserialization. Set to false if this field is not required to be present during deserialization.

Обычно ошибка возникает, если поле не предоставлено во время десериализации. Установите значение false, если это поле не должно присутствовать при десериализации.

Setting this to `False` also allows the object attribute or dictionary key to be omitted from output when serializing the instance. If the key is not present it will simply not be included in the output representation.

Установка этого значения в `False` также позволяет не выводить атрибут объекта или ключ словаря при сериализации экземпляра. Если ключ не присутствует, он просто не будет включен в выходное представление.

Defaults to `True`. If you're using [Model Serializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) default value will be `False` if you have specified `blank=True` or `default` or `null=True` at your field in your `Model`.

По умолчанию имеет значение `True`. Если вы используете [Model Serializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) значение по умолчанию будет `False`, если вы указали `blank=True` или `default` или `null=True` для вашего поля в вашей `Model`.

### `default`

### `default`

If set, this gives the default value that will be used for the field if no input value is supplied. If not set the default behavior is to not populate the attribute at all.

Если установлено, это значение дает значение по умолчанию, которое будет использоваться для поля, если входное значение не предоставлено. Если значение не задано, то по умолчанию атрибут вообще не заполняется.

The `default` is not applied during partial update operations. In the partial update case only fields that are provided in the incoming data will have a validated value returned.

Значение `default` не применяется во время операций частичного обновления. В случае частичного обновления только полям, указанным во входящих данных, будет возвращено подтвержденное значение.

May be set to a function or other callable, in which case the value will be evaluated each time it is used. When called, it will receive no arguments. If the callable has a `requires_context = True` attribute, then the serializer field will be passed as an argument.

Может быть установлен в функцию или другую вызываемую функцию, в этом случае значение будет оцениваться каждый раз при его использовании. При вызове она не получает никаких аргументов. Если вызываемая функция имеет атрибут `requires_context = True`, то поле сериализатора будет передано в качестве аргумента.

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

При сериализации экземпляра будет использоваться значение по умолчанию, если атрибут объекта или ключ словаря не присутствует в экземпляре.

Note that setting a `default` value implies that the field is not required. Including both the `default` and `required` keyword arguments is invalid and will raise an error.

Обратите внимание, что установка значения `default` подразумевает, что поле не является обязательным. Включение обоих ключевых аргументов `default` и `required` является недопустимым и приведет к ошибке.

### `allow_null`

### `allow_null`

Normally an error will be raised if `None` is passed to a serializer field. Set this keyword argument to `True` if `None` should be considered a valid value.

Обычно возникает ошибка, если в поле сериализатора передается `None`. Установите этот аргумент ключевого слова в `True`, если `None` должно считаться допустимым значением.

Note that, without an explicit `default`, setting this argument to `True` will imply a `default` value of `null` for serialization output, but does not imply a default for input deserialization.

Обратите внимание, что без явного `default`, установка этого аргумента в `True` будет подразумевать `default` значение `null` для вывода сериализации, но не подразумевает значение по умолчанию для десериализации ввода.

Defaults to `False`

По умолчанию `False`.

### `source`

### `source`

The name of the attribute that will be used to populate the field. May be a method that only takes a `self` argument, such as `URLField(source='get_absolute_url')`, or may use dotted notation to traverse attributes, such as `EmailField(source='user.email')`.

Имя атрибута, который будет использоваться для заполнения поля. Может быть методом, принимающим только аргумент `self`, например, `URLField(source='get_absolute_url')`, или может использовать точечную нотацию для обхода атрибутов, например, `EmailField(source='user.email')`.

When serializing fields with dotted notation, it may be necessary to provide a `default` value if any object is not present or is empty during attribute traversal. Beware of possible n+1 problems when using source attribute if you are accessing a relational orm model. For example:

При сериализации полей с точечной нотацией может возникнуть необходимость предоставить значение `default`, если какой-либо объект отсутствует или пуст при обходе атрибутов. Остерегайтесь возможных проблем n+1 при использовании атрибута source, если вы обращаетесь к реляционной модели orm. Например:

```
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField(source="user.email")
```

This case would require user object to be fetched from database when it is not prefetched. If that is not wanted, be sure to be using `prefetch_related` and `select_related` methods appropriately. For more information about the methods refer to [django documentation](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

В этом случае потребуется извлечь объект пользователя из базы данных, если он не был предварительно извлечен. Если это нежелательно, убедитесь, что вы используете методы `prefetch_related` и `select_related` соответствующим образом. Более подробную информацию об этих методах можно найти в [документации django](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

The value `source='*'` has a special meaning, and is used to indicate that the entire object should be passed through to the field. This can be useful for creating nested representations, or for fields which require access to the complete object in order to determine the output representation.

Значение `source='*'` имеет специальное значение и используется для указания того, что в поле должен быть передан весь объект. Это может быть полезно при создании вложенных представлений или для полей, которым требуется доступ к полному объекту для определения выходного представления.

Defaults to the name of the field.

По умолчанию используется имя поля.

### `validators`

### `валидаторы`

A list of validator functions which should be applied to the incoming field input, and which either raise a validation error or simply return. Validator functions should typically raise `serializers.ValidationError`, but Django's built-in `ValidationError` is also supported for compatibility with validators defined in the Django codebase or third party Django packages.

Список функций валидатора, которые должны быть применены к вводимому полю и которые либо выдают ошибку валидации, либо просто возвращаются. Функции валидатора обычно должны вызывать `serializers.ValidationError`, но встроенный в Django `ValidationError` также поддерживается для совместимости с валидаторами, определенными в кодовой базе Django или в сторонних пакетах Django.

### `error_messages`

### `error_messages`

A dictionary of error codes to error messages.

Словарь кодов ошибок к сообщениям об ошибках.

### `label`

### `label`

A short text string that may be used as the name of the field in HTML form fields or other descriptive elements.

Короткая текстовая строка, которая может использоваться в качестве имени поля в полях формы HTML или других описательных элементах.

### `help_text`

### `help_text`

A text string that may be used as a description of the field in HTML form fields or other descriptive elements.

Текстовая строка, которая может быть использована в качестве описания поля в полях формы HTML или других описательных элементах.

### `initial`

### `initial`

A value that should be used for pre-populating the value of HTML form fields. You may pass a callable to it, just as you may do with any regular Django `Field`:

Значение, которое должно использоваться для предварительного заполнения значений полей HTML-формы. Вы можете передать ему вызываемый объект, как и в случае с любым обычным Django `Field`:

```
import datetime
from rest_framework import serializers
class ExampleSerializer(serializers.Serializer):
    day = serializers.DateField(initial=datetime.date.today)
```

### `style`

### `style`

A dictionary of key-value pairs that can be used to control how renderers should render the field.

Словарь пар ключ-значение, которые могут быть использованы для управления тем, как рендеринг должен отображать поле.

Two examples here are `'input_type'` and `'base_template'`:

Двумя примерами здесь являются `'input_type'` и `'base_template'`:

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

Более подробную информацию можно найти в документации [HTML & Forms](../topics/html-and-forms.md).

---

# Boolean fields

# Булевы поля

## BooleanField

## BooleanField

A boolean representation.

Булево представление.

When using HTML encoded form input be aware that omitting a value will always be treated as setting a field to `False`, even if it has a `default=True` option specified. This is because HTML checkbox inputs represent the unchecked state by omitting the value, so REST framework treats omission as if it is an empty checkbox input.

При использовании HTML-кодированных форм ввода следует помнить, что отсутствие значения всегда будет рассматриваться как установка поля в `False`, даже если для него указана опция `default=True`. Это связано с тем, что входы с флажками HTML представляют состояние без флажка, когда значение отсутствует, поэтому REST framework рассматривает отсутствие значения как пустой вход с флажком.

Note that Django 2.1 removed the `blank` kwarg from `models.BooleanField`. Prior to Django 2.1 `models.BooleanField` fields were always `blank=True`. Thus since Django 2.1 default `serializers.BooleanField` instances will be generated without the `required` kwarg (i.e. equivalent to `required=True`) whereas with previous versions of Django, default `BooleanField` instances will be generated with a `required=False` option. If you want to control this behavior manually, explicitly declare the `BooleanField` on the serializer class, or use the `extra_kwargs` option to set the `required` flag.

Обратите внимание, что в Django 2.1 из `models.BooleanField` был удален карг `blank`. До Django 2.1 поля `models.BooleanField` всегда были `blank=True`. Таким образом, начиная с Django 2.1 экземпляры `serializers.BooleanField` по умолчанию будут генерироваться без kwarg `required` (т.е. эквивалентно `required=True`), тогда как в предыдущих версиях Django экземпляры `BooleanField` по умолчанию будут генерироваться с опцией `required=False`. Если вы хотите управлять этим поведением вручную, явно объявите `BooleanField` в классе сериализатора или используйте опцию `extra_kwargs` для установки флага `required`.

Corresponds to `django.db.models.fields.BooleanField`.

Соответствует `django.db.models.fields.BooleanField`.

**Signature:** `BooleanField()`

**Подпись:** `BooleanField()`.

---

# String fields

# Строковые поля

## CharField

## CharField

A text representation. Optionally validates the text to be shorter than `max_length` and longer than `min_length`.

Текстовое представление. Опционально проверяет, чтобы текст был короче `max_length` и длиннее `min_length`.

Corresponds to `django.db.models.fields.CharField` or `django.db.models.fields.TextField`.

Соответствует `django.db.models.fields.CharField` или `django.db.models.fields.TextField`.

**Signature:** `CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`

**Подпись:** `CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`.

* `max_length` - Validates that the input contains no more than this number of characters.
* `min_length` - Validates that the input contains no fewer than this number of characters.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `trim_whitespace` - If set to `True` then leading and trailing whitespace is trimmed. Defaults to `True`.

* `max_length` - Проверяет, что входные данные содержат не более указанного количества символов.
* `min_length` - Проверяет, что вводимые данные содержат не менее этого количества символов.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недействительной и вызовет ошибку проверки. По умолчанию `False`.
* `trim_whitespace` - Если установлено значение `True`, то ведущие и последующие пробельные символы будут обрезаны. По умолчанию `True`.

The `allow_null` option is also available for string fields, although its usage is discouraged in favor of `allow_blank`. It is valid to set both `allow_blank=True` and `allow_null=True`, but doing so means that there will be two differing types of empty value permissible for string representations, which can lead to data inconsistencies and subtle application bugs.

Опция `allow_null` также доступна для строковых полей, хотя ее использование не рекомендуется в пользу `allow_blank`. Можно установить и `allow_blank=True`, и `allow_null=True`, но это означает, что для строковых представлений будут допустимы два разных типа пустого значения, что может привести к несоответствию данных и тонким ошибкам в работе приложения.

## EmailField

## EmailField

A text representation, validates the text to be a valid e-mail address.

Текстовое представление, проверяет, является ли текст действительным адресом электронной почты.

Corresponds to `django.db.models.fields.EmailField`

Соответствует `django.db.models.fields.EmailField`.

**Signature:** `EmailField(max_length=None, min_length=None, allow_blank=False)`

**Подпись:** `EmailField(max_length=None, min_length=None, allow_blank=False)`.

## RegexField

## RegexField

A text representation, that validates the given value matches against a certain regular expression.

Текстовое представление, которое проверяет соответствие заданного значения определенному регулярному выражению.

Corresponds to `django.forms.fields.RegexField`.

Соответствует `django.forms.fields.RegexField`.

**Signature:** `RegexField(regex, max_length=None, min_length=None, allow_blank=False)`

**Подпись:** `RegexField(regex, max_length=None, min_length=None, allow_blank=False)`.

The mandatory `regex` argument may either be a string, or a compiled python regular expression object.

Обязательный аргумент `regex` может быть либо строкой, либо скомпилированным объектом регулярного выражения python.

Uses Django's `django.core.validators.RegexValidator` for validation.

Использует `django.core.validators.RegexValidator` для валидации.

## SlugField

## SlugField

A `RegexField` that validates the input against the pattern `[a-zA-Z0-9_-]+`.

Поле `RegexField`, которое проверяет вводимые данные на соответствие шаблону `[a-zA-Z0-9_-]+`.

Corresponds to `django.db.models.fields.SlugField`.

Соответствует `django.db.models.fields.SlugField`.

**Signature:** `SlugField(max_length=50, min_length=None, allow_blank=False)`

**Подпись:** `SlugField(max_length=50, min_length=None, allow_blank=False)`.

## URLField

## URLField

A `RegexField` that validates the input against a URL matching pattern. Expects fully qualified URLs of the form `http://<host>/<path>`.

Поле `RegexField`, которое проверяет вводимые данные на соответствие шаблону URL. Ожидаются полностью определенные URL вида `http://<host>/<path>`.

Corresponds to `django.db.models.fields.URLField`. Uses Django's `django.core.validators.URLValidator` for validation.

Соответствует `django.db.models.fields.URLField`. Для валидации использует `django.core.validators.URLValidator`.

**Signature:** `URLField(max_length=200, min_length=None, allow_blank=False)`

**Подпись:** `URLField(max_length=200, min_length=None, allow_blank=False)`.

## UUIDField

## UUIDField

A field that ensures the input is a valid UUID string. The `to_internal_value` method will return a `uuid.UUID` instance. On output the field will return a string in the canonical hyphenated format, for example:

Поле, которое гарантирует, что вводимые данные являются действительной строкой UUID. Метод `to_internal_value` возвращает экземпляр `uuid.UUID`. На выходе поле вернет строку в каноническом дефисном формате, например:

```
"de305d54-75b4-431b-adb2-eb6b9e546013"
```

**Signature:** `UUIDField(format='hex_verbose')`

**Подпись:** `UUIDField(format='hex_verbose')`.

* `format`: Determines the representation format of the uuid value
    - `'hex_verbose'` - The canonical hex representation, including hyphens: `"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`
    - `'hex'` - The compact hex representation of the UUID, not including hyphens: `"5ce0e9a55ffa654bcee01238041fb31a"`
    - `'int'` - A 128 bit integer representation of the UUID: `"123456789012312313134124512351145145114"`
    - `'urn'` - RFC 4122 URN representation of the UUID: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` Changing the `format` parameters only affects representation values. All formats are accepted by `to_internal_value`

* ``формат``: Определяет формат представления значения uuid
- `'hex_verbose'` - Каноническое шестнадцатеричное представление, включая дефисы: ``5ce0e9a5-5ffa-654b-cee0-1238041fb31a``.
- `'hex'` - Компактное шестнадцатеричное представление UUID, не включая дефисы: `'5ce0e9a55ffa654bcee01238041fb31a``.
- `'int'` - 128-битное целочисленное представление UUID: ``123456789012312313134124512351145145114``.
- `'urn'` - RFC 4122 URN представление UUID: `'urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` Изменение параметров `формата` влияет только на значения представления. Все форматы принимаются функцией `to_internal_value`.

## FilePathField

## FilePathField

A field whose choices are limited to the filenames in a certain directory on the filesystem

Поле, выбор которого ограничен именами файлов в определенном каталоге в файловой системе

Corresponds to `django.forms.fields.FilePathField`.

Соответствует `django.forms.fields.FilePathField`.

**Signature:** `FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`

**Значение:** `FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`.

* `path` - The absolute filesystem path to a directory from which this FilePathField should get its choice.
* `match` - A regular expression, as a string, that FilePathField will use to filter filenames.
* `recursive` - Specifies whether all subdirectories of path should be included. Default is `False`.
* `allow_files` - Specifies whether files in the specified location should be included. Default is `True`. Either this or `allow_folders` must be `True`.
* `allow_folders` - Specifies whether folders in the specified location should be included. Default is `False`. Either this or `allow_files` must be `True`.

* ``path`` - абсолютный путь файловой системы к каталогу, из которого это поле FilePathField должно получить свой выбор.
* `match` - Регулярное выражение в виде строки, которое FilePathField будет использовать для фильтрации имен файлов.
* `recursive` - Указывает, должны ли включаться все подкаталоги пути. По умолчанию `False`.
* `allow_files` - Указывает, должны ли включаться файлы в указанном месте. По умолчанию `True`. Либо это, либо `allow_folders` должно быть `True`.
* `allow_folders` - Указывает, следует ли включать папки в указанном месте. По умолчанию `False`. Либо это, либо `allow_files` должно быть `True`.

## IPAddressField

## IPAddressField

A field that ensures the input is a valid IPv4 or IPv6 string.

Поле, которое гарантирует, что вводимые данные являются действительной строкой IPv4 или IPv6.

Corresponds to `django.forms.fields.IPAddressField` and `django.forms.fields.GenericIPAddressField`.

Соответствует `django.forms.fields.IPAddressField` и `django.forms.fields.GenericIPAddressField`.

**Signature**: `IPAddressField(protocol='both', unpack_ipv4=False, **options)`

**Подпись**: `IPAddressField(protocol='both', unpack_ipv4=False, **options)`.

* `protocol` Limits valid inputs to the specified protocol. Accepted values are 'both' (default), 'IPv4' or 'IPv6'. Matching is case insensitive.
* `unpack_ipv4` Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option is enabled that address would be unpacked to 192.0.2.1. Default is disabled. Can only be used when protocol is set to 'both'.

* `protocol` Ограничивает допустимые входы указанным протоколом. Принимаемые значения: 'both' (по умолчанию), 'IPv4' или 'IPv6'. Соответствие нечувствительно к регистру.
* `unpack_ipv4` Распаковывает сопоставленные с IPv4 адреса, например ::ffff:192.0.2.1. Если эта опция включена, то адрес будет распакован в 192.0.2.1. По умолчанию отключена. Может использоваться, только когда протокол установлен в 'both'.

---

# Numeric fields

# Числовые поля

## IntegerField

## IntegerField

An integer representation.

Целочисленное представление.

Corresponds to `django.db.models.fields.IntegerField`, `django.db.models.fields.SmallIntegerField`, `django.db.models.fields.PositiveIntegerField` and `django.db.models.fields.PositiveSmallIntegerField`.

Соответствует `django.db.models.fields.IntegerField`, `django.db.models.fields.SmallIntegerField`, `django.db.models.fields.PositiveIntegerField` и `django.db.models.fields.PositiveSmallIntegerField`.

**Signature**: `IntegerField(max_value=None, min_value=None)`

**Подпись**: `IntegerField(max_value=None, min_value=None)`.

* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.

* `max_value` Проверьте, что предоставленное число не больше этого значения.
* `min_value` Убедитесь, что предоставленное число не меньше этого значения.

## FloatField

## FloatField

A floating point representation.

Представление с плавающей запятой.

Corresponds to `django.db.models.fields.FloatField`.

Соответствует `django.db.models.fields.FloatField`.

**Signature**: `FloatField(max_value=None, min_value=None)`

**Подпись**: `FloatField(max_value=None, min_value=None)`.

* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.

* `max_value` Проверьте, что предоставленное число не больше этого значения.
* `min_value` Убедитесь, что предоставленное число не меньше этого значения.

## DecimalField

## DecimalField

A decimal representation, represented in Python by a `Decimal` instance.

Десятичное представление, представленное в Python экземпляром `Decimal`.

Corresponds to `django.db.models.fields.DecimalField`.

Соответствует `django.db.models.fields.DecimalField`.

**Signature**: `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`

**Подпись**: `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`.

* `max_digits` The maximum number of digits allowed in the number. It must be either `None` or an integer greater than or equal to `decimal_places`.
* `decimal_places` The number of decimal places to store with the number.
* `coerce_to_string` Set to `True` if string values should be returned for the representation, or `False` if `Decimal` objects should be returned. Defaults to the same value as the `COERCE_DECIMAL_TO_STRING` settings key, which will be `True` unless overridden. If `Decimal` objects are returned by the serializer, then the final output format will be determined by the renderer. Note that setting `localize` will force the value to `True`.
* `max_value` Validate that the number provided is no greater than this value.
* `min_value` Validate that the number provided is no less than this value.
* `localize` Set to `True` to enable localization of input and output based on the current locale. This will also force `coerce_to_string` to `True`. Defaults to `False`. Note that data formatting is enabled if you have set `USE_L10N=True` in your settings file.
* `rounding` Sets the rounding mode used when quantising to the configured precision. Valid values are [`decimal` module rounding modes](https://docs.python.org/3/library/decimal.html#rounding-modes). Defaults to `None`.
* `normalize_output` Will normalize the decimal value when serialized. This will strip all trailing zeroes and change the value's precision to the minimum required precision to be able to represent the value without loosing data. Defaults to `False`.

* `max_digits` Максимальное количество цифр, допустимое в номере. [...]
[...]
[...]  [...]  [...]  [...]
[...]
[...]
[...]  [...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]

#### Example usage

#### Пример использования

To validate numbers up to 999 with a resolution of 2 decimal places, you would use:

Для проверки чисел до 999 с разрешением 2 знака после запятой можно использовать:

```
serializers.DecimalField(max_digits=5, decimal_places=2)
```

And to validate numbers up to anything less than one billion with a resolution of 10 decimal places:

И проверять числа вплоть до любого менее одного миллиарда с разрешением 10 знаков после запятой:

```
serializers.DecimalField(max_digits=19, decimal_places=10)
```

---

# Date and time fields

# Поля даты и времени

## DateTimeField

## DateTimeField

A date and time representation.

Представление даты и времени.

Corresponds to `django.db.models.fields.DateTimeField`.

Соответствует `django.db.models.fields.DateTimeField`.

**Signature:** `DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)`

**Подпись:** `DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)`.

* `format` - A string representing the output format. If not specified, this defaults to the same value as the `DATETIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `datetime` objects should be returned by `to_representation`. In this case the datetime encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date. If not specified, the `DATETIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.
* `default_timezone` - A `tzinfo` subclass (`zoneinfo` or `pytz`) prepresenting the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone). If `USE_TZ` is disabled, then datetime objects will be naive.

* ``формат`` - строка, представляющая формат вывода. Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `DATETETIME_FORMAT`, который будет `'iso-8601'`, если он не задан. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `datetime` должны быть возвращены `to_representation`. В этом случае кодировка времени будет определяться рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут быть использованы для разбора даты. Если он не указан, будет использована настройка `DATETIME_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.
* `default_timezone` - Подкласс `tzinfo` (`zoneinfo` или `pytz`), представляющий часовой пояс. Если не указан и включен параметр `USE_TZ`, то по умолчанию используется [текущий часовой пояс](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone). Если `USE_TZ` отключена, то объекты datetime будут наивными.

#### `DateTimeField` format strings.

#### Строки формата `DateTimeField`.

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style datetimes should be used. (eg `'2013-01-29T12:34:56.000000Z'`)

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать время даты в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (eg `'2013-01-29T12:34:56.000000Z'`)

When a value of `None` is used for the format `datetime` objects will be returned by `to_representation` and the final output representation will determined by the renderer class.

Когда для формата используется значение `None`, объекты `datetime` будут возвращены `to_representation`, а окончательное представление вывода будет определяться классом renderer.

#### `auto_now` and `auto_now_add` model fields.

#### `auto_now` и `auto_now_add` поля модели.

When using `ModelSerializer` or `HyperlinkedModelSerializer`, note that any model fields with `auto_now=True` or `auto_now_add=True` will use serializer fields that are `read_only=True` by default.

При использовании `ModelSerializer` или `HyperlinkedModelSerializer` обратите внимание, что любые поля модели с `auto_now=True` или `auto_now_add=True` будут использовать поля сериализатора, которые по умолчанию имеют значение `read_only=True`.

If you want to override this behavior, you'll need to declare the `DateTimeField` explicitly on the serializer. For example:

Если вы хотите переопределить это поведение, вам необходимо явно объявить `DateTimeField` в сериализаторе. Например:

```
class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField()

    class Meta:
        model = Comment
```

## DateField

## DateField

A date representation.

Представление даты.

Corresponds to `django.db.models.fields.DateField`

Соответствует `django.db.models.fields.DateField`.

**Signature:** `DateField(format=api_settings.DATE_FORMAT, input_formats=None)`

**Подпись:** `DateField(format=api_settings.DATE_FORMAT, input_formats=None)`.

* `format` - A string representing the output format. If not specified, this defaults to the same value as the `DATE_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `date` objects should be returned by `to_representation`. In this case the date encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date. If not specified, the `DATE_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.

* ``формат`` - строка, представляющая формат вывода. Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `DATE_FORMAT`, который будет `'iso-8601'`, если он не задан. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `date` должны быть возвращены `to_representation`. В этом случае кодировка даты будет определяться рендерером.
* `input_formats` - Список строк, представляющих входные форматы, которые могут быть использованы для разбора даты. Если он не указан, будет использована настройка `DATE_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.

#### `DateField` format strings

#### Строки формата `DateField`.

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style dates should be used. (eg `'2013-01-29'`)

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать даты в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (например, `'2013-01-29'`)

## TimeField

## TimeField

A time representation.

Представление времени.

Corresponds to `django.db.models.fields.TimeField`

Соответствует `django.db.models.fields.TimeField`.

**Signature:** `TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`

**Подпись:** `TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`.

* `format` - A string representing the output format. If not specified, this defaults to the same value as the `TIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `time` objects should be returned by `to_representation`. In this case the time encoding will be determined by the renderer.
* `input_formats` - A list of strings representing the input formats which may be used to parse the date. If not specified, the `TIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.

* ``формат`` - строка, представляющая формат вывода. Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `TIME_FORMAT`, который будет `'iso-8601'`, если он не установлен. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `time` должны быть возвращены `to_representation`. В этом случае кодировка времени будет определяться рендерером.
* `input_formats` - Список строк, представляющих входные форматы, которые могут быть использованы для разбора даты. Если он не указан, будет использована настройка `TIME_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.

#### `TimeField` format strings

#### Строки формата `TimeField`.

Format strings may either be [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601](https://www.w3.org/TR/NOTE-datetime) style times should be used. (eg `'12:34:56.000000'`)

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать время в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (например, `'12:34:56.000000'`)

## DurationField

## DurationField

A Duration representation. Corresponds to `django.db.models.fields.DurationField`

Представление Duration. Соответствует `django.db.models.fields.DurationField`.

The `validated_data` for these fields will contain a `datetime.timedelta` instance. The representation is a string following this format `'[DD] [HH:[MM:]]ss[.uuuuuu]'`.

В `validated_data` для этих полей будет содержаться экземпляр `datetime.timedelta`. Он представляет собой строку, следующую формату `'[DD] [HH:[MM:]]ss[.uuuuuuuu]'`.

**Signature:** `DurationField(max_value=None, min_value=None)`

**Подпись:** `DurationField(max_value=None, min_value=None)`.

* `max_value` Validate that the duration provided is no greater than this value.
* `min_value` Validate that the duration provided is no less than this value.

* `max_value` Убедитесь, что предоставленная продолжительность не превышает этого значения.
* `min_value` Убедитесь, что предоставленная продолжительность не меньше этого значения.

---

# Choice selection fields

# Поля выбора

## ChoiceField

## ChoiceField

A field that can accept a value out of a limited set of choices.

Поле, которое может принимать значение из ограниченного набора вариантов.

Used by `ModelSerializer` to automatically generate fields if the corresponding model field includes a `choices=…` argument.

Используется `ModelSerializer` для автоматической генерации полей, если соответствующее поле модели включает аргумент `choices=...`.

**Signature:** `ChoiceField(choices)`

**Подпись:** `ChoiceField(choices)`.

* `choices` - A list of valid values, or a list of `(key, display_name)` tuples.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Can be used to ensure that automatically generated ChoiceFields with very large possible selections do not prevent a template from rendering. Defaults to `None`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `choices` - список допустимых значений, или список кортежей `(key, display_name)`.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недопустимой и вызовет ошибку валидации. По умолчанию `False`.
* `html_cutoff` - Если установлено, то это максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Может использоваться для того, чтобы автоматически генерируемые поля выбора с очень большим количеством возможных вариантов выбора не препятствовали отрисовке шаблона. По умолчанию `None`.
* `html_cutoff_text` - Если установлено, то будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию ``Больше чем {count} элементов...``.

Both the `allow_blank` and `allow_null` are valid options on `ChoiceField`, although it is highly recommended that you only use one and not both. `allow_blank` should be preferred for textual choices, and `allow_null` should be preferred for numeric or other non-textual choices.

Оба параметра `allow_blank` и `allow_null` являются допустимыми для `ChoiceField`, хотя настоятельно рекомендуется использовать только один из них, а не оба. `allow_blank` следует предпочесть для текстовых вариантов, а `allow_null` - для числовых или других нетекстовых вариантов.

## MultipleChoiceField

## MultipleChoiceField

A field that can accept a set of zero, one or many values, chosen from a limited set of choices. Takes a single mandatory argument. `to_internal_value` returns a `set` containing the selected values.

Поле, которое может принимать набор из нуля, одного или многих значений, выбранных из ограниченного набора вариантов. Принимает один обязательный аргумент. `to_internal_value` возвращает `set`, содержащий выбранные значения.

**Signature:** `MultipleChoiceField(choices)`

**Подпись:** `MultipleChoiceField(choices)`.

* `choices` - A list of valid values, or a list of `(key, display_name)` tuples.
* `allow_blank` - If set to `True` then the empty string should be considered a valid value. If set to `False` then the empty string is considered invalid and will raise a validation error. Defaults to `False`.
* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Can be used to ensure that automatically generated ChoiceFields with very large possible selections do not prevent a template from rendering. Defaults to `None`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `choices` - список допустимых значений, или список кортежей `(key, display_name)`.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недопустимой и вызовет ошибку валидации. По умолчанию `False`.
* `html_cutoff` - Если установлено, то это максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Может использоваться для того, чтобы автоматически генерируемые поля выбора с очень большим количеством возможных вариантов выбора не препятствовали отрисовке шаблона. По умолчанию `None`.
* `html_cutoff_text` - Если установлено, то будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию ``Больше чем {count} элементов...``.

As with `ChoiceField`, both the `allow_blank` and `allow_null` options are valid, although it is highly recommended that you only use one and not both. `allow_blank` should be preferred for textual choices, and `allow_null` should be preferred for numeric or other non-textual choices.

Как и в случае с `ChoiceField`, оба параметра `allow_blank` и `allow_null` являются допустимыми, хотя настоятельно рекомендуется использовать только один из них, а не оба. `allow_blank` следует предпочесть для текстовых вариантов, а `allow_null` - для числовых или других нетекстовых вариантов.

---

# File upload fields

# Поля для загрузки файлов

#### Parsers and file uploads.

#### Парсеры и загрузка файлов.

The `FileField` and `ImageField` classes are only suitable for use with `MultiPartParser` or `FileUploadParser`. Most parsers, such as e.g. JSON don't support file uploads. Django's regular [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS) are used for handling uploaded files.

Классы `FileField` и `ImageField` подходят только для использования с `MultiPartParser` или `FileUploadParser`. Большинство парсеров, таких как, например, JSON, не поддерживают загрузку файлов. Для обработки загруженных файлов используются штатные [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS) Django.

## FileField

## FileField

A file representation. Performs Django's standard FileField validation.

Представление файла. Выполняет стандартную для Django валидацию FileField.

Corresponds to `django.forms.fields.FileField`.

Соответствует `django.forms.fields.FileField`.

**Signature:** `FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

**Подпись:** `FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`.

* `max_length` - Designates the maximum length for the file name.
* `allow_empty_file` - Designates if empty files are allowed.
* `use_url` - If set to `True` then URL string values will be used for the output representation. If set to `False` then filename string values will be used for the output representation. Defaults to the value of the `UPLOADED_FILES_USE_URL` settings key, which is `True` unless set otherwise.

* `max_length` - Указывает максимальную длину имени файла.
* `allow_empty_file` - Указывает, разрешены ли пустые файлы.
* `use_url` - Если установлено значение `True`, то для выходного представления будут использоваться строковые значения URL. Если установлено значение `False`, то для вывода будут использоваться строковые значения имени файла. По умолчанию используется значение ключа настроек `UPLOADED_FILES_USE_URL`, которое равно `True`, если не установлено иное.

## ImageField

## ImageField

An image representation. Validates the uploaded file content as matching a known image format.

Представление изображения. Проверяет соответствие содержимого загруженного файла известному формату изображения.

Corresponds to `django.forms.fields.ImageField`.

Соответствует `django.forms.fields.ImageField`.

**Signature:** `ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

**Подпись:** `ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`.

* `max_length` - Designates the maximum length for the file name.
* `allow_empty_file` - Designates if empty files are allowed.
* `use_url` - If set to `True` then URL string values will be used for the output representation. If set to `False` then filename string values will be used for the output representation. Defaults to the value of the `UPLOADED_FILES_USE_URL` settings key, which is `True` unless set otherwise.

* `max_length` - Указывает максимальную длину имени файла.
* `allow_empty_file` - Указывает, разрешены ли пустые файлы.
* `use_url` - Если установлено значение `True`, то для представления выходных данных будут использоваться строковые значения URL. Если установлено значение `False`, то для вывода будут использоваться строковые значения имени файла. По умолчанию используется значение ключа настроек `UPLOADED_FILES_USE_URL`, которое равно `True`, если не установлено иное.

Requires either the `Pillow` package or `PIL` package. The `Pillow` package is recommended, as `PIL` is no longer actively maintained.

Требуется либо пакет `Pillow`, либо пакет `PIL`. Рекомендуется использовать пакет `Pillow`, поскольку пакет `PIL` больше не поддерживается.

---

# Composite fields

# Составные поля

## ListField

## ListField

A field class that validates a list of objects.

Класс поля, который проверяет список объектов.

**Signature**: `ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)`

**Подпись**: `ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)`.

* `child` - A field instance that should be used for validating the objects in the list. If this argument is not provided then objects in the list will not be validated.
* `allow_empty` - Designates if empty lists are allowed.
* `min_length` - Validates that the list contains no fewer than this number of elements.
* `max_length` - Validates that the list contains no more than this number of elements.

* `child` - экземпляр поля, которое должно использоваться для проверки объектов в списке. Если этот аргумент не указан, то объекты в списке не будут проверяться.
* `allow_empty` - Указывает, разрешены ли пустые списки.
* `min_length` - Проверяет, что список содержит не менее данного количества элементов.
* `max_length` - Проверяет, что список содержит не более этого количества элементов.

For example, to validate a list of integers you might use something like the following:

Например, для проверки списка целых чисел вы можете использовать что-то вроде следующего:

```
scores = serializers.ListField(
   child=serializers.IntegerField(min_value=0, max_value=100)
)
```

The `ListField` class also supports a declarative style that allows you to write reusable list field classes.

Класс `ListField` также поддерживает декларативный стиль, который позволяет вам писать многократно используемые классы полей списков.

```
class StringListField(serializers.ListField):
    child = serializers.CharField()
```

We can now reuse our custom `StringListField` class throughout our application, without having to provide a `child` argument to it.

Теперь мы можем повторно использовать наш пользовательский класс `StringListField` во всем нашем приложении, без необходимости предоставлять ему аргумент `child`.

## DictField

## DictField

A field class that validates a dictionary of objects. The keys in `DictField` are always assumed to be string values.

Класс поля, который проверяет словарь объектов. Предполагается, что ключи в `DictField` всегда являются строковыми значениями.

**Signature**: `DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

**Подпись**: `DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)`.

* `child` - A field instance that should be used for validating the values in the dictionary. If this argument is not provided then values in the mapping will not be validated.
* `allow_empty` - Designates if empty dictionaries are allowed.

* `child` - экземпляр поля, который должен использоваться для проверки значений в словаре. Если этот аргумент не указан, то значения в связке не будут проверяться.
* `allow_empty` - Указывает, разрешены ли пустые словари.

For example, to create a field that validates a mapping of strings to strings, you would write something like this:

Например, чтобы создать поле, которое проверяет соответствие строк строкам, вы должны написать что-то вроде этого:

```
document = DictField(child=CharField())
```

You can also use the declarative style, as with `ListField`. For example:

Вы также можете использовать декларативный стиль, как в `ListField`. Например:

```
class DocumentField(DictField):
    child = CharField()
```

## HStoreField

## HStoreField

A preconfigured `DictField` that is compatible with Django's postgres `HStoreField`.

Предварительно настроенное `DictField`, совместимое с `HStoreField` от Django для postgres.

**Signature**: `HStoreField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

**Подпись**: `HStoreField(child=<A_FIELD_INSTANCE>, allow_empty=True)`.

* `child` - A field instance that is used for validating the values in the dictionary. The default child field accepts both empty strings and null values.
* `allow_empty` - Designates if empty dictionaries are allowed.

* `child` - экземпляр поля, который используется для проверки значений в словаре. По умолчанию дочернее поле принимает как пустые строки, так и значения null.
* `allow_empty` - Указывает, разрешены ли пустые словари.

Note that the child field **must** be an instance of `CharField`, as the hstore extension stores values as strings.

Обратите внимание, что дочернее поле **должно** быть экземпляром `CharField`, поскольку расширение hstore хранит значения в виде строк.

## JSONField

## JSONField

A field class that validates that the incoming data structure consists of valid JSON primitives. In its alternate binary mode, it will represent and validate JSON-encoded binary strings.

Класс поля, который проверяет, что входящая структура данных состоит из допустимых примитивов JSON. В альтернативном бинарном режиме он представляет и проверяет бинарные строки, закодированные в JSON.

**Signature**: `JSONField(binary, encoder)`

**Подпись**: `JSONField(binary, encoder)`.

* `binary` - If set to `True` then the field will output and validate a JSON encoded string, rather than a primitive data structure. Defaults to `False`.
* `encoder` - Use this JSON encoder to serialize input object. Defaults to `None`.

* `binary` - Если установлено значение `True`, то поле будет выводить и проверять строку в кодировке JSON, а не примитивную структуру данных. По умолчанию установлено значение `False`.
* `encoder` - Используйте этот JSON-кодер для сериализации входного объекта. По умолчанию `None`.

---

# Miscellaneous fields

# Разные поля

## ReadOnlyField

## ReadOnlyField

A field class that simply returns the value of the field without modification.

Класс поля, который просто возвращает значение поля без модификации.

This field is used by default with `ModelSerializer` when including field names that relate to an attribute rather than a model field.

Это поле используется по умолчанию в `ModelSerializer` при включении имен полей, относящихся к атрибуту, а не к полю модели.

**Signature**: `ReadOnlyField()`

**Подпись**: `ReadOnlyField()`.

For example, if `has_expired` was a property on the `Account` model, then the following serializer would automatically generate it as a `ReadOnlyField`:

Например, если `has_expired` было свойством модели `Account`, то следующий сериализатор автоматически сгенерирует его как `ReadOnlyField`:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'has_expired']
```

## HiddenField

## HiddenField

A field class that does not take a value based on user input, but instead takes its value from a default value or callable.

Класс поля, которое не принимает значение на основе пользовательского ввода, а берет его из значения по умолчанию или вызываемого поля.

**Signature**: `HiddenField()`

**Подпись**: `HiddenField()`.

For example, to include a field that always provides the current time as part of the serializer validated data, you would use the following:

Например, чтобы включить поле, которое всегда предоставляет текущее время как часть проверяемых сериализатором данных, вы можете использовать следующее:

```
modified = serializers.HiddenField(default=timezone.now)
```

The `HiddenField` class is usually only needed if you have some validation that needs to run based on some pre-provided field values, but you do not want to expose all of those fields to the end user.

Класс `HiddenField` обычно нужен только в том случае, если у вас есть валидация, которая должна выполняться на основе некоторых предварительно предоставленных значений полей, но вы не хотите раскрывать все эти поля конечному пользователю.

For further examples on `HiddenField` see the [validators](validators.md) documentation.

Дополнительные примеры по `HiddenField` смотрите в документации [validators](validators.md).

## ModelField

## ModelField

A generic field that can be tied to any arbitrary model field. The `ModelField` class delegates the task of serialization/deserialization to its associated model field. This field can be used to create serializer fields for custom model fields, without having to create a new custom serializer field.

Общее поле, которое может быть привязано к любому произвольному полю модели. Класс `ModelField` делегирует задачу сериализации/десериализации связанному с ним полю модели. Это поле можно использовать для создания полей сериализатора для пользовательских полей модели, без необходимости создавать новое пользовательское поле сериализатора.

This field is used by `ModelSerializer` to correspond to custom model field classes.

Это поле используется `ModelSerializer` для соответствия классам полей пользовательской модели.

**Signature:** `ModelField(model_field=<Django ModelField instance>)`

**Подпись:** `ModelField(model_field=<Django ModelField instance>)`.

The `ModelField` class is generally intended for internal use, but can be used by your API if needed. In order to properly instantiate a `ModelField`, it must be passed a field that is attached to an instantiated model. For example: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`

Класс `ModelField` обычно предназначен для внутреннего использования, но при необходимости может быть использован вашим API. Для того чтобы правильно инстанцировать `ModelField`, ему должно быть передано поле, которое присоединено к инстанцированной модели. Например: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`.

## SerializerMethodField

## SerializerMethodField

This is a read-only field. It gets its value by calling a method on the serializer class it is attached to. It can be used to add any sort of data to the serialized representation of your object.

Это поле доступно только для чтения. Оно получает свое значение путем вызова метода класса сериализатора, к которому оно присоединено. Его можно использовать для добавления любых данных в сериализованное представление вашего объекта.

**Signature**: `SerializerMethodField(method_name=None)`

**Подпись**: `SerializerMethodField(method_name=None)`.

* `method_name` - The name of the method on the serializer to be called. If not included this defaults to `get_<field_name>`.

* `method_name` - Имя метода сериализатора, который будет вызван. Если он не включен, то по умолчанию используется `get_<имя_поля>`.

The serializer method referred to by the `method_name` argument should accept a single argument (in addition to `self`), which is the object being serialized. It should return whatever you want to be included in the serialized representation of the object. For example:

Метод сериализатора, на который ссылается аргумент `имя_метода`, должен принимать единственный аргумент (в дополнение к `self`), которым является сериализуемый объект. Он должен возвращать все, что вы хотите включить в сериализованное представление объекта. Например:

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

# Пользовательские поля

If you want to create a custom field, you'll need to subclass `Field` and then override either one or both of the `.to_representation()` and `.to_internal_value()` methods. These two methods are used to convert between the initial datatype, and a primitive, serializable datatype. Primitive datatypes will typically be any of a number, string, boolean, `date`/`time`/`datetime` or `None`. They may also be any list or dictionary like object that only contains other primitive objects. Other types might be supported, depending on the renderer that you are using.

Если вы хотите создать пользовательское поле, вам необходимо создать подкласс `Field` и переопределить один или оба метода `.to_representation()` и `.to_internal_value()`. Эти два метода используются для преобразования между исходным типом данных и примитивным, сериализуемым типом данных. Примитивными типами данных обычно являются число, строка, булево, `date`/`time`/`datetime` или `None`. Они также могут быть любым списком или словарем, который содержит только другие примитивные объекты. Могут поддерживаться и другие типы, в зависимости от используемого рендерера.

The `.to_representation()` method is called to convert the initial datatype into a primitive, serializable datatype.

Метод `.to_representation()` вызывается для преобразования исходного типа данных в примитивный, сериализуемый тип данных.

The `.to_internal_value()` method is called to restore a primitive datatype into its internal python representation. This method should raise a `serializers.ValidationError` if the data is invalid.

Метод `.to_internal_value()` вызывается для восстановления примитивного типа данных в его внутреннее представление в python. Этот метод должен вызывать `serializers.ValidationError, если данные недействительны.

## Examples

## Примеры

### A Basic Custom Field

### Базовое пользовательское поле

Let's look at an example of serializing a class that represents an RGB color value:

Рассмотрим пример сериализации класса, представляющего значение цвета RGB:

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

By default field values are treated as mapping to an attribute on the object. If you need to customize how the field value is accessed and set you need to override `.get_attribute()` and/or `.get_value()`.

По умолчанию значения полей рассматриваются как сопоставление с атрибутом объекта. Если вам нужно настроить способ получения и установки значения поля, вам нужно переопределить `.get_attribute()` и/или `.get_value()`.

As an example, let's create a field that can be used to represent the class name of the object being serialized:

В качестве примера создадим поле, которое можно использовать для представления имени класса сериализуемого объекта:

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

### Вызывая ошибки валидации

Our `ColorField` class above currently does not perform any data validation. To indicate invalid data, we should raise a `serializers.ValidationError`, like so:

Наш класс `ColorField`, приведенный выше, в настоящее время не выполняет никакой проверки данных. Чтобы указать на недопустимые данные, мы должны поднять `serializers.ValidationError`, как показано ниже:

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

Метод `.fail()` - это ярлык для вызова `ValidationError`, который принимает строку сообщения из словаря `error_messages`. Например:

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

Этот стиль делает сообщения об ошибках более чистыми и отделенными от кода, и его следует предпочесть.

### Using `source='*'`

### Использование `source='*'`

Here we'll take an example of a *flat* `DataPoint` model with `x_coordinate` and `y_coordinate` attributes.

Здесь мы рассмотрим пример *плоской* модели `DataPoint` с атрибутами `x_coordinate` и `y_coordinate`.

```
class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()
```

Using a custom field and `source='*'` we can provide a nested representation of the coordinate pair:

Используя пользовательское поле и `source='*'`, мы можем предоставить вложенное представление пары координат:

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

Note that this example doesn't handle validation. Partly for that reason, in a real project, the coordinate nesting might be better handled with a nested serializer using `source='*'`, with two `IntegerField` instances, each with their own `source` pointing to the relevant field.

Обратите внимание, что этот пример не обрабатывает валидацию. Отчасти по этой причине в реальном проекте вложенность координат может быть лучше обработана вложенным сериализатором с использованием `source='*'`, с двумя экземплярами `IntegerField`, каждый из которых имеет свой собственный `source`, указывающий на соответствующее поле.

The key points from the example, though, are:

Однако ключевыми моментами из примера являются:

* `to_representation` is passed the entire `DataPoint` object and must map from that to the desired output.
    ```
    >>> instance = DataPoint(label='Example', x_coordinate=1, y_coordinate=2)
      >>> out_serializer = DataPointSerializer(instance)
      >>> out_serializer.data
      ReturnDict([('label', 'Example'), ('coordinates', {'x': 1, 'y': 2})])
    ```
* Unless our field is to be read-only, `to_internal_value` must map back to a dict suitable for updating our target object. With `source='*'`, the return from `to_internal_value` will update the root validated data dictionary, rather than a single key.
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

* `to_representation` передается весь объект `DataPoint` и он должен отобразить его в желаемый вывод.
[...]
[...]
[...]
[...]
[...]
[...]
[...]  [...]
[...]
[...]
[...]      [...]  [...]
[...]      [...]  [...]
[...]          [...]  [...]
[...]          [...]  [...]
[...]      [...]
[...]  [...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]

For completeness lets do the same thing again but with the nested serializer approach suggested above:

Для полноты картины повторим то же самое, но с использованием вложенного сериализатора, предложенного выше:

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

Here the mapping between the target and source attribute pairs (`x` and `x_coordinate`, `y` and `y_coordinate`) is handled in the `IntegerField` declarations. It's our `NestedCoordinateSerializer` that takes `source='*'`.

Здесь отображение между парами атрибутов цели и источника (`x` и `x_coordinate`, `y` и `y_coordinate`) обрабатывается в объявлениях `IntegerField`. Это наш `NestedCoordinateSerializer`, который принимает `source='*'`.

Our new `DataPointSerializer` exhibits the same behavior as the custom field approach.

Наш новый `DataPointSerializer` демонстрирует такое же поведение, как и подход с использованием пользовательских полей.

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

Но мы также получаем встроенную валидацию бесплатно:

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

For this reason, the nested serializer approach would be the first to try. You would use the custom field approach when the nested serializer becomes infeasible or overly complex.

По этой причине в первую очередь следует попробовать вложенный сериализатор. Вы будете использовать подход пользовательских полей, когда вложенный сериализатор станет невыполнимым или слишком сложным.

# Third party packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF Compound Fields

## Составные поля DRF

The [drf-compound-fields](https://drf-compound-fields.readthedocs.io) package provides "compound" serializer fields, such as lists of simple values, which can be described by other fields rather than serializers with the `many=True` option. Also provided are fields for typed dictionaries and values that can be either a specific type or a list of items of that type.

Пакет [drf-compound-fields](https://drf-compound-fields.readthedocs.io) предоставляет "составные" поля сериализатора, такие как списки простых значений, которые могут быть описаны другими полями, а не сериализаторами с опцией `many=True`. Также предоставляются поля для типизированных словарей и значений, которые могут быть либо определенным типом, либо списком элементов этого типа.

## DRF Extra Fields

## Дополнительные поля DRF

The [drf-extra-fields](https://github.com/Hipo/drf-extra-fields) package provides extra serializer fields for REST framework, including `Base64ImageField` and `PointField` classes.

Пакет [drf-extra-fields](https://github.com/Hipo/drf-extra-fields) предоставляет дополнительные поля сериализатора для фреймворка REST, включая классы `Base64ImageField` и `PointField`.

## djangorestframework-recursive

## djangorestframework-recursive

the [djangorestframework-recursive](https://github.com/heywbj/django-rest-framework-recursive) package provides a `RecursiveField` for serializing and deserializing recursive structures

пакет [djangorestframework-recursive](https://github.com/heywbj/django-rest-framework-recursive) предоставляет `RecursiveField` для сериализации и десериализации рекурсивных структур

## django-rest-framework-gis

## django-rest-framework-gis

The [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) package provides geographic addons for django rest framework like a `GeometryField` field and a GeoJSON serializer.

Пакет [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) предоставляет географические дополнения для django rest framework, такие как поле `GeometryField` и сериализатор GeoJSON.

## django-rest-framework-hstore

## django-rest-framework-hstore

The [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) package provides an `HStoreField` to support [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` model field.

Пакет [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `HStoreField` для поддержки поля модели [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField`.