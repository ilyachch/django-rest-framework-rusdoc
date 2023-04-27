<!-- TRANSLATED by md-translate -->
---

source:
    - pagination.py

источник:
- pagination.py

---

# Pagination

# Пагинация

> Django provides a few classes that help you manage paginated data – that is, data that’s split across several pages, with “Previous/Next” links.
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/topics/pagination/)

> Django предоставляет несколько классов, которые помогают вам управлять постраничными данными - то есть данными, разделенными на несколько страниц, со ссылками "Предыдущая/Следующая".
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/topics/pagination/)

REST framework includes support for customizable pagination styles. This allows you to modify how large result sets are split into individual pages of data.

REST-фреймворк включает поддержку настраиваемых стилей пагинации. Это позволяет изменять, как большие наборы результатов разбиваются на отдельные страницы данных.

The pagination API can support either:

API пагинации может поддерживать любую из этих функций:

* Pagination links that are provided as part of the content of the response.
* Pagination links that are included in response headers, such as `Content-Range` or `Link`.

* Ссылки пагинации, которые предоставляются как часть содержимого ответа.
* Ссылки пагинации, включенные в заголовки ответа, такие как `Content-Range` или `Link`.

The built-in styles currently all use links included as part of the content of the response. This style is more accessible when using the browsable API.

В настоящее время все встроенные стили используют ссылки, включенные как часть содержимого ответа. Этот стиль более доступен при использовании API с возможностью просмотра.

Pagination is only performed automatically if you're using the generic views or viewsets. If you're using a regular `APIView`, you'll need to call into the pagination API yourself to ensure you return a paginated response. See the source code for the `mixins.ListModelMixin` and `generics.GenericAPIView` classes for an example.

Пагинация выполняется автоматически, только если вы используете общие представления или наборы представлений. Если вы используете обычное `APIView`, вам нужно будет самостоятельно обратиться к API пагинации, чтобы убедиться, что вы возвращаете ответ с пагинацией. Пример смотрите в исходном коде классов `mixins.ListModelMixin` и `generics.GenericAPIView`.

Pagination can be turned off by setting the pagination class to `None`.

Пагинацию можно отключить, установив для класса пагинации значение `None`.

## Setting the pagination style

## Установка стиля пагинации

The pagination style may be set globally, using the `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` setting keys. For example, to use the built-in limit/offset pagination, you would do something like this:

Стиль пагинации можно задать глобально, используя ключи настройки `DEFAULT_PAGINATION_CLASS` и `PAGE_SIZE`. Например, чтобы использовать встроенную пагинацию с ограничением/смещением, вы должны сделать следующее:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
```

Note that you need to set both the pagination class, and the page size that should be used.  Both `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` are `None` by default.

Обратите внимание, что необходимо задать как класс пагинации, так и размер страницы, которая будет использоваться.  По умолчанию и `DEFAULT_PAGINATION_CLASS`, и `PAGE_SIZE` имеют значение `None`.

You can also set the pagination class on an individual view by using the `pagination_class` attribute. Typically you'll want to use the same pagination style throughout your API, although you might want to vary individual aspects of the pagination, such as default or maximum page size, on a per-view basis.

Вы также можете установить класс пагинации для отдельного представления с помощью атрибута `pagination_class`. Обычно вы хотите использовать один и тот же стиль пагинации во всем API, хотя вы можете захотеть варьировать отдельные аспекты пагинации, такие как размер страницы по умолчанию или максимальный размер страницы, на основе каждого представления.

## Modifying the pagination style

## Изменение стиля пагинации

If you want to modify particular aspects of the pagination style, you'll want to override one of the pagination classes, and set the attributes that you want to change.

Если вы хотите изменить определенные аспекты стиля пагинации, вам нужно переопределить один из классов пагинации и установить атрибуты, которые вы хотите изменить.

```
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

You can then apply your new style to a view using the `pagination_class` attribute:

