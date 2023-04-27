<!-- TRANSLATED by md-translate -->
# Поля сериализатора

> Каждое поле в классе Form отвечает не только за проверку данных, но и за их "очистку" &mdash; нормализацию до согласованного формата.
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data)

Поля сериализатора обрабатывают преобразование между примитивными значениями и внутренними типами данных.  Они также занимаются проверкой входных значений, а также получением и установкой значений из своих родительских объектов.

---

**Примечание:** Поля сериализатора объявляются в `fields.py`, но по соглашению вы должны импортировать их с помощью `from rest_framework import serializers` и ссылаться на поля как `serializers.<FieldName>`.

---

## Основные аргументы

Каждый конструктор класса поля сериализатора принимает как минимум эти аргументы.  Некоторые классы Field принимают дополнительные, специфические для данного поля аргументы, но следующие должны приниматься всегда:

### `read_only`

Поля, доступные только для чтения, включаются в вывод API, но не должны включаться во ввод при операциях создания или обновления. Любые поля "только для чтения", которые неправильно включены во входные данные сериализатора, будут проигнорированы.

Установите значение `True`, чтобы гарантировать, что поле используется при сериализации представления, но не используется при создании или обновлении экземпляра во время десериализации.

По умолчанию `False`.

### `write_only`

Установите значение `True` для того, чтобы поле могло использоваться при обновлении или создании экземпляра, но не включалось при сериализации представления.

По умолчанию `False`.

### `обязательно`

Обычно ошибка возникает, если поле не предоставлено во время десериализации.
Установите значение false, если это поле не должно присутствовать при десериализации.

Установка этого значения в `False` также позволяет не выводить атрибут объекта или ключ словаря при сериализации экземпляра. Если ключ не присутствует, он просто не будет включен в выходное представление.

По умолчанию имеет значение `True`. Если вы используете [Model Serializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) значение по умолчанию будет `False`, если вы указали `blank=True` или `default` или `null=True` для вашего поля в вашей `Model`.

### `default`

Если установлено, это значение дает значение по умолчанию, которое будет использоваться для поля, если входное значение не предоставлено. Если значение не задано, то по умолчанию атрибут вообще не заполняется.

Значение `default` не применяется во время операций частичного обновления. В случае частичного обновления только полям, указанным во входящих данных, будет возвращено подтвержденное значение.

Может быть установлен в функцию или другую вызываемую функцию, в этом случае значение будет оцениваться каждый раз при его использовании. При вызове оно не получает никаких аргументов. Если вызываемая функция имеет атрибут `requires_context = True`, то поле сериализатора будет передано в качестве аргумента.

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

При сериализации экземпляра будет использоваться значение по умолчанию, если атрибут объекта или ключ словаря не присутствует в экземпляре.

Обратите внимание, что установка значения `default` подразумевает, что поле не является обязательным. Включение обоих ключевых аргументов `default` и `required` является недопустимым и приведет к ошибке.

### `allow_null`

Обычно возникает ошибка, если в поле сериализатора передается `None`. Установите этот аргумент ключевого слова в `True`, если `None` должно считаться допустимым значением.

Обратите внимание, что без явного `default`, установка этого аргумента в `True` будет подразумевать `default` значение `null` для вывода сериализации, но не подразумевает значение по умолчанию для десериализации ввода.

По умолчанию `False`.

### `source`

Имя атрибута, который будет использоваться для заполнения поля.  Может быть методом, принимающим только аргумент `self`, например, `URLField(source='get_absolute_url')`, или может использовать точечную нотацию для обхода атрибутов, например, `EmailField(source='user.email')`.

При сериализации полей с точечной нотацией может возникнуть необходимость предоставить значение `default`, если какой-либо объект отсутствует или пуст при обходе атрибутов. Остерегайтесь возможных проблем n+1 при использовании атрибута source, если вы обращаетесь к реляционной модели orm. Например:

```
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField(source="user.email")
```

