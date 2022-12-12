<!-- TRANSLATED by md-translate -->
---

source:
    - serializers.py

источник:
- serializers.py

---

# Serializers

# Сериализаторы

> Expanding the usefulness of the serializers is something that we would

> Расширение полезности сериалов - это то, что мы будем

like to address.  However, it's not a trivial problem, and it
will take some serious design work.

нравится обращаться.
Однако это не тривиальная проблема, и это
Пойдет несколько серьезных дизайнерских работ.

>
>
> &mdash; Russell Keith-Magee, [Django users group](https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion)

>
>
> & mdash;
Рассел Кейт-Маги, [группа пользователей Django] (https://groups.google.com/d/topic/django-users/svfaofqi4wy/discussion)

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into `JSON`, `XML` or other content types.  Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

Сериализаторы позволяют преобразовать сложные данные, такие как запросы и экземпляры модели, в нативные данные Python, которые затем можно легко отображать в `json`,` xml` или другие типы контента.
Сериализаторы также обеспечивают десериализацию, позволяя конвертировать данные обратно в сложные типы после сначала проверки входящих данных.

The serializers in REST framework work very similarly to Django's `Form` and `ModelForm` classes. We provide a `Serializer` class which gives you a powerful, generic way to control the output of your responses, as well as a `ModelSerializer` class which provides a useful shortcut for creating serializers that deal with model instances and querysets.

Сериализаторы в рамках REST работают очень аналогично классам Джанго «Форма» и «Modelform».
Мы предоставляем класс «Serializer», который дает вам мощный, общий способ управления выводами ваших ответов, а также класс «Modelerializer», который обеспечивает полезный ярлык для создания сериализаторов, которые имеют дело с экземплярами модели и запросами.

## Declaring Serializers

## объявление сериалов

Let's start by creating a simple object we can use for example purposes:

Давайте начнем с создания простого объекта, который мы можем использовать, например, цели:

```
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')
```

We'll declare a serializer that we can use to serialize and deserialize data that corresponds to `Comment` objects.

Мы объявим сериализатор, который мы можем использовать для сериализации и десериализации данных, которые соответствуют объектам «Комментарий».

Declaring a serializer looks very similar to declaring a form:

Объявление сериализатора выглядит очень похоже на объявление формы:

```
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Serializing objects

## сериализация объектов

We can now use `CommentSerializer` to serialize a comment, or list of comments. Again, using the `Serializer` class looks a lot like using a `Form` class.

Теперь мы можем использовать «Комментарии» для сериализации комментария или списка комментариев.
Опять же, использование класса «Serializer» очень похоже на использование класса «форма».

```
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
```

At this point we've translated the model instance into Python native datatypes.  To finalise the serialization process we render the data into `json`.

На этом этапе мы перевели экземпляр модели в нативные данные Python.
Чтобы завершить процесс сериализации, мы переводим данные в `json '.

```
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
```

## Deserializing objects

## deserialization объектов

Deserialization is similar. First we parse a stream into Python native datatypes...

Десериализация похожа.
Сначала мы проанализируем поток в народные дата дата Python ...

```
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
```

...then we restore those native datatypes into a dictionary of validated data.

... Затем мы восстанавливаем эти собственные данные дата в словаре подтвержденных данных.

```
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
```

## Saving instances

## Сохранение экземпляров

If we want to be able to return complete object instances based on the validated data we need to implement one or both of the `.create()` and `.update()` methods. For example:

Если мы хотим иметь возможность вернуть полные экземпляры объектов на основе проверенных данных, нам необходимо реализовать один или оба метода `.create ()` и `.update ()`.
Например:

```
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance
```

If your object instances correspond to Django models you'll also want to ensure that these methods save the object to the database. For example, if `Comment` was a Django model, the methods might look like this:

Если экземпляры вашего объекта соответствуют моделям Django, вы также захотите убедиться, что эти методы сохраняют объект в базе данных.
Например, если «Комментарий» был моделью Джанго, методы могут выглядеть так:

```
def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
```

Now when deserializing data, we can call `.save()` to return an object instance, based on the validated data.

Теперь, когда десериализуйте данные, мы можем вызвать `.save ()`, чтобы вернуть экземпляр объекта на основе проверенных данных.

```
comment = serializer.save()
```

Calling `.save()` will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class:

Вызов `.save ()` будет либо создать новый экземпляр, либо обновить существующий экземпляр, в зависимости от того, был ли существующий экземпляр пропускался при создании класса сериализатора:

```
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)
```

Both the `.create()` and `.update()` methods are optional. You can implement either none, one, or both of them, depending on the use-case for your serializer class.

Оба метода `.create ()` и `.update ()` являются необязательными.
Вы можете реализовать ни один, один или оба из них, в зависимости от использования валя для вашего класса Serializer.

#### Passing additional attributes to `.save()`

#### Передача дополнительных атрибутов `.save ()`

Sometimes you'll want your view code to be able to inject additional data at the point of saving the instance. This additional data might include information like the current user, the current time, or anything else that is not part of the request data.

Иногда вы захотите, чтобы ваш код представления имел возможность вводить дополнительные данные в точке сохранения экземпляра.
Эти дополнительные данные могут включать информацию, такую как текущий пользователь, текущее время или что -либо еще, что не является частью данных запроса.

You can do so by including additional keyword arguments when calling `.save()`. For example:

Вы можете сделать это, включив дополнительные аргументы ключевых слов при вызове `.save ()`.
Например:

```
serializer.save(owner=request.user)
```

Any additional keyword arguments will be included in the `validated_data` argument when `.create()` or `.update()` are called.

Любые дополнительные аргументы ключевых слов будут включены в аргумент `valyated_data`, когда` .create () `или` .update () `вызываются.

#### Overriding `.save()` directly.

#### переопределение `.save ()` напрямую.

In some cases the `.create()` and `.update()` method names may not be meaningful. For example, in a contact form we may not be creating new instances, but instead sending an email or other message.

В некоторых случаях имена методов `.create ()` и `.update ()` не могут быть значимыми.
Например, в контактной форме мы можем не создавать новые экземпляры, а отправлять электронное письмо или другое сообщение.

In these cases you might instead choose to override `.save()` directly, as being more readable and meaningful.

В этих случаях вы можете вместо этого переопределить `.save ()` напрямую, как более читаемое и значимое.

For example:

Например:

```
class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(from=email, message=message)
```

Note that in the case above we're now having to access the serializer `.validated_data` property directly.

Обратите внимание, что в приведенном выше случае нам теперь приходится получить доступ к свойству. Validated_data` напрямую.

## Validation

## Проверка

When deserializing data, you always need to call `is_valid()` before attempting to access the validated data, or save an object instance. If any validation errors occur, the `.errors` property will contain a dictionary representing the resulting error messages.  For example:

При десериализации данных вам всегда нужно вызовать `is_valid ()`, прежде чем пытаться получить доступ к проверенным данным или сохранить экземпляр объекта.
Если возникают какие -либо ошибки проверки, свойство `.errors 'будет содержать словарь, представляющий полученные сообщения об ошибках.
Например:

```
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
```

Each key in the dictionary will be the field name, and the values will be lists of strings of any error messages corresponding to that field.  The `non_field_errors` key may also be present, and will list any general validation errors. The name of the `non_field_errors` key may be customized using the `NON_FIELD_ERRORS_KEY` REST framework setting.

Каждый ключ в словаре будет именем поля, а значения будут списками строк любых сообщений об ошибках, соответствующих этому поле.
Ключ `non_field_errors
Имя ключа `non_field_errors` может быть настроено с помощью настройки платформы non_field_errors_key`.

When deserializing a list of items, errors will be returned as a list of dictionaries representing each of the deserialized items.

При десериализации списка элементов ошибки будут возвращены в виде списка словарей, представляющих каждый из десериализованных элементов.

#### Raising an exception on invalid data

#### Поднимает исключение на недопустимых данных

The `.is_valid()` method takes an optional `raise_exception` flag that will cause it to raise a `serializers.ValidationError` exception if there are validation errors.

Метод `.is_valid ()` принимает необязательный флаг `maus_exception`, который заставит его поднять исключение` serializers.validationError`, если есть ошибки проверки.

These exceptions are automatically dealt with by the default exception handler that REST framework provides, and will return `HTTP 400 Bad Request` responses by default.

Эти исключения автоматически рассматриваются в обработчике исключений по умолчанию, который предоставляет Framework REST, и по умолчанию возвращает `http 400 Bad Request 'ответы.

```
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

#### Field-level validation

#### проверка на уровне поля

You can specify custom field-level validation by adding `.validate_<field_name>` methods to your `Serializer` subclass.  These are similar to the `.clean_<field_name>` methods on Django forms.

Вы можете указать пользовательскую проверку на уровне поля, добавив `.validate_ <field_name>` методы в ваш подкласс `serializer`.
Они похожи на методы `.clean_ <field_name>` на формах django.

These methods take a single argument, which is the field value that requires validation.

Эти методы принимают один аргумент, который является значением поля, требующим проверки.

Your `validate_<field_name>` methods should return the validated value or raise a `serializers.ValidationError`.  For example:

Ваши методы `validate_ <field_name>` должны вернуть подтвержденное значение или повысить `serializers.validationError`.
Например:

```
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

---

**Note:** If your `<field_name>` is declared on your serializer with the parameter `required=False` then this validation step will not take place if the field is not included.

** ПРИМЕЧАНИЕ: ** Если ваш `<Field_Name>` объявлен на вашем сериализаторе с параметром `required = false`, то этот шаг проверки не будет состояться, если поле не будет включено.

---

#### Object-level validation

#### Проверка на уровне объекта

To do any other validation that requires access to multiple fields, add a method called `.validate()` to your `Serializer` subclass.  This method takes a single argument, which is a dictionary of field values.  It should raise a `serializers.ValidationError` if necessary, or just return the validated values.  For example:

Чтобы выполнить любую другую проверку, которая требует доступа к нескольким полям, добавьте метод под названием `.validate ()` к вашему подклассу `serializer.
Этот метод принимает один аргумент, который является словарем значений поля.
Он должен поднять `serializers.validationError`, если это необходимо, или просто вернуть проверенные значения.
Например:

```
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```

#### Validators

#### Validators

Individual fields on a serializer can include validators, by declaring them on the field instance, for example:

Отдельные поля на сериализаторе могут включать валидаторы, объявив их в экземпляре поля, например:

```
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...
```

Serializer classes can also include reusable validators that are applied to the complete set of field data. These validators are included by declaring them on an inner `Meta` class, like so:

Классы сериализатора также могут включать валидаторы многократного использования, которые применяются к полному набору полевых данных.
Эти валидаторы включены, объявляя их на внутреннем классе «Мета», как и так:

```
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # Each room only has one event per day.
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['room_number', 'date']
            )
        ]
```

For more information see the [validators documentation](validators.md).

Для получения дополнительной информации см. Документацию [Validators] (validators.md).

## Accessing the initial data and instance

## Доступ к начальным данным и экземпляру

When passing an initial object or queryset to a serializer instance, the object will be made available as `.instance`. If no initial object is passed then the `.instance` attribute will be `None`.

При передаче начального объекта или запроса на экземпляр сериализатора объект будет доступен как `.Instance`.
Если начальный объект не пройден, то атрибут `.Instance` будет« нет ».

When passing data to a serializer instance, the unmodified data will be made available as `.initial_data`. If the `data` keyword argument is not passed then the `.initial_data` attribute will not exist.

При передаче данных в экземпляр Serializer, немодифицированные данные будут доступны как `.initial_data`.
Если аргумент ключевого слова «Data» не будет принят, то атрибут `.Initial_Data` не будет существовать.

## Partial updates

## частичные обновления

By default, serializers must be passed values for all required fields or they will raise validation errors. You can use the `partial` argument in order to allow partial updates.

По умолчанию сериализаторы должны быть переданы значения для всех требуемых полей, иначе они приведут к ошибкам проверки.
Вы можете использовать аргумент «частичный», чтобы разрешить частичные обновления.

```
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
```

## Dealing with nested objects

## имеет дело с вложенными объектами

The previous examples are fine for dealing with objects that only have simple datatypes, but sometimes we also need to be able to represent more complex objects, where some of the attributes of an object might not be simple datatypes such as strings, dates or integers.

Предыдущие примеры подходят для работы с объектами, которые имеют только простые данные дата, но иногда нам также необходимо иметь возможность представлять более сложные объекты, где некоторые атрибуты объекта могут быть не простыми данными, такими как строки, даты или целые числа.

The `Serializer` class is itself a type of `Field`, and can be used to represent relationships where one object type is nested inside another.

Класс `serializer 'сам по себе является типом` field' и может использоваться для представления отношений, когда один тип объекта вложен в другой.

```
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

If a nested representation may optionally accept the `None` value you should pass the `required=False` flag to the nested serializer.

Если вложенное представление может примечательно принять значение «Нет», вы должны передать флаг `require = false` к вложенному сериализатору.

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Similarly if a nested representation should be a list of items, you should pass the `many=True` flag to the nested serializer.

Точно так же, если вложенное представление должно быть списком элементов, вы должны передать флаг `myry = true` в вложенный сериализатор.

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Writable nested representations

## Вложенные представления о записи

When dealing with nested representations that support deserializing the data, any errors with nested objects will be nested under the field name of the nested object.

При работе с вложенными представлениями, которые поддерживают десериализацию данных, любые ошибки с вложенными объектами будут вложены под полевым именем вложенного объекта.

```
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid e-mail address.']}, 'created': ['This field is required.']}
```

Similarly, the `.validated_data` property will include nested data structures.

Точно так же свойство `.validated_data` будет включать вложенные структуры данных.

#### Writing `.create()` methods for nested representations

#### Написание `.create ()` Методы для вложенных представлений

If you're supporting writable nested representations you'll need to write `.create()` or `.update()` methods that handle saving multiple objects.

Если вы поддерживаете вложенные представления о записи, вам нужно написать `.create ()` или `.update ()` методы, которые обрабатывают сохранение нескольких объектов.

The following example demonstrates how you might handle creating a user with a nested profile object.

Следующий пример демонстрирует, как вы можете справиться с созданием пользователя с вложенным объектом профиля.

```
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
```

#### Writing `.update()` methods for nested representations

#### Написание `.update ()` Методы для вложенных представлений

For updates you'll want to think carefully about how to handle updates to relationships. For example if the data for the relationship is `None`, or not provided, which of the following should occur?

Для обновлений вы захотите тщательно подумать о том, как обрабатывать обновления к отношениям.
Например, если данные для отношений являются «нет» или не предоставлены, что из следующего должно происходить?

* Set the relationship to `NULL` in the database.
* Delete the associated instance.
* Ignore the data and leave the instance as it is.
* Raise a validation error.

* Установите отношение к `null` в базе данных.
* Удалить связанный экземпляр.
* Игнорируйте данные и оставьте экземпляр таким, какой он есть.
* Установите ошибку проверки.

Here's an example for an `.update()` method on our previous `UserSerializer` class.

Вот пример для метода.

```
def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.is_premium_member = profile_data.get(
            'is_premium_member',
            profile.is_premium_member
        )
        profile.has_support_contract = profile_data.get(
            'has_support_contract',
            profile.has_support_contract
         )
        profile.save()

        return instance
```

Because the behavior of nested creates and updates can be ambiguous, and may require complex dependencies between related models, REST framework 3 requires you to always write these methods explicitly. The default `ModelSerializer` `.create()` and `.update()` methods do not include support for writable nested representations.

Поскольку поведение вложенных создает и обновления может быть неоднозначным и может потребовать сложных зависимостей между родственными моделями, Framework REST 3 требует, чтобы вы всегда писали эти методы явно.
По умолчанию `modelerializer`` .create () `и` .update () `Методы не включают поддержку вложенных записи для представлений.

There are however, third-party packages available such as [DRF Writable Nested](serializers.md#drf-writable-nested) that support automatic writable nested representations.

Однако существуют сторонние пакеты, такие как [DRF-записи, вложенные] (Serializers.md#DRF-Wrible-Tlear), которые поддерживают автоматические вложенные представления о записи.

#### Handling saving related instances in model manager classes

#### Обработка сохранения связанных экземпляров в классах менеджера моделей

An alternative to saving multiple related instances in the serializer is to write custom model manager classes that handle creating the correct instances.

Альтернативой сохранению нескольких связанных экземпляров в сериализаторе является написание пользовательских классов менеджера моделей, которые обрабатывают создание правильных экземпляров.

For example, suppose we wanted to ensure that `User` instances and `Profile` instances are always created together as a pair. We might write a custom manager class that looks something like this:

Например, предположим, что мы хотим убедиться, что экземпляры пользователя и экземпляры «профиль» всегда создаются вместе как пара.
Мы могли бы написать класс пользовательского менеджера, который выглядит примерно так:

```
class UserManager(models.Manager):
    ...

    def create(self, username, email, is_premium_member=False, has_support_contract=False):
        user = User(username=username, email=email)
        user.save()
        profile = Profile(
            user=user,
            is_premium_member=is_premium_member,
            has_support_contract=has_support_contract
        )
        profile.save()
        return user
```

This manager class now more nicely encapsulates that user instances and profile instances are always created at the same time. Our `.create()` method on the serializer class can now be re-written to use the new manager method.

Этот класс менеджера теперь более хорошо инкапсулирует, что экземпляры пользователя и экземпляры профиля всегда создаются одновременно.
Наш метод `.create ()` на классе сериализатора теперь можно переписать, чтобы использовать новый метод менеджера.

```
def create(self, validated_data):
    return User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        is_premium_member=validated_data['profile']['is_premium_member'],
        has_support_contract=validated_data['profile']['has_support_contract']
    )
