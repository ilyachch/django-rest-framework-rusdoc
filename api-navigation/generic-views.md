# Общие представления

> Общие представления (generic views) были придуманы для часто повторяющихся действиий... Они используют общие элементы, встречающиеся в представлении, и сокращают их, так, что вы быстро можете написать самые распространенные представления, при этом не повторяясь.
>
> — Документация Django

Одно из ключевых приемуществ представлений-классов заключается в том, что они позволяют использовать повторяющиеся паттерны. REST framework реализует эту идею через встроенные представления. Общие представления REST framework позволяют быстро строить представления API, которые тесно связаны с вашими моделями баз данных.

Если общие представления не подходят целям вашего API, вы всегда можете отказаться от них в пользу обычных классов `APIView` или повторно использовать миксины и базовые классы, используемые в общих представлениях для того, чтобы создать свой набор многократно используемых общих представлений.

## Примеры

Как правило, при использовании общих представлений вы должны переписать ваше представление и установить несколько атрибутов класса:

```python

from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
```

Для более сложных классов вам также может понадобиться переписать различные методы класса представления. Например:

```python
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
```

Для самых простых случаев вам может понадобиться передать любой атрибут класса с помощью метода `.as_view()`. Например, ваш URLconf может включать следующую строку:

```python

url(r'^/users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')

```

# Привязка к API

## GenericAPIView

Этот класс расширяет класс `APIView`, реализуя часто повторяющееся поведение. Каждое общее представление строится путем комбинации `GenericAPIView` с одним из классов-миксинов.

### Атрибуты

**Базовые настройки:**

Следующие атрибуты управляют основным поведеним представления.

* `queryset` - queryset, который должен использоваться для того, чтобы возвращать объекты представления. Как правило, вы должны либо прописать этот атбрибут, либо переписать метод `get_queryset()`. Если вы переписываете метод представления, важно, чтобы вы обращались к `get_queryset()` вместо того, чтобы напрямую получать доступ к этому свойству, так как  queryset вычисляется лишь единожды, и эти результаты будут кешированы для всех последующих запросов.

* `serializer_class` - класс сериализатора, который должен использоваться для валидации, десериализации ввода и для сериализации вывода. Как правило, вы должны либо прописать этот атрибут, либо переписать метод `get_serializer_class()`.

* `lookup_field` - поле модели, которое используется для поиска объектов отдельных экземпляров модели. По умолчанию стоит `pk`. Обратите внимание, что при использовании API по ссылке, вам нужно удостовериться, что в представленит API и в классах сериализатора прописаны поля подстановки, если вам нужно использовать индивидуальное значение.

* `lookup_url_kwarg` - ключовй аргумент URL, который используется для поиска объекта. URL conf должен включать аргумент-ключ, который относится к этому значению. По умолчнию указаны те же значения, что и в `lookup_field`. 

**Пагинация:**
Следующие атрибуты используются для управлении пагинацией при использовании list views.

* `pagination_class` - класс пагинации, который нужно использовать при постраничном выводе результатов list. По умолчанию принимает те же значения, что и настройка `DEFAULT_PAGINATION_CLASS`, а именно `'rest_framework.pagination.PageNumberPagination'`. Настройка `pagination_class=None` отключает пагианцию в данном представлении.

**Фильтрация**

* `filter_backends` - список классов, используемых для фильтрации queryset. По умолчанию принимает такие же значения, как и настройка `DEFAULT_FILTER_BACKENDS`.

## Методы

**Базовые методы:**

* `get_queryset(self)`

Возвращает queryset, который должен использоваться для  list views, а также в качестве основы для поиска в detail views.

По умолчанию возвращает queryset, указанный в атрибуте queryset.

Этот метод всегда будеь предпочтительнее, чем прямое обращаение к `self.queryset`, так как `self.queryset` вычисляется тольно один раз, и эти результаты кешируются для все последующих запросов.

Может быть переписан для динамического поведения, например для возвращения queryset, связянных с особыми запросами пользователя.

Например:

```python

def get_queryset(self):
    user = self.request.user
    return user.accounts.all()
get_object(self)
```

Возвращает экземпляр объекта, который используется для detail views. По умолчанию для фильтрации базового queryset используется параметр `lookup_field`. Вместо этого может использоваться более сложный сценарий, например поиск объектов по более чем одному URL kwarg.

Например:

```python

def get_object(self):
    queryset = self.get_queryset()
    filter = {}
    for field in self.multiple_lookup_fields:
        filter[field] = self.kwargs[field]

    obj = get_object_or_404(queryset, **filter)
    self.check_object_permissions(self.request, obj)
    return obj
```

Обратите внимание. что если ваш API не включает полномочия на объект, то есть возможность исключить `self.check_object_permissions` и просто вернуть объект из `get_object_or_404`.

* `filter_queryset(self, queryset)`

При наличии queryset фильтрует его в соответствии с фильтрами, которые используются на бэкэнде, и возвращает новый queryset.

Например:

