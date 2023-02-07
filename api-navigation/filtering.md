<!-- TRANSLATED by md-translate -->
# Фильтрация

> Корневой набор запросов, предоставляемый менеджером, описывает все объекты в таблице базы данных. Обычно, однако, вам нужно выбрать только подмножество полного набора объектов.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters)

Стандартным поведением общих представлений списка в DRF является возврат всего набора запросов для менеджера модели. Часто вы хотите, чтобы ваш API ограничивал элементы, возвращаемые набором запросов.

Самый простой способ фильтрации набора запросов любого представления, подкласса `GenericAPIView`, - переопределить метод `.get_queryset()`.

Переопределение этого метода позволяет вам настраивать набор запросов, возвращаемый представлением, различными способами.

## Фильтрация по текущему пользователю

Вы можете захотеть отфильтровать набор запросов, чтобы гарантировать, что будут возвращены только результаты, относящиеся к текущему аутентифицированному пользователю, сделавшему запрос.

Это можно сделать с помощью фильтрации на основе значения `request.user`.

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

Другой стиль фильтрации может включать ограничение набора запросов на основе некоторой части URL.

Например, если ваша конфигурация URL содержит такую запись:

```python
re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
```

Затем вы можете написать представление, которое возвращает набор запросов на покупку, отфильтрованный по имени пользователя в части URL:

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

Последним примером фильтрации начального набора запросов может быть определение начального набора запросов на основе параметров запроса в url.

Мы можем переопределить `.get_queryset()` для работы с URL, такими как `http://example.com/api/purchases?username=denvercoder9`, и фильтровать набор запросов, только если параметр `username` включен в URL:

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

Помимо возможности переопределения набора запросов по умолчанию, DRF также включает поддержку общих бэкендов фильтрации, которые позволяют легко создавать сложные поиски и фильтры.

Общие фильтры также могут быть представлены в виде элементов управления HTML в просматриваемом API и API администратора.

