<!-- TRANSLATED by md-translate -->
# Представления, основанные на классах

> Представления Django, основанные на классах, являются приятным отступлением от представлений старого стиля.
>
> - [Reinout van Rees](https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-usage.html)

DRF предоставляет класс `APIView`, который является подклассом класса Django `View`.

Классы `APIView` отличаются от обычных классов `View` следующим образом:

* Запросы, передаваемые методам обработчика, будут экземплярами `Request` DRF, а не экземплярами `HttpRequest` Django.
* Методы обработчика могут возвращать `Response` DRF, а не `HttpResponse` Django. Представление будет управлять согласованием содержимого и установкой правильного рендерера в ответе.
* Любые исключения `APIException` будут перехвачены и переведены в соответствующие ответы.
* Входящие запросы будут аутентифицированы, и перед отправкой запроса в метод-обработчик будут выполняться соответствующие проверки разрешений и/или дросселирования.

Использование класса `APIView` практически не отличается от использования обычного класса `View`. Как обычно, входящий запрос передается соответствующему методу-обработчику, такому как `.get()` или `.post()`. Кроме того, для класса может быть установлен ряд атрибутов, которые контролируют различные аспекты политики API.

Например:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```

---

**Примечание**: Полные методы, атрибуты и отношения между `APIView`, `GenericAPIView`, различными `Mixins` и `Viewsets` DRF могут быть изначально сложными. В дополнение к документации, представленной здесь, ресурс [Classy Django REST Framework](http://www.cdrf.co) предоставляет просматриваемую ссылку с полными методами и атрибутами для каждого из представлений DRF, основанных на классах.

---

## Атрибуты политики API

Следующие атрибуты управляют подключаемыми аспектами представлений API.

### .renderer_classes

### .parser_classes

### .authentication_classes

### .throttle_classes

### .permission_classes

### .content_negotiation_class

## Методы инстанцирования политики API

Следующие методы используются DRF для инстанцирования различных подключаемых политик API. Как правило, вам не нужно переопределять эти методы.

### .get_renderers(self)

### .get_parsers(self)

### .get_authenticators(self)

### .get_throttles(self)

### .get_permissions(self)

### .get_content_negotiator(self)

### .get_exception_handler(self)

## Методы реализации политики API

Перед отправкой в метод обработчика вызываются следующие методы.

### .check_permissions(self, request)

### .check_throttles(self, request)

### .perform_content_negotiation(self, request, force=False)

## Dispatch методы

Следующие методы вызываются непосредственно методом `.dispatch()` представления. Они выполняют любые действия, которые должны произойти до или после вызова методов обработчика, таких как `.get()`, `.post()`, `put()`, `patch()` и `.delete()`.

### .initial(self, request, *args, **kwargs)

Выполняет любые действия, которые должны произойти до вызова метода обработчика. Этот метод используется для обеспечения разрешений и дросселирования, а также для согласования содержимого.

Обычно вам не нужно переопределять этот метод.

### .handle_exception(self, exc)

Любое исключение, выброшенное методом обработчика, будет передано в этот метод, который либо возвращает экземпляр `Response`, либо повторно вызывает исключение.

Реализация по умолчанию обрабатывает любой подкласс `rest_framework.exceptions.APIException`, а также исключения Django `Http404` и `PermissionDenied`, и возвращает соответствующий ответ об ошибке.

Если вам нужно настроить ответы на ошибки, которые возвращает ваш API, вам следует подклассифицировать этот метод.

### .initialize_request(self, request, *args, **kwargs)

Гарантирует, что объект запроса, передаваемый методу обработчика, является экземпляром `Request`, а не обычным Django `HttpRequest`.

Обычно вам не нужно переопределять этот метод.

### .finalize_response(self, request, response, *args, **kwargs)

Гарантирует, что любой объект `Response`, возвращенный из метода обработчика, будет преобразован в правильный тип содержимого, как определено в процессе согласования содержимого.

Обычно вам не нужно переопределять этот метод.

---

# Представления на основе функций

> Говорить [что представления, основанные на классах] всегда являются лучшим решением - это ошибка.
>
> - [Nick Coghlan](http://www.boredomandlaziness.org/2012/05/djangos-cbvs-are-not-mistake-but.html)

DRF также позволяет работать с обычными представлениями, основанными на функциях. Он предоставляет набор простых декораторов, которые оборачивают ваши представления на основе функций, чтобы они получали экземпляр `Request` (а не обычный Django `HttpRequest`) и позволяли им возвращать `Response` (а не Django `HttpResponse`), а также позволяют вам настраивать, как обрабатывается запрос.

## @api_view()

**Сигнатура:** `@api_view(http_method_names=['GET'])`.

Ядром этой функциональности является декоратор `api_view`, который принимает список методов HTTP, на которые должно отвечать ваше представление. Например, вот как можно написать очень простое представление, которое просто вручную возвращает некоторые данные:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

Это представление будет использовать рендереры по умолчанию, парсеры, классы аутентификации и т.д., указанные в [settings](settings.md).

По умолчанию принимаются только методы `GET`. Другие методы будут отвечать "405 Method Not Allowed". Чтобы изменить это поведение, укажите, какие методы разрешены представлению, например, так:

```python
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})
```

## Декораторы политики API

Чтобы переопределить настройки по умолчанию, DRF предоставляет набор дополнительных декораторов, которые можно добавить к вашим представлениям. Они должны быть *после* (ниже) декоратора `@api_view`. Например, чтобы создать представление, которое использует [throttle](throttling.md) для обеспечения того, что оно может быть вызвано только один раз в день определенным пользователем, используйте декоратор `@throttle_classes`, передавая список классов throttle:

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

Эти декораторы соответствуют атрибутам, установленным на подклассах `APIView`, описанных выше.

Доступными декораторами являются:

* `@renderer_classes(...)`
* `@parser_classes(...)`
* `@authentication_classes(...)`
* `@throttle_classes(...)`
* `@permission_classes(...)`
* `@content_negotiation_class(...)`
* `@metadata_class(...)`
* `@versioning_class(...)`

Каждый из этих декораторов эквивалентен установке соответствующих [атрибутов политики API](#атрибуты-политики-api).

Все декораторы принимают один аргумент. Те, которые заканчиваются на `_class`, ожидают один класс, а те, которые заканчиваются на `_classes`, ожидают список или кортеж классов.
## Декоратор схемы представления

Чтобы переопределить генерацию схемы по умолчанию для представлений на основе функций, вы можете использовать декоратор `@schema`. Он должен располагаться *после* (ниже) декоратора `@api_view`. Например:

```python
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema

class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        # override view introspection here...

@api_view(['GET'])
@schema(CustomAutoSchema())
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

Этот декоратор принимает экземпляр `AutoSchema`, экземпляр подкласса `AutoSchema` или экземпляр `ManualSchema`, как описано в документации [Schemas documentation](schemas.md). Вы можете передать `None`, чтобы исключить представление из генерации схемы.

```python
@api_view(['GET'])
@schema(None)
def view(request):
    return Response({"message": "Will not appear in schema!"})
```