```python

def filter_queryset(self, queryset):
    filter_backends = (CategoryFilter,)

    if 'geo_route' in self.request.query_params:
        filter_backends = (GeoRouteFilter, CategoryFilter)
    elif 'geo_point' in self.request.query_params:
        filter_backends = (GeoPointFilter, CategoryFilter)

    for backend in list(filter_backends):
        queryset = backend().filter_queryset(self.request, queryset, view=self)

    return queryset
```
* `get_serializer_class(self)`

Возвращает класс, который должен использоваться с сериализатором. По умолчанию возвращает атрибут `serializer_class`.

Может быть изменен, чтобы обеспечить динамическое поведение, например использование различных сериализаторов для чтения и записи операций или организации различных сериализаторов для разных типов пользователей.

Например:

```python
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer
```

**Сохранение и удаление:**

Следующие хуки предоставляются классами миксинов и позволяют легко переписывать поведение объекта, связанное с сохранением и удалением.

* `perform_create(self, serializer)` - Вызывает  `CreateModelMixin` при сохранении нового экземпляра объекта.
* `perform_update(self, serializer)` - Вызывает  `UpdateModelMixin` при сохранении существующего экземпляра объекта.
* `perform_destroy(self, instance)` - Вызывает  `DestroyModelMixin` при удалении экземпляра объекта.

Эти хуки особенно полезны для установки атрибутов, которые подразумеваются в запросах, но не являются частью данных запроса. Например, вы можете установить атрибут для объекта на основе request user или основываясь на аргументе-ключевом слове URL. 

```python

def perform_create(self, serializer):
    serializer.save(user=self.request.user)
These override points are also particularly useful for adding behavior that occurs before or after saving an object, such as emailing a confirmation, or logging the update.

def perform_update(self, serializer):
    instance = serializer.save()
    send_email_confirmation(user=self.request.user, modified=instance)
```

Вы также можете использовать эти хуки для дополнительной валидации, обратившись к `ValidationError()`. Это может пригодиться, если вы хотите применить некую логику к валидации на этапе сохранения в базу данных. Например:

```python

def perform_create(self, serializer):
    queryset = SignupRequest.objects.filter(user=self.request.user)
    if queryset.exists():
        raise ValidationError('You have already signed up')
    serializer.save(user=self.request.user)
```

**Примечание:** эти методы заменяют старые методы версии 2.x `pre_save`, `post_save`, `pre_delete` и `post_delete`, которые больше недоступны.

**Другие методы**
Как правило, вам не нужно переписыать следующие методы, хотя вы можете прибегнуть к этому, если пишите совбственные представления, используя `GenericAPIView`.

* `get_serializer_context(self)` - возвращает словарь с любым дополнительным контекстом, который должен быть предоставлен сериализатору. По умолчанию включает ключи'request', 'view' и 'format'.
* `get_serializer(self, instance=None, data=None, many=False, partial=False)` - Возвращает сериализованный экземпляр.
* `get_paginated_response(self, data)` - Постранично выводит объект `Response`.
* `paginate_queryset(self, queryset)` - Постранично выводит queryset, либо возвращает объект страницы, либо `None`, если пагинация не настроена для данного представления.
* `filter_queryset(self, queryset)` - При наличии queryset фильтруего его с помощью фильтров бэкэнда, возвращая новый  queryset.

# Миксины

Классы миксинов предоставляют инструментарий для настройки основного поведения представления. Учитывайте, что миксины дают методы действиий, а не определяют напрямую методы обработки, такие как `get()` и `.post()`. Это позволяет более гибко настроить поведение.

Классы миксинов могут быть импортированы из `rest_framework.mixins`.

## ListModelMixin

Предоставляет метод `.list(request, *args, **kwargs)`, который внедряет листинг и queryset.

Если queryset заполнен, то в ответ получаем сообщение `200 OK` с сериализованным представлением queryset тела ответа. Опционально данные ответа могуть быть пронумерованны.

## CreateModelMixin

Предоставляет метод `.create(request, *args, **kwargs)`, который реализует создание и сохранение новых экземпляров модели.

Если объект создан, то в ответ получаем сообщение `201 Created` с сериализированным представлением объекта тела запроса. Если представление содержит url-ключ, то  Location header ответа будет заполнен этим значением.

Если данные запроса для создания объекта были некорректными, будет возвращаться ответ `400 Bad Request`.

## RetrieveModelMixin\

Предоставляет метод `.retrieve(request, *args, **kwargs)`, который реализует возвращение существующего экземпляра модели в ответе. 

Если объект возможно вернуть,  то в ответ получаем сообщение `200 OK` с сериализованным представлением queryset тела ответа. В провтинов случае получим `404 Not Found`.

## UpdateModelMixin

Предоставляет метод `.update(request, *args, **kwargs`), который реализует дополнение и сохранение существующего экземпляра модели.

Также предоставляет метод `.partial_update(request, *args, **kwargs)`, который похож на метод `update`, за исключением того, что все поля update будут опциональными. Это позволяет поддерживать HTTP запросы `PATCH`. 

Если объект был дополнен, то получаем сообщение `200 OK` с сериализованным представлением queryset тела ответа.