Затем вы можете применить ваш новый стиль к представлению с помощью атрибута `pagination_class`:

```
class BillingRecordsView(generics.ListAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingRecordsSerializer
    pagination_class = LargeResultsSetPagination
```

Or apply the style globally, using the `DEFAULT_PAGINATION_CLASS` settings key. For example:

Или примените стиль глобально, используя ключ настройки `DEFAULT_PAGINATION_CLASS`. Например:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
}
```

---

# API Reference

# API Reference

## PageNumberPagination

## PageNumberPagination

This pagination style accepts a single number page number in the request query parameters.

Этот стиль пагинации принимает номер страницы с одним номером в параметрах запроса.

**Request**:

**Запрос**:

```
GET https://api.example.org/accounts/?page=4
```

**Response**:

**Ответ**:

```
HTTP 200 OK
{
    "count": 1023,
    "next": "https://api.example.org/accounts/?page=5",
    "previous": "https://api.example.org/accounts/?page=3",
    "results": [
       …
    ]
}
```

#### Setup

#### Настройка

To enable the `PageNumberPagination` style globally, use the following configuration, and set the `PAGE_SIZE` as desired:

Чтобы включить стиль `PageNumberPagination` глобально, используйте следующую конфигурацию и установите `PAGE_SIZE` по желанию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `PageNumberPagination` on a per-view basis.

В подклассах `GenericAPIView` вы также можете установить атрибут `pagination_class` для выбора `PageNumberPagination` на основе каждого вида.

#### Configuration

#### Конфигурация

The `PageNumberPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `PageNumberPagination` включает ряд атрибутов, которые могут быть переопределены для изменения стиля пагинации.

To set these attributes you should override the `PageNumberPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, необходимо переопределить класс `PageNumberPagination`, а затем включить свой собственный класс пагинации, как указано выше.

* `django_paginator_class` - The Django Paginator class to use. Default is `django.core.paginator.Paginator`, which should be fine for most use cases.
* `page_size` - A numeric value indicating the page size. If set, this overrides the `PAGE_SIZE` setting. Defaults to the same value as the `PAGE_SIZE` settings key.
* `page_query_param` - A string value indicating the name of the query parameter to use for the pagination control.
* `page_size_query_param` - If set, this is a string value indicating the name of a query parameter that allows the client to set the page size on a per-request basis. Defaults to `None`, indicating that the client may not control the requested page size.
* `max_page_size` - If set, this is a numeric value indicating the maximum allowable requested page size. This attribute is only valid if `page_size_query_param` is also set.
* `last_page_strings` - A list or tuple of string values indicating values that may be used with the `page_query_param` to request the final page in the set. Defaults to `('last',)`
* `template` - The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/numbers.html"`.

* `django_paginator_class` - Класс Django Paginator, который будет использоваться. По умолчанию это `django.core.paginator.Paginator`, что должно быть хорошо для большинства случаев использования.
* `page_size` - Числовое значение, указывающее размер страницы. Если установлено, оно отменяет настройку `PAGE_SIZE`. По умолчанию имеет то же значение, что и ключ настройки `PAGE_SIZE`.
* `page_query_param` - Строковое значение, указывающее имя параметра запроса, который будет использоваться для управления пагинацией.
* `page_size_query_param` - Если установлено, это строковое значение, указывающее имя параметра запроса, который позволяет клиенту устанавливать размер страницы на основе каждого запроса. По умолчанию `None`, что означает, что клиент не может контролировать размер запрашиваемой страницы.
* `max_page_size` - Если установлено, это числовое значение, указывающее на максимально допустимый размер запрашиваемой страницы. Этот атрибут действителен, только если `page_size_query_param` также установлен.
* `last_page_strings` - Список или кортеж строковых значений, указывающих на значения, которые могут быть использованы с `page_query_param` для запроса последней страницы в наборе. По умолчанию `('last',)`)
* `template` - Имя шаблона для использования при отображении элементов управления пагинацией в просматриваемом API. Может быть переопределено для изменения стиля рендеринга или установлено в `None` для полного отключения HTML элементов управления пагинацией. По умолчанию используется `"rest_framework/pagination/numbers.html"`.

