<!-- TRANSLATED by md-translate -->
---

источник:
- serializers.py

---

# Сериализаторы

> Расширение полезности сериализаторов - это то, чем мы хотели бы заняться. Однако это не тривиальная проблема, и она потребует серьезной работы над дизайном.
>
> &mdash; Russell Keith-Magee, [Django users group](https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion)

Сериализаторы позволяют преобразовывать сложные данные, такие как наборы запросов и экземпляры моделей, в собственные типы данных Python, которые затем могут быть легко преобразованы в `JSON`, `XML` или другие типы содержимого. Сериализаторы также обеспечивают десериализацию, позволяя преобразовывать разобранные данные обратно в сложные типы после предварительной проверки входящих данных.

Сериализаторы в DRF работают очень похоже на классы Django `Form` и `ModelForm`. Мы предоставляем класс `Serializer`, который дает вам мощный, универсальный способ управления выводом ваших ответов, а также класс `ModelSerializer`, который предоставляет полезный ярлык для создания сериализаторов, работающих с экземплярами моделей и наборами запросов.

## Объявление сериализаторов

Давайте начнем с создания простого объекта, который мы можем использовать для примера:

```python
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')
```

Мы объявим сериализатор, который мы можем использовать для сериализации и десериализации данных, соответствующих объектам `Comment`.

Объявление сериализатора очень похоже на объявление формы:

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Сериализация объектов

Теперь мы можем использовать `CommentSerializer` для сериализации комментария или списка комментариев. Опять же, использование класса `Serializer` очень похоже на использование класса `Form`.

```python
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
```

На данном этапе мы перевели экземпляр модели в собственные типы данных Python. Чтобы завершить процесс сериализации, мы преобразуем данные в `json`.

```python
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
```

## Десериализация объектов

Десериализация аналогична. Сначала мы разбираем поток на собственные типы данных Python...

```python
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
```

затем мы восстанавливаем эти родные типы данных в словарь проверенных данных.

```python
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
```

## Сохранение экземпляров

Если мы хотим иметь возможность возвращать полные экземпляры объектов на основе проверенных данных, нам необходимо реализовать один или оба метода `.create()` и `.update()`. Например:

```python
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

Если ваши экземпляры объектов соответствуют моделям Django, вы также захотите убедиться, что эти методы сохраняют объект в базе данных. Например, если `Comment` является моделью Django, методы могут выглядеть следующим образом:

```python
def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
```

Теперь при десериализации данных мы можем вызвать `.save()`, чтобы вернуть экземпляр объекта, основанный на проверенных данных.

```python
comment = serializer.save()
```

Вызов `.save()` либо создаст новый экземпляр, либо обновит существующий, в зависимости от того, был ли передан существующий экземпляр при инстанцировании класса сериализатора:

```python
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)
```

Методы `.create()` и `.update()` являются необязательными. Вы можете реализовать либо ни один из них, либо один, либо оба, в зависимости от условий использования вашего класса сериализатора.

#### Передача дополнительных атрибутов в `.save()`.

Иногда вы хотите, чтобы код представления мог вводить дополнительные данные в момент сохранения экземпляра. Эти дополнительные данные могут включать информацию о текущем пользователе, текущем времени или что-нибудь еще, что не является частью данных запроса.

Вы можете сделать это, включив дополнительные именованные аргументы при вызове `.save()`. Например:

```python
serializer.save(owner=request.user)
```

Любые дополнительные именованные аргументы будут включены в аргумент `validated_data` при вызове `.create()` или `.update()`.

#### Переопределение `.save()` напрямую.

В некоторых случаях имена методов `.create()` и `.update()` могут не иметь смысла. Например, в контактной форме мы можем не создавать новые экземпляры, а отправлять электронное письмо или другое сообщение.

В этих случаях вы можете вместо этого переопределить `.save()` напрямую, как более читабельный и осмысленный.

Например:

```python
class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(from=email, message=message)
```

Обратите внимание, что в приведенном выше случае нам приходится напрямую обращаться к свойству сериализатора `.validated_data`.

## Валидация

При десериализации данных всегда нужно вызывать `is_valid()` прежде, чем пытаться получить доступ к проверенным данным или сохранить экземпляр объекта. Если возникнут ошибки валидации, свойство `.errors` будет содержать словарь, представляющий сообщения об ошибках. Например:

```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid email address.'], 'created': ['This field is required.']}
```

Каждый ключ в словаре будет именем поля, а значения будут списками строк любых сообщений об ошибках, соответствующих этому полю. Также может присутствовать ключ `non_field_errors`, в котором будут перечислены все общие ошибки валидации. Имя ключа `non_field_errors` можно настроить с помощью параметра DRF `NON_FIELD_ERRORS_KEY`.

При десериализации списка элементов ошибки будут возвращены в виде списка словарей, представляющих каждый из десериализованных элементов.

#### Возбуждение исключения при недопустимых данных

Метод `.is_valid()` принимает необязательный флаг `raise_exception`, который заставит его поднять исключение `serializers.ValidationError`, если есть ошибки валидации.

Эти исключения автоматически обрабатываются обработчиком исключений по умолчанию, который предоставляет DRF, и по умолчанию будут возвращать ответы `HTTP 400 Bad Request`.

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

#### Валидация на уровне поля

Вы можете задать пользовательскую валидацию на уровне полей, добавив методы `.validate_<имя_поля>` в подкласс `Serializer`. Они аналогичны методам `.clean_<имя_поля>` в формах Django.

Эти методы принимают единственный аргумент, который является значением поля, требующего проверки.

Ваши методы `validate_<имя_поля>` должны возвращать проверенное значение или вызывать `serializers.ValidationError`. Например:

```python
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

