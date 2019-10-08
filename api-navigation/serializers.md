# Cериализаторы
>Нам бы очень хотелось расширить применение сериализаторов, но это не тривиальная пробема, и она требует серьезной работы.

— Russell Keith-Magee, Django users group

Сериализаторы позволяют преобразовывать сложные данные, такие как querysets и экземпляры моделей, в нативные типы данных Python, которые затем могут быть легко срендерены в JSON, XML или другие типы контента. Сериализаторы также обеспечивают десериализацию, позволяя преобразовать спарсенные данные обратно в сложные типы после проверки входящих данных.

Сериализаторы в REST framework работают аналогично классам Django `Form` и `ModelForm`. Мы предоставляем класс `Serializer`, который дает вам мощный, общий способ управления вашими ответами, а также класс `ModelSerializer`-  полезный и быстрый способ создания сериализаторов, которые имеют дело с экземплярами модели и querysets.

## Объявление сериализаторов
Сперва создадим простой проект, на котором будем демонстрировать примеры:

```python
from datetime import datetime

class Comment(object):
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

На этом этапе мы преобразовали экземпляр модели в нативные типы данных Python. Чтобы завершить процесс сериализации, мы рендерим данные в `json`.

```python
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
```



## Десериализация объектов 
Аналогично проходит десериализация. Сначала мы парсиим поток в натинвые типы данных Python ...

```python
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

stream = BytesIO(json)
data = JSONParser().parse(stream)
```


...затем мы сохраняем эти нативные типы данных в словарь валидных данных.

```python
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
```

## Сохранение экземпляров

Если мы хотим иметь возможность возвращать полные экземпляры объектов на основе проверенных данных, нам нужно реализовать один или оба метода `.create()` и `update()`. Например:


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
Если экземпляры объектов соответствуют моделям Django, то вам также нужнр убедиться, что эти методы сохраняют объект в базе данных. Например, если `Comment` был моделью Django, методы могут выглядеть так:

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

Теперь при десериализации данных мы можем вызвать `.save()`, чтобы вернуть экземпляр объекта на основе проверенных данных.
```python
comment = serializer.save()
```

При вызове `.save()` будет создаваться либо новый экземпляр, либо обновляться существующий экземпляр, в зависимости от того, был ли передан существующий экземпляр при создании экземпляра класса сериализатора:

```python
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)
```


Оба метода `.create()` и `.update()` являются необязательными. Вы можете применять их вмете, по отдельности, либо вообще отказаться от них, в зависимости от конкретного случая использования вашего класса сериализатора.

### Передача дополнительных атрибутов в `.save()`

Иногда вам нужно, чтобы код представления мог добавлять дополнительные данные в момент сохранения экземпляра. Эти дополнительные данные могут включать в себя информацию, такую как текущий пользователь, текущее время или что-либо еще, что не является частью данных запроса.

Вы можете сделать это, указав дополнительные аргументы ключевого слова при вызове `.save().` Например:

```python
serializer.save(owner=request.user)
```
Любые дополнительные аргументы ключевого слова будут включены в аргумент `validated_data` при вызове `.create()` или `.update()`.
### Переопределение .save() напрямую.

В некоторых случаях имена методов `.create()` и `.update()` могут не иметь смысла. Например, в форме контакта мы можем не создавать новые экземпляры, а вместо этого отправлять электронную почту или другое сообщение.

В этих случаях вы можете переопределить `.save()` напрямую, в целях читабельности и прозрачности.

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

Обратите внимание, что в приведенном выше случае нам теперь нужно напрямую получить доступ к свойству `serialval.validated_data.`

## Проверка(Validation)
При десериализации данных вам всегда нужно вызвать` is_valid()`, прежде чем пытаться получить доступ к проверенным данным или сохранить экземпляр объекта. Если возникнут какие-либо ошибки проверки, свойство `.errors` будет содержать словарь, представляющий сообщения об ошибках. Например:

```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': [u'Enter a valid e-mail address.'], 'created': [u'This field is required.']}
```


Каждый ключ в словаре будет именем поля, а значениями будут списками строк любых сообщений об ошибках, соответствующих этому полю. Также может присутствовать ключ `non_field_errors`, который  перечисляет любые общие ошибки валидности. Имя ключа `non_field_errors` может быть настроено с использованием параметра N`ON_FIELD_ERRORS_KEY REST`.

При десериализации списка элементов ошибки будут возвращаться в виде списка словарей, представляющих каждый из десериализованных элементов.

### Получение исключения по недействительным данным

Метод `.is_valid()` принимает необязательный флаг `raise_exception`, который заставит его вызвать исключение `serializers.ValidationError`, в случае, если есть ошибки проверки.

Эти исключения автоматически обрабатываются обработчиком исключений, который предоставляет REST framework, и будет возвращать ответы `HTTP 400 Bad Request` по умолчанию.

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

### Проверка на уровне поля

Вы можете указать настраиваемую проверку на уровне поля, добавив методы `.validate_<field_name>` в ваш подкласс `Serializer`. Они аналогичны методам `.clean_<field_name>` в формах Django.

Эти методы принимают один аргумент, который является значением поля, требующим проверки.

Методы `.validate_<field_name>` должны возвращать проверенное значение или вызывать `serializers.ValidationError`. Например:

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

**Примечание.** Если ваш `<field_name>` объявлен в вашем сериализаторе с параметром `required = False`, то этот шаг проверки не будет выполняться, если поле не включено.


### Проверка на уровне объекта

Чтобы выполнить любую другую проверку, требующую доступа к нескольким полям, добавьте метод под названием `.validate()` в ваш подкласс `Serializer`. Этот метод принимает один аргумент, который является словарем значений полей. При необходимости он должен вызвать `serializers.ValidationError` или просто вернуть проверенные значения. Например:

```python
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```


### Валидаторы

В отдельные поля в сериализаторе можно включить валидаторы, объявив их в экземпляре поля, например:
```python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...
```

Классы сериализаторов могут также включать повторно используемые валидаторы, которые применяются к полному набору данных поля. Эти валидаторы подключаются путем объявления их во внутреннем мета-классе, например:

```python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # Each room only has one event per day.
        validators = UniqueTogetherValidator(
            queryset=Event.objects.all(),
            fields=['room_number', 'date']
        )
