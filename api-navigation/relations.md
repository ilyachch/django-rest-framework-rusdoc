# Отношения сериализатора

> Структуры данных, а не алгоритмы, играют ключевую роль в программировании.
>
> — [Rob Pike][cite]

Реляционные поля используются для представления отношений модели. Они могут применяться к отношениям `ForeignKey`, `ManyToManyField` и `OneToOneField`, а также к обратным отношениям и настраиваемым отношениям, таким как `GenericForeignKey`.

---

**Примечание:** Реляционные поля объявлены в файле `Relations.py`, но по соглашению вы должны импортировать их из модуля `serializers`, используя `from rest_framework import serializers` и называть поля `сериализаторами.<FieldName>`.

---

#### Проверка отношений.

При использовании класса `ModelSerializer` поля и отношения сериализатора будут автоматически сгенерированы для вас. Проверка этих автоматически сгенерированных полей может быть полезным инструментом для определения того, как настроить стиль отношений.

Для этого откройте оболочку Django, используя `python manage.py shell`, затем импортируйте класс сериализатора, создайте его экземпляр и распечатайте представление объекта...

```python
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

# Справочник по API

Чтобы объяснить различные типы реляционных полей, мы воспользуемся парой простых моделей для наших примеров. Наши модели будут для музыкальных альбомов и треков, перечисленных в каждом альбоме.

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

`StringRelatedField` может использоваться для представления цели отношения с помощью его метода __str__.

Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Будет сериализован в следующее представление:

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

* `many` - если применяется к отношению ко многим, вы должны установить для этого аргумента значение `True`.

## PrimaryKeyRelatedField

`PrimaryKeyRelatedField` может использоваться для представления цели отношения с использованием ее первичного ключа.

Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Будет сериализован в такое представление:

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

По умолчанию это поле предназначено для чтения и записи, хотя вы можете изменить это поведение, используя флаг `read_only`.

**Аргументы**:

* `queryset` - набор запросов, используемый для поиска экземпляров модели при проверке ввода поля. Отношения должны либо явно задавать набор запросов, либо устанавливать `read_only=True`.
* `many` - если применяется к отношению ко многим, вы должны установить для этого аргумента значение `True`.
* `Allow_null` - Если установлено значение `True`, поле будет принимать значения `None` или пустую строку для обнуляемых отношений. По умолчанию False.
* `pk_field` - Установите в поле для управления сериализацией / десериализацией значения первичного ключа. Например, `pk_field = UUIDField(format='hex')` сериализует первичный ключ UUID в его компактное шестнадцатеричное представление.

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

Будет сериализован в такое представление:

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

По умолчанию это поле предназначено для чтения и записи, хотя вы можете изменить это поведение, используя флаг `read_only`.

---

**Примечание**: это поле предназначено для объектов, которые сопоставляются с URL-адресом, который принимает один аргумент ключевого слова URL-адреса, установленный с помощью аргументов `lookup_field` и` lookup_url_kwarg`.

Это подходит для URL-адресов, которые содержат один первичный ключ или аргумент slug как часть URL-адреса.

Если вам требуется более сложное представление с гиперссылками, вам необходимо настроить поле, как описано в разделе [настраиваемые поля с гиперссылками](#custom-hyperlinked-fields) ниже.

---

**Аргументы**:

* `view_name` - имя представления, которое должно использоваться как цель отношения. Если вы используете [стандартные классы маршрутизаторов][routers], это будет строка в формате `<имя модели>-detail`. **обязательный**.
* `queryset` - набор запросов, используемый для поиска экземпляров модели при проверке ввода поля. Отношения должны либо явно задавать набор запросов, либо устанавливать `read_only=True`.
* `many` - если применяется к отношению ко многим, вы должны установить для этого аргумента значение `True`.
* `allow_null` - Если установлено значение `True`, поле будет принимать значения `None` или пустую строку для отношений, допускающих значение NULL. По умолчанию `False`.
* `lookup_field` - поле цели, которое должно использоваться для поиска. Должен соответствовать аргументу ключевого слова URL в указанном представлении. По умолчанию - `'pk'`.
* `lookup_url_kwarg` - Имя аргумента ключевого слова, определенного в URL-conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, поля с гиперссылками будут использовать тот же суффикс формата для целевого объекта, если он не переопределен с помощью аргумента` format`.

## SlugRelatedField

`SlugRelatedField` может использоваться для представления цели отношения, используя поле цели.

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

Будет сериализован в такое представление:

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

По умолчанию это поле предназначено для чтения и записи, хотя вы можете изменить это поведение, используя флаг `read_only`.

При использовании `SlugRelatedField` в качестве поля для чтения и записи обычно требуется убедиться, что поле slug соответствует полю модели с `unique=True`.

**Аргументы**:

* `slug_field` - Поле цели, которое должно использоваться для ее представления. Это должно быть поле, которое однозначно идентифицирует любой данный экземпляр. Например, `username`. **обязательный**
* `queryset` - набор запросов, используемый для поиска экземпляров модели при проверке ввода поля. Отношения должны либо явно задавать набор запросов, либо устанавливать `read_only=True`.
* `many` - если применяется к отношению ко многим, вы должны установить для этого аргумента значение `True`.
* `Allow_null` - Если установлено значение `True`, поле будет принимать значения `None` или пустую строку для обнуляемых отношений. По умолчанию `False`.

## HyperlinkedIdentityField

Это поле может применяться в качестве отношения идентичности, например, в качестве поля `'url'` в `HyperlinkedModelSerializer`. Его также можно использовать для атрибута объекта. Например, следующий сериализатор:

```python
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

