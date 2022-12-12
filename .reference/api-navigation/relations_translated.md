<!-- TRANSLATED by md-translate -->
---

source:
    - relations.py

источник:
- unitions.py

---

# Serializer relations

# Сериализационные отношения

> Data structures, not algorithms, are central to programming.
>
> &mdash; [Rob Pike](http://users.ece.utexas.edu/~adnan/pike.html)

> Структуры данных, а не алгоритмы, являются центральными для программирования.
>
> & mdash;
[Роб Пайк] (http://users.ece.utexas.edu/~adnan/pike.html)

Relational fields are used to represent model relationships.  They can be applied to `ForeignKey`, `ManyToManyField` and `OneToOneField` relationships, as well as to reverse relationships, and custom relationships such as `GenericForeignKey`.

Реляционные поля используются для представления модельных отношений.
Они могут быть применены к отношениям «иностранный», «Многотоманфилд» и «Онетонефилд», а также к обращению отношений и пользовательским отношениям, таким как «genericforeignkey».

---

**Note:** The relational fields are declared in `relations.py`, but by convention you should import them from the `serializers` module, using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.

** ПРИМЕЧАНИЕ.
`.

---

---

**Note:** REST Framework does not attempt to automatically optimize querysets passed to serializers in terms of `select_related` and `prefetch_related` since it would be too much magic. A serializer with a field spanning an orm relation through its source attribute could require an additional database hit to fetch related objects from the database. It is the programmer's responsibility to optimize queries to avoid additional database hits which could occur while using such a serializer.

** ПРИМЕЧАНИЕ.
Сериализатор с полем, охватывающим соотношение ORM через его атрибут источника, может потребовать дополнительного удара базы данных для извлечения связанных объектов из базы данных.
Ответственность программиста несет в себе оптимизацию запросов, чтобы избежать дополнительных попаданий в базу данных, которые могут возникнуть при использовании такого сериализатора.

For example, the following serializer would lead to a database hit each time evaluating the tracks field if it is not prefetched:

Например, следующий сериализатор приведет к тому, что база данных ударил каждый раз, когда оценивает поле треков, если оно не будет предварительно выбран:

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

Если `AlbumSerializer` используется для сериализации довольно большой запроса с` mysome = true`, то это может быть серьезной проблемой производительности.
Оптимизация запроса перехода к «альбомереализеру» с:

```
qs = Album.objects.prefetch_related('tracks')
# No additional database hits required
print(AlbumSerializer(qs, many=True).data)
```

would solve the issue.

решит проблему.

---

#### Inspecting relationships.

#### Проверка отношений.

When using the `ModelSerializer` class, serializer fields and relationships will be automatically generated for you. Inspecting these automatically generated fields can be a useful tool for determining how to customize the relationship style.

При использовании класса `modelerializer поля сериализатора и отношения будут автоматически созданы для вас.
Осмотр этих автоматически сгенерированных полей может быть полезным инструментом для определения того, как настроить стиль взаимоотношений.

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

# API Reference

# Ссылка на API

In order to explain the various types of relational fields, we'll use a couple of simple models for our examples.  Our models will be for music albums, and the tracks listed on each album.

Чтобы объяснить различные типы реляционных полей, мы будем использовать пару простых моделей для наших примеров.
Наши модели будут для музыкальных альбомов, а треки перечислены на каждом альбоме.

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

## StringRelatedfield

`StringRelatedField` may be used to represent the target of the relationship using its `__str__` method.

`StringRelatedField` может использоваться для представления цели взаимосвязи, используя его метод` __str__`.

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

Будет сериализовать на следующее представление:

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

Это поле читается только.

**Arguments**:

** Аргументы **:

* `many` - If applied to a to-many relationship, you should set this argument to `True`.

* `Много ' - если применяется к ко многим отношениям, вы должны установить этот аргумент на` true'.

## PrimaryKeyRelatedField

## Primarykeyrelatedfield

`PrimaryKeyRelatedField` may be used to represent the target of the relationship using its primary key.

`Primarykeyrelated Field можно использовать для представления цели взаимосвязи, используя его первичный ключ.

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

Будет сериализовать на такое представление, как это:

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

По умолчанию это поле считывается, хотя вы можете изменить это поведение, используя флаг `read_only`.

**Arguments**:

** Аргументы **:

* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.
* `pk_field` - Set to a field to control serialization/deserialization of the primary key's value. For example, `pk_field=UUIDField(format='hex')` would serialize a UUID primary key into its compact hex representation.

* `Queryset` - QuerySet, используемый для поиска экземпляров модели при проверке ввода поля.
Отношения должны либо установить запрос явно, либо установить `read_only = true`.
* `Много ' - если применяется к ко многим отношениям, вы должны установить этот аргумент на` true'.
* `allow_null` - Если установлено в` true`, поле примет значения `none` или пустую строку для нулевых отношений.
По умолчанию «ложь».
* `pk_field` - установить на поле для управления сериализацией/десериализацией значения первичного ключа.
Например, `pk_field = uuidfield (format = 'hex')` сериализует первичный ключ UUID в его компактный шестнадцатеричный представление.

## HyperlinkedRelatedField

## HyperlinkedRelatedfield

`HyperlinkedRelatedField` may be used to represent the target of the relationship using a hyperlink.

`HyperlinkedRelated` может использоваться для представления цели взаимосвязи с использованием гиперссылки.

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

Будет сериализовать на такое представление, как это:

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

По умолчанию это поле считывается, хотя вы можете изменить это поведение, используя флаг `read_only`.

---

**Note**: This field is designed for objects that map to a URL that accepts a single URL keyword argument, as set using the `lookup_field` and `lookup_url_kwarg` arguments.

** ПРИМЕЧАНИЕ **: Это поле предназначено для объектов, которые отображают URL, который принимает один аргумент ключевого слова URL, как установлено с использованием аргументов `lookup_field` и` lookup_url_kwarg`.

This is suitable for URLs that contain a single primary key or slug argument as part of the URL.

Это подходит для URL -адресов, которые содержат один первичный ключ или аргумент слизняка как часть URL.

If you require more complex hyperlinked representation you'll need to customize the field, as described in the [custom hyperlinked fields](#custom-hyperlinked-fields) section, below.

Если вам требуется более сложное гиперсвязанное представление, вам необходимо настраивать поле, как описано в разделе [Пользовательские гиперссылки] (#Custom-Hyperlinked-поля), ниже.

---

**Arguments**:

** Аргументы **:

* `view_name` - The view name that should be used as the target of the relationship.  If you're using [the standard router classes](https://www.django-rest-framework.org/api-guide/routers#defaultrouter) this will be a string with the format `<modelname>-detail`. **required**.
* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.
* `lookup_field` - The field on the target that should be used for the lookup.  Should correspond to a URL keyword argument on the referenced view.  Default is `'pk'`.
* `lookup_url_kwarg` - The name of the keyword argument defined in the URL conf that corresponds to the lookup field. Defaults to using the same value as `lookup_field`.
* `format` - If using format suffixes, hyperlinked fields will use the same format suffix for the target unless overridden by using the `format` argument.

* `view_name` - Имя представления, которое следует использовать в качестве цели отношений. Если вы используете [Стандартные классы маршрутизатора] (https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<modelname> -detail`. **требуется**.
* `Queryset` - QuerySet, используемый для поиска экземпляров модели при проверке ввода поля. Отношения должны либо установить запрос явно, либо установить `read_only = true`.
* `Много ' - если применяется к ко многим отношениям, вы должны установить этот аргумент на` true'.
* `allow_null` - Если установлено в` true`, поле примет значения `none` или пустую строку для нулевых отношений. По умолчанию «ложь».
* `lookup_field` - поле на цели, которое следует использовать для поиска. Должен соответствовать аргументу ключевого слова URL в указанном представлении. По умолчанию `'pk''.
* `lookup_url_kwarg` - имя аргумента ключевого слова, определенное в конфузе URL, которое соответствует полю поиска. По умолчанию использовать то же значение, что и `lookup_field`.
* `format` - если использование суффиксов формата, гиперсвязанные поля будут использовать один и тот же суффикс формата для цели, если это не переопределено, используя аргумент` format`.

## SlugRelatedField

## slugrelatedfield

`SlugRelatedField` may be used to represent the target of the relationship using a field on the target.

`SlugrelatedField можно использовать для представления цели взаимосвязи, используя поле на цели.

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

Будет сериализовать на такое представление, как это:

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

По умолчанию это поле считывается, хотя вы можете изменить это поведение, используя флаг `read_only`.

When using `SlugRelatedField` as a read-write field, you will normally want to ensure that the slug field corresponds to a model field with `unique=True`.

При использовании `slugrelatedfield` в качестве поля чтения-записи, вы обычно захотите убедиться, что поле слизни соответствует поле модели с` уникальным = true`.

**Arguments**:

** Аргументы **:

* `slug_field` - The field on the target that should be used to represent it.  This should be a field that uniquely identifies any given instance.  For example, `username`.  **required**
* `queryset` - The queryset used for model instance lookups when validating the field input. Relationships must either set a queryset explicitly, or set `read_only=True`.
* `many` - If applied to a to-many relationship, you should set this argument to `True`.
* `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.

* `slug_field` - поле на цели, которое следует использовать для его представления.
Это должно быть поле, которое однозначно идентифицирует любой данное экземпляр.
Например, «имя пользователя».
**требуется**
* `Queryset` - QuerySet, используемый для поиска экземпляров модели при проверке ввода поля.
Отношения должны либо установить запрос явно, либо установить `read_only = true`.
* `Много ' - если применяется к ко многим отношениям, вы должны установить этот аргумент на` true'.
* `allow_null` - Если установлено в` true`, поле примет значения `none` или пустую строку для нулевых отношений.
По умолчанию «ложь».

## HyperlinkedIdentityField

## Hyperlinkedidentityfield

This field can be applied as an identity relationship, such as the `'url'` field on  a HyperlinkedModelSerializer.  It can also be used for an attribute on the object.  For example, the following serializer:

Это поле может быть применено в качестве идентификационного отношения, например, поля «url'» на гиперлинкедмоделериализаторе.
Его также можно использовать для атрибута на объекте.
Например, следующий сериализатор:

```
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

Would serialize to a representation like this:

Будет сериализовать на такое представление, как это:

```
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

This field is always read-only.

Это поле всегда только читает.

**Arguments**:

** Аргументы **:

* `view_name` - The view name that should be used as the target of the relationship.  If you're using [the standard router classes](https://www.django-rest-framework.org/api-guide/routers#defaultrouter) this will be a string with the format `<model_name>-detail`.  **required**.
* `lookup_field` - The field on the target that should be used for the lookup.  Should correspond to a URL keyword argument on the referenced view.  Default is `'pk'`.
* `lookup_url_kwarg` - The name of the keyword argument defined in the URL conf that corresponds to the lookup field. Defaults to using the same value as `lookup_field`.
* `format` - If using format suffixes, hyperlinked fields will use the same format suffix for the target unless overridden by using the `format` argument.

* `view_name` - Имя представления, которое следует использовать в качестве цели отношений.
Если вы используете [Стандартные классы маршрутизатора] (https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<dethod_name> -detail`.
**требуется**.
* `lookup_field` - поле на цели, которое следует использовать для поиска.
Должен соответствовать аргументу ключевого слова URL в указанном представлении.
По умолчанию `'pk''.
* `lookup_url_kwarg` - имя аргумента ключевого слова, определенное в конфузе URL, которое соответствует полю поиска.
По умолчанию использовать то же значение, что и `lookup_field`.
* `format` - если использование суффиксов формата, гиперсвязанные поля будут использовать один и тот же суффикс формата для цели, если это не переопределено, используя аргумент` format`.

---

# Nested relationships

# Вложенные отношения

As opposed to previously discussed *references* to another entity, the referred entity can instead also be embedded or *nested*
in the representation of the object that refers to it.
Such nested relationships can be expressed by using serializers as fields.

В отличие от ранее обсуждаемых *ссылок *на другую сущность, указанная сущность также может быть встроена или *вложена *
в представлении объекта, который относится к нему.
Такие вложенные отношения могут быть выражены с использованием сериалов в качестве полей.

If the field is used to represent a to-many relationship, you should add the `many=True` flag to the serializer field.

Если поле используется для представления отношения ко многим, вы должны добавить флаг `myry = true` в поле сериализатора.

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

Будет сериализовать на вложенное представление, подобное этому:

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

## Вложенные сериалы для записи

By default nested serializers are read-only. If you want to support write-operations to a nested serializer field you'll need to create `create()` and/or `update()` methods in order to explicitly specify how the child relationships should be saved:

По умолчанию вложенные сериалы только для чтения.
Если вы хотите поддержать операции на записи в вложенное поле сериализатора, вам нужно будет создать методы `create ()` и/или `update ()`, чтобы явно указать, как должны быть сохранены отношения дочерних отношений:

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

In rare cases where none of the existing relational styles fit the representation you need,
you can implement a completely custom relational field, that describes exactly how the
output representation should be generated from the model instance.

В редких случаях, когда ни один из существующих реляционных стилей не соответствует необходимому вам представление,
Вы можете реализовать совершенно пользовательское реляционное поле, которое точно описывает, как
Выходное представление должно генерироваться из экземпляра модели.

To implement a custom relational field, you should override `RelatedField`, and implement the `.to_representation(self, value)` method. This method takes the target of the field as the `value` argument, and should return the representation that should be used to serialize the target. The `value` argument will typically be a model instance.

Чтобы реализовать пользовательское реляционное поле, вы должны переопределить `indulityfield` и реализовать метод` .to_representation (self, value) `.
Этот метод принимает цель поля в качестве аргумента «значения» и должен вернуть представление, которое следует использовать для сериализации цели.
Аргумент `value` обычно будет модельным экземпляром.

If you want to implement a read-write relational field, you must also implement the [`.to_internal_value(self, data)` method](https://www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data).

Если вы хотите реализовать реляционное поле Read-Write, вы также должны реализовать [`.to_internal_value (self, data)` method] (https://www.django-rest-framework.org/api-guide/serializers/
#to_internal_valueself-data).

To provide a dynamic queryset based on the `context`, you can also override `.get_queryset(self)` instead of specifying `.queryset` on the class or when initializing the field.

Чтобы обеспечить динамический запрос на основе «контекста», вы также можете переопределить `.get_queryset (self)` вместо указания `.queryset` на классе или при инициализации поля.

## Example

## Пример

For example, we could define a relational field to serialize a track to a custom string representation, using its ordering, title, and duration:

Например, мы могли бы определить реляционное поле для сериализации трека на индивидуальное представление строки, используя его упорядочение, заголовок и продолжительность:

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

Это пользовательское поле затем сериализуется на следующее представление:

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

# Пользовательские поля гиперссылки

In some cases you may need to customize the behavior of a hyperlinked field, in order to represent URLs that require more than a single lookup field.

В некоторых случаях вам может потребоваться настроить поведение поля с гиперссылкой, чтобы представлять URL-адреса, для которых требуется более одного поля поиска.

You can achieve this by overriding `HyperlinkedRelatedField`. There are two methods that may be overridden:

Вы можете добиться этого, переопределив `Hyperlink RelatedField`. Есть два метода, которые могут быть переопределены:

**get_url(self, obj, view_name, request, format)**

**get_url(self, obj, view_name, запрос, формат)**

The `get_url` method is used to map the object instance to its URL representation.

Метод `get_url` используется для сопоставления экземпляра объекта с его представлением URL.

May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
attributes are not configured to correctly match the URL conf.

Может возникнуть ошибка `NoReverseMatch`, если атрибуты `view_name` и `lookup_field' не настроены на корректное соответствие URL conf.

**get_object(self, view_name, view_args, view_kwargs)**

**get_object(self, view_name, view_args, view_kwargs)**

If you want to support a writable hyperlinked field then you'll also want to override `get_object`, in order to map incoming URLs back to the object they represent. For read-only hyperlinked fields there is no need to override this method.

Если вы хотите поддерживать доступное для записи поле с гиперссылками, вам также потребуется переопределить `get_object`, чтобы сопоставить входящие URL-адреса обратно с объектом, который они представляют. Для полей гиперссылок, доступных только для чтения, нет необходимости переопределять этот метод.

The return value of this method should the object that corresponds to the matched URL conf arguments.

Возвращаемым значением этого метода должен быть объект, соответствующий соответствующим аргументам URL conf.

May raise an `ObjectDoesNotExist` exception.

Может вызвать исключение "ObjectDoesNotExist".

## Example

## Пример

Say we have a URL for a customer object that takes two keyword arguments, like so:

Допустим, у нас есть URL-адрес объекта customer, который принимает два аргумента ключевого слова, например:

```
/api/<organization_slug>/customers/<customer_pk>/
```

This cannot be represented with the default implementation, which accepts only a single lookup field.

Это не может быть представлено с помощью реализации по умолчанию, которая принимает только одно поле поиска.

In this case we'd need to override `HyperlinkedRelatedField` to get the behavior we want:

В этом случае нам нужно было бы переопределить `Hyperlink RelatedField`, чтобы получить желаемое поведение:

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

Обратите внимание, что если вы хотите использовать этот стиль вместе с общими представлениями, то вам также нужно будет переопределить `.get_object` в представлении, чтобы получить правильное поведение поиска.

Generally we recommend a flat style for API representations where possible, but the nested URL style can also be reasonable when used in moderation.

Как правило, мы рекомендуем использовать единый стиль для представлений API, где это возможно, но вложенный стиль URL-адреса также может быть разумным при умеренном использовании.

---

# Further notes

# Дополнительные примечания

## The `queryset` argument

## Аргумент `queryset`

The `queryset` argument is only ever required for *writable* relationship field, in which case it is used for performing the model instance lookup, that maps from the primitive user input, into a model instance.

Аргумент `queryset` всегда требуется только для поля отношений *доступно для записи*, и в этом случае он используется для выполнения поиска экземпляра модели, который сопоставляется с примитивным пользовательским вводом в экземпляр модели.

In version 2.x a serializer class could *sometimes* automatically determine the `queryset` argument *if* a `ModelSerializer` class was being used.

В версии 2.x класс сериализатора *иногда* автоматически определял аргумент `queryset` *, если* использовался класс `ModelSerializer`.

This behavior is now replaced with *always* using an explicit `queryset` argument for writable relational fields.

Это поведение теперь заменено на *всегда* с использованием явного аргумента `queryset` для доступных для записи реляционных полей.

Doing so reduces the amount of hidden 'magic' that `ModelSerializer` provides, makes the behavior of the field more clear, and ensures that it is trivial to move between using the `ModelSerializer` shortcut, or using fully explicit `Serializer` classes.

Это уменьшает количество скрытой "магии", которую предоставляет "ModelSerializer", делает поведение поля более понятным и гарантирует, что тривиально переключаться между использованием ярлыка "ModelSerializer" или использованием полностью явных классов "Serializer".

## Customizing the HTML display

## Настройка отображения HTML-кода

The built-in `__str__` method of the model will be used to generate string representations of the objects used to populate the `choices` property. These choices are used to populate select HTML inputs in the browsable API.

Встроенный метод модели `__str__` будет использоваться для генерации строковых представлений объектов, используемых для заполнения свойства `choices`. Эти параметры используются для заполнения выбранных входных данных HTML в доступном для просмотра API.

To provide customized representations for such inputs, override `display_value()` of a `RelatedField` subclass. This method will receive a model object, and should return a string suitable for representing it. For example:

Чтобы предоставить настраиваемые представления для таких входных данных, переопределите `display_value()` подкласса `RelatedField`. Этот метод получит объект модели и должен вернуть строку, подходящую для его представления. Например:

```
class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Track: %s' % (instance.title)
```

## Select field cutoffs

## Выберите границы полей

When rendered in the browsable API relational fields will default to only displaying a maximum of 1000 selectable items. If more items are present then a disabled option with "More than 1000 items…" will be displayed.

При отображении в доступном для просмотра API реляционные поля по умолчанию будут отображать не более 1000 выбираемых элементов. Если присутствует больше элементов, то будет отображаться отключенная опция с надписью "Более 1000 элементов...".

This behavior is intended to prevent a template from being unable to render in an acceptable timespan due to a very large number of relationships being displayed.

Это поведение предназначено для предотвращения невозможности отображения шаблона в приемлемый промежуток времени из-за отображения очень большого количества взаимосвязей.

There are two keyword arguments you can use to control this behavior:

Есть два аргумента ключевого слова, которые вы можете использовать для управления этим поведением:

* `html_cutoff` - If set this will be the maximum number of choices that will be displayed by a HTML select drop down. Set to `None` to disable any limiting. Defaults to `1000`.
* `html_cutoff_text` - If set this will display a textual indicator if the maximum number of items have been cutoff in an HTML select drop down. Defaults to `"More than {count} items…"`

* `html_cutoff` - если задано, это будет максимальное количество вариантов, которые будут отображаться в раскрывающемся списке выбора HTML. Установите значение "Нет", чтобы отключить любые ограничения. Значение по умолчанию равно `1000`.* `html_cutoff_text` - если задано это значение, будет отображаться текстовый индикатор, если максимальное количество элементов было обрезано в раскрывающемся списке выбора HTML. Значение по умолчанию равно "Более {count} элементов..."`

You can also control these globally using the settings `HTML_SELECT_CUTOFF` and `HTML_SELECT_CUTOFF_TEXT`.

Вы также можете управлять ими глобально, используя настройки `HTML_SELECT_CUTOFF` и `HTML_SELECT_CUTOFF_TEXT`.

In cases where the cutoff is being enforced you may want to instead use a plain input field in the HTML form. You can do so using the `style` keyword argument. For example:

В тех случаях, когда ограничение применяется принудительно, вы можете вместо этого использовать обычное поле ввода в HTML-форме. Вы можете сделать это, используя аргумент ключевого слова `style`. Например:

```
assigned_to = serializers.SlugRelatedField(
   queryset=User.objects.all(),
   slug_field='username',
   style={'base_template': 'input.html'}
)
```

## Reverse relations

## ## Обратные отношения

Note that reverse relationships are not automatically included by the `ModelSerializer` and `HyperlinkedModelSerializer` classes.  To include a reverse relationship, you must explicitly add it to the fields list.  For example:

Обратите внимание, что обратные отношения не включаются автоматически классами `ModelSerializer` и `Hyperlink ModelSerializer`. Чтобы включить обратную связь, вы должны явно добавить ее в список полей. Например:

```
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tracks', ...]
```

You'll normally want to ensure that you've set an appropriate `related_name` argument on the relationship, that you can use as the field name.  For example:

Обычно вам нужно убедиться, что вы установили соответствующий аргумент `related_name` для отношения, который вы можете использовать в качестве имени поля. Например:

```
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    ...
```

If you have not set a related name for the reverse relationship, you'll need to use the automatically generated related name in the `fields` argument.  For example:

Если вы не задали связанное имя для обратной связи, вам нужно будет использовать автоматически сгенерированное связанное имя в аргументе `fields`. Например:

```
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['track_set', ...]
```

See the Django documentation on [reverse relationships](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward) for more details.

Смотрите документацию Django по [reverse relationships](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward ) для получения более подробной информации.

## Generic relationships

## Родовые отношения

If you want to serialize a generic foreign key, you need to define a custom field, to determine explicitly how you want to serialize the targets of the relationship.

Если вы хотите сериализовать общий внешний ключ, вам необходимо определить пользовательское поле, чтобы явно определить, как вы хотите сериализовать целевые объекты связи.

For example, given the following model for a tag, which has a generic relationship with other arbitrary models:

Например, дана следующая модель для тега, которая имеет общую связь с другими произвольными моделями:

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

Мы могли бы определить пользовательское поле, которое можно было бы использовать для сериализации помеченных экземпляров, используя тип каждого экземпляра, чтобы определить, как он должен быть сериализован:

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

Обратите внимание, что обратные универсальные ключи, выраженные с помощью поля `GenericRelation`, могут быть сериализованы с использованием обычных типов реляционных полей, поскольку тип целевого объекта в отношениях всегда известен.

For more information see [the Django documentation on generic relations](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1).

Для получения дополнительной информации см. [документацию Django по общим отношениям](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1 ).

## ManyToManyFields with a Through Model

## ## Manytomanyfield со сквозной моделью

By default, relational fields that target a `ManyToManyField` with a
`through` model specified are set to read-only.

По умолчанию для реляционных полей, которые нацелены на "ManyToManyField" с указанной моделью "throughthrough", установлено значение только для чтения.

If you explicitly specify a relational field pointing to a
`ManyToManyField` with a through model, be sure to set `read_only`
to `True`.

Если вы явно указываете реляционное поле, указывающее на `ManyToManyField` с сквозной моделью, обязательно установите для `read_only`
значение `True'.

If you wish to represent [extra fields on a through model](https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany) then you may serialize the through model as [a nested object](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects).

Если вы хотите представить [дополнительные поля в сквозной модели](https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany ) затем вы можете сериализовать сквозную модель как [вложенный объект](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects ).

---

# Third Party Packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF Nested Routers

## Вложенные маршрутизаторы DRF

The [drf-nested-routers package](https://github.com/alanjds/drf-nested-routers) provides routers and relationship fields for working with nested resources.

Пакет [drf-nested-routers package](https://github.com/alanjds/drf-nested-routers ) предоставляет маршрутизаторы и поля связей для работы с вложенными ресурсами.

## Rest Framework Generic Relations

## Общие отношения Rest Framework

The [rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations) library provides read/write serialization for generic foreign keys.

[rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations ) библиотека обеспечивает сериализацию чтения /записи для общих внешних ключей.
