<!-- TRANSLATED by md-translate -->
---

source:

источник:

* serializers.py

* serializers.py

---

# Serializers

# Сериализаторы

> Expanding the usefulness of the serializers is something that we would like to address. However, it's not a trivial problem, and it will take some serious design work.
>
> — Russell Keith-Magee, [Django users group](https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion)

> Расширение полезности сериализаторов - это то, чем мы хотели бы заняться. Однако это не тривиальная проблема, и потребуется серьезная работа над дизайном.
>
> - Russell Keith-Magee, [Django users group](https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion)

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into `JSON`, `XML` or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

Сериализаторы позволяют преобразовывать сложные данные, такие как наборы запросов и экземпляры моделей, в собственные типы данных Python, которые затем могут быть легко преобразованы в `JSON`, `XML` или другие типы содержимого. Сериализаторы также обеспечивают десериализацию, позволяя преобразовывать разобранные данные обратно в сложные типы после предварительной проверки входящих данных.

The serializers in REST framework work very similarly to Django's `Form` and `ModelForm` classes. We provide a `Serializer` class which gives you a powerful, generic way to control the output of your responses, as well as a `ModelSerializer` class which provides a useful shortcut for creating serializers that deal with model instances and querysets.

Сериализаторы в REST framework работают очень похоже на классы Django `Form` и `ModelForm`. Мы предоставляем класс `Serializer`, который дает вам мощный, универсальный способ управления выводом ваших ответов, а также класс `ModelSerializer`, который предоставляет полезный ярлык для создания сериализаторов, работающих с экземплярами моделей и наборами запросов.

## Declaring Serializers

## Объявление сериализаторов

Let's start by creating a simple object we can use for example purposes:

Давайте начнем с создания простого объекта, который мы можем использовать для примера:

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

Мы объявим сериализатор, который мы можем использовать для сериализации и десериализации данных, соответствующих объектам `Comment`.

Declaring a serializer looks very similar to declaring a form:

Объявление сериализатора очень похоже на объявление формы:

```
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Serializing objects

## Сериализация объектов

We can now use `CommentSerializer` to serialize a comment, or list of comments. Again, using the `Serializer` class looks a lot like using a `Form` class.

Теперь мы можем использовать `CommentSerializer` для сериализации комментария или списка комментариев. Опять же, использование класса `Serializer` очень похоже на использование класса `Form`.

```
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
```

At this point we've translated the model instance into Python native datatypes. To finalise the serialization process we render the data into `json`.

На данном этапе мы перевели экземпляр модели в собственные типы данных Python. Чтобы завершить процесс сериализации, мы преобразуем данные в `json`.

```
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
```

## Deserializing objects

## Десериализация объектов

Deserialization is similar. First we parse a stream into Python native datatypes...

Десериализация аналогична. Сначала мы разбираем поток на собственные типы данных Python...

```
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
```

...then we restore those native datatypes into a dictionary of validated data.

затем мы восстанавливаем эти родные типы данных в словарь проверенных данных.

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

Если мы хотим иметь возможность возвращать полные экземпляры объектов на основе проверенных данных, нам необходимо реализовать один или оба метода `.create()` и `.update()`. Например:

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

Если ваши экземпляры объектов соответствуют моделям Django, вы также захотите убедиться, что эти методы сохраняют объект в базе данных. Например, если `Comment` является моделью Django, методы могут выглядеть следующим образом:

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

Теперь при десериализации данных мы можем вызвать `.save()`, чтобы вернуть экземпляр объекта, основанный на проверенных данных.

```
comment = serializer.save()
```

Calling `.save()` will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class:

Вызов `.save()` либо создаст новый экземпляр, либо обновит существующий, в зависимости от того, был ли передан существующий экземпляр при инстанцировании класса сериализатора:

```
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)
```

Both the `.create()` and `.update()` methods are optional. You can implement either none, one, or both of them, depending on the use-case for your serializer class.

Методы `.create()` и `.update()` являются необязательными. Вы можете реализовать либо ни один из них, либо один, либо оба, в зависимости от условий использования вашего класса сериализатора.

#### Passing additional attributes to `.save()`

#### Передача дополнительных атрибутов в `.save()`.

Sometimes you'll want your view code to be able to inject additional data at the point of saving the instance. This additional data might include information like the current user, the current time, or anything else that is not part of the request data.

Иногда вы хотите, чтобы код представления мог вводить дополнительные данные в момент сохранения экземпляра. Эти дополнительные данные могут включать информацию о текущем пользователе, текущем времени или что-нибудь еще, что не является частью данных запроса.

You can do so by including additional keyword arguments when calling `.save()`. For example:

Вы можете сделать это, включив дополнительные аргументы ключевых слов при вызове `.save()`. Например:

```
serializer.save(owner=request.user)
```

Any additional keyword arguments will be included in the `validated_data` argument when `.create()` or `.update()` are called.

Любые дополнительные аргументы ключевых слов будут включены в аргумент `validated_data` при вызове `.create()` или `.update()`.

#### Overriding `.save()` directly.

#### Переопределение `.save()` напрямую.

In some cases the `.create()` and `.update()` method names may not be meaningful. For example, in a contact form we may not be creating new instances, but instead sending an email or other message.

В некоторых случаях имена методов `.create()` и `.update()` могут не иметь смысла. Например, в контактной форме мы можем не создавать новые экземпляры, а отправлять электронное письмо или другое сообщение.

In these cases you might instead choose to override `.save()` directly, as being more readable and meaningful.

В этих случаях вы можете вместо этого переопределить `.save()` напрямую, как более читабельный и осмысленный.

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

Обратите внимание, что в приведенном выше случае нам приходится напрямую обращаться к свойству сериализатора `.validated_data`.

## Validation

## Валидация

When deserializing data, you always need to call `is_valid()` before attempting to access the validated data, or save an object instance. If any validation errors occur, the `.errors` property will contain a dictionary representing the resulting error messages. For example:

При десериализации данных всегда нужно вызывать `is_valid()` перед попыткой получить доступ к проверенным данным или сохранить экземпляр объекта. Если возникнут ошибки валидации, свойство `.errors` будет содержать словарь, представляющий сообщения об ошибках. Например:

```
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
```

Each key in the dictionary will be the field name, and the values will be lists of strings of any error messages corresponding to that field. The `non_field_errors` key may also be present, and will list any general validation errors. The name of the `non_field_errors` key may be customized using the `NON_FIELD_ERRORS_KEY` REST framework setting.

Каждый ключ в словаре будет именем поля, а значения будут списками строк любых сообщений об ошибках, соответствующих этому полю. Также может присутствовать ключ `non_field_errors`, в котором будут перечислены все общие ошибки валидации. Имя ключа `non_field_errors` можно настроить с помощью параметра REST-фреймворка `NON_FIELD_ERRORS_KEY`.

When deserializing a list of items, errors will be returned as a list of dictionaries representing each of the deserialized items.

При десериализации списка элементов ошибки будут возвращены в виде списка словарей, представляющих каждый из десериализованных элементов.

#### Raising an exception on invalid data

#### Возбуждение исключения при недопустимых данных

The `.is_valid()` method takes an optional `raise_exception` flag that will cause it to raise a `serializers.ValidationError` exception if there are validation errors.

Метод `.is_valid()` принимает необязательный флаг `raise_exception`, который заставит его поднять исключение `serializers.ValidationError`, если есть ошибки валидации.

These exceptions are automatically dealt with by the default exception handler that REST framework provides, and will return `HTTP 400 Bad Request` responses by default.

Эти исключения автоматически обрабатываются обработчиком исключений по умолчанию, который предоставляет REST framework, и по умолчанию будут возвращать ответы `HTTP 400 Bad Request`.

```
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

#### Field-level validation

#### Валидация на полевом уровне

You can specify custom field-level validation by adding `.validate_<field_name>` methods to your `Serializer` subclass. These are similar to the `.clean_<field_name>` methods on Django forms.