Будет сериализован в такое представление:

```python
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

Это поле всегда только для чтения.

**Аргументы**:

* `view_name` - имя представления, которое должно использоваться как цель отношения. Если вы используете [стандартные классы маршрутизаторов][routers], это будет строка в формате `<имя_модели>-detail`. **обязательный**.
* `lookup_field` - поле цели, которое должно использоваться для поиска. Должен соответствовать аргументу ключевого слова URL в указанном представлении. По умолчанию - `'pk'`.
* `lookup_url_kwarg` - Имя аргумента ключевого слова, определенного в URL-адресе conf, который соответствует полю поиска. По умолчанию используется то же значение, что и `lookup_field`.
* `format` - Если используются суффиксы формата, поля с гиперссылками будут использовать тот же суффикс формата для целевого объекта, если он не переопределен с помощью аргумента `format`.

# Вложенные отношения

В отличие от ранее обсужденных _references_ к другой сущности, упомянутая сущность может вместо этого также быть встроена или _nested_ в представление объекта, который ссылается на нее. Такие вложенные отношения могут быть выражены с помощью сериализаторов в качестве полей.

Если поле используется для представления отношения ко многим, вы должны добавить флаг `many=True` в поле сериализатора.

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

Будет сериализоваться во вложенное представление следующим образом:

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

## Вложенные сериализаторы с возможностью записи

По умолчанию вложенные сериализаторы доступны только для чтения. Если вы хотите поддерживать операции записи во вложенное поле сериализатора, вам необходимо создать методы `create()` и/или `update()`, чтобы явно указать, как следует сохранять дочерние отношения:

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

# Пользовательские реляционные поля

В редких случаях, когда ни один из существующих реляционных стилей не подходит для нужного вам представления, вы можете реализовать полностью настраиваемое реляционное поле, которое точно описывает, как выходное представление должно быть сгенерировано из экземпляра модели.

Чтобы реализовать настраиваемое реляционное поле, вы должны переопределить `RelatedField` и реализовать метод `.to_presentation(self, value)`. Этот метод принимает цель поля в качестве аргумента `value` и должен возвращать представление, которое следует использовать для сериализации цели. Аргумент `value` обычно будет экземпляром модели.

Если вы хотите реализовать реляционное поле для чтения и записи, вы также должны реализовать метод [`.to_internal_value(self, data)`] [to_internal_value].

Чтобы предоставить динамический набор запросов на основе `context`, вы также можете переопределить `.get_queryset (self)` вместо указания `.queryset` в классе или при инициализации поля.

## Пример

Для примера, мы могли бы определить реляционное поле для сериализации дорожки в настраиваемое строковое представление, используя ее порядок, заголовок и продолжительность:

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

Это настраиваемое поле затем будет сериализовано в следующее представление:

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

# Custom hyperlinked fields

В некоторых случаях вам может потребоваться настроить поведение поля с гиперссылкой, чтобы представлять URL-адреса, для которых требуется более одного поля поиска.

Вы можете добиться этого, переопределив `HyperlinkedRelatedField`. Есть два метода, которые можно переопределить:

**get_url(self, obj, view_name, request, format)**

Метод `get_url` используется для сопоставления экземпляра объекта с его представлением URL.

Может вызвать `NoReverseMatch`, если атрибуты `view_name` и `lookup_field` не настроены для правильного соответствия URL conf.

**get_object(self, view_name, view_args, view_kwargs)**

Если вы хотите поддерживать доступное для записи поле с гиперссылкой, вы также захотите переопределить `get_object`, чтобы отображать входящие URL-адреса обратно в объект, который они представляют. Для полей с гиперссылками только для чтения нет необходимости переопределять этот метод.

Возвращаемое значение этого метода должно быть объектом, который соответствует согласованным аргументам conf URL.

Может вызвать исключение `ObjectDoesNotExist`.

## Пример

Допустим, у нас есть URL-адрес для объекта клиента, который принимает два аргумента ключевого слова, например:

```python
/api/<organization_slug>/customers/<customer_pk>/
```

Это не может быть представлено реализацией по умолчанию, которая принимает только одно поле поиска.

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

Обратите внимание: если вы хотите использовать этот стиль вместе с общими представлениями, вам также необходимо переопределить `.get_object` в представлении, чтобы получить правильное поведение поиска.

Обычно мы рекомендуем плоский стиль для представлений API, где это возможно, но вложенный стиль URL также может быть разумным при использовании в модерации.

# Дальнейшие примечания

## Аргумент `queryset`

Аргумент `queryset` всегда требуется только для *записываемого* поля отношения, и в этом случае он используется для выполнения поиска экземпляра модели, который преобразуется из примитивного пользовательского ввода в экземпляр модели.

В версии 2.x класс сериализатора мог *иногда* автоматически определять аргумент `queryset`, *если* использовался класс `ModelSerializer`.

Это поведение теперь заменено на "*всегда*" с использованием явного аргумента `queryset` для доступных для записи реляционных полей.

Doing so reduces the amount of hidden 'magic' that `ModelSerializer` provides, makes the behavior of the field more clear, and ensures that it is trivial to move between using the `ModelSerializer` shortcut, or using fully explicit `Serializer` classes.

Это уменьшает количество скрытой «магии», которую предоставляет `ModelSerializer`, делает поведение поля более понятным и гарантирует тривиальность перехода между использованием ярлыка `ModelSerializer` или использованием полностью явных классов `Serializer`.

## Настройка отображения HTML

Встроенный метод модели `__str__` будет использоваться для генерации строковых представлений объектов, используемых для заполнения свойства `choices`. Эти варианты используются для заполнения выбранных входов HTML в доступном для просмотра API.

Чтобы обеспечить индивидуальное представление таких входных данных, переопределите `display_value()` подкласса `RelatedField`. Этот метод получит объект модели и должен вернуть строку, подходящую для его представления. Например:

```python
class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Track: %s' % (instance.title)
```

## Выберите обрезки полей

При отображении в доступных для просмотра реляционных полях API по умолчанию отображается не более 1000 выбираемых элементов. Если присутствуют другие элементы, то будет отображаться отключенная опция с «More than 1000 items...».

Такое поведение предназначено для предотвращения невозможности визуализации шаблона в приемлемый промежуток времени из-за отображения очень большого количества взаимосвязей.

Для управления этим поведением можно использовать два аргумента ключевого слова:

- `html_cutoff` - если установлено, это будет максимальное количество вариантов, которое будет отображаться в раскрывающемся списке выбора HTML. Установите значение `None`, чтобы отключить какие-либо ограничения. По умолчанию `1000`.
- `html_cutoff_text` - Если установлено, это будет отображать текстовый индикатор, если максимальное количество элементов было вырезано в раскрывающемся списке выбора HTML. По умолчанию: `More than {count} items...`

Вы также можете управлять ими глобально, используя настройки `HTML_SELECT_CUTOFF` и `HTML_SELECT_CUTOFF_TEXT`.

В случаях, когда выполняется принудительное отключение, вы можете вместо этого использовать простое поле ввода в форме HTML. Вы можете сделать это с помощью аргумента ключевого слова `style`. Например:

```python
assigned_to = serializers.SlugRelatedField(
    queryset=User.objects.all(),
    slug_field='username',
    style={'base_template': 'input.html'}
)
```

## Обратные отношения

Обратите внимание, что обратные отношения не включаются автоматически в классы `ModelSerializer` и `HyperlinkedModelSerializer`. Чтобы включить обратную связь, вы должны явно добавить ее в список полей. Например:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tracks', ...]
```

