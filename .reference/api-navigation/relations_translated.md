<!-- TRANSLATED by md-translate -->
---

source:

источник:

* relations.py

* relations.py

---

# Serializer relations

# Отношения сериализатора

> Data structures, not algorithms, are central to programming.
>
> — [Rob Pike](http://users.ece.utexas.edu/~adnan/pike.html)

> Структуры данных, а не алгоритмы, занимают центральное место в программировании.
>
> - [Роб Пайк] (http://users.ece.utexas.edu/~adnan/pike.html)

Relational fields are used to represent model relationships. They can be applied to `ForeignKey`, `ManyToManyField` and `OneToOneField` relationships, as well as to reverse relationships, and custom relationships such as `GenericForeignKey`.

Реляционные поля используются для представления отношений между моделями. Они могут применяться к отношениям `ForeignKey`, `ManyToManyField` и `OneToOneField`, а также к обратным отношениям и пользовательским отношениям, таким как `GenericForeignKey`.

---

**Note:** The relational fields are declared in `relations.py`, but by convention you should import them from the `serializers` module, using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.

**Примечание:** Реляционные поля объявляются в `relations.py`, но по соглашению вы должны импортировать их из модуля `serializers`, используя `from rest_framework import serializers` и ссылаться на поля как `serializers.<FieldName>`.

---

---

**Note:** REST Framework does not attempt to automatically optimize querysets passed to serializers in terms of `select_related` and `prefetch_related` since it would be too much magic. A serializer with a field spanning an orm relation through its source attribute could require an additional database hit to fetch related objects from the database. It is the programmer's responsibility to optimize queries to avoid additional database hits which could occur while using such a serializer.

**Примечание:** REST Framework не пытается автоматически оптимизировать передаваемые сериализаторам наборы запросов в терминах `select_related` и `prefetch_related`, поскольку это было бы слишком сложной магией. Сериализатор с полем, охватывающим отношение orm через атрибут source, может потребовать дополнительного обращения к базе данных для получения связанных объектов из базы данных. В обязанности программиста входит оптимизация запросов, чтобы избежать дополнительных обращений к базе данных, которые могут возникнуть при использовании такого сериализатора.

For example, the following serializer would lead to a database hit each time evaluating the tracks field if it is not prefetched:

Например, следующий сериализатор будет приводить к попаданию в базу данных каждый раз при оценке поля tracks, если оно не префетчено:

```
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

# For each album object, tracks should be fetched from database
qs = Album.objects.all()
print(AlbumSerializer(qs, many=True).data)
```

If `AlbumSerializer` is used to serialize a fairly large queryset with `many=True` then it could be a serious performance problem. Optimizing the queryset passed to `AlbumSerializer` with:

Если `AlbumSerializer` используется для сериализации довольно большого набора запросов с `many=True`, то это может стать серьезной проблемой производительности. Оптимизация кверисета, передаваемого `AlbumSerializer` с:

```
qs = Album.objects.prefetch_related('tracks')
# No additional database hits required
print(AlbumSerializer(qs, many=True).data)
```

would solve the issue.

решит эту проблему.

---

#### Inspecting relationships.

#### Инспектирование отношений.

When using the `ModelSerializer` class, serializer fields and relationships will be automatically generated for you. Inspecting these automatically generated fields can be a useful tool for determining how to customize the relationship style.

При использовании класса `ModelSerializer`, поля и отношения сериализатора будут автоматически сгенерированы для вас. Проверка этих автоматически сгенерированных полей может быть полезным инструментом для определения того, как настроить стиль отношений.

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

# API Reference

# API Reference

In order to explain the various types of relational fields, we'll use a couple of simple models for our examples. Our models will be for music albums, and the tracks listed on each album.

Для того чтобы объяснить различные типы реляционных полей, мы будем использовать пару простых моделей для наших примеров. Нашими моделями будут музыкальные альбомы и треки, перечисленные в каждом альбоме.

```
class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
```

## StringRelatedField

## StringRelatedField

`StringRelatedField` may be used to represent the target of the relationship using its `__str__` method.

`StringRelatedField` может использоваться для представления цели отношения с помощью своего метода `__str__`.

For example, the following serializer:

Например, следующий сериализатор:

```
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Would serialize to the following representation:

Сериализуется в следующее представление:

```
{
    'album_name': 'Things We Lost In The Fire',
    'artist': 'Low',
    'tracks': [
        '1: Sunflower',
        '2: Whitetail',
        '3: Dinosaur Act',
        ...
    ]
}
```

This field is read only.

Это поле доступно только для чтения.

**Arguments**:

**Аргументы**:

* `many` - If applied to a to-many relationship, you should set this argument to `True`.

* `many` - Если применяется к отношениям типа "ко многим", следует установить этот аргумент в `True`.

## PrimaryKeyRelatedField

## PrimaryKeyRelatedField

`PrimaryKeyRelatedField` may be used to represent the target of the relationship using its primary key.

`PrimaryKeyRelatedField` может использоваться для представления цели отношения с помощью его первичного ключа.

For example, the following serializer:

Например, следующий сериализатор:

```
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Would serialize to a representation like this:

Сериализуется в представление, подобное этому:

```
{
    'album_name': 'Undun',
    'artist': 'The Roots',
    'tracks': [
        89,
        90,
        91,
        ...
    ]
}
```

By default this field is read-write, although you can change this behavior using the `read_only` flag.

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

**Arguments**:

**Аргументы**:

* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.
* `pk_field` - Set to a field to control serialization/deserialization of the primary key's value. For example, `pk_field=UUIDField(format='hex')` would serialize a UUID primary key into its compact hex representation.

* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию `False`.
* `pk_field` - Устанавливается в поле для управления сериализацией/десериализацией значения первичного ключа. Например, `pk_field=UUIDField(format='hex')` будет сериализовать первичный ключ UUID в его компактное шестнадцатеричное представление.

## HyperlinkedRelatedField

## HyperlinkedRelatedField

`HyperlinkedRelatedField` may be used to represent the target of the relationship using a hyperlink.

`HyperlinkedRelatedField` может использоваться для представления цели отношения с помощью гиперссылки.

For example, the following serializer:

Например, следующий сериализатор:

```
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Would serialize to a representation like this:

Сериализуется в представление, подобное этому:

```
{
    'album_name': 'Graceland',
    'artist': 'Paul Simon',
    'tracks': [
        'http://www.example.com/api/tracks/45/',
        'http://www.example.com/api/tracks/46/',
        'http://www.example.com/api/tracks/47/',
        ...
    ]
}
```

By default this field is read-write, although you can change this behavior using the `read_only` flag.

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

---

**Note**: This field is designed for objects that map to a URL that accepts a single URL keyword argument, as set using the `lookup_field` and `lookup_url_kwarg` arguments.

**Примечание**: Это поле предназначено для объектов, сопоставленных с URL, который принимает один аргумент ключевого слова URL, заданный с помощью аргументов `lookup_field` и `lookup_url_kwarg`.

This is suitable for URLs that contain a single primary key or slug argument as part of the URL.

Это подходит для URL, которые содержат один первичный ключ или аргумент slug как часть URL.

If you require more complex hyperlinked representation you'll need to customize the field, as described in the [custom hyperlinked fields](#custom-hyperlinked-fields) section, below.

Если вам требуется более сложное представление гиперссылок, вам необходимо настроить поле, как описано ниже в разделе [пользовательские гиперссылочные поля](#custom-hyperlinked-fields).

---

**Arguments**:

**Аргументы**:

* `view_name` - The view name that should be used as the target of the relationship. If you're using [the standard router classes](https://www.django-rest-framework.org/api-guide/routers#defaultrouter) this will be a string with the format `<modelname>-detail`. **required**.
* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.
* `lookup_field` - The field on the target that should be used for the lookup. Should correspond to a URL keyword argument on the referenced view. Default is `'pk'`.
* `lookup_url_kwarg` - The name of the keyword argument defined in the URL conf that corresponds to the lookup field. Defaults to using the same value as `lookup_field`.
* `format` - If using format suffixes, hyperlinked fields will use the same format suffix for the target unless overridden by using the `format` argument.

* ``имя_представления`` - Имя представления, которое должно использоваться в качестве цели отношения. Если вы используете [стандартные классы маршрутизаторов](https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<имя модели>-detail`. **необходимо**.
* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию `False`.
* `lookup_field` - Поле цели, которое должно быть использовано для поиска. Должно соответствовать аргументу ключевого слова URL в ссылающемся представлении. По умолчанию `'pk''.
* `lookup_url_kwarg` - Имя аргумента ключевого слова, определенного в URL conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, то поля с гиперссылками будут использовать тот же суффикс формата для цели, если это не отменено с помощью аргумента `format`.

## SlugRelatedField

## SlugRelatedField

`SlugRelatedField` may be used to represent the target of the relationship using a field on the target.

`SlugRelatedField` может использоваться для представления цели отношения с помощью поля цели.

For example, the following serializer:

Например, следующий сериализатор:

```
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Would serialize to a representation like this:

Сериализуется в представление, подобное этому:

```
{
    'album_name': 'Dear John',
    'artist': 'Loney Dear',
    'tracks': [
        'Airport Surroundings',
        'Everything Turns to You',
        'I Was Only Going Out',
        ...
    ]
}
```

By default this field is read-write, although you can change this behavior using the `read_only` flag.

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

When using `SlugRelatedField` as a read-write field, you will normally want to ensure that the slug field corresponds to a model field with `unique=True`.

При использовании `SlugRelatedField` в качестве поля для чтения-записи вы обычно хотите убедиться, что поле slug соответствует полю модели с `unique=True`.

**Arguments**:

**Аргументы**:

* `slug_field` - The field on the target that should be used to represent it. This should be a field that uniquely identifies any given instance. For example, `username`. **required**
* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.

* `slug_field` - Поле цели, которое должно быть использовано для ее представления. Это должно быть поле, которое однозначно идентифицирует любой данный экземпляр. Например, `username`. **обязательно**
* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию установлено значение `False`.

## HyperlinkedIdentityField

## HyperlinkedIdentityField

This field can be applied as an identity relationship, such as the `'url'` field on a HyperlinkedModelSerializer. It can also be used for an attribute on the object. For example, the following serializer:

Это поле может применяться как отношение идентичности, например, поле `'url'` в HyperlinkedModelSerializer. Оно также может быть использовано для атрибута объекта. Например, следующий сериализатор:

```
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

Would serialize to a representation like this:

Сериализуется в представление, подобное этому:

```
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

This field is always read-only.

Это поле всегда доступно только для чтения.

**Arguments**:

**Аргументы**:

* `view_name` - The view name that should be used as the target of the relationship. If you're using [the standard router classes](https://www.django-rest-framework.org/api-guide/routers#defaultrouter) this will be a string with the format `<model_name>-detail`. **required**.
* `lookup_field` - The field on the target that should be used for the lookup. Should correspond to a URL keyword argument on the referenced view. Default is `'pk'`.
* `lookup_url_kwarg` - The name of the keyword argument defined in the URL conf that corresponds to the lookup field. Defaults to using the same value as `lookup_field`.
* `format` - If using format suffixes, hyperlinked fields will use the same format suffix for the target unless overridden by using the `format` argument.

* ``имя_представления`` - Имя представления, которое должно использоваться в качестве цели отношения. Если вы используете [стандартные классы маршрутизаторов](https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<имя_модели>-detail`. **необходимо**.
* `lookup_field` - Поле цели, которое должно быть использовано для поиска. Должно соответствовать аргументу ключевого слова URL в ссылающемся представлении. По умолчанию `'pk''.
* `lookup_url_kwarg` - Имя аргумента ключевого слова, определенного в URL conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, поля с гиперссылками будут использовать тот же суффикс формата для цели, если это не будет отменено с помощью аргумента `format`.

---

# Nested relationships

# Вложенные отношения

As opposed to previously discussed *references* to another entity, the referred entity can instead also be embedded or *nested* in the representation of the object that refers to it. Such nested relationships can be expressed by using serializers as fields.

В отличие от ранее рассмотренных *ссылок* на другую сущность, ссылающаяся сущность может быть встроена или *вложена* в представление объекта, который на нее ссылается. Такие вложенные отношения могут быть выражены с помощью сериализаторов в качестве полей.

If the field is used to represent a to-many relationship, you should add the `many=True` flag to the serializer field.

Если поле используется для представления отношения "ко многим", необходимо добавить флаг `many=True` к полю сериализатора.

## Example

## Пример

For example, the following serializer:

Например, следующий сериализатор:

```
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Would serialize to a nested representation like this:

Сериализуется во вложенное представление следующим образом:

```
>>> album = Album.objects.create(album_name="The Grey Album", artist='Danger Mouse')
>>> Track.objects.create(album=album, order=1, title='Public Service Announcement', duration=245)
<Track: Track object>
>>> Track.objects.create(album=album, order=2, title='What More Can I Say', duration=264)
<Track: Track object>
>>> Track.objects.create(album=album, order=3, title='Encore', duration=159)
<Track: Track object>
>>> serializer = AlbumSerializer(instance=album)
>>> serializer.data
{
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
        ...
    ],
}
```

## Writable nested serializers

## Записываемые вложенные сериализаторы

By default nested serializers are read-only. If you want to support write-operations to a nested serializer field you'll need to create `create()` and/or `update()` methods in order to explicitly specify how the child relationships should be saved:

По умолчанию вложенные сериализаторы доступны только для чтения. Если вы хотите поддерживать операции записи во вложенное поле сериализатора, вам необходимо создать методы `create()` и/или `update()`, чтобы явно указать, как должны сохраняться дочерние отношения:

```
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

>>> data = {
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
    ],
}
>>> serializer = AlbumSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.save()
<Album: Album object>
```

---

# Custom relational fields

# Пользовательские реляционные поля

In rare cases where none of the existing relational styles fit the representation you need, you can implement a completely custom relational field, that describes exactly how the output representation should be generated from the model instance.

В редких случаях, когда ни один из существующих реляционных стилей не подходит для нужного вам представления, вы можете реализовать полностью пользовательское реляционное поле, которое описывает, как именно должно быть сгенерировано выходное представление из экземпляра модели.

To implement a custom relational field, you should override `RelatedField`, and implement the `.to_representation(self, value)` method. This method takes the target of the field as the `value` argument, and should return the representation that should be used to serialize the target. The `value` argument will typically be a model instance.

Для реализации пользовательского реляционного поля необходимо переопределить `RelatedField` и реализовать метод `.to_representation(self, value)`. Этот метод принимает цель поля в качестве аргумента `значение` и должен возвращать представление, которое должно использоваться для сериализации цели. Аргумент `значение` обычно представляет собой экземпляр модели.

If you want to implement a read-write relational field, you must also implement the [`.to_internal_value(self, data)` method](https://www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data).

Если вы хотите реализовать реляционное поле для чтения и записи, вы должны также реализовать метод [`.to_internal_value(self, data)`](https://www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data).

To provide a dynamic queryset based on the `context`, you can also override `.get_queryset(self)` instead of specifying `.queryset` on the class or when initializing the field.

Чтобы обеспечить динамический набор запросов, основанный на `контексте`, вы также можете переопределить `.get_queryset(self)` вместо указания `.queryset` в классе или при инициализации поля.

## Example

## Пример

For example, we could define a relational field to serialize a track to a custom string representation, using its ordering, title, and duration:

Например, мы можем определить реляционное поле для сериализации трека в пользовательское строковое представление, используя его порядок, название и продолжительность:

```
import time

class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(value.duration))
        return 'Track %d: %s (%s)' % (value.order, value.name, duration)

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackListingField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