**Примечание:** Если ваше `<имя_поля>` объявлено в вашем сериализаторе с параметром `required=False`, то этот шаг валидации не будет выполняться, если поле не включено.

---

#### Валидация на уровне объекта

Чтобы выполнить любую другую проверку, требующую доступа к нескольким полям, добавьте метод `.validate()` к вашему подклассу `Serializer`. Этот метод принимает единственный аргумент, который является словарем значений полей. При необходимости он должен вызывать `serializers.ValidationError, или просто возвращать проверенные значения. Например:

```python
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

#### Валидаторы

Отдельные поля сериализатора могут включать валидаторы, например, путем объявления их в экземпляре поля:

```python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = serializers.IntegerField(validators=[multiple_of_ten])
    ...
```

Классы сериализаторов могут также включать многократно используемые валидаторы, которые применяются к полному набору данных поля. Эти валидаторы включаются путем объявления их во внутреннем классе `Meta`, например, так:

```python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.ChoiceField(choices=[101, 102, 103, 201])
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

Для получения дополнительной информации см. документацию [validators](validators.md).

## Доступ к исходным данным и экземпляру

При передаче исходного объекта или набора запросов экземпляру сериализатора, объект будет доступен как `.instance`. Если начальный объект не передан, то атрибут `.instance` будет иметь значение `None`.

При передаче данных экземпляру сериализатора, немодифицированные данные будут доступны как `.initial_data`. Если именованный аргумент `data` не передан, то атрибут `.initial_data` не будет существовать.

## Частичные обновления

По умолчанию сериализаторам должны передаваться значения для всех обязательных полей, иначе они будут выдавать ошибки валидации. Вы можете использовать аргумент `partial`, чтобы разрешить частичное обновление.

```python
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
```

## Работа с вложенными объектами

Предыдущие примеры хорошо подходят для работы с объектами, которые имеют только простые типы данных, но иногда нам также необходимо иметь возможность представлять более сложные объекты, где некоторые атрибуты объекта могут не быть простыми типами данных, такими как строки, даты или целые числа.

Класс `Serializer` сам является типом `Field` и может быть использован для представления отношений, в которых один тип объекта вложен в другой.

```python
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Если вложенное представление может опционально принимать значение `None`, вы должны передать флаг `required=False` вложенному сериализатору.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Аналогично, если вложенное представление должно быть списком элементов, вы должны передать флаг `many=True` в сериализатор вложенных элементов.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Записываемые вложенные представления

При работе с вложенными представлениями, поддерживающими десериализацию данных, любые ошибки с вложенными объектами будут вложены под именем поля вложенного объекта.

```python
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid email address.']}, 'created': ['This field is required.']}
```

Аналогично, свойство `.validated_data` будет включать в себя вложенные структуры данных.

#### Написание методов `.create()` для вложенных представлений

Если вы поддерживаете записываемые вложенные представления, вам нужно написать методы `.create()` или `.update()`, которые обрабатывают сохранение нескольких объектов.

В следующем примере показано, как можно создать пользователя с вложенным объектом профиля.

```python
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

#### Написание методов `.update()` для вложенных представлений

Для обновлений вам необходимо тщательно продумать, как обрабатывать обновления отношений. Например, если данные для отношения `None`, или не предоставлены, что из перечисленного ниже должно произойти?

* Установите для отношения значение `NULL` в базе данных.
* Удалите связанный экземпляр.
* Игнорировать данные и оставить экземпляр как есть.
* Вызвать ошибку валидации.

Вот пример метода `.update()` для нашего предыдущего класса `UserSerializer`.

```python
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

Поскольку поведение вложенных созданий и обновлений может быть неоднозначным и может требовать сложных зависимостей между связанными моделями, DRF 3 требует, чтобы вы всегда писали эти методы явно. Методы `ModelSerializer` `.create()` и `.update()` по умолчанию не включают поддержку записываемых вложенных представлений.

Однако существуют сторонние пакеты, такие как [DRF Writable Nested](serializers.md#drf-writable-nested), которые поддерживают автоматические записываемые вложенные представления.

#### Обработка сохранения связанных экземпляров в классах менеджера моделей

Альтернативой сохранению нескольких связанных экземпляров в сериализаторе является написание пользовательских классов менеджера модели, которые занимаются созданием нужных экземпляров.

Например, предположим, мы хотим, чтобы экземпляры `User` и `Profile` всегда создавались вместе как пара. Мы можем написать пользовательский класс менеджера, который будет выглядеть примерно так:

```python
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

Этот класс менеджера теперь более точно передает, что экземпляры пользователя и профиля всегда создаются одновременно. Наш метод `.create()` в классе сериализатора теперь может быть переписан для использования нового метода менеджера.

```python
def create(self, validated_data):
    return User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        is_premium_member=validated_data['profile']['is_premium_member'],
        has_support_contract=validated_data['profile']['has_support_contract']
    )