![Пример фильтра](https://github.com/encode/django-rest-framework/raw/master/docs/img/filter-controls.png)

## Настройка бэкендов фильтров

Бэкенды фильтров по умолчанию можно установить глобально, используя параметр `DEFAULT_FILTER_BACKENDS`. Например.

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Вы также можете установить бэкенды фильтров на основе каждого представления или каждого набора представлений, используя представления на основе класса `GenericAPIView`.

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

Обратите внимание, что если бэкэнд фильтра настроен для представления, то помимо того, что он используется для фильтрации представлений списка, он также будет использоваться для фильтрации наборов запросов, используемых для возврата одного объекта.

Например, учитывая предыдущий пример и продукт с id `4675`, следующий URL либо вернет соответствующий объект, либо выдаст ответ 404, в зависимости от того, были ли выполнены условия фильтрации для данного экземпляра продукта:

```
http://example.com/api/products/4675/?category=clothing&max_price=10.00
```

## Переопределение начального набора запросов

Обратите внимание, что вы можете использовать и переопределенный `.get_queryset()`, и общую фильтрацию вместе, и все будет работать, как ожидалось. Например, если `Product` имеет отношение "многие-ко-многим" с `User`, названное `purchase`, вы можете написать представление следующим образом:

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

Библиотека [`django-filter`](https://django-filter.readthedocs.io/en/latest/index.html) включает класс `DjangoFilterBackend`, который поддерживает высоконастраиваемую фильтрацию полей для REST-фреймворка.

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

Теперь вам следует либо добавить бэкенд фильтра в настройки:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Или добавьте бэкэнд фильтра к отдельному представлению или набору представлений.

```python
from django_filters.rest_framework import DjangoFilterBackend

class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]
```

Если вам нужна простая фильтрация на основе равенства, вы можете установить атрибут `filterset_fields` для представления или набора представлений, перечислив набор полей, по которым вы хотите фильтровать.

```python
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']
```

Это автоматически создаст класс `FilterSet` для заданных полей и позволит вам делать такие запросы, как:

```
http://example.com/api/products?category=clothing&in_stock=True
```

Для более сложных требований к фильтрации вы можете указать класс `FilterSet`, который должен использоваться представлением. Подробнее о `FilterSet` вы можете прочитать в [документации по django-filter](https://django-filter.readthedocs.io/en/latest/index.html). Также рекомендуется прочитать раздел [Интеграция DRF](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html).

## SearchFilter

Класс `SearchFilter` поддерживает простой поиск по одному параметру запроса и основан на [Django admin's search functionality](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields).

При использовании API с возможностью просмотра будет включать элемент управления `SearchFilter`:

![Фильтр поиска](https://github.com/encode/django-rest-framework/raw/master/docs/img/search-filter.png)

Класс `SearchFilter` будет применяться, только если у представления установлен атрибут `search_fields`. Атрибут `search_fields` должен представлять собой список имен полей текстового типа в модели, таких как `CharField` или `TextField`.

```python
from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
```

Это позволит клиенту фильтровать элементы в списке, делая такие запросы, как:

```
http://example.com/api/users?search=russell
```

Вы также можете выполнить связанный поиск по полю ForeignKey или ManyToManyField с помощью нотации двойного неравенства API поиска:

```python
search_fields = ['username', 'email', 'profile__profession']
```

Для полей [JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield) и [HStoreField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#hstorefield) вы можете фильтровать на основе вложенных значений внутри структуры данных, используя ту же нотацию двойного ундеркорда:

```python
search_fields = ['data__breed', 'data__owner__other_pets__0__name']
```

По умолчанию при поиске используются частичные совпадения без учета регистра. Параметр поиска может содержать несколько условий поиска, которые должны быть разделены пробелами и/или запятыми. Если используется несколько условий поиска, то объекты будут возвращены в списке только в том случае, если совпадут все указанные условия.

Поведение поиска может быть ограничено путем добавления различных символов к `полям_поиска`.

* '^' Поиск с начала.
* '=' Точное совпадение.
* '@' Полнотекстовый поиск. (В настоящее время поддерживается только [PostgreSQL backend](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/) Django).
* '$' Регексный поиск.

Например:

```python
search_fields = ['=username', '=email']
```

По умолчанию параметр поиска называется `'search'', но его можно переопределить с помощью параметра `SEARCH_PARAM`.

Чтобы динамически изменять поля поиска на основе содержимого запроса, можно подклассифицировать `SearchFilter` и переопределить функцию `get_search_fields()`. Например, следующий подкласс будет искать только по `title`, если в запросе присутствует параметр запроса `title_only`:

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

![Ordering Filter](https://github.com/encode/django-rest-framework/raw/master/docs/img/ordering-filter.png)

По умолчанию параметр запроса называется `'ordering'', но его можно переопределить с помощью параметра `ORDERING_PARAM'.

Например, чтобы упорядочить пользователей по имени пользователя:

```
http://example.com/api/users?ordering=username
```

Клиент также может указать обратный порядок, добавив к имени поля префикс '-', как показано ниже:

```
http://example.com/api/users?ordering=-username
```

Также можно указать несколько порядков:

```
http://example.com/api/users?ordering=account,username
```

### Указание того, какие поля могут быть заказаны против

Рекомендуется явно указать, какие поля API должен разрешить в фильтре упорядочивания. Это можно сделать, установив атрибут `ordering_fields` для представления, как показано ниже:

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
```

Это помогает предотвратить непредвиденную утечку данных, например, разрешение пользователям делать заказы по хэш-полю пароля или других конфиденциальных данных.

Если вы *не* указали атрибут `orderering_fields` для представления, класс фильтра будет по умолчанию позволять пользователю фильтровать по любым читаемым полям на сериализаторе, указанном атрибутом `serializer_class`.

Если вы уверены, что кверисет, используемый представлением, не содержит конфиденциальных данных, вы также можете явно указать, что представление должно разрешить упорядочивание по *любому* полю модели или агрегату кверисета, используя специальное значение `'__all__'`.

```python
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
```

### Указание порядка по умолчанию

Если для представления установлен атрибут `ordering`, он будет использоваться в качестве упорядочивания по умолчанию.

Обычно вы контролируете это, устанавливая `order_by` в исходном наборе запросов, но использование параметра `ordering` в представлении позволяет вам указать порядок таким образом, что он может быть автоматически передан в качестве контекста шаблону рендеринга. Это позволяет автоматически отображать заголовки столбцов по-разному, если они используются для упорядочивания результатов.

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
```

Атрибут `orderering` может быть либо строкой, либо списком/кортежем строк.

---

# Пользовательская общая фильтрация

Вы также можете предоставить свой собственный общий бэкэнд фильтрации или написать устанавливаемое приложение для использования другими разработчиками.

Для этого переопределите `BaseFilterBackend` и переопределите метод `.filter_queryset(self, request, queryset, view)`. Метод должен возвращать новый, отфильтрованный набор запросов.

Помимо того, что клиенты могут выполнять поиск и фильтрацию, общие бэкенды фильтров могут быть полезны для ограничения того, какие объекты должны быть видны для каждого конкретного запроса или пользователя.

## Пример

Например, вам может понадобиться ограничить доступ пользователей только к созданным ими объектам.

```python
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

Мы могли бы добиться такого же поведения, переопределив `get_queryset()` в представлениях, но использование бэкенда фильтров позволяет вам легче добавить это ограничение к нескольким представлениям или применить его ко всему API.

## Настройка интерфейса

Общие фильтры также могут представлять интерфейс в просматриваемом API. Для этого необходимо реализовать метод `to_html()`, который возвращает отрисованное HTML-представление фильтра. Этот метод должен иметь следующую сигнатуру:

`to_html(self, request, queryset, view)`.

Метод должен возвращать отрендеренную строку HTML.

# Пакеты сторонних производителей

Следующие пакеты сторонних производителей предоставляют дополнительные реализации фильтров.

## Пакет фильтров фреймворка Django REST

Пакет [django-rest-framework-filters](https://github.com/philipn/django-rest-framework-filters) работает вместе с классом `DjangoFilterBackend` и позволяет вам легко создавать фильтры по отношениям или создавать несколько типов поиска фильтра для заданного поля.

## Django REST framework поиск по словам

[djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter) разработан как альтернатива `filters.SearchFilter`, который будет искать полное слово в тексте, или точное совпадение.

## Django URL Filter

[django-url-filter](https://github.com/miki725/django-url-filter) предоставляет безопасный способ фильтрации данных по удобным для человека URL. Он работает очень похоже на сериализаторы и поля DRF в том смысле, что они могут быть вложенными, за исключением того, что они называются filtersets и filters. Это обеспечивает простой способ фильтрации связанных данных. Также эта библиотека является универсальной, поэтому ее можно использовать для фильтрации других источников данных, а не только Django `QuerySet`.

## drf-url-filters

[drf-url-filter](https://github.com/manjitkumar/drf-url-filters) - это простое Django приложение для применения фильтров к drf `ModelViewSet` `Queryset` чистым, простым и настраиваемым способом. Оно также поддерживает валидацию входящих параметров запроса и их значений. Для проверки входящих параметров запроса используется красивый пакет python `Voluptuous`. Самое лучшее в voluptuous то, что вы можете определить свои собственные валидации в соответствии с требованиями к параметрам запроса.
