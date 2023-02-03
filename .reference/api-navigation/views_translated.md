<!-- TRANSLATED by md-translate -->
---

source:

источник:

* decorators.py
* views.py

* decorators.py
* views.py

---

# Class-based Views

# Представления, основанные на классах

> Django's class-based views are a welcome departure from the old-style views.
>
> — [Reinout van Rees](https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-usage.html)

> Представления Django, основанные на классах, являются приятным отступлением от представлений старого стиля.
>
> - [Reinout van Rees](https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-usage.html)

REST framework provides an `APIView` class, which subclasses Django's `View` class.

Фреймворк REST предоставляет класс `APIView`, который является подклассом класса Django `View`.

`APIView` classes are different from regular `View` classes in the following ways:

Классы `APIView` отличаются от обычных классов `View` следующим образом:

* Requests passed to the handler methods will be REST framework's `Request` instances, not Django's `HttpRequest` instances.
* Handler methods may return REST framework's `Response`, instead of Django's `HttpResponse`. The view will manage content negotiation and setting the correct renderer on the response.
* Any `APIException` exceptions will be caught and mediated into appropriate responses.
* Incoming requests will be authenticated and appropriate permission and/or throttle checks will be run before dispatching the request to the handler method.

* Запросы, передаваемые методам обработчика, будут экземплярами `Request` фреймворка REST, а не экземплярами `HttpRequest` Django.
* Методы обработчика могут возвращать `Response` фреймворка REST, а не `HttpResponse` Django. Представление будет управлять согласованием содержимого и установкой правильного рендеринга в ответе.
* Любые исключения `APIException` будут перехвачены и опосредованы в соответствующие ответы.
* Входящие запросы будут аутентифицированы, и перед отправкой запроса в метод-обработчик будут выполняться соответствующие проверки разрешений и/или дросселирования.

Using the `APIView` class is pretty much the same as using a regular `View` class, as usual, the incoming request is dispatched to an appropriate handler method such as `.get()` or `.post()`. Additionally, a number of attributes may be set on the class that control various aspects of the API policy.

Использование класса `APIView` практически не отличается от использования обычного класса `View`. Как обычно, входящий запрос передается соответствующему методу-обработчику, такому как `.get()` или `.post()`. Кроме того, для класса может быть установлен ряд атрибутов, которые контролируют различные аспекты политики API.

For example:

Например:

```
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

**Note**: The full methods, attributes on, and relations between Django REST Framework's `APIView`, `GenericAPIView`, various `Mixins`, and `Viewsets` can be initially complex. In addition to the documentation here, the [Classy Django REST Framework](http://www.cdrf.co) resource provides a browsable reference, with full methods and attributes, for each of Django REST Framework's class-based views.

**Примечание**: Полные методы, атрибуты и отношения между `APIView`, `GenericAPIView`, различными `Mixins` и `Viewsets` Django REST Framework могут быть изначально сложными. В дополнение к документации, представленной здесь, ресурс [Classy Django REST Framework](http://www.cdrf.co) предоставляет просматриваемую ссылку с полными методами и атрибутами для каждого из представлений Django REST Framework, основанных на классах.

---

## API policy attributes

## Атрибуты политики API

The following attributes control the pluggable aspects of API views.

Следующие атрибуты управляют подключаемыми аспектами представлений API.

### .renderer_classes

### .renderer_classes

### .parser_classes

### .parser_classes

### .authentication_classes

### .authentication_classes

### .throttle_classes

### .throttle_classes

### .permission_classes

### .permission_classes

### .content_negotiation_class

### .content_negotiation_class

## API policy instantiation methods

## Методы инстанцирования политики API

The following methods are used by REST framework to instantiate the various pluggable API policies. You won't typically need to override these methods.

Следующие методы используются каркасом REST для инстанцирования различных подключаемых политик API. Как правило, вам не нужно переопределять эти методы.

### .get_renderers(self)

### .get_renderers(self)

### .get_parsers(self)

### .get_parsers(self)

### .get_authenticators(self)

### .get_authenticators(self)

### .get_throttles(self)

### .get_throttles(self)

### .get_permissions(self)

### .get_permissions(self)

### .get_content_negotiator(self)

### .get_content_negotiator(self)

### .get_exception_handler(self)

### .get_exception_handler(self)

## API policy implementation methods

## Методы реализации политики API

The following methods are called before dispatching to the handler method.

Перед отправкой в метод обработчика вызываются следующие методы.

### .check_permissions(self, request)

### .check_permissions(self, request)

### .check_throttles(self, request)

### .check_throttles(self, request)

### .perform_content_negotiation(self, request, force=False)

### .perform_content_negotiation(self, request, force=False)

## Dispatch methods

## Диспетчерские методы

The following methods are called directly by the view's `.dispatch()` method. These perform any actions that need to occur before or after calling the handler methods such as `.get()`, `.post()`, `put()`, `patch()` and `.delete()`.

Следующие методы вызываются непосредственно методом `.dispatch()` представления. Они выполняют любые действия, которые должны произойти до или после вызова методов обработчика, таких как `.get()`, `.post()`, `put()`, `patch()` и `.delete()`.

### .initial(self, request, *args, **kwargs)

### .initial(self, request, *args, **kwargs)

Performs any actions that need to occur before the handler method gets called. This method is used to enforce permissions and throttling, and perform content negotiation.

Выполняет любые действия, которые должны произойти до вызова метода обработчика. Этот метод используется для обеспечения разрешений и дросселирования, а также для согласования содержимого.

You won't typically need to override this method.

Обычно вам не нужно переопределять этот метод.

### .handle_exception(self, exc)

### .handle_exception(self, exc)

Any exception thrown by the handler method will be passed to this method, which either returns a `Response` instance, or re-raises the exception.

Любое исключение, выброшенное методом обработчика, будет передано в этот метод, который либо возвращает экземпляр `Response`, либо повторно вызывает исключение.

The default implementation handles any subclass of `rest_framework.exceptions.APIException`, as well as Django's `Http404` and `PermissionDenied` exceptions, and returns an appropriate error response.

Реализация по умолчанию обрабатывает любой подкласс `rest_framework.exceptions.APIException`, а также исключения Django `Http404` и `PermissionDenied`, и возвращает соответствующий ответ об ошибке.

If you need to customize the error responses your API returns you should subclass this method.

Если вам нужно настроить ответы на ошибки, которые возвращает ваш API, вам следует подклассифицировать этот метод.

### .initialize_request(self, request, *args, **kwargs)

### .initialize_request(self, request, *args, **kwargs)

Ensures that the request object that is passed to the handler method is an instance of `Request`, rather than the usual Django `HttpRequest`.

Гарантирует, что объект запроса, передаваемый методу обработчика, является экземпляром `Request`, а не обычным Django `HttpRequest`.

You won't typically need to override this method.

Обычно вам не нужно переопределять этот метод.

### .finalize_response(self, request, response, *args, **kwargs)

### .finalize_response(self, request, response, *args, **kwargs)

Ensures that any `Response` object returned from the handler method will be rendered into the correct content type, as determined by the content negotiation.

Гарантирует, что любой объект `Response`, возвращенный из метода обработчика, будет преобразован в правильный тип содержимого, как определено в процессе согласования содержимого.

You won't typically need to override this method.

Обычно вам не нужно переопределять этот метод.

---

# Function Based Views

# Представления на основе функций

> Saying [that class-based views] is always the superior solution is a mistake.
>
> — [Nick Coghlan](http://www.boredomandlaziness.org/2012/05/djangos-cbvs-are-not-mistake-but.html)

> Говорить [что классовые взгляды] всегда являются лучшим решением - это ошибка.
>
> - [Nick Coghlan](http://www.boredomandlaziness.org/2012/05/djangos-cbvs-are-not-mistake-but.html)

REST framework also allows you to work with regular function based views. It provides a set of simple decorators that wrap your function based views to ensure they receive an instance of `Request` (rather than the usual Django `HttpRequest`) and allows them to return a `Response` (instead of a Django `HttpResponse`), and allow you to configure how the request is processed.

REST-фреймворк также позволяет работать с обычными представлениями, основанными на функциях. Он предоставляет набор простых декораторов, которые оборачивают ваши представления на основе функций, чтобы они получали экземпляр `Request` (а не обычный Django `HttpRequest`) и позволяли им возвращать `Response` (а не Django `HttpResponse`), а также позволяют вам настраивать, как обрабатывается запрос.

## @api_view()

## @api_view()

**Signature:** `@api_view(http_method_names=['GET'])`

**Подпись:** `@api_view(http_method_names=['GET'])`.

The core of this functionality is the `api_view` decorator, which takes a list of HTTP methods that your view should respond to. For example, this is how you would write a very simple view that just manually returns some data:

Ядром этой функциональности является декоратор `api_view`, который принимает список методов HTTP, на которые должно отвечать ваше представление. Например, вот как можно написать очень простое представление, которое просто вручную возвращает некоторые данные:

```
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