Вы можете задать пользовательскую валидацию на уровне полей, добавив методы `.validate_<имя_поля>` в подкласс `Serializer`. Они аналогичны методам `.clean_<имя_поля>` в формах Django.

These methods take a single argument, which is the field value that requires validation.

Эти методы принимают единственный аргумент, который является значением поля, требующего проверки.

Your `validate_<field_name>` methods should return the validated value or raise a `serializers.ValidationError`. For example:

Ваши методы `validate_<имя_поля>` должны возвращать проверенное значение или вызывать `serializers.ValidationError`. Например:

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

**Примечание:** Если ваше `<имя_поля>` объявлено в вашем сериализаторе с параметром `required=False`, то этот шаг валидации не будет выполняться, если поле не включено.

---

#### Object-level validation

#### Валидация на уровне объекта

To do any other validation that requires access to multiple fields, add a method called `.validate()` to your `Serializer` subclass. This method takes a single argument, which is a dictionary of field values. It should raise a `serializers.ValidationError` if necessary, or just return the validated values. For example:

Чтобы выполнить любую другую проверку, требующую доступа к нескольким полям, добавьте метод `.validate()` к вашему подклассу `Serializer`. Этот метод принимает единственный аргумент, который является словарем значений полей. При необходимости он должен вызывать `serializers.ValidationError, или просто возвращать проверенные значения. Например:

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

#### Валидаторы

Individual fields on a serializer can include validators, by declaring them on the field instance, for example:

Отдельные поля сериализатора могут включать валидаторы, например, путем объявления их в экземпляре поля:

```
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...
```

Serializer classes can also include reusable validators that are applied to the complete set of field data. These validators are included by declaring them on an inner `Meta` class, like so:

Классы сериализаторов могут также включать многократно используемые валидаторы, которые применяются к полному набору данных поля. Эти валидаторы включаются путем объявления их во внутреннем классе `Meta`, например, так:

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

Для получения дополнительной информации см. документацию [validators](validators.md).

## Accessing the initial data and instance

## Доступ к исходным данным и экземпляру

When passing an initial object or queryset to a serializer instance, the object will be made available as `.instance`. If no initial object is passed then the `.instance` attribute will be `None`.

При передаче исходного объекта или набора запросов экземпляру сериализатора, объект будет доступен как `.instance`. Если начальный объект не передан, то атрибут `.instance` будет иметь значение `None`.

When passing data to a serializer instance, the unmodified data will be made available as `.initial_data`. If the `data` keyword argument is not passed then the `.initial_data` attribute will not exist.

При передаче данных экземпляру сериализатора, немодифицированные данные будут доступны как `.initial_data`. Если аргумент ключевого слова `data` не передан, то атрибут `.initial_data` не будет существовать.

## Partial updates

## Частичные обновления

By default, serializers must be passed values for all required fields or they will raise validation errors. You can use the `partial` argument in order to allow partial updates.

По умолчанию сериализаторам должны передаваться значения для всех обязательных полей, иначе они будут выдавать ошибки валидации. Вы можете использовать аргумент `partial`, чтобы разрешить частичное обновление.

```
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
```

## Dealing with nested objects

## Работа с вложенными объектами

The previous examples are fine for dealing with objects that only have simple datatypes, but sometimes we also need to be able to represent more complex objects, where some of the attributes of an object might not be simple datatypes such as strings, dates or integers.

Предыдущие примеры хорошо подходят для работы с объектами, которые имеют только простые типы данных, но иногда нам также необходимо иметь возможность представлять более сложные объекты, где некоторые атрибуты объекта могут не быть простыми типами данных, такими как строки, даты или целые числа.

The `Serializer` class is itself a type of `Field`, and can be used to represent relationships where one object type is nested inside another.

Класс `Serializer` сам является типом `Field` и может быть использован для представления отношений, в которых один тип объекта вложен в другой.

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

Если вложенное представление может опционально принимать значение `None`, вы должны передать флаг `required=False` вложенному сериализатору.

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Similarly if a nested representation should be a list of items, you should pass the `many=True` flag to the nested serializer.

Аналогично, если вложенное представление должно быть списком элементов, вы должны передать флаг `many=True` в сериализатор вложенных элементов.

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Writable nested representations

## Записываемые вложенные представления

When dealing with nested representations that support deserializing the data, any errors with nested objects will be nested under the field name of the nested object.

При работе с вложенными представлениями, поддерживающими десериализацию данных, любые ошибки с вложенными объектами будут вложены под именем поля вложенного объекта.

```
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid e-mail address.']}, 'created': ['This field is required.']}
```

Similarly, the `.validated_data` property will include nested data structures.

Аналогично, свойство `.validated_data` будет включать в себя вложенные структуры данных.

#### Writing `.create()` methods for nested representations

#### Написание методов `.create()` для вложенных представлений

If you're supporting writable nested representations you'll need to write `.create()` or `.update()` methods that handle saving multiple objects.

Если вы поддерживаете записываемые вложенные представления, вам нужно написать методы `.create()` или `.update()`, которые обрабатывают сохранение нескольких объектов.

The following example demonstrates how you might handle creating a user with a nested profile object.

В следующем примере показано, как можно создать пользователя с вложенным объектом профиля.

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

#### Написание методов `.update()` для вложенных представлений

For updates you'll want to think carefully about how to handle updates to relationships. For example if the data for the relationship is `None`, or not provided, which of the following should occur?

Для обновлений вам необходимо тщательно продумать, как обрабатывать обновления отношений. Например, если данные для отношения `None`, или не предоставлены, что из перечисленного ниже должно произойти?

* Set the relationship to `NULL` in the database.
* Delete the associated instance.
* Ignore the data and leave the instance as it is.
* Raise a validation error.

* Установите для отношения значение `NULL` в базе данных.
* Удалите связанный экземпляр.
* Игнорировать данные и оставить экземпляр как есть.
* Вызвать ошибку валидации.

Here's an example for an `.update()` method on our previous `UserSerializer` class.

Вот пример метода `.update()` для нашего предыдущего класса `UserSerializer`.

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

Поскольку поведение вложенных созданий и обновлений может быть неоднозначным и может требовать сложных зависимостей между связанными моделями, REST framework 3 требует, чтобы вы всегда писали эти методы явно. Методы `ModelSerializer` `.create()` и `.update()` по умолчанию не включают поддержку записываемых вложенных представлений.

There are however, third-party packages available such as [DRF Writable Nested](serializers.md#drf-writable-nested) that support automatic writable nested representations.

Однако существуют сторонние пакеты, такие как [DRF Writable Nested](serializers.md#drf-writable-nested), которые поддерживают автоматические записываемые вложенные представления.

#### Handling saving related instances in model manager classes

#### Обработка сохранения связанных экземпляров в классах менеджера моделей

An alternative to saving multiple related instances in the serializer is to write custom model manager classes that handle creating the correct instances.

Альтернативой сохранению нескольких связанных экземпляров в сериализаторе является написание пользовательских классов менеджера модели, которые занимаются созданием нужных экземпляров.

For example, suppose we wanted to ensure that `User` instances and `Profile` instances are always created together as a pair. We might write a custom manager class that looks something like this:

Например, предположим, мы хотим убедиться, что экземпляры `User` и `Profile` всегда создаются вместе как пара. Мы можем написать пользовательский класс менеджера, который будет выглядеть примерно так:

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

Этот класс менеджера теперь более точно передает, что экземпляры пользователя и профиля всегда создаются одновременно. Наш метод `.create()` в классе сериализатора теперь может быть переписан для использования нового метода менеджера.

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

Подробнее об этом подходе смотрите документацию Django по [менеджерам моделей] (https://docs.djangoproject.com/en/stable/topics/db/managers/), и [этот блогпост об использовании классов моделей и менеджеров] (https://www.dabapps.com/blog/django-models-and-encapsulation/).

## Dealing with multiple objects

## Работа с несколькими объектами

The `Serializer` class can also handle serializing or deserializing lists of objects.

Класс `Serializer` также может обрабатывать сериализацию или десериализацию списков объектов.

#### Serializing multiple objects

#### Сериализация нескольких объектов

To serialize a queryset or list of objects instead of a single object instance, you should pass the `many=True` flag when instantiating the serializer. You can then pass a queryset or list of objects to be serialized.

Чтобы сериализовать кверисет или список объектов вместо одного экземпляра объекта, необходимо передать флаг `many=True` при инстанцировании сериализатора. Затем вы можете передать кверисет или список объектов для сериализации.

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

#### Десериализация нескольких объектов

The default behavior for deserializing multiple objects is to support multiple object creation, but not support multiple object updates. For more information on how to support or customize either of these cases, see the [ListSerializer](#listserializer) documentation below.

Поведение по умолчанию для десериализации нескольких объектов - это поддержка создания нескольких объектов, но не поддержка обновления нескольких объектов. Для получения дополнительной информации о том, как поддержать или настроить любой из этих случаев, см. документацию по [ListSerializer](#listserializer) ниже.

## Including extra context

## Включение дополнительного контекста

There are some cases where you need to provide extra context to the serializer in addition to the object being serialized. One common case is if you're using a serializer that includes hyperlinked relations, which requires the serializer to have access to the current request so that it can properly generate fully qualified URLs.

Бывают случаи, когда вам необходимо предоставить сериализатору дополнительный контекст в дополнение к сериализуемому объекту. Одним из распространенных случаев является использование сериализатора, который включает отношения с гиперссылками, что требует, чтобы сериализатор имел доступ к текущему запросу, чтобы он мог правильно генерировать полностью определенные URL.

You can provide arbitrary additional context by passing a `context` argument when instantiating the serializer. For example:

Вы можете предоставить произвольный дополнительный контекст, передав аргумент `context` при инстанцировании сериализатора. Например:

```
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': 'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
```

The context dictionary can be used within any serializer field logic, such as a custom `.to_representation()` method, by accessing the `self.context` attribute.

Контекстный словарь можно использовать в любой логике поля сериализатора, например, в пользовательском методе `.to_representation()`, обращаясь к атрибуту `self.context`.

---

# ModelSerializer

# ModelSerializer

Often you'll want serializer classes that map closely to Django model definitions.

Часто вам понадобятся классы сериализаторов, которые близко сопоставляются с определениями моделей Django.

The `ModelSerializer` class provides a shortcut that lets you automatically create a `Serializer` class with fields that correspond to the Model fields.

Класс `ModelSerializer` предоставляет ярлык, позволяющий автоматически создать класс `Serializer` с полями, соответствующими полям модели.

**The `ModelSerializer` class is the same as a regular `Serializer` class, except that**:

**Класс `ModelSerializer` такой же, как и обычный класс `Serializer`, за исключением того, что**:

* It will automatically generate a set of fields for you, based on the model.
* It will automatically generate validators for the serializer, such as unique_together validators.
* It includes simple default implementations of `.create()` and `.update()`.

* Он автоматически сгенерирует для вас набор полей на основе модели.
* Он автоматически генерирует валидаторы для сериализатора, такие как валидаторы unique_together.
* Он включает простые реализации по умолчанию `.create()` и `.update()`.

Declaring a `ModelSerializer` looks like this:

Объявление `ModelSerializer` выглядит следующим образом:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

By default, all the model fields on the class will be mapped to a corresponding serializer fields.

По умолчанию все поля модели класса будут отображены на соответствующие поля сериализатора.

Any relationships such as foreign keys on the model will be mapped to `PrimaryKeyRelatedField`. Reverse relationships are not included by default unless explicitly included as specified in the [serializer relations](relations.md) documentation.

Любые отношения, такие как внешние ключи в модели, будут отображены на `PrimaryKeyRelatedField`. Обратные отношения не включаются по умолчанию, если они не включены явно, как указано в документации [serializer relations](relations.md).

#### Inspecting a `ModelSerializer`

#### Проверка `ModelSerializer`.

Serializer classes generate helpful verbose representation strings, that allow you to fully inspect the state of their fields. This is particularly useful when working with `ModelSerializers` where you want to determine what set of fields and validators are being automatically created for you.

Классы сериализаторов генерируют полезные строки представления, которые позволяют полностью просмотреть состояние их полей. Это особенно полезно при работе с `ModelSerializers`, когда вы хотите определить, какой набор полей и валидаторов автоматически создается для вас.

To do so, open the Django shell, using `python manage.py shell`, then import the serializer class, instantiate it, and print the object representation…

Для этого откройте оболочку Django, используя `python manage.py shell`, затем импортируйте класс сериализатора, инстанцируйте его и выведите представление объекта...

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

## Указание полей для включения

If you only want a subset of the default fields to be used in a model serializer, you can do so using `fields` or `exclude` options, just as you would with a `ModelForm`. It is strongly recommended that you explicitly set all fields that should be serialized using the `fields` attribute. This will make it less likely to result in unintentionally exposing data when your models change.

Если вы хотите, чтобы в сериализаторе модели использовалось только подмножество полей по умолчанию, вы можете сделать это с помощью опций `fields` или `exclude`, как и в случае с `ModelForm`. Настоятельно рекомендуется явно задавать все поля, которые должны быть сериализованы, с помощью атрибута `fields`. Это уменьшит вероятность непреднамеренного раскрытия данных при изменении ваших моделей.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

You can also set the `fields` attribute to the special value `'__all__'` to indicate that all fields in the model should be used.

Вы также можете установить для атрибута `fields` специальное значение `'__all__'`, чтобы указать, что должны использоваться все поля в модели.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
```