```

Более подробно об этом подходе смотрите документацию Django по [менеджерам моделей](https://docs.djangoproject.com/en/stable/topics/db/managers/), и [этот блогпост об использовании классов моделей и менеджеров](https://www.dabapps.com/blog/django-models-and-encapsulation/).

## Работа с несколькими объектами

Класс `Serializer` также может обрабатывать сериализацию или десериализацию списков объектов.

#### Сериализация нескольких объектов

Чтобы сериализовать кверисет или список объектов вместо одного экземпляра объекта, необходимо передать флаг `many=True` при инстанцировании сериализатора. Затем вы можете передать кверисет или список объектов для сериализации.

```python
queryset = Book.objects.all()
serializer = BookSerializer(queryset, many=True)
serializer.data
# [
#     {'id': 0, 'title': 'The electric kool-aid acid test', 'author': 'Tom Wolfe'},
#     {'id': 1, 'title': 'If this is a man', 'author': 'Primo Levi'},
#     {'id': 2, 'title': 'The wind-up bird chronicle', 'author': 'Haruki Murakami'}
# ]
```

#### Десериализация нескольких объектов

Поведение по умолчанию для десериализации нескольких объектов - это поддержка создания нескольких объектов, но не поддержка обновления нескольких объектов. Для получения дополнительной информации о том, как поддержать или настроить любой из этих случаев, см. документацию по [ListSerializer](#listserializer) ниже.

## Включение дополнительного контекста

Бывают случаи, когда вам необходимо предоставить сериализатору дополнительный контекст в дополнение к сериализуемому объекту. Одним из распространенных случаев является использование сериализатора, который включает отношения с гиперссылками, что требует, чтобы сериализатор имел доступ к текущему запросу, чтобы он мог правильно генерировать полностью определенные URL.

Вы можете предоставить произвольный дополнительный контекст, передав аргумент `context` при инстанцировании сериализатора. Например:

```python
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': 'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
```

Контекстный словарь можно использовать в любой логике поля сериализатора, например, в пользовательском методе `.to_representation()`, обращаясь к атрибуту `self.context`.

---

# ModelSerializer

Часто вам понадобятся классы сериализаторов, которые близко сопоставляются с определениями моделей Django.

Класс `ModelSerializer` предоставляет ярлык, позволяющий автоматически создать класс `Serializer` с полями, соответствующими полям модели.

**Класс `ModelSerializer` такой же, как и обычный класс `Serializer`, за исключением того, что**:

* Он автоматически сгенерирует для вас набор полей на основе модели.
* Он автоматически генерирует валидаторы для сериализатора, такие как валидаторы unique_together.
* Он включает простые реализации по умолчанию `.create()` и `.update()`.

Объявление `ModelSerializer` выглядит следующим образом:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

По умолчанию все поля модели класса будут отображены на соответствующие поля сериализатора.

Любые отношения, такие как внешние ключи в модели, будут отображены на `PrimaryKeyRelatedField`. Обратные отношения не включаются по умолчанию, если они не включены явно, как указано в документации [serializer relations](relations.md).

#### Проверка `ModelSerializer`.

Классы сериализаторов генерируют полезные строки представления, которые позволяют полностью просмотреть состояние их полей. Это особенно полезно при работе с `ModelSerializers`, когда вы хотите определить, какой набор полей и валидаторов автоматически создается для вас.

Для этого откройте оболочку Django, используя `python manage.py shell`, затем импортируйте класс сериализатора, инстанцируйте его и выведите представление объекта...

```python
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

## Указание, какие поля включать

Если вы хотите, чтобы в сериализаторе модели использовалось только подмножество полей по умолчанию, вы можете сделать это с помощью опций `fields` или `exclude`, как и в случае с `ModelForm`. Настоятельно рекомендуется явно задавать все поля, которые должны быть сериализованы, с помощью атрибута `fields`. Это уменьшит вероятность непреднамеренного раскрытия данных при изменении ваших моделей.

Например:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

Вы также можете установить для атрибута `fields` специальное значение `'__all__'`, чтобы указать, что должны использоваться все поля в модели.

Например:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
```

Вы можете установить атрибут `exclude` в список полей, которые должны быть исключены из сериализатора.

Например:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['users']
```

В приведенном выше примере, если модель `Account` имеет 3 поля `account_name`, `users` и `created`, это приведет к тому, что поля `account_name` и `created` будут сериализованы.

Имена в атрибутах `fields` и `exclude` обычно отображаются на поля модели в классе модели.

Альтернативные имена в опциях `fields` могут отображаться на свойства или методы, не принимающие аргументов, которые существуют в классе модели.

Начиная с версии 3.3.0, **обязательным** является предоставление одного из атрибутов `fields` или `exclude`.

## Указание вложенной сериализации