This custom field would then serialize to the following representation:

Это пользовательское поле затем сериализуется в следующее представление:

```
{
    'album_name': 'Sometimes I Wish We Were an Eagle',
    'artist': 'Bill Callahan',
    'tracks': [
        'Track 1: Jim Cain (04:39)',
        'Track 2: Eid Ma Clack Shaw (04:19)',
        'Track 3: The Wind and the Dove (04:34)',
        ...
    ]
}
```

---

# Custom hyperlinked fields

# Пользовательские поля с гиперссылками

In some cases you may need to customize the behavior of a hyperlinked field, in order to represent URLs that require more than a single lookup field.

В некоторых случаях вам может понадобиться настроить поведение поля с гиперссылкой, чтобы представить URL-адреса, для которых требуется более одного поля поиска.

You can achieve this by overriding `HyperlinkedRelatedField`. There are two methods that may be overridden:

Вы можете добиться этого, переопределив `HyperlinkedRelatedField`. Есть два метода, которые могут быть переопределены:

**get_url(self, obj, view_name, request, format)**

**get_url(self, obj, view_name, request, format)**.

The `get_url` method is used to map the object instance to its URL representation.

Метод `get_url` используется для сопоставления экземпляра объекта с его URL-представлением.

May raise a `NoReverseMatch` if the `view_name` and `lookup_field` attributes are not configured to correctly match the URL conf.

