<!-- TRANSLATED by md-translate -->
---

source:

источник:

* filters.py

* Filters.py

---

# Filtering

# Фильтрация

> The root QuerySet provided by the Manager describes all objects in the database table. Usually, though, you'll need to select only a subset of the complete set of objects.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters)

> Корневой запрос, предоставленный менеджером, описывает все объекты в таблице базы данных.
Обычно, однако, вам нужно выбрать только подмножество полного набора объектов.
>
>-[документация Django] (https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-price-objects-with-filters)

The default behavior of REST framework's generic list views is to return the entire queryset for a model manager. Often you will want your API to restrict the items that are returned by the queryset.

Поведение по умолчанию общих видов списка REST Framework состоит в том, чтобы вернуть весь запрос для менеджера моделей.
Часто вы захотите, чтобы ваш API ограничивал элементы, которые возвращаются Queryset.

The simplest way to filter the queryset of any view that subclasses `GenericAPIView` is to override the `.get_queryset()` method.

Самый простой способ отфильтровать запрос любого представления о том, что подклассы `genericapiview` - это переопределить метод .get_queryset ()`.

Overriding this method allows you to customize the queryset returned by the view in a number of different ways.

Переопределение этого метода позволяет настроить запрос, возвращаемый представлением различными способами.

## Filtering against the current user

## фильтрация по текущему пользователю

You might want to filter the queryset to ensure that only results relevant to the currently authenticated user making the request are returned.

Возможно, вы захотите отфильтровать Queryset, чтобы гарантировать, что только результаты, имеющие отношение к нынешнему аутентированному пользователю, возвращаются запрос.

You can do so by filtering based on the value of `request.user`.

Вы можете сделать это путем фильтрации на основе значения `request.user`.

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

## фильтрация против URL

Another style of filtering might involve restricting the queryset based on some part of the URL.

Другой стиль фильтрации может включать ограничение запроса на основе какой -то части URL.

For example if your URL config contained an entry like this:

Например, если ваша конфигурация URL содержала запись, подобную следующему:

```
re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
```

You could then write a view that returned a purchase queryset filtered by the username portion of the URL:

Затем вы можете написать представление, которое вернуло заправочный запрос, отфильтрованную частью URL -имени пользователя:

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

Последним примером фильтрации начального запроса было бы определить начальный запрос на основе параметров запроса в URL.

We can override `.get_queryset()` to deal with URLs such as `http://example.com/api/purchases?username=denvercoder9`, and filter the queryset only if the `username` parameter is included in the URL:

Мы можем переопределить `.get_queryset ()` для работы с URL -адресами, такими как `http: //example.com/api/purchases? Username = denvercoder9`, и отфильтруйте Queryset только в том случае, если параметр` username 'включен в URL:

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

Помимо возможности переопределить запрос по умолчанию, структура REST также включает в себя поддержку бэкэндов общей фильтрации, которые позволяют легко создавать сложные поиски и фильтры.

Generic filters can also present themselves as HTML controls in the browsable API and admin API.

Общие фильтры также могут представлять себя в качестве управления HTML в API и AD API для просмотра и администратора.

![Filter Example](../img/filter-controls.png)

! [Пример фильтра] (../ img/filter-controls.png)

## Setting filter backends

## Установка бэкэндов фильтра

The default filter backends may be set globally, using the `DEFAULT_FILTER_BACKENDS` setting. For example.

Бэкэнды фильтра по умолчанию могут быть установлены по всему миру, используя настройку `default_filter_backends`.
Например.

```
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

You can also set the filter backends on a per-view, or per-viewset basis, using the `GenericAPIView` class-based views.

Вы также можете установить бэкэнды фильтра для каждого вида или на основе на расстояние, используя классовые представления `genericapiview` на основе класса.

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

Обратите внимание, что если бэкэнд фильтра настроен для представления, а также используется для фильтрации видов списка, он также будет использоваться для фильтрации запросов, используемых для возврата одного объекта.

