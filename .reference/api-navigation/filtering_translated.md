<!-- TRANSLATED by md-translate -->
---

source:

источник:

* filters.py

* filters.py

---

# Filtering

# Фильтрация

> The root QuerySet provided by the Manager describes all objects in the database table. Usually, though, you'll need to select only a subset of the complete set of objects.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters)

> Корневой набор запросов, предоставляемый менеджером, описывает все объекты в таблице базы данных. Обычно, однако, вам нужно выбрать только подмножество полного набора объектов.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters)

The default behavior of REST framework's generic list views is to return the entire queryset for a model manager. Often you will want your API to restrict the items that are returned by the queryset.

Стандартным поведением общих представлений списка в REST framework является возврат всего набора запросов для менеджера модели. Часто вы хотите, чтобы ваш API ограничивал элементы, возвращаемые набором запросов.

The simplest way to filter the queryset of any view that subclasses `GenericAPIView` is to override the `.get_queryset()` method.

Самый простой способ фильтрации набора запросов любого представления, подкласса `GenericAPIView`, - переопределить метод `.get_queryset()`.

Overriding this method allows you to customize the queryset returned by the view in a number of different ways.

Переопределение этого метода позволяет вам настраивать набор запросов, возвращаемый представлением, различными способами.

## Filtering against the current user

## Фильтрация по текущему пользователю

You might want to filter the queryset to ensure that only results relevant to the currently authenticated user making the request are returned.

Вы можете захотеть отфильтровать набор запросов, чтобы гарантировать, что будут возвращены только результаты, относящиеся к текущему аутентифицированному пользователю, сделавшему запрос.

You can do so by filtering based on the value of `request.user`.

Это можно сделать с помощью фильтрации на основе значения `request.user`.

For example:

Например:

```
from myapp.models import Purchase
from myapp.serializers import PurchaseSerializer
from rest_framework import generics

class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Purchase.objects.filter(purchaser=user)
```

## Filtering against the URL

## Фильтрация по URL

Another style of filtering might involve restricting the queryset based on some part of the URL.

Другой стиль фильтрации может включать ограничение набора запросов на основе некоторой части URL.

For example if your URL config contained an entry like this:

Например, если ваша конфигурация URL содержит такую запись:

```
re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
```

You could then write a view that returned a purchase queryset filtered by the username portion of the URL:

Затем вы можете написать представление, которое возвращает набор запросов на покупку, отфильтрованный по имени пользователя в части URL:

```
class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)
```

## Filtering against query parameters

## Фильтрация по параметрам запроса

A final example of filtering the initial queryset would be to determine the initial queryset based on query parameters in the url.

Последним примером фильтрации начального набора запросов может быть определение начального набора запросов на основе параметров запроса в url.

We can override `.get_queryset()` to deal with URLs such as `http://example.com/api/purchases?username=denvercoder9`, and filter the queryset only if the `username` parameter is included in the URL:

Мы можем переопределить `.get_queryset()` для работы с URL, такими как `http://example.com/api/purchases?username=denvercoder9`, и фильтровать набор запросов, только если параметр `username` включен в URL:

```
class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Purchase.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset
```

---

# Generic Filtering

# Общая фильтрация

As well as being able to override the default queryset, REST framework also includes support for generic filtering backends that allow you to easily construct complex searches and filters.

Помимо возможности переопределения набора запросов по умолчанию, REST framework также включает поддержку общих бэкендов фильтрации, которые позволяют легко создавать сложные поиски и фильтры.

Generic filters can also present themselves as HTML controls in the browsable API and admin API.

Общие фильтры также могут быть представлены в виде элементов управления HTML в просматриваемом API и API администратора.

![Filter Example](../img/filter-controls.png)

![Пример фильтра](../img/filter-controls.png)

## Setting filter backends

## Настройка бэкендов фильтров

The default filter backends may be set globally, using the `DEFAULT_FILTER_BACKENDS` setting. For example.

Бэкенды фильтров по умолчанию можно установить глобально, используя параметр `DEFAULT_FILTER_BACKENDS`. Например.

