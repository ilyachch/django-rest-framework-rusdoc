<!-- TRANSLATED by md-translate -->
---

source:

источник:

* pagination.py

* Pagination.py

---

# Pagination

# Парень

> Django provides a few classes that help you manage paginated data – that is, data that’s split across several pages, with “Previous/Next” links.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/topics/pagination/)

> Django предоставляет несколько классов, которые помогают вам управлять страничными данными, то есть данных, которые разделены на несколько страниц, по ссылкам «предыдущее/следующее».
>
> - [документация Django] (https://docs.djangoproject.com/en/stable/topics/pagination/)

REST framework includes support for customizable pagination styles. This allows you to modify how large result sets are split into individual pages of data.

Структура REST включает в себя поддержку настраиваемых стилей страниц.
Это позволяет изменить, насколько большие наборы результатов разделены на отдельные страницы данных.

The pagination API can support either:

Pagination API может поддержать либо:

* Pagination links that are provided as part of the content of the response.
* Pagination links that are included in response headers, such as `Content-Range` or `Link`.

* Ссылки на странице, которые предоставляются как часть содержания ответа.
* Ссылки на странице, которые включены в заголовки ответов, такие как «контент-range» или `link`.

The built-in styles currently all use links included as part of the content of the response. This style is more accessible when using the browsable API.

Встроенные стили в настоящее время используют ссылки, включенные как часть содержания ответа.
Этот стиль более доступен при использовании API -файла.

Pagination is only performed automatically if you're using the generic views or viewsets. If you're using a regular `APIView`, you'll need to call into the pagination API yourself to ensure you return a paginated response. See the source code for the `mixins.ListModelMixin` and `generics.GenericAPIView` classes for an example.

Парень выполняется автоматически только в том случае, если вы используете общие виды или виды.
Если вы используете обычный `apiview`, вам нужно будет позвонить в API страниц самостоятельно, чтобы убедиться, что вы возвращаете лицензионный ответ.
См. Исходный код для классов `mixins.listmodelmixin` и` generics.genericapiview` для примера.

Pagination can be turned off by setting the pagination class to `None`.

Парень может быть отключен, установив класс страниц на «нет».

## Setting the pagination style

## Установка стиля страниц

The pagination style may be set globally, using the `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` setting keys. For example, to use the built-in limit/offset pagination, you would do something like this:

Стиль странификации может быть установлен во всем мире, используя клавиши `default_pagination_class` и` page_size` настройки.
Например, для использования встроенного предела/смещения страниц, вы сделаете что-то вроде этого:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
```

Note that you need to set both the pagination class, and the page size that should be used. Both `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` are `None` by default.

Обратите внимание, что вам нужно установить как класс страниц, так и размер страницы, который следует использовать.
Оба `default_pagination_class` и` page_size` - это `none` по умолчанию.

You can also set the pagination class on an individual view by using the `pagination_class` attribute. Typically you'll want to use the same pagination style throughout your API, although you might want to vary individual aspects of the pagination, such as default or maximum page size, on a per-view basis.

Вы также можете установить класс страниц в отдельном представлении, используя атрибут `pagination_class`.
Как правило, вы захотите использовать один и тот же стиль страниц на протяжении всего вашего API, хотя вы можете различить отдельные аспекты страниц, такие как по умолчанию или максимальный размер страницы, на основе просмотра.

## Modifying the pagination style

## Изменение стиля страниц

If you want to modify particular aspects of the pagination style, you'll want to override one of the pagination classes, and set the attributes that you want to change.

Если вы хотите изменить определенные аспекты стиля страниц, вы захотите переопределить один из классов страниц и установить атрибуты, которые вы хотите изменить.

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

Затем вы можете применить свой новый стиль к представлению, используя атрибут `pagination_class`:

```
class BillingRecordsView(generics.ListAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingRecordsSerializer
    pagination_class = LargeResultsSetPagination
```

Or apply the style globally, using the `DEFAULT_PAGINATION_CLASS` settings key. For example:

Или примените стиль глобально, используя клавишу настроек `default_pagination_class`.
Например:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
}
```

---

# API Reference

# Ссылка на API

## PageNumberPagination

## PageNumberPagination

This pagination style accepts a single number page number in the request query parameters.

Этот стиль страниц принимает один номер страницы номеров в параметрах запроса запроса.

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

#### Настраивать

To enable the `PageNumberPagination` style globally, use the following configuration, and set the `PAGE_SIZE` as desired:

Чтобы включить стиль `pagenumberpagination` глобально, используйте следующую конфигурацию и установите` page_size` по желанию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `PageNumberPagination` on a per-view basis.

В подклассах `genericapiview` вы также можете установить атрибут` pagination_class` для выбора `pagenumberpagination` на основе для просмотра.

#### Configuration

#### Конфигурация

The `PageNumberPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `pagenumberpagination 'включает в себя ряд атрибутов, которые могут быть переопределены, чтобы изменить стиль страниц.

To set these attributes you should override the `PageNumberPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, вы должны переопределить класс «PageNumberPagination», а затем включить свой класс пользовательской страниц, как указано выше.

* `django_paginator_class` - The Django Paginator class to use. Default is `django.core.paginator.Paginator`, which should be fine for most use cases.
* `page_size` - A numeric value indicating the page size. If set, this overrides the `PAGE_SIZE` setting. Defaults to the same value as the `PAGE_SIZE` settings key.
* `page_query_param` - A string value indicating the name of the query parameter to use for the pagination control.
* `page_size_query_param` - If set, this is a string value indicating the name of a query parameter that allows the client to set the page size on a per-request basis. Defaults to `None`, indicating that the client may not control the requested page size.
* `max_page_size` - If set, this is a numeric value indicating the maximum allowable requested page size. This attribute is only valid if `page_size_query_param` is also set.
* `last_page_strings` - A list or tuple of string values indicating values that may be used with the `page_query_param` to request the final page in the set. Defaults to `('last',)`
* `template` - The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/numbers.html"`.

* `django_paginator_class` - класс Django Paginator для использования.
По умолчанию `django.core.paginator.paginator`, что должно быть хорошо для большинства вариантов использования.
* `page_size` - числовое значение, указывающее размер страницы.
Если установлено, это переопределяет настройку `page_size`.
По умолчанию к тому же значению, что и клавиша настройки `page_size`.
* `page_query_param` - Значение строки, указывающее имя параметра запроса для использования для элемента управления страницей.
* `page_size_query_param` - Если установлено, это строковое значение, указывающее имя параметра запроса, который позволяет клиенту устанавливать размер страницы на основе для первого запроса.
По умолчанию «нет», указывая, что клиент не может контролировать запрошенную размер страницы.
* `max_page_size` - Если установлено, это числовое значение, указывающее максимально допустимый запрошенный размер страницы.
Этот атрибут действителен только в том случае, если `page_size_query_param` также установлен.
* `last_page_strings` - список или кортеж строковых значений, указывающие значения, которые могут использоваться с` page_query_param`, чтобы запросить окончательную страницу в наборе.
По умолчанию `('last',)`
* `шаблон
Может быть переопределен, чтобы изменить стиль рендеринга или установить на «Нет», чтобы полностью отключить управление HTML Pagination.
По умолчанию `" rest_framework/pagination/number.html "`.

---

## LimitOffsetPagination

## LimitOffSetPagination

This pagination style mirrors the syntax used when looking up multiple database records. The client includes both a "limit" and an "offset" query parameter. The limit indicates the maximum number of items to return, and is equivalent to the `page_size` in other styles. The offset indicates the starting position of the query in relation to the complete set of unpaginated items.

Этот стиль страниц отражает синтаксис, используемый при поиске нескольких записей базы данных.
Клиент включает в себя как «предел», так и параметр запроса «смещения».
Предел указывает максимальное количество элементов для возврата и эквивалентно `page_size` в других стилях.
Смещение указывает на исходную позицию запроса в отношении полного набора неагированных элементов.

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

#### Настраивать

To enable the `LimitOffsetPagination` style globally, use the following configuration:

Чтобы включить стиль `LimitOffSetPagination 'во всем мире, используйте следующую конфигурацию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}
```

Optionally, you may also set a `PAGE_SIZE` key. If the `PAGE_SIZE` parameter is also used then the `limit` query parameter will be optional, and may be omitted by the client.

При желании вы также можете установить клавишу `page_size`.
Если также используется параметр `page_size`, то параметр запроса` limit` будет необязательным и может быть опущен клиентом.

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `LimitOffsetPagination` on a per-view basis.

В подклассах `genericapiview` вы также можете установить атрибут` pagination_class`, чтобы выбрать `LimitoffsetPagination` на основе для каждого обзора.

#### Configuration

#### Конфигурация

The `LimitOffsetPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `LimitoffsetPagination 'включает в себя ряд атрибутов, которые могут быть переопределены для изменения стиля страниц.

To set these attributes you should override the `LimitOffsetPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, вы должны переопределить класс `LimitoffsetPagination`, а затем включить свой класс пользовательского страниц, как указано выше.

* `default_limit` - A numeric value indicating the limit to use if one is not provided by the client in a query parameter. Defaults to the same value as the `PAGE_SIZE` settings key.
* `limit_query_param` - A string value indicating the name of the "limit" query parameter. Defaults to `'limit'`.
* `offset_query_param` - A string value indicating the name of the "offset" query parameter. Defaults to `'offset'`.
* `max_limit` - If set this is a numeric value indicating the maximum allowable limit that may be requested by the client. Defaults to `None`.
* `template` - The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/numbers.html"`.

* `default_limit` - числовое значение, указывающее ограничение для использования, если кто -то не предоставлен клиентом в параметре запроса.
По умолчанию к тому же значению, что и клавиша настройки `page_size`.
* `Limit_query_param` - Значение строки, указывающее имя параметра запроса« Limit ».
По умолчанию «ограничение».
* `offset_query_param` - Значение строки, указывающее имя параметра запроса« Offset ».
По умолчанию «смещение».
* `max_limit` - если установлено, это числовое значение, указывающее максимально допустимое предел, который может быть запрошен клиентом.
По умолчанию «нет».
* `шаблон
Может быть переопределен, чтобы изменить стиль рендеринга или установить на «Нет», чтобы полностью отключить управление HTML Pagination.
По умолчанию `" rest_framework/pagination/number.html "`.

---

## CursorPagination

## cursorpagination

The cursor-based pagination presents an opaque "cursor" indicator that the client may use to page through the result set. This pagination style only presents forward and reverse controls, and does not allow the client to navigate to arbitrary positions.

На основе курсора страсть представляет собой непрозрачный индикатор «курсора», который клиент может использовать для страницы через набор результатов.
Этот стиль страниц представляет только вперед и обратный элемент управления и не позволяет клиенту перемещаться в произвольные позиции.

Cursor based pagination requires that there is a unique, unchanging ordering of items in the result set. This ordering might typically be a creation timestamp on the records, as this presents a consistent ordering to paginate against.

На основе курсора нужен уникальный, неизменной заказ элементов в наборе результатов.
Это упорядочение, как правило, может быть временной меткой создания в записях, так как это представляет собой последовательный упорядоченность на странице.

Cursor based pagination is more complex than other schemes. It also requires that the result set presents a fixed ordering, and does not allow the client to arbitrarily index into the result set. However it does provide the following benefits:

На основе курсора страсть более сложна, чем другие схемы.
Также требуется, чтобы набор результатов представлял фиксированный заказ и не позволяет клиенту произвольно индекс в набор результатов.
Однако это дает следующие преимущества:

* Provides a consistent pagination view. When used properly `CursorPagination` ensures that the client will never see the same item twice when paging through records, even when new items are being inserted by other clients during the pagination process.
* Supports usage with very large datasets. With extremely large datasets pagination using offset-based pagination styles may become inefficient or unusable. Cursor based pagination schemes instead have fixed-time properties, and do not slow down as the dataset size increases.

* Обеспечивает последовательный вид на страсть.
При правильном использовании `cursorpagination` гарантирует, что клиент никогда не увидит один и тот же предмет дважды при подкидке через записи, даже когда новые элементы вставляются другими клиентами в процессе страниц.
* Поддерживает использование с очень большими наборами данных.
С чрезвычайно большими наборами данных с использованием смещанных стилей страниц может стать неэффективным или непригодным.
Вместо этого схемы страниц на основе курсора обладают свойствами фиксированного времени и не замедляются по мере увеличения размера набора данных.

#### Details and limitations

#### Детали и ограничения

Proper use of cursor based pagination requires a little attention to detail. You'll need to think about what ordering you want the scheme to be applied against. The default is to order by `"-created"`. This assumes that **there must be a 'created' timestamp field** on the model instances, and will present a "timeline" style paginated view, with the most recently added items first.

Правильное использование страниц на основе курсора требует небольшого внимания к деталям.
Вам нужно подумать о том, с каким заказом вы хотите применить схему.
По умолчанию есть заказ на `"-created "`.
Это предполагает, что ** должно быть «созданное» поле Timestamp ** на экземплярах модели, и представит странный вид в стиле «график», а в первую очередь из последних добавленных элементов.

You can modify the ordering by overriding the `'ordering'` attribute on the pagination class, or by using the `OrderingFilter` filter class together with `CursorPagination`. When used with `OrderingFilter` you should strongly consider restricting the fields that the user may order by.

Вы можете изменить упорядочение, переопределив атрибут «Заказа» в классе страниц или используя класс фильтра `OrdingFilter 'вместе с` cursorpagination'.
При использовании с `OrdingFilter` вы должны решительно рассмотреть возможность ограничения поля, которые пользователь может заказывать.

Proper usage of cursor pagination should have an ordering field that satisfies the following:

Правильное использование курсора -страниц должно иметь поле для упорядочения, которое удовлетворяет следующему:

* Should be an unchanging value, such as a timestamp, slug, or other field that is only set once, on creation.
* Should be unique, or nearly unique. Millisecond precision timestamps are a good example. This implementation of cursor pagination uses a smart "position plus offset" style that allows it to properly support not-strictly-unique values as the ordering.
* Should be a non-nullable value that can be coerced to a string.
* Should not be a float. Precision errors easily lead to incorrect results. Hint: use decimals instead. (If you already have a float field and must paginate on that, an [example `CursorPagination` subclass that uses decimals to limit precision is available here](https://gist.github.com/keturn/8bc88525a183fd41c73ffb729b8865be#file-fpcursorpagination-py).)
* The field should have a database index.

* Должен быть неизменным значением, таким как метка времени, слизняк или другое поле, которое установлено только один раз, при создании.
* Должен быть уникальным или почти уникальным.
Миллисекундные точные временные метки - хороший пример.
В этой реализации курсоровской страниц используется умный стиль «позиции плюс смещение», который позволяет ему должным образом поддерживать нетронутые значения в качестве упорядочения.
* Должно быть не нулеваемое значение, которое может быть принуждено к строке.
* Не должен быть поплавком.
Точные ошибки легко приводят к неправильным результатам.
Подсказка: вместо этого используйте десятичные десятки.
(Если у вас уже есть поле для плавания, и вы должны нанесены на пчел на это, здесь доступен [пример `cursorpagination`, который использует десятичные десятичные знаки для ограничения точности] (https://gist.github.com/keturn/8bc88525a183fd41c73ffb729b8865be#file-fpcursportic-
py).)
* Поле должно иметь индекс базы данных.

Using an ordering field that does not satisfy these constraints will generally still work, but you'll be losing some of the benefits of cursor pagination.

Использование поля заказа, которое не удовлетворяет эти ограничения, как правило, все еще будет работать, но вы потеряете некоторые преимущества курсора.

For more technical details on the implementation we use for cursor pagination, the ["Building cursors for the Disqus API"](https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api) blog post gives a good overview of the basic approach.

Для получения дополнительной технической информации о реализации, которую мы используем для курсора, [«Строительные курсоры для API DISQUS»] (https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api
) Пост в блоге дает хороший обзор основного подхода.

#### Setup

#### Настраивать

To enable the `CursorPagination` style globally, use the following configuration, modifying the `PAGE_SIZE` as desired:

Чтобы включить стиль `cursorpagination 'глобально, используйте следующую конфигурацию, изменив` page_size` по желанию:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 100
}
```

On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `CursorPagination` on a per-view basis.

В подклассах `genericapiview` вы также можете установить атрибут` pagination_class`, чтобы выбрать `cursorpagination` на основе для обзора.

#### Configuration

#### Конфигурация

The `CursorPagination` class includes a number of attributes that may be overridden to modify the pagination style.

Класс `cursorpagination включает в себя ряд атрибутов, которые могут быть переопределены, чтобы изменить стиль странификации.

To set these attributes you should override the `CursorPagination` class, and then enable your custom pagination class as above.

Чтобы установить эти атрибуты, вы должны переопределить класс `cursorpagination ', а затем включить свой собственный класс страниц, как указано выше.

* `page_size` = A numeric value indicating the page size. If set, this overrides the `PAGE_SIZE` setting. Defaults to the same value as the `PAGE_SIZE` settings key.
* `cursor_query_param` = A string value indicating the name of the "cursor" query parameter. Defaults to `'cursor'`.
* `ordering` = This should be a string, or list of strings, indicating the field against which the cursor based pagination will be applied. For example: `ordering = 'slug'`. Defaults to `-created`. This value may also be overridden by using `OrderingFilter` on the view.
* `template` = The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/previous_and_next.html"`.

* `page_size` = числовое значение, указывающее размер страницы.
Если установлено, это переопределяет настройку `page_size`.
По умолчанию к тому же значению, что и клавиша настройки `page_size`.
* `cursor_query_param` = Значение строки, указывающее имя параметра запроса« Курсор ».
По умолчанию «курсор».
* `ordering` = это должна быть строка или список строк, что указывает на поле, против которого будет применяться страница на основе курсора.
Например: `ording = 'slug'`.
По умолчанию `-created`.
Это значение также может быть переопределено с использованием `ordingfilter` в представлении.
* `Шаблон` = Имя шаблона для использования при рендерингах управления страницей в API -файлах просмотра.
Может быть переопределен, чтобы изменить стиль рендеринга или установить на «Нет», чтобы полностью отключить управление HTML Pagination.
По умолчанию `" REST_FRAMEWORD/PAGINATION/PAREL_AND_NEXT.HTML "`.

---

# Custom pagination styles

# Пользовательские стили страниц

To create a custom pagination serializer class, you should inherit the subclass `pagination.BasePagination`, override the `paginate_queryset(self, queryset, request, view=None)`, and `get_paginated_response(self, data)` methods:

Чтобы создать пользовательский класс сериализатора страниц, вы должны унаследовать подкласс `pagination.basepagination`, переопределить` paginate_queryset (self, queryset, request, view = none) `и` get_pagination_response (self, data) `Методы: Методы: Методы: Методы: Методы: Методы: Методы: Методы

* The `paginate_queryset` method is passed to the initial queryset and should return an iterable object. That object contains only the data in the requested page.
* The `get_paginated_response` method is passed to the serialized page data and should return a `Response` instance.

* Метод `paginate_queryset` передается в начальный запрос и должен вернуть итерабильный объект.
Этот объект содержит только данные на запрошенной странице.
* Метод `get_pagination_response` передается в сериализованные данные страницы и должен вернуть экземпляр` recsess '.

Note that the `paginate_queryset` method may set state on the pagination instance, that may later be used by the `get_paginated_response` method.

Обратите внимание, что метод `paginate_queryset` может установить состояние на экземпляре страниц, который впоследствии может использоваться методом` get_pagination_response`.

## Example

## Пример

Suppose we want to replace the default pagination output style with a modified format that includes the next and previous links under in a nested 'links' key. We could specify a custom pagination class like so:

Предположим, мы хотим заменить стиль вывода страниц по умолчанию измененным форматом, который включает в себя следующие и предыдущие ссылки по вложенным ключам «ссылок».
Мы могли бы указать пользовательский класс страниц, как SO:

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

We'd then need to setup the custom class in our configuration:

Затем нам нужно настроить пользовательский класс в нашей конфигурации:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.CustomPagination',
    'PAGE_SIZE': 100
}
```

Note that if you care about how the ordering of keys is displayed in responses in the browsable API you might choose to use an `OrderedDict` when constructing the body of paginated responses, but this is optional.

Обратите внимание, что если вы заботитесь о том, как отображается заказ клавиш в ответах в API, подлежащих просмотру, вы можете использовать `orsomedDict 'при построении тела лиц на странах, но это необязательно.

## Using your custom pagination class

## Использование урока пользовательского страниц

To have your custom pagination class be used by default, use the `DEFAULT_PAGINATION_CLASS` setting:

Чтобы ваш пользовательский класс страниц был использован по умолчанию, используйте настройку `default_pagination_class`:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100
}
```

API responses for list endpoints will now include a `Link` header, instead of including the pagination links as part of the body of the response, for example:

Ответы API для конечных точек списка теперь будут включать заголовок «ссылки», вместо того, чтобы включать ссылки на страницы как часть тела ответа, например:

![Link Header](../img/link-header-pagination.png)

! [Заголовок ссылки] (../ IMG/Link-Header-pagination.png)

*A custom pagination style, using the 'Link' header'*

*Пользовательский стиль страниц, используя заголовок "ссылки"*

---

# HTML pagination controls

# HTML Pagination Controls

By default using the pagination classes will cause HTML pagination controls to be displayed in the browsable API. There are two built-in display styles. The `PageNumberPagination` and `LimitOffsetPagination` classes display a list of page numbers with previous and next controls. The `CursorPagination` class displays a simpler style that only displays a previous and next control.

По умолчанию с использованием классов страниц приведет к отображению управлений HTML -страниц в API.
Есть два встроенных стиля дисплея.
В классах `pagenumberpagination и` LimitoffsetPagination отображается список номеров страниц с предыдущими и следующими элементами управления.
Класс `cursorpagination отображает более простой стиль, который отображает только предыдущий и следующий элемент управления.

## Customizing the controls

## Настройка элементов управления

You can override the templates that render the HTML pagination controls. The two built-in styles are:

Вы можете переопределить шаблоны, которые отображают контроль HTML Pagination.
Два встроенных стиля:

* `rest_framework/pagination/numbers.html`
* `rest_framework/pagination/previous_and_next.html`

* `rest_framework/pagination/number.html`
* `REST_FRAMEWORD/PAGINATION/PAREL_AND_NEXT.HTML`

Providing a template with either of these paths in a global template directory will override the default rendering for the relevant pagination classes.

Предоставление шаблона с любым из этих путей в глобальном каталоге шаблонов будет переоценит рендеринг по умолчанию для соответствующих классов страниц.

Alternatively you can disable HTML pagination controls completely by subclassing on of the existing classes, setting `template = None` as an attribute on the class. You'll then need to configure your `DEFAULT_PAGINATION_CLASS` settings key to use your custom class as the default pagination style.

В качестве альтернативы вы можете полностью отключить управление страницей HTML, подклассные на существующих классах, установив `template = none` в качестве атрибута в классе.
Затем вам нужно настроить клавишу настроек `default_pagination_class`, чтобы использовать свой пользовательский класс в качестве стиля страниц по умолчанию.

#### Low-level API

#### Низкоуровневый API

The low-level API for determining if a pagination class should display the controls or not is exposed as a `display_page_controls` attribute on the pagination instance. Custom pagination classes should be set to `True` in the `paginate_queryset` method if they require the HTML pagination controls to be displayed.

API низкого уровня для определения того, должен ли класс странификации отображать элементы управления или нет, выставлен как атрибут `display_page_controls` в экземпляре страниц.
Пользовательские классы страниц должны быть установлены на `true` в методе` paginate_queryset`, если они требуют отображения элементов управления Pagination HTML.

The `.to_html()` and `.get_html_context()` methods may also be overridden in a custom pagination class in order to further customize how the controls are rendered.

Методы `.to_html ()` и `.get_html_context ()` также могут быть переопределены в пользовательском классе страниц, чтобы дополнительно настроить, как отображаются элементы управления.

---

# Third party packages

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## DRF-extensions

## drf-extensions

The [`DRF-extensions` package](https://chibisov.github.io/drf-extensions/docs/) includes a [`PaginateByMaxMixin` mixin class](https://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin) that allows your API clients to specify `?page_size=max` to obtain the maximum allowed page size.

[`` Drf-extensions` package] (https://chibisov.github.io/drf-extensions/docs/) включает в себя [`paginatebymaxmixin` class] (https://chibisov.github.io/drf-extensions] (https://chibisov.github.io/drf-extensions
/docs/#paginatebymaxmixin), который позволяет вашим клиентам API указывать `? Page_size = max`, чтобы получить максимально допустимый размер страницы.

## drf-proxy-pagination

## DRF-Proxy-Pagination

The [`drf-proxy-pagination` package](https://github.com/tuffnatty/drf-proxy-pagination) includes a `ProxyPagination` class which allows to choose pagination class with a query parameter.

[`` Drf-proxy-pagination` package] (https://github.com/tuffnatty/drf-proxy-pagination) включает класс `proxypagination`, который позволяет выбрать класс лиц с параметрами запроса.

## link-header-pagination

## Ссылка-заголовка

The [`django-rest-framework-link-header-pagination` package](https://github.com/tbeadle/django-rest-framework-link-header-pagination) includes a `LinkHeaderPagination` class which provides pagination via an HTTP `Link` header as described in [GitHub REST API documentation](https://docs.github.com/en/rest/guides/traversing-with-pagination).

[`` Django-rest-framework-link-header-pagination 'package] (https://github.com/tbeadle/django-rest-framework-leink-he-deran
заголовок http `link`, как описано в [документации Github Rest API] (https://docs.github.com/en/rest/guides/traversing-with-pagination).