```

For more details on this approach see the Django documentation on [model managers](https://docs.djangoproject.com/en/stable/topics/db/managers/), and [this blogpost on using model and manager classes](https://www.dabapps.com/blog/django-models-and-encapsulation/).

Для получения более подробной информации об этом подходе см. Документацию Django по [Managers] (https://docs.djangoproject.com/en/stable/topics/db/managers/) и [этот блог об использовании классов модели и менеджера] (
https://www.dabapps.com/blog/django-models-and-capsulation/).

## Dealing with multiple objects

## имеет дело с несколькими объектами

The `Serializer` class can also handle serializing or deserializing lists of objects.

Класс `serializer 'также может обрабатывать сериализацию или десеризацию списков объектов.

#### Serializing multiple objects

#### сериализация нескольких объектов

To serialize a queryset or list of objects instead of a single object instance, you should pass the `many=True` flag when instantiating the serializer.  You can then pass a queryset or list of objects to be serialized.

Чтобы сериализовать запрос или список объектов вместо одного экземпляра объекта, вы должны передать флаг `myry = true` при создании сериализатора.
Затем вы можете передавать запрос или список объектов, которые будут сериализованы.

```
queryset = Book.objects.all()
serializer = BookSerializer(queryset, many=True)
serializer.data
# [
#     {'id': 0, 'title': 'The electric kool-aid acid test', 'author': 'Tom Wolfe'},
#     {'id': 1, 'title': 'If this is a man', 'author': 'Primo Levi'},
#     {'id': 2, 'title': 'The wind-up bird chronicle', 'author': 'Haruki Murakami'}
# ]
```