You can set the `exclude` attribute to a list of fields to be excluded from the serializer.

Вы можете установить атрибут `exclude` в список полей, которые должны быть исключены из сериализатора.

For example:

Например:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['users']
```

In the example above, if the `Account` model had 3 fields `account_name`, `users`, and `created`, this will result in the fields `account_name` and `created` to be serialized.

В приведенном выше примере, если модель `Account` имеет 3 поля `account_name`, `users` и `created`, это приведет к тому, что поля `account_name` и `created` будут сериализованы.

The names in the `fields` and `exclude` attributes will normally map to model fields on the model class.

Имена в атрибутах `fields` и `exclude` обычно отображаются на поля модели в классе модели.

Alternatively names in the `fields` options can map to properties or methods which take no arguments that exist on the model class.

Альтернативные имена в опциях `fields` могут отображаться на свойства или методы, не принимающие аргументов, которые существуют в классе модели.

Since version 3.3.0, it is **mandatory** to provide one of the attributes `fields` or `exclude`.

Начиная с версии 3.3.0, **обязательным** является предоставление одного из атрибутов `fields` или `exclude`.

## Specifying nested serialization

## Указание вложенной сериализации

The default `ModelSerializer` uses primary keys for relationships, but you can also easily generate nested representations using the `depth` option:

По умолчанию `ModelSerializer` использует первичные ключи для отношений, но вы также можете легко генерировать вложенные представления с помощью опции `depth`:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        depth = 1
```

The `depth` option should be set to an integer value that indicates the depth of relationships that should be traversed before reverting to a flat representation.

Параметр `depth` должен быть установлен в целочисленное значение, которое указывает глубину отношений, которые должны быть пройдены перед возвратом к плоскому представлению.

If you want to customize the way the serialization is done you'll need to define the field yourself.

Если вы хотите настроить способ сериализации, вам нужно будет определить поле самостоятельно.

## Specifying fields explicitly

## Указание полей в явном виде

You can add extra fields to a `ModelSerializer` or override the default fields by declaring fields on the class, just as you would for a `Serializer` class.

Вы можете добавить дополнительные поля в `ModelSerializer` или переопределить поля по умолчанию, объявив поля в классе, как и в классе `Serializer`.

```
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
        fields = ['url', 'groups']
```

