<!-- TRANSLATED by md-translate -->
# ViewSets

> После того, как маршрутизация определила, какой контроллер использовать для запроса, ваш контроллер отвечает за осмысление запроса и создание соответствующего вывода.
>
> - [Ruby on Rails Documentation](https://guides.rubyonrails.org/action_controller_overview.html)

DRF позволяет объединить логику для набора связанных представлений в одном классе, называемом `ViewSet`. В других фреймворках вы также можете найти концептуально похожие реализации, названные, например, "Ресурсы" или "Контроллеры".

Класс `ViewSet` - это просто ** тип представления на основе класса, который не предоставляет никаких обработчиков методов**, таких как `.get()` или `.post()`, и вместо этого предоставляет такие действия, как `.list()` и `.create()`.

Обработчики методов для `ViewSet` привязываются к соответствующим действиям только в момент финализации представления, используя метод `.as_view()`.

Обычно вместо явной регистрации представлений в наборе представлений в urlconf, вы регистрируете набор представлений в классе маршрутизатора, который автоматически определяет urlconf для вас.

## Пример

Давайте определим простой набор представлений, который можно использовать для перечисления или извлечения всех пользователей в системе.

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

Если нужно, мы можем разделить этот набор представлений на два отдельных представления, например, так:

```python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

Обычно мы не делаем этого, а вместо этого регистрируем набор представлений в маршрутизаторе и позволяем автоматически генерировать urlconf.

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

Вместо того чтобы писать свои собственные наборы представлений, вы часто захотите использовать существующие базовые классы, которые предоставляют набор поведения по умолчанию. Например:

```python
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

Есть два основных преимущества использования класса `ViewSet` вместо класса `View`.

* Повторяющаяся логика может быть объединена в один класс. В приведенном выше примере нам нужно указать `queryset` только один раз, и он будет использоваться в нескольких представлениях.
* Используя маршрутизаторы, нам больше не нужно самим создавать URL conf.

В обоих случаях приходится идти на компромисс. Использование обычных представлений и URL-конфигураций является более явным и дает вам больше контроля. Наборы представлений полезны, если вы хотите быстро приступить к работе, или если у вас большой API и вы хотите обеспечить согласованную конфигурацию URL.

## Действия ViewSet

Маршрутизаторы по умолчанию, входящие в состав DRF, обеспечивают маршруты для стандартного набора действий в стиле create/retrieve/update/destroy, как показано ниже:

```python
class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
```

## Интроспекция действий ViewSet

Во время диспетчеризации для `ViewSet` доступны следующие атрибуты.

* `basename` - основа, которую следует использовать для создаваемых имен URL.
* `action` - имя текущего действия (например, `list`, `create`).
* `detail` - булево значение, указывающее, настроено ли текущее действие на просмотр списка или деталей.
* `suffix` - суффикс отображения для типа набора представлений - зеркальное отражение атрибута `detail`.
* `name` - отображаемое имя для набора представлений. Этот аргумент является взаимоисключающим с `suffix`.
* `description` - отображаемое описание для отдельного вида набора представлений.

Вы можете проверить эти атрибуты, чтобы настроить поведение в зависимости от текущего действия. Например, вы можете ограничить разрешения на все действия, кроме действия `list`, подобно этому:

```python
def get_permissions(self):
    """
    Instantiates and returns the list of permissions that this view requires.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]
```

## Добавление дополнительных действий в маршрутизацию

Если у вас есть специальные методы, которые должны быть маршрутизируемыми, вы можете пометить их как таковые с помощью декоратора `@action`. Как и обычные действия, дополнительные действия могут быть предназначены как для одного объекта, так и для целой коллекции. Чтобы указать это, установите аргумент `detail` в `True` или `False`. Маршрутизатор настроит свои шаблоны URL соответствующим образом. Например, `DefaultRouter` настроит подробные действия так, чтобы они содержали `pk` в своих шаблонах URL.

Более полный пример дополнительных действий:

```python
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
```

Декоратор `action` по умолчанию направляет запросы `GET`, но может принимать и другие методы HTTP, задавая аргумент `methods`. Например:

```python
@action(detail=True, methods=['post', 'delete'])
def unset_password(self, request, pk=None):
    ...
```

Декоратор позволяет переопределить любую конфигурацию уровня набора представлений, такую как `permission_classes`, `serializer_class`, `filter_backends`...:

```python
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
def set_password(self, request, pk=None):
    ...
```

Два новых действия будут доступны по адресам `^users/{pk}/set_password/$` и `^users/{pk}/unset_password/$`. Используйте параметры `url_path` и `url_name` для изменения сегмента URL и обратного имени URL действия.

Чтобы просмотреть все дополнительные действия, вызовите метод `.get_extra_actions()`.

### Маршрутизация дополнительных методов HTTP для дополнительных действий

Дополнительные действия могут отображать дополнительные методы HTTP на отдельные методы `ViewSet`. Например, описанные выше методы установки/снятия пароля могут быть объединены в один маршрут. Обратите внимание, что дополнительные сопоставления не принимают аргументов.

```python
@action(detail=True, methods=['put'], name='Change Password')
def password(self, request, pk=None):
    """Update the user's password."""
    ...

@password.mapping.delete
def delete_password(self, request, pk=None):
    """Delete the user's password."""
    ...
```

## URL-адреса обратного действия

Если вам нужно получить URL действия, используйте метод `.reverse_action()`. Это удобная обертка для `reverse()`, автоматически передающая объект `request` представления и дополняющая `url_name` атрибутом `.basename`.

Обратите внимание, что `basename` предоставляется маршрутизатором во время регистрации `ViewSet`. Если вы не используете маршрутизатор, то вы должны предоставить аргумент `basename` методу `.as_view()`.

Используя пример из предыдущего раздела:

```python
>>> view.reverse_action('set-password', args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

В качестве альтернативы можно использовать атрибут `url_name`, установленный декоратором `@action`.

```python
>>> view.reverse_action(view.set_password.url_name, args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

Аргумент `url_name` для `.reverse_action()` должен совпадать с тем же аргументом декоратора `@action`. Кроме того, этот метод можно использовать для отмены действий по умолчанию, таких как `list` и `create`.

---

# API Reference

## ViewSet

Класс `ViewSet` наследуется от `APIView`. Вы можете использовать любые стандартные атрибуты, такие как `permission_classes`, `authentication_classes` для управления политикой API на наборе представлений.

Класс `ViewSet` не предоставляет никаких реализаций действий. Чтобы использовать класс `ViewSet`, вы должны переопределить его и явно определить реализацию действий.

## GenericViewSet

Класс `GenericViewSet` наследуется от `GenericAPIView`, и предоставляет набор методов `get_object`, `get_queryset` и другое поведение базы generic view по умолчанию, но не включает никаких действий по умолчанию.

Чтобы использовать класс `GenericViewSet`, вы должны переопределить его и либо смешать необходимые классы mixin, либо явно определить реализацию действий.

## ModelViewSet

Класс `ModelViewSet` наследуется от `GenericAPIView` и включает в себя реализации различных действий, смешивая поведение различных классов mixin.

Действия, предоставляемые классом `ModelViewSet`: `.list()`, `.retrieve()`, `.create()`, `.update()`, `.partial_update()` и `.destroy()`.

#### Пример

Поскольку `ModelViewSet` расширяет `GenericAPIView`, вам обычно необходимо предоставить как минимум атрибуты `queryset` и `serializer_class`. Например:

```python
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```

Обратите внимание, что вы можете использовать любой из стандартных атрибутов или переопределений методов, предоставляемых `GenericAPIView`. Например, чтобы использовать `ViewSet`, который динамически определяет набор запросов, с которым он должен работать, вы можете поступить следующим образом:

```python
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()
```

Однако обратите внимание, что после удаления свойства `queryset` из вашего `ViewSet`, любой связанный с ним [router](routers.md) не сможет автоматически вывести базовое имя вашей Модели, поэтому вам придется указать именованный аргумент `basename` как часть вашей регистрации [router](routers.md).

Также обратите внимание, что хотя этот класс по умолчанию предоставляет полный набор действий create/list/retrieve/update/destroy, вы можете ограничить доступные операции с помощью стандартных классов разрешений.

## ReadOnlyModelViewSet

Класс `ReadOnlyModelViewSet` также наследуется от `GenericAPIView`. Как и `ModelViewSet`, он также включает реализации различных действий, но в отличие от `ModelViewSet` предоставляет только действия "только для чтения", `.list()` и `.retrieve()`.

#### Пример

Как и в случае с `ModelViewSet`, обычно требуется предоставить как минимум атрибуты `queryset` и `serializer_class`. Например:

```python
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
```

Опять же, как и в случае с `ModelViewSet`, вы можете использовать любые стандартные атрибуты и переопределения методов, доступные для `GenericAPIView`.

# Пользовательские базовые классы ViewSet

Вам может понадобиться предоставить пользовательские классы `ViewSet`, которые не имеют полного набора действий `ModelViewSet`, или которые настраивают поведение каким-либо другим способом.

## Пример

Чтобы создать базовый класс набора представлений, обеспечивающий операции `create`, `list` и `retrieve`, наследуйте от `GenericViewSet` и добавьте необходимые действия:

```python
from rest_framework import mixins

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass
```

Создавая свои собственные базовые классы `ViewSet`, вы можете обеспечить общее поведение, которое может быть повторно использовано в нескольких наборах представлений в вашем API.