This view will use the default renderers, parsers, authentication classes etc specified in the [settings](settings.md).

Это представление будет использовать рендереры по умолчанию, парсеры, классы аутентификации и т.д., указанные в [settings](settings.md).

By default only `GET` methods will be accepted. Other methods will respond with "405 Method Not Allowed". To alter this behavior, specify which methods the view allows, like so:

По умолчанию принимаются только методы `GET`. Другие методы будут отвечать "405 Method Not Allowed". Чтобы изменить это поведение, укажите, какие методы разрешены представлению, например, так:

```
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})
```

## API policy decorators

## Декораторы политики API

To override the default settings, REST framework provides a set of additional decorators which can be added to your views. These must come *after* (below) the `@api_view` decorator. For example, to create a view that uses a [throttle](throttling.md) to ensure it can only be called once per day by a particular user, use the `@throttle_classes` decorator, passing a list of throttle classes:

Чтобы переопределить настройки по умолчанию, REST framework предоставляет набор дополнительных декораторов, которые можно добавить к вашим представлениям. Они должны быть *после* (ниже) декоратора `@api_view`. Например, чтобы создать представление, которое использует [throttle](throttling.md) для обеспечения того, что оно может быть вызвано только один раз в день определенным пользователем, используйте декоратор `@throttle_classes`, передавая список классов throttle:

```
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

These decorators correspond to the attributes set on `APIView` subclasses, described above.

Эти декораторы соответствуют атрибутам, установленным на подклассах `APIView`, описанных выше.

The available decorators are:

Доступными декораторами являются:

* `@renderer_classes(...)`
* `@parser_classes(...)`
* `@authentication_classes(...)`
* `@throttle_classes(...)`
* `@permission_classes(...)`

* `@renderer_classes(...)`
* `@parser_classes(...)`
* `@authentication_classes(...)`
* `@throttle_classes(...)`
* `@permission_classes(...)`

Each of these decorators takes a single argument which must be a list or tuple of classes.

Каждый из этих декораторов принимает один аргумент, который должен быть списком или кортежем классов.

## View schema decorator

## Декоратор схемы представления

To override the default schema generation for function based views you may use the `@schema` decorator. This must come *after* (below) the `@api_view` decorator. For example:

Чтобы переопределить генерацию схемы по умолчанию для представлений на основе функций, вы можете использовать декоратор `@schema`. Он должен располагаться *после* (ниже) декоратора `@api_view`. Например:

```
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

This decorator takes a single `AutoSchema` instance, an `AutoSchema` subclass instance or `ManualSchema` instance as described in the [Schemas documentation](schemas.md). You may pass `None` in order to exclude the view from schema generation.

Этот декоратор принимает один экземпляр `AutoSchema`, экземпляр подкласса `AutoSchema` или экземпляр `ManualSchema`, как описано в документации [Schemas documentation](schemas.md). Вы можете передать `None`, чтобы исключить представление из генерации схемы.

```
@api_view(['GET'])
@schema(None)
def view(request):
    return Response({"message": "Will not appear in schema!"})
```