В этом случае потребуется извлечь объект пользователя из базы данных, если он не был предварительно извлечен. Если это нежелательно, убедитесь, что вы используете методы `prefetch_related` и `select_related` соответствующим образом. Более подробную информацию об этих методах можно найти в [документации django](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

Значение `source='*'` имеет специальное значение и используется для указания того, что в поле должен быть передан весь объект.  Это может быть полезно при создании вложенных представлений или для полей, которым требуется доступ к полному объекту для определения выходного представления.

По умолчанию используется имя поля.

### `валидаторы`

Список функций валидатора, которые должны быть применены к вводимому полю и которые либо выдают ошибку валидации, либо просто возвращаются. Функции валидатора обычно должны вызывать `serializers.ValidationError`, но встроенный в Django `ValidationError` также поддерживается для совместимости с валидаторами, определенными в кодовой базе Django или в сторонних пакетах Django.

### `error_messages`

Словарь кодов ошибок к сообщениям об ошибках.

### `label`

Короткая текстовая строка, которая может использоваться в качестве имени поля в полях формы HTML или других описательных элементах.

### `help_text`

Текстовая строка, которая может быть использована в качестве описания поля в полях формы HTML или других описательных элементах.

### `initial`

Значение, которое должно использоваться для предварительного заполнения значений полей HTML-формы. Вы можете передать ему вызываемый объект, как и
как и в случае с любым обычным полем Django `Field`:

```
import datetime
from rest_framework import serializers
class ExampleSerializer(serializers.Serializer):
    day = serializers.DateField(initial=datetime.date.today)
```

### `style`

Словарь пар ключ-значение, которые могут быть использованы для управления тем, как рендеринг должен отображать поле.

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

Более подробную информацию можно найти в документации [HTML & Forms](../topics/html-and-forms.md).

---

# Булевы поля

## BooleanField

Булево представление.

При использовании HTML-кодированных форм ввода следует помнить, что отсутствие значения всегда будет рассматриваться как установка поля в `False`, даже если для него указана опция `default=True`. Это связано с тем, что входы с флажками HTML представляют состояние без флажка, когда значение отсутствует, поэтому REST framework рассматривает отсутствие значения как пустой вход с флажком.

Обратите внимание, что в Django 2.1 из `models.BooleanField` был удален карг `blank`. До Django 2.1 поля `models.BooleanField` всегда были `blank=True`. Таким образом, начиная с Django 2.1 экземпляры `serializers.BooleanField` по умолчанию будут генерироваться без kwarg `required` (т.е. эквивалентно `required=True`), тогда как в предыдущих версиях Django экземпляры `BooleanField` по умолчанию будут генерироваться с опцией `required=False`.  Если вы хотите управлять этим поведением вручную, явно объявите `BooleanField` в классе сериализатора или используйте опцию `extra_kwargs` для установки флага `required`.

Соответствует `django.db.models.fields.BooleanField`.

**Подпись:** `BooleanField()`.

---

# Строковые поля

## CharField

Текстовое представление. Опционально проверяет, чтобы текст был короче `max_length` и длиннее `min_length`.

Соответствует `django.db.models.fields.CharField` или `django.db.models.fields.TextField`.

**Подпись:** `CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`.

* `max_length` - Проверяет, что входные данные содержат не более указанного количества символов.
* `min_length` - Проверяет, что вводимые данные содержат не менее этого количества символов.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недействительной и вызовет ошибку проверки. По умолчанию `False`.
* `trim_whitespace` - Если установлено значение `True`, то ведущие и последующие пробельные символы будут обрезаны. По умолчанию `True`.

Опция `allow_null` также доступна для строковых полей, хотя ее использование не рекомендуется в пользу `allow_blank`. Можно установить и `allow_blank=True`, и `allow_null=True`, но это означает, что для строковых представлений будут допустимы два разных типа пустого значения, что может привести к несоответствию данных и тонким ошибкам в работе приложения.

## EmailField

Текстовое представление, проверяет, является ли текст действительным адресом электронной почты.

Соответствует `django.db.models.fields.EmailField`.

**Подпись:** `EmailField(max_length=None, min_length=None, allow_blank=False)`.

## RegexField

Текстовое представление, которое проверяет соответствие заданного значения определенному регулярному выражению.

Соответствует `django.forms.fields.RegexField`.

**Подпись:** `RegexField(regex, max_length=None, min_length=None, allow_blank=False)`.

Обязательный аргумент `regex` может быть либо строкой, либо скомпилированным объектом регулярного выражения python.

Использует `django.core.validators.RegexValidator` для валидации.

## SlugField

Поле `RegexField`, которое проверяет вводимые данные по шаблону `[a-zA-Z0-9_-]+`.

Соответствует `django.db.models.fields.SlugField`.

**Подпись:** `SlugField(max_length=50, min_length=None, allow_blank=False)`.

## URLField

Поле `RegexField`, которое проверяет вводимые данные на соответствие шаблону URL. Ожидаются полностью определенные URL вида `http://<host>/<path>`.

Соответствует `django.db.models.fields.URLField`.  Для валидации использует `django.core.validators.URLValidator`.

**Подпись:** `URLField(max_length=200, min_length=None, allow_blank=False)`.

## UUIDField

Поле, которое гарантирует, что вводимые данные являются действительной строкой UUID. Метод `to_internal_value` возвращает экземпляр `uuid.UUID`. На выходе поле вернет строку в каноническом дефисном формате, например:

```
"de305d54-75b4-431b-adb2-eb6b9e546013"
```

**Подпись:** `UUIDField(format='hex_verbose')`.

* ``формат``: Определяет формат представления значения uuid
- `'hex_verbose'` - Каноническое шестнадцатеричное представление, включая дефисы: ``5ce0e9a5-5ffa-654b-cee0-1238041fb31a``.
- `'hex'` - Компактное шестнадцатеричное представление UUID, не включая дефисы: `'5ce0e9a55ffa654bcee01238041fb31a``.
- `'int'` - 128-битное целочисленное представление UUID: ``123456789012312313134124512351145145114``.
- `'urn'` - RFC 4122 URN представление UUID: `'urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a``.

Изменение параметров `формата` влияет только на значения представления. Все форматы принимаются `to_internal_value`.

## FilePathField

Поле, выбор которого ограничен именами файлов в определенном каталоге в файловой системе

Соответствует `django.forms.fields.FilePathField`.

**Значение:** `FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`.

* ``path`` - абсолютный путь файловой системы к каталогу, из которого это поле FilePathField должно получить свой выбор.
* `match` - Регулярное выражение в виде строки, которое FilePathField будет использовать для фильтрации имен файлов.
* `recursive` - Указывает, должны ли включаться все подкаталоги пути.  По умолчанию `False`.
* `allow_files` - Указывает, должны ли включаться файлы в указанном месте. По умолчанию `True`. Либо это, либо `allow_folders` должно быть `True`.
* `allow_folders` - Указывает, следует ли включать папки в указанном месте. По умолчанию `False`. Либо это, либо `allow_files` должно быть `True`.

## IPAddressField

Поле, которое гарантирует, что вводимые данные являются действительной строкой IPv4 или IPv6.

Соответствует `django.forms.fields.IPAddressField` и `django.forms.fields.GenericIPAddressField`.

**Подпись**: `IPAddressField(protocol='both', unpack_ipv4=False, **options)`.

* `protocol` Ограничивает допустимые входы указанным протоколом. Принимаемые значения: 'both' (по умолчанию), 'IPv4' или 'IPv6'. Соответствие не чувствительно к регистру.
* `unpack_ipv4` Распаковывает IPv4 сопоставленные адреса, например ::ffff:192.0.2.1. Если эта опция включена, то адрес будет распакован в 192.0.2.1. По умолчанию отключена. Может использоваться, только когда протокол установлен в 'both'.

---

# Числовые поля

## IntegerField

Целочисленное представление.

Соответствует `django.db.models.fields.IntegerField`, `django.db.models.fields.SmallIntegerField`, `django.db.models.fields.PositiveIntegerField` и `django.db.models.fields.PositiveSmallIntegerField`.

**Подпись**: `IntegerField(max_value=None, min_value=None)`.

* `max_value` Проверьте, что предоставленное число не больше этого значения.
* `min_value` Убедитесь, что предоставленное число не меньше этого значения.

## FloatField

Представление с плавающей запятой.

Соответствует `django.db.models.fields.FloatField`.

**Подпись**: `FloatField(max_value=None, min_value=None)`.

* `max_value` Проверьте, что предоставленное число не больше этого значения.
* `min_value` Убедитесь, что предоставленное число не меньше этого значения.

## DecimalField

Десятичное представление, представленное в Python экземпляром `Decimal`.

Соответствует `django.db.models.fields.DecimalField`.

**Подпись**: `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`.

* `max_digits` Максимальное количество цифр, допустимое в номере. I
[...]
[...]  [...]  [...]  [...]
[...]
[...]
[...]  [...]  [...]  [...]
[...]  [...]  [...]
[...]  [...]  [...]

#### Пример использования

Для проверки чисел до 999 с разрешением 2 знака после запятой можно использовать:

```
serializers.DecimalField(max_digits=5, decimal_places=2)
```

И проверять числа вплоть до любого менее одного миллиарда с разрешением 10 знаков после запятой:

```
serializers.DecimalField(max_digits=19, decimal_places=10)
```

---

# Поля даты и времени

## DateTimeField

Представление даты и времени.

Соответствует `django.db.models.fields.DateTimeField`.

**Подпись:** `DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)`.

* ``формат`` - строка, представляющая формат вывода. Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `DATETETIME_FORMAT`, который будет `'iso-8601'`, если он не задан. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `datetime` должны быть возвращены `to_representation`. В этом случае кодировка времени будет определяться рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут быть использованы для разбора даты.  Если он не указан, будет использована настройка `DATETIME_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.
* `default_timezone` - Подкласс `tzinfo` (`zoneinfo` или `pytz`), представляющий часовой пояс. Если он не указан и включен параметр `USE_TZ`, то по умолчанию используется [текущий часовой пояс](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone). Если `USE_TZ` отключена, то объекты datetime будут наивными.

#### Строки формата `DateTimeField`.

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать время даты в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (eg `'2013-01-29T12:34:56.000000Z'`)

Когда для формата используется значение `None`, объекты `datetime` будут возвращены `to_representation`, а окончательное представление вывода будет определяться классом renderer.

#### `auto_now` и `auto_now_add` поля модели.

При использовании `ModelSerializer` или `HyperlinkedModelSerializer` обратите внимание, что любые поля модели с `auto_now=True` или `auto_now_add=True` будут использовать поля сериализатора, которые по умолчанию имеют значение `read_only=True`.

Если вы хотите переопределить это поведение, вам необходимо явно объявить `DateTimeField` в сериализаторе.  Например:

```
class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField()

    class Meta:
        model = Comment
```

## DateField

Представление даты.

Соответствует `django.db.models.fields.DateField`.

**Подпись:** `DateField(format=api_settings.DATE_FORMAT, input_formats=None)`.

* ``формат`` - строка, представляющая формат вывода.  Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `DATE_FORMAT`, который будет `'iso-8601'`, если он не задан. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `date` должны быть возвращены `to_representation`. В этом случае кодировка даты будет определяться рендерером.
* `input_formats` - список строк, представляющих входные форматы, которые могут быть использованы для разбора даты.  Если он не указан, будет использована настройка `DATE_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.

#### Строки формата `DateField`.

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать даты в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (например, `'2013-01-29'`)

## TimeField

Представление времени.

Соответствует `django.db.models.fields.TimeField`.

**Подпись:** `TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`.

* ``формат`` - строка, представляющая формат вывода.  Если она не указана, то по умолчанию используется то же значение, что и ключ настройки `TIME_FORMAT`, который будет `'iso-8601'`, если он не установлен. Установка в строку формата указывает, что возвращаемые значения `to_representation` должны быть принудительно выведены в строковый формат. Строки формата описаны ниже. Установка этого значения в `None` указывает, что объекты Python `time` должны быть возвращены `to_representation`. В этом случае кодировка времени будет определяться рендерером.
* `input_formats` - Список строк, представляющих входные форматы, которые могут быть использованы для разбора даты.  Если он не указан, будет использована настройка `TIME_INPUT_FORMATS`, которая по умолчанию имеет значение `['iso-8601']`.

#### Строки формата `TimeField`.

Строки формата могут быть либо [Python strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior), которые явно указывают формат, либо специальной строкой `'iso-8601'`, которая указывает, что следует использовать время в стиле [ISO 8601](https://www.w3.org/TR/NOTE-datetime). (например, `'12:34:56.000000'`)

## DurationField

Представление Duration.
Соответствует `django.db.models.fields.DurationField`.

В `validated_data` для этих полей будет содержаться экземпляр `datetime.timedelta`.
Он представляет собой строку, следующую формату `'[DD] [HH:[MM:]]ss[.uuuuuuuu]'`.

**Подпись:** `DurationField(max_value=None, min_value=None)`.

* `max_value` Убедитесь, что предоставленная продолжительность не превышает этого значения.
* `min_value` Убедитесь, что предоставленная продолжительность не меньше этого значения.

---

# Поля выбора

## ChoiceField

Поле, которое может принимать значение из ограниченного набора вариантов.

Используется `ModelSerializer` для автоматической генерации полей, если соответствующее поле модели включает аргумент `choices=...`.

**Подпись:** `ChoiceField(choices)`.

* `choices` - список допустимых значений, или список кортежей `(key, display_name)`.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недопустимой и вызовет ошибку валидации. По умолчанию `False`.
* `html_cutoff` - Если установлено, то это максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Может использоваться для того, чтобы автоматически генерируемые поля выбора с очень большим количеством возможных вариантов выбора не препятствовали отрисовке шаблона. По умолчанию `None`.
* `html_cutoff_text` - Если установлено, то будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию ``Больше чем {count} элементов...``.

Оба параметра `allow_blank` и `allow_null` являются допустимыми для `ChoiceField`, хотя настоятельно рекомендуется использовать только один из них, а не оба. `allow_blank` следует предпочесть для текстовых вариантов, а `allow_null` - для числовых или других нетекстовых вариантов.

## MultipleChoiceField

Поле, которое может принимать набор из нуля, одного или многих значений, выбранных из ограниченного набора вариантов. Принимает один обязательный аргумент. `to_internal_value` возвращает `set`, содержащий выбранные значения.

**Подпись:** `MultipleChoiceField(choices)`.

* `choices` - список допустимых значений, или список кортежей `(key, display_name)`.
* `allow_blank` - Если установлено значение `True`, то пустая строка будет считаться допустимым значением. Если установлено значение `False`, то пустая строка будет считаться недопустимой и вызовет ошибку валидации. По умолчанию `False`.
* `html_cutoff` - Если установлено, то это максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Может использоваться для того, чтобы автоматически генерируемые поля выбора с очень большим количеством возможных вариантов выбора не мешали отрисовке шаблона. По умолчанию `None`.
* `html_cutoff_text` - Если установлено, то будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию ``Больше чем {count} элементов...``.

Как и в случае с `ChoiceField`, оба параметра `allow_blank` и `allow_null` являются допустимыми, хотя настоятельно рекомендуется использовать только один из них, а не оба. `allow_blank` следует предпочесть для текстовых вариантов, а `allow_null` - для числовых или других нетекстовых вариантов.

---

# Поля для загрузки файлов

#### Парсеры и загрузка файлов.

Классы `FileField` и `ImageField` подходят только для использования с `MultiPartParser` или `FileUploadParser`. Большинство парсеров, таких как, например, JSON, не поддерживают загрузку файлов.
Для обработки загруженных файлов используются штатные [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS) Django.

## FileField

Представление файла.  Выполняет стандартную для Django валидацию FileField.

Соответствует `django.forms.fields.FileField`.

**Подпись:** `FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`.

* `max_length` - Указывает максимальную длину имени файла.
* `allow_empty_file` - Указывает, разрешены ли пустые файлы.
* `use_url` - Если установлено значение `True`, то для представления выходных данных будут использоваться строковые значения URL. Если установлено значение `False`, то для вывода будут использоваться строковые значения имени файла. По умолчанию используется значение ключа настроек `UPLOADED_FILES_USE_URL`, которое равно `True`, если не установлено иное.

## ImageField

Представление изображения. Проверяет соответствие содержимого загруженного файла известному формату изображения.

Соответствует `django.forms.fields.ImageField`.

**Подпись:** `ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`.

* `max_length` - Указывает максимальную длину имени файла.
* `allow_empty_file` - Указывает, разрешены ли пустые файлы.
* `use_url` - Если установлено значение `True`, то для представления выходных данных будут использоваться строковые значения URL. Если установлено значение `False`, то для вывода будут использоваться строковые значения имени файла. По умолчанию используется значение ключа настроек `UPLOADED_FILES_USE_URL`, которое равно `True`, если не установлено иное.

Требуется либо пакет `Pillow`, либо пакет `PIL`.  Рекомендуется использовать пакет `Pillow`, поскольку пакет `PIL` больше не поддерживается.

---

# Составные поля

## ListField

Класс поля, который проверяет список объектов.

**Подпись**: `ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)`.

* `child` - экземпляр поля, которое должно использоваться для проверки объектов в списке. Если этот аргумент не указан, то объекты в списке не будут проверяться.
* `allow_empty` - Указывает, разрешены ли пустые списки.
* `min_length` - Проверяет, что список содержит не менее данного количества элементов.
* `max_length` - Проверяет, что список содержит не более этого количества элементов.

Например, для проверки списка целых чисел вы можете использовать что-то вроде следующего:

```
scores = serializers.ListField(
   child=serializers.IntegerField(min_value=0, max_value=100)
)
```

Класс `ListField` также поддерживает декларативный стиль, который позволяет вам писать многократно используемые классы полей списков.

```
class StringListField(serializers.ListField):
    child = serializers.CharField()
```

Теперь мы можем повторно использовать наш пользовательский класс `StringListField` во всем нашем приложении, без необходимости предоставлять ему аргумент `child`.

## DictField

Класс поля, который проверяет словарь объектов. Предполагается, что ключи в `DictField` всегда являются строковыми значениями.

**Подпись**: `DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)`.

* `child` - экземпляр поля, который должен использоваться для проверки значений в словаре. Если этот аргумент не указан, то значения в связке не будут проверяться.
* `allow_empty` - Указывает, разрешены ли пустые словари.

Например, чтобы создать поле, которое проверяет соответствие строк строкам, вы должны написать что-то вроде этого:

```
document = DictField(child=CharField())
```

Вы также можете использовать декларативный стиль, как в `ListField`. Например:

```
class DocumentField(DictField):
    child = CharField()
```

## HStoreField

Предварительно настроенное `DictField`, совместимое с `HStoreField` от Django для postgres.

**Подпись**: `HStoreField(child=<A_FIELD_INSTANCE>, allow_empty=True)`.

* `child` - экземпляр поля, который используется для проверки значений в словаре. По умолчанию дочернее поле принимает как пустые строки, так и значения null.
* `allow_empty` - Указывает, разрешены ли пустые словари.

Обратите внимание, что дочернее поле **должно** быть экземпляром `CharField`, поскольку расширение hstore хранит значения в виде строк.

## JSONField

Класс поля, который проверяет, что входящая структура данных состоит из допустимых примитивов JSON. В альтернативном бинарном режиме он представляет и проверяет бинарные строки, закодированные в JSON.

**Подпись**: `JSONField(binary, encoder)`.

* `binary` - Если установлено значение `True`, то поле будет выводить и проверять строку в кодировке JSON, а не примитивную структуру данных. По умолчанию установлено значение `False`.
* `encoder` - Используйте этот JSON-кодер для сериализации входного объекта. По умолчанию `None`.

---

# Разные поля

## ReadOnlyField

Класс поля, который просто возвращает значение поля без модификации.

Это поле используется по умолчанию в `ModelSerializer` при включении имен полей, относящихся к атрибуту, а не к полю модели.

**Подпись**: `ReadOnlyField()`.

Например, если `has_expired` было свойством модели `Account`, то следующий сериализатор автоматически сгенерирует его как `ReadOnlyField`:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'has_expired']
```

## HiddenField

Класс поля, которое не принимает значение на основе пользовательского ввода, а берет его из значения по умолчанию или вызываемого поля.

**Подпись**: `HiddenField()`.

Например, чтобы включить поле, которое всегда предоставляет текущее время как часть проверяемых сериализатором данных, вы можете использовать следующее:

```
modified = serializers.HiddenField(default=timezone.now)
```

Класс `HiddenField` обычно нужен только в том случае, если у вас есть валидация, которая должна выполняться на основе некоторых предварительно предоставленных значений полей, но вы не хотите раскрывать все эти поля конечному пользователю.

Дополнительные примеры по `HiddenField` смотрите в документации [validators](validators.md).

## ModelField

Общее поле, которое может быть привязано к любому произвольному полю модели. Класс `ModelField` делегирует задачу сериализации/десериализации связанному с ним полю модели.  Это поле можно использовать для создания полей сериализатора для пользовательских полей модели, без необходимости создавать новое пользовательское поле сериализатора.

Это поле используется `ModelSerializer` для соответствия классам полей пользовательской модели.

**Подпись:** `ModelField(model_field=<Django ModelField instance>)`.

Класс `ModelField` обычно предназначен для внутреннего использования, но при необходимости может быть использован вашим API.  Для того чтобы правильно инстанцировать `ModelField`, ему должно быть передано поле, которое присоединено к инстанцированной модели.  Например: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`.

## SerializerMethodField

Это поле доступно только для чтения. Оно получает свое значение путем вызова метода класса сериализатора, к которому оно присоединено. Его можно использовать для добавления любых данных в сериализованное представление вашего объекта.

**Подпись**: `SerializerMethodField(method_name=None)`.

* `method_name` - Имя метода сериализатора, который будет вызван. Если он не включен, то по умолчанию используется `get_<имя_поля>`.

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

# Пользовательские поля

Если вы хотите создать пользовательское поле, вам необходимо создать подкласс `Field` и переопределить один или оба метода `.to_representation()` и `.to_internal_value()`.  Эти два метода используются для преобразования между исходным типом данных и примитивным, сериализуемым типом данных. Примитивными типами данных обычно являются число, строка, булево, `date`/`time`/`datetime` или `None`. Они также могут быть любым списком или словарем, который содержит только другие примитивные объекты. Могут поддерживаться и другие типы, в зависимости от используемого рендерера.

Метод `.to_representation()` вызывается для преобразования исходного типа данных в примитивный, сериализуемый тип данных.

Метод `.to_internal_value()` вызывается для восстановления примитивного типа данных в его внутреннее представление на языке python. Этот метод должен вызывать `serializers.ValidationError, если данные недействительны.

## Примеры

### Базовое пользовательское поле

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

По умолчанию значения полей рассматриваются как сопоставление с атрибутом объекта.  Если вам нужно настроить способ доступа и установки значения поля, вам нужно переопределить `.get_attribute()` и/или `.get_value()`.

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

### Вызывая ошибки валидации

Наш класс `ColorField`, приведенный выше, в настоящее время не выполняет никакой проверки данных.
Чтобы указать на недопустимые данные, мы должны поднять `serializers.ValidationError`, как показано ниже:

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

Этот стиль делает сообщения об ошибках более чистыми и отделенными от кода, поэтому его следует предпочесть.

### Использование `source='*'`

Здесь мы рассмотрим пример *плоской* модели `DataPoint` с атрибутами `x_coordinate` и `y_coordinate`.

```
class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()
```

Используя пользовательское поле и `source='*'`, мы можем предоставить вложенное представление
пары координат:

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

Обратите внимание, что этот пример не обрабатывает валидацию. Отчасти по этой причине в
реальном проекте вложенность координат лучше обрабатывать с помощью вложенного сериализатора
используя `source='*'`, с двумя экземплярами `IntegerField`, каждый из которых имеет свой собственный `source`.
указывающим на соответствующее поле.

Однако ключевыми моментами из примера являются:

* `to_representation` передается весь объект `DataPoint` и должен отображаться из него.

на нужный выход.

```
>>> instance = DataPoint(label='Example', x_coordinate=1, y_coordinate=2)
    >>> out_serializer = DataPointSerializer(instance)
    >>> out_serializer.data
    ReturnDict([('label', 'Example'), ('coordinates', {'x': 1, 'y': 2})])
```

* Если наше поле не предназначено только для чтения, `to_internal_value` должно отображаться обратно в dict

подходит для обновления нашего целевого объекта. При `source='*'`, возврат от
`to_internal_value` будет обновлен корневой словарь данных, а не один ключ.

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

Для полноты картины повторим то же самое, но с вложенным сериализатором
подход, предложенный выше:

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

Здесь отображение между парами атрибутов цели и источника (`x` и
`x_координата`, `y` и `y_координата`) обрабатывается в `IntegerField`
объявлениях. Это наш `NestedCoordinateSerializer`, который принимает `source='*'`.

Наш новый `DataPointSerializer` демонстрирует такое же поведение, как и пользовательское поле
подход.

Сериализация:

```
>>> out_serializer = DataPointSerializer(instance)
>>> out_serializer.data
ReturnDict([('label', 'testing'),
            ('coordinates', OrderedDict([('x', 1), ('y', 2)]))])
```

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

По этой причине подход вложенного сериализатора будет первым, который следует попробовать. Вы
будете использовать подход пользовательских полей, когда вложенный сериализатор станет невыполнимым
или слишком сложным.

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## Составные поля DRF

Пакет [drf-compound-fields](https://drf-compound-fields.readthedocs.io) предоставляет "составные" поля сериализатора, такие как списки простых значений, которые могут быть описаны другими полями, а не сериализаторами с опцией `many=True`. Также предоставляются поля для типизированных словарей и значений, которые могут быть либо определенным типом, либо списком элементов этого типа.

## Дополнительные поля DRF

Пакет [drf-extra-fields](https://github.com/Hipo/drf-extra-fields) предоставляет дополнительные поля сериализатора для фреймворка REST, включая классы `Base64ImageField` и `PointField`.

## djangorestframework-recursive

пакет [djangorestframework-recursive](https://github.com/heywbj/django-rest-framework-recursive) предоставляет `RecursiveField` для сериализации и десериализации рекурсивных структур

## django-rest-framework-gis

Пакет [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) предоставляет географические дополнения для django rest framework, такие как поле `GeometryField` и сериализатор GeoJSON.

## django-rest-framework-hstore

Пакет [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `HStoreField` для поддержки поля модели [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField`.