#### Deserializing multiple objects

#### deserialization несколько объектов

The default behavior for deserializing multiple objects is to support multiple object creation, but not support multiple object updates. For more information on how to support or customize either of these cases, see the [ListSerializer](#listserializer) documentation below.

Поведение по умолчанию для десеризации нескольких объектов заключается в поддержке создания нескольких объектов, но не поддержание нескольких обновлений объектов.
Для получения дополнительной информации о том, как поддержать или настроить любой из этих случаев, см. Документацию [ListSerializer] (#ListSerializer) ниже.

## Including extra context

## включает в себя дополнительный контекст

There are some cases where you need to provide extra context to the serializer in addition to the object being serialized.  One common case is if you're using a serializer that includes hyperlinked relations, which requires the serializer to have access to the current request so that it can properly generate fully qualified URLs.

Есть некоторые случаи, когда вам необходимо предоставить дополнительный контекст сериализатору в дополнение к сериализованному объекту.
Одним из распространенных случаев является то, что вы используете сериализатор, который включает в себя гиперсвязанные отношения, которые требуют, чтобы сериализатор имел доступ к текущему запросу, чтобы он мог должным образом генерировать полностью квалифицированные URL -адреса.

You can provide arbitrary additional context by passing a `context` argument when instantiating the serializer.  For example:

Вы можете предоставить произвольный дополнительный контекст, передавая аргумент «контекста» при создании сериализатора.
Например:

```
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': 'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
```

The context dictionary can be used within any serializer field logic, such as a custom `.to_representation()` method, by accessing the `self.context` attribute.

Словарь контекста может использоваться в любой логике поля сериализатора, такой как пользовательский метод `.to_representation ()`, путем доступа к атрибуту `self.context`.

---

# ModelSerializer

# ModelseRializer

Often you'll want serializer classes that map closely to Django model definitions.

Часто вам понадобятся классы сериализатора, которые тесно связаны с определениями моделей Django.

The `ModelSerializer` class provides a shortcut that lets you automatically create a `Serializer` class with fields that correspond to the Model fields.

Класс `modelseRializer обеспечивает ярлык, который позволяет автоматически создавать класс« сериализатора »с полями, которые соответствуют полям модели.

**The `ModelSerializer` class is the same as a regular `Serializer` class, except that**:

** Класс `modelerializer 'такой же, как и обычный класс` serializer`, за исключением того, что **:

* It will automatically generate a set of fields for you, based on the model.
* It will automatically generate validators for the serializer, such as unique_together validators.
* It includes simple default implementations of `.create()` and `.update()`.

* Он автоматически генерирует набор полей для вас, в зависимости от модели.
* Он будет автоматически генерировать валидаторы для сериализатора, таких как уникальные валидаторы.
* Он включает в себя простые реализации по умолчанию `.create ()` и `.update ()`.

Declaring a `ModelSerializer` looks like this:

Объявление «моделиеализатор» выглядит так:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

By default, all the model fields on the class will be mapped to a corresponding serializer fields.

По умолчанию все поля модели в классе будут сопоставлены с соответствующими полями сериализатора.

Any relationships such as foreign keys on the model will be mapped to `PrimaryKeyRelatedField`. Reverse relationships are not included by default unless explicitly included as specified in the [serializer relations](relations.md) documentation.

Любые отношения, такие как иностранные ключи на модели, будут сопоставлены с «PrimaryKeyRetatedField».
Обратные отношения не включены по умолчанию, если только явно включено, как указано в документацию [Serializer Ontions] (untations.md).

#### Inspecting a `ModelSerializer`

#### Проверка `modelerializer

Serializer classes generate helpful verbose representation strings, that allow you to fully inspect the state of their fields. This is particularly useful when working with `ModelSerializers` where you want to determine what set of fields and validators are being automatically created for you.

Классы сериализатора генерируют полезные устные строки представления, которые позволяют полностью осмотреть состояние их полей.
Это особенно полезно при работе с `moderializers`, где вы хотите определить, какой набор полей и валидаторов автоматически создается для вас.

To do so, open the Django shell, using `python manage.py shell`, then import the serializer class, instantiate it, and print the object representation…

Для этого откройте оболочку Django, используя `python Manage.py Shell`, затем импортируйте класс сериализатора, создайте его и распечатайте представление объекта…

```
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

## Specifying which fields to include

## указание, какие поля включать

If you only want a subset of the default fields to be used in a model serializer, you can do so using `fields` or `exclude` options, just as you would with a `ModelForm`. It is strongly recommended that you explicitly set all fields that should be serialized using the `fields` attribute. This will make it less likely to result in unintentionally exposing data when your models change.

Если вы хотите, чтобы только подмножество полей по умолчанию использовалось в модельном сериализаторе, вы можете сделать это, используя параметры `fields` или` exklide
Настоятельно рекомендуется, чтобы вы явно установили все поля, которые должны быть сериализованы с использованием атрибута «Поля».
Это приведет к тому, что это приведет к непреднамеренно разоблачить данные при изменении ваших моделей.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

You can also set the `fields` attribute to the special value `'__all__'` to indicate that all fields in the model should be used.

Вы также можете установить атрибут «Fields» на специальное значение `'__ll __'`, чтобы указать, что все поля в модели следует использовать.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
```

You can set the `exclude` attribute to a list of fields to be excluded from the serializer.

Вы можете установить атрибут `exklide` в список полей, которые будут исключены из сериализатора.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['users']
```

In the example above, if the `Account` model had 3 fields `account_name`, `users`, and `created`, this will result in the fields `account_name` and `created` to be serialized.

В приведенном выше примере, если модель `chounct` имела 3 поля` account_name`, `users` и` catence`, это приведет к полям `Account_Name` и« создан », чтобы быть сериализованными.

The names in the `fields` and `exclude` attributes will normally map to model fields on the model class.

Имена в атрибутах `fields` и` exclude` обычно отображаются по полевым полям в классе модели.

Alternatively names in the `fields` options can map to properties or methods which take no arguments that exist on the model class.

В качестве альтернативы имена в параметрах «Поля» могут сопоставить свойства или методы, которые не принимают аргументов, которые существуют в классе модели.

Since version 3.3.0, it is **mandatory** to provide one of the attributes `fields` or `exclude`.

Со времени версии 3.3.0, ** обязательно ** предоставить один из атрибутов `fields` или` exklide`.

## Specifying nested serialization

## Указание вложенной сериализации

The default `ModelSerializer` uses primary keys for relationships, but you can also easily generate nested representations using the `depth` option:

По умолчанию `modelerializer` использует первичные ключи для отношений, но вы также можете легко генерировать вложенные представления, используя опцию« глубины »:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        depth = 1
```

The `depth` option should be set to an integer value that indicates the depth of relationships that should be traversed before reverting to a flat representation.

Опция «глубины» должна быть установлена на целочисленное значение, которое указывает на глубину отношений, которые следует пересекать, прежде чем вернуться к плоскому представлению.

If you want to customize the way the serialization is done you'll need to define the field yourself.

Если вы хотите настроить способ выполнения сериализации, вам нужно определить поле самостоятельно.

## Specifying fields explicitly

## Определение полей явно

You can add extra fields to a `ModelSerializer` or override the default fields by declaring fields on the class, just as you would for a `Serializer` class.

Вы можете добавить дополнительные поля в `modelerializer` или переопределить поля по умолчанию, объявив поля в классе, как и для класса« Serializer ».

```
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
        fields = ['url', 'groups']
```

Extra fields can correspond to any property or callable on the model.

Дополнительные поля могут соответствовать любому свойству или вызовому на модели.

## Specifying read only fields

## Указание только поля чтения

You may wish to specify multiple fields as read-only. Instead of adding each field explicitly with the `read_only=True` attribute, you may use the shortcut Meta option, `read_only_fields`.

Вы можете указать несколько полей как только для чтения.
Вместо того, чтобы явно добавлять каждое поле с атрибутом `read_only = true

This option should be a list or tuple of field names, and is declared as follows:

Эта опция должна быть списком или кортежом имен полевых имен и объявлен следующим образом:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name']
```

Model fields which have `editable=False` set, and `AutoField` fields will be set to read-only by default, and do not need to be added to the `read_only_fields` option.

Поля моделей, которые имеют edable = false` set, и поля `autofield` будут установлены только для чтения по умолчанию, и не нужно добавлять в опцию` read_only_fields.

---

**Note**: There is a special-case where a read-only field is part of a `unique_together` constraint at the model level. In this case the field is required by the serializer class in order to validate the constraint, but should also not be editable by the user.

** ПРИМЕЧАНИЕ **: Существует специальная сторона, где поле только для чтения является частью ограничения `уникально_together` на уровне модели.
В этом случае поле требуется классом Serializer для проверки ограничения, но также не должно быть редактировано пользователем.

The right way to deal with this is to specify the field explicitly on the serializer, providing both the `read_only=True` and `default=…` keyword arguments.

Правильный способ справиться с этим - явно указать поле в сериализаторе, предоставляя как `read_only = true`, так и` default =… `аргументы ключевых слов.

One example of this is a read-only relation to the currently authenticated `User` which is `unique_together` with another identifier. In this case you would declare the user field like so:

Одним из примеров этого является связь только для чтения к нынешнему аутентифицированному «пользователю», который является `inistry_together` с другим идентификатором.
В этом случае вы объявите поле пользователя так:

```
user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
```

Please review the [Validators Documentation](/api-guide/validators/) for details on the [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) and [CurrentUserDefault](/api-guide/validators/#currentuserdefault) classes.

Пожалуйста, просмотрите [документацию Validators] (/API-Guide/Validators/) для получения подробной информации о [UniquetogetherSetherValidator] (/API-Guide/Validators/#UniqueTogetherSerDator) и [CurrentUserDefault] (/API-Guide/validators/#CurrentUserFault)
Анкет

---

## Additional keyword arguments

## Дополнительные аргументы ключевых слов

There is also a shortcut allowing you to specify arbitrary additional keyword arguments on fields, using the `extra_kwargs` option. As in the case of `read_only_fields`, this means you do not need to explicitly declare the field on the serializer.

Существует также ярлык, позволяющий указать произвольные дополнительные аргументы ключевых слов в полях, используя опцию aucepl_kwargs.
Как и в случае с `read_only_fields`, это означает, что вам не нужно явно объявлять поле на сериализаторе.

This option is a dictionary, mapping field names to a dictionary of keyword arguments. For example:

Этот вариант является словарем, сопоставляющим имена поля в словарь аргументов ключевых слов.
Например:

```
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
```

Please keep in mind that, if the field has already been explicitly declared on the serializer class, then the `extra_kwargs` option will be ignored.

Пожалуйста, имейте в виду, что, если поле уже было явно объявлено в классе сериализатора, то опция `extra_kwargs будет игнорирована.

## Relational fields

## Реляционные поля

When serializing model instances, there are a number of different ways you might choose to represent relationships.  The default representation for `ModelSerializer` is to use the primary keys of the related instances.

При сериализации модельных экземпляров есть ряд различных способов представления отношений.
Представление по умолчанию для `modelerializer` - использовать основные ключи связанных экземпляров.

Alternative representations include serializing using hyperlinks, serializing complete nested representations, or serializing with a custom representation.

Альтернативные представления включают сериализацию с использованием гиперссылок, сериализацию полных вложенных представлений или сериализацию с пользовательским представлением.

For full details see the [serializer relations](relations.md) documentation.

Для получения полной информации см. Документацию [Serializer Relations] (Ontations.md).

## Customizing field mappings

## Настройка полевых отображений

The ModelSerializer class also exposes an API that you can override in order to alter how serializer fields are automatically determined when instantiating the serializer.

Класс моделейализатора также обнаруживает API, который вы можете переопределить, чтобы изменить то, как поля сериализатора автоматически определяются при создании сериализатора.

Normally if a `ModelSerializer` does not generate the fields you need by default then you should either add them to the class explicitly, or simply use a regular `Serializer` class instead. However in some cases you may want to create a new base class that defines how the serializer fields are created for any given model.

Обычно, если `modelerializer` не генерирует необходимые поля, которые вам нужны по умолчанию, вы должны либо явно добавить их в класс, либо просто использовать обычный класс` serializer 'вместо этого.
Однако в некоторых случаях вы можете создать новый базовый класс, который определяет, как создаются поля сериализатора для любой данной модели.

### `.serializer_field_mapping`

### `.serializer_field_mapping`

A mapping of Django model fields to REST framework serializer fields. You can override this mapping to alter the default serializer fields that should be used for each model field.

Сопоставление поля модели Django с полями сериализатора REST.
Вы можете переопределить это отображение, чтобы изменить поля сериализатора по умолчанию, которые следует использовать для каждого поля модели.

### `.serializer_related_field`

### `.serializer_related_field`

This property should be the serializer field class, that is used for relational fields by default.

Это свойство должно быть полевым классом сериализатора, который используется для реляционных полей по умолчанию.

For `ModelSerializer` this defaults to `serializers.PrimaryKeyRelatedField`.

Для `modelerializer` это по умолчанию« сериализаторам.primarykeyrelated ».

For `HyperlinkedModelSerializer` this defaults to `serializers.HyperlinkedRelatedField`.

Для `HyperlinkedModelserializer` это по умолчанию« serializers.hyperlinkedRelated ».

### `.serializer_url_field`

### `.serializer_url_field`

The serializer field class that should be used for any `url` field on the serializer.

Класс поля сериализатора, который следует использовать для любого `url` поля на сериализаторе.

Defaults to `serializers.HyperlinkedIdentityField`

По умолчанию «serializers.hyperlinkedidentityfield»

### `.serializer_choice_field`

### `.serializer_choice_field`

The serializer field class that should be used for any choice fields on the serializer.

Класс поля сериализатора, который должен использоваться для любых полей выбора на сериализаторе.

Defaults to `serializers.ChoiceField`

По умолчанию в `serializers.choicefield`

### The field_class and field_kwargs API

### API Field_class и Field_kwargs

The following methods are called to determine the class and keyword arguments for each field that should be automatically included on the serializer. Each of these methods should return a two tuple of `(field_class, field_kwargs)`.

Следующие методы вызываются для определения аргументов класса и ключевых слов для каждого поля, которые должны быть автоматически включены в сериализатор.
Каждый из этих методов должен вернуть два кортежа `(field_class, field_kwargs)`.

### `.build_standard_field(self, field_name, model_field)`

### `.build_standard_field (self, field_name, model_field)`

Called to generate a serializer field that maps to a standard model field.

Вызвано для создания поле сериализатора, которое отображает в стандартном поле модели.

The default implementation returns a serializer class based on the `serializer_field_mapping` attribute.

Реализация по умолчанию возвращает класс Serializer на основе атрибута `serializer_field_mapping`.

### `.build_relational_field(self, field_name, relation_info)`

### `.build_relational_field (self, field_name, nection_info)`

Called to generate a serializer field that maps to a relational model field.

Призван генерировать поле сериализатора, которое отображает в поле реляционной модели.

The default implementation returns a serializer class based on the `serializer_related_field` attribute.

Реализация по умолчанию возвращает класс Serializer на основе атрибута `serializer_related_field`.

The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.

Аргумент `neacht_info` - это названный кортеж, который содержит` model_field`, `indive_model`,` to_many` и `Has_through_model` свойства.

### `.build_nested_field(self, field_name, relation_info, nested_depth)`

### `.build_nest_field (self, field_name, nection_info, nested_depth)`

Called to generate a serializer field that maps to a relational model field, when the `depth` option has been set.

Призван для создания поля сериализатора, которое отображает в поле реляционной модели, когда была установлена параметр «глубины».

The default implementation dynamically creates a nested serializer class based on either `ModelSerializer` or `HyperlinkedModelSerializer`.

Реализация по умолчанию динамически создает вложенный класс сериализатора, основанный либо на `modelseRializer`, либо` HyperlinkedModelserializer '.

The `nested_depth` will be the value of the `depth` option, minus one.

`Nested_depth` будет значением опции« глубины », минус один.

The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.

Аргумент `neacht_info` - это названный кортеж, который содержит` model_field`, `indive_model`,` to_many` и `Has_through_model` свойства.

### `.build_property_field(self, field_name, model_class)`

### `.build_property_field (self, field_name, model_class)`

Called to generate a serializer field that maps to a property or zero-argument method on the model class.

Вызвано для генерации поля сериализатора, которое отображает свой свойство или метод нулевого аргумента в классе модели.

The default implementation returns a `ReadOnlyField` class.

Реализация по умолчанию возвращает класс `readonlyfield`.

### `.build_url_field(self, field_name, model_class)`

### `.build_url_field (self, field_name, model_class)`

Called to generate a serializer field for the serializer's own `url` field. The default implementation returns a `HyperlinkedIdentityField` class.

Призван генерировать поле сериализатора для собственного поля сериализатора.
Реализация по умолчанию возвращает класс `HyperlinkedIdentityfield`.

### `.build_unknown_field(self, field_name, model_class)`

### `.build_unknown_field (self, field_name, model_class)`

Called when the field name did not map to any model field or model property.
The default implementation raises an error, although subclasses may customize this behavior.

Вызовов, когда имя поля не отображалось ни в каком поле модели или свойства модели.
Реализация по умолчанию повышает ошибку, хотя подклассы могут настроить это поведение.

---

# HyperlinkedModelSerializer

# HyperlinkedModelserializer

The `HyperlinkedModelSerializer` class is similar to the `ModelSerializer` class except that it uses hyperlinks to represent relationships, rather than primary keys.

Класс `HyperlinkedModelserializer` аналогичен классу` modelerializer ', за исключением того, что он использует гиперссылки для представления отношений, а не первичных ключей.

By default the serializer will include a `url` field instead of a primary key field.

По умолчанию сериализатор будет включать в себя поле `url 'вместо первичного поля ключа.

The url field will be represented using a `HyperlinkedIdentityField` serializer field, and any relationships on the model will be represented using a `HyperlinkedRelatedField` serializer field.

Поле URL будет представлено с использованием поля сериализатора «HyperlinkedIdentityfield», и любые отношения на модели будут представлены с использованием поля сериализатора `‘ HyperlinkedRelated`.

You can explicitly include the primary key by adding it to the `fields` option, for example:

Вы можете явно включить первичный ключ, добавив его в опцию «Поля», например:

```
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'account_name', 'users', 'created']
```

## Absolute and relative URLs

## абсолютные и относительные URL -адреса

When instantiating a `HyperlinkedModelSerializer` you must include the current
`request` in the serializer context, for example:

При создании `‘ HyperlinkedModelserializer 'вы должны включить текущий
`Запрос` в контексте сериализатора, например:

```
serializer = AccountSerializer(queryset, context={'request': request})
```

Doing so will ensure that the hyperlinks can include an appropriate hostname,
so that the resulting representation uses fully qualified URLs, such as:

Это гарантирует, что гиперссылки могут включать подходящее имя хоста,
так что полученное представление использует полностью квалифицированные URL -адреса, такие как:

```
http://api.example.com/accounts/1/
```

Rather than relative URLs, such as:

А не относительные URL, такие как:

```
/accounts/1/
```

If you *do* want to use relative URLs, you should explicitly pass `{'request': None}`
in the serializer context.

Если вы * хотите * использовать относительные URL -адреса, вы должны явно передать `{'request': none}`
В контексте сериализатора.

## How hyperlinked views are determined

##, как определяются гиперссылки

There needs to be a way of determining which views should be used for hyperlinking to model instances.

Должен быть способ определить, какие представления следует использовать для гиперлизма для модельных экземпляров.

By default hyperlinks are expected to correspond to a view name that matches the style `'{model_name}-detail'`, and looks up the instance by a `pk` keyword argument.

Ожидается, что гиперссылки по умолчанию будут соответствовать имени представления, которое соответствует стилю `'{model_name} -detail'`' и поиск экземпляра с помощью аргумента ключевого слова` pk`.

You can override a URL field view name and lookup field by using either, or both of, the `view_name` and `lookup_field` options in the `extra_kwargs` setting, like so:

Вы можете переопределить имя и поле зрения и поля поиска URL, используя варианты или оба из оба из параметров `view_name` и` lookup_field` в настройке euceple_kwargs`, например, так:

```
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['account_url', 'account_name', 'users', 'created']
        extra_kwargs = {
            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'users': {'lookup_field': 'username'}
        }
```

Alternatively you can set the fields on the serializer explicitly. For example:

В качестве альтернативы вы можете явно установить поля на сериализатор.
Например:

```
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts',
        lookup_field='slug'
    )
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = ['url', 'account_name', 'users', 'created']
```

---

**Tip**: Properly matching together hyperlinked representations and your URL conf can sometimes be a bit fiddly. Printing the `repr` of a `HyperlinkedModelSerializer` instance is a particularly useful way to inspect exactly which view names and lookup fields the relationships are expected to map too.

** Совет **: Правильно сопоставить вместе гиперссыщенные представления, и ваш URL Conf иногда может быть немного неудобным.
Печать `repr` экземпляра` ’HyperlinkedModelserializer` - особенно полезный способ точно проверить, какие имена и поля поиска и поля поиска, как ожидается, также будут отображаться.

---

## Changing the URL field name

## Изменение имени поля URL

The name of the URL field defaults to 'url'.  You can override this globally, by using the `URL_FIELD_NAME` setting.

Имя поля URL по умолчанию «URL».
Вы можете переопределить это во всем мире, используя настройку `url_field_name`.

---

# ListSerializer

# ListSerializer

The `ListSerializer` class provides the behavior for serializing and validating multiple objects at once. You won't *typically* need to use `ListSerializer` directly, but should instead simply pass `many=True` when instantiating a serializer.

Класс `listserializer 'обеспечивает поведение для сериализации и проверки нескольких объектов одновременно.
Вам не нужно *, как правило, * необходимо использовать `listSerializer 'напрямую, но вместо этого следует просто пройти` mary = true` при создании сериализатора.

When a serializer is instantiated and `many=True` is passed, a `ListSerializer` instance will be created. The serializer class then becomes a child of the parent `ListSerializer`

Когда сериализатор создается и пройден `mary = true
Затем класс сериализатора становится ребенком родителя `listserializer

The following argument can also be passed to a `ListSerializer` field or a serializer that is passed `many=True`:

Следующий аргумент также может быть передан в поле «Listserializer» или сериализатор, который передается `mysome = true`:

### `allow_empty`

### `allow_empty`

This is `True` by default, but can be set to `False` if you want to disallow empty lists as valid input.

Это «true» по умолчанию, но может быть установлено на `false`, если вы хотите запретить пустые списки как действительный ввод.

### `max_length`

### `max_length`

This is `None` by default, but can be set to a positive integer if you want to validates that the list contains no more than this number of elements.

Это «нет» по умолчанию, но может быть установлено на положительное целое число, если вы хотите подтвердить, что список содержит не больше этого количества элементов.

### `min_length`

### `min_length`

This is `None` by default, but can be set to a positive integer if you want to validates that the list contains no fewer than this number of elements.

Это «нет» по умолчанию, но может быть установлено на положительное целое число, если вы хотите подтвердить, что список содержит не меньше, чем это количество элементов.

### Customizing `ListSerializer` behavior

### Настройка `listserializer` поведение

There *are* a few use cases when you might want to customize the `ListSerializer` behavior. For example:

Есть * несколько вариантов использования, когда вы можете настроить поведение `listserializer.
Например:

* You want to provide particular validation of the lists, such as checking that one element does not conflict with another element in a list.
* You want to customize the create or update behavior of multiple objects.

* Вы хотите предоставить особую проверку списков, например, проверка того, что один элемент не противоречит другому элементу в списке.
* Вы хотите настроить поведение создать или обновить несколько объектов.

For these cases you can modify the class that is used when `many=True` is passed, by using the `list_serializer_class` option on the serializer `Meta` class.

Для этих случаев вы можете изменить класс, который используется, когда передается `mary = true`, используя опцию` list_serializer_class` в классе Serializer `meta`.

For example:

Например:

```
class CustomListSerializer(serializers.ListSerializer):
    ...

class CustomSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = CustomListSerializer
```

#### Customizing multiple create

#### Настройка нескольких созданий

The default implementation for multiple object creation is to simply call `.create()` for each item in the list. If you want to customize this behavior, you'll need to customize the `.create()` method on `ListSerializer` class that is used when `many=True` is passed.

Реализация по умолчанию для создания нескольких объектов заключается в том, чтобы просто вызовать `.create ()` для каждого элемента в списке.
Если вы хотите настроить это поведение, вам нужно настроить метод `.create ()` на классе `listserializer`, который используется, когда проходит` mary = true`.

For example:

Например:

```
class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [Book(**item) for item in validated_data]
        return Book.objects.bulk_create(books)

class BookSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = BookListSerializer
```

#### Customizing multiple update

#### Настройка нескольких обновлений

By default the `ListSerializer` class does not support multiple updates. This is because the behavior that should be expected for insertions and deletions is ambiguous.

По умолчанию класс `ListSerializer 'не поддерживает несколько обновлений.
Это связано с тем, что поведение, которое следует ожидать для вставки и удалений, является неоднозначным.

To support multiple updates you'll need to do so explicitly. When writing your multiple update code make sure to keep the following in mind:

Чтобы поддержать несколько обновлений, вам понадобится это явно.
При написании вашего кода с несколькими обновлениями обязательно помните о следующем:

* How do you determine which instance should be updated for each item in the list of data?
* How should insertions be handled? Are they invalid, or do they create new objects?
* How should removals be handled? Do they imply object deletion, or removing a relationship? Should they be silently ignored, or are they invalid?
* How should ordering be handled? Does changing the position of two items imply any state change or is it ignored?

* Как вы определяете, какой экземпляр должен быть обновлен для каждого элемента в списке данных?
* Как следует обрабатывать вставки?
Они недействительны, или они создают новые объекты?
* Как следует обращаться с удалением?
Они подразумевают удаление объекта или удаление отношений?
Должны ли их молча игнорировать, или они недействительны?
* Как следует обрабатывать заказа?
Подразумевает ли изменение позиции двух элементов какое -либо изменение состояния или его игнорируют?

You will need to add an explicit `id` field to the instance serializer. The default implicitly-generated `id` field is marked as `read_only`. This causes it to be removed on updates. Once you declare it explicitly, it will be available in the list serializer's `update` method.

Вам нужно будет добавить явное поле «id` в сериализатор экземпляра».
Поле по умолчанию неявно сгенерированное `id` по поле помечено как` read_only`.
Это приводит к удалению его в обновлениях.
После того, как вы заявите это явно, он будет доступен в методе «Обновление» Serializer.

Here's an example of how you might choose to implement multiple updates:

Вот пример того, как вы можете внедрить несколько обновлений:

```
class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret

class BookSerializer(serializers.Serializer):
    # We need to identify elements in the list using their primary key,
    # so use a writable field here, rather than the default which would be read-only.
    id = serializers.IntegerField()
    ...

    class Meta:
        list_serializer_class = BookListSerializer
```

It is possible that a third party package may be included alongside the 3.1 release that provides some automatic support for multiple update operations, similar to the `allow_add_remove` behavior that was present in REST framework 2.

Вполне возможно, что сторонний пакет может быть включен вместе с выпуском 3.1, который обеспечивает некоторую автоматическую поддержку для нескольких операций обновления, аналогично поведению `alluct_add_remove`, которое присутствовало в Framework 2 REST 2.

#### Customizing ListSerializer initialization

#### Настройка инициализации ListSerializer

When a serializer with `many=True` is instantiated, we need to determine which arguments and keyword arguments should be passed to the `.__init__()` method for both the child `Serializer` class, and for the parent `ListSerializer` class.

Когда сериализатор с «многими = true» создан экземпляр, нам необходимо определить, какие аргументы и аргументы ключевых слов должны быть переданы методу `.__ __p __ ()` как для класса Serializer, так и для родителей `listserializer`
Анкет

The default implementation is to pass all arguments to both classes, except for `validators`, and any custom keyword arguments, both of which are assumed to be intended for the child serializer class.

Реализация по умолчанию состоит в том, чтобы передавать все аргументы в обоих классов, за исключением «валидаторов», и любые пользовательские аргументы ключевых слов, которые предполагаются для класса сериализатора детей.

Occasionally you might need to explicitly specify how the child and parent classes should be instantiated when `many=True` is passed. You can do so by using the `many_init` class method.

Время от времени вам может придется явно указать, как должны быть созданы классы ребенка и родителя, когда проходит `mary = true.
Вы можете сделать это, используя метод класса `many_init`.

```
@classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return CustomListSerializer(*args, **kwargs)
```

---

# BaseSerializer

# BaseSerializer

`BaseSerializer` class that can be used to easily support alternative serialization and deserialization styles.

`Class класс BaseSerializer, который может быть использован для легкой поддержки альтернативной сериализации и стилей десериализации.

This class implements the same basic API as the `Serializer` class:

Этот класс реализует тот же базовый API, что и класс `serializer`:

* `.data` - Returns the outgoing primitive representation.
* `.is_valid()` - Deserializes and validates incoming data.
* `.validated_data` - Returns the validated incoming data.
* `.errors` - Returns any errors during validation.
* `.save()` - Persists the validated data into an object instance.

* `.data` - возвращает исходящее примитивное представление.
* `.is_valid ()` - десериализует и проверяет входящие данные.
* `.validated_data` - Возвращает проверенные входящие данные.
* `.errors` - возвращает любые ошибки во время проверки.
* `.save ()` - сохраняет проверенные данные в экземпляр объекта.

There are four methods that can be overridden, depending on what functionality you want the serializer class to support:

Есть четыре метода, которые можно переопределить, в зависимости от того, какую функциональность вы хотите, чтобы класс Serializer поддерживал:

* `.to_representation()` - Override this to support serialization, for read operations.
* `.to_internal_value()` - Override this to support deserialization, for write operations.
* `.create()` and `.update()` - Override either or both of these to support saving instances.

* `.to_representation ()` - переопределить это, чтобы поддержать сериализацию, для операций чтения.
* `.to_internal_value ()` - переопределить это, чтобы поддержать десериализацию, для операций записи.
* `.create ()` и `.update ()` - переопределить один или оба из них для поддержки сохранения экземпляров.

Because this class provides the same interface as the `Serializer` class, you can use it with the existing generic class-based views exactly as you would for a regular `Serializer` or `ModelSerializer`.

Поскольку этот класс обеспечивает тот же интерфейс, что и класс `serializer ', вы можете использовать его с существующими общими представлениями на основе классов точно так же, как и для обычного` serializer' или `modelserializer '.

The only difference you'll notice when doing so is the `BaseSerializer` classes will not generate HTML forms in the browsable API. This is because the data they return does not include all the field information that would allow each field to be rendered into a suitable HTML input.

Единственная разница, которую вы заметите при этом, - это классы `baseserializer. Не генерируют HTML -формы в API -файлах.
Это связано с тем, что данные, которые они возвращают, не включают всю информацию поля, которая позволила бы каждому полю быть отображенным в подходящий HTML -вход.

#### Read-only `BaseSerializer` classes

#### credt-only `caseserializer` классы

To implement a read-only serializer using the `BaseSerializer` class, we just need to override the `.to_representation()` method. Let's take a look at an example using a simple Django model:

Чтобы реализовать сериализатор только для чтения с использованием класса `baseerializer ', нам просто нужно переопределить метод .to_representation ()`.
Давайте посмотрим на пример, используя простую модель Django:

```
class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()
```

It's simple to create a read-only serializer for converting `HighScore` instances into primitive data types.

Это просто создать сериализатор только для чтения для преобразования экземпляров `Highscore в примитивные типы данных.

```
class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }
```

We can now use this class to serialize single `HighScore` instances:

Теперь мы можем использовать этот класс для сериализации одиночных экземпляров `Highscore`:

```
@api_view(['GET'])
def high_score(request, pk):
    instance = HighScore.objects.get(pk=pk)
    serializer = HighScoreSerializer(instance)
    return Response(serializer.data)
```

Or use it to serialize multiple instances:

Или используйте его для сериализации нескольких экземпляров:

```
@api_view(['GET'])
def all_high_scores(request):
    queryset = HighScore.objects.order_by('-score')
    serializer = HighScoreSerializer(queryset, many=True)
    return Response(serializer.data)
```

#### Read-write `BaseSerializer` classes

#### Read-write `caseserializer` классы

To create a read-write serializer we first need to implement a `.to_internal_value()` method. This method returns the validated values that will be used to construct the object instance, and may raise a `serializers.ValidationError` if the supplied data is in an incorrect format.

Чтобы создать сериализатор для чтения-записи, нам сначала нужно реализовать метод `.to_internal_value ()`.
Этот метод возвращает проверенные значения, которые будут использоваться для построения экземпляра объекта, и может повысить `serializers.validationError`, если предоставленные данные находятся в неправильном формате.

Once you've implemented `.to_internal_value()`, the basic validation API will be available on the serializer, and you will be able to use `.is_valid()`, `.validated_data` and `.errors`.

После реализации `.to_internal_value ()`, базовый API проверки будет доступен на сериализаторе, и вы сможете использовать `.is_valid ()`, `.validated_data` и` .errors`.

If you want to also support `.save()` you'll need to also implement either or both of the `.create()` and `.update()` methods.

Если вы хотите также поддержать `.save ()` вам также нужно также реализовать один или оба метода `.create ()` и `.update ()`.

Here's a complete example of our previous `HighScoreSerializer`, that's been updated to support both read and write operations.

Вот полный пример нашего предыдущего «Highscoreerializer», который был обновлен для поддержки как операций чтения, так и записи.

```
class HighScoreSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')

        # Perform the data validation.
        if not score:
            raise serializers.ValidationError({
                'score': 'This field is required.'
            })
        if not player_name:
            raise serializers.ValidationError({
                'player_name': 'This field is required.'
            })
        if len(player_name) > 10:
            raise serializers.ValidationError({
                'player_name': 'May not be more than 10 characters.'
            })

		# Return the validated values. This will be available as
		# the `.validated_data` property.
        return {
            'score': int(score),
            'player_name': player_name
        }

    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }

    def create(self, validated_data):
        return HighScore.objects.create(**validated_data)
