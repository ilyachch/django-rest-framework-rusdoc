# ViewSets
> Для запроса определяется контролер, и он отвечает за обработку запроса и выдает нужный результат.

— Документация Ruby on Rails


Django REST framework позволяет комбинировать логику для набора связанных представлений в одном классе, который назвается ViewSet. В других фреймворках вы также можете встретить похожие концепции под названием 'Resources' или 'Controllers'.
Класс ViewSet это просто представление-класс, которое не используеи никаких методов обработки, как `.get()` или `.post()`, а вместо этого включает действия `.list()` и `.create()`.
Обработчики метода для ViewSet связаны только для соответствующих действий на моменте окончательной обработке представления, используя метод `.as_view()`.
Как правило, вместо того, чтобы подробно регистрировать представления в viewset в urlconf, вы регистрируете viewset в классе маршрутизатора, который автоматически определяет для вас urlconf.

## Пример
Давайте определим простой viewset, который может быть использован для перечисления или поиска всех пользователей в системе.

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

В случае необходимости мы можем связать этот viewset с двумя отдельными представлениями:

```python

user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```
Как правило, вместо этого мы регистрируем viewset в маршрутизаторе и разрешаем автоматическое создание urlconf.

```python

from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
urlpatterns = router.urls
```
Вместо того, чтобы писать собственные viewset'ы, чаще рациональнее использовать существующие базовые классы, которые описывают стандартное поведение. Например:

```python

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```
Класс `ViewSet` дает два главных преимущества перед классом `View`.

* Можно заключить неоднократно повторяющуюся логику в один класс. Выше нам потребовалось лишь один раз уточнить queryset, и после этого он будет использоваться во множестве представлений.
* Используя маршрутизаторы нам больше не нужно самим писать URL conf.
Однако эти плюсы несут свои компромиссы. Использование обычных представлений и URL confs более очевидно и предоставляет больше контроля. ViewSets полезны если вы хотите, чтобы все заработало как можно быстрее, или когда у вас большой API, и вам требуется обеспечить равномерную конфигурацию URL во всем проекте.

## Дополнительные действия для маршрутизации

Средства REST framework предоставляют маршрутизаторы для стандартных операций create/retrieve/update/destroy, как показано ниже:

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
Если у вас есть специальные методы ad-hoc, вы можете отметить их как требующими маршрутизации, используя декораторы `@detail_route` или `@list_route`.
Декоратор `@detail_route` содержит `pk` в своем URL паттерне и предназначается для методов, которые требуют один экземпляр. Декоратор `@list_route` предназначен для методов, которые взаимодейстуют со списками объектов.


Например:
```python

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def recent_users(self, request):
        recent_users = User.objects.all().order('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
```
К тому же декораторы могут принимать дополнительные аргументы, которые будут указываться только для маршрутизированных представлений. Например...

`!!!!!The decorators can additionally take extra arguments that will be set for the routed view only. For example...!!!!!`

```python
    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
       ...
```
Эти декораторы будут маршутизировать `GET` запросы по умолчанию, но также могут принимать другие методы HTTP с помощью методов аргрумента. Например:
```python
    @detail_route(methods=['post', 'delete'])
    def unset_password(self, request, pk=None):
       ...
```
Два новых действия будут доступны по urls `^users/{pk}/set_password/$` и `^users/{pk}/unset_password/$`

# Обращение к API
## ViewSet

Класс `ViewSet` наследуется от APIView. Вы можете использовать любой из стандартных атрибутов, такие как `permission_classes`, `authentication_classes`, чтобы контролировать поведение API в viewset.
Класс `ViewSet`не реализует действия. Для того чтобы воспользоваться классом `ViewSet` нужно переписать класс и  расписать действия.

## GenericViewSet

Класс `GenericViewSet` наследуется от `GenericAPIView` и предоставляет стандартный набо методов `get_object`, `get_queryset` и другие общие механизмы поведения педставления, но при этом не реализует их.

Для того, чтобы использовать `GenericViewSet` вам нужно переписать класс и, либо создать миксины требуемых классов, либо явно определить реализацию действий.

## ModelViewSet
Класс `ModelViewSet` наследуется от `GenericAPIView` и реализует различные действия, совмещая функционал различных классов миксинов.
Класс `ModelViewSet` предоставляет следующие действия `.list()`, `.retrieve()`, `.create()`, `.update()`, `.partial_update()`, и `.destroy()`.

### Пример
Так как `ModelViewSet`расширяет `GenericAPIView` вам по меньшей мере нужно предоставить по крайней мере queryset и атрибуты `serializer_class`. Например:

```python
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```

Вы можете использовать стандартные атрибуты или подменять методы, предоставленные `GenericAPIView`. Например, чтобы использовать `ViewSet`, который динамически определяет queryset, вы можете сделать следующее:
```python

class AccountViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet для просмотра и редактирования
    аккаунтов, привязанных к пользователю
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()
```

Однако заметьте, что при удалении свойства queryset из вышего `ViewSet` любой связанный `маршрутизатор` не сможет автоматически выделить base_name вашей модели, таким образом вам придется указать kwarg для `base_name` при регистрации роутера.
Также заметьте, что хоть этот класс и реализует по умолчанию  полный набор действий create/list/retrieve/update/destroy, вы можете ограничить доступный функционал, используя стандартные разрешающие классы. 

## ReadOnlyModelViewSet
Класс `ReadOnlyModelViewSet` также наследуется от `GenericAPIView`. Как и в слчае с `ModelViewSet` он также реализует различные действия, но в отличие от `ModelViewSet` ограничивается лишь функционалом 'только для чтения' `.list()` и `.retrieve()`.

### Пример
Как и при использовании `ModelViewSet`, вам как минимум нужно предоставить queryset и атрибуты `serializer_class`

Например:

```python

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Простой ViewSet для просмотра аккунтов.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
```
Вновь, как и в случае с `ModelViewSet` вы можете использовать стандартне атрибуты и замены методов, доступные в 
GenericAPIView
`!!!!!!!!!!!!Again, as with ModelViewSet, you can use any of the standard attributes and method overrides available to GenericAPIView.!!!!!!!!!!!!!`



## Кастомые базовые классы ViewSet
Возможно вам понадобится использоваться кастомными классами, которые не реализуют весь набор действий `ModelViewSet`, или каким-то образом изменяют поведение.

### Пример

Чтобы создать базовый класс viewset, который реализует действия create, list и retrieve, наследуется от `GenericViewSet` и создает миксины для требуемых действий:

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
Создавая собственные базовые классы ViewSet, вы можете реализовать общее поведение, которое может быть повторно использовано в вашем API.