---

## LimitOffsetPagination

## LimitOffsetPagination

This pagination style mirrors the syntax used when looking up multiple database records. The client includes both a "limit" and an
"offset" query parameter. The limit indicates the maximum number of items to return, and is equivalent to the `page_size` in other styles. The offset indicates the starting position of the query in relation to the complete set of unpaginated items.

Этот стиль пагинации повторяет синтаксис, используемый при поиске нескольких записей в базе данных. Клиент включает в себя как "предел", так и
параметр запроса "смещение". Лимит указывает на максимальное количество возвращаемых элементов и эквивалентен `размер страницы` в других стилях. Смещение указывает начальную позицию запроса по отношению к полному набору непагинированных элементов.

**Request**:

**Запрос**:

```
GET https://api.example.org/accounts/?limit=100&offset=400
```

**Response**:

**Ответ**:

```
HTTP 200 OK
{
    "count": 1023,
    "next": "https://api.example.org/accounts/?limit=100&offset=500",
    "previous": "https://api.example.org/accounts/?limit=100&offset=300",
    "results": [
       …
    ]
}
```

#### Setup

#### Настройка

To enable the `LimitOffsetPagination` style globally, use the following configuration:

Чтобы включить стиль `LimitOffsetPagination` глобально, используйте следующую конфигурацию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}
```

Optionally, you may also set a `PAGE_SIZE` key. If the `PAGE_SIZE` parameter is also used then the `limit` query parameter will be optional, and may be omitted by the client.

По желанию вы также можете задать ключ `PAGE_SIZE`. Если параметр `PAGE_SIZE` также используется, то параметр запроса `limit` будет необязательным и может быть опущен клиентом.

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `LimitOffsetPagination` on a per-view basis.

В подклассах `GenericAPIView` вы также можете установить атрибут `pagination_class` для выбора `LimitOffsetPagination` на основе каждого представления.

#### Configuration

#### Конфигурация

The `LimitOffsetPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `LimitOffsetPagination` включает ряд атрибутов, которые могут быть переопределены для изменения стиля пагинации.

To set these attributes you should override the `LimitOffsetPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, вы должны переопределить класс `LimitOffsetPagination`, а затем включить свой собственный класс пагинации, как указано выше.

* `default_limit` - A numeric value indicating the limit to use if one is not provided by the client in a query parameter. Defaults to the same value as the `PAGE_SIZE` settings key.
* `limit_query_param` - A string value indicating the name of the "limit" query parameter. Defaults to `'limit'`.
* `offset_query_param` - A string value indicating the name of the "offset" query parameter. Defaults to `'offset'`.
* `max_limit` - If set this is a numeric value indicating the maximum allowable limit that may be requested by the client. Defaults to `None`.
* `template` - The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/numbers.html"`.