```


## Доступ к исходным данным и экземпляру

При передаче исходного объекта или queryset в экземпляр сериализатора объект будет доступен как `.instance`. Если не было передано никакого начального объекта, то атрибут `.instance` будет None.

При передаче данных в экземпляр сериализатора немодифицированные данные будут доступны как `.initial_data`. Если аргумент ключевого слова данных не передается, атрибут `.initial_data` не будет создан.

## Частичные обновления
По умолчанию, сериализаторам должны быть переданы значения для всех обязательных полей, в противном случае они вызовут ошибку валидации. Вы можете использовать аргумент `partial`, чтобы разрешить частичные обновления.
```python
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)
```

## Работа с вложенными объектами
Предыдущие примеры хорошо подходят для работы с объектами, которые имеют только простые типы данных, но иногда нам также нужно иметь возможность представлять более сложные объекты, где некоторые атрибуты объекта могут быть не простыми типами данных, такими как строки, даты или целые числа.

Класс `Serializer` сам по себе является типом `Field` и может использоваться для представления отношений, в которых один тип объекта вложен внутри другого.

```python

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Если вложенное представление может опционально принимать значение `None`, вы должны передать флаг `required = False` вложенному сериализатору.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

Аналогично, если вложенное представление должно быть списком элементов, вы должны передать флаг `many = True` вложенному сериализатору.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```


## Writable вложенные представления
При работе с вложенными представлениями, которые поддерживают десериализацию данных, любые ошибки с вложенными объектами будут вложены под именем поля вложенного объекта.
```python
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': [u'Enter a valid e-mail address.']}, 'created': [u'This field is required.']}
```

Аналогично, свойство `.validated_data` будет включать вложенные структуры данных.

### Написание методов `.create()` для вложенных представлений

Если вы собираетесь поддерживать writable вложенные представления, вам потребуется написать методы `.create()` или .`update()`, которые обрабатывают сохранение нескольких объектов.

В следующем примере показано, как можно обрабатывать создание пользователя с вложенным объектом профиля.

```python
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
```

### Написание методов .update() для вложенных представлений

Вам нужно будет тщательно подумать о том, как обрабатывать обновления отношений. Например, что из следующего должно произойти, если данные отношений раняются `None`?

* Отношение устанавливается как NULL в базе данных.
* Связянный экземпляр удаляется.
* Данные игнорируются и экземпляр остается таким, какой он есть.
* Вызов ошибки проверки.

Ниже приведен пример метода `update()` на основе нашего `UserSerializer`.


```python
def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
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

Поскольку поведение вложенных create и update может быть неоднозначным и требующим зависимостей между связанными моделями, REST framework 3 требует, чтобы вы всегда записывали эти методы явно. Стандартные методы `ModelSerializer` `.create()` и `.update()` не включают поддержку writable вложенных представлений.



## Обработка связанных с сохранением экземпляров в классах менеджера моделей

Альтернативой сохранению нескольких связанных экземпляров в сериализаторе является создание пользовательских классов диспетчера моделей, которые обрабатывают создание правильных экземпляров.

Предположим, что нам нужно убедиться, что экземпляры `User` и экземпляры `Profile` всегда создаются парно. Мы могли бы написать собственный класс менеджера, который выглядел бы примерно так:

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

Этот класс менеджера теперь лучше инкапсулирует, что экземпляры пользователей и экземпляры профиля всегда создаются одновременно. Наш метод `.create() `в классе сериализатора теперь может быть переписан для использования нового метода менеджера.