По умолчанию `ModelSerializer` использует первичные ключи для отношений, но вы также можете легко генерировать вложенные представления с помощью опции `depth`:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        depth = 1
```

Параметр `depth` должен быть установлен в целочисленное значение, которое указывает глубину отношений, которые должны быть пройдены перед возвратом к плоскому представлению.

Если вы хотите настроить способ сериализации, вам нужно будет определить поле самостоятельно.

## Указание полей в явном виде

Вы можете добавить дополнительные поля в `ModelSerializer` или переопределить поля по умолчанию, объявив поля в классе, как и в классе `Serializer`.

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
        fields = ['url', 'groups']
```

Дополнительные поля могут соответствовать любому свойству или вызываемому объекту модели.

## Указание полей, доступных только для чтения

Вы можете указать несколько полей как доступные только для чтения. Вместо того чтобы добавлять каждое поле явно с атрибутом `read_only=True`, вы можете использовать сокращенную опцию Meta, `read_only_fields`.

Этот параметр должен представлять собой список или кортеж имен полей и объявляется следующим образом:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name']
```

Поля модели, для которых установлено значение `editable=False`, и поля `AutoField` по умолчанию будут установлены в режим только для чтения, и их не нужно добавлять в опцию `read_only_fields`.

---

**Примечание**: Существует особый случай, когда поле, доступное только для чтения, является частью ограничения `unique_together` на уровне модели. В этом случае поле требуется классу сериализатора для проверки ограничения, но также не должно редактироваться пользователем.

Правильный способ справиться с этим - явно указать поле в сериализаторе, предоставив именованные аргументы `read_only=True` и `default=...`.

Одним из примеров этого является отношение только для чтения к текущему аутентифицированному `User`, который является `unique_together` с другим идентификатором. В этом случае вы объявите поле пользователя следующим образом:

```python
user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
```

Пожалуйста, ознакомьтесь с документацией [Validators Documentation](validators.md) для получения подробной информации о классах [UniqueTogetherValidator](validators.md#uniquetogethervalidator) и [CurrentUserDefault](validators.md#currentuserdefault).

---

## Дополнительные именованные аргументы

Также есть возможность указать произвольные дополнительные именованные аргументы для полей, используя опцию `extra_kwargs`. Как и в случае с `read_only_fields`, это означает, что вам не нужно явно объявлять поле в сериализаторе.

Эта опция представляет собой словарь, отображающий имена полей на словарь именованных аргументов. Например:

```python
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

Следует помнить, что если поле уже было явно объявлено в классе сериализатора, то опция `extra_kwargs` будет проигнорирована.

## Реляционные поля

При сериализации экземпляров модели существует несколько различных способов представления отношений. Представление по умолчанию для `ModelSerializer` заключается в использовании первичных ключей связанных экземпляров.

Альтернативные представления включают сериализацию с помощью гиперссылок, сериализацию полных вложенных представлений или сериализацию с помощью пользовательского представления.

Более подробную информацию можно найти в документации [serializer relations](relations.md).

## Настройка сопоставлений полей

Класс ModelSerializer также предоставляет API, который вы можете переопределить, чтобы изменить способ автоматического определения полей сериализатора при инстанцировании сериализатора.

Обычно, если `ModelSerializer` не генерирует нужные вам поля по умолчанию, вы должны либо добавить их в класс явно, либо просто использовать вместо них обычный класс `Serializer`. Однако в некоторых случаях вы можете захотеть создать новый базовый класс, определяющий, как создаются поля сериализатора для любой конкретной модели.

### `serializer_field_mapping`.

Отображение полей модели Django на поля сериализатора DRF. Вы можете переопределить это отображение, чтобы изменить поля сериализатора по умолчанию, которые должны использоваться для каждого поля модели.

### `serializer_related_field`.

Это свойство должно быть классом поля сериализатора, который по умолчанию используется для реляционных полей.

Для `ModelSerializer` это значение по умолчанию равно `serializers.PrimaryKeyRelatedField`.

Для `HyperlinkedModelSerializer` это значение по умолчанию равно `serializers.HyperlinkedRelatedField`.

### `serializer_url_field`.

Класс поля сериализатора, который должен использоваться для любого поля `url` в сериализаторе.

По умолчанию `serializers.HyperlinkedIdentityField`.

### `serializer_choice_field`

Класс поля сериализатора, который должен использоваться для любых полей выбора в сериализаторе.

По умолчанию `serializers.ChoiceField`.

### API field_class и field_kwargs

Следующие методы вызываются для определения класса и именованных аргументов для каждого поля, которое должно быть автоматически включено в сериализатор. Каждый из этих методов должен возвращать кортеж `(field_class, field_kwargs)`.

### `build_standard_field(self, field_name, model_field)`.

Вызывается для генерации поля сериализатора, которое сопоставляется со стандартным полем модели.

Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_field_mapping`.

### `build_relational_field(self, field_name, relation_info)`.

Вызывается для генерации поля сериализатора, которое сопоставляется с полем реляционной модели.

Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_related_field`.