* `default_limit` - Числовое значение, указывающее предел, который следует использовать, если он не указан клиентом в параметре запроса. По умолчанию имеет то же значение, что и ключ настройки `PAGE_SIZE`.
* `limit_query_param` - Строковое значение, указывающее имя параметра запроса "limit". По умолчанию имеет значение `'limit''.
* `offset_query_param` - Строковое значение, указывающее имя параметра запроса "offset". По умолчанию `'offset'`.
* `max_limit` - Если установлено, то это числовое значение, указывающее на максимально допустимый лимит, который может быть запрошен клиентом. По умолчанию `None`.
* `template` - Имя шаблона, который будет использоваться при отображении элементов управления пагинацией в просматриваемом API. Может быть переопределено для изменения стиля рендеринга или установлено в `None` для полного отключения HTML элементов управления пагинацией. По умолчанию используется `"rest_framework/pagination/numbers.html"`.

---

## CursorPagination

## CursorPagination

The cursor-based pagination presents an opaque "cursor" indicator that the client may use to page through the result set. This pagination style only presents forward and reverse controls, and does not allow the client to navigate to arbitrary positions.

Пагинация на основе курсора представляет непрозрачный индикатор "курсор", который клиент может использовать для просмотра набора результатов. Этот стиль пагинации представляет только элементы управления перемоткой вперед и назад и не позволяет клиенту переходить к произвольным позициям.

Cursor based pagination requires that there is a unique, unchanging ordering of items in the result set. This ordering might typically be a creation timestamp on the records, as this presents a consistent ordering to paginate against.

Пагинация на основе курсора требует наличия уникального, неизменного порядка следования элементов в наборе результатов. Обычно таким упорядочиванием может быть временная метка создания записей, так как она представляет собой последовательный порядок для постраничного просмотра.

Cursor based pagination is more complex than other schemes. It also requires that the result set presents a fixed ordering, and does not allow the client to arbitrarily index into the result set. However it does provide the following benefits:

Пагинация на основе курсора является более сложной, чем другие схемы. Она также требует, чтобы набор результатов представлял фиксированный порядок, и не позволяет клиенту произвольно индексировать набор результатов. Однако она обеспечивает следующие преимущества:

* Provides a consistent pagination view. When used properly `CursorPagination` ensures that the client will never see the same item twice when paging through records, even when new items are being inserted by other clients during the pagination process.
* Supports usage with very large datasets. With extremely large datasets pagination using offset-based pagination styles may become inefficient or unusable. Cursor based pagination schemes instead have fixed-time properties, and do not slow down as the dataset size increases.

* Обеспечивает последовательное представление пагинации. При правильном использовании `CursorPagination` гарантирует, что клиент никогда не увидит один и тот же элемент дважды при листании записей, даже если новые элементы вставляются другими клиентами во время процесса пагинации.
* Поддержка использования с очень большими наборами данных. При работе с очень большими наборами данных пагинация с использованием стилей пагинации на основе смещения может стать неэффективной или непригодной для использования. Вместо этого схемы пагинации на основе курсора имеют свойства фиксированного времени и не замедляются при увеличении размера набора данных.

#### Details and limitations

#### Подробности и ограничения

Proper use of cursor based pagination requires a little attention to detail. You'll need to think about what ordering you want the scheme to be applied against. The default is to order by `"-created"`. This assumes that **there must be a 'created' timestamp field** on the model instances, and will present a "timeline" style paginated view, with the most recently added items first.

Правильное использование пагинации на основе курсора требует некоторого внимания к деталям. Вам нужно подумать о том, в каком порядке вы хотите применять схему. По умолчанию используется порядок по `"-created"`. Это предполагает, что **в экземплярах модели должно быть поле временной метки "создано "**, и будет представлено постраничное представление в стиле "временной шкалы", где первыми будут самые последние добавленные элементы.

You can modify the ordering by overriding the `'ordering'` attribute on the pagination class, or by using the `OrderingFilter` filter class together with `CursorPagination`. When used with `OrderingFilter` you should strongly consider restricting the fields that the user may order by.

Вы можете изменить порядок, переопределив атрибут `'ordering'` класса пагинации, или используя класс фильтра `OrderingFilter` вместе с `CursorPagination`. При использовании `OrderingFilter` следует тщательно продумать ограничение полей, по которым пользователь может делать заказ.

Proper usage of cursor pagination should have an ordering field that satisfies the following:

Правильное использование пагинации курсора должно иметь поле упорядочивания, которое удовлетворяет следующим требованиям:

* Should be an unchanging value, such as a timestamp, slug, or other field that is only set once, on creation.
* Should be unique, or nearly unique. Millisecond precision timestamps are a good example. This implementation of cursor pagination uses a smart "position plus offset" style that allows it to properly support not-strictly-unique values as the ordering.
* Should be a non-nullable value that can be coerced to a string.
* Should not be a float. Precision errors easily lead to incorrect results.
Hint: use decimals instead.
(If you already have a float field and must paginate on that, an
[example `CursorPagination` subclass that uses decimals to limit precision is available here](https://gist.github.com/keturn/8bc88525a183fd41c73ffb729b8865be#file-fpcursorpagination-py).)
* The field should have a database index.

* Должно быть неизменным значением, таким как временная метка, slug или другое поле, которое устанавливается только один раз, при создании.
* Должно быть уникальным или почти уникальным. Хорошим примером являются временные метки с точностью до миллисекунды. Эта реализация пагинации курсора использует интеллектуальный стиль "позиция плюс смещение", что позволяет ей правильно поддерживать не строго уникальные значения в качестве упорядочивания.
* Должно быть не нулевым значением, которое можно принудительно преобразовать в строку.
* Не должно быть плавающей точкой. Ошибки точности легко приводят к неправильным результатам.
Подсказка: используйте вместо этого десятичные числа.
(Если у вас уже есть поле с плавающей запятой и вам нужно сделать постраничную запись по нему, можно воспользоваться командой
[пример подкласса `CursorPagination`, который использует десятичные числа для ограничения точности, доступен здесь] (https://gist.github.com/keturn/8bc88525a183fd41c73ffb729b8865be#file-fpcursorpagination-py).)
* Поле должно иметь индекс базы данных.

Using an ordering field that does not satisfy these constraints will generally still work, but you'll be losing some of the benefits of cursor pagination.

Использование поля упорядочивания, которое не удовлетворяет этим ограничениям, как правило, будет работать, но вы потеряете некоторые преимущества пагинации курсора.

For more technical details on the implementation we use for cursor pagination, the ["Building cursors for the Disqus API"](https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api) blog post gives a good overview of the basic approach.

Для получения более подробной технической информации о реализации, которую мы используем для пагинации курсоров, в статье ["Building cursors for the Disqus API"](https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api) блога дается хороший обзор основного подхода.

#### Setup

#### Настройка

To enable the `CursorPagination` style globally, use the following configuration, modifying the `PAGE_SIZE` as desired:

Чтобы включить стиль `CursorPagination` глобально, используйте следующую конфигурацию, изменяя `PAGE_SIZE` по желанию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 100
}
```

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `CursorPagination` on a per-view basis.

