<!-- TRANSLATED by md-translate -->
# Отношения сериализаторов

> Структуры данных, а не алгоритмы, занимают центральное место в программировании.
>
> - [Роб Пайк](http://users.ece.utexas.edu/~adnan/pike.html)

Реляционные поля используются для представления отношений между моделями. Они могут применяться к отношениям `ForeignKey`, `ManyToManyField` и `OneToOneField`, а также к обратным отношениям и пользовательским отношениям, таким как `GenericForeignKey`.

---

**Примечание:** Реляционные поля объявляются в `relations.py`, но по соглашению вы должны импортировать их из модуля `serializers`, используя `from rest_framework import serializers` и ссылаться на поля как `serializers.<FieldName>`.

---

**Примечание:** DRF не пытается автоматически оптимизировать передаваемые сериализаторам наборы запросов в терминах `select_related` и `prefetch_related`, поскольку это было бы слишком сложной магией. Сериализатор с полем, охватывающим отношение orm через атрибут source, может потребовать дополнительного обращения к базе данных для получения связанных объектов из базы данных. В обязанности программиста входит оптимизация запросов, чтобы избежать дополнительных обращений к базе данных, которые могут возникнуть при использовании такого сериализатора.

Например, следующий сериализатор будет приводить к попаданию в базу данных каждый раз при оценке поля `tracks`, если оно не префетчено:

```python
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

Если `AlbumSerializer` используется для сериализации довольно большого набора запросов с `many=True`, то это может стать серьезной проблемой производительности. Оптимизация кверисета, передаваемого `AlbumSerializer` с:

```python
qs = Album.objects.prefetch_related('tracks')
# No additional database hits required
print(AlbumSerializer(qs, many=True).data)
```

решит эту проблему.

---

#### Инспектирование отношений.

При использовании класса `ModelSerializer`, поля и отношения сериализатора будут автоматически сгенерированы для вас. Проверка этих автоматически сгенерированных полей может быть полезным инструментом для определения того, как настроить стиль отношений.

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

# API Reference

Для того чтобы объяснить различные типы реляционных полей, мы будем использовать пару простых моделей для наших примеров. Нашими моделями будут музыкальные альбомы и треки, перечисленные в каждом альбоме.

```python
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

`StringRelatedField` может использоваться для представления цели отношения с помощью своего метода `__str__`.

Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Сериализуется в следующее представление:

```python
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

Это поле доступно только для чтения.

**Аргументы**:

* `many` - Если применяется к отношениям типа "ко многим", следует установить этот аргумент в `True`.

## PrimaryKeyRelatedField

`PrimaryKeyRelatedField` может использоваться для представления цели отношения с помощью его первичного ключа.

Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Сериализуется в представление, подобное этому:

```python
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

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

**Аргументы**:

* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию `False`.
* `pk_field` - Устанавливается в поле для управления сериализацией/десериализацией значения первичного ключа. Например, `pk_field=UUIDField(format='hex')` будет сериализовать первичный ключ UUID в его компактное шестнадцатеричное представление.

## HyperlinkedRelatedField

`HyperlinkedRelatedField` может использоваться для представления цели отношения с помощью гиперссылки.

Например, следующий сериализатор:

```python
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

Сериализуется в представление, подобное этому:

```python
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

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

---

**Примечание**: Это поле предназначено для объектов, сопоставленных с URL, который принимает один именованный аргумент URL, заданный с помощью аргументов `lookup_field` и `lookup_url_kwarg`.

Это подходит для URL, которые содержат один первичный ключ или аргумент slug как часть URL.

Если вам требуется более сложное представление гиперссылок, вам необходимо настроить поле, как описано ниже в разделе [пользовательские гиперссылочные поля](#пользовательские-поля-с-гиперссылками).

---

**Аргументы**:

* `view_name` - Имя представления, которое должно использоваться в качестве цели отношения. Если вы используете [стандартные классы маршрутизаторов](https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<имя модели>-detail`. **необходимо**.
* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию `False`.
* `lookup_field` - Поле цели, которое должно быть использовано для поиска. Должно соответствовать именованному аргументу URL в ссылающемся представлении. По умолчанию `'pk'`.
* `lookup_url_kwarg` - Имя именованного аргумента, определенного в URL conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, то поля с гиперссылками будут использовать тот же суффикс формата для цели, если это не отменено с помощью аргумента `format`.

## SlugRelatedField

`SlugRelatedField` может использоваться для представления цели отношения с помощью поля цели.

Например, следующий сериализатор:

```python
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

Сериализуется в представление, подобное этому:

```python
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

По умолчанию это поле предназначено для чтения-записи, хотя вы можете изменить это поведение с помощью флага `read_only`.

При использовании `SlugRelatedField` в качестве поля для чтения-записи вы обычно хотите убедиться, что поле slug соответствует полю модели с `unique=True`.

**Аргументы**:

* `slug_field` - Поле цели, которое должно быть использовано для ее представления. Это должно быть поле, которое однозначно идентифицирует любой данный экземпляр. Например, `username`. **обязательно**
* `queryset` - Набор запросов, используемый для поиска экземпляра модели при проверке ввода поля. Отношения должны либо явно задать queryset, либо установить `read_only=True`.
* `many` - Если применяется к отношениям типа "ко многим", вы должны установить этот аргумент в `True`.
* `allow_null` - Если установить значение `True`, поле будет принимать значения `None` или пустую строку для нулевых отношений. По умолчанию установлено значение `False`.

## HyperlinkedIdentityField

Это поле может применяться как отношение идентичности, например, поле `'url'` в `HyperlinkedModelSerializer`. Оно также может быть использовано для атрибута объекта. Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

Сериализуется в представление, подобное этому:

```python
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

Это поле всегда доступно только для чтения.

**Аргументы**:

* `view_name` - Имя представления, которое должно использоваться в качестве цели отношения. Если вы используете [стандартные классы маршрутизаторов](https://www.django-rest-framework.org/api-guide/routers#defaultrouter), это будет строка с форматом `<имя_модели>-detail`. **необходимо**.
* `lookup_field` - Поле цели, которое должно быть использовано для поиска. Должно соответствовать именованному аргументу URL в ссылающемся представлении. По умолчанию `'pk'`.
* `lookup_url_kwarg` - Имя именованного слова, определенного в URL conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, поля с гиперссылками будут использовать тот же суффикс формата для цели, если это не будет отменено с помощью аргумента `format`.

---

# Вложенные отношения

В отличие от ранее рассмотренных *ссылок* на другую сущность, ссылающаяся сущность может быть встроена или *вложена* в представление объекта, который на нее ссылается. Такие вложенные отношения могут быть выражены с помощью сериализаторов в качестве полей.

Если поле используется для представления отношения "ко многим", необходимо добавить флаг `many=True` к полю сериализатора.

## Пример

Например, следующий сериализатор:

```python
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

Сериализуется во вложенное представление следующим образом:

```python
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

## Записываемые вложенные сериализаторы

По умолчанию вложенные сериализаторы доступны только для чтения. Если вы хотите поддерживать операции записи во вложенное поле сериализатора, вам необходимо создать методы `create()` и/или `update()`, чтобы явно указать, как должны сохраняться дочерние отношения:

```python
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

# Пользовательские реляционные поля

В редких случаях, когда ни один из существующих реляционных стилей не подходит для нужного вам представления, вы можете реализовать полностью пользовательское реляционное поле, которое описывает, как именно должно быть сгенерировано выходное представление из экземпляра модели.

Для реализации пользовательского реляционного поля необходимо переопределить `RelatedField` и реализовать метод `.to_representation(self, value)`. Этот метод принимает цель поля в качестве аргумента `value` и должен возвращать представление, которое должно использоваться для сериализации цели. Аргумент `value` обычно представляет собой экземпляр модели.

Если вы хотите реализовать реляционное поле для чтения и записи, вы должны также реализовать метод [`.to_internal_value(self, data)`](https://www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data).

Чтобы обеспечить динамический набор запросов, основанный на `context`, вы также можете переопределить `.get_queryset(self)` вместо указания `.queryset` в классе или при инициализации поля.

## Пример

Например, мы можем определить реляционное поле для сериализации трека в пользовательское строковое представление, используя его порядок, название и продолжительность:

```python
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

Это пользовательское поле затем сериализуется в следующее представление:

```python
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

# Пользовательские поля с гиперссылками

В некоторых случаях вам может понадобиться настроить поведение поля с гиперссылкой, чтобы представить URL-адреса, для которых требуется более одного поля поиска.

Вы можете добиться этого, переопределив `HyperlinkedRelatedField`. Есть два метода, которые могут быть переопределены:

**get_url(self, obj, view_name, request, format)**.

Метод `get_url` используется для сопоставления экземпляра объекта с его URL-представлением.

Может вызвать ошибку `NoReverseMatch`, если атрибуты `view_name` и `lookup_field` не настроены на правильное соответствие URL conf.

**get_object(self, view_name, view_args, view_kwargs)**.

Если вы хотите поддерживать записываемое поле с гиперссылками, вам также потребуется переопределить `get_object`, чтобы сопоставить входящие URL обратно с объектом, который они представляют. Для полей с гиперссылками, доступных только для чтения, нет необходимости переопределять этот метод.

Возвращаемое значение этого метода - объект, соответствующий аргументам URL conf.

Может вызвать исключение `ObjectDoesNotExist`.

## Пример

Допустим, у нас есть URL для объекта customer, который принимает два аргумента в виде ключевых слов, как показано ниже:

```python
/api/<organization_slug>/customers/<customer_pk>/
```

Это не может быть представлено с помощью реализации по умолчанию, которая принимает только одно поле поиска.

В этом случае нам нужно переопределить `HyperlinkedRelatedField`, чтобы получить желаемое поведение:

```python
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

Обратите внимание, что если вы хотите использовать этот стиль вместе с общими представлениями, то вам также необходимо переопределить `.get_object` в представлении, чтобы получить правильное поведение поиска.

Обычно мы рекомендуем использовать плоский стиль для представления API, когда это возможно, но вложенный стиль URL также может быть разумным при умеренном использовании.

---

# Дальнейшие примечания

## Аргумент `queryset`.

Аргумент `queryset` требуется только для *записываемого* поля отношения, в этом случае он используется для выполнения поиска экземпляра модели, который отображает примитивный пользовательский ввод в экземпляр модели.

В версии 2.x класс сериализатора мог *иногда* автоматически определять аргумент `queryset`, *если* использовался класс `ModelSerializer`.

Теперь это поведение заменено на *всегда* использование явного аргумента `queryset` для записываемых реляционных полей.

Это уменьшает количество скрытой "магии", которую обеспечивает `ModelSerializer`, делает поведение поля более понятным и гарантирует, что можно легко переходить от использования ярлыка `ModelSerializer` к использованию полностью явных классов `Serializer`.

## Настройка отображения HTML

Встроенный метод `__str__` модели будет использоваться для создания строковых представлений объектов, используемых для заполнения свойства `choices`. Эти варианты используются для заполнения HTML-вводов выбора в Web-интерфейсе API.

Чтобы обеспечить настраиваемое представление для таких входов, переопределите `display_value()` подкласса `RelatedField`. Этот метод получит объект модели и должен вернуть строку, подходящую для его представления. Например:

```python
class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Track: %s' % (instance.title)
```

## Выберите отсечение полей

При отображении в Web-интерфейсе API реляционные поля по умолчанию будут отображать не более 1000 элементов для выбора. Если элементов больше, то будет отображаться отключенная опция `'More than 1000 items...'`.

Это поведение предназначено для того, чтобы предотвратить невозможность отрисовки шаблона за приемлемое время из-за отображения очень большого количества связей.

Есть два именованных аргумента, которые можно использовать для управления этим поведением:

* `html_cutoff` - Если установлено, это будет максимальное количество вариантов выбора, которое будет отображаться в выпадающем списке HTML select. Установите значение `None`, чтобы отключить любое ограничение. По умолчанию `1000`.
* `html_cutoff_text` - При установке этого параметра будет отображаться текстовый индикатор, если максимальное количество элементов было отсечено в выпадающем списке HTML select. По умолчанию `'More than {count} items...'`.

Вы также можете управлять ими глобально, используя настройки `HTML_SELECT_CUTOFF` и `HTML_SELECT_CUTOFF_TEXT`.

В случаях, когда отсечение вводится принудительно, вы можете использовать обычное поле ввода в HTML-форме. Вы можете сделать это, используя именованный аргумент `style`. Например:

```python
assigned_to = serializers.SlugRelatedField(
   queryset=User.objects.all(),
   slug_field='username',
   style={'base_template': 'input.html'}
)
```

## Обратные отношения

Обратите внимание, что обратные отношения не включаются автоматически классами `ModelSerializer` и `HyperlinkedModelSerializer`. Чтобы включить обратное отношение, вы должны явно добавить его в список полей. Например:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tracks', ...]
```

Обычно вам нужно убедиться, что вы установили соответствующий аргумент `related_name` для отношения, который вы можете использовать в качестве имени поля. Например:

```python
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    ...
```

Если вы не задали связанное имя для обратного отношения, вам придется использовать автоматически сгенерированное связанное имя в аргументе `fields`. Например:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['track_set', ...]
```

Более подробную информацию смотрите в документации Django по [обратным отношениям](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward).

## Общие отношения

Если вы хотите сериализовать общий внешний ключ, вам необходимо определить пользовательское поле, чтобы явно определить, как вы хотите сериализовать цели отношения.

Например, дана следующая модель для тега, которая имеет общие отношения с другими произвольными моделями:

```python
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

И следующие две модели, которые могут иметь связанные теги:

```python
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

Мы можем определить пользовательское поле, которое будет использоваться для сериализации помеченных экземпляров, используя тип каждого экземпляра для определения того, как он должен быть сериализован:

```python
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

Если вам нужно, чтобы цель отношения имела вложенное представление, вы можете использовать необходимые сериализаторы внутри метода `.to_representation()`:

```python
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

Обратите внимание, что обратные родовые ключи, выраженные с помощью поля `GenericRelation`, могут быть сериализованы с использованием обычных типов реляционных полей, поскольку тип цели в отношениях всегда известен.

Для получения дополнительной информации смотрите [документацию Django по общим отношениям](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1).

## ManyToManyFields со сквозной моделью

По умолчанию реляционные поля, нацеленные на `ManyToManyField` с указанной моделью `through`, устанавливаются только для чтения.

Если вы явно указываете реляционное поле, указывающее на `ManyToManyField` со сквозной моделью, обязательно установите `read_only` в `True`.

Если вы хотите представить [дополнительные поля в сквозной модели](https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany), то вы можете сериализовать сквозную модель как [вложенный объект](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects).

---

# Сторонние пакеты

Также доступны следующие пакеты сторонних производителей.

## DRF nested routers

Пакет [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) предоставляет маршрутизаторы и поля отношений для работы с вложенными ресурсами.

## Rest Framework Generic Relations

Библиотека [rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations) обеспечивает сериализацию чтения/записи для общих внешних ключей.