Extra fields can correspond to any property or callable on the model.

Дополнительные поля могут соответствовать любому свойству или вызываемому объекту модели.

## Specifying read only fields

## Указание полей, доступных только для чтения

You may wish to specify multiple fields as read-only. Instead of adding each field explicitly with the `read_only=True` attribute, you may use the shortcut Meta option, `read_only_fields`.

Вы можете указать несколько полей как доступные только для чтения. Вместо того чтобы добавлять каждое поле явно с атрибутом `read_only=True`, вы можете использовать сокращенную опцию Meta, `read_only_fields`.

This option should be a list or tuple of field names, and is declared as follows:

Этот параметр должен представлять собой список или кортеж имен полей и объявляется следующим образом:

```
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name']
```

Model fields which have `editable=False` set, and `AutoField` fields will be set to read-only by default, and do not need to be added to the `read_only_fields` option.

Поля модели, для которых установлено значение `editable=False`, и поля `AutoField` по умолчанию будут установлены в режим только для чтения, и их не нужно добавлять в опцию `read_only_fields`.

---

**Note**: There is a special-case where a read-only field is part of a `unique_together` constraint at the model level. In this case the field is required by the serializer class in order to validate the constraint, but should also not be editable by the user.

**Примечание**: Существует особый случай, когда поле, доступное только для чтения, является частью ограничения `unique_together` на уровне модели. В этом случае поле требуется классу сериализатора для проверки ограничения, но также не должно редактироваться пользователем.

The right way to deal with this is to specify the field explicitly on the serializer, providing both the `read_only=True` and `default=…` keyword arguments.

Правильный способ справиться с этим - явно указать поле в сериализаторе, предоставив ключевые аргументы `read_only=True` и `default=...`.

One example of this is a read-only relation to the currently authenticated `User` which is `unique_together` with another identifier. In this case you would declare the user field like so:

Одним из примеров этого является отношение только для чтения к текущему аутентифицированному `User`, который является `unique_together` с другим идентификатором. В этом случае вы объявите поле пользователя следующим образом:

```
user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
```