Аргумент `relation_info` представляет собой именованный кортеж, содержащий свойства `model_field`, `related_model`, `to_many` и `has_through_model`.

### `build_nested_field(self, field_name, relation_info, nested_depth)`.

Вызывается для генерации поля сериализатора, которое сопоставляется с полем реляционной модели, если установлен параметр `depth`.

Реализация по умолчанию динамически создает вложенный класс сериализатора на основе `ModelSerializer` или `HyperlinkedModelSerializer`.

Значение `nested_depth` будет равно значению опции `depth`, минус один.

Аргумент `relation_info` представляет собой именованный кортеж, содержащий свойства `model_field`, `related_model`, `to_many` и `has_through_model`.

### `build_property_field(self, field_name, model_class)`.

Вызывается для генерации поля сериализатора, которое сопоставляется со свойством или методом с нулевым аргументом класса модели.

Реализация по умолчанию возвращает класс `ReadOnlyField`.

### `build_url_field(self, field_name, model_class)`.

Вызывается для генерации поля сериализатора для собственного поля сериализатора `url`. Реализация по умолчанию возвращает класс `HyperlinkedIdentityField`.

### `build_unknown_field(self, field_name, model_class)`.

Вызывается, когда имя поля не сопоставлено ни с одним полем модели или свойством модели. Реализация по умолчанию вызывает ошибку, хотя подклассы могут настраивать это поведение.

---

# HyperlinkedModelSerializer

Класс `HyperlinkedModelSerializer` похож на класс `ModelSerializer`, за исключением того, что он использует гиперссылки для представления отношений, а не первичные ключи.

По умолчанию сериализатор будет включать поле `url` вместо поля первичного ключа.

Поле url будет представлено с помощью поля сериализатора `HyperlinkedIdentityField`, а любые отношения в модели будут представлены с помощью поля сериализатора `HyperlinkedRelatedField`.

Вы можете явно включить первичный ключ, добавив его, например, в опцию `fields`:

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'account_name', 'users', 'created']
```

## Абсолютные и относительные URL-адреса

При инстанцировании `HyperlinkedModelSerializer` вы должны включить текущий `request` в контекст сериализатора, например:

```python
serializer = AccountSerializer(queryset, context={'request': request})
```

Это гарантирует, что гиперссылки будут содержать соответствующее имя хоста, чтобы в результирующем представлении использовались полные URL-адреса, например:

```python
http://api.example.com/accounts/1/
```

Вместо относительных URL-адресов, таких как:

```python
/accounts/1/
```

Если вы *хотите* использовать относительные URL, вы должны явно передать `{'request': None}` в контексте сериализатора.

## Как определяются представления с гиперссылками

Необходимо определить, какие представления следует использовать для гиперссылок на экземпляры модели.

По умолчанию ожидается, что гиперссылки будут соответствовать имени представления, которое соответствует стилю `'{имя_модели}-detail'`, и ищет экземпляр по именованному аргументу `pk`.

Вы можете переопределить имя представления поля URL и поле поиска, используя один или оба параметра `view_name` и `lookup_field` в параметре `extra_kwargs`, как показано ниже:

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['account_url', 'account_name', 'users', 'created']
        extra_kwargs = {
            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'users': {'lookup_field': 'username'}
        }
```

В качестве альтернативы вы можете явно задать поля в сериализаторе. Например:

```python
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

**Совет**: Правильное согласование гиперссылочных представлений и вашего URL conf иногда может быть немного сложным. Печать `repr` экземпляра `HyperlinkedModelSerializer` - особенно полезный способ проверить, какие именно имена представлений и поля поиска должны отображать отношения.

---

## Изменение имени поля URL

Имя поля URL по умолчанию равно 'url'. Вы можете переопределить его глобально, используя параметр `URL_FIELD_NAME`.

---

# ListSerializer

Класс `ListSerializer` обеспечивает поведение для сериализации и валидации нескольких объектов одновременно. Обычно вам не нужно использовать `ListSerializer` напрямую, а следует просто передать `many=True` при инстанцировании сериализатора.

При инстанцировании сериализатора и передаче `many=True` будет создан экземпляр `ListSerializer`. Затем класс сериализатора становится дочерним классом родительского `ListSerializer`.

Следующий аргумент также может быть передан полю `ListSerializer` или сериализатору, которому передано `many=True`:

### `allow_empty`

По умолчанию это `True`, но может быть установлено в `False`, если вы хотите запретить пустые списки в качестве допустимого ввода.

### `max_length`

По умолчанию это `None`, но может быть установлено в положительное целое число, если вы хотите проверить, что список содержит не более этого количества элементов.

### `min_length`

По умолчанию это `None`, но может быть установлено в положительное целое число, если вы хотите проверить, что список содержит не менее этого количества элементов.

### Настройка поведения `ListSerializer`.

*Существует* несколько случаев, когда вы захотите настроить поведение `ListSerializer`. Например:

* Вы хотите обеспечить определенную проверку списков, например, проверить, что один элемент не конфликтует с другим элементом списка.
* Вы хотите настроить поведение создания или обновления нескольких объектов.

Для этих случаев вы можете изменить класс, который используется при передаче `many=True`, используя опцию `list_serializer_class` для класса сериализатора `Meta`.

Например:

```python
class CustomListSerializer(serializers.ListSerializer):
    ...

class CustomSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = CustomListSerializer
```

#### Настройка множественного создания

Реализация по умолчанию для создания нескольких объектов заключается в простом вызове `.create()` для каждого элемента списка. Если вы хотите настроить это поведение, вам нужно настроить метод `.create()` класса `ListSerializer`, который используется, когда передается `many=True`.

Например:

```python
class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [Book(**item) for item in validated_data]
        return Book.objects.bulk_create(books)

class BookSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = BookListSerializer
```

#### Настройка многократного обновления

По умолчанию класс `ListSerializer` не поддерживает множественные обновления. Это связано с тем, что поведение, которое следует ожидать для вставок и удалений, неоднозначно.

Для поддержки нескольких обновлений необходимо сделать это явно. При написании кода множественных обновлений обязательно учитывайте следующее:

* Как определить, какой экземпляр должен быть обновлен для каждого элемента в списке данных?
* Как следует обрабатывать вставки? Являются ли они недействительными, или они создают новые объекты?
* Как следует обрабатывать удаления? Означают ли они удаление объекта или удаление отношения? Следует ли их молча игнорировать, или они недействительны?
* Как следует обрабатывать упорядочивание? Влечет ли изменение положения двух объектов изменение состояния или оно игнорируется?

Вам нужно будет добавить явное поле `id` в сериализатор экземпляра. По умолчанию неявно генерируемое поле `id` помечено как `read_only`. Это приводит к тому, что оно удаляется при обновлении. Как только вы объявите его явно, оно будет доступно в методе `update` сериализатора списка.

Вот пример того, как можно реализовать несколько обновлений:

```python
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

#### Настройка инициализации ListSerializer

Когда инстанцируется сериализатор с `many=True`, нам необходимо определить, какие аргументы и ключевые слова следует передать в метод `.__init__()` как для дочернего класса `Serializer`, так и для родительского класса `ListSerializer`.

По умолчанию все аргументы передаются обоим классам, за исключением `validators` и любых пользовательских именованных аргументов, которые, как предполагается, предназначены для дочернего класса сериализатора.

Иногда вам может понадобиться явно указать, как дочерний и родительский классы должны быть инстанцированы при передаче `many=True`. Вы можете сделать это с помощью метода класса `many_init`.

```python
@classmethod
def many_init(cls, *args, **kwargs):
    # Instantiate the child serializer.
    kwargs['child'] = cls()
    # Instantiate the parent list serializer.
    return CustomListSerializer(*args, **kwargs)
```

---

# BaseSerializer

Класс `BaseSerializer`, который можно использовать для простой поддержки альтернативных стилей сериализации и десериализации.

Этот класс реализует тот же базовый API, что и класс `Serializer`:

* `.data` - Возвращает исходящее примитивное представление.
* `.is_valid()` - Десериализует и проверяет входящие данные.
* `.validated_data` - Возвращает проверенные входящие данные.
* `.errors` - Возвращает любые ошибки во время валидации.
* `.save()` - Сохраняет проверенные данные в экземпляре объекта.

Есть четыре метода, которые могут быть переопределены, в зависимости от того, какую функциональность вы хотите, чтобы поддерживал класс сериализатора:

* `.to_representation()` - Переопределить это для поддержки сериализации, для операций чтения.
* `.to_internal_value()` - Переопределить это для поддержки десериализации, для операций записи.
* `.create()` и `.update()` - Переопределите один из этих параметров или оба для поддержки сохранения экземпляров.

Поскольку этот класс предоставляет тот же интерфейс, что и класс `Serializer`, вы можете использовать его с существующими общими представлениями на основе классов точно так же, как и обычный `Serializer` или `ModelSerializer`.

Единственное отличие, которое вы заметите при этом - классы `BaseSerializer` не будут генерировать HTML-формы в Web-интерфейсе API. Это происходит потому, что данные, которые они возвращают, не включают всю информацию о полях, которая позволит преобразовать каждое поле в подходящий HTML-ввод.

#### Классы `BaseSerializer` только для чтения.

Чтобы реализовать сериализатор только для чтения, используя класс `BaseSerializer`, нам просто нужно переопределить метод `.to_representation()`. Давайте рассмотрим пример на примере простой модели Django:

```python
class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()
```

Очень просто создать сериализатор только для чтения для преобразования экземпляров `HighScore` в примитивные типы данных.

```python
class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }
```

Теперь мы можем использовать этот класс для сериализации отдельных экземпляров `HighScore`:

```python
@api_view(['GET'])
def high_score(request, pk):
    instance = HighScore.objects.get(pk=pk)
    serializer = HighScoreSerializer(instance)
    return Response(serializer.data)
```

Или используйте его для сериализации нескольких экземпляров:

```python
@api_view(['GET'])
def all_high_scores(request):
    queryset = HighScore.objects.order_by('-score')
    serializer = HighScoreSerializer(queryset, many=True)
    return Response(serializer.data)
```

#### Классы `BaseSerializer` с функцией чтения-записи

