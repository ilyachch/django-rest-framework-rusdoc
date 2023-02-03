<!-- TRANSLATED by md-translate -->
---

source:

источник:

* validators.py

* validators.py

---

# Validators

# Валидаторы

> Validators can be useful for re-using validation logic between different types of fields.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/ref/validators/)

> Валидаторы могут быть полезны для повторного использования логики проверки между различными типами полей.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/ref/validators/)

Most of the time you're dealing with validation in REST framework you'll simply be relying on the default field validation, or writing explicit validation methods on serializer or field classes.

В большинстве случаев, когда вы имеете дело с валидацией в REST-фреймворке, вы просто полагаетесь на валидацию полей по умолчанию или пишете явные методы валидации в сериализаторе или классах полей.

However, sometimes you'll want to place your validation logic into reusable components, so that it can easily be reused throughout your codebase. This can be achieved by using validator functions and validator classes.

Однако иногда вам захочется поместить логику валидации в многоразовые компоненты, чтобы ее можно было легко использовать повторно во всей вашей кодовой базе. Этого можно достичь с помощью функций валидатора и классов валидатора.

## Validation in REST framework

## Валидация в REST-фреймворке

Validation in Django REST framework serializers is handled a little differently to how validation works in Django's `ModelForm` class.

Валидация в сериализаторах Django REST framework обрабатывается немного иначе, чем валидация в классе Django `ModelForm`.

With `ModelForm` the validation is performed partially on the form, and partially on the model instance. With REST framework the validation is performed entirely on the serializer class. This is advantageous for the following reasons:

При использовании `ModelForm` проверка выполняется частично на форме, а частично на экземпляре модели. В фреймворке REST валидация выполняется полностью на классе сериализатора. Это выгодно по следующим причинам:

* It introduces a proper separation of concerns, making your code behavior more obvious.
* It is easy to switch between using shortcut `ModelSerializer` classes and using explicit `Serializer` classes. Any validation behavior being used for `ModelSerializer` is simple to replicate.
* Printing the `repr` of a serializer instance will show you exactly what validation rules it applies. There's no extra hidden validation behavior being called on the model instance.

* Это вводит правильное разделение проблем, делая поведение вашего кода более очевидным.
* Легко переключаться между использованием коротких классов `ModelSerializer` и явными классами `Serializer`. Любое поведение валидации, используемое для `ModelSerializer`, легко воспроизвести.
* Распечатка `repr` экземпляра сериализатора покажет вам, какие именно правила валидации он применяет. Нет никакого дополнительного скрытого поведения валидации, вызываемого на экземпляре модели.

When you're using `ModelSerializer` all of this is handled automatically for you. If you want to drop down to using `Serializer` classes instead, then you need to define the validation rules explicitly.

При использовании `ModelSerializer` все это обрабатывается автоматически. Если вы хотите перейти к использованию классов `Serializer`, то вам необходимо явно определить правила валидации.

#### Example

#### Пример

As an example of how REST framework uses explicit validation, we'll take a simple model class that has a field with a uniqueness constraint.

В качестве примера того, как фреймворк REST использует явную валидацию, возьмем простой класс модели, в котором есть поле с ограничением уникальности.

```
class CustomerReportRecord(models.Model):
    time_raised = models.DateTimeField(default=timezone.now, editable=False)
    reference = models.CharField(unique=True, max_length=20)
    description = models.TextField()
```

Here's a basic `ModelSerializer` that we can use for creating or updating instances of `CustomerReportRecord`:

Вот базовый `ModelSerializer`, который мы можем использовать для создания или обновления экземпляров `CustomerReportRecord`:

```
class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReportRecord
```

If we open up the Django shell using `manage.py shell` we can now

Если мы откроем оболочку Django с помощью `manage.py shell`, то теперь мы можем

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

Интересным здесь является поле `reference`. Мы видим, что ограничение уникальности явно обеспечивается валидатором на поле сериализатора.

Because of this more explicit style REST framework includes a few validator classes that are not available in core Django. These classes are detailed below.

Из-за этого более явного стиля REST framework включает несколько классов валидаторов, которые недоступны в основном Django. Эти классы подробно описаны ниже.

---

## UniqueValidator

## UniqueValidator

This validator can be used to enforce the `unique=True` constraint on model fields. It takes a single required argument, and an optional `messages` argument:

Этот валидатор можно использовать для обеспечения ограничения `unique=True` для полей модели. Он принимает один обязательный аргумент и необязательный аргумент `messages`:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `message` - The error message that should be used when validation fails.
* `lookup` - The lookup used to find an existing instance with the value being validated. Defaults to `'exact'`.