```python

def create(self, validated_data):
    return User.objects.create(
        username=validated_data['username'],
        email=validated_data['email']
        is_premium_member=validated_data['profile']['is_premium_member']
        has_support_contract=validated_data['profile']['has_support_contract']
    )
```

Для дополнительной информации по данному методу см докумениацию Джанго по [менеджерам моделей](https://docs.djangoproject.com/en/1.11/topics/db/managers/), а также [этот пост](https://www.dabapps.com/blog/django-models-and-encapsulation/), посвященный использованию классов моделей и менеджеров.

## Работа с несколькими объектами
Класс `Serializer` также может обрабатывать сериализацию или десериализацию списков объектов.

### Сериализация нескольких объектов

Чтобы сериализовать queryset или список объектов вместо экземпляра одного объекта, вы должны передать флаг `many = True` при создании экземпляра сериализатора. Затем вы можете передать queryset или список объектов для сериализации.

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


### Десериализация нескольких объектов

Стандартный процесс десериализации нескольких объектов поддерживает создание нескольких объектов, но не поддреживает обновление нескольких объектов. Дополнительные сведения о поддержке или настройке любого из этих случаев см в ListSerializer ниже.

## Включение дополнительного контекста
В некоторых случаях вам необходимо предоставить дополнительный контекст для сериализатора в дополнение к сериализуемому объекту. Распространенный случай, когда вы используете сериализатор, который включает в себя отношения-гиперссылки, это подразумевает, что сериализатор имеет доступ к текущему запросу, чтобы он мог правильно генерировать полные URL-адреса.

Вы можете предоставить произвольный дополнительный контекст, передав аргумент `context` при создании экземпляра сериализатора. Например:

```python
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': u'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
```


Словарь контекста может использоваться в любой логике поля сериализатора, такой как пользовательский метод `.to_representation()`, путем доступа к атрибуту `self.context`.


# ModelSerializer

Часто вам нужны классы сериализатора, которые тесно связаны с определениями моделей Django.

Класс `ModelSerializer` позволяет автоматически создавать класс `Serializer` с полями, соответствующими полям Model.

Класс `ModelSerializer` совпадает с обычным классом `Serializer`, за исключением того, что:

* Он автоматически генерирует набор полей на основе модели.
* Он автоматически генерирует валидаторы для сериализатора, такие как `unique_together`.
* Он включает простые стандартные реализации `.create()` и `.update()`.

Объявление `ModelSerializer` выглядит так:

```python

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
```

По умолчанию все поля модели в классе будут сопоставлены с соответствующими полями сериализатора.

Любые отношения, такие как внешние ключи модели, будут сопоставлены с `PrimaryKeyRelatedField`. Обратные отношения не включаются по умолчанию, если только это не сделано явно, как указано в документации по отношениям сериализатора.

## Проверка ModelSerializer

Классы сериализатора генерируют полезные verbose строки представления, которые позволяют вам полностью проверить состояние ваших полей. Это особенно полезно при работе с `ModelSerializers`, где вы хотите определить, какой набор полей и валидаторов автоматически создается для вас.

Для этого откройте оболочку Django, используя `python manage.py shell`, затем импортируйте класс сериализатора, создайте экземпляр и выполните print представления объекта ...

```print
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

## Определение полей для включения 
Если вы хотите, чтобы подмножество полей по умолчанию использовалось в модельном сериализаторе, то можете сделать используя опции `fields` или `exclude`, аналогично тому, как бы вы это сделали с `ModelForm`. Настоятельно рекомендуется явно указать все поля, которые должны быть сериализованы с использованием атрибута `fields`. Это уменьшит вероятность непреднамеренного обнародования данных при изменении ваших моделей.
Например:
```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
```


Вы также можете установить специальное значения `__all__` в качестве атрибут полей, чтобы указать, что должны использоваться все поля в модели.

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
        exclude = ('users',)
```


В приведенном выше примере, если модель `Account` имеет 3 поля` account_name`, `users`, и `created`, это приведет к тому, что резудьтат полей` account_name` и `created` будет сериализирован.

Имена в атрибутах `fields` и `exclude` обычно отображаются в полях модели в классе модели.

В качестве альтернативы имена в параметрах `fields` могут отображаться в свойствах или методах, которые не принимают аргументов, существующих в классе модели.


## Определение вложенной сериализации
По умолчанию `ModelSerializer` использует первичные ключи для отношений, но вы  можете легко создавать вложенные представления, используя параметр `depth`:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
        depth = 1
```

Параметр `depth` должен принимать целочисленное значение, указывающее глубину отношений, которые должны быть пройдены, прежде чем возвращаться к flat представлению.

Если вы хотите настроить способ сериализации, вам необходимо определить поле самостоятельно.


## Явное указание полей
Вы можете добавить дополнительные поля в `ModelSerializer` или переопределить поля по умолчанию, объявив поля в классе, аналогично тому как это делается в классе `Serializer`.

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
```

Дополнительные поля могут соответствовать любому свойству или вызываемому объекту на модели.


## Определение read only полей
Вы можете указать несколько полей только для чтения. Вместо того, чтобы явно добавлять каждое поле с атрибутом `read_only = True`, вы можете использовать опцию Meta shortcut, `read_only_fields`.

Этот параметр должен быть списком или кортежем, содержащим имя полей и объявляется следующим образом:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
        read_only_fields = ('account_name',)
```
Поля модели с `editable = False` и поля `AutoField` будут установлены по умолчанию только для чтения и не должны добавляться в параметр `read_only_fields`.

**Примечание:** Есть особый случай, когда поле только для чтения является частью ограничения `unique_together` на уровне модели. В этом случае поле требуется классу сериализатора для проверки ограничения, но также не должно быть доступно для редактирования пользователем.

Правильный способ справиться с этим - указать поле явно на сериализаторе, предоставляя как аргументы `read_only = True`, так и `default = ...`

Одним из примеров этого является read-only отношение к аутентифицированному `User`, который `unique_together` с другим идентификатором. В этом случае вы должны объявить поле пользователя следующим образом:


```python
user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
```

## Дополнительные ключевые документы
Существует также shortcut, позволяющий указать произвольные дополнительные аргументы ключевых слов в полях, используя опцию `extra_kwargs`. Как и в случае с `read_only_fields`, это означает, что вам не нужно явно объявлять поле в сериализаторе.
Этот параметр является словарем, который соотносит имена полей к словарю аргументов ключевых слов. Например:


```python
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
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

## Реляционные поля
При сериализации экземпляров модели существует несколько разных способов представления отношений. Для `ModelSerializer` представление по умолчанию заключается в использовании первичных ключей соответствующих экземпляров.

Альтернативные представления включают сериализацию с использованием гиперссылок, сериализацию полных вложенных представлений или сериализацию с пользовательским представлением.

## Настройка соотношения полей

Класс `ModelSerializer` также показывает API, который вы можете переписать для того, чтобы изменить автоматическое определение полей сериализатора при его инициализации.

Обычно, если `ModelSerializer` не генерирует поля, которые вам нужны по умолчанию, вы должны либо добавить их в класс явно, либо просто использовать обычный класс `Serializer`. Однако в некоторых случаях вам может понадобиться создать новый базовый класс, который определяет, как поля сериализатора создаются для любой модели.

```python
.serializer_field_mapping
```

Соотношение классов модели Django к классам сериализатора REST framework. Вы можете переопределить это соотношение, чтобы изменить стандартные классы сериализатора, которые должны использоваться для каждого класса модели.
```python
.serializer_related_field
```


Это свойство должно быть классом поля сериализатора, который по умолчанию используется для реляционных полей.

Для `ModelSerializer` по умолчанию используется `PrimaryKeyRelatedField`.

Для `HyperlinkedModelSerializer` это значение по умолчанию равняется `serializers.HyperlinkedRelatedField`.
```python
serializer_url_field
```

Класс поля сериализатора, который должен использоваться для любого поля `url` в сериализаторе.

По умолчанию `serializers.HyperlinkedIdentityField`
```python
serializer_choice_field
```
Класс поля сериализатора, который должен использоваться для любых полей выбора в сериализаторе.

По умолчанию `serializers.ChoiceField` 



## field_class и field_kwargs API

Следующие методы вызываются для определения аргументов класса и ключевого слова для каждого поля, которое должно автоматически включаться в сериализатор. Каждый из этих методов должен возвращать два кортежа (field_class, field_kwargs).
```python
.build_standard_field(self, field_name, model_field)
```

Вызывается для создания поля сериализатора, которое соотношается со стандартным полем модели.
Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_field_mapping`.

```python
.build_relational_field(self, field_name, relation_info)
```


Вызывается для создания поля сериализатора, которое соотносится с полем реляционной модели.

Реализация по умолчанию возвращает класс сериализатора на основе атрибута `serializer_relational_field`.

Аргумент `relation_info` - это именованный кортеж, который содержит свойства `model_field`, `related_model`, `to_many` и `through_model`.

```python
.build_nested_field(self, field_name, relation_info, nested_depth)
```

Вызывается для создания поля сериализатора, которое соотносится с полем реляционной модели, когда задан параметр `depth`.
Реализация по умолчанию динамически создает вложенный класс сериализатора на основе `ModelSerializer`, либо `HyperlinkedModelSerializer`.
Значение `nested_depth` будет принимать значение параметра `depth` минус единица.
Аргумент `relation_info` - это именованный кортеж, который содержит свойства `model_field`, `related_model`, `to_many` и `through_model`.

```python

.build_property_field(self, field_name, model_class)
```
Вызывается для создания поля сериализатора, которое соотносится с методом свойства или с нулевом аргументом в классе модели.

Реализация по умолчанию возвращает класс `ReadOnlyField`.

```python
.build_url_field(self, field_name, model_class)
```


Вызывается для создания поля сериализатора для собственного поля `url`.
Реализация по умолчнию возвращает класс `HyperlinkedIdentityField`.
```python
.build_unknown_field(self, field_name, model_class)
```

Вызывается, когда имя поля не соотносится ни с одним из полей моделей или свойством модели. По умолчанию реализация вызывает ошибку, хотя с помощью подклассов можено настраивать это поведение.

# HyperlinkedModelSerializer


Класс `HyperlinkedModelSerializer` похож на класс `ModelSerializer`, за исключением того, что для представления отношений он использует гиперссылки, а не первичные ключи.

По умолчанию сериализатор будет содержать поле url вместо поля первичного ключа.

Поле url будет представлено с использованием поля сериализатора `HyperlinkedIdentityField`, и любые отношения в модели будут представлены с использованием поля сериализатора `HyperlinkedRelatedField`.

Вы можете явно включить первичный ключ, добавив его в опцию полей, например:


```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('url', 'id', 'account_name', 'users', 'created')
```


## Абсолютные и относительные URL

При создании экземпляра `HyperlinkedModelSerializer` вы должны включить текущий запрос в контекст сериализатора, например:


```python
serializer = AccountSerializer(queryset, context={'request': request})
```

Это гарантирует, что гиперссылки могут содержать соответствующее имя хоста, таким образом в конечном представлении используются полностью определенные URL-адреса, например:



```python
http://api.example.com/accounts/1/
```

А не относительные:
```python
/accounts/1/
```

Если вы все-таки хотите использовать относительные URL, то для этого вам нужно явно передать `{'request': None}` в контекст сериализатора.


## Как определяются гиперссылочные представления

Должен быть способ определения того, какие представления следует использовать в качестве гиперссылки на экземпляры модели.

Предполагается, что по умолчанию гиперссылки будут соответствовать имени представления, которое соответствует стилю `'{model_name} -detail'`, и ищет экземпляр по аргументу `pk`.

Вы можете переопределить имя поля поля URL и поле поиска с помощью опций `view_name` и `lookup_field` в параметрах `extra_kwargs`:


```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('account_url', 'account_name', 'users', 'created')
        extra_kwargs = {
            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'users': {'lookup_field': 'username'}
        }
```

В качестве альтернативы вы можете явно установить поля в сериализаторе. Например:


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
        fields = ('url', 'account_name', 'users', 'created')
```
**Совет**. Правильное сопоставление гиперссылочных представлений и URL conf порой может быть непромтой задачей. Чтобы узнать к каким именам представлений и lookup полям должны соотносниться отношения можно с помощью print вывести `repr` экземпляра `HyperlinkedModelSerializer`.


## Изменение имени поля URL
По умолчанию имя поля URL значится как 'url'. Вы можете переопределить это глобально, используя параметр `URL_FIELD_NAME`.

# ListSerializer
Класс `ListSerializer` обеспечивает поведение для последовательной и одновременной проверки нескольких объектов. Обычно вам не нужно использовать ListSerializer напрямую но вместо этого нужно просто передать аргумент `many = True` при создании экземпляра сериализатора.

Когда инициализируется сериализатор и передается аргумент `many = True`, создается экземпляр `ListSerializer`. Затем класс сериализатора становится потомком родительского `ListSerializer`

Следующий аргумент также может быть передан в поле `ListSerializer` или сериализатор, которому передается `many = True`:

```python
allow_empty
```

По умолчанию `True`, но может быть равным `False`, если вы хотите запретить пустые списки в качестве допустимого ввода.

## Настройка поведения ListSerializer

Есть ряд случаев, когда вам может потребоваться настроить поведение `ListSerializer`. Например:

* Вы хотите обеспечить определенную проверку списков, например проверку того, что один элемент не конфликтует с другим элементом в списке.
* Вы хотите настроить процесс создания или обновления нескольких объектов.

Для этих случаев вы можете изменить класс, который используется, при передаче аргумента ` many=True` , используя опцию `list_serializer_class` в классе `Meta` сериализатора.

Например:



```python
class CustomListSerializer(serializers.ListSerializer):
    ...

class CustomSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = CustomListSerializer
```


## Настройка нескольких create

По умолчанию несколько объектов можно создать просто вызвав `.create()` для каждого элемента в списке. Если вы хотите настроить это поведение, вам нужно настроить метод `.create()` в классе `ListSerializer`, который используется, когда передается аргумент `many=True`.
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


## Настройка нескольких update

По умолчанию класс `ListSerializer` не поддерживает несколько update. Это связано с тем, что поведение, которое следует ожидать при вставках и удалениях, неоднозначно.

Чтобы поддерживать нескольких обновлений, вам нужно сделать это явно. При написании кода множественного обновления обязательно учитывайте следующее:

* Как вы определяете, какой экземпляр должен быть обновлен для каждого элемента в списке данных?
* Как следует обрабатывать вставки? Они недействительны или создают новые объекты?
* Как следует обрабатывать удаление? Оно подразумевают удаление объекта или удаление отношений? Следует ли его игнорировать, или считать недействительным?
* Как следует обрабатывать сортировку? Изменяет ли положение двух элементов любое изменение состояния или игнорируется?
Вам нужно будет добавить явное поле `id` в сериализатор экземпляра. По умолчанию неявно сгенерированное поле id помечено как `read_only`. Это приводит к его удалению при обновлении. Как только вы объявите его явно, он будет доступен в списке методов обновления сериализатора.
Пример того, как вы можете реализовать несколько обновлений:


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

Возможно, в следующую версию фреймворка будет включен пакет сторонних разработчиков, который обеспечивал бы некоторую автоматическую поддержку для нескольких операций обновления, аналогичную поведению `allow_add_remove`, которое присутствовало в REST framework 2.


## Настройка инициализации ListSerializer

Когда создается экземпляр сериализатора с ` many=True` , нам нужно определить, какие аргументы и аргументы ключевых слов должны быть переданы методу `.__init__()` для дочернего класса `Serializer` и для родительского класса `ListSerializer`.

Реализация по умолчанию - передать все аргументы обоим классам, за исключением валидаторов, и любые пользовательские аргументы ключевых слов, оба из которых предназначены для дочернего класса сериализатора.

Иногда вам может потребоваться явно указать, каким образом следует создать экземпляр дочернего и родительского классов при передаче аргументов `many=True`. Вы можете сделать это, используя метод класса `many_init`.


```python
 @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return CustomListSerializer(*args, **kwargs)
```

## BaseSerializer
Класс `BaseSerializer` может использоваться для легкой поддержки альтернативных стилей сериализации и десериализации.

Этот класс реализует тот же базовый API, что и класс `Serializer`:

* .data - возвращает исходное примитивное представление.
* .is_valid() - десериализирует и проверяет входящие данные.
* .validated_data - возвращает проверенные входящие данные.
* .errors - Возвращает любые ошибки во время проверки.
* .save() - Сохраняет проверенные данные в экземпляре объекта.
Существует четыре метода, которые можно переопределить, в зависимости от того, какую функциональность вы хотите использовать для класса сериализатора:

* .to_representation () - переопределите для поддержки сериализации для операций чтения.
* .to_internal_value () - переопределите для поддержки десериализации для операций записи.
* .create () и .update () - переопределите однин или оба метода для поддержки экземпляров сохранения.

Поскольку этот класс предоставляет тот же интерфейс, что и класс `Serializer`, вы можете использовать его с существующими общими представлениями-классами, точно так же, как обычный `Serializer` или `ModelSerializer`.

Единственное отличие, которое вы заметите при этом, - это то, что классы `BaseSerializer` не будут генерировать HTML-формы в API-интерфейсе. Это связано с тем, что возвращаемые данные не включают всю информацию о поле, которая позволяет рендерить каждое поле в подходящий HTML.

Read-only `BaseSerializer` классы

Чтобы реализовать read-only сериализатор с использованием класса `BaseSerializer`, нам просто нужно переопределить метод `.to_representation()`. Давайте рассмотрим пример с использованием простой модели Django:


```python
class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()
```

Нет ничего сложного в том, чтобы создать сериализатор только для чтения для преобразования экземпляров `HighScore` в примитивные типы данных.


```python
class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'score': obj.score,
            'player_name': obj.player_name
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


Или использовать его для сериализации нескольких экземпляров:

```python
@api_view(['GET'])
def all_high_scores(request):
    queryset = HighScore.objects.order_by('-score')
    serializer = HighScoreSerializer(queryset, many=True)
    return Response(serializer.data)
```

### Read-write BaseSerializer классы

Чтобы создать сериализатор чтения и записи, сначала необходимо реализовать метод `.to_internal_value()`. Этот метод возвращает проверенные значения, которые будут использоваться для создания экземпляра объекта, и может вызвать `ValidationError`, если предоставленные данные находятся в неправильном формате.

После того, как вы внедрили `.to_internal_value()`, базовый API проверки будет доступен в сериализаторе, и вы сможете использовать `.is_valid()`, `.validated_data` и `.errors`.

Если помимо этого вам требуется поддержка .save (), вам также необходимо реализовать один или оба метода `.create()` и `.update()`.

Вот полный пример нашего предыдущего `HighScoreSerializer`, который был обновлен для поддержки операций чтения и записи.

```python
class HighScoreSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')

        # Осуществляется проверка данных.
        if not score:
            raise ValidationError({
                'score': 'This field is required.'
            })
        if not player_name:
            raise ValidationError({
                'player_name': 'This field is required.'
            })
        if len(player_name) > 10:
            raise ValidationError({
                'player_name': 'May not be more than 10 characters.'
            })

        # Возвращает проверенные значения. Они будут доступны
        # в качестве свойства `.validated_data` .
        return {
            'score': int(score),
            'player_name': player_name
        }

    def to_representation(self, obj):
        return {
            'score': obj.score,
            'player_name': obj.player_name
        }

    def create(self, validated_data):
        return HighScore.objects.create(**validated_data)
```

## Создание новых базовых классов

Класс `BaseSerializer` также полезен, если вы хотите внедрять новые общие классы сериализатора для работы с определенными стилями сериализации или для интеграции с альтернативными обработчиками хранилищ.

Следующий класс является примером универсального сериализатора, который может преобразовывать произвольные объекты в примитивные представления.


```python
class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_representation(self, obj):
        for attribute_name in dir(obj):
            attribute = getattr(obj, attribute_name)
            if attribute_name('_'):
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
```

# Продвинутое использование сериализаторов
## Переопределение процесса сериализации и десериализации

Если вам необходимо изменить поведение сериализации или десериализации класса сериализатора, вы можете сделать это, переопределив методы `.to_representation()` или `.to_internal_value()`.

Некоторые причины, почему это может быть полезно ...

* Добавление нового поведения для новых классов базового класса.
* Несущественное измение поведения существующего класса.
* Улучшение производительности сериализации для часто используемой конечной точки API, которая возвращает большое количество данных.
* Подписи для этих методов заключаются в следующем:

У этих методов следующие подписи:

```python
.to_representation(self, obj)
```
Принимает экземпляр объекта, который требует сериализации, и  возвращает примитивное представление. Обычно это означает возврат структуры встроенных типов данных Python. Точные типы, которые можно обрабатывать, будут зависеть от классов рендеринга, которые вы настроили для вашего API.


```python
.to_internal_value(self, data)
```

Принимает невалидные входящие данные и возвращает проверенные данные, которые будут доступны как `serializer.validated_data`. Возвращаемое значение также будет передано методам `.create()` или `.update()`, если в классе сериализатора вызывается `.save()`.

Если какая-либо проверка не выполняется, тогда метод должен вызвать `serializers.ValidationError(errors)`. Аргумент `errors` должен быть словарем, который соотносит имена полей (или `settings.NON_FIELD_ERRORS_KEY)` с списком сообщений об ошибках. Если вы не хотите изменять поведение десериализации, и вместо этого вам требуется обеспечить проверку уровня объекта, рекомендуется переопределить метод `.validate()`.


Аргумент данных, переданный этому методу, обычно будет значением `request.data`, поэтому предоставляемый им тип данных будет зависеть от классов парсеров, которые вы настроили для вашего API.

## Наследование сериализаторов
Подобно формам Django, вы можете расширять и повторно использовать сериализаторы через наследование. Это позволяет объявлять общий набор полей или методов родительского класса, который затем может использоваться в ряде сериализаторов. Например,

```python
class MyBaseSerializer(Serializer):
    my_field = serializers.CharField()

    def validate_my_field(self):
        ...