Для создания сериализатора чтения-записи нам сначала нужно реализовать метод `.to_internal_value()`. Этот метод возвращает проверенные значения, которые будут использованы для создания экземпляра объекта, и может вызвать `serializers.ValidationError`, если предоставленные данные имеют неправильный формат.

Как только вы реализуете `.to_internal_value()`, базовый API валидации будет доступен в сериализаторе, и вы сможете использовать `.is_valid()`, `.validated_data` и `.errors`.

Если вы хотите также поддерживать `.save()`, вам необходимо также реализовать один или оба метода `.create()` и `.update()`.

Вот полный пример нашего предыдущего `HighScoreSerializer`, который был обновлен для поддержки операций чтения и записи.

```python
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

#### Создание новых базовых классов

Класс `BaseSerializer` также полезен, если вы хотите реализовать новые общие классы сериализаторов для работы с определенными стилями сериализации или для интеграции с альтернативными бэкендами хранения данных.

Следующий класс является примером общего сериализатора, который может обрабатывать принудительное преобразование произвольных сложных объектов в примитивные представления.

```python
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

# Расширенное использование сериализатора

## Переопределение поведения сериализации и десериализации

Если вам нужно изменить поведение сериализации или десериализации класса сериализатора, вы можете сделать это, переопределив методы `.to_representation()` или `.to_internal_value()`.

Некоторые причины, по которым это может быть полезно, включают...

* Добавление нового поведения для новых базовых классов сериализаторов.
* Небольшое изменение поведения для существующего класса.
* Улучшение производительности сериализации для часто используемой конечной точки API, которая возвращает много данных.

Подписи для этих методов следующие:

#### `to_representation(self, instance)`.

Принимает экземпляр объекта, который требует сериализации, и должен вернуть примитивное представление. Обычно это означает возврат структуры встроенных в Python типов данных. Точные типы, которые могут быть обработаны, зависят от классов рендеринга, которые вы настроили для своего API.

Может быть переопределена для изменения стиля представления. Например:

```python
def to_representation(self, instance):
    """Convert `username` to lowercase."""
    ret = super().to_representation(instance)
    ret['username'] = ret['username'].lower()
    return ret
```

#### `to_internal_value(self, data)`.

Принимает невалидированные входящие данные в качестве входных и должен вернуть валидированные данные, которые будут доступны как `serializer.validated_data`. Возвращаемое значение также будет передано в методы `.create()` или `.update()`, если для класса сериализатора будет вызван `.save()`.