В подклассах `GenericAPIView` вы также можете установить атрибут `pagination_class` для выбора `CursorPagination` на основе каждого вида.

#### Configuration

#### Конфигурация

The `CursorPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `CursorPagination` включает ряд атрибутов, которые могут быть переопределены для изменения стиля пагинации.

To set these attributes you should override the `CursorPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, необходимо переопределить класс `CursorPagination`, а затем включить свой собственный класс пагинации, как указано выше.

* `page_size` = A numeric value indicating the page size. If set, this overrides the `PAGE_SIZE` setting. Defaults to the same value as the `PAGE_SIZE` settings key.
* `cursor_query_param` = A string value indicating the name of the "cursor" query parameter. Defaults to `'cursor'`.
* `ordering` = This should be a string, or list of strings, indicating the field against which the cursor based pagination will be applied. For example: `ordering = 'slug'`. Defaults to `-created`. This value may also be overridden by using `OrderingFilter` on the view.
* `template` = The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/previous_and_next.html"`.

* ``размер страницы`` = числовое значение, указывающее размер страницы. Если установлено, оно отменяет настройку `PAGE_SIZE`. По умолчанию имеет то же значение, что и ключ настройки `PAGE_SIZE`.
* `cursor_query_param` = Строковое значение, указывающее имя параметра запроса "cursor". По умолчанию `'cursor''.
* `orderering` = Это должна быть строка или список строк, указывающих на поле, к которому будет применяться пагинация на основе курсора. Например: `ordering = 'slug'`. По умолчанию используется `-created`. Это значение также может быть переопределено с помощью `OrderingFilter` в представлении.
* `template` = Имя шаблона, который будет использоваться при отображении элементов управления пагинацией в API просмотра. Может быть переопределено для изменения стиля рендеринга или установлено в `None` для полного отключения HTML элементов управления пагинацией. По умолчанию используется `"rest_framework/pagination/previous_and_next.html"`.

---

# Custom pagination styles

# Пользовательские стили пагинации

To create a custom pagination serializer class, you should inherit the subclass `pagination.BasePagination`, override the `paginate_queryset(self, queryset, request, view=None)`, and `get_paginated_response(self, data)` methods:

Чтобы создать собственный класс сериализатора пагинации, необходимо унаследовать подкласс `pagination.BasePagination`, переопределить методы `paginate_queryset(self, queryset, request, view=None)` и `get_paginated_response(self, data)`:

* The `paginate_queryset` method is passed to the initial queryset and should return an iterable object. That object contains only the data in the requested page.
* The `get_paginated_response` method is passed to the serialized page data and should return a `Response` instance.

* Метод `paginate_queryset` передается начальному кверисету и должен возвращать итерируемый объект. Этот объект содержит только данные запрашиваемой страницы.
* Метод `get_paginated_response` передается сериализованным данным страницы и должен возвращать экземпляр `Response`.

Note that the `paginate_queryset` method may set state on the pagination instance, that may later be used by the `get_paginated_response` method.

Обратите внимание, что метод `paginate_queryset` может установить состояние экземпляра пагинации, которое впоследствии может быть использовано методом `get_paginated_response`.

## Example

## Пример

Suppose we want to replace the default pagination output style with a modified format that includes the next and previous links under in a nested 'links' key. We could specify a custom pagination class like so:

Предположим, мы хотим заменить стандартный стиль вывода пагинации на модифицированный формат, который включает следующую и предыдущую ссылки во вложенном ключе 'links'. Мы можем указать пользовательский класс пагинации следующим образом:

```
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
```

We'd then need to set up the custom class in our configuration:

Затем нам нужно будет установить пользовательский класс в нашей конфигурации:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.CustomPagination',
    'PAGE_SIZE': 100
}
```