Может вызвать ошибку `NoReverseMatch`, если атрибуты `view_name` и `lookup_field` не настроены на правильное соответствие URL conf.

**get_object(self, view_name, view_args, view_kwargs)**

**get_object(self, view_name, view_args, view_kwargs)**.

If you want to support a writable hyperlinked field then you'll also want to override `get_object`, in order to map incoming URLs back to the object they represent. For read-only hyperlinked fields there is no need to override this method.

Если вы хотите поддерживать записываемое поле с гиперссылками, вам также потребуется переопределить `get_object`, чтобы сопоставить входящие URL обратно с объектом, который они представляют. Для полей с гиперссылками, доступных только для чтения, нет необходимости переопределять этот метод.

The return value of this method should the object that corresponds to the matched URL conf arguments.

Возвращаемое значение этого метода - объект, соответствующий аргументам URL conf.

May raise an `ObjectDoesNotExist` exception.

Может вызвать исключение `ObjectDoesNotExist`.

## Example

## Пример

Say we have a URL for a customer object that takes two keyword arguments, like so:

Допустим, у нас есть URL для объекта customer, который принимает два аргумента в виде ключевых слов, как показано ниже:

```
/api/<organization_slug>/customers/<customer_pk>/
```

This cannot be represented with the default implementation, which accepts only a single lookup field.

