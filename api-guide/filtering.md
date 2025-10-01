<!-- TRANSLATED by md-translate -->
---

источник:
- filters.py

---

# Фильтрация

> Корневой QuerySet, предоставляемый менеджером, описывает все объекты в таблице базы данных. Однако обычно требуется выбрать только подмножество из полного набора объектов.
>
> &mdash; [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters)

По умолчанию общие списочные представления DRF возвращают весь `QuerySet` для менеджера модели. Часто требуется, чтобы API ограничивал количество элементов, возвращаемых `QuerySet`.

Простейшим способом фильтрации `QuerySet` любого представления, подкласса `GenericAPIView`, является переопределение метода `.get_queryset()`.

Переопределение этого метода позволяет настраивать `QuerySet`, возвращаемый представлением, различными способами.

## Фильтрация по текущему пользователю

Возможно, потребуется отфильтровать `QuerySet`, чтобы возвращать только результаты, относящиеся к текущему аутентифицированному пользователю, сделавшему запрос.

Это можно сделать с помощью фильтрации по значению `request.user`.

Например:

```python
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

## Фильтрация по URL

Другой стиль фильтрации может включать ограничение `QuerySet` на основе некоторой части URL.

Например, если в конфигурации URL содержится запись следующего вида:

```python
re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
```

Затем вы можете написать представление, возвращающее `QuerySet` покупок, отфильтрованный по имени пользователя в части URL:

```python
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

## Фильтрация по параметрам запроса

Следующим примером фильтрации исходного QuerySet может быть определение исходного QuerySet на основе параметров запроса в url.

Мы можем переопределить `.get_queryset()` для работы с такими URL, как `http://example.com/api/purchases?username=denvercoder9`, и фильтровать QuerySet только в том случае, если в URL включен параметр `username`:

```python
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

# Общая фильтрация

Помимо возможности переопределения стандартного QuerySet, DRF также включает поддержку общих бэкендов фильтрации, которые позволяют легко строить сложные поисковые запросы и фильтры.

Общие фильтры также могут быть представлены в виде элементов управления HTML в API просмотра и API администрирования.

![Пример фильтра](https://github.com/encode/django-rest-framework/raw/main/docs/img/filter-controls.png)

## Настройка бэкендов фильтров

Бэкенды фильтров по умолчанию могут быть заданы глобально, с помощью параметра `DEFAULT_FILTER_BACKENDS`. Например:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Вы также можете задать бэкенды фильтров для каждого вида или для каждого набора видов, используя класс `GenericAPIView`, основанный на представлениях.

```python
import django_filters.rest_framework
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
```

## Фильтрация и поиск объектов

Обратите внимание, что если для представления настроен бэкэнд фильтрации, то он будет использоваться не только для фильтрации списочных представлений, но и для фильтрации `QuerySet`, используемых для возврата одного объекта.

Например, если взять предыдущий пример и товар с идентификатором `4675`, то следующий URL будет либо возвращать соответствующий объект, либо возвращать ответ 404, в зависимости от того, были ли выполнены условия фильтрации для данного экземпляра товара:

```bash
http://example.com/api/products/4675/?category=clothing&max_price=10.00
```

## Переопределение исходного QuerySet

Обратите внимание, что можно использовать и переопределенный `.get_queryset()`, и общую фильтрацию, и все будет работать так, как ожидается. Например, если у `Product` есть отношение "многие-ко-многим" с `User`, названное `purchase`, вы можете написать представление следующим образом:

```python
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

# Руководство по API

## DjangoFilterBackend