```

#### Creating new base classes

#### Создание новых базовых классов

The `BaseSerializer` class is also useful if you want to implement new generic serializer classes for dealing with particular serialization styles, or for integrating with alternative storage backends.

Класс `baseerializer также полезен, если вы хотите внедрить новые классы Generic Serializer для борьбы с конкретными стилями сериализации или для интеграции с альтернативными бэкэндами хранения.

The following class is an example of a generic serializer that can handle coercing arbitrary complex objects into primitive representations.

Следующий класс является примером общего сериализатора, который может обрабатывать принудительные сложные объекты в примитивные представления.

```
class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_representation(self, instance):
        output = {}
        for attribute_name in dir(instance):
            attribute = getattr(instance, attribute_name)
            if attribute_name.startswith('_'):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [
                    self.to_representation(item) for item in attribute
                ]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {
                    str(key): self.to_representation(value)
                    for key, value in attribute.items()
                }
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)
        return output
```

---

# Advanced serializer usage

# Усовершенствованное использование сериализатора

## Overriding serialization and deserialization behavior

## Перепроячая поведение сериализации и десериализации

If you need to alter the serialization or deserialization behavior of a serializer class, you can do so by overriding the `.to_representation()` or `.to_internal_value()` methods.

Если вам необходимо изменить поведение сериализации или десериализации класса сериализатора, вы можете сделать это, переопределив методы `.to_representation ()` или `.to_internal_value ()`.