class MySerializer(MyBaseSerializer):
    ...

```

Как и классы `Django Model` и `ModelForm`, внутренний класс `Meta` на сериализаторах неявно наследуется от внутренних `Meta`-классов своих родителей. Если вы хотите, чтобы класс `Meta` наследовался от родительского класса, вы должны сделать это явно. Например:



```python
class AccountSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        model = Account
```


Обычно мы не рекомендуем использовать наследование для внутренних классов `Meta` и вместо этого явно объявляем все опции.

Кроме того, следующие ограничения относятся к наследованию сериализатора:

* Применяются нормальные правила разрешения имен Python. Если у вас есть несколько базовых классов, объявляющих внутренний класс Meta, будет использоваться только первый. Например это может быть дочерний `Meta`, если он существует, в противном случае это будет `Meta` первого родителя и т.д.
* Можно удалить с помощью описания `Field`, унаследованное от родительского класса, задав для него имя `None` в подклассе.

```python
class MyBaseSerializer(ModelSerializer):
    my_field = serializers.CharField()

class MySerializer(MyBaseSerializer):
    my_field = None
```
Однако вы можете использовать этот способ только для устранения поля, определенного родительским классом с помощью описания; это не помешает `ModelSerializer` генерировать поле по умолчанию. Чтобы отказаться от полей по умолчанию, см. Определение полей для включения.

# Динамически изменяемые поля

Как только сериализатор был задан, словарь полей, которые установлены в сериализаторе, может быть доступен с использованием атрибута `.fields`. Доступ и изменение этого атрибута позволяет динамически изменять сериализатор.

Изменение аргумента полей напрямую позволяет вам делать интересные вещи, такие как изменение аргументов в полях сериализатора во время выполнения, а не в момент объявления сериализатора.


## Пример
Например, если вы хотите указать, какие поля должны использоваться сериализатором в точке его инициализации, вы можете создать класс сериализатора следующим образом:

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
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

```