Если данные запроса для создания объекта были некорректными, получим ответ `400 Bad Request`.

## DestroyModelMixin

Предоставляет метод `.destroy(request, *args, **kwargs)` который реализует удаление текующего экземпляра модели.

В случае удаления объекта получим сообщение `204 No Content`, в противном случае получим `404 Not Found`.

# Конкретные представления-классы

Следующие классы являются конкретными представлениями. Если вы используете общие представления, то обычно вы работаете с использованем этих классов,за исключением тех случаев, когда нужна очень тонкая настройка.

Классы представлений можно импортировать из `rest_framework.generics`.

## CreateAPIView

Используется для создающих конечных точек.

Предоставляет: обработчик метода `post`.

Расширяет: GenericAPIView, CreateModelMixin

## ListAPIView

Используется для создания неизменяемых конечных точек для набора экземпляров модели.

Предоставляет: обработчик метода `get`.

Расширяет: GenericAPIView, ListModelMixin

## RetrieveAPIView

Используется для создания неизменяемых конечных точек для экземпляра одной модели.

Предоставляет: обработчик метода `get`.

Расширяет: GenericAPIView, RetrieveModelMixin

## DestroyAPIView

Используется для создания только удаляемых конечных точек для экземпляра одной модели.

Предоставляет: обработчик метода `delete`.

Расширяет: GenericAPIView, DestroyModelMixin

## UpdateAPIView

Используется для создания только дополняемых конечных точек для экземпляра одной модели.

Предоставляет: обработчик методов `put` и `patch`.

Расширяет: GenericAPIView, UpdateModelMixin

## ListCreateAPIView

Используется для конечных точек считывания и записи для набора экземпляров модели.

Предоставляет: обработчик методов `get` и `post`.

Расширяет: GenericAPIView, ListModelMixin, CreateModelMixin

## RetrieveUpdateAPIView

Используется для чтения и дополнения конечных точек для экземпляра одной модели.

Предоставляет: обработчик методов `get`, `put` и `patch`.

Расширяет: GenericAPIView, RetrieveModelMixin, UpdateModelMixin

## RetrieveDestroyAPIView

Используется для чтения или удаления конечных точек для экземпляра одной модели.

Предоставляет: обработчик методов `get` и `delete`.

Расширяет: GenericAPIView, RetrieveModelMixin, DestroyModelMixin

## RetrieveUpdateDestroyAPIView

Используется для чтения-записи-удаления конечных точек для экземпляра одной модели.

Предоставляет: обработчик методов `get`, `put`, `patch` и `delete`.

Расширяет: GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

# Модификация общий представлений

Часто будет возникать ситуация, когда вам захочется использовать общее представление, но с небольшими изменениями. Если вы используете повторно некоторые части модифицированного поведения в множестве мест, то возможно захотите внести эти модификации в общий класс, чтобы потом без лишних действий применять их к любому представлению.

## Создание кастомных миксинов

Например, если вам понадобилось найти объекты во множестве полей в URL conf, вы могли бы создать класс миксин как ниже:

```python

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
```

Затем вы легко сможете применять этот миксин к представлению или viewset, как только вам понадобиться применить модификации.

```python

class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ('account', 'username')
Using custom mixins is a good option if you have custom behavior that needs to be used.
```

## Создание кастомных базовых классов

Если вы используете миксины во множестве представлений, то можете не останавливаться на этом и создать свой набор базовых представлений, которые потом будете использоваться в своих проектах. Например:

```python
class BaseRetrieveView(MultipleFieldLookupMixin,
                       generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin,
                                    generics.RetrieveUpdateDestroyAPIView):
    pass
```

Использование кастомных классов это хорошее решение, если вы хотите настроить паттерн, который будет повторяться во множестве ваших проектов.

# PUT в качестве create

До версии 3.0 REST framework миксины использовали `PUT` только для операций update или create, в зависимости от того существует объект или нет.

Использование `PUT` для создания является проблематичной задачей, так как это обязательно раскроет информацию о существовании или отсутствии объектов. Также не совсем очевидно преимущество прозрачного воссоздания удаленных экземпляров перед обычным возвратом соообщений `404`. ***` It's also not obvious that transparently allowing re-creating of previously deleted instances is necessarily a better default behavior than simply returning 404 responses.`***

Оба подхода "PUT как 404" и "PUT как create" мргут быть валидными в разных ситациях, но начиная с версии 3.0 по умолчанию используется вариант с 404, так как он более прост и очевиден.
Если вы хотите релизовать поведение PUT-as-create, то возможно вы включите класс-миксин наподобие `AllowPUTAsCreateMixin` в ваши представления.

# Сторонние пакеты

Следующие сторонние пакеты реализуют дополнителный функционал общих представлений.

## Django REST Framework bulk

Пакет `django-rest-framework-bulk`задействует миксины общих представлений, а также некоторые распространенные конкретные представления, которые позволяют применять массивные операции через запросы API.

## Django Rest Multiple Models

`Django Rest Multiple Models` предоставлет общее представление (и миксин) для передачи нескольких сериализованных моделей и/или querysets через один API запрос.