Some reasons this might be useful include...

Некоторые причины, по которым это может быть полезно, включают ...

* Adding new behavior for new serializer base classes.
* Modifying the behavior slightly for an existing class.
* Improving serialization performance for a frequently accessed API endpoint that returns lots of data.

* Добавление нового поведения для новых классов базовых сериализаторов.
* Слегка изменение поведения для существующего класса.
* Улучшение производительности сериализации для часто доступной конечной точки API, которая возвращает много данных.

The signatures for these methods are as follows:

Подписи для этих методов следующие:

#### `.to_representation(self, instance)`

#### `.to_representation (self, экземпляр)`

Takes the object instance that requires serialization, and should return a primitive representation. Typically this means returning a structure of built-in Python datatypes. The exact types that can be handled will depend on the render classes you have configured for your API.

Принимает экземпляр объекта, который требует сериализации, и должен вернуть примитивное представление.
Как правило, это означает возврат структуры встроенных данных Python.
Точные типы, которые можно обрабатывать, будут зависеть от классов рендеринга, которые вы настроены для вашего API.

May be overridden in order to modify the representation style. For example:

Может быть переопределен, чтобы изменить стиль представления.
Например:

```
def to_representation(self, instance):
    """Convert `username` to lowercase."""
    ret = super().to_representation(instance)
    ret['username'] = ret['username'].lower()
    return ret
```

