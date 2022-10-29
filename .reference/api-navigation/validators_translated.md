---

source:
    - validators.py

источник:
- validators.py

---

# Validators

# Validators

> Validators can be useful for re-using validation logic between different types of fields.
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/ref/validators/)

> Валидаторы могут быть полезны для повторного использования логики проверки между различными типами полей.
>
> & mdash;
[Документация Django] (https://docs.djangoproject.com/en/stable/ref/validators/)

Most of the time you're dealing with validation in REST framework you'll simply be relying on the default field validation, or writing explicit validation methods on serializer or field classes.

Большую часть времени вы имеете дело с валидацией в рамках REST, вы просто будете полагаться на проверку поля по умолчанию или написание явных методов проверки на сериализаторах или полевых классах.

However, sometimes you'll want to place your validation logic into reusable components, so that it can easily be reused throughout your codebase. This can be achieved by using validator functions and validator classes.

Тем не менее, иногда вы захотите разместить свою логику проверки в компоненты многократного использования, чтобы ее можно было легко повторно использовать на всей вашей кодовой базе.
Это может быть достигнуто с помощью функций валидатора и классов валидаторов.

## Validation in REST framework

## проверка в рамках REST

Validation in Django REST framework serializers is handled a little differently to how validation works in Django's `ModelForm` class.

Валидация в Django Rest Framework Serializers обрабатывается немного по -разному с тем, как работает проверка в классе Django «Modelform».

With `ModelForm` the validation is performed partially on the form, and partially on the model instance. With REST framework the validation is performed entirely on the serializer class. This is advantageous for the following reasons:

С `modelform` валидация выполняется частично в форме и частично в экземпляре модели.
С структурой отдыха проверка выполняется полностью на классе сериализатора.
Это выгодно по следующим причинам:

* It introduces a proper separation of concerns, making your code behavior more obvious.
* It is easy to switch between using shortcut `ModelSerializer` classes and using  explicit `Serializer` classes. Any validation behavior being used for `ModelSerializer` is simple to replicate.
* Printing the `repr` of a serializer instance will show you exactly what validation rules it applies. There's no extra hidden validation behavior being called on the model instance.

* Он вводит правильное разделение проблем, что делает ваше код более очевидным.
* Легко переключаться между использованием классов `modelerializer 'и с использованием явных классов` serializer.
Любое валидационное поведение, используемое для `moderializer`, просто воспроизвести.
* Печать `repr` экземпляра сериализатора покажет вам, какие правила проверки он применяется.
Нет никакого дополнительного скрытого валидационного поведения, вызванного экземпляром модели.

When you're using `ModelSerializer` all of this is handled automatically for you. If you want to drop down to using `Serializer` classes instead, then you need to define the validation rules explicitly.

Когда вы используете `modelerializer`, все это обрабатывается автоматически для вас.
Если вы хотите вместо этого прийти к использованию классов `serializer ', вам необходимо явно определить правила проверки.

#### Example

#### Пример

As an example of how REST framework uses explicit validation, we'll take a simple model class that has a field with a uniqueness constraint.

В качестве примера того, как Framework REST использует явную проверку, мы возьмем простой класс модели, который имеет поле с уникальностью.

```
class CustomerReportRecord(models.Model):
    time_raised = models.DateTimeField(default=timezone.now, editable=False)
    reference = models.CharField(unique=True, max_length=20)
    description = models.TextField()
```

Here's a basic `ModelSerializer` that we can use for creating or updating instances of `CustomerReportRecord`:

Вот базовый `modelerializer`, который мы можем использовать для создания или обновления экземпляров` customerreportrecord`:

```
class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReportRecord
```

If we open up the Django shell using `manage.py shell` we can now

Если мы откроем оболочку django, используя `Manage.py Shell

```
>>> from project.example.serializers import CustomerReportSerializer
>>> serializer = CustomerReportSerializer()
>>> print(repr(serializer))
CustomerReportSerializer():
    id = IntegerField(label='ID', read_only=True)
    time_raised = DateTimeField(read_only=True)
    reference = CharField(max_length=20, validators=[<UniqueValidator(queryset=CustomerReportRecord.objects.all())>])
    description = CharField(style={'type': 'textarea'})
```

The interesting bit here is the `reference` field. We can see that the uniqueness constraint is being explicitly enforced by a validator on the serializer field.

Интересный бит здесь - поле «Справочник».
Мы видим, что ограничение уникальности явно применяется валидатором на поле сериализатора.

Because of this more explicit style REST framework includes a few validator classes that are not available in core Django. These classes are detailed below.

Из -за этого более явного стиля структура REST включает в себя несколько классов валидаторов, которые недоступны в Core Django.
Эти классы подробно описаны ниже.

---

## UniqueValidator

## Uniquevalidator

This validator can be used to enforce the `unique=True` constraint on model fields.
It takes a single required argument, and an optional `messages` argument:

Этот валидатор может использоваться для обеспечения соблюдения ограничения `уникально = true` на модельных полях.
Требуется один необходимый аргумент и дополнительный аргумент «Сообщения»:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `message` - The error message that should be used when validation fails.
* `lookup` - The lookup used to find an existing instance with the value being validated. Defaults to `'exact'`.

* `Queryset` * требуется * - это вопрос, против которого должна быть введена уникальность.
* `message` - сообщение об ошибке, которое следует использовать при сбое проверки.
* `lookup` - поиск, используемый для поиска существующего экземпляра со значением, подтвержденным.
По умолчанию к «точному».

This validator should be applied to *serializer fields*, like so:

Этот валидатор должен быть применен к *полям сериализатора *, как так:

```
from rest_framework.validators import UniqueValidator

slug = SlugField(
    max_length=100,
    validators=[UniqueValidator(queryset=BlogPost.objects.all())]
)
```

## UniqueTogetherValidator

## Uniquetogethervalidator

This validator can be used to enforce `unique_together` constraints on model instances.
It has two required arguments, and a single optional `messages` argument:

Этот валидатор может использоваться для обеспечения соблюдения ограничений `in ulize_together` на экземплярах модели.
У него есть два требуемых аргумента и один необязательный аргумент «Сообщения»:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `fields` *required* - A list or tuple of field names which should make a unique set. These must exist as fields on the serializer class.
* `message` - The error message that should be used when validation fails.

* `Queryset` * требуется * - это вопрос, против которого должна быть введена уникальность.
* `fields` * требуется * - список или кортеж с именами поля, которые должны создавать уникальный набор.
Они должны существовать как поля на классе сериализатора.
* `message` - сообщение об ошибке, которое следует использовать при сбое проверки.

The validator should be applied to *serializer classes*, like so:

Валидатор должен быть применен к *классам сериализатора *, как так:

```
from rest_framework.validators import UniqueTogetherValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # ToDo items belong to a parent list, and have an ordering defined
        # by the 'position' field. No two items in a given list may share
        # the same position.
        validators = [
            UniqueTogetherValidator(
                queryset=ToDoItem.objects.all(),
                fields=['list', 'position']
            )
        ]
```

---

**Note**: The `UniqueTogetherValidator` class always imposes an implicit constraint that all the fields it applies to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.

** ПРИМЕЧАНИЕ **: Класс `uniquetogetherSethervalidator` всегда налагает неявное ограничение, к которому все поля применяются, всегда рассматриваются по мере необходимости.
Поля со значениями «по умолчанию» являются исключением из этого, поскольку они всегда предоставляют значение, даже если они опущены от пользовательского ввода.

---

## UniqueForDateValidator

## uniquefordatevalidator

## UniqueForMonthValidator

## uniqueformonthvalidator

## UniqueForYearValidator

## uniqueforyearvalidator

These validators can be used to enforce the `unique_for_date`, `unique_for_month` and `unique_for_year` constraints on model instances. They take the following arguments:

Эти валидаторы могут быть использованы для обеспечения соблюдения ограничений `inkiply_for_date`,` inkiply_for_month` и `in ulious_for_year` на экземплярах модели.
Они принимают следующие аргументы:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `field` *required* - A field name against which uniqueness in the given date range will be validated. This must exist as a field on the serializer class.
* `date_field` *required* - A field name which will be used to determine date range for the uniqueness constrain. This must exist as a field on the serializer class.
* `message` - The error message that should be used when validation fails.

* `Queryset` * требуется * - это вопрос, против которого должна быть введена уникальность.
* `field` * требуется * - Имя поля, против которого будет подтверждена уникальность в данном диапазоне дат.
Это должно существовать как поле на классе сериализатора.
* `date_field` * требуется * - Имя поля, которое будет использоваться для определения диапазона дат для ограничения уникальности.
Это должно существовать как поле на классе сериализатора.
* `message` - сообщение об ошибке, которое следует использовать при сбое проверки.

The validator should be applied to *serializer classes*, like so:

Валидатор должен быть применен к *классам сериализатора *, как так:

```
from rest_framework.validators import UniqueForYearValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # Blog posts should have a slug that is unique for the current year.
        validators = [
            UniqueForYearValidator(
                queryset=BlogPostItem.objects.all(),
                field='slug',
                date_field='published'
            )
        ]
```

The date field that is used for the validation is always required to be present on the serializer class. You can't simply rely on a model class `default=...`, because the value being used for the default wouldn't be generated until after the validation has run.

Поле даты, которое используется для проверки, всегда необходимо присутствовать в классе сериализатора.
Вы не можете просто полагаться на модельный класс `default = ...`, потому что значение, используемое для по умолчанию, не будет генерироваться до тех пор, пока не будет выполнена проверка.

There are a couple of styles you may want to use for this depending on how you want your API to behave. If you're using `ModelSerializer` you'll probably simply rely on the defaults that REST framework generates for you, but if you are using `Serializer` or simply want more explicit control, use on of the styles demonstrated below.

Есть несколько стилей, которые вы можете использовать для этого в зависимости от того, как вы хотите, чтобы ваш API вел себя.
Если вы используете `modelerializer`, вы, вероятно, просто полагаетесь на дефолты, которые создает структура REST для вас, но если вы используете« Serializer »или просто хотите более явного управления, использование стилей, показанных ниже.

#### Using with a writable date field.

#### Использование с полем даты записи.

If you want the date field to be writable the only thing worth noting is that you should ensure that it is always available in the input data, either by setting a `default` argument, or by setting `required=True`.

Если вы хотите, чтобы поле даты подлежит записи, единственное, что стоит отметить, это то, что вы должны убедиться, что оно всегда доступно во входных данных, либо установив аргумент «по умолчанию», либо установив `required = true`.

```
published = serializers.DateTimeField(required=True)
```

#### Using with a read-only date field.

#### Использование с полетом только для чтения.

If you want the date field to be visible, but not editable by the user, then set `read_only=True` and additionally set a `default=...` argument.

Если вы хотите, чтобы поле даты было видимым, но не редактируемом пользователем, установите `read_only = true` и дополнительно установите аргумент` default = ... `.

```
published = serializers.DateTimeField(read_only=True, default=timezone.now)
```

#### Using with a hidden date field.

#### Использование с скрытым полем даты.

If you want the date field to be entirely hidden from the user, then use `HiddenField`. This field type does not accept user input, but instead always returns its default value to the `validated_data` in the serializer.

Если вы хотите, чтобы поле даты было полностью скрыто от пользователя, используйте `hiddenfield '.
Этот тип поля не принимает пользовательский ввод, но вместо этого всегда возвращает свое значение по умолчанию в `valyated_data` в сериализаторе.

```
published = serializers.HiddenField(default=timezone.now)
```

---

**Note**: The `UniqueFor<Range>Validator` classes impose an implicit constraint that the fields they are applied to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.

** ПРИМЕЧАНИЕ **: Классы `уникальны <Диапазон> Validator` налагают неявное ограничение, к которым применяются поля, которые они применяются, всегда рассматриваются по мере необходимости.
Поля со значениями «по умолчанию» являются исключением из этого, поскольку они всегда предоставляют значение, даже если они опущены от пользовательского ввода.

---

# Advanced field defaults

# Усовершенствованные поля по умолчанию

Validators that are applied across multiple fields in the serializer can sometimes require a field input that should not be provided by the API client, but that *is* available as input to the validator.

Валидаторы, которые применяются по нескольким полям в сериализаторе, иногда могут требовать входного входа, который не должен быть предоставлен клиентом API, но это * доступно в качестве входного валидатора.

Two patterns that you may want to use for this sort of validation include:

Два шаблона, которые вы можете использовать для такого рода проверки, включают:

* Using `HiddenField`. This field will be present in `validated_data` but *will not* be used in the serializer output representation.
* Using a standard field with `read_only=True`, but that also includes a `default=…` argument. This field *will* be used in the serializer output representation, but cannot be set directly by the user.

* Использование `hiddenfield`.
Это поле будет присутствовать в `valyated_data`, но * не будет * использоваться в выходном представлении сериализатора.
* Использование стандартного поля с `read_only = true`, но это также включает в себя аргумент default =…`.
Это поле * будет * использоваться в представлении вывода сериализатора, но не может быть установлено непосредственно пользователем.

REST framework includes a couple of defaults that may be useful in this context.

Структура REST включает в себя пару значений по умолчанию, которые могут быть полезны в этом контексте.

#### CurrentUserDefault

#### currentUserDefault

A default class that can be used to represent the current user. In order to use this, the 'request' must have been provided as part of the context dictionary when instantiating the serializer.

Класс по умолчанию, который можно использовать для представления текущего пользователя.
Чтобы использовать это, «запрос» должен был быть предоставлен как часть контекстного словаря при создании сериализатора.

```
owner = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
```

#### CreateOnlyDefault

#### createonlydefault

A default class that can be used to *only set a default argument during create operations*. During updates the field is omitted.

Класс по умолчанию, который можно использовать для *только установить аргумент по умолчанию во время операций создания *.
Во время обновлений поле опущено.

It takes a single argument, which is the default value or callable that should be used during create operations.

Требуется один аргумент, который является значением по умолчанию или применению, который следует использовать во время операций создания.

```
created_at = serializers.DateTimeField(
    default=serializers.CreateOnlyDefault(timezone.now)
)
```

---

# Limitations of validators

# Ограничения валидаторов

There are some ambiguous cases where you'll need to instead handle validation
explicitly, rather than relying on the default serializer classes that
`ModelSerializer` generates.

Есть несколько неоднозначных случаев, когда вам нужно вместо этого обрабатывать проверку
явно, а не полагаться на классы сериализатора по умолчанию, которые
`ModelseRializer 'генерирует.

In these cases you may want to disable the automatically generated validators,
by specifying an empty list for the serializer `Meta.validators` attribute.

В этих случаях вы можете отключить автоматически сгенерированные валидаторы,
указав пустой список для атрибута сериализатора `meta.validators`.

## Optional fields

## необязательные поля

By default "unique together" validation enforces that all fields be
`required=True`. In some cases, you might want to explicit apply
`required=False` to one of the fields, in which case the desired behaviour
of the validation is ambiguous.

По умолчанию «уникальная вместе» проверка обеспечивает соблюдение того, что все поля будут
`обязательно = true`.
В некоторых случаях вы можете явно применить
`tread = false` в одну из полей, и в этом случае желаемое поведение
валидации неоднозначна.

In this case you will typically need to exclude the validator from the
serializer class, and instead write any validation logic explicitly, either
in the `.validate()` method, or else in the view.

В этом случае вам обычно нужно исключить валидатор из
класс сериализатора и вместо этого явно напишите любую логику проверки, либо
в методе `.validate ()` или в том виде представления.

For example:

Например:

```
class BillingRecordSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # Apply custom validation either here, or in the view.

    class Meta:
        fields = ['client', 'date', 'amount']
        extra_kwargs = {'client': {'required': False}}
        validators = []  # Remove a default "unique together" constraint.
```

## Updating nested serializers

## Обновление вложенных сериалов

When applying an update to an existing instance, uniqueness validators will
exclude the current instance from the uniqueness check. The current instance
is available in the context of the uniqueness check, because it exists as
an attribute on the serializer, having initially been passed using
`instance=...` when instantiating the serializer.

При применении обновления к существующему экземпляру валидаторы уникальности будут
Исключите текущий экземпляр из проверки уникальности.
Текущий экземпляр
доступен в контексте проверки уникальности, потому что она существует как
атрибут на сериализаторе, изначально прошел с помощью
`encement = ...` При создании сериализатора.

In the case of update operations on *nested* serializers there's no way of
applying this exclusion, because the instance is not available.

В случае операций обновления на * вложенных * сериализаторах нет способа
применяя это исключение, потому что экземпляр недоступен.

Again, you'll probably want to explicitly remove the validator from the
serializer class, and write the code for the validation constraint
explicitly, in a `.validate()` method, or in the view.

Опять же, вы, вероятно, захотите явно удалить валидатор из
класс сериализатора и напишите код для ограничения проверки
Явно, в методе `.validate ()` или в представлении.

## Debugging complex cases

## отладка сложных случаев

If you're not sure exactly what behavior a `ModelSerializer` class will
generate it is usually a good idea to run `manage.py shell`, and print
an instance of the serializer, so that you can inspect the fields and
validators that it automatically generates for you.

Если вы не уверены, какое поведение будет
генерировать это, как правило, хорошая идея для запуска `Manage.py Shell
экземпляр сериализатора, чтобы вы могли осмотреть поля и
валидаторы, которые он автоматически генерирует для вас.

```
>>> serializer = MyComplexModelSerializer()
>>> print(serializer)
class MyComplexModelSerializer:
    my_fields = ...
```

Also keep in mind that with complex cases it can often be better to explicitly
define your serializer classes, rather than relying on the default
`ModelSerializer` behavior. This involves a little more code, but ensures
that the resulting behavior is more transparent.

Также имейте в виду, что при сложных случаях часто может быть лучше явно
Определите свои классы сериализатора, а не полагаясь на дефолт
`Поведение моделейализатора.
Это включает немного больше кода, но обеспечивает
что полученное поведение является более прозрачным.

---

# Writing custom validators

# Написание пользовательских валидаторов

You can use any of Django's existing validators, or write your own custom validators.

Вы можете использовать любой из существующих валидаторов Django или написать свои собственные пользовательские валидаторы.

## Function based

## Функция на основе

A validator may be any callable that raises a `serializers.ValidationError` on failure.

Валидатор может быть любым вызовом, который поднимает `serializers.validationError

```
def even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even number.')
```

#### Field-level validation

#### проверка на уровне поля

You can specify custom field-level validation by adding `.validate_<field_name>` methods
to your `Serializer` subclass. This is documented in the
[Serializer docs](https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation)

Вы можете указать пользовательскую проверку на уровне поля, добавив `.validate_ <field_name>` Методы
к вашему подклассу «сериализатора».
Это задокументировано в
[Docs Serializer] (https://www.django-rest-framework.org/api-guide/serializers/#field-validation)

## Class-based

## классовый

To write a class-based validator, use the `__call__` method. Class-based validators are useful as they allow you to parameterize and reuse behavior.

Чтобы написать валидатор на основе класса, используйте метод `__CALL__`.
Валидаторы на основе классов полезны, поскольку они позволяют вам параметризировать и повторно использовать поведение.

```
class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            message = 'This field must be a multiple of %d.' % self.base
            raise serializers.ValidationError(message)
```

#### Accessing the context

#### Доступ к контексту

In some advanced cases you might want a validator to be passed the serializer
field it is being used with as additional context. You can do so by setting
a `requires_context = True` attribute on the validator. The `__call__` method
will then be called with the `serializer_field`
or `serializer` as an additional argument.

В некоторых передовых случаях вы можете захотеть пройти Vadidator сериализатор
Поле это используется в качестве дополнительного контекста.
Вы можете сделать это, настроив
a `tress_context = true` -атрибут в валидаторе.
Метод `__CALL__
тогда будет вызван с помощью `serializer_field`
или `serializer` как дополнительный аргумент.

```
requires_context = True

def __call__(self, value, serializer_field):
    ...
```