Это не может быть представлено с помощью реализации по умолчанию, которая принимает только одно поле поиска.

In this case we'd need to override `HyperlinkedRelatedField` to get the behavior we want:

В этом случае нам нужно переопределить `HyperlinkedRelatedField`, чтобы получить желаемое поведение:

```
from rest_framework import serializers
from rest_framework.reverse import reverse

class CustomerHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'customer-detail'
    queryset = Customer.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'organization_slug': obj.organization.slug,
            'customer_pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['organization_slug'],
           'pk': view_kwargs['customer_pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
```

Note that if you wanted to use this style together with the generic views then you'd also need to override `.get_object` on the view in order to get the correct lookup behavior.

Обратите внимание, что если вы хотите использовать этот стиль вместе с общими представлениями, то вам также необходимо переопределить `.get_object` в представлении, чтобы получить правильное поведение поиска.

Generally we recommend a flat style for API representations where possible, but the nested URL style can also be reasonable when used in moderation.

Обычно мы рекомендуем использовать плоский стиль для представления API, когда это возможно, но вложенный стиль URL также может быть разумным при умеренном использовании.

---

# Further notes

# Дальнейшие примечания

## The `queryset` argument

## Аргумент `queryset`.

The `queryset` argument is only ever required for *writable* relationship field, in which case it is used for performing the model instance lookup, that maps from the primitive user input, into a model instance.