Это позволит вам сделать следующее:

```python
>>> class UserSerializer(DynamicFieldsModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ('id', 'username', 'email')
>>>
>>> print UserSerializer(user)
{'id': 2, 'username': 'jonwatts', 'email': 'jon@example.com'}
>>>
>>> print UserSerializer(user, fields=('id', 'email'))
{'id': 2, 'email': 'jon@example.com'}
```

## Настройка полей по умолчанию
REST framework 2 предоставил API, который позволяет разработчикам переопределять, как класс `ModelSerializer` автоматически генерирует набор полей по умолчанию.

Этот API включал методы `.get_field()`, `.get_pk_field()` и другие методы.

Поскольку сериализаторы были коренным образом переработаны в 3.0 версии, этот API больше не существует. Вы все равно можете изменить создающиеся поля, но вам нужно будет обратиться к исходному коду. Имейте в виду, что если сделанные вами изменения будут противоречить некоторым компонентам API, то их можно изменить.

# Сторонние пакеты
Доступны следующие сторонние пакеты.

## Django REST marshmallow
Пакет [django-rest-marshmallow](https://github.com/marshmallow-code/django-rest-marshmallow) обеспечивает альтернативную реализацию для сериализаторов, используя библиотеку python [marshmallow](https://marshmallow.readthedocs.io/en/latest/). Он предоставляет тот же API, что и сериализаторы REST framework и может использоваться в качестве замены в некоторых случаях использования.
## Serpy
Ппакет [Serpy](https://github.com/clarkduvall/serpy) - альтернативная скоростная реализация для сериализаторов. Serpy сериализует сложные типы данных для простых родных типов. Нативные типы могут быть легко преобразованы в JSON или в любой другой формат.
## MongoengineModelSerializer
Пакет [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) предоставляет класс сериализатора `MongoEngineModelSerializer`, который поддерживает использование `MongoDB` в качестве уровня хранения для Django REST framework.
## GeoFeatureModelSerializer
Пакет [django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) предоставляет класс сериализатора `GeoFeatureModelSerializer`, который поддерживает GeoJSON для операций чтения и записи.
## HStoreSerializer
Пакет [django-rest-framework-hstore]() предоставляет `HStoreSerializer` для поддержки поля модели django-hstore `DictionaryField` и его функции schema-mode.
## Dynamic REST
Пакет [dynamic-rest](https://github.com/AltSchool/dynamic-rest) расширяет интерфейсы `ModelSerializer` и `ModelViewSet`, добавляя параметры запроса API для фильтрации, сортировки и включения / исключения всех полей и отношений, определенных вашими сериализаторами.
## Dynamic Fields Mixin
Пакет [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) предоставляет миксины для динамического ограничения полей сериализатора на подмножество, заданное в параметре URL.
## DRF FlexFields
Пакет [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) расширяет `ModelSerializer` и `ModelViewSet` для предоставления часто использующегося функционала для динамического задания полей и расширения примитивных полей для вложенных моделей как из параметров URL, так и из определений классов сериализатора.
## Serializer Extensions
Пакет [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) предоставляет набор инструментов для того, чтобы ваши сериализаторы соответствовали принципу DRY, позволяя определять поля на основе каждого взятого представления/запроса. Поля могут быть добавлены в белый список, черные списки и дочерние сериализаторы могут быть дополнительно расширены.
## HTML JSON Forms
Пакет [html-json-forms](https://github.com/wq/html-json-forms) предоставляет алгоритм и сериализатор для обработки поданных <form> через (неактивную) [спецификацию HTML JSON](https://www.w3.org/TR/html-json-forms/). Сериализатор облегчает обработку произвольно вложенных структур JSON внутри HTML. Например, `<input name = "items [0][id]" value = "5">` будет интерпретироваться как `{"items": [{"id": "5"}]}`.
## DRF-Base64
[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64) предоставляет набор полевых и модельных сериализаторов, которые обрабатывают загрузку base64-encode
## QueryFields
[djangorestframework-queryfields](http://djangorestframework-queryfields.readthedocs.io/en/latest/) позволяет указывать клиентам API, какие поля будут отправляться в ответе через параметры inclusion/exclusion.
## DRF Writable Nested
Пакет [drf-writable-nested](https://github.com/beda-software/drf-writable-nested) обеспечивает доступный для записи вложенный сериализатор модели, который позволяет создаватьобновлять модели с вложенными связанными данными.