Библиотека [`django-filter`](https://django-filter.readthedocs.io/en/latest/index.html) включает класс `DjangoFilterBackend`, который поддерживает высоконастраиваемую фильтрацию полей для DRF.

Чтобы использовать `DjangoFilterBackend`, сначала установите `django-filter`.

```bash
pip install django-filter
```

Затем добавьте `'django_filters'` в `INSTALLED_APPS` Django:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

Теперь необходимо либо добавить бэкэнд фильтра в настройки:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Или добавить бэкэнд фильтрации в отдельный `View` или `ViewSet`.

```python
from django_filters.rest_framework import DjangoFilterBackend

class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]
```

Если вам нужна простая фильтрация на основе равенства, вы можете установить атрибут `filterset_fields` для представления или набора представлений, перечислив набор полей, по которым вы хотите осуществлять фильтрацию.

```python
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']
```

Это автоматически создаст класс `FilterSet` для заданных полей и позволит выполнять такие запросы, как:

```bash
http://example.com/api/products?category=clothing&in_stock=True
```

Для более сложных требований к фильтрации можно указать класс `FilterSet`, который должен использоваться представлением. Более подробно о `FilterSet` можно прочитать в [документации django-filter](https://django-filter.readthedocs.io/en/latest/index.html). Также рекомендуется прочитать раздел [Интеграция DRF](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

## SearchFilter

Класс `SearchFilter` поддерживает простой поиск по одному параметру запроса и основан на функциональности [поиска в админ-панели Django](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

При использовании в состав Web-интерфейса API будет входить элемент управления `SearchFilter`:

![Фильтр поиска](https://github.com/encode/django-rest-framework/raw/main/docs/img/search-filter.png)

Класс `SearchFilter` будет применяться только в том случае, если у представления установлен атрибут `search_fields`. Атрибут `search_fields` должен представлять собой список имен полей текстового типа в модели, например `CharField` или `TextField`.

```python
from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
```

Это позволит клиенту фильтровать элементы списка, задавая такие запросы, как:

```bash
http://example.com/api/users?search=russell
```

Также можно выполнить связанный поиск по полю `ForeignKey` или `ManyToManyField` с помощью нотации двойного подчеркивания в API поиска:

```python
search_fields = ['username', 'email', 'profile__profession']
```

Для полей [JSONField](https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.JSONField) и [HStoreField](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/fields/#hstorefield) можно осуществлять фильтрацию по вложенным значениям внутри структуры данных, используя ту же нотацию двойного подчеркивания:

```python
search_fields = ['data__breed', 'data__owner__other_pets__0__name']
```

По умолчанию в поиске используются частичные совпадения без учета регистра. Параметр `search` может содержать несколько условий поиска, которые должны быть разделены пробелами и/или запятыми. Если используется несколько условий поиска, то объекты будут возвращены в списке только при совпадении всех указанных условий. Поиск может содержать _цитируемые фразы_ с пробелами, каждая фраза рассматривается как один поисковый термин.

Поведение поиска может быть задано путем добавления префикса к именам полей в `search_fields` одним из следующих символов (что эквивалентно добавлению `__<lookup>` к полю):

| Префикс | Поиск         |                                                                                                                                                                   |
|---------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `^`     | `istartswith` | Начинается с поиска.                                                                                                                                              |
| `=`     | `iexact`      | Точные совпадения.                                                                                                                                                |
| `$`     | `iregex`      | Regex-поиск.                                                                                                                                                      |
| `@`     | `search`      | Полнотекстовый поиск (в настоящее время поддерживается только бэкенд Django [PostgreSQL](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/)). |
| None    | `icontains`   | Содержит поиск (по умолчанию).                                                                                                                                    |

Например:

```python
search_fields = ['=username', '=email']
```

По умолчанию параметр поиска называется `'search'`, но это можно переопределить с помощью параметра `SEARCH_PARAM`.

Для динамического изменения полей поиска в зависимости от содержимого запроса можно подклассифицировать `SearchFilter` и переопределить функцию `get_search_fields()`. Например, следующий подкласс будет искать по `title`, только если в запросе присутствует параметр запроса `title_only`:

```python
from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)
```

Более подробную информацию можно найти в [документации Django](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

---

## OrderingFilter

Класс `OrderingFilter` поддерживает простое упорядочивание результатов, управляемое параметрами запроса.

![Ordering Filter](https://github.com/encode/django-rest-framework/raw/main/docs/img/ordering-filter.png)

По умолчанию параметр запроса называется `'ordering'`, но это можно переопределить с помощью параметра `ORDERING_PARAM`.

Например, чтобы упорядочить пользователей по имени пользователя:

```bash
http://example.com/api/users?ordering=username
```

Клиент может задать и обратный порядок, добавив к имени поля префикс '-', например, так:

```bash
http://example.com/api/users?ordering=-username
```

Также может быть задано несколько порядков:

```bash
http://example.com/api/users?ordering=account,username
```

### Указание того, какие поля могут быть использованы для упорядочивания

Рекомендуется явно указывать, какие поля API должен разрешать в фильтре упорядочивания. Это можно сделать, установив атрибут `ordering_fields` на представлении, например, так:

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
```

Это позволяет предотвратить непредвиденную утечку данных, например, разрешить пользователям заказывать по хэш-полю пароли или другие конфиденциальные данные.

Если _не_ указать атрибут `orderering_fields` для представления, то класс фильтра будет по умолчанию позволять пользователю фильтровать по любым читаемым полям на сериализаторе, указанном атрибутом `serializer_class`.

Если вы уверены, что используемый представлением `Queryset` не содержит конфиденциальных данных, вы также можете явно указать, что представление должно разрешать упорядочивание по _любому_ полю модели или агрегату `Queryset`, используя специальное значение `'__all__'`.

```python
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
```

### Указание порядка по умолчанию

Если у представления установлен атрибут `ordering`, то он будет использоваться в качестве упорядочивания по умолчанию.

Обычно для этого используется параметр `order_by` в исходном `Queryset`, но использование параметра `ordering` в представлении позволяет указать порядок таким образом, что он может быть автоматически передан в качестве контекста в шаблон рендеринга. Это позволяет автоматически отображать заголовки столбцов по-разному, если они используются для упорядочивания результатов.

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
```

Атрибут `orderering` может быть как строкой, так и списком/кортежем строк.

---

# Пользовательская общая фильтрация

Вы также можете предоставить свой собственный бэкэнд фильтрации или написать устанавливаемое приложение для использования другими разработчиками.

Для этого переопределите `BaseFilterBackend` и переопределите метод `.filter_queryset(self, request, queryset, view)`. Метод должен возвращать новый, отфильтрованный `QuerySet`.

Помимо того, что клиенты могут выполнять поиск и фильтрацию, общие бэкенды фильтров могут быть полезны для ограничения того, какие объекты должны быть видны для каждого конкретного запроса или пользователя.

## Пример

Например, может потребоваться ограничить доступ пользователей только к созданным ими объектам.

```python
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

Мы могли бы добиться такого же поведения, переопределив `get_queryset()` в представлениях, но использование бэкенда фильтров позволяет более просто добавить это ограничение к нескольким представлениям или применить его ко всему API.

## Настройка интерфейса

Общие фильтры также могут представлять интерфейс в Web-интерфейсе API. Для этого необходимо реализовать метод `to_html()`, который возвращает отрендеренное HTML-представление фильтра. Этот метод должен иметь следующую сигнатуру:

`to_html(self, request, queryset, view)`.

Метод должен возвращать отрендеренную HTML-строку.

# Пакеты сторонних производителей

Следующие пакеты сторонних производителей предоставляют дополнительные реализации фильтров.

## Django-rest-framework-filters

[django-rest-framework-filters](https://github.com/philipn/django-rest-framework-filters) работает совместно с классом `DjangoFilterBackend` и позволяет легко создавать фильтры по отношениям, а также создавать несколько типов фильтров для поиска по заданному полю.

## Djangorestframework-word-filter

[djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter) разработан как альтернатива `filters.SearchFilter`, который будет искать полное слово в тексте, либо точное совпадение.

## Django-url-filter

[django-url-filter](https://github.com/miki725/django-url-filter) предоставляет безопасный способ фильтрации данных по удобным для человека URL-адресам. Он работает очень похоже на сериализаторы и поля DRF в том смысле, что они могут быть вложенными, за исключением того, что они называются `filtersets` и `filters`. Это обеспечивает простой способ фильтрации связанных данных. Кроме того, эта библиотека является универсальной, поэтому ее можно использовать для фильтрации других источников данных, а не только Django `QuerySet`.

## drf-url-filters

[drf-url-filter](https://github.com/manjitkumar/drf-url-filters) - это простое Django-приложение для применения фильтров к `Queryset` в `ModelViewSet` чистым, простым и настраиваемым способом. Оно также поддерживает валидацию входящих параметров запроса и их значений. Для валидации входящих параметров запроса используется красивый python-пакет `Voluptuous`. Самое приятное в `Voluptuous` то, что вы можете определить свои собственные валидации в соответствии с требованиями к параметрам запроса.