Если какая-либо из валидаций не прошла, то метод должен вызвать `serializers.ValidationError(errors)`. Аргумент `errors` должен представлять собой словарь, отображающий имена полей (или `settings.NON_FIELD_ERRORS_KEY`) на список сообщений об ошибках. Если вам не нужно изменять поведение десериализации и вместо этого вы хотите обеспечить проверку на уровне объекта, рекомендуется переопределить метод [`.validate()`](#валидация-на-уровне-объекта).

Аргумент `data`, передаваемый этому методу, обычно является значением `request.data`, поэтому тип данных, который он предоставляет, будет зависеть от классов парсера, которые вы настроили для своего API.

## Наследование сериализатора

Подобно формам Django, вы можете расширять и повторно использовать сериализаторы с помощью наследования. Это позволяет вам объявить общий набор полей или методов в родительском классе, который затем может быть использован в нескольких сериализаторах. Например,

```python
class MyBaseSerializer(Serializer):
    my_field = serializers.CharField()

    def validate_my_field(self, value):
        ...

class MySerializer(MyBaseSerializer):
    ...
```

Как и классы `Model` и `ModelForm` в Django, внутренний класс `Meta` в сериализаторах не наследуется неявно от внутренних классов `Meta` своих родителей. Если вы хотите, чтобы класс `Meta` наследовался от родительского класса, вы должны сделать это явно. Например:

```python
class AccountSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        model = Account
```

Обычно мы рекомендуем *не* использовать наследование для внутренних классов Meta, а вместо этого объявлять все опции явно.

Кроме того, следующие предостережения относятся к наследованию сериализаторов:

* Применяются обычные правила разрешения имен Python. Если у вас есть несколько базовых классов, которые объявляют внутренний класс `Meta`, будет использоваться только первый класс. Это означает дочерний `Meta`, если он существует, иначе `Meta` первого родителя и т.д.
* Можно декларативно удалить `Field`, унаследованный от родительского класса, указав значение `None` в подклассе.

```python
class MyBaseSerializer(ModelSerializer):
    my_field = serializers.CharField()

class MySerializer(MyBaseSerializer):
    my_field = None
```

Однако вы можете использовать эту технику только для отказа от поля, определенного декларативно родительским классом; это не помешает `ModelSerializer` сгенерировать поле по умолчанию. Чтобы отказаться от полей по умолчанию, смотрите [Указание, какие поля включать](#указание-какие-поля-включать).

## Динамическое изменение полей

После инициализации сериализатора, к словарю полей, установленных в сериализаторе, можно получить доступ с помощью атрибута `.fields`. Доступ и изменение этого атрибута позволяет динамически модифицировать сериализатор.

Изменение аргумента `fields` напрямую позволяет вам делать такие интересные вещи, как изменение аргументов полей сериализатора во время выполнения, а не в момент объявления сериализатора.

### Пример

Например, если вы хотите иметь возможность установить, какие поля должны использоваться сериализатором в момент его инициализации, вы можете создать класс сериализатора следующим образом:

```python
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

Это позволит вам сделать следующее:

```python
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

## Настройка полей по умолчанию

REST framework 2 предоставил API, позволяющий разработчикам переопределять, как класс `ModelSerializer` будет автоматически генерировать набор полей по умолчанию.

Этот API включал методы `.get_field()`, `.get_pk_field()` и другие.

Поскольку сериализаторы были кардинально переработаны в версии 3.0, этот API больше не существует. Вы все еще можете изменять создаваемые поля, но вам придется обратиться к исходному коду, и имейте в виду, что если изменения, которые вы делаете, направлены против частных частей API, то они могут быть изменены.

---

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## Django REST marshmallow

Пакет [django-rest-marshmallow](https://marshmallow-code.github.io/django-rest-marshmallow/) предоставляет альтернативную реализацию сериализаторов, используя библиотеку python [marshmallow](https://marshmallow.readthedocs.io/en/latest/). Он предоставляет тот же API, что и сериализаторы DRF, и может быть использован в качестве замены в некоторых случаях.

## Serpy

Пакет [serpy](https://github.com/clarkduvall/serpy) - это альтернативная реализация сериализаторов, созданная для скорости. [Serpy](https://github.com/clarkduvall/serpy) сериализует сложные типы данных в простые нативные типы. Родные типы могут быть легко преобразованы в JSON или любой другой необходимый формат.

## MongoengineModelSerializer

Пакет [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) предоставляет класс сериализатора `MongoEngineModelSerializer`, который поддерживает использование MongoDB в качестве уровня хранения данных для DRF.

## GeoFeatureModelSerializer

Пакет [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) предоставляет класс сериализатора `GeoFeatureModelSerializer`, который поддерживает GeoJSON как для операций чтения, так и для записи.

## HStoreSerializer

Пакет [django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) предоставляет `HStoreSerializer` для поддержки поля модели [django-hstore](https://github.com/djangonauts/django-hstore) `DictionaryField` и его функции `chema-mode`.

## Dynamic REST

Пакет [dynamic-rest](https://github.com/AltSchool/dynamic-rest) расширяет интерфейсы ModelSerializer и ModelViewSet, добавляя параметры запроса API для фильтрации, сортировки, включения/исключения всех полей и отношений, определенных вашими сериализаторами.

## Dynamic Fields Mixin

Пакет [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) предоставляет миксин для динамического ограничения полей для сериализатора подмножеством, заданным параметром URL.

## DRF FlexFields

Пакет [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) расширяет ModelSerializer и ModelViewSet для обеспечения широко используемой функциональности для динамической установки полей и расширения примитивных полей во вложенные модели, как из параметров URL, так и из определений класса вашего сериализатора.

## Serializer Extensions

Пакет [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) предоставляет набор инструментов для DRY up ваших сериализаторов, позволяя определять поля на основе каждого представления/запроса. Поля могут быть внесены в белый или черный список, а дочерние сериализаторы могут быть расширены по желанию.

## HTML JSON Forms

Пакет [html-json-forms](https://github.com/wq/html-json-forms) предоставляет алгоритм и сериализатор для обработки `<form>` в соответствии с (неактивной) [спецификацией HTML JSON Form](https://www.w3.org/TR/html-json-forms/). Сериализатор облегчает обработку произвольно вложенных структур JSON в HTML. Например, `<input name="items[0][id]" value="5">` будет интерпретирован как `{"items": [{"id": "5"}]}`.

## DRF-Base64

[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64) предоставляет набор сериализаторов полей и моделей, который обрабатывает загрузку файлов в base64-кодировке.

## QueryFields

[djangorestframework-queryfields](https://djangorestframework-queryfields.readthedocs.io/) позволяет клиентам API указать, какие поля будут отправлены в ответе с помощью параметров запроса включения/исключения.

## DRF Writable Nested

Пакет [drf-writable-nested](https://github.com/beda-software/drf-writable-nested) предоставляет записываемый сериализатор вложенных моделей, который позволяет создавать/обновлять модели с вложенными связанными данными.

## DRF Encrypt Content

Пакет [drf-encrypt-content](https://github.com/oguzhancelikarslan/drf-encrypt-content) помогает вам шифровать данные, сериализованные через `ModelSerializer`. Он также содержит некоторые вспомогательные функции. Это поможет вам зашифровать ваши данные.

## Shapeless Serializers

Пакет [drf-shapeless-serializers](https://github.com/khaledsukkar2/drf-shapeless-serializers) предоставляет возможности динамической настройки сериализатора, позволяя выбирать поля во время выполнения, переименовывать их, изменять атрибуты и настраивать вложенные отношения без создания нескольких классов сериализатора. Это помогает устранить шаблонные коды сериализатора и обеспечивает гибкие ответы API.