Аргумент `queryset` требуется только для *записываемого* поля отношения, в этом случае он используется для выполнения поиска экземпляра модели, который отображает примитивный пользовательский ввод в экземпляр модели.

In version 2.x a serializer class could *sometimes* automatically determine the `queryset` argument *if* a `ModelSerializer` class was being used.

В версии 2.x класс сериализатора мог *иногда* автоматически определять аргумент `queryset`, *если* использовался класс `ModelSerializer`.

This behavior is now replaced with *always* using an explicit `queryset` argument for writable relational fields.

Теперь это поведение заменено на *всегда* использование явного аргумента `queryset` для записываемых реляционных полей.

Doing so reduces the amount of hidden 'magic' that `ModelSerializer` provides, makes the behavior of the field more clear, and ensures that it is trivial to move between using the `ModelSerializer` shortcut, or using fully explicit `Serializer` classes.

Это уменьшает количество скрытой "магии", которую обеспечивает `ModelSerializer`, делает поведение поля более понятным и гарантирует, что можно легко переходить от использования ярлыка `ModelSerializer` к использованию полностью явных классов `Serializer`.

## Customizing the HTML display

## Настройка отображения HTML

The built-in `__str__` method of the model will be used to generate string representations of the objects used to populate the `choices` property. These choices are used to populate select HTML inputs in the browsable API.

