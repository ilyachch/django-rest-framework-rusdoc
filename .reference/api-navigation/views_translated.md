<!-- TRANSLATED by md-translate -->
---

source:

источник:

* decorators.py
* views.py

* Decerators.py
* views.py

---

# Class-based Views

# Классовые взгляды

> Django's class-based views are a welcome departure from the old-style views.
>
> — [Reinout van Rees](https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-usage.html)

> Взгляды Джанго, основанные на классе, являются долгожданным отходом от просмотров старого стиля.
>
>-[Reinout van Rees] (https://reinout.vanrees.org/weblog/2011/08/24/class на основе views-usage.html)

REST framework provides an `APIView` class, which subclasses Django's `View` class.

Framework REST предоставляет класс `apiview`, который подкласлен класс Django` view`.

`APIView` classes are different from regular `View` classes in the following ways:

`Классы Apiview` отличаются от обычных классов` View` по следующим образом:

* Requests passed to the handler methods will be REST framework's `Request` instances, not Django's `HttpRequest` instances.
* Handler methods may return REST framework's `Response`, instead of Django's `HttpResponse`. The view will manage content negotiation and setting the correct renderer on the response.
* Any `APIException` exceptions will be caught and mediated into appropriate responses.
* Incoming requests will be authenticated and appropriate permission and/or throttle checks will be run before dispatching the request to the handler method.

* Запросы, передаваемые методам обработчика, будут экземпляры Framework Framework, а не экземпляры Django `httprequest.
* Методы обработчика могут возвращать `` `` ``, вместо «httpresponse», вместо «httpresponse» Джанго.
Представление будет управлять переговорами о контенте и устанавливать правильный визуализатор на ответе.
* Любые исключения `apiexception 'будут пойманы и опосредованы в соответствующих ответах.
* Входящие запросы будут аутентифицированы, и перед отправкой запроса будут выполнены соответствующие разрешения, и/или проверка дроссельной заслонки.

Using the `APIView` class is pretty much the same as using a regular `View` class, as usual, the incoming request is dispatched to an appropriate handler method such as `.get()` or `.post()`. Additionally, a number of attributes may be set on the class that control various aspects of the API policy.

Использование класса `apiview` в значительной степени такое же, как использование обычного класса` view`, как обычно, входящий запрос отправляется на соответствующий метод обработчика, такой как `.get ()` или `.post ()`.
Кроме того, в классе может быть установлен ряд атрибутов, которые контролируют различные аспекты политики API.

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

** ПРИМЕЧАНИЕ **: Полные методы, атрибуты и отношения между Django Rest Framework `apiview`,` genericapiview`, различные `mixins` и` Viewsets` могут быть изначально сложными.
В дополнение к документации здесь, ресурс [Classy Django REST] (http://www.cdrf.co) предоставляет справочную справку с полными методами и атрибутами, для каждого из представлений Django Rest Framework на основе классов.

---

## API policy attributes

## Атрибуты политики API

The following attributes control the pluggable aspects of API views.

Следующие атрибуты контролируют подключаемые аспекты представлений API.

### .renderer_classes

### .renderer_classes

### .parser_classes

### .parser_classes

### .authentication_classes

### .Authentication_Classes

### .throttle_classes

### .throttle_classes

### .permission_classes

### .permission_classes

### .content_negotiation_class

### .content_negotiation_class

## API policy instantiation methods

## Методы экземпляры политики API

The following methods are used by REST framework to instantiate the various pluggable API policies. You won't typically need to override these methods.

Следующие методы используются в рамках REST для создания создания различных политик API -платформы.
Обычно вам не нужно переопределять эти методы.

### .get_renderers(self)

### .get_renderers (self)

### .get_parsers(self)

### .get_parsers (self)

### .get_authenticators(self)

### .get_authenticators (self)

### .get_throttles(self)

### .get_throttles (self)

### .get_permissions(self)

### .get_permissions (self)

### .get_content_negotiator(self)

### .get_content_negotiator (self)

### .get_exception_handler(self)

### .get_exception_handler (self)

## API policy implementation methods

## Методы реализации политики API

The following methods are called before dispatching to the handler method.

Следующие методы вызываются перед отправкой на метод обработчика.

### .check_permissions(self, request)

### .check_permissions (Self, запрос)

### .check_throttles(self, request)

### .check_throttles (Self, запрос)

### .perform_content_negotiation(self, request, force=False)

### .perform_content_negotiation (self, запрос, force = false)

## Dispatch methods

## методы отправки

The following methods are called directly by the view's `.dispatch()` method. These perform any actions that need to occur before or after calling the handler methods such as `.get()`, `.post()`, `put()`, `patch()` and `.delete()`.

Следующие методы называются непосредственно методом представления `.dispatch ()`.
Они выполняют любые действия, которые должны происходить до или после вызова методов обработчика, таких как `.get ()`, `.post ()`, `put ()`, `patch ()` и `.delete ()`.

### .initial(self, request, *args, **kwargs)

### .initial (Self, запрос, *args, ** kwargs)

Performs any actions that need to occur before the handler method gets called. This method is used to enforce permissions and throttling, and perform content negotiation.

Выполняет любые действия, которые должны произойти до того, как метод обработчика будет вызван.
Этот метод используется для обеспечения разрешений и дросселирования, а также для выполнения переговоров по контенту.

You won't typically need to override this method.

Обычно вам не нужно переопределить этот метод.

### .handle_exception(self, exc)

### .handle_exception (self, exc)

Any exception thrown by the handler method will be passed to this method, which either returns a `Response` instance, or re-raises the exception.

Любое исключение, брошенное методом обработчика, будет передано этому методу, который либо возвращает экземпляр «Ответа», либо повторно воспринимает исключение.

The default implementation handles any subclass of `rest_framework.exceptions.APIException`, as well as Django's `Http404` and `PermissionDenied` exceptions, and returns an appropriate error response.

Реализация по умолчанию обрабатывает любой подкласс `rest_framework.exceptions.apiexception`, а также исключения Django` http404` и `ormissiondenied` и возвращает соответствующий ответ ошибки.

If you need to customize the error responses your API returns you should subclass this method.

Если вам нужно настроить ответы на ошибку, возвращается ваш API, вы должны подключить этот метод.

### .initialize_request(self, request, *args, **kwargs)

### .Initialize_Request (Self, запрос, *args, ** kwargs)

Ensures that the request object that is passed to the handler method is an instance of `Request`, rather than the usual Django `HttpRequest`.

Гарантирует, что объект запроса, который передается методу обработчика, является экземпляром `request`, а не обычного Django` httprequest.

You won't typically need to override this method.

Обычно вам не нужно переопределить этот метод.

### .finalize_response(self, request, response, *args, **kwargs)

### .finalize_response (Self, запрос, ответ, *args, ** kwargs)

Ensures that any `Response` object returned from the handler method will be rendered into the correct content type, as determined by the content negotiation.

Обеспечивает, чтобы любой объект «ответа» возвращается из метода обработчика, будет отображаться в правильный тип контента, как определено соглашением о контенте.

You won't typically need to override this method.

Обычно вам не нужно переопределить этот метод.

---

# Function Based Views

# Просмотры на основе функций

> Saying [that class-based views] is always the superior solution is a mistake.
>
> — [Nick Coghlan](http://www.boredomandlaziness.org/2012/05/djangos-cbvs-are-not-mistake-but.html)

> Сказать [эти классовые взгляды] всегда является превосходным решением-ошибка.
>
>-[Ник Коглан] (http://www.boredomandlainess.org/2012/05/djangos-cbvs-are-not-mistake-but.html)

REST framework also allows you to work with regular function based views. It provides a set of simple decorators that wrap your function based views to ensure they receive an instance of `Request` (rather than the usual Django `HttpRequest`) and allows them to return a `Response` (instead of a Django `HttpResponse`), and allow you to configure how the request is processed.

Структура REST также позволяет вам работать с регулярными видами на основе функций.
Он предоставляет набор простых декораторов, которые обертывают ваши виды на основе функций, чтобы убедиться, что они получают экземпляр «запроса» (а не обычный Django `httprequest`) и позволяет им вернуть` response` (вместо django `httpresponse`
) и позволить вам настроить, как обрабатывается запрос.

## @api_view()

## @api_view ()

**Signature:** `@api_view(http_method_names=['GET'])`

** Подпись: ** `@API_VIEW (http_method_names = ['get'])`

The core of this functionality is the `api_view` decorator, which takes a list of HTTP methods that your view should respond to. For example, this is how you would write a very simple view that just manually returns some data:

Ядром этой функции является декоратор `api_view`, который содержит список методов HTTP, на которые должно отвечать ваше представление.
Например, именно так вы бы написали очень простое представление, которое просто вручную возвращает некоторые данные:

```
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

This view will use the default renderers, parsers, authentication classes etc specified in the [settings](settings.md).

В этом представлении будут использоваться визуализаторы по умолчанию, анализаторы, классы аутентификации и т. Д., Указанные в [настройках] (настройки.md).

By default only `GET` methods will be accepted. Other methods will respond with "405 Method Not Allowed". To alter this behavior, specify which methods the view allows, like so:

По умолчанию будут приняты только методы `get`.
Другие методы будут отвечать «405 методом не разрешен».
Чтобы изменить это поведение, укажите, какие методы позволяет представление, например:

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

Чтобы переопределить настройки по умолчанию, Framework REST предоставляет набор дополнительных декораторов, которые можно добавить к вашим взглядам.
Они должны прийти * после * (ниже) декоратор `@api_view`.
Например, чтобы создать представление, в котором используется [дроссельная заслонка] (trottling.md), чтобы убедиться, что его можно называть только один раз в день, используйте декоратор `@Throtttle_classes`, пропустив список классов дроссельной заслонки:

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

Эти декораторы соответствуют атрибутам, установленным на подклассах `apiview`, описанных выше.

The available decorators are:

Доступные декораторы:

* `@renderer_classes(...)`
* `@parser_classes(...)`
* `@authentication_classes(...)`
* `@throttle_classes(...)`
* `@permission_classes(...)`

* `@Renderer_Classes (...)`
* `@parser_classes (...)`
* `@authentication_classes (...)`
* `@throttle_classes (...)`
* `@permission_classes (...)`

Each of these decorators takes a single argument which must be a list or tuple of classes.

Каждый из этих декораторов берет один аргумент, который должен быть списком или кортежей классов.

## View schema decorator

## View Schema Decorator

To override the default schema generation for function based views you may use the `@schema` decorator. This must come *after* (below) the `@api_view` decorator. For example:

Чтобы переопределить генерацию схемы по умолчанию для представлений на основе функций, вы можете использовать декоратор `@Schema`.
Это должно прийти * после * (ниже) декоратор `@api_view`.
Например:

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

Этот декоратор принимает один экземпляр `autoschema`, экземпляр подкласса Autoschema` или экземпляр« Руководство », как описано в [схемах документации] (Schemas.md).
Вы можете пройти «нет», чтобы исключить представление из генерации схемы.

```
@api_view(['GET'])
@schema(None)
def view(request):
    return Response({"message": "Will not appear in schema!"})
```