```
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

You can also set the filter backends on a per-view, or per-viewset basis, using the `GenericAPIView` class-based views.

Вы также можете установить бэкенды фильтров на основе каждого представления или каждого набора представлений, используя представления на основе класса `GenericAPIView`.

```
import django_filters.rest_framework
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
```

## Filtering and object lookups

## Фильтрация и поиск объектов

Note that if a filter backend is configured for a view, then as well as being used to filter list views, it will also be used to filter the querysets used for returning a single object.

Обратите внимание, что если бэкэнд фильтра настроен для представления, то помимо того, что он используется для фильтрации представлений списка, он также будет использоваться для фильтрации наборов запросов, используемых для возврата одного объекта.

For instance, given the previous example, and a product with an id of `4675`, the following URL would either return the corresponding object, or return a 404 response, depending on if the filtering conditions were met by the given product instance:

Например, учитывая предыдущий пример и продукт с id `4675`, следующий URL либо вернет соответствующий объект, либо выдаст ответ 404, в зависимости от того, были ли выполнены условия фильтрации для данного экземпляра продукта:

```
http://example.com/api/products/4675/?category=clothing&max_price=10.00
```

## Overriding the initial queryset

## Переопределение начального набора запросов

Note that you can use both an overridden `.get_queryset()` and generic filtering together, and everything will work as expected. For example, if `Product` had a many-to-many relationship with `User`, named `purchase`, you might want to write a view like this:

Обратите внимание, что вы можете использовать и переопределенный `.get_queryset()`, и общую фильтрацию вместе, и все будет работать, как ожидалось. Например, если `Product` имеет отношение "многие-ко-многим" с `User`, названное `purchase`, вы можете написать представление следующим образом:

```
class PurchasedProductsList(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Product
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        user = self.request.user
        return user.purchase_set.all()
```

---

# API Guide

# Руководство по API

## DjangoFilterBackend

## DjangoFilterBackend

The [`django-filter`](https://django-filter.readthedocs.io/en/latest/index.html) library includes a `DjangoFilterBackend` class which supports highly customizable field filtering for REST framework.

Библиотека [`django-filter`](https://django-filter.readthedocs.io/en/latest/index.html) включает класс `DjangoFilterBackend`, который поддерживает высоконастраиваемую фильтрацию полей для REST-фреймворка.

To use `DjangoFilterBackend`, first install `django-filter`.

Чтобы использовать `DjangoFilterBackend`, сначала установите `django-filter`.

```
pip install django-filter
```

Then add `'django_filters'` to Django's `INSTALLED_APPS`:

Затем добавьте `'django_filters'` в `INSTALLED_APPS` Django:

```
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

You should now either add the filter backend to your settings:

Теперь вам следует либо добавить бэкенд фильтра в настройки:

```
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Or add the filter backend to an individual View or ViewSet.

Или добавьте бэкэнд фильтра к отдельному представлению или набору представлений.

```
from django_filters.rest_framework import DjangoFilterBackend

class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]
```

If all you need is simple equality-based filtering, you can set a `filterset_fields` attribute on the view, or viewset, listing the set of fields you wish to filter against.

Если вам нужна простая фильтрация на основе равенства, вы можете установить атрибут `filterset_fields` для представления или набора представлений, перечислив набор полей, по которым вы хотите фильтровать.

```
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']
```

This will automatically create a `FilterSet` class for the given fields, and will allow you to make requests such as:

Это автоматически создаст класс `FilterSet` для заданных полей и позволит вам делать такие запросы, как:

```
http://example.com/api/products?category=clothing&in_stock=True
```

For more advanced filtering requirements you can specify a `FilterSet` class that should be used by the view. You can read more about `FilterSet`s in the [django-filter documentation](https://django-filter.readthedocs.io/en/latest/index.html). It's also recommended that you read the section on [DRF integration](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

Для более сложных требований к фильтрации вы можете указать класс `FilterSet`, который должен использоваться представлением. Подробнее о `FilterSet` вы можете прочитать в [документации по django-filter](https://django-filter.readthedocs.io/en/latest/index.html). Также рекомендуется прочитать раздел [Интеграция DRF](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

## SearchFilter

## SearchFilter

The `SearchFilter` class supports simple single query parameter based searching, and is based on the [Django admin's search functionality](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

Класс `SearchFilter` поддерживает простой поиск по одному параметру запроса и основан на [Django admin's search functionality](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

When in use, the browsable API will include a `SearchFilter` control:

При использовании API с возможностью просмотра будет включать элемент управления `SearchFilter`:

![Search Filter](../img/search-filter.png)

![Фильтр поиска](../img/search-filter.png)

The `SearchFilter` class will only be applied if the view has a `search_fields` attribute set. The `search_fields` attribute should be a list of names of text type fields on the model, such as `CharField` or `TextField`.

Класс `SearchFilter` будет применяться, только если у представления установлен атрибут `search_fields`. Атрибут `search_fields` должен представлять собой список имен полей текстового типа в модели, таких как `CharField` или `TextField`.

```
from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
```

This will allow the client to filter the items in the list by making queries such as:

Это позволит клиенту фильтровать элементы в списке, делая такие запросы, как:

```
http://example.com/api/users?search=russell
```

You can also perform a related lookup on a ForeignKey or ManyToManyField with the lookup API double-underscore notation:

Вы также можете выполнить связанный поиск по полю ForeignKey или ManyToManyField с помощью нотации двойного неравенства API поиска:

```
search_fields = ['username', 'email', 'profile__profession']
```

For [JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield) and [HStoreField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#hstorefield) fields you can filter based on nested values within the data structure using the same double-underscore notation:

Для полей [JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield) и [HStoreField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#hstorefield) вы можете фильтровать на основе вложенных значений внутри структуры данных, используя ту же нотацию двойного ундеркорда:

```
search_fields = ['data__breed', 'data__owner__other_pets__0__name']
```

By default, searches will use case-insensitive partial matches. The search parameter may contain multiple search terms, which should be whitespace and/or comma separated. If multiple search terms are used then objects will be returned in the list only if all the provided terms are matched.

По умолчанию при поиске используются частичные совпадения без учета регистра. Параметр поиска может содержать несколько условий поиска, которые должны быть разделены пробелами и/или запятыми. Если используется несколько условий поиска, то объекты будут возвращены в списке только в том случае, если совпадут все указанные условия.

The search behavior may be restricted by prepending various characters to the `search_fields`.

Поведение поиска может быть ограничено путем добавления различных символов к `полям_поиска`.

* '^' Starts-with search.
* '=' Exact matches.
* '@' Full-text search. (Currently only supported Django's [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
* '$' Regex search.

* '^' Поиск с начала.
* '=' Точное совпадение.
* '@' Полнотекстовый поиск. (В настоящее время поддерживается только [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) Django).
* '$' Регексный поиск.

For example:

Например:

```
search_fields = ['=username', '=email']
```

By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting.

По умолчанию параметр поиска называется `'search'', но его можно переопределить с помощью параметра `SEARCH_PARAM`.