Встроенный метод `__str__` модели будет использоваться для создания строковых представлений объектов, используемых для заполнения свойства `choices`. Эти варианты используются для заполнения HTML-вводов выбора в просматриваемом API.

To provide customized representations for such inputs, override `display_value()` of a `RelatedField` subclass. This method will receive a model object, and should return a string suitable for representing it. For example:

Чтобы обеспечить настраиваемое представление для таких входов, переопределите `display_value()` подкласса `RelatedField`. Этот метод получит объект модели и должен вернуть строку, подходящую для его представления. Например:

```
class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Track: %s' % (instance.title)
```

## Select field cutoffs

## Выберите отсечение полей

When rendered in the browsable API relational fields will default to only displaying a maximum of 1000 selectable items. If more items are present then a disabled option with "More than 1000 items…" will be displayed.

При отображении в просматриваемом API реляционные поля по умолчанию будут отображать не более 1000 элементов для выбора. Если элементов больше, то будет отображаться отключенная опция "Более 1000 элементов...".

This behavior is intended to prevent a template from being unable to render in an acceptable timespan due to a very large number of relationships being displayed.

Это поведение предназначено для того, чтобы предотвратить невозможность отрисовки шаблона за приемлемое время из-за отображения очень большого количества связей.

There are two keyword arguments you can use to control this behavior:

Есть два ключевых аргумента, которые можно использовать для управления этим поведением:

* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Set to `None` to disable any limiting. Defaults to `1000`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `html_cutoff` - Если установлено, это будет максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Установите значение `None`, чтобы отключить любое ограничение. По умолчанию `1000`.
* `html_cutoff_text` - При установке этого параметра будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию ``Больше чем {count} элементов...``.

You can also control these globally using the settings `HTML_SELECT_CUTOFF` and `HTML_SELECT_CUTOFF_TEXT`.

Вы также можете управлять ими глобально, используя настройки `HTML_SELECT_CUTOFF` и `HTML_SELECT_CUTOFF_TEXT`.

In cases where the cutoff is being enforced you may want to instead use a plain input field in the HTML form. You can do so using the `style` keyword argument. For example:

В случаях, когда отсечение вводится принудительно, вы можете использовать обычное поле ввода в HTML-форме. Вы можете сделать это, используя аргумент ключевого слова `style`. Например:

```
assigned_to = serializers.SlugRelatedField(
   queryset=User.objects.all(),
   slug_field='username',
   style={'base_template': 'input.html'}
)
```

## Reverse relations

## Обратные отношения

Note that reverse relationships are not automatically included by the `ModelSerializer` and `HyperlinkedModelSerializer` classes. To include a reverse relationship, you must explicitly add it to the fields list. For example:

Обратите внимание, что обратные отношения не включаются автоматически классами `ModelSerializer` и `HyperlinkedModelSerializer`. Чтобы включить обратное отношение, вы должны явно добавить его в список полей. Например:

```
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tracks', ...]
```

You'll normally want to ensure that you've set an appropriate `related_name` argument on the relationship, that you can use as the field name. For example:

Обычно вам нужно убедиться, что вы установили соответствующий аргумент `related_name` для отношения, который вы можете использовать в качестве имени поля. Например:

```
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    ...
```

If you have not set a related name for the reverse relationship, you'll need to use the automatically generated related name in the `fields` argument. For example:

