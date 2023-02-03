<!-- TRANSLATED by md-translate -->
---

source:

источник:

* mixins.py
* generics.py

* mixins.py
* generics.py

---

# Generic views

# Общие представления

> Django’s generic views... were developed as a shortcut for common usage patterns... They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to repeat yourself.
>
> — [Django Documentation](https://docs.djangoproject.com/en/stable/ref/class-based-views/#base-vs-generic-views)

> Общие представления в Django... были разработаны как кратчайший путь к общим шаблонам использования... Они берут определенные общие идиомы и паттерны, встречающиеся в разработке представлений, и абстрагируют их, чтобы вы могли быстро писать общие представления данных без необходимости повторяться.
>
> - [Документация Django](https://docs.djangoproject.com/en/stable/ref/class-based-views/#base-vs-generic-views)

One of the key benefits of class-based views is the way they allow you to compose bits of reusable behavior. REST framework takes advantage of this by providing a number of pre-built views that provide for commonly used patterns.

Одним из ключевых преимуществ представлений, основанных на классах, является то, что они позволяют составлять фрагменты многократно используемого поведения. Фреймворк REST использует это преимущество, предоставляя ряд готовых представлений, которые обеспечивают часто используемые шаблоны.

The generic views provided by REST framework allow you to quickly build API views that map closely to your database models.

Типовые представления, предоставляемые REST-фреймворком, позволяют быстро создавать представления API, которые тесно связаны с моделями вашей базы данных.

If the generic views don't suit the needs of your API, you can drop down to using the regular `APIView` class, or reuse the mixins and base classes used by the generic views to compose your own set of reusable generic views.

Если типовые представления не удовлетворяют потребностям вашего API, вы можете перейти к использованию обычного класса `APIView` или повторно использовать миксины и базовые классы, используемые типовыми представлениями, для создания собственного набора многократно используемых типовых представлений.

## Examples

## Примеры

Typically when using the generic views, you'll override the view, and set several class attributes.

Обычно при использовании общих представлений вы переопределяете представление и устанавливаете несколько атрибутов класса.

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

Для более сложных случаев вы также можете захотеть переопределить различные методы класса представления. Например.

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

Для очень простых случаев вы можете передать любые атрибуты класса с помощью метода `.as_view()`. Например, ваша URLconf может включать что-то вроде следующей записи:

```
path('users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
```

---

# API Reference

# API Reference

## GenericAPIView

## GenericAPIView

This class extends REST framework's `APIView` class, adding commonly required behavior for standard list and detail views.

Этот класс расширяет класс `APIView` фреймворка REST, добавляя часто требуемое поведение для стандартных представлений списка и детализации.

Each of the concrete generic views provided is built by combining `GenericAPIView`, with one or more mixin classes.

Каждое из конкретных типовых представлений создается путем объединения `GenericAPIView` с одним или несколькими классами-миксинами.

### Attributes

### Атрибуты

**Basic settings**:

**Основные настройки**:

The following attributes control the basic view behavior.

Следующие атрибуты управляют основным поведением представления.

* `queryset` - The queryset that should be used for returning objects from this view. Typically, you must either set this attribute, or override the `get_queryset()` method. If you are overriding a view method, it is important that you call `get_queryset()` instead of accessing this property directly, as `queryset` will get evaluated once, and those results will be cached for all subsequent requests.
* `serializer_class` - The serializer class that should be used for validating and deserializing input, and for serializing output. Typically, you must either set this attribute, or override the `get_serializer_class()` method.
* `lookup_field` - The model field that should be used for performing object lookup of individual model instances. Defaults to `'pk'`. Note that when using hyperlinked APIs you'll need to ensure that *both* the API views *and* the serializer classes set the lookup fields if you need to use a custom value.
* `lookup_url_kwarg` - The URL keyword argument that should be used for object lookup. The URL conf should include a keyword argument corresponding to this value. If unset this defaults to using the same value as `lookup_field`.

* `queryset` - Набор queryset, который должен использоваться для возврата объектов из этого представления. Как правило, вы должны либо установить этот атрибут, либо переопределить метод `get_queryset()`. Если вы переопределяете метод представления, важно вызвать `get_queryset()`, а не обращаться к этому свойству напрямую, так как `queryset` будет оценен один раз, и эти результаты будут кэшироваться для всех последующих запросов.
* `serializer_class - Класс сериализатора, который должен использоваться для проверки и десериализации входных данных, а также для сериализации выходных данных. Как правило, вы должны либо установить этот атрибут, либо переопределить метод `get_serializer_class()`.
* `lookup_field` - Поле модели, которое должно использоваться для выполнения поиска объектов в отдельных экземплярах модели. По умолчанию используется значение `'pk''. Обратите внимание, что при использовании API с гиперссылками вам нужно убедиться, что *и* представления API, *и* классы сериализатора устанавливают поля поиска, если вам нужно использовать пользовательское значение.
* `lookup_url_kwarg` - Аргумент ключевого слова URL, который должен использоваться для поиска объекта. URL conf должен включать аргумент ключевого слова, соответствующий этому значению. Если значение не установлено, по умолчанию используется то же значение, что и `lookup_field`.

**Pagination**:

**Пагинация**:

The following attributes are used to control pagination when used with list views.

Следующие атрибуты используются для управления пагинацией при использовании представлений списка.

* `pagination_class` - The pagination class that should be used when paginating list results. Defaults to the same value as the `DEFAULT_PAGINATION_CLASS` setting, which is `'rest_framework.pagination.PageNumberPagination'`. Setting `pagination_class=None` will disable pagination on this view.

* `pagination_class` - Класс пагинации, который должен использоваться при пагинации результатов списка. По умолчанию имеет то же значение, что и параметр `DEFAULT_PAGINATION_CLASS`, который является `'rest_framework.pagination.PageNumberPagination'`. Установка `pagination_class=None` отключит пагинацию в этом представлении.

**Filtering**:

**Фильтрация**:

* `filter_backends` - A list of filter backend classes that should be used for filtering the queryset. Defaults to the same value as the `DEFAULT_FILTER_BACKENDS` setting.

* `filter_backends` - Список классов бэкендов фильтра, которые должны использоваться для фильтрации набора запросов. По умолчанию имеет то же значение, что и параметр `DEFAULT_FILTER_BACKENDS`.

### Methods

### Методы

**Base methods**:

**Базовые методы**:

#### `get_queryset(self)`

#### `get_queryset(self)`.

Returns the queryset that should be used for list views, and that should be used as the base for lookups in detail views. Defaults to returning the queryset specified by the `queryset` attribute.

Возвращает набор запросов, который должен использоваться для представлений списка и который должен использоваться в качестве базы для поиска в детальных представлениях. По умолчанию возвращается кверисет, указанный атрибутом `queryset`.

This method should always be used rather than accessing `self.queryset` directly, as `self.queryset` gets evaluated only once, and those results are cached for all subsequent requests.

Этот метод всегда следует использовать вместо прямого обращения к `self.queryset`, поскольку `self.queryset` оценивается только один раз, и эти результаты кэшируются для всех последующих запросов.

May be overridden to provide dynamic behavior, such as returning a queryset, that is specific to the user making the request.

Может быть переопределена для обеспечения динамического поведения, например, возврата набора запросов, специфичного для пользователя, делающего запрос.

For example:

Например:

```
def get_queryset(self):
    user = self.request.user
    return user.accounts.all()
```

---

**Note:** If the `serializer_class` used in the generic view spans orm relations, leading to an n+1 problem, you could optimize your queryset in this method using `select_related` and `prefetch_related`. To get more information about n+1 problem and use cases of the mentioned methods refer to related section in [django documentation](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

**Примечание:** Если класс `serializer_class`, используемый в общем представлении, охватывает несколько отношений, что приводит к проблеме n+1, вы можете оптимизировать ваш набор запросов в этом методе, используя `select_related` и `prefetch_related`. Для получения дополнительной информации о проблеме n+1 и случаях использования упомянутых методов обратитесь к разделу related в [документации django](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related).

---

#### `get_object(self)`

#### `get_object(self)`.

Returns an object instance that should be used for detail views. Defaults to using the `lookup_field` parameter to filter the base queryset.

Возвращает экземпляр объекта, который должен использоваться для детальных представлений. По умолчанию используется параметр `lookup_field` для фильтрации базового набора запросов.

May be overridden to provide more complex behavior, such as object lookups based on more than one URL kwarg.

Может быть переопределена для обеспечения более сложного поведения, например, поиска объектов на основе более чем одного URL kwarg.

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

Обратите внимание, что если ваш API не включает разрешения на уровне объекта, вы можете исключить `self.check_object_permissions`, и просто вернуть объект из поиска `get_object_or_404`.

#### `filter_queryset(self, queryset)`

#### `filter_queryset(self, queryset)`.

Given a queryset, filter it with whichever filter backends are in use, returning a new queryset.

Получив набор запросов, отфильтруйте его с помощью тех бэкендов фильтрации, которые используются, и верните новый набор запросов.

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

#### `get_serializer_class(self)`.

Returns the class that should be used for the serializer. Defaults to returning the `serializer_class` attribute.

Возвращает класс, который должен быть использован для сериализатора. По умолчанию возвращается атрибут `serializer_class`.

May be overridden to provide dynamic behavior, such as using different serializers for read and write operations, or providing different serializers to different types of users.

Может быть переопределен для обеспечения динамического поведения, например, использования различных сериализаторов для операций чтения и записи, или предоставления различных сериализаторов различным типам пользователей.

For example:

Например:

```
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer
```

**Save and deletion hooks**:

**Крючки для сохранения и удаления**:

The following methods are provided by the mixin classes, and provide easy overriding of the object save or deletion behavior.

Следующие методы предоставляются классами mixin и обеспечивают легкое переопределение поведения сохранения или удаления объекта.

* `perform_create(self, serializer)` - Called by `CreateModelMixin` when saving a new object instance.
* `perform_update(self, serializer)` - Called by `UpdateModelMixin` when saving an existing object instance.
* `perform_destroy(self, instance)` - Called by `DestroyModelMixin` when deleting an object instance.

* `perform_create(self, serializer)` - Вызывается `CreateModelMixin` при сохранении нового экземпляра объекта.
* `perform_update(self, serializer)` - Вызывается `UpdateModelMixin` при сохранении существующего экземпляра объекта.
* `perform_destroy(self, instance)` - Вызывается `DestroyModelMixin` при удалении экземпляра объекта.

These hooks are particularly useful for setting attributes that are implicit in the request, but are not part of the request data. For instance, you might set an attribute on the object based on the request user, or based on a URL keyword argument.

Эти крючки особенно полезны для установки атрибутов, которые подразумеваются в запросе, но не являются частью данных запроса. Например, вы можете установить атрибут объекта на основе пользователя запроса или на основе аргумента ключевого слова URL.

```
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
```

These override points are also particularly useful for adding behavior that occurs before or after saving an object, such as emailing a confirmation, or logging the update.

Эти точки переопределения также особенно полезны для добавления поведения, которое происходит до или после сохранения объекта, например, отправки подтверждения по электронной почте или регистрации обновления.

```
def perform_update(self, serializer):
    instance = serializer.save()
    send_email_confirmation(user=self.request.user, modified=instance)
```

You can also use these hooks to provide additional validation, by raising a `ValidationError()`. This can be useful if you need some validation logic to apply at the point of database save. For example:

Вы также можете использовать эти крючки для обеспечения дополнительной проверки, вызывая `ValidationError()`. Это может быть полезно, если вам нужно применить логику валидации в момент сохранения базы данных. Например:

```
def perform_create(self, serializer):
    queryset = SignupRequest.objects.filter(user=self.request.user)
    if queryset.exists():
        raise ValidationError('You have already signed up')
    serializer.save(user=self.request.user)
```

**Other methods**:

**Другие методы**:

You won't typically need to override the following methods, although you might need to call into them if you're writing custom views using `GenericAPIView`.

Обычно вам не нужно переопределять следующие методы, хотя вам может понадобиться обращаться к ним, если вы пишете пользовательские представления, используя `GenericAPIView`.

* `get_serializer_context(self)` - Returns a dictionary containing any extra context that should be supplied to the serializer. Defaults to including `'request'`, `'view'` and `'format'` keys.
* `get_serializer(self, instance=None, data=None, many=False, partial=False)` - Returns a serializer instance.
* `get_paginated_response(self, data)` - Returns a paginated style `Response` object.
* `paginate_queryset(self, queryset)` - Paginate a queryset if required, either returning a page object, or `None` if pagination is not configured for this view.
* `filter_queryset(self, queryset)` - Given a queryset, filter it with whichever filter backends are in use, returning a new queryset.

* ``get_serializer_context(self)`` - Возвращает словарь, содержащий любой дополнительный контекст, который должен быть предоставлен сериализатору. По умолчанию включает ключи `'request'`, `'view'` и `'format'`.
* ``get_serializer(self, instance=None, data=None, many=False, partial=False)`` - Возвращает экземпляр сериализатора.
* ``get_paginated_response(self, data)`` - Возвращает объект `Response` в стиле paginated.
* `paginate_queryset(self, queryset)` - Пагинация набора запросов, если требуется, возвращает либо объект страницы, либо `None`, если пагинация не настроена для этого представления.
* `filter_queryset(self, queryset)` - Получив набор запросов, отфильтровать его с помощью используемых бэкендов фильтрации, возвращая новый набор запросов.

---

# Mixins

# Миксины

The mixin classes provide the actions that are used to provide the basic view behavior. Note that the mixin classes provide action methods rather than defining the handler methods, such as `.get()` and `.post()`, directly. This allows for more flexible composition of behavior.

Классы mixin предоставляют действия, которые используются для обеспечения базового поведения представления. Обратите внимание, что классы mixin предоставляют методы действий, а не определяют методы обработчиков, такие как `.get()` и `.post()`, напрямую. Это позволяет более гибко компоновать поведение.

The mixin classes can be imported from `rest_framework.mixins`.

Классы миксинов могут быть импортированы из `rest_framework.mixins`.

## ListModelMixin

## ListModelMixin

Provides a `.list(request, *args, **kwargs)` method, that implements listing a queryset.

Предоставляет метод `.list(request, *args, **kwargs)`, который реализует перечисление набора запросов.

If the queryset is populated, this returns a `200 OK` response, with a serialized representation of the queryset as the body of the response. The response data may optionally be paginated.

Если набор запросов заполнен, возвращается ответ `200 OK` с сериализованным представлением набора запросов в качестве тела ответа. По желанию данные ответа могут быть постраничными.

## CreateModelMixin

## CreateModelMixin

Provides a `.create(request, *args, **kwargs)` method, that implements creating and saving a new model instance.

Предоставляет метод `.create(request, *args, **kwargs)`, который реализует создание и сохранение нового экземпляра модели.

If an object is created this returns a `201 Created` response, with a serialized representation of the object as the body of the response. If the representation contains a key named `url`, then the `Location` header of the response will be populated with that value.

Если объект создан, возвращается ответ `201 Created` с сериализованным представлением объекта в качестве тела ответа. Если представление содержит ключ с именем `url`, то заголовок `Location` ответа будет заполнен этим значением.

If the request data provided for creating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.

Если данные запроса, предоставленные для создания объекта, были недействительными, будет возвращен ответ `400 Bad Request`, а в теле ответа будет содержаться информация об ошибке.

## RetrieveModelMixin

## RetrieveModelMixin

Provides a `.retrieve(request, *args, **kwargs)` method, that implements returning an existing model instance in a response.

Предоставляет метод `.retrieve(request, *args, **kwargs)`, который реализует возврат существующего экземпляра модели в ответ.

If an object can be retrieved this returns a `200 OK` response, with a serialized representation of the object as the body of the response. Otherwise, it will return a `404 Not Found`.

Если объект может быть получен, то возвращается ответ `200 OK` с сериализованным представлением объекта в качестве тела ответа. В противном случае будет возвращен ответ `404 Not Found`.

## UpdateModelMixin

## UpdateModelMixin

Provides a `.update(request, *args, **kwargs)` method, that implements updating and saving an existing model instance.

Предоставляет метод `.update(request, *args, **kwargs)`, который реализует обновление и сохранение существующего экземпляра модели.

Also provides a `.partial_update(request, *args, **kwargs)` method, which is similar to the `update` method, except that all fields for the update will be optional. This allows support for HTTP `PATCH` requests.

Также предоставляет метод `.partial_update(request, *args, **kwargs)`, который похож на метод `update`, за исключением того, что все поля для обновления будут необязательными. Это позволяет поддерживать HTTP-запросы `PATCH`.

If an object is updated this returns a `200 OK` response, with a serialized representation of the object as the body of the response.

Если объект обновлен, возвращается ответ `200 OK` с сериализованным представлением объекта в качестве тела ответа.

If the request data provided for updating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.

Если данные запроса, предоставленные для обновления объекта, были недействительными, будет возвращен ответ `400 Bad Request`, в теле которого будет содержаться информация об ошибке.

## DestroyModelMixin

## DestroyModelMixin

Provides a `.destroy(request, *args, **kwargs)` method, that implements deletion of an existing model instance.

Предоставляет метод `.destroy(request, *args, **kwargs)`, который реализует удаление существующего экземпляра модели.

If an object is deleted this returns a `204 No Content` response, otherwise it will return a `404 Not Found`.

Если объект удален, возвращается ответ `204 No Content`, в противном случае возвращается ответ `404 Not Found`.

---

# Concrete View Classes

# Классы бетонного вида

The following classes are the concrete generic views. If you're using generic views this is normally the level you'll be working at unless you need heavily customized behavior.

Следующие классы являются конкретными общими представлениями. Если вы используете общие представления, то обычно вы работаете именно на этом уровне, если только вам не нужно сильно измененное поведение.

The view classes can be imported from `rest_framework.generics`.

Классы представления могут быть импортированы из `rest_framework.generics`.

## CreateAPIView

## CreateAPIView

Used for **create-only** endpoints.

Используется только для **создания** конечных точек.

Provides a `post` method handler.

Предоставляет обработчик метода `post`.

Extends: [GenericAPIView](#genericapiview), [CreateModelMixin](#createmodelmixin)

Расширяет: [GenericAPIView](#genericapiview), [CreateModelMixin](#createmodelmixin)

## ListAPIView

## ListAPIView

Used for **read-only** endpoints to represent a **collection of model instances**.

Используется для конечных точек **только для чтения** для представления **коллекции экземпляров модели**.

Provides a `get` method handler.

Предоставляет обработчик метода `get`.

Extends: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin)

## RetrieveAPIView

## RetrieveAPIView

Used for **read-only** endpoints to represent a **single model instance**.

Используется для конечных точек **только для чтения** для представления **одного экземпляра модели**.

Provides a `get` method handler.

Предоставляет обработчик метода `get`.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin)

## DestroyAPIView

## DestroyAPIView

Used for **delete-only** endpoints for a **single model instance**.

Используется для **только для удаления** конечных точек для **одного экземпляра модели**.

Provides a `delete` method handler.

Предоставляет обработчик метода `delete`.

Extends: [GenericAPIView](#genericapiview), [DestroyModelMixin](#destroymodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [DestroyModelMixin](#destroymodelmixin)

## UpdateAPIView

## UpdateAPIView

Used for **update-only** endpoints for a **single model instance**.

Используется для **только для обновления** конечных точек для **одного экземпляра модели**.

Provides `put` and `patch` method handlers.

Предоставляет обработчики методов `put` и `patch`.

Extends: [GenericAPIView](#genericapiview), [UpdateModelMixin](#updatemodelmixin)

Расширяет: [GenericAPIView](#genericapiview), [UpdateModelMixin](#updatemodelmixin)

## ListCreateAPIView

## ListCreateAPIView

Used for **read-write** endpoints to represent a **collection of model instances**.

Используется для конечных точек **чтения-записи** для представления **коллекции экземпляров модели**.

Provides `get` and `post` method handlers.

Предоставляет обработчики методов `get` и `post`.

Extends: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin), [CreateModelMixin](#createmodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [ListModelMixin](#listmodelmixin), [CreateModelMixin](#createmodelmixin)

## RetrieveUpdateAPIView

## RetrieveUpdateAPIView

Used for **read or update** endpoints to represent a **single model instance**.

Используется для **чтения или обновления** конечных точек для представления **одного экземпляра модели**.

Provides `get`, `put` and `patch` method handlers.

Предоставляет обработчики методов `get`, `put` и `patch`.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin)

## RetrieveDestroyAPIView

## RetrieveDestroyAPIView

Used for **read or delete** endpoints to represent a **single model instance**.

Используется для конечных точек **чтения или удаления** для представления **одного экземпляра модели**.

Provides `get` and `delete` method handlers.

Предоставляет обработчики методов `get` и `delete`.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [DestroyModelMixin](#destroymodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [DestroyModelMixin](#destroymodelmixin)

## RetrieveUpdateDestroyAPIView

## RetrieveUpdateDestroyAPIView

Used for **read-write-delete** endpoints to represent a **single model instance**.

Используется для конечных точек **чтение-запись-удаление** для представления **одного экземпляра модели**.

Provides `get`, `put`, `patch` and `delete` method handlers.

Предоставляет обработчики методов `get`, `put`, `patch` и `delete`.

Extends: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin), [DestroyModelMixin](#destroymodelmixin)

Расширяется: [GenericAPIView](#genericapiview), [RetrieveModelMixin](#retrievemodelmixin), [UpdateModelMixin](#updatemodelmixin), [DestroyModelMixin](#destroymodelmixin)

---

# Customizing the generic views

# Настройка общих представлений

Often you'll want to use the existing generic views, but use some slightly customized behavior. If you find yourself reusing some bit of customized behavior in multiple places, you might want to refactor the behavior into a common class that you can then just apply to any view or viewset as needed.

Часто вы хотите использовать существующие типовые представления, но использовать несколько измененное поведение. Если вы столкнулись с повторным использованием некоторого настроенного поведения в нескольких местах, вы можете захотеть рефакторизовать это поведение в общий класс, который затем можно просто применить к любому представлению или набору представлений по мере необходимости.

## Creating custom mixins

## Создание пользовательских миксинов

For example, if you need to lookup objects based on multiple fields in the URL conf, you could create a mixin class like the following:

Например, если вам нужно искать объекты на основе нескольких полей в URL conf, вы можете создать класс mixin, подобный следующему:

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

Затем вы можете просто применить этот миксин к представлению или набору представлений в любое время, когда вам нужно применить пользовательское поведение.

```
class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['account', 'username']
```

Using custom mixins is a good option if you have custom behavior that needs to be used.

Использование пользовательских миксинов - хороший вариант, если у вас есть пользовательское поведение, которое необходимо использовать.

## Creating custom base classes

## Создание пользовательских базовых классов

If you are using a mixin across multiple views, you can take this a step further and create your own set of base views that can then be used throughout your project. For example:

Если вы используете миксин в нескольких представлениях, вы можете пойти дальше и создать свой собственный набор базовых представлений, которые затем можно использовать во всем проекте. Например:

```
class BaseRetrieveView(MultipleFieldLookupMixin,
                       generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin,
                                    generics.RetrieveUpdateDestroyAPIView):
    pass
```

Using custom base classes is a good option if you have custom behavior that consistently needs to be repeated across a large number of views throughout your project.

Использование пользовательских базовых классов является хорошим вариантом, если у вас есть пользовательское поведение, которое последовательно должно повторяться в большом количестве представлений в вашем проекте.

---

# PUT as create

# PUT как создать

Prior to version 3.0 the REST framework mixins treated `PUT` as either an update or a create operation, depending on if the object already existed or not.

До версии 3.0 миксины фреймворка REST рассматривали `PUT` как операцию обновления или создания, в зависимости от того, существовал ли уже объект или нет.

Allowing `PUT` as create operations is problematic, as it necessarily exposes information about the existence or non-existence of objects. It's also not obvious that transparently allowing re-creating of previously deleted instances is necessarily a better default behavior than simply returning `404` responses.

Разрешение `PUT` в качестве операций создания является проблематичным, поскольку оно обязательно раскрывает информацию о существовании или несуществовании объектов. Также не очевидно, что прозрачное разрешение повторного создания ранее удаленных экземпляров обязательно является лучшим поведением по умолчанию, чем простое возвращение ответов `404`.

Both styles "`PUT` as 404" and "`PUT` as create" can be valid in different circumstances, but from version 3.0 onwards we now use 404 behavior as the default, due to it being simpler and more obvious.

Оба стиля "`PUT` as 404" и "`PUT` as create" могут быть действительны в различных обстоятельствах, но начиная с версии 3.0 мы теперь используем поведение 404 по умолчанию, поскольку оно проще и очевиднее.

If you need to generic PUT-as-create behavior you may want to include something like [this `AllowPUTAsCreateMixin` class](https://gist.github.com/tomchristie/a2ace4577eff2c603b1b) as a mixin to your views.

Если вам необходимо универсальное поведение PUT-как-создание, вы можете включить что-то вроде [this `AllowPUTAsCreateMixin` class](https://gist.github.com/tomchristie/a2ace4577eff2c603b1b) в качестве миксина в ваши представления.

---

# Third party packages

# Пакеты сторонних производителей

The following third party packages provide additional generic view implementations.

Следующие пакеты сторонних производителей предоставляют дополнительные реализации общих представлений.

## Django Rest Multiple Models

## Django Rest Multiple Models

[Django Rest Multiple Models](https://github.com/MattBroach/DjangoRestMultipleModels) provides a generic view (and mixin) for sending multiple serialized models and/or querysets via a single API request.

[Django Rest Multiple Models](https://github.com/MattBroach/DjangoRestMultipleModels) предоставляет общее представление (и миксин) для отправки нескольких сериализованных моделей и/или наборов запросов через один запрос API.