#### `.to_internal_value(self, data)`

#### `.to_internal_value (self, data)`

Takes the unvalidated incoming data as input and should return the validated data that will be made available as `serializer.validated_data`. The return value will also be passed to the `.create()` or `.update()` methods if `.save()` is called on the serializer class.

Принимает неиспользованные входящие данные в качестве входных данных и должен вернуть проверенные данные, которые будут доступны как `serializer.validated_data`.
Возвратное значение также будет передано в методы `.create ()` или `.

If any of the validation fails, then the method should raise a `serializers.ValidationError(errors)`. The `errors` argument should be a dictionary mapping field names (or `settings.NON_FIELD_ERRORS_KEY`) to a list of error messages. If you don't need to alter deserialization behavior and instead want to provide object-level validation, it's recommended that you instead override the [`.validate()`](#object-level-validation) method.

Если какая -либо из проверки не удается, то метод должен поднять `serializers.validationError (ошибки)`.
Аргументом «ошибки» должен быть именами поля сопоставления словаря (или `futs.non_field_errors_key`) в список сообщений об ошибках.
Если вам не нужно изменять поведение десериализации и вместо этого вы хотите обеспечить проверку на уровне объекта, рекомендуется вместо этого переопределить метод [`.validate ()`] (#validation).

The `data` argument passed to this method will normally be the value of `request.data`, so the datatype it provides will depend on the parser classes you have configured for your API.

Аргумент «Data», переданный этому методу, обычно будет значением `request.data`, поэтому предоставленный он датт, который он предоставляет, будет зависеть от классов анализатора, которые вы настроены для вашего API.

## Serializer Inheritance

## Наследство сериализатора

Similar to Django forms, you can extend and reuse serializers through inheritance. This allows you to declare a common set of fields or methods on a parent class that can then be used in a number of serializers. For example,

Подобно формам Django, вы можете расширить и повторно использовать сериализаторы через наследство.
Это позволяет вам объявить общий набор полей или методов на родительском классе, которые затем можно использовать в ряде сериализаторов.
Например,

```
class MyBaseSerializer(Serializer):
    my_field = serializers.CharField()

    def validate_my_field(self, value):
        ...