Обычно вы хотите убедиться, что вы установили соответствующий аргумент `related_name` для отношения, который вы можете использовать в качестве имени поля. Например:

```python
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    ...
```

Если вы не установили связанное имя для обратной связи, вам нужно будет использовать автоматически сгенерированное связанное имя в аргументе `fields`. Например:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['track_set', ...]
```

См. Документацию Django по [обратным отношениям][reverse-relationships] для получения более подробной информации.

## Общие отношения

Если вы хотите сериализовать общий внешний ключ, вам необходимо определить настраиваемое поле, чтобы явно определить, как вы хотите сериализовать цели отношения.

Например, учитывая следующую модель тега, которая имеет общие отношения с другими произвольными моделями:

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

Мы могли бы определить настраиваемое поле, которое можно было бы использовать для сериализации помеченных экземпляров, используя тип каждого экземпляра, чтобы определить, как он должен быть сериализован:

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

Если вам нужно, чтобы цель отношения имела вложенное представление, вы можете использовать требуемые сериализаторы внутри метода `.to_presentation()`:

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

Обратите внимание, что обратные универсальные ключи, выраженные с помощью поля `GenericRelation`, могут быть сериализованы с использованием обычных реляционных типов полей, поскольку тип цели в отношении всегда известен.

Для получения дополнительной информации см. [документацию Django по родовым отношениям][generic-relations].

## ManyToManyFields с промежуточной моделью

По умолчанию реляционные поля, нацеленные на `ManyToManyField` с указанной моделью `through`, предназначены только для чтения.

Если вы явно указываете реляционное поле, указывающее на `ManyToManyField` со сквозной моделью, обязательно установите для `read_only` значение `True`.

Если вы хотите представить [дополнительные поля в сквозной модели][django-mediary-manytomany], вы можете сериализовать сквозную модель как [вложенный объект][dealing-with-nested-objects].

# Сторонние пакеты

Также доступны следующие сторонние пакеты.

## Вложенные маршрутизаторы DRF

Пакет [drf-nested-router package][drf-nested-routers] предоставляет маршрутизаторы и поля отношений для работы с вложенными ресурсами.

## Общие отношения Rest Framework


Библиотека [rest-framework-generic-Relations][drf-nested-Relations] обеспечивает сериализацию чтения/записи для общих внешних ключей.

[cite]: http://users.ece.utexas.edu/~adnan/pike.html
[reverse-relationships]: https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward
[routers]: https://www.django-rest-framework.org/api-guide/routers#defaultrouter
[generic-relations]: https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1
[drf-nested-routers]: https://github.com/alanjds/drf-nested-routers
[drf-nested-relations]: https://github.com/Ian-Foote/rest-framework-generic-relations
[django-intermediary-manytomany]: https://docs.djangoproject.com/en/2.2/topics/db/models/#intermediary-manytomany
[dealing-with-nested-objects]: https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
[to_internal_value]: https://www.django-rest-framework.org/api-guide/serializers/#to_internal_valueself-data