For instance, given the previous example, and a product with an id of `4675`, the following URL would either return the corresponding object, or return a 404 response, depending on if the filtering conditions were met by the given product instance:

Например, с учетом предыдущего примера и продукта с идентификатором `4675`, следующий URL -адрес вернет соответствующий объект, либо вернет ответ 404, в зависимости от того, были ли условия фильтрации соответствующим экземпляру продукта:

```
http://example.com/api/products/4675/?category=clothing&max_price=10.00
```

## Overriding the initial queryset

## переопределяет начальный запрос

Note that you can use both an overridden `.get_queryset()` and generic filtering together, and everything will work as expected. For example, if `Product` had a many-to-many relationship with `User`, named `purchase`, you might want to write a view like this:

Обратите внимание, что вы можете использовать как переопределенную `.get_queryset ()`, так и общая фильтрация вместе, и все будет работать, как и ожидалось.
Например, если `product` имел много ко многим отношениям с` user ', именем «покупка», вы, возможно, захотите написать представление, как это:

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

# Guide API

## DjangoFilterBackend

## djangofilterbackend

The [`django-filter`](https://django-filter.readthedocs.io/en/latest/index.html) library includes a `DjangoFilterBackend` class which supports highly customizable field filtering for REST framework.

Библиотека [`` django-filter`] (https://django-filter.readthedocs.io/en/latest/index.html) включает в себя класс djangofilterbackend`, который поддерживает высоко настраиваемые полевые фильтрации для Framework.

To use `DjangoFilterBackend`, first install `django-filter`.

Чтобы использовать `djangofilterbackend`, сначала установите` django-filter '.

```
pip install django-filter
```

Then add `'django_filters'` to Django's `INSTALLED_APPS`:

Затем добавьте `'django_filters'' к Django` staded_apps`:

```
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

You should now either add the filter backend to your settings:

Теперь вы должны либо добавить бэкэнд фильтра в свои настройки:

```
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Or add the filter backend to an individual View or ViewSet.

Или добавьте бэкэнд фильтра в отдельный вид или сет.

```
from django_filters.rest_framework import DjangoFilterBackend

class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]
```

If all you need is simple equality-based filtering, you can set a `filterset_fields` attribute on the view, or viewset, listing the set of fields you wish to filter against.

Если все, что вам нужно,-это простая фильтрация на основе равенства, вы можете установить атрибут `filterest_fields` в представлении или сет, перечисляя набор полей, с которыми вы хотите отфильтровать.

```
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']
```

This will automatically create a `FilterSet` class for the given fields, and will allow you to make requests such as:

Это автоматически создаст класс `filterset` для данных полей и позволит вам выполнять такие запросы, как:

```
http://example.com/api/products?category=clothing&in_stock=True
```

For more advanced filtering requirements you can specify a `FilterSet` class that should be used by the view. You can read more about `FilterSet`s in the [django-filter documentation](https://django-filter.readthedocs.io/en/latest/index.html). It's also recommended that you read the section on [DRF integration](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

Для получения более продвинутых требований к фильтрации вы можете указать класс «Фильтра», который следует использовать с помощью представления.
Вы можете прочитать больше о «FilterSet» в документации [django-filter] (https://django-filter.readthedocs.io/en/latest/index.html).
Также рекомендуется прочитать раздел по [DRF Integration] (https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

## SearchFilter

## searchfilter

The `SearchFilter` class supports simple single query parameter based searching, and is based on the [Django admin's search functionality](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

Класс `searchfilter` поддерживает простой поиск на основе параметров одного запроса и основан на функциональности поиска [Django Admin] (https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.
admin.modeladmin.search_fields).

When in use, the browsable API will include a `SearchFilter` control:

При использовании в API Browsable будет включать элемент управления SearchFilter`:

![Search Filter](../img/search-filter.png)

! [Поиск фильтра] (../ img/search-filter.png)

The `SearchFilter` class will only be applied if the view has a `search_fields` attribute set. The `search_fields` attribute should be a list of names of text type fields on the model, such as `CharField` or `TextField`.

Класс `searchfilter` будет применяться только в том случае, если представление имеет набор атрибутов search_fields`.
Атрибутом `search_fields` должен быть список имен полей типа текста на модели, таких как` charfield` или `textfield`.

```
from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
```

This will allow the client to filter the items in the list by making queries such as:

Это позволит клиенту отфильтровать элементы в списке, делая такие запросы, как:

```
http://example.com/api/users?search=russell
```

You can also perform a related lookup on a ForeignKey or ManyToManyField with the lookup API double-underscore notation:

Вы также можете выполнить связанный поиск на иностранной кладке или многопоманфилде с нотацией API API API:

```
search_fields = ['username', 'email', 'profile__profession']
```

For [JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield) and [HStoreField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#hstorefield) fields you can filter based on nested values within the data structure using the same double-underscore notation:

Для [jsonfield] (https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield) и [hstorefield] (https://docs.djangoproject.com/en/3.0/ref
/Поля Contrib/Postgres/Fields/#hstorefield) Вы можете фильтровать на основе вложенных значений в структуре данных, используя одинаковую двойную нотацию:

```
search_fields = ['data__breed', 'data__owner__other_pets__0__name']
```

By default, searches will use case-insensitive partial matches. The search parameter may contain multiple search terms, which should be whitespace and/or comma separated. If multiple search terms are used then objects will be returned in the list only if all the provided terms are matched.

По умолчанию поиски будут использовать нежелательные частичные совпадения.
Параметр поиска может содержать несколько терминов поиска, которые должны быть отделены пробелы и/или запятой.
Если используются несколько членов поиска, то объекты будут возвращены в списке, только если все предоставленные термины сопоставлены.

The search behavior may be restricted by prepending various characters to the `search_fields`.

Поведение поиска может быть ограничено путем подготовки различных символов к `search_fields`.

* '^' Starts-with search.
* '=' Exact matches.
* '@' Full-text search. (Currently only supported Django's [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
* '$' Regex search.

* '^' Запускается с поиском.
* '=' Точные совпадения.
* '@' Полнотекстовый поиск.
(В настоящее время только поддерживает Django [Postgresql Backend] (https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/).)
* '$' Поиск режима.

For example:

Например:

```
search_fields = ['=username', '=email']
```

By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting.

По умолчанию параметр поиска называется «Поиск», но это может быть переопределено с настройкой `search_param`.

To dynamically change search fields based on request content, it's possible to subclass the `SearchFilter` and override the `get_search_fields()` function. For example, the following subclass will only search on `title` if the query parameter `title_only` is in the request:

Чтобы динамически изменить поля поиска на основе содержимого запроса, можно подкласс `searchfilter` и переопределить функцию` get_search_fields () `.
Например, следующий подкласс будет искать только на `title`, если параметр запроса` title_only` находится в запросе:

```
from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)
```

For more details, see the [Django documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

Для получения дополнительной информации см. Документацию [django] (https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.modeladmin.search_fields).

---

## OrderingFilter

## ordingfilter

The `OrderingFilter` class supports simple query parameter controlled ordering of results.

Класс `OrdingFilter` поддерживает простой параметр« Параметр -параметры », контролируемый параметрами, контролируемые результатами.

![Ordering Filter](../img/ordering-filter.png)

! [Заказать фильтр] (../ img/ording-filter.png)

By default, the query parameter is named `'ordering'`, but this may by overridden with the `ORDERING_PARAM` setting.

По умолчанию параметр запроса называется «заказ», но это может переопределяться с настройкой `ordering_param`.

For example, to order users by username:

Например, заказывать пользователей по имени пользователя:

```
http://example.com/api/users?ordering=username
```

The client may also specify reverse orderings by prefixing the field name with '-', like so:

Клиент также может указать обратные заказы, префиксив имя поля с '-', как так:

```
http://example.com/api/users?ordering=-username
```

Multiple orderings may also be specified:

Также могут быть указаны несколько заказов:

```
http://example.com/api/users?ordering=account,username
```

### Specifying which fields may be ordered against

### Указание, какие поля могут быть заказаны против

It's recommended that you explicitly specify which fields the API should allowing in the ordering filter. You can do this by setting an `ordering_fields` attribute on the view, like so:

Рекомендуется, чтобы вы явно указали, какие поля API следует разрешать в фильтре упорядочения.
Вы можете сделать это, установив атрибут `ordering_fields` в представлении, например, так:

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
```

This helps prevent unexpected data leakage, such as allowing users to order against a password hash field or other sensitive data.

Это помогает предотвратить неожиданную утечку данных, такую как позволяет пользователям заказывать поля хэша пароля или другие конфиденциальные данные.

If you *don't* specify an `ordering_fields` attribute on the view, the filter class will default to allowing the user to filter on any readable fields on the serializer specified by the `serializer_class` attribute.

Если вы * не * укажите атрибут `ordering_fields` в представлении, класс фильтра по умолчанию позволит пользователю фильтровать любые читаемые поля на сериализаторе, указанном атрибутом` serializer_class`.

If you are confident that the queryset being used by the view doesn't contain any sensitive data, you can also explicitly specify that a view should allow ordering on *any* model field or queryset aggregate, by using the special value `'__all__'`.

Если вы уверены, что запрос, который используется представлением, не содержит никаких конфиденциальных данных, вы также можете явно указать, что представление должно разрешать упорядочение на * любое * поле Model или заполнитель запроса, используя специальное значение `__all__ '
`.

```
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
```

### Specifying a default ordering

### Указание по умолчанию

If an `ordering` attribute is set on the view, this will be used as the default ordering.

Если атрибут `Заказа` установлен в представлении, он будет использоваться в качестве упорядочения по умолчанию.

Typically you'd instead control this by setting `order_by` on the initial queryset, but using the `ordering` parameter on the view allows you to specify the ordering in a way that it can then be passed automatically as context to a rendered template. This makes it possible to automatically render column headers differently if they are being used to order the results.

Как правило, вместо этого вы управляете этим, установив `order_by` на начальный запрос, но использование параметра` ordering` в представлении позволяет указать упорядочение так, чтобы его можно было автоматически передавать в качестве контекста в шаблон рендеринга.
Это позволяет автоматически отображать заголовки столбцов по -разному, если они используются для упорядочения результатов.

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
```

The `ordering` attribute may be either a string or a list/tuple of strings.

Атрибут `ordering` может быть либо строкой, либо списком/корпусом строк.

---

# Custom generic filtering

# Пользовательская общая фильтрация

You can also provide your own generic filtering backend, or write an installable app for other developers to use.

Вы также можете предоставить свой собственный бэкэнд фильтрации фильтрации или написать приложение для использования установленным приложением для других разработчиков.

To do so override `BaseFilterBackend`, and override the `.filter_queryset(self, request, queryset, view)` method. The method should return a new, filtered queryset.

Чтобы переопределить `basefilterbackend` и переопределить метод` .filter_queryset (self, запрос, queryset, view) `.
Метод должен вернуть новый фильтрованный запрос.

As well as allowing clients to perform searches and filtering, generic filter backends can be useful for restricting which objects should be visible to any given request or user.

Помимо разрешения клиентов выполнять поиск и фильтрацию, общие бэкэнды фильтров могут быть полезны для ограничения того, какие объекты должны быть видны любому данному запросу или пользователю.

## Example

## Пример

For example, you might need to restrict users to only being able to see objects they created.

Например, вам может потребоваться ограничить пользователей только возможность видеть объекты, которые они создали.

```
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

We could achieve the same behavior by overriding `get_queryset()` on the views, but using a filter backend allows you to more easily add this restriction to multiple views, or to apply it across the entire API.

Мы могли бы достичь того же поведения, переопределив `get_queryset ()` в представлениях, но использование бэкэнда фильтра позволяет вам легче добавить это ограничение к нескольким представлениям или применять его по всему API.

## Customizing the interface

## Настройка интерфейса

Generic filters may also present an interface in the browsable API. To do so you should implement a `to_html()` method which returns a rendered HTML representation of the filter. This method should have the following signature:

Общие фильтры также могут представлять интерфейс в API -интерфейсе.
Для этого вы должны реализовать метод `to_html ()`, который возвращает отображаемое HTML -представление фильтра.
Этот метод должен иметь следующую подпись:

`to_html(self, request, queryset, view)`

`to_html (Self, запрос, запрос, просмотр)`

The method should return a rendered HTML string.

Метод должен вернуть отображаемую строку HTML.

# Third party packages

# Сторонние пакеты

The following third party packages provide additional filter implementations.

Следующие сторонние пакеты предоставляют дополнительные реализации фильтров.

## Django REST framework filters package

## Django Rest Framework Filters Package

The [django-rest-framework-filters package](https://github.com/philipn/django-rest-framework-filters) works together with the `DjangoFilterBackend` class, and allows you to easily create filters across relationships, or create multiple filter lookup types for a given field.

[Django-rest-framework-filters пакет] (https://github.com/philipn/django-rest-framework-filters) работает вместе с классом djangofilterbackend` и позволяет легко создавать фильтры по отношениям или
Создайте несколько типов поиска фильтров для данного поля.

## Django REST framework full word search filter

## Django Rest Framework Полный поиск

The [djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter) developed as alternative to `filters.SearchFilter` which will search full word in text, or exact match.

[Djangestframeworkword-word-filter] (https://github.com/trollknurr/django-rest-framework-word-search-pilter) разработан как альтернатива `filters.searchfilter`, который будет искать полное слово в тексте или точное
соответствие.

## Django URL Filter

## Django URL -фильтр

[django-url-filter](https://github.com/miki725/django-url-filter) provides a safe way to filter data via human-friendly URLs. It works very similar to DRF serializers and fields in a sense that they can be nested except they are called filtersets and filters. That provides easy way to filter related data. Also this library is generic-purpose so it can be used to filter other sources of data and not only Django `QuerySet`s.

[django-url-filter] (https://github.com/miki725/django-url-filter) обеспечивает безопасный способ фильтрации данных с помощью URL-адресов, благоприятных для человека.
Это очень похоже на сериалы и поля DRF в некотором смысле, что их можно вложить, за исключением того, что они называются фильтрами и фильтрами.
Это обеспечивает простой способ фильтрации связанных данных.
Также эта библиотека является общим назначением, поэтому ее можно использовать для фильтрации других источников данных, а не только Django `Queryset.

## drf-url-filters

## DRF-URL-Фильтер

[drf-url-filter](https://github.com/manjitkumar/drf-url-filters) is a simple Django app to apply filters on drf `ModelViewSet`'s `Queryset` in a clean, simple and configurable way. It also supports validations on incoming query params and their values. A beautiful python package `Voluptuous` is being used for validations on the incoming query parameters. The best part about voluptuous is you can define your own validations as per your query params requirements.

[DRF-url-Filter] (https://github.com/manjitkumar/drf-url-filters)-это простое приложение Django для применения фильтров на DRF `modelViewSet` QuerySet` в чистом, простом и настраиваемом способе
Анкет
Он также поддерживает подтверждения в входящих параметрах запроса и их значениях.
Красивый пакет Python `Fultbout 'используется для проверки в входящих параметрах запроса.
Самое приятное в сладострастном - это определить свои собственные проверки в соответствии с требованиями параметров запросов.