class MySerializer(MyBaseSerializer):
    ...
```

Like Django's `Model` and `ModelForm` classes, the inner `Meta` class on serializers does not implicitly inherit from it's parents' inner `Meta` classes. If you want the `Meta` class to inherit from a parent class you must do so explicitly. For example:

Как и классы Django «Model» и «Modelform», внутренний класс Meta` на сериалах неявно наследует от своих родителей.
Если вы хотите, чтобы класс Meta` унаследовал от родительского класса, вы должны сделать это явно.
Например:

```
class AccountSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        model = Account
```

Typically we would recommend *not* using inheritance on inner Meta classes, but instead declaring all options explicitly.

Как правило, мы рекомендуем * не * использовать наследование на внутренних классах мета, а вместо этого явно объявляя все варианты.

Additionally, the following caveats apply to serializer inheritance:

Кроме того, следующие предостережения применяются к наследованию сериализатора:

* Normal Python name resolution rules apply. If you have multiple base classes that declare a `Meta` inner class, only the first one will be used. This means the child’s `Meta`, if it exists, otherwise the `Meta` of the first parent, etc.
* It’s possible to declaratively remove a `Field` inherited from a parent class by setting the name to be `None` on the subclass.
    ```
    class MyBaseSerializer(ModelSerializer):
          my_field = serializers.CharField()
    
      class MySerializer(MyBaseSerializer):
          my_field = None
    ```However, you can only use this technique to opt out from a field defined declaratively by a parent class; it won’t prevent the `ModelSerializer` from generating a default field. To opt-out from default fields, see [Specifying which fields to include](#specifying-which-fields-to-include).

* Применяются нормальные правила разрешения имени питона.
Если у вас есть несколько базовых классов, которые объявляют внутренний класс «мета», будет использоваться только первый.
Это означает, что ребенок «мета», если он существует, в противном случае «мета» первого родителя и т. Д.
* Можно объявить «Поле», унаследованное от родительского класса, установив имя как «нет» на подкласс.
`` `
класс mybaseSerializer (ModelseRializer):
my_field = serializers.charfield ()
класс Myserializer (mybaseSerializer):
my_field = нет
`` `Однако вы можете использовать только эту технику, чтобы отказаться от поля, определенного декларативным образом родительским классом;
Это не предотвратит создание поля по умолчанию.
Чтобы отказаться от полей по умолчанию, см. [Указание того, какие поля включают] (#указание, которые будут в том, что в них включают).

## Dynamically modifying fields

## Динамически модифицирующие поля

Once a serializer has been initialized, the dictionary of fields that are set on the serializer may be accessed using the `.fields` attribute.  Accessing and modifying this attribute allows you to dynamically modify the serializer.

После того, как сериализатор был инициализирован, можно получить к словарю полей, установленных на сериализаторе с использованием атрибута .fields '.
Доступ и изменение этого атрибута позволяет динамически модифицировать сериализатор.

Modifying the `fields` argument directly allows you to do interesting things such as changing the arguments on serializer fields at runtime, rather than at the point of declaring the serializer.

Изменение аргумента «полей» напрямую позволяет вам делать интересные вещи, такие как изменение аргументов на полях сериализатора во время выполнения, а не в точке объявления сериализатора.

### Example

### Пример

For example, if you wanted to be able to set which fields should be used by a serializer at the point of initializing it, you could create a serializer class like so:

Например, если вы хотите иметь возможность установить, какие поля следует использовать сериализатором в точке его инициализации, вы можете создать класс сериализатора, как SO:

```
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
```

This would then allow you to do the following:

Это позволило бы вам сделать следующее:

```
>>> class UserSerializer(DynamicFieldsModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ['id', 'username', 'email']
>>>
>>> print(UserSerializer(user))
{'id': 2, 'username': 'jonwatts', 'email': 'jon@example.com'}
>>>
>>> print(UserSerializer(user, fields=('id', 'email')))
{'id': 2, 'email': 'jon@example.com'}
```

## Customizing the default fields

## Настройка полей по умолчанию

REST framework 2 provided an API to allow developers to override how a `ModelSerializer` class would automatically generate the default set of fields.

REST Framework 2 предоставил API, чтобы позволить разработчикам переопределить, как класс `modelerializer 'автоматически генерирует набор по умолчанию полей.

This API included the `.get_field()`, `.get_pk_field()` and other methods.

Этот API включал `.get_field ()`, `.get_pk_field ()` и другие методы.

Because the serializers have been fundamentally redesigned with 3.0 this API no longer exists. You can still modify the fields that get created but you'll need to refer to the source code, and be aware that if the changes you make are against private bits of API then they may be subject to change.

Поскольку сериализаторы были в корне переработаны с 3,0, этот API больше не существует.
Вы по -прежнему можете изменить созданные поля, но вам нужно обратиться к исходному коду и помнить, что если изменения, которые вы вносят, противостоят частным битам API, они могут быть изменены.

---

# Third party packages

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## Django REST marshmallow

## Django Rest Marshmallow

The [django-rest-marshmallow](https://marshmallow-code.github.io/django-rest-marshmallow/) package provides an alternative implementation for serializers, using the python [marshmallow](https://marshmallow.readthedocs.io/en/latest/) library. It exposes the same API as the REST framework serializers, and can be used as a drop-in replacement in some use-cases.

[Django-rest-marshmallow] (https://marshmallow-code.github.io/django-rest-marshmallow/) предоставляет альтернативную реализацию для сериализаторов, используя Python [Marshmallow] (https: //marshmallow.readthedocs
.io/en/last/) библиотека.
Он обнажает тот же API, что и сериализаторы REST Framework, и может использоваться в качестве замены в некоторых случаях использования.

## Serpy

## Serpy

The [serpy](https://github.com/clarkduvall/serpy) package is an alternative implementation for serializers that is built for speed. [Serpy](https://github.com/clarkduvall/serpy) serializes complex datatypes to simple native types. The native types can be easily converted to JSON or any other format needed.

Пакет [serpy] (https://github.com/clarkduvall/serpy) является альтернативной реализацией для сериализаторов, которая создана для скорости.
[Serpy] (https://github.com/clarkduvall/serpy) сериализует сложные данные дата на простые нативные типы.
Нативные типы могут быть легко преобразованы в JSON или в любой другой необходимый формат.

## MongoengineModelSerializer

## mongoenginemodelserializer

The [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) package provides a `MongoEngineModelSerializer` serializer class that supports using MongoDB as the storage layer for Django REST framework.

Пакет [https://github.com/umutbozkurt/django-rest-frame-mongoengine) предоставляет [django-rest-framework-mongoengine] (https://github.com/umutbozkurt/django-rest-framework-mongoengine).

## GeoFeatureModelSerializer

## geofeaturemodelserializer

The [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) package provides a `GeoFeatureModelSerializer` serializer class that supports GeoJSON both for read and write operations.

Пакет [django-rest-framework-gis] (https://github.com/djangonauts/django-rest-framework-gis) предоставляет класс сериализатора «Geofeaturemodelserializer», который поддерживает Geojson для чтения и записи.

## HStoreSerializer

## horsoreerializer

The [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) package provides an `HStoreSerializer` to support [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` model field and its `schema-mode` feature.

В пакете [https://github.com/djangonauts/django-rest-framework) (https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `hStoreSerializer` для поддержки [django-hstore] (https://github.com для поддержки
/djangonauts/django-hstore) `Dictionaryfield's Model Field и его функция« режим схемы ».

## Dynamic REST

## Динамический отдых

The [dynamic-rest](https://github.com/AltSchool/dynamic-rest) package extends the ModelSerializer and ModelViewSet interfaces, adding API query parameters for filtering, sorting, and including / excluding all fields and relationships defined by your serializers.

Пакет [Dynamic-Rest] (https://github.com/altschool/dynamic-rest) расширяет интерфейсы моделейализатора и моделей.
Анкет

## Dynamic Fields Mixin

## Dynamic Fields Mixin

The [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) package provides a mixin to dynamically limit the fields per serializer to a subset specified by an URL parameter.

Пакет [https://github.com/dbrgn/drf-fields) (https://github.com/dbrgn/drf-dynamic) обеспечивает смесин для динамического ограничения поля на сериализатор до подмножества, указанного параметром URL.

## DRF FlexFields

## DRF Flexfields

The [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) package extends the ModelSerializer and ModelViewSet to provide commonly used functionality for dynamically setting fields and expanding primitive fields to nested models, both from URL parameters and your serializer class definitions.

Пакет [drf-flexfields] (https://github.com/rsinger86/drf-flex fields) расширяет модельные модели и модели для обеспечения широко используемых функциональности для поля динамического настройки и расширяющихся примитивных полей на заложенные модели, оба из
Параметры URL и определения вашего класса сериализатора.

## Serializer Extensions

## расширения сериализатора

The [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions)
package provides a collection of tools to DRY up your serializers, by allowing
fields to be defined on a per-view/request basis. Fields can be whitelisted,
blacklisted and child serializers can be optionally expanded.

[Django-rest-framework-serializer-extensions] (https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions)
Пакет предоставляет коллекцию инструментов для высушивания ваших сериалов, позволяя
Поля должны быть определены на основе просмотра/запроса.
Поля могут быть белым списком,
Черные списки и детские сериализаторы могут быть расширены.

## HTML JSON Forms

## html json forms

The [html-json-forms](https://github.com/wq/html-json-forms) package provides an algorithm and serializer for processing `<form>` submissions per the (inactive) [HTML JSON Form specification](https://www.w3.org/TR/html-json-forms/).  The serializer facilitates processing of arbitrarily nested JSON structures within HTML.  For example, `<input name="items[0][id]" value="5">` will be interpreted as `{"items": [{"id": "5"}]}`.

Пакет [html-json-forms] (https://github.com/wq/html-json-forms) предоставляет алгоритм и сериализатор для обработки `<form>` Представки на (неактивную) [HTML JSON Specification]
(https://www.w3.org/tr/html-json-forms/).
Сериализатор облегчает обработку произвольно вложенных структур JSON в HTML.
Например, `<input name =" items [0] [id] "value =" 5 ">` будет интерпретироваться как `{" элементы ": [{" id ":" 5 "}]}`.

## DRF-Base64

## drf-base64

[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64) provides a set of field and model serializers that handles the upload of base64-encoded files.

[Drf-base64] (https://bitbucket.org/levit_scs/drf_base64) предоставляет набор сериалеров поля и модели, которые обрабатывают загрузку файлов Base64-кодировки.

## QueryFields

## QueryFields

[djangorestframework-queryfields](https://djangorestframework-queryfields.readthedocs.io/) allows API clients to specify which fields will be sent in the response via inclusion/exclusion query parameters.

[djangorestframework-queryfields] (https://djangorestframework-queryfields.readthedocs.io/) позволяет клиентам API указывать, какие поля будут отправлены в ответ через параметры включения/исключения.

## DRF Writable Nested

## DRF Записывается

The [drf-writable-nested](https://github.com/beda-software/drf-writable-nested) package provides writable nested model serializer which allows to create/update models with nested related data.

В пакете [DRF-Wriable-nested] (https://github.com/beda-software/drf-wrable-nest) предоставляет сериализатор вложенного модели с записи, который позволяет создавать/обновлять модели с вложенными связанными данными.

## DRF Encrypt Content

## DRF Encrypt Content

The [drf-encrypt-content](https://github.com/oguzhancelikarslan/drf-encrypt-content) package helps you encrypt your data, serialized through ModelSerializer. It also contains some helper functions. Which helps you to encrypt your data.

Пакет [https://github.com/oguzhancelikarslan/drf-encrypt-content) поможет вам зашифровать ваши данные, сериализованные через моделиализатор.
Он также содержит некоторые вспомогательные функции.
Что помогает вам зашифровать ваши данные.