* `queryset` *required* - Это набор запросов, в отношении которого должна обеспечиваться уникальность.
* `message` - Сообщение об ошибке, которое должно быть использовано при неудачной проверке.
* `lookup` - Поиск, используемый для нахождения существующего экземпляра с проверяемым значением. По умолчанию `'exact''.

This validator should be applied to *serializer fields*, like so:

Этот валидатор должен применяться к *полям сериализатора*, например, так:

```
from rest_framework.validators import UniqueValidator

slug = SlugField(
    max_length=100,
    validators=[UniqueValidator(queryset=BlogPost.objects.all())]
)
```

## UniqueTogetherValidator

## UniqueTogetherValidator

This validator can be used to enforce `unique_together` constraints on model instances. It has two required arguments, and a single optional `messages` argument:

Этот валидатор можно использовать для наложения ограничений `unique_together` на экземпляры модели. Он имеет два обязательных аргумента и один необязательный аргумент `messages`:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `fields` *required* - A list or tuple of field names which should make a unique set. These must exist as fields on the serializer class.
* `message` - The error message that should be used when validation fails.

* `queryset` *required* - Это набор запросов, в отношении которого должна обеспечиваться уникальность.
* `fields` *обязательно* - Список или кортеж имен полей, которые должны составлять уникальный набор. Они должны существовать как поля в классе сериализатора.
* `message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

The validator should be applied to *serializer classes*, like so:

Валидатор должен применяться к классам *сериализаторов*, например, так:

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

**Примечание**: Класс `UniqueTogetherValidator` всегда накладывает неявное ограничение на то, что все поля, к которым он применяется, всегда рассматриваются как обязательные. Поля со значениями `default` являются исключением из этого правила, поскольку они всегда предоставляют значение, даже если оно опущено при вводе пользователем.

---

## UniqueForDateValidator

## UniqueForDateValidator

## UniqueForMonthValidator

## UniqueForMonthValidator

## UniqueForYearValidator

## UniqueForYearValidator

These validators can be used to enforce the `unique_for_date`, `unique_for_month` and `unique_for_year` constraints on model instances. They take the following arguments:

Эти валидаторы могут быть использованы для наложения ограничений `unique_for_date`, `unique_for_month` и `unique_for_year` на экземпляры модели. Они принимают следующие аргументы:

* `queryset` *required* - This is the queryset against which uniqueness should be enforced.
* `field` *required* - A field name against which uniqueness in the given date range will be validated. This must exist as a field on the serializer class.
* `date_field` *required* - A field name which will be used to determine date range for the uniqueness constrain. This must exist as a field on the serializer class.
* `message` - The error message that should be used when validation fails.