Если вы не задали связанное имя для обратного отношения, вам придется использовать автоматически сгенерированное связанное имя в аргументе `fields`. Например:

```
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['track_set', ...]
```

See the Django documentation on [reverse relationships](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward) for more details.

Более подробную информацию смотрите в документации Django по [обратным отношениям](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward).

## Generic relationships

## Общие отношения

If you want to serialize a generic foreign key, you need to define a custom field, to determine explicitly how you want to serialize the targets of the relationship.

Если вы хотите сериализовать общий внешний ключ, вам необходимо определить пользовательское поле, чтобы явно определить, как вы хотите сериализовать цели отношения.

For example, given the following model for a tag, which has a generic relationship with other arbitrary models:

Например, дана следующая модель для тега, которая имеет общие отношения с другими произвольными моделями:

```
class TaggedItem(models.Model):
    """
    Tags arbitrary model instances using a generic relation.

    See: https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/
    """
    tag_name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag_name
```

And the following two models, which may have associated tags:

И следующие две модели, которые могут иметь связанные теги:

```
class Bookmark(models.Model):
    """
    A bookmark consists of a URL, and 0 or more descriptive tags.
    """
    url = models.URLField()
    tags = GenericRelation(TaggedItem)


class Note(models.Model):
    """
    A note consists of some text, and 0 or more descriptive tags.
    """
    text = models.CharField(max_length=1000)
    tags = GenericRelation(TaggedItem)
```

We could define a custom field that could be used to serialize tagged instances, using the type of each instance to determine how it should be serialized:

Мы можем определить пользовательское поле, которое будет использоваться для сериализации помеченных экземпляров, используя тип каждого экземпляра для определения того, как он должен быть сериализован:

```
class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Bookmark):
            return 'Bookmark: ' + value.url
        elif isinstance(value, Note):
            return 'Note: ' + value.text
        raise Exception('Unexpected type of tagged object')
```

If you need the target of the relationship to have a nested representation, you can use the required serializers inside the `.to_representation()` method:

Если вам нужно, чтобы цель отношения имела вложенное представление, вы можете использовать необходимые сериализаторы внутри метода `.to_representation()`:

```
def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Bookmark):
            serializer = BookmarkSerializer(value)
        elif isinstance(value, Note):
            serializer = NoteSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data
```

Note that reverse generic keys, expressed using the `GenericRelation` field, can be serialized using the regular relational field types, since the type of the target in the relationship is always known.

Обратите внимание, что обратные родовые ключи, выраженные с помощью поля `GenericRelation`, могут быть сериализованы с использованием обычных типов реляционных полей, поскольку тип цели в отношениях всегда известен.

For more information see [the Django documentation on generic relations](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1).

Для получения дополнительной информации смотрите [документацию Django по общим отношениям](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1).

## ManyToManyFields with a Through Model

## ManyToManyFields со сквозной моделью

By default, relational fields that target a `ManyToManyField` with a `through` model specified are set to read-only.

По умолчанию реляционные поля, нацеленные на `ManyToManyField` с указанной моделью `through`, устанавливаются только для чтения.

If you explicitly specify a relational field pointing to a `ManyToManyField` with a through model, be sure to set `read_only` to `True`.

Если вы явно указываете реляционное поле, указывающее на `ManyToManyField` со сквозной моделью, обязательно установите `read_only` в `True`.

If you wish to represent [extra fields on a through model](https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany) then you may serialize the through model as [a nested object](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects).

Если вы хотите представить [дополнительные поля в сквозной модели] (https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany), то вы можете сериализовать сквозную модель как [вложенный объект] (https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects).

---

# Third Party Packages

# Сторонние пакеты

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF Nested Routers

## Вложенные маршрутизаторы DRF

The [drf-nested-routers package](https://github.com/alanjds/drf-nested-routers) provides routers and relationship fields for working with nested resources.

Пакет [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) предоставляет маршрутизаторы и поля отношений для работы с вложенными ресурсами.

## Rest Framework Generic Relations

## Rest Framework Generic Relations

The [rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations) library provides read/write serialization for generic foreign keys.

Библиотека [rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations) обеспечивает сериализацию чтения/записи для общих внешних ключей.