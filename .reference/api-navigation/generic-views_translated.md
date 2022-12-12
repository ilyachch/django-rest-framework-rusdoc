<!-- TRANSLATED by md-translate -->
---

source:

источник:

* mixins.py
* generics.py

* Mixins.py
* generics.py

---

# Generic views

# Общие виды

> Django’s generic views... were developed as a shortcut for common usage patterns... They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to repeat yourself.
>
> — [Django Documentation](https://docs.djangoproject.com/en/stable/ref/class-based-views/#base-vs-generic-views)

> Общие взгляды Джанго ... были разработаны в качестве ярлыка для общих моделей использования ... они принимают определенные общие идиомы и закономерности, найденные в области развития и абстрагируют их, чтобы вы могли быстро писать общие взгляды на данные, не повторяя себя.
>
>-[Django Documentation] (https://docs.djangoproject.com/en/stable/ref/class на основе Views/#base-vs-generic-views)

One of the key benefits of class-based views is the way they allow you to compose bits of reusable behavior. REST framework takes advantage of this by providing a number of pre-built views that provide for commonly used patterns.

Одним из ключевых преимуществ взглядов на основе классов является то, как они позволяют вам составлять биты многоразового поведения.
REST Framework использует это, предоставляя ряд предварительно созданных представлений, которые обеспечивают широко используемые шаблоны.

The generic views provided by REST framework allow you to quickly build API views that map closely to your database models.

Общие представления, предоставленные Framework REST, позволяют быстро создавать представления API, которые тесно связаны с вашими моделями базы данных.

If the generic views don't suit the needs of your API, you can drop down to using the regular `APIView` class, or reuse the mixins and base classes used by the generic views to compose your own set of reusable generic views.

Если общие виды не соответствуют потребностям вашего API, вы можете прийти к использованию обычного класса `apiview` или повторно использовать микшины и базовые классы, используемые общими представлениями для составления собственного набора многоразовых общих видов.

## Examples

## Примеры

Typically when using the generic views, you'll override the view, and set several class attributes.

Как правило, при использовании общих представлений вы переопределяете представление и установите несколько атрибутов класса.

```
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
```

For more complex cases you might also want to override various methods on the view class. For example.

Для более сложных случаев вы также можете переопределить различные методы в классе View.
Например.

```
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
```

For very simple cases you might want to pass through any class attributes using the `.as_view()` method. For example, your URLconf might include something like the following entry:

Для очень простых случаев вы можете пройти через любые атрибуты класса, используя метод `.as_view ()`.
Например, ваш UrlConf может включать в себя что -то вроде следующей записи:

```
path('users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
```

---

# API Reference

# Ссылка на API

## GenericAPIView

## genericapiview

This class extends REST framework's `APIView` class, adding commonly required behavior for standard list and detail views.

Этот класс расширяет класс Framework `apiview`, добавляя обычно требуемое поведение для стандартных и подробных представлений.

Each of the concrete generic views provided is built by combining `GenericAPIView`, with one or more mixin classes.

Каждый из предоставленных бетонных общих видов построен путем объединения `genericapiview` с одним или несколькими классами микшина.

### Attributes

### Атрибуты

**Basic settings**:

**Базовые настройки**:

The following attributes control the basic view behavior.

Следующие атрибуты контролируют поведение основного представления.

* `queryset` - The queryset that should be used for returning objects from this view. Typically, you must either set this attribute, or override the `get_queryset()` method. If you are overriding a view method, it is important that you call `get_queryset()` instead of accessing this property directly, as `queryset` will get evaluated once, and those results will be cached for all subsequent requests.
* `serializer_class` - The serializer class that should be used for validating and deserializing input, and for serializing output. Typically, you must either set this attribute, or override the `get_serializer_class()` method.
* `lookup_field` - The model field that should be used for performing object lookup of individual model instances. Defaults to `'pk'`. Note that when using hyperlinked APIs you'll need to ensure that *both* the API views *and* the serializer classes set the lookup fields if you need to use a custom value.
* `lookup_url_kwarg` - The URL keyword argument that should be used for object lookup. The URL conf should include a keyword argument corresponding to this value. If unset this defaults to using the same value as `lookup_field`.

* `Queryset` - Queryset, который следует использовать для возврата объектов из этой точки зрения.
Как правило, вы должны либо установить этот атрибут, либо переопределить метод `get_queryset ()`.
Если вы переопределяете метод представления, важно, чтобы вы называли `get_queryset ()` вместо того, чтобы обращаться к этому свойству напрямую, так как `Queryset` будет оцениваться один раз, и эти результаты будут кэшированы для всех последующих запросов.
* `serializer_class` - класс Serializer, который следует использовать для проверки и десеризации ввода, и для сериализации вывода.
Как правило, вы должны либо установить этот атрибут, либо переопределить метод `get_serializer_class ()`.
* `lookup_field` - поле модели, которое следует использовать для выполнения поиска объектов отдельных экземпляров модели.
По умолчанию «pk».
Обратите внимание, что при использовании API -интерфейсов гиперссылки вам понадобится, чтобы * оба * представления API * и * классы сериализатора устанавливают поля поиска, если вам нужно использовать пользовательское значение.
* `lookup_url_kwarg` - аргумент ключевого слова URL, который следует использовать для поиска объектов.
URL CONF должен включать аргумент ключевого слова, соответствующий этому значению.
Если по умолчанию не познакомитесь с использованием того же значения, что и `lookup_field`.

**Pagination**:

** страдание **:

The following attributes are used to control pagination when used with list views.

Следующие атрибуты используются для управления страницей при использовании с видами списков.

* `pagination_class` - The pagination class that should be used when paginating list results. Defaults to the same value as the `DEFAULT_PAGINATION_CLASS` setting, which is `'rest_framework.pagination.PageNumberPagination'`. Setting `pagination_class=None` will disable pagination on this view.

* `pagination_class` - класс страниц, который следует использовать при получении листа.
По умолчанию к тому же значению, что и настройка `default_pagination_class`, которая является` 'rest_framework.pagination.pageNumberPagination'.
Установка `pagination_class = none` будет отключить страницу на этой точке.

**Filtering**:

** Фильтрация **:

* `filter_backends` - A list of filter backend classes that should be used for filtering the queryset. Defaults to the same value as the `DEFAULT_FILTER_BACKENDS` setting.

* `filter_backends` - список классов бэкэнд фильтров, которые следует использовать для фильтрации запроса.
По умолчанию к тому же значению, что и настройка `default_filter_backends`.

### Methods

### Методы

**Base methods**:

** Базовые методы **:

#### `get_queryset(self)`

#### `get_queryset (self)`

Returns the queryset that should be used for list views, and that should be used as the base for lookups in detail views. Defaults to returning the queryset specified by the `queryset` attribute.

Возвращает запрос, который следует использовать для представлений списков, и который следует использовать в качестве основы для поиска в подробном представлении.
По умолчанию возвращать запрос, указанный атрибутом `Queryset '.

This method should always be used rather than accessing `self.queryset` directly, as `self.queryset` gets evaluated only once, and those results are cached for all subsequent requests.

Этот метод всегда должен использоваться, а не доступ к `self.queryset` напрямую, так как` self.queryset 'оценивается только один раз, и эти результаты кэшируются для всех последующих запросов.

May be overridden to provide dynamic behavior, such as returning a queryset, that is specific to the user making the request.

Может быть переопределен, чтобы обеспечить динамическое поведение, такое как возврат запроса, который является характерным для пользователя, делающего запрос.

For example:

Например:

```
def get_queryset(self):
    user = self.request.user
    return user.accounts.all()
```

---

**Note:** If the `serializer_class` used in the generic view spans orm relations, leading to an n+1 problem, you could optimize your queryset in this method using `select_related` and `prefetch_related`. To get more information about n+1 problem and use cases of the mentioned methods refer to related section in [django documentation](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

** ПРИМЕЧАНИЕ.
Чтобы получить дополнительную информацию о проблеме n+1 и вариантах использования упомянутых методов, см. Связанный раздел в [Django Documentation] (https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db
.models.query.queryset.select_related).

---

#### `get_object(self)`

#### `get_object (self)`

Returns an object instance that should be used for detail views. Defaults to using the `lookup_field` parameter to filter the base queryset.

Возвращает экземпляр объекта, который следует использовать для подробных представлений.
По умолчанию использование параметра `lookup_field` для фильтрации базового запроса.

May be overridden to provide more complex behavior, such as object lookups based on more than one URL kwarg.

Может быть переопределен, чтобы обеспечить более сложное поведение, такое как поиск объектов на основе более чем одного URL Kwarg.

For example:

Например:

```
def get_object(self):
    queryset = self.get_queryset()
    filter = {}
    for field in self.multiple_lookup_fields:
        filter[field] = self.kwargs[field]

    obj = get_object_or_404(queryset, **filter)
    self.check_object_permissions(self.request, obj)
    return obj
```

Note that if your API doesn't include any object level permissions, you may optionally exclude the `self.check_object_permissions`, and simply return the object from the `get_object_or_404` lookup.

Обратите внимание, что если ваш API не включает никаких разрешений на уровень объекта, вы можете при желании исключить `self.check_object_permissions` и просто вернуть объект из поиска` get_object_or_404`.

#### `filter_queryset(self, queryset)`

#### `filter_queryset (self, queryset)`

Given a queryset, filter it with whichever filter backends are in use, returning a new queryset.

Учитывая запрос, отфильтруйте его с любыми бэкэнами фильтра, возвращая новый запрос.

For example:

Например:

```
def filter_queryset(self, queryset):
    filter_backends = [CategoryFilter]

    if 'geo_route' in self.request.query_params:
        filter_backends = [GeoRouteFilter, CategoryFilter]
    elif 'geo_point' in self.request.query_params:
        filter_backends = [GeoPointFilter, CategoryFilter]

    for backend in list(filter_backends):
        queryset = backend().filter_queryset(self.request, queryset, view=self)

    return queryset
```

#### `get_serializer_class(self)`

#### `get_serializer_class (self)`

Returns the class that should be used for the serializer. Defaults to returning the `serializer_class` attribute.

Возвращает класс, который следует использовать для сериализатора.
По умолчанию возвращать атрибут `serializer_class`.

May be overridden to provide dynamic behavior, such as using different serializers for read and write operations, or providing different serializers to different types of users.

Может быть переопределен, чтобы обеспечить динамическое поведение, такое как использование различных сериалов для операций чтения и записи или предоставление различных сериализаторов для различных типов пользователей.

For example:

Например:

```
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer
```

**Save and deletion hooks**:

** Сохранить и удалять крючки **:

The following methods are provided by the mixin classes, and provide easy overriding of the object save or deletion behavior.

Следующие методы предоставляются классами Mixin и обеспечивают легкое переоценку поведения сохранения объекта или удаления.

* `perform_create(self, serializer)` - Called by `CreateModelMixin` when saving a new object instance.
* `perform_update(self, serializer)` - Called by `UpdateModelMixin` when saving an existing object instance.
* `perform_destroy(self, instance)` - Called by `DestroyModelMixin` when deleting an object instance.

* `exective_create (self, serializer)` - называется `createmodelmixin` при сохранении нового экземпляра объекта.
* `refect_update (self, serializer)` - называется `updatemodelmixin` при сохранении существующего экземпляра объекта.
* `exective_destroy (self, exant)` - называется `destressmodelmixin` при удалении экземпляра объекта.

These hooks are particularly useful for setting attributes that are implicit in the request, but are not part of the request data. For instance, you might set an attribute on the object based on the request user, or based on a URL keyword argument.

Эти крючки особенно полезны для настройки атрибутов, которые подразумеваются в запросе, но не являются частью данных запроса.
Например, вы можете установить атрибут на объекте на основе пользователя запроса или на основе аргумента ключевого слова URL.

```
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
```

These override points are also particularly useful for adding behavior that occurs before or after saving an object, such as emailing a confirmation, or logging the update.

Эти точки переопределения также особенно полезны для добавления поведения, которое происходит до или после сохранения объекта, например, по электронной почте подтверждения или регистрация обновления.

```
def perform_update(self, serializer):
    instance = serializer.save()
    send_email_confirmation(user=self.request.user, modified=instance)
```

You can also use these hooks to provide additional validation, by raising a `ValidationError()`. This can be useful if you need some validation logic to apply at the point of database save. For example:

Вы также можете использовать эти крючки для обеспечения дополнительной проверки, подняв `valyationError ()`.
Это может быть полезно, если вам нужна какая -то логика проверки для применения в точке сохранения базы данных.
Например:

```
def perform_create(self, serializer):
    queryset = SignupRequest.objects.filter(user=self.request.user)
    if queryset.exists():
        raise ValidationError('You have already signed up')
    serializer.save(user=self.request.user)
```

**Other methods**:

** Другие методы **:

You won't typically need to override the following methods, although you might need to call into them if you're writing custom views using `GenericAPIView`.

Обычно вам не нужно переопределять следующие методы, хотя вам может потребоваться вызвать их, если вы пишете пользовательские представления, используя `genericapiview '.

* `get_serializer_context(self)` - Returns a dictionary containing any extra context that should be supplied to the serializer. Defaults to including `'request'`, `'view'` and `'format'` keys.
* `get_serializer(self, instance=None, data=None, many=False, partial=False)` - Returns a serializer instance.
* `get_paginated_response(self, data)` - Returns a paginated style `Response` object.
* `paginate_queryset(self, queryset)` - Paginate a queryset if required, either returning a page object, or `None` if pagination is not configured for this view.
* `filter_queryset(self, queryset)` - Given a queryset, filter it with whichever filter backends are in use, returning a new queryset.

* `get_serializer_context (self)` - возвращает словарь, содержащий любой дополнительный контекст, который должен быть предоставлен сериализатору.
По умолчанию включить `'request' ',`' view '' 'и `' format '' клавиши.
* `get_serializer (self, encement = none, data = none, много = false, partial = false)` - возвращает экземпляр сериализатора.
* `get_pagination_response (self, data)` - Возвращает объект ответа `` `` `` `` `` объект.
* `paginate_queryset (self, queryset)` - Paginate queryset, если это необходимо, либо возвращение объекта страницы, либо `none`, если для этого представления не настроено.
* `filter_queryset (self, queryset)` - Учитывая запрос, отфильтровал его с помощью каких -либо бэкэндов фильтра, возвращая новый запрос.

---

# Mixins

# Микшины

The mixin classes provide the actions that are used to provide the basic view behavior. Note that the mixin classes provide action methods rather than defining the handler methods, such as `.get()` and `.post()`, directly. This allows for more flexible composition of behavior.

Классы Mixin обеспечивают действия, которые используются для обеспечения основного поведения.
Обратите внимание, что классы микшина предоставляют методы действия, а не определяют методы обработчика, такие как `.get ()` и `.post ()`, напрямую.
Это обеспечивает более гибкий состав поведения.

The mixin classes can be imported from `rest_framework.mixins`.

Классы Mixin могут быть импортированы из `rest_framework.mixins`.

## ListModelMixin

## listmodelmixin

Provides a `.list(request, *args, **kwargs)` method, that implements listing a queryset.

Предоставляет метод `.List (запрос, *args, ** kwargs), который реализует перечисление запроса.

If the queryset is populated, this returns a `200 OK` response, with a serialized representation of the queryset as the body of the response. The response data may optionally be paginated.

Если запрос на заполнен, это возвращает ответ «200 OK» с сериализованным представлением запроса в качестве тела ответа.
Данные ответа могут быть опционально быть страстными.

## CreateModelMixin

## createmodelmixin

Provides a `.create(request, *args, **kwargs)` method, that implements creating and saving a new model instance.

Предоставляет метод. Create (запрос, *args, ** kwargs), который реализует создание и сохранение нового экземпляра модели.

If an object is created this returns a `201 Created` response, with a serialized representation of the object as the body of the response. If the representation contains a key named `url`, then the `Location` header of the response will be populated with that value.

Если создается объект, это возвращает ответ «201», созданный, с сериализованным представлением объекта как тела ответа.
Если представление содержит ключ с именем «url», то заголовок «местоположение» ответа будет заполнен этим значением.

If the request data provided for creating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.

Если данные запроса, предоставленные для создания объекта, были недействительными, будет возвращен ответ `400 Bad Request`, а подробности ошибки в качестве тела ответа.

## RetrieveModelMixin

## retivemodelmixin

Provides a `.retrieve(request, *args, **kwargs)` method, that implements returning an existing model instance in a response.

Предоставляет метод `.retrieve (запрос, *args, ** kwargs), который реализует возвращение существующего экземпляра модели в ответе.

If an object can be retrieved this returns a `200 OK` response, with a serialized representation of the object as the body of the response. Otherwise, it will return a `404 Not Found`.

Если объект может быть извлечен, это возвращает ответ `200 OK`, с сериализованным представлением объекта как тела ответа.
В противном случае он вернет `404 не найдено.

## UpdateModelMixin

## Updatemodelmixin

Provides a `.update(request, *args, **kwargs)` method, that implements updating and saving an existing model instance.

Предоставляет метод.

Also provides a `.partial_update(request, *args, **kwargs)` method, which is similar to the `update` method, except that all fields for the update will be optional. This allows support for HTTP `PATCH` requests.

Также предоставляет метод `.partial_update (запрос, *args, ** kwargs), который аналогичен методу` update`, за исключением того, что все поля для обновления будут необязательными.
Это позволяет поддержать запросы http `patch '.

If an object is updated this returns a `200 OK` response, with a serialized representation of the object as the body of the response.

Если объект обновляется, это возвращает ответ `200 OK` с сериализованным представлением объекта как тела ответа.

If the request data provided for updating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.

Если данные запроса, предоставленные для обновления объекта, были недействительными, будет возвращен ответ `400 Bad Request`, а подробности ошибки в качестве тела ответа.

## DestroyModelMixin

## Dissultmodelmixin

Provides a `.destroy(request, *args, **kwargs)` method, that implements deletion of an existing model instance.

Предоставляет метод.

If an object is deleted this returns a `204 No Content` response, otherwise it will return a `404 Not Found`.

Если объект удален, это возвращает ответ `204 Нет контента ', в противном случае он вернет` 404 не найдено'.

---

# Concrete View Classes

# Contrent View Clesess

The following classes are the concrete generic views. If you're using generic views this is normally the level you'll be working at unless you need heavily customized behavior.

Следующие классы являются бетонными общими видами.
Если вы используете общие виды, это обычно, на котором вы будете работать, если вам не нужно индивидуальное поведение.

The view classes can be imported from `rest_framework.generics`.

Классы просмотра могут быть импортированы из `rest_framework.generics`.

## CreateAPIView

## createApiview

Used for **create-only** endpoints.

Используется для ** только для создания ** конечных точек.

Provides a `post` method handler.

Предоставляет обработчик метода «post».

Extends: [GenericAPIView](#genericapiview), [CreateModelMixin](#createmodelmixin)

Extends: [genericapiview] (#genericapiview), [createmodelmixin] (#createmodelmixin)

## ListAPIView

## listapiview

Used for **read-only** endpoints to represent a **collection of model instances**.

Используется для ** только для чтения ** конечных точек для представления ** коллекции модельных экземпляров **.

Provides a `get` method handler.

Предоставляет обработчик метода `get '.

Extends: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin)

Extends: [genericapiview] (#genericapiview), [listmodelmixin] (#listmodelmixin)

## RetrieveAPIView

## retiveiePiview

Used for **read-only** endpoints to represent a **single model instance**.

Используется для ** только для чтения ** конечных точек для представления ** экземпляра единой модели **.

Provides a `get` method handler.

Предоставляет обработчик метода `get '.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin)

Extends: [genericapiview] (#genericapiview), [retivemodelmixin] (#retivemodelmixin)

## DestroyAPIView

## dissomeapiview

Used for **delete-only** endpoints for a **single model instance**.

Используется для ** только удаления ** конечных точек для ** экземпляра с одной моделью **.

Provides a `delete` method handler.

Предоставляет обработчик метода удаления.

Extends: [GenericAPIView](#genericapiview), [DestroyModelMixin](#destroymodelmixin)

Extends: [genericapiview] (#genericapiview), [destressmodelmixin] (#destressmodelmixin)

## UpdateAPIView

## UpdateApiview

Used for **update-only** endpoints for a **single model instance**.

Используется для ** только обновления ** конечные точки для ** экземпляра с одной моделью **.

Provides `put` and `patch` method handlers.

Обеспечивает обработчики метода Pat 'и `patch`.

Extends: [GenericAPIView](#genericapiview), [UpdateModelMixin](#updatemodelmixin)

Extends: [genericapiview] (#genericapiview), [updatemodelmixin] (#updateModelmixin)

## ListCreateAPIView

## listcreateapiview

Used for **read-write** endpoints to represent a **collection of model instances**.

Используется для ** readwrite ** конечные точки, чтобы представлять ** коллекцию модельных экземпляров **.

Provides `get` and `post` method handlers.

Предоставляет обработчики метода ‘get` и` post`.

Extends: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin), [CreateModelMixin](#createmodelmixin)

Extends: [genericapiview] (#genericapiview), [listmodelmixin] (#listmodelmixin), [createmodelmixin] (#createmodelmixin)

## RetrieveUpdateAPIView

## retiveupdateapiview

Used for **read or update** endpoints to represent a **single model instance**.

Используется для ** Читать или обновление ** конечные точки для представления ** экземпляра единой модели **.

Provides `get`, `put` and `patch` method handlers.

Обеспечивает обработчики метода `get ',` put' и `patch '.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin)

Extends: [genericapiview] (#genericapiview), [retievemodelmixin] (#retivemodelmixin), [updatemodelmixin] (#updatemodelmixin)

## RetrieveDestroyAPIView

## retrendestroyapiview

Used for **read or delete** endpoints to represent a **single model instance**.

Используется для ** Читать или удалить ** конечные точки, чтобы представить ** экземпляр одиночной модели **.

Provides `get` and `delete` method handlers.

Предоставляет обработчики метода `get 'и` delete'.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [DestroyModelMixin](#destroymodelmixin)

Extends: [genericapiview] (#genericapiview), [retievemodelmixin] (#retievemodelmixin), [destressmodelmixin] (#destropmodelmixin)

## RetrieveUpdateDestroyAPIView

## retiveupdatedErsoyapiview

Used for **read-write-delete** endpoints to represent a **single model instance**.

Используется для ** read-write-delete ** конечные точки для представления ** экземпляра с одной моделью **.

Provides `get`, `put`, `patch` and `delete` method handlers.

Предоставляет `get`,` put`, `patch` и` delete 'обработчики метода.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin), [DestroyModelMixin](#destroymodelmixin)

Extends: [genericapiview] (#genericapiview), [retievemodelmixin] (#retievemodelmixin), [updatemodelmixin] (#updatemodelmixin), [destropmodelmixin] (#destroymodelmixin)

---

# Customizing the generic views

# Настройка общих видов

Often you'll want to use the existing generic views, but use some slightly customized behavior. If you find yourself reusing some bit of customized behavior in multiple places, you might want to refactor the behavior into a common class that you can then just apply to any view or viewset as needed.

Часто вы захотите использовать существующие общие представления, но использовать немного настроенного поведения.
Если вы обнаружите, что повторно используете какое -то индивидуальное поведение в нескольких местах, вы можете переоборудовать поведение в общий класс, который вы можете просто применить к любому представлению или сбору просмотра по мере необходимости.

## Creating custom mixins

## Создание пользовательских микшинов

For example, if you need to lookup objects based on multiple fields in the URL conf, you could create a mixin class like the following:

Например, если вам нужно искать объекты на основе нескольких полей в URL Conf, вы можете создать класс Mixin, как следующее:

```
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
```

You can then simply apply this mixin to a view or viewset anytime you need to apply the custom behavior.

Затем вы можете просто применить этот микшин к представлению или сбору просмотра в любое время, чтобы применить пользовательское поведение.

```
class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['account', 'username']
```

Using custom mixins is a good option if you have custom behavior that needs to be used.

Использование пользовательских микшинов является хорошим вариантом, если у вас есть пользовательское поведение, которое необходимо использовать.

## Creating custom base classes

## Создание пользовательских базовых классов

If you are using a mixin across multiple views, you can take this a step further and create your own set of base views that can then be used throughout your project. For example:

Если вы используете микшин для нескольких просмотров, вы можете сделать этот шаг дальше и создать свой собственный набор базовых представлений, которые затем можно использовать на протяжении всего проекта.
Например:

```
class BaseRetrieveView(MultipleFieldLookupMixin,
                       generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin,
                                    generics.RetrieveUpdateDestroyAPIView):
    pass
```

Using custom base classes is a good option if you have custom behavior that consistently needs to be repeated across a large number of views throughout your project.

Использование пользовательских базовых классов является хорошим вариантом, если у вас есть пользовательское поведение, которое неизменно нужно повторять во многих видах на протяжении всего вашего проекта.

---

# PUT as create

# Поставьте в качестве создания

Prior to version 3.0 the REST framework mixins treated `PUT` as either an update or a create operation, depending on if the object already existed or not.

До версии 3.0 микшины REST Framework рассматривали `put` как обновление или операцию создания, в зависимости от того, существовал ли объект или нет.

Allowing `PUT` as create operations is problematic, as it necessarily exposes information about the existence or non-existence of objects. It's also not obvious that transparently allowing re-creating of previously deleted instances is necessarily a better default behavior than simply returning `404` responses.

Разрешение «put» в качестве операций является проблематичным, поскольку он обязательно раскрывает информацию о существовании или небывании объектов.
Также не очевидно, что прозрачная разрешение воссоздания ранее удаленных экземпляров обязательно является лучшим поведением по умолчанию, чем просто возвращение ответов «404».

Both styles "`PUT` as 404" and "`PUT` as create" can be valid in different circumstances, but from version 3.0 onwards we now use 404 behavior as the default, due to it being simpler and more obvious.

Оба стиля «Put» как 404 »и« put »как создание» могут быть действительными в разных обстоятельствах, но с версии 3.0 мы теперь используем поведение 404 в качестве дефолта, поскольку он является более простым и более очевидным.

If you need to generic PUT-as-create behavior you may want to include something like [this `AllowPUTAsCreateMixin` class](https://gist.github.com/tomchristie/a2ace4577eff2c603b1b) as a mixin to your views.

Если вам нужно общее поведение, как поведение, вы можете включить что-то вроде [this `allyputAscreatemixin` class] (https://gist.github.com/tomchristie/a2ace4577aff2c603b1b) в виде микшина с вашими взглядами.

---

# Third party packages

# Сторонние пакеты

The following third party packages provide additional generic view implementations.

Следующие сторонние пакеты предоставляют дополнительные общие реализации просмотра.

## Django Rest Multiple Models

## django rete несколько моделей

[Django Rest Multiple Models](https://github.com/MattBroach/DjangoRestMultipleModels) provides a generic view (and mixin) for sending multiple serialized models and/or querysets via a single API request.

[Django Rest несколько моделей] (https://github.com/mattbroach/djangorestmultiplemodels) предоставляет общий вид (и миксин) для отправки нескольких сериализованных моделей и/или запросов через один запрос API.