Note that if you care about how the ordering of keys is displayed in responses in the browsable API you might choose to use an `OrderedDict` when constructing the body of paginated responses, but this is optional.

Обратите внимание, что если вам важно, как порядок ключей отображается в ответах в просматриваемом API, вы можете использовать `OrderedDict` при построении тела постраничных ответов, но это необязательно.

## Using your custom pagination class

## Использование вашего пользовательского класса пагинации

To have your custom pagination class be used by default, use the `DEFAULT_PAGINATION_CLASS` setting:

Чтобы ваш пользовательский класс пагинации использовался по умолчанию, используйте параметр `DEFAULT_PAGINATION_CLASS`:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100
}
```

API responses for list endpoints will now include a `Link` header, instead of including the pagination links as part of the body of the response, for example:

Ответы API для конечных точек списка теперь будут включать заголовок `Link`, вместо того чтобы, например, включать ссылки пагинации как часть тела ответа:

![Link Header](../img/link-header-pagination.png)

![Заголовок ссылки](../img/link-header-pagination.png)

_A custom pagination style, using the 'Link' header_

*Настраиваемый стиль пагинации с использованием заголовка "Ссылка".

---

# HTML pagination controls

# Элементы управления пагинацией HTML

By default using the pagination classes will cause HTML pagination controls to be displayed in the browsable API. There are two built-in display styles. The `PageNumberPagination` and `LimitOffsetPagination` classes display a list of page numbers with previous and next controls. The `CursorPagination` class displays a simpler style that only displays a previous and next control.

По умолчанию использование классов пагинации приводит к отображению элементов управления пагинацией HTML в просматриваемом API. Существует два встроенных стиля отображения. Классы `PageNumberPagination` и `LimitOffsetPagination` отображают список номеров страниц с предыдущим и следующим элементами управления. Класс `CursorPagination` отображает более простой стиль, в котором отображаются только предыдущий и следующий элементы управления.

## Customizing the controls

## Настройка элементов управления

You can override the templates that render the HTML pagination controls. The two built-in styles are:

Вы можете переопределить шаблоны, которые отображают элементы управления пагинацией HTML. Есть два встроенных стиля:

* `rest_framework/pagination/numbers.html`
* `rest_framework/pagination/previous_and_next.html`

* ``rest_framework/pagination/numbers.html``
* ``rest_framework/pagination/previous_and_next.html``

Providing a template with either of these paths in a global template directory will override the default rendering for the relevant pagination classes.

Предоставление шаблона с любым из этих путей в глобальном каталоге шаблонов переопределит рендеринг по умолчанию для соответствующих классов пагинации.

Alternatively you can disable HTML pagination controls completely by subclassing on of the existing classes, setting `template = None` as an attribute on the class. You'll then need to configure your `DEFAULT_PAGINATION_CLASS` settings key to use your custom class as the default pagination style.

В качестве альтернативы вы можете полностью отключить элементы управления HTML-пагинацией, создав подкласс одного из существующих классов и установив `template = None` в качестве атрибута класса. Затем вам нужно будет настроить ключ параметров `DEFAULT_PAGINATION_CLASS`, чтобы использовать ваш пользовательский класс в качестве стиля пагинации по умолчанию.

#### Low-level API

#### Низкоуровневый API

The low-level API for determining if a pagination class should display the controls or not is exposed as a `display_page_controls` attribute on the pagination instance. Custom pagination classes should be set to `True` in the `paginate_queryset` method if they require the HTML pagination controls to be displayed.

Низкоуровневый API для определения того, должен ли класс пагинации отображать элементы управления или нет, раскрывается как атрибут `display_page_controls` на экземпляре пагинации. Пользовательские классы пагинации должны быть установлены в `True` в методе `paginate_queryset`, если они требуют отображения элементов управления пагинацией HTML.

The `.to_html()` and `.get_html_context()` methods may also be overridden in a custom pagination class in order to further customize how the controls are rendered.

Методы `.to_html()` и `.get_html_context()` также могут быть переопределены в пользовательском классе пагинации для дальнейшей настройки отображения элементов управления.

---

# Third party packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF-extensions

## DRF-extensions

The [`DRF-extensions` package](https://chibisov.github.io/drf-extensions/docs/) includes a [`PaginateByMaxMixin` mixin class](https://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin) that allows your API clients to specify `?page_size=max` to obtain the maximum allowed page size.

Пакет [`DRF-extensions`] (https://chibisov.github.io/drf-extensions/docs/) включает класс-миксин [`PaginateByMaxMixin`] (https://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin), который позволяет вашим клиентам API указывать `?page_size=max` для получения максимально допустимого размера страницы.

## drf-proxy-pagination

## drf-proxy-pagination

The [`drf-proxy-pagination` package](https://github.com/tuffnatty/drf-proxy-pagination) includes a `ProxyPagination` class which allows to choose pagination class with a query parameter.

Пакет [`drf-proxy-pagination`](https://github.com/tuffnatty/drf-proxy-pagination) включает класс `ProxyPagination`, который позволяет выбирать класс пагинации с помощью параметра запроса.

## link-header-pagination

## link-header-pagination

The [`django-rest-framework-link-header-pagination` package](https://github.com/tbeadle/django-rest-framework-link-header-pagination) includes a `LinkHeaderPagination` class which provides pagination via an HTTP `Link` header as described in [GitHub REST API documentation](https://docs.github.com/en/rest/guides/traversing-with-pagination).

Пакет [`django-rest-framework-link-header-pagination`](https://github.com/tbeadle/django-rest-framework-link-header-pagination) включает класс `LinkHeaderPagination`, который обеспечивает пагинацию через HTTP-заголовок `Link`, как описано в [документации GitHub REST API](https://docs.github.com/en/rest/guides/traversing-with-pagination).