Please review the [Validators Documentation](/api-guide/validators/) for details on the [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) and [CurrentUserDefault](/api-guide/validators/#currentuserdefault) classes.

Пожалуйста, ознакомьтесь с документацией [Validators Documentation](/api-guide/validators/) для получения подробной информации о классах [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) и [CurrentUserDefault](/api-guide/validators/#currentuserdefault).

---

## Additional keyword arguments

## Дополнительные аргументы ключевых слов

There is also a shortcut allowing you to specify arbitrary additional keyword arguments on fields, using the `extra_kwargs` option. As in the case of `read_only_fields`, this means you do not need to explicitly declare the field on the serializer.

Существует также возможность указать произвольные дополнительные аргументы ключевых слов для полей, используя опцию `extra_kwargs`. Как и в случае с `read_only_fields`, это означает, что вам не нужно явно объявлять поле в сериализаторе.

This option is a dictionary, mapping field names to a dictionary of keyword arguments. For example:

Эта опция представляет собой словарь, отображающий имена полей на словарь аргументов ключевых слов. Например:

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

Следует помнить, что если поле уже было явно объявлено в классе сериализатора, то опция `extra_kwargs` будет проигнорирована.

## Relational fields

## Реляционные поля

When serializing model instances, there are a number of different ways you might choose to represent relationships. The default representation for `ModelSerializer` is to use the primary keys of the related instances.

При сериализации экземпляров модели существует несколько различных способов представления отношений. Представление по умолчанию для `ModelSerializer` заключается в использовании первичных ключей связанных экземпляров.

Alternative representations include serializing using hyperlinks, serializing complete nested representations, or serializing with a custom representation.

Альтернативные представления включают сериализацию с помощью гиперссылок, сериализацию полных вложенных представлений или сериализацию с помощью пользовательского представления.

For full details see the [serializer relations](relations.md) documentation.

Более подробную информацию можно найти в документации [serializer relations](relations.md).

## Customizing field mappings

## Настройка сопоставлений полей

The ModelSerializer class also exposes an API that you can override in order to alter how serializer fields are automatically determined when instantiating the serializer.

Класс ModelSerializer также предоставляет API, который вы можете переопределить, чтобы изменить способ автоматического определения полей сериализатора при инстанцировании сериализатора.

Normally if a `ModelSerializer` does not generate the fields you need by default then you should either add them to the class explicitly, or simply use a regular `Serializer` class instead. However in some cases you may want to create a new base class that defines how the serializer fields are created for any given model.

Обычно, если `ModelSerializer` не генерирует нужные вам поля по умолчанию, вы должны либо добавить их в класс явно, либо просто использовать вместо них обычный класс `Serializer`. Однако в некоторых случаях вы можете захотеть создать новый базовый класс, определяющий, как создаются поля сериализатора для любой конкретной модели.

### `serializer_field_mapping`

### `serializer_field_mapping`.

A mapping of Django model fields to REST framework serializer fields. You can override this mapping to alter the default serializer fields that should be used for each model field.

Отображение полей модели Django на поля сериализатора фреймворка REST. Вы можете переопределить это отображение, чтобы изменить поля сериализатора по умолчанию, которые должны использоваться для каждого поля модели.

### `serializer_related_field`

### `serializer_related_field`.

This property should be the serializer field class, that is used for relational fields by default.

Это свойство должно быть классом поля сериализатора, который по умолчанию используется для реляционных полей.

For `ModelSerializer` this defaults to `serializers.PrimaryKeyRelatedField`.

Для `ModelSerializer` это значение по умолчанию равно `serializers.PrimaryKeyRelatedField`.

For `HyperlinkedModelSerializer` this defaults to `serializers.HyperlinkedRelatedField`.

Для `HyperlinkedModelSerializer` это значение по умолчанию равно `serializers.HyperlinkedRelatedField`.

### `serializer_url_field`

### `serializer_url_field`.

The serializer field class that should be used for any `url` field on the serializer.

Класс поля сериализатора, который должен использоваться для любого поля `url` в сериализаторе.

Defaults to `serializers.HyperlinkedIdentityField`

По умолчанию `serializers.HyperlinkedIdentityField`.

### `serializer_choice_field`

### `serializer_choice_field`

The serializer field class that should be used for any choice fields on the serializer.

Класс поля сериализатора, который должен использоваться для любых полей выбора в сериализаторе.

Defaults to `serializers.ChoiceField`

По умолчанию `serializers.ChoiceField`.

### The field_class and field_kwargs API

### API field_class и field_kwargs

The following methods are called to determine the class and keyword arguments for each field that should be automatically included on the serializer. Each of these methods should return a two tuple of `(field_class, field_kwargs)`.

Следующие методы вызываются для определения класса и аргументов ключевых слов для каждого поля, которое должно быть автоматически включено в сериализатор. Каждый из этих методов должен возвращать кортеж `(field_class, field_kwargs)`.

### `build_standard_field(self, field_name, model_field)`

### `build_standard_field(self, field_name, model_field)`.

Called to generate a serializer field that maps to a standard model field.

Вызывается для генерации поля сериализатора, которое сопоставляется со стандартным полем модели.

The default implementation returns a serializer class based on the `serializer_field_mapping` attribute.

Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_field_mapping`.

### `build_relational_field(self, field_name, relation_info)`

### `build_relational_field(self, field_name, relation_info)`.

Called to generate a serializer field that maps to a relational model field.

Вызывается для генерации поля сериализатора, которое сопоставляется с полем реляционной модели.

The default implementation returns a serializer class based on the `serializer_related_field` attribute.

Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_related_field`.

The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.

Аргумент `relation_info` представляет собой именованный кортеж, содержащий свойства `model_field`, `related_model`, `to_many` и `has_through_model`.

### `build_nested_field(self, field_name, relation_info, nested_depth)`

### `build_nested_field(self, field_name, relation_info, nested_depth)`.

Called to generate a serializer field that maps to a relational model field, when the `depth` option has been set.

Вызывается для генерации поля сериализатора, которое сопоставляется с полем реляционной модели, если установлен параметр `depth`.

The default implementation dynamically creates a nested serializer class based on either `ModelSerializer` or `HyperlinkedModelSerializer`.

Реализация по умолчанию динамически создает вложенный класс сериализатора на основе `ModelSerializer` или `HyperlinkedModelSerializer`.

The `nested_depth` will be the value of the `depth` option, minus one.

Значение `nested_depth` будет равно значению опции `depth`, минус один.

The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.

Аргумент `relation_info` представляет собой именованный кортеж, содержащий свойства `model_field`, `related_model`, `to_many` и `has_through_model`.

### `build_property_field(self, field_name, model_class)`

### `build_property_field(self, field_name, model_class)`.

Called to generate a serializer field that maps to a property or zero-argument method on the model class.

Вызывается для генерации поля сериализатора, которое сопоставляется со свойством или методом с нулевым аргументом класса модели.

The default implementation returns a `ReadOnlyField` class.

Реализация по умолчанию возвращает класс `ReadOnlyField`.

### `build_url_field(self, field_name, model_class)`

### `build_url_field(self, field_name, model_class)`.

Called to generate a serializer field for the serializer's own `url` field. The default implementation returns a `HyperlinkedIdentityField` class.

Вызывается для генерации поля сериализатора для собственного поля сериализатора `url`. Реализация по умолчанию возвращает класс `HyperlinkedIdentityField`.

### `build_unknown_field(self, field_name, model_class)`

### `build_unknown_field(self, field_name, model_class)`.

Called when the field name did not map to any model field or model property. The default implementation raises an error, although subclasses may customize this behavior.

Вызывается, когда имя поля не сопоставлено ни с одним полем модели или свойством модели. Реализация по умолчанию вызывает ошибку, хотя подклассы могут настраивать это поведение.

---

# HyperlinkedModelSerializer

# HyperlinkedModelSerializer

The `HyperlinkedModelSerializer` class is similar to the `ModelSerializer` class except that it uses hyperlinks to represent relationships, rather than primary keys.

Класс `HyperlinkedModelSerializer` похож на класс `ModelSerializer`, за исключением того, что он использует гиперссылки для представления отношений, а не первичные ключи.

By default the serializer will include a `url` field instead of a primary key field.

По умолчанию сериализатор будет включать поле `url` вместо поля первичного ключа.

The url field will be represented using a `HyperlinkedIdentityField` serializer field, and any relationships on the model will be represented using a `HyperlinkedRelatedField` serializer field.

Поле url будет представлено с помощью поля сериализатора `HyperlinkedIdentityField`, а любые отношения в модели будут представлены с помощью поля сериализатора `HyperlinkedRelatedField`.

You can explicitly include the primary key by adding it to the `fields` option, for example:

Вы можете явно включить первичный ключ, добавив его, например, в опцию `fields`:

```
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'account_name', 'users', 'created']
```

## Absolute and relative URLs

## Абсолютные и относительные URL-адреса

When instantiating a `HyperlinkedModelSerializer` you must include the current `request` in the serializer context, for example:

При инстанцировании `HyperlinkedModelSerializer` вы должны включить текущий `запрос` в контекст сериализатора, например:

```
serializer = AccountSerializer(queryset, context={'request': request})
```

Doing so will ensure that the hyperlinks can include an appropriate hostname, so that the resulting representation uses fully qualified URLs, such as:

Это гарантирует, что гиперссылки могут включать соответствующее имя хоста, так что результирующее представление использует полные URL-адреса, такие как:

```
http://api.example.com/accounts/1/
```

Rather than relative URLs, such as:

Вместо относительных URL-адресов, таких как:

```
/accounts/1/
```

If you *do* want to use relative URLs, you should explicitly pass `{'request': None}` in the serializer context.

Если вы *хотите* использовать относительные URL, вам следует явно передать `{'request': None}` в контексте сериализатора.

## How hyperlinked views are determined

## Как определяются представления с гиперссылками

There needs to be a way of determining which views should be used for hyperlinking to model instances.

Необходимо определить, какие представления следует использовать для гиперссылок на экземпляры модели.

By default hyperlinks are expected to correspond to a view name that matches the style `'{model_name}-detail'`, and looks up the instance by a `pk` keyword argument.

По умолчанию ожидается, что гиперссылки будут соответствовать имени представления, которое соответствует стилю `'{имя_модели}-detail'`, и ищет экземпляр по аргументу ключевого слова `pk`.

You can override a URL field view name and lookup field by using either, or both of, the `view_name` and `lookup_field` options in the `extra_kwargs` setting, like so:

Вы можете переопределить имя представления поля URL и поле поиска, используя один или оба параметра `view_name` и `lookup_field` в параметре `extra_kwargs`, как показано ниже:

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

В качестве альтернативы вы можете явно задать поля в сериализаторе. Например:

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

**Совет**: Правильное согласование гиперссылочных представлений и вашего URL conf иногда может быть немного сложным. Печать `repr` экземпляра `HyperlinkedModelSerializer` - особенно полезный способ проверить, какие именно имена представлений и поля поиска должны отображать отношения.

---

## Changing the URL field name

## Изменение имени поля URL

The name of the URL field defaults to 'url'. You can override this globally, by using the `URL_FIELD_NAME` setting.

Имя поля URL по умолчанию равно 'url'. Вы можете переопределить его глобально, используя параметр `URL_FIELD_NAME`.

---

# ListSerializer

# ListSerializer

The `ListSerializer` class provides the behavior for serializing and validating multiple objects at once. You won't *typically* need to use `ListSerializer` directly, but should instead simply pass `many=True` when instantiating a serializer.

Класс `ListSerializer` обеспечивает поведение для сериализации и валидации нескольких объектов одновременно. Обычно вам не нужно использовать `ListSerializer` напрямую, а следует просто передать `many=True` при инстанцировании сериализатора.

When a serializer is instantiated and `many=True` is passed, a `ListSerializer` instance will be created. The serializer class then becomes a child of the parent `ListSerializer`

При инстанцировании сериализатора и передаче `many=True` будет создан экземпляр `ListSerializer`. Затем класс сериализатора становится дочерним классом родительского `ListSerializer`.

The following argument can also be passed to a `ListSerializer` field or a serializer that is passed `many=True`:

Следующий аргумент также может быть передан полю `ListSerializer` или сериализатору, которому передано `many=True`:

### `allow_empty`

### `allow_empty`

This is `True` by default, but can be set to `False` if you want to disallow empty lists as valid input.

По умолчанию это `True`, но может быть установлено в `False`, если вы хотите запретить пустые списки в качестве допустимого ввода.

### `max_length`

### `max_length`

This is `None` by default, but can be set to a positive integer if you want to validates that the list contains no more than this number of elements.

По умолчанию это `None`, но может быть установлено в положительное целое число, если вы хотите проверить, что список содержит не более этого количества элементов.

### `min_length`

### `min_length`

This is `None` by default, but can be set to a positive integer if you want to validates that the list contains no fewer than this number of elements.

По умолчанию это `None`, но может быть установлено в положительное целое число, если вы хотите проверить, что список содержит не менее этого количества элементов.

### Customizing `ListSerializer` behavior

### Настройка поведения `ListSerializer`.

There *are* a few use cases when you might want to customize the `ListSerializer` behavior. For example:

Существует *несколько случаев, когда вы можете захотеть настроить поведение `ListSerializer`. Например:

* You want to provide particular validation of the lists, such as checking that one element does not conflict with another element in a list.
* You want to customize the create or update behavior of multiple objects.

* Вы хотите обеспечить определенную проверку списков, например, проверить, что один элемент не конфликтует с другим элементом списка.
* Вы хотите настроить поведение создания или обновления нескольких объектов.

For these cases you can modify the class that is used when `many=True` is passed, by using the `list_serializer_class` option on the serializer `Meta` class.

Для этих случаев вы можете изменить класс, который используется при передаче `many=True`, используя опцию `list_serializer_class` для класса сериализатора `Meta`.

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

#### Настройка множественного создания

The default implementation for multiple object creation is to simply call `.create()` for each item in the list. If you want to customize this behavior, you'll need to customize the `.create()` method on `ListSerializer` class that is used when `many=True` is passed.

Реализация по умолчанию для создания нескольких объектов заключается в простом вызове `.create()` для каждого элемента списка. Если вы хотите настроить это поведение, вам нужно настроить метод `.create()` класса `ListSerializer`, который используется, когда передается `many=True`.

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

#### Настройка многократного обновления

By default the `ListSerializer` class does not support multiple updates. This is because the behavior that should be expected for insertions and deletions is ambiguous.

По умолчанию класс `ListSerializer` не поддерживает множественные обновления. Это связано с тем, что поведение, которое следует ожидать для вставок и удалений, неоднозначно.

To support multiple updates you'll need to do so explicitly. When writing your multiple update code make sure to keep the following in mind:

Для поддержки нескольких обновлений необходимо сделать это явно. При написании кода множественных обновлений обязательно учитывайте следующее:

* How do you determine which instance should be updated for each item in the list of data?
* How should insertions be handled? Are they invalid, or do they create new objects?
* How should removals be handled? Do they imply object deletion, or removing a relationship? Should they be silently ignored, or are they invalid?
* How should ordering be handled? Does changing the position of two items imply any state change or is it ignored?

* Как определить, какой экземпляр должен быть обновлен для каждого элемента в списке данных?
* Как следует обрабатывать вставки? Являются ли они недействительными, или они создают новые объекты?
* Как следует обрабатывать удаления? Означают ли они удаление объекта или удаление отношения? Следует ли их молча игнорировать, или они недействительны?
* Как следует обрабатывать упорядочивание? Влечет ли изменение положения двух объектов изменение состояния или оно игнорируется?

You will need to add an explicit `id` field to the instance serializer. The default implicitly-generated `id` field is marked as `read_only`. This causes it to be removed on updates. Once you declare it explicitly, it will be available in the list serializer's `update` method.

Вам нужно будет добавить явное поле `id` в сериализатор экземпляра. По умолчанию неявно генерируемое поле `id` помечено как `read_only`. Это приводит к тому, что оно удаляется при обновлении. Как только вы объявите его явно, оно будет доступно в методе `update` сериализатора списка.

Here's an example of how you might choose to implement multiple updates:

Вот пример того, как можно реализовать несколько обновлений:

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

Возможно, в релиз 3.1 будет включен пакет сторонних разработчиков, обеспечивающий автоматическую поддержку нескольких операций обновления, подобно поведению `allow_add_remove`, которое присутствовало в REST framework 2.

#### Customizing ListSerializer initialization

#### Настройка инициализации ListSerializer

When a serializer with `many=True` is instantiated, we need to determine which arguments and keyword arguments should be passed to the `.__init__()` method for both the child `Serializer` class, and for the parent `ListSerializer` class.

Когда инстанцируется сериализатор с `many=True`, нам необходимо определить, какие аргументы и ключевые слова следует передать в метод `.__init__()` как для дочернего класса `Serializer`, так и для родительского класса `ListSerializer`.

The default implementation is to pass all arguments to both classes, except for `validators`, and any custom keyword arguments, both of which are assumed to be intended for the child serializer class.

По умолчанию все аргументы передаются обоим классам, за исключением `validators` и любых пользовательских аргументов ключевых слов, которые, как предполагается, предназначены для дочернего класса сериализатора.

Occasionally you might need to explicitly specify how the child and parent classes should be instantiated when `many=True` is passed. You can do so by using the `many_init` class method.

Иногда вам может понадобиться явно указать, как дочерний и родительский классы должны быть инстанцированы при передаче `many=True`. Вы можете сделать это с помощью метода класса `many_init`.

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

Класс `BaseSerializer`, который можно использовать для простой поддержки альтернативных стилей сериализации и десериализации.

This class implements the same basic API as the `Serializer` class:

Этот класс реализует тот же базовый API, что и класс `Serializer`:

* `.data` - Returns the outgoing primitive representation.
* `.is_valid()` - Deserializes and validates incoming data.
* `.validated_data` - Returns the validated incoming data.
* `.errors` - Returns any errors during validation.
* `.save()` - Persists the validated data into an object instance.

* `.data' - Возвращает исходящее примитивное представление.
* `.is_valid()` - Десериализует и проверяет входящие данные.
* `.validated_data` - Возвращает проверенные входящие данные.
* `.errors` - Возвращает любые ошибки во время валидации.
* `.save()` - Сохраняет проверенные данные в экземпляре объекта.

There are four methods that can be overridden, depending on what functionality you want the serializer class to support:

Есть четыре метода, которые могут быть переопределены, в зависимости от того, какую функциональность вы хотите, чтобы поддерживал класс сериализатора:

* `.to_representation()` - Override this to support serialization, for read operations.
* `.to_internal_value()` - Override this to support deserialization, for write operations.
* `.create()` and `.update()` - Override either or both of these to support saving instances.

* `.to_representation()` - Переопределить это для поддержки сериализации, для операций чтения.
* `.to_internal_value()` - Переопределить это для поддержки десериализации, для операций записи.
* `.create()` и `.update()` - Переопределите один из этих параметров или оба для поддержки сохранения экземпляров.

Because this class provides the same interface as the `Serializer` class, you can use it with the existing generic class-based views exactly as you would for a regular `Serializer` or `ModelSerializer`.

Поскольку этот класс предоставляет тот же интерфейс, что и класс `Serializer`, вы можете использовать его с существующими представлениями на основе общих классов точно так же, как и обычный `Serializer` или `ModelSerializer`.

The only difference you'll notice when doing so is the `BaseSerializer` classes will not generate HTML forms in the browsable API. This is because the data they return does not include all the field information that would allow each field to be rendered into a suitable HTML input.

Единственное отличие, которое вы заметите при этом - классы `BaseSerializer` не будут генерировать HTML-формы в просматриваемом API. Это происходит потому, что данные, которые они возвращают, не включают всю информацию о полях, которая позволила бы преобразовать каждое поле в подходящий HTML-ввод.

#### Read-only `BaseSerializer` classes

#### Классы `BaseSerializer` только для чтения.

To implement a read-only serializer using the `BaseSerializer` class, we just need to override the `.to_representation()` method. Let's take a look at an example using a simple Django model:

Чтобы реализовать сериализатор только для чтения, используя класс `BaseSerializer`, нам просто нужно переопределить метод `.to_representation()`. Давайте рассмотрим пример на примере простой модели Django:

```
class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()
```

It's simple to create a read-only serializer for converting `HighScore` instances into primitive data types.

Очень просто создать сериализатор только для чтения для преобразования экземпляров `HighScore` в примитивные типы данных.

```
class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }
```

We can now use this class to serialize single `HighScore` instances:

Теперь мы можем использовать этот класс для сериализации отдельных экземпляров `HighScore`:

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

#### Классы `BaseSerializer` с функцией чтения-записи

To create a read-write serializer we first need to implement a `.to_internal_value()` method. This method returns the validated values that will be used to construct the object instance, and may raise a `serializers.ValidationError` if the supplied data is in an incorrect format.

Для создания сериализатора чтения-записи нам сначала нужно реализовать метод `.to_internal_value()`. Этот метод возвращает проверенные значения, которые будут использованы для создания экземпляра объекта, и может вызвать `serializers.ValidationError, если предоставленные данные имеют неправильный формат.

Once you've implemented `.to_internal_value()`, the basic validation API will be available on the serializer, and you will be able to use `.is_valid()`, `.validated_data` and `.errors`.

Как только вы реализуете `.to_internal_value()`, базовый API валидации будет доступен в сериализаторе, и вы сможете использовать `.is_valid()`, `.validated_data` и `.errors`.

If you want to also support `.save()` you'll need to also implement either or both of the `.create()` and `.update()` methods.

Если вы хотите также поддерживать `.save()`, вам необходимо также реализовать один или оба метода `.create()` и `.update()`.

Here's a complete example of our previous `HighScoreSerializer`, that's been updated to support both read and write operations.

Вот полный пример нашего предыдущего `HighScoreSerializer`, который был обновлен для поддержки операций чтения и записи.

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

Класс `BaseSerializer` также полезен, если вы хотите реализовать новые общие классы сериализаторов для работы с определенными стилями сериализации или для интеграции с альтернативными бэкендами хранения данных.

The following class is an example of a generic serializer that can handle coercing arbitrary complex objects into primitive representations.

Следующий класс является примером общего сериализатора, который может обрабатывать принудительное преобразование произвольных сложных объектов в примитивные представления.

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

# Расширенное использование сериализатора

## Overriding serialization and deserialization behavior

## Переопределение поведения сериализации и десериализации

If you need to alter the serialization or deserialization behavior of a serializer class, you can do so by overriding the `.to_representation()` or `.to_internal_value()` methods.

Если вам нужно изменить поведение сериализации или десериализации класса сериализатора, вы можете сделать это, переопределив методы `.to_representation()` или `.to_internal_value()`.

Some reasons this might be useful include...

Некоторые причины, по которым это может быть полезно, включают...

* Adding new behavior for new serializer base classes.
* Modifying the behavior slightly for an existing class.
* Improving serialization performance for a frequently accessed API endpoint that returns lots of data.

* Добавление нового поведения для новых базовых классов сериализаторов.
* Небольшое изменение поведения для существующего класса.
* Улучшение производительности сериализации для часто используемой конечной точки API, которая возвращает много данных.

The signatures for these methods are as follows:

Подписи для этих методов следующие:

#### `to_representation(self, instance)`

#### `to_representation(self, instance)`.

Takes the object instance that requires serialization, and should return a primitive representation. Typically this means returning a structure of built-in Python datatypes. The exact types that can be handled will depend on the render classes you have configured for your API.

Принимает экземпляр объекта, который требует сериализации, и должен вернуть примитивное представление. Обычно это означает возврат структуры встроенных в Python типов данных. Точные типы, которые могут быть обработаны, зависят от классов рендеринга, которые вы настроили для своего API.

May be overridden in order to modify the representation style. For example:

Может быть переопределена для изменения стиля представления. Например:

```
def to_representation(self, instance):
    """Convert `username` to lowercase."""
    ret = super().to_representation(instance)
    ret['username'] = ret['username'].lower()
    return ret
```

#### `to_internal_value(self, data)`

#### `to_internal_value(self, data)`.

Takes the unvalidated incoming data as input and should return the validated data that will be made available as `serializer.validated_data`. The return value will also be passed to the `.create()` or `.update()` methods if `.save()` is called on the serializer class.

Принимает невалидированные входящие данные в качестве входных и должен вернуть валидированные данные, которые будут доступны как `serializer.validated_data`. Возвращаемое значение также будет передано методам `.create()` или `.update()`, если для класса сериализатора будет вызван `.save()`.

If any of the validation fails, then the method should raise a `serializers.ValidationError(errors)`. The `errors` argument should be a dictionary mapping field names (or `settings.NON_FIELD_ERRORS_KEY`) to a list of error messages. If you don't need to alter deserialization behavior and instead want to provide object-level validation, it's recommended that you instead override the [`.validate()`](#object-level-validation) method.

Если какая-либо из валидаций не прошла, то метод должен вызвать `serializers.ValidationError(errors)`. Аргумент `errors` должен представлять собой словарь, отображающий имена полей (или `settings.NON_FIELD_ERRORS_KEY`) на список сообщений об ошибках. Если вам не нужно изменять поведение десериализации и вместо этого вы хотите обеспечить проверку на уровне объекта, рекомендуется переопределить метод [`.validate()`](#object-level-validation).

The `data` argument passed to this method will normally be the value of `request.data`, so the datatype it provides will depend on the parser classes you have configured for your API.

Аргумент `data`, передаваемый этому методу, обычно является значением `request.data`, поэтому тип данных, который он предоставляет, будет зависеть от классов парсера, которые вы настроили для своего API.

## Serializer Inheritance

## Наследование сериализатора

Similar to Django forms, you can extend and reuse serializers through inheritance. This allows you to declare a common set of fields or methods on a parent class that can then be used in a number of serializers. For example,

Подобно формам Django, вы можете расширять и повторно использовать сериализаторы с помощью наследования. Это позволяет вам объявить общий набор полей или методов в родительском классе, который затем может быть использован в нескольких сериализаторах. Например,

```
class MyBaseSerializer(Serializer):
    my_field = serializers.CharField()

    def validate_my_field(self, value):
        ...

class MySerializer(MyBaseSerializer):
    ...
```

Like Django's `Model` and `ModelForm` classes, the inner `Meta` class on serializers does not implicitly inherit from it's parents' inner `Meta` classes. If you want the `Meta` class to inherit from a parent class you must do so explicitly. For example:

Как и классы `Model` и `ModelForm` в Django, внутренний класс `Meta` в сериализаторах не наследуется неявно от внутренних классов `Meta` своих родителей. Если вы хотите, чтобы класс `Meta` наследовался от родительского класса, вы должны сделать это явно. Например:

```
class AccountSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        model = Account
```

Typically we would recommend *not* using inheritance on inner Meta classes, but instead declaring all options explicitly.

Обычно мы рекомендуем *не* использовать наследование для внутренних классов Meta, а вместо этого объявлять все опции явно.

Additionally, the following caveats apply to serializer inheritance:

Кроме того, следующие предостережения относятся к наследованию сериализаторов:

* Normal Python name resolution rules apply. If you have multiple base classes that declare a `Meta` inner class, only the first one will be used. This means the child’s `Meta`, if it exists, otherwise the `Meta` of the first parent, etc.
* It’s possible to declaratively remove a `Field` inherited from a parent class by setting the name to be `None` on the subclass.
    ```
    class MyBaseSerializer(ModelSerializer):
          my_field = serializers.CharField()
    
      class MySerializer(MyBaseSerializer):
          my_field = None
    ```However, you can only use this technique to opt out from a field defined declaratively by a parent class; it won’t prevent the `ModelSerializer` from generating a default field. To opt-out from default fields, see [Specifying which fields to include](#specifying-which-fields-to-include).

* Применяются обычные правила разрешения имен Python. Если у вас есть несколько базовых классов, которые объявляют внутренний класс `Meta`, будет использоваться только первый класс. Это означает дочерний `Meta`, если он существует, иначе `Meta` первого родителя и т.д.
* Можно декларативно удалить `Field`, унаследованный от родительского класса, установив его имя в `None` в подклассе.
```
class MyBaseSerializer(ModelSerializer):
my_field = serializers.CharField()
class MySerializer(MyBaseSerializer):
my_field = None
Однако, вы можете использовать эту технику только для отказа от поля, определенного декларативно родительским классом; это не помешает `ModelSerializer` сгенерировать поле по умолчанию. Чтобы отказаться от полей по умолчанию, смотрите [Specifying what fields to include](#specifying-which-fields-to-include).

## Dynamically modifying fields

## Динамическое изменение полей

Once a serializer has been initialized, the dictionary of fields that are set on the serializer may be accessed using the `.fields` attribute. Accessing and modifying this attribute allows you to dynamically modify the serializer.

После инициализации сериализатора, к словарю полей, установленных в сериализаторе, можно получить доступ с помощью атрибута `.fields`. Доступ и изменение этого атрибута позволяет динамически модифицировать сериализатор.

Modifying the `fields` argument directly allows you to do interesting things such as changing the arguments on serializer fields at runtime, rather than at the point of declaring the serializer.

Изменение аргумента `fields` напрямую позволяет вам делать такие интересные вещи, как изменение аргументов полей сериализатора во время выполнения, а не в момент объявления сериализатора.

### Example

### Пример

For example, if you wanted to be able to set which fields should be used by a serializer at the point of initializing it, you could create a serializer class like so:

Например, если вы хотите иметь возможность установить, какие поля должны использоваться сериализатором в момент его инициализации, вы можете создать класс сериализатора следующим образом:

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

Это позволит вам сделать следующее:

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

REST framework 2 предоставил API, позволяющий разработчикам переопределять, как класс `ModelSerializer` будет автоматически генерировать набор полей по умолчанию.

This API included the `.get_field()`, `.get_pk_field()` and other methods.

Этот API включал методы `.get_field()`, `.get_pk_field()` и другие.

Because the serializers have been fundamentally redesigned with 3.0 this API no longer exists. You can still modify the fields that get created but you'll need to refer to the source code, and be aware that if the changes you make are against private bits of API then they may be subject to change.

Поскольку сериализаторы были кардинально переработаны в версии 3.0, этот API больше не существует. Вы все еще можете изменять создаваемые поля, но вам придется обратиться к исходному коду, и имейте в виду, что если изменения, которые вы делаете, направлены против частных частей API, то они могут быть изменены.

---

# Third party packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## Django REST marshmallow

## Django REST marshmallow

The [django-rest-marshmallow](https://marshmallow-code.github.io/django-rest-marshmallow/) package provides an alternative implementation for serializers, using the python [marshmallow](https://marshmallow.readthedocs.io/en/latest/) library. It exposes the same API as the REST framework serializers, and can be used as a drop-in replacement in some use-cases.

Пакет [django-rest-marshmallow](https://marshmallow-code.github.io/django-rest-marshmallow/) предоставляет альтернативную реализацию сериализаторов, используя библиотеку python [marshmallow](https://marshmallow.readthedocs.io/en/latest/). Он предоставляет тот же API, что и сериализаторы фреймворка REST, и может быть использован в качестве замены в некоторых случаях.

## Serpy

## Serpy

The [serpy](https://github.com/clarkduvall/serpy) package is an alternative implementation for serializers that is built for speed. [Serpy](https://github.com/clarkduvall/serpy) serializes complex datatypes to simple native types. The native types can be easily converted to JSON or any other format needed.

Пакет [serpy](https://github.com/clarkduvall/serpy) - это альтернативная реализация сериализаторов, созданная для скорости. [Serpy](https://github.com/clarkduvall/serpy) сериализует сложные типы данных в простые нативные типы. Родные типы могут быть легко преобразованы в JSON или любой другой необходимый формат.

## MongoengineModelSerializer

## MongoengineModelSerializer

The [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) package provides a `MongoEngineModelSerializer` serializer class that supports using MongoDB as the storage layer for Django REST framework.

Пакет [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) предоставляет класс сериализатора `MongoEngineModelSerializer`, который поддерживает использование MongoDB в качестве уровня хранения данных для Django REST framework.

## GeoFeatureModelSerializer

## GeoFeatureModelSerializer

The [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) package provides a `GeoFeatureModelSerializer` serializer class that supports GeoJSON both for read and write operations.

Пакет [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) предоставляет класс сериализатора `GeoFeatureModelSerializer`, который поддерживает GeoJSON как для операций чтения, так и для записи.

## HStoreSerializer

## HStoreSerializer

The [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) package provides an `HStoreSerializer` to support [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` model field and its `schema-mode` feature.

Пакет [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `HStoreSerializer` для поддержки поля модели [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` и его функции `chema-mode`.

## Dynamic REST

## Динамический REST

The [dynamic-rest](https://github.com/AltSchool/dynamic-rest) package extends the ModelSerializer and ModelViewSet interfaces, adding API query parameters for filtering, sorting, and including / excluding all fields and relationships defined by your serializers.

Пакет [dynamic-rest](https://github.com/AltSchool/dynamic-rest) расширяет интерфейсы ModelSerializer и ModelViewSet, добавляя параметры запроса API для фильтрации, сортировки, включения/исключения всех полей и отношений, определенных вашими сериализаторами.

## Dynamic Fields Mixin

## Миксин динамических полей

The [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) package provides a mixin to dynamically limit the fields per serializer to a subset specified by an URL parameter.

Пакет [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) предоставляет миксин для динамического ограничения полей для сериализатора подмножеством, заданным параметром URL.

## DRF FlexFields

## DRF FlexFields

The [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) package extends the ModelSerializer and ModelViewSet to provide commonly used functionality for dynamically setting fields and expanding primitive fields to nested models, both from URL parameters and your serializer class definitions.

Пакет [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) расширяет ModelSerializer и ModelViewSet для обеспечения широко используемой функциональности для динамической установки полей и расширения примитивных полей во вложенные модели, как из параметров URL, так и из определений класса вашего сериализатора.

## Serializer Extensions

## Расширения сериализатора

The [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) package provides a collection of tools to DRY up your serializers, by allowing fields to be defined on a per-view/request basis. Fields can be whitelisted, blacklisted and child serializers can be optionally expanded.

Пакет [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) предоставляет набор инструментов для DRY up ваших сериализаторов, позволяя определять поля на основе каждого представления/запроса. Поля могут быть внесены в белый или черный список, а дочерние сериализаторы могут быть расширены по желанию.

## HTML JSON Forms

## HTML JSON Forms

The [html-json-forms](https://github.com/wq/html-json-forms) package provides an algorithm and serializer for processing `<form>` submissions per the (inactive) [HTML JSON Form specification](https://www.w3.org/TR/html-json-forms/). The serializer facilitates processing of arbitrarily nested JSON structures within HTML. For example, `<input name="items[0][id]" value="5">` will be interpreted as `{"items": [{"id": "5"}]}`.

Пакет [html-json-forms](https://github.com/wq/html-json-forms) предоставляет алгоритм и сериализатор для обработки `<form>` представлений в соответствии с (неактивной) [HTML JSON Form specification](https://www.w3.org/TR/html-json-forms/). Сериализатор облегчает обработку произвольно вложенных структур JSON в HTML. Например, `<input name="items[0][id]" value="5">` будет интерпретирован как `{"items": [{"id": "5"}]}`.

## DRF-Base64

## DRF-Base64

[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64) provides a set of field and model serializers that handles the upload of base64-encoded files.

[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64) предоставляет набор сериализаторов полей и моделей, который обрабатывает загрузку файлов в base64-кодировке.

## QueryFields

## QueryFields

[djangorestframework-queryfields](https://djangorestframework-queryfields.readthedocs.io/) allows API clients to specify which fields will be sent in the response via inclusion/exclusion query parameters.

[djangorestframework-queryfields](https://djangorestframework-queryfields.readthedocs.io/) позволяет клиентам API указать, какие поля будут отправлены в ответе с помощью параметров запроса включения/исключения.

## DRF Writable Nested

## DRF Записываемый вложенный

The [drf-writable-nested](https://github.com/beda-software/drf-writable-nested) package provides writable nested model serializer which allows to create/update models with nested related data.

Пакет [drf-writable-nested](https://github.com/beda-software/drf-writable-nested) предоставляет записываемый сериализатор вложенных моделей, который позволяет создавать/обновлять модели с вложенными связанными данными.

## DRF Encrypt Content

## DRF Зашифровать содержимое

The [drf-encrypt-content](https://github.com/oguzhancelikarslan/drf-encrypt-content) package helps you encrypt your data, serialized through ModelSerializer. It also contains some helper functions. Which helps you to encrypt your data.

Пакет [drf-encrypt-content](https://github.com/oguzhancelikarslan/drf-encrypt-content) помогает вам шифровать данные, сериализованные через ModelSerializer. Он также содержит некоторые вспомогательные функции. Которые помогут вам зашифровать данные.