* `queryset` *required* - Это набор запросов, в отношении которого должна обеспечиваться уникальность.
* `field` *обязательно* - Имя поля, по которому будет проверяться уникальность в заданном диапазоне дат. Оно должно существовать как поле в классе сериализатора.
* `date_field` *обязательно* - Имя поля, которое будет использоваться для определения диапазона дат для ограничения уникальности. Оно должно существовать как поле в классе сериализатора.
* `message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

The validator should be applied to *serializer classes*, like so:

Валидатор должен применяться к классам *сериализаторов*, например, так:

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

Поле даты, которое используется для валидации, всегда должно присутствовать в классе сериализатора. Вы не можете просто положиться на класс модели `default=...`, потому что значение, используемое по умолчанию, будет создано только после выполнения валидации.

There are a couple of styles you may want to use for this depending on how you want your API to behave. If you're using `ModelSerializer` you'll probably simply rely on the defaults that REST framework generates for you, but if you are using `Serializer` or simply want more explicit control, use on of the styles demonstrated below.

Существует несколько стилей, которые вы можете использовать для этого, в зависимости от того, как вы хотите, чтобы вел себя ваш API. Если вы используете `ModelSerializer`, вы, вероятно, просто будете полагаться на значения по умолчанию, которые REST framework генерирует для вас, но если вы используете `Serializer` или просто хотите более явного контроля, используйте один из стилей, продемонстрированных ниже.

#### Using with a writable date field.

#### Использование с записываемым полем даты.

If you want the date field to be writable the only thing worth noting is that you should ensure that it is always available in the input data, either by setting a `default` argument, or by setting `required=True`.

Если вы хотите, чтобы поле даты было доступно для записи, единственное, что стоит отметить, это то, что вы должны убедиться, что оно всегда доступно во входных данных, либо задав аргумент `default`, либо установив `required=True`.

```
published = serializers.DateTimeField(required=True)
```

#### Using with a read-only date field.

#### Использование с полем даты, доступным только для чтения.

If you want the date field to be visible, but not editable by the user, then set `read_only=True` and additionally set a `default=...` argument.

Если вы хотите, чтобы поле даты было видимым, но не редактируемым пользователем, то установите `read_only=True` и дополнительно задайте аргумент `default=...`.

```
published = serializers.DateTimeField(read_only=True, default=timezone.now)
```

#### Using with a hidden date field.

#### Использование со скрытым полем даты.

If you want the date field to be entirely hidden from the user, then use `HiddenField`. This field type does not accept user input, but instead always returns its default value to the `validated_data` in the serializer.

Если вы хотите, чтобы поле даты было полностью скрыто от пользователя, используйте `HiddenField`. Этот тип поля не принимает ввод пользователя, а вместо этого всегда возвращает значение по умолчанию в `validated_data` в сериализаторе.

```
published = serializers.HiddenField(default=timezone.now)
```

---

**Note**: The `UniqueFor<Range>Validator` classes impose an implicit constraint that the fields they are applied to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.

**Примечание**: Классы `UniqueFor<Range>Validator` накладывают неявное ограничение на то, что поля, к которым они применяются, всегда рассматриваются как обязательные. Поля со значениями `default` являются исключением из этого правила, поскольку они всегда предоставляют значение, даже если оно опущено при вводе пользователем.

---

# Advanced field defaults

# Расширенные значения полей по умолчанию

Validators that are applied across multiple fields in the serializer can sometimes require a field input that should not be provided by the API client, but that *is* available as input to the validator.

Валидаторы, применяемые к нескольким полям в сериализаторе, иногда могут потребовать ввода поля, которое не должно предоставляться клиентом API, но которое *доступно* в качестве ввода для валидатора.

Two patterns that you may want to use for this sort of validation include:

Два шаблона, которые вы можете использовать для такого рода проверки, включают:

* Using `HiddenField`. This field will be present in `validated_data` but *will not* be used in the serializer output representation.
* Using a standard field with `read_only=True`, but that also includes a `default=…` argument. This field *will* be used in the serializer output representation, but cannot be set directly by the user.

* Использование `HiddenField`. Это поле будет присутствовать в `validated_data`, но *не будет* использоваться в выходном представлении сериализатора.
* Использование стандартного поля с `read_only=True`, но которое также включает аргумент `default=...`. Это поле *будет* использоваться в выходном представлении сериализатора, но не может быть задано непосредственно пользователем.

REST framework includes a couple of defaults that may be useful in this context.

Структура REST включает в себя несколько параметров по умолчанию, которые могут быть полезны в данном контексте.

#### CurrentUserDefault

#### CurrentUserDefault

A default class that can be used to represent the current user. In order to use this, the 'request' must have been provided as part of the context dictionary when instantiating the serializer.

Класс по умолчанию, который может быть использован для представления текущего пользователя. Чтобы использовать его, 'request' должен быть предоставлен как часть контекстного словаря при инстанцировании сериализатора.

```
owner = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
```

#### CreateOnlyDefault

#### CreateOnlyDefault

A default class that can be used to *only set a default argument during create operations*. During updates the field is omitted.

Класс по умолчанию, который можно использовать для *только для установки аргумента по умолчанию во время операций создания*. При обновлении поле опускается.

It takes a single argument, which is the default value or callable that should be used during create operations.

Он принимает единственный аргумент, который является значением по умолчанию или вызываемой переменной, которая должна использоваться во время операций создания.

```
created_at = serializers.DateTimeField(
    default=serializers.CreateOnlyDefault(timezone.now)
)
```

---

# Limitations of validators

# Ограничения валидаторов

There are some ambiguous cases where you'll need to instead handle validation explicitly, rather than relying on the default serializer classes that `ModelSerializer` generates.

Есть несколько неоднозначных случаев, когда вам нужно будет явно обработать проверку, а не полагаться на классы сериализаторов по умолчанию, которые генерирует `ModelSerializer`.

In these cases you may want to disable the automatically generated validators, by specifying an empty list for the serializer `Meta.validators` attribute.

В таких случаях вы можете отключить автоматически создаваемые валидаторы, указав пустой список для атрибута сериализатора `Meta.validators`.

## Optional fields

## Необязательные поля

By default "unique together" validation enforces that all fields be `required=True`. In some cases, you might want to explicit apply `required=False` to one of the fields, in which case the desired behavior of the validation is ambiguous.

По умолчанию валидация "unique together" заставляет все поля быть `required=True`. В некоторых случаях вы можете захотеть явно применить `required=False` к одному из полей, в этом случае желаемое поведение валидации будет неоднозначным.

In this case you will typically need to exclude the validator from the serializer class, and instead write any validation logic explicitly, either in the `.validate()` method, or else in the view.

В этом случае обычно необходимо исключить валидатор из класса сериализатора, а вместо этого написать логику валидации явно, либо в методе `.validate()`, либо в представлении.

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

## Обновление вложенных сериализаторов

When applying an update to an existing instance, uniqueness validators will exclude the current instance from the uniqueness check. The current instance is available in the context of the uniqueness check, because it exists as an attribute on the serializer, having initially been passed using `instance=...` when instantiating the serializer.

При применении обновления к существующему экземпляру, валидаторы уникальности исключают текущий экземпляр из проверки уникальности. Текущий экземпляр доступен в контексте проверки уникальности, поскольку он существует как атрибут сериализатора, будучи изначально переданным с помощью `instance=...` при инстанцировании сериализатора.

In the case of update operations on *nested* serializers there's no way of applying this exclusion, because the instance is not available.

В случае операций обновления для *вложенных* сериализаторов нет возможности применить это исключение, поскольку экземпляр недоступен.

Again, you'll probably want to explicitly remove the validator from the serializer class, and write the code for the validation constraint explicitly, in a `.validate()` method, or in the view.

Опять же, вы, вероятно, захотите явно удалить валидатор из класса сериализатора и написать код для ограничения валидации явно, в методе `.validate()` или в представлении.

## Debugging complex cases

## Отладка сложных случаев

If you're not sure exactly what behavior a `ModelSerializer` class will generate it is usually a good idea to run `manage.py shell`, and print an instance of the serializer, so that you can inspect the fields and validators that it automatically generates for you.

Если вы не уверены, какое именно поведение будет генерировать класс `ModelSerializer`, обычно полезно запустить `manage.py shell` и распечатать экземпляр сериализатора, чтобы вы могли проверить поля и валидаторы, которые он автоматически генерирует для вас.

```
>>> serializer = MyComplexModelSerializer()
>>> print(serializer)
class MyComplexModelSerializer:
    my_fields = ...
```

Also keep in mind that with complex cases it can often be better to explicitly define your serializer classes, rather than relying on the default `ModelSerializer` behavior. This involves a little more code, but ensures that the resulting behavior is more transparent.

Также имейте в виду, что в сложных случаях часто бывает лучше явно определить свои классы сериализаторов, а не полагаться на поведение `ModelSerializer` по умолчанию. Это требует немного больше кода, но гарантирует, что результирующее поведение будет более прозрачным.

---

# Writing custom validators

# Написание пользовательских валидаторов

You can use any of Django's existing validators, or write your own custom validators.

Вы можете использовать любой из существующих валидаторов Django или написать свой собственный валидатор.

## Function based

## Функция основана

A validator may be any callable that raises a `serializers.ValidationError` on failure.

Валидатором может быть любой вызываемый объект, который при неудаче выдает `serializers.ValidationError.

```
def even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even number.')
    return value
```

#### Field-level validation

#### Валидация на полевом уровне

You can specify custom field-level validation by adding `.validate_<field_name>` methods to your `Serializer` subclass. This is documented in the [Serializer docs](https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation)

Вы можете задать пользовательскую валидацию на уровне полей, добавив методы `.validate_<имя_поля>` в подкласс `Serializer`. Это описано в [Serializer docs](https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation).

## Class-based

## На основе класса

To write a class-based validator, use the `__call__` method. Class-based validators are useful as they allow you to parameterize and reuse behavior.

Чтобы написать валидатор на основе класса, используйте метод `__call__`. Валидаторы на основе классов полезны, поскольку позволяют параметризовать и повторно использовать поведение.

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

In some advanced cases you might want a validator to be passed the serializer field it is being used with as additional context. You can do so by setting a `requires_context = True` attribute on the validator. The `__call__` method will then be called with the `serializer_field` or `serializer` as an additional argument.

В некоторых сложных случаях вы можете захотеть, чтобы валидатору передавалось поле сериализатора, с которым он используется, в качестве дополнительного контекста. Вы можете сделать это, установив атрибут `requires_context = True` для валидатора. Тогда метод `__call__` будет вызван с полем `serializer_field` или `serializer` в качестве дополнительного аргумента.

```
requires_context = True

def __call__(self, value, serializer_field):
    ...
```