To dynamically change search fields based on request content, it's possible to subclass the `SearchFilter` and override the `get_search_fields()` function. For example, the following subclass will only search on `title` if the query parameter `title_only` is in the request:

Чтобы динамически изменять поля поиска на основе содержимого запроса, можно подклассифицировать `SearchFilter` и переопределить функцию `get_search_fields()`. Например, следующий подкласс будет искать только по `title`, если в запросе присутствует параметр запроса `title_only`:

```
from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)
```

For more details, see the [Django documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

Более подробную информацию можно найти в [документации Django](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

---

## OrderingFilter

## OrderingFilter

The `OrderingFilter` class supports simple query parameter controlled ordering of results.

Класс `OrderingFilter` поддерживает простое упорядочивание результатов, управляемое параметрами запроса.

![Ordering Filter](../img/ordering-filter.png)

![Ordering Filter](../img/ordering-filter.png)

By default, the query parameter is named `'ordering'`, but this may by overridden with the `ORDERING_PARAM` setting.

По умолчанию параметр запроса называется `'ordering'', но его можно переопределить с помощью параметра `ORDERING_PARAM'.

For example, to order users by username:

Например, чтобы упорядочить пользователей по имени пользователя:

```
http://example.com/api/users?ordering=username
```

The client may also specify reverse orderings by prefixing the field name with '-', like so:

Клиент также может указать обратный порядок, добавив к имени поля префикс '-', как показано ниже:

```
http://example.com/api/users?ordering=-username
```

Multiple orderings may also be specified:

Также можно указать несколько порядков:

```
http://example.com/api/users?ordering=account,username
```

### Specifying which fields may be ordered against

### Указание того, какие поля могут быть заказаны против

It's recommended that you explicitly specify which fields the API should allowing in the ordering filter. You can do this by setting an `ordering_fields` attribute on the view, like so:

Рекомендуется явно указать, какие поля API должен разрешить в фильтре упорядочивания. Это можно сделать, установив атрибут `ordering_fields` для представления, как показано ниже:

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
```

This helps prevent unexpected data leakage, such as allowing users to order against a password hash field or other sensitive data.

Это помогает предотвратить непредвиденную утечку данных, например, разрешение пользователям делать заказы по хэш-полю пароля или других конфиденциальных данных.

If you *don't* specify an `ordering_fields` attribute on the view, the filter class will default to allowing the user to filter on any readable fields on the serializer specified by the `serializer_class` attribute.

Если вы *не* указали атрибут `orderering_fields` для представления, класс фильтра будет по умолчанию позволять пользователю фильтровать по любым читаемым полям на сериализаторе, указанном атрибутом `serializer_class`.

If you are confident that the queryset being used by the view doesn't contain any sensitive data, you can also explicitly specify that a view should allow ordering on *any* model field or queryset aggregate, by using the special value `'__all__'`.

Если вы уверены, что кверисет, используемый представлением, не содержит конфиденциальных данных, вы также можете явно указать, что представление должно разрешить упорядочивание по *любому* полю модели или агрегату кверисета, используя специальное значение `'__all__'`.

```
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
```

### Specifying a default ordering

### Указание порядка по умолчанию

If an `ordering` attribute is set on the view, this will be used as the default ordering.

Если для представления установлен атрибут `ordering`, он будет использоваться в качестве упорядочивания по умолчанию.

Typically you'd instead control this by setting `order_by` on the initial queryset, but using the `ordering` parameter on the view allows you to specify the ordering in a way that it can then be passed automatically as context to a rendered template. This makes it possible to automatically render column headers differently if they are being used to order the results.

Обычно вы контролируете это, устанавливая `order_by` в исходном наборе запросов, но использование параметра `ordering` в представлении позволяет вам указать порядок таким образом, что он может быть автоматически передан в качестве контекста шаблону рендеринга. Это позволяет автоматически отображать заголовки столбцов по-разному, если они используются для упорядочивания результатов.

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
```

The `ordering` attribute may be either a string or a list/tuple of strings.

Атрибут `orderering` может быть либо строкой, либо списком/кортежем строк.

---

# Custom generic filtering

# Пользовательская общая фильтрация

You can also provide your own generic filtering backend, or write an installable app for other developers to use.

Вы также можете предоставить свой собственный общий бэкэнд фильтрации или написать устанавливаемое приложение для использования другими разработчиками.

To do so override `BaseFilterBackend`, and override the `.filter_queryset(self, request, queryset, view)` method. The method should return a new, filtered queryset.

Для этого переопределите `BaseFilterBackend` и переопределите метод `.filter_queryset(self, request, queryset, view)`. Метод должен возвращать новый, отфильтрованный набор запросов.

As well as allowing clients to perform searches and filtering, generic filter backends can be useful for restricting which objects should be visible to any given request or user.

Помимо того, что клиенты могут выполнять поиск и фильтрацию, общие бэкенды фильтров могут быть полезны для ограничения того, какие объекты должны быть видны для каждого конкретного запроса или пользователя.

## Example

## Пример

For example, you might need to restrict users to only being able to see objects they created.

Например, вам может понадобиться ограничить доступ пользователей только к созданным ими объектам.

```
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

We could achieve the same behavior by overriding `get_queryset()` on the views, but using a filter backend allows you to more easily add this restriction to multiple views, or to apply it across the entire API.

Мы могли бы добиться такого же поведения, переопределив `get_queryset()` в представлениях, но использование бэкенда фильтров позволяет вам легче добавить это ограничение к нескольким представлениям или применить его ко всему API.

## Customizing the interface

## Настройка интерфейса

Generic filters may also present an interface in the browsable API. To do so you should implement a `to_html()` method which returns a rendered HTML representation of the filter. This method should have the following signature:

Общие фильтры также могут представлять интерфейс в просматриваемом API. Для этого необходимо реализовать метод `to_html()`, который возвращает отрисованное HTML-представление фильтра. Этот метод должен иметь следующую сигнатуру:

`to_html(self, request, queryset, view)`

`to_html(self, request, queryset, view)`.

The method should return a rendered HTML string.

Метод должен возвращать отрендеренную строку HTML.

# Third party packages

# Пакеты сторонних производителей

The following third party packages provide additional filter implementations.

Следующие пакеты сторонних производителей предоставляют дополнительные реализации фильтров.

## Django REST framework filters package

## Пакет фильтров фреймворка Django REST

The [django-rest-framework-filters package](https://github.com/philipn/django-rest-framework-filters) works together with the `DjangoFilterBackend` class, and allows you to easily create filters across relationships, or create multiple filter lookup types for a given field.

Пакет [django-rest-framework-filters](https://github.com/philipn/django-rest-framework-filters) работает вместе с классом `DjangoFilterBackend` и позволяет вам легко создавать фильтры по отношениям или создавать несколько типов поиска фильтра для заданного поля.

## Django REST framework full word search filter

## Django REST framework полный фильтр поиска слов

The [djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter) developed as alternative to `filters.SearchFilter` which will search full word in text, or exact match.

[djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter) разработан как альтернатива `filters.SearchFilter`, который будет искать полное слово в тексте, или точное совпадение.

## Django URL Filter

## Django URL Filter

[django-url-filter](https://github.com/miki725/django-url-filter) provides a safe way to filter data via human-friendly URLs. It works very similar to DRF serializers and fields in a sense that they can be nested except they are called filtersets and filters. That provides easy way to filter related data. Also this library is generic-purpose so it can be used to filter other sources of data and not only Django `QuerySet`s.

[django-url-filter](https://github.com/miki725/django-url-filter) предоставляет безопасный способ фильтрации данных по удобным для человека URL. Он работает очень похоже на сериализаторы и поля DRF в том смысле, что они могут быть вложенными, за исключением того, что они называются filtersets и filters. Это обеспечивает простой способ фильтрации связанных данных. Также эта библиотека является универсальной, поэтому ее можно использовать для фильтрации других источников данных, а не только Django `QuerySet`.

## drf-url-filters

## drf-url-filters

[drf-url-filter](https://github.com/manjitkumar/drf-url-filters) is a simple Django app to apply filters on drf `ModelViewSet`'s `Queryset` in a clean, simple and configurable way. It also supports validations on incoming query params and their values. A beautiful python package `Voluptuous` is being used for validations on the incoming query parameters. The best part about voluptuous is you can define your own validations as per your query params requirements.

[drf-url-filter](https://github.com/manjitkumar/drf-url-filters) - это простое Django приложение для применения фильтров к drf `ModelViewSet` `Queryset` чистым, простым и настраиваемым способом. Оно также поддерживает валидацию входящих параметров запроса и их значений. Для проверки входящих параметров запроса используется красивый пакет python `Voluptuous`. Самое лучшее в voluptuous то, что вы можете определить свои собственные валидации в соответствии с требованиями к параметрам запроса.