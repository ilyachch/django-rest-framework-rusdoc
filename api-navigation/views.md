# Предсталвения-классы

> Представления-классы Django это безусловно шаг вперед по сравнению со старыми представлениями.
>
> — Рейну ван Рес

REST framework предоставляет класс `APIView`, который является подклассом джанговских классов `View`.

Классы `APIView` имеют следующие отличиия от обычных классов `View`:

* Запросы, переданные обработчику будут экземплярами `Request` REST framework, а не джанговских `HttpRequest`.
* Обрабатыващие методы могут возвращать `Response` REST framework вместо джанговских `HttpResponse`. Представление будет осущестлвять согласование содержимого и устанавливать нужный рендерер для ответа.
* Любые исключения `APIException` будут выявлены и связаны с соответствующими ответами.
* Входящие запросы будут подтверждены и соответствующее разрешение и/или проверки будут произведены перед тем как передать запрос на обработку.

Использование класса `APIView` не особо отличается от использования обычных классов `View`.Как правило, входящий запрос отправляется на обработку соответсвующему методу, как `.get()` или `.post()`.  Для класса, который отвечает за различные аспекты поведения API, могут задаваться дополнительные атрибуты.

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
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```

# Атрибуты API

Следующие атрибуты отвечают за подключаемые аспекты представлений API.

* `.renderer_classes`
* `.parser_classes`
* `.authentication_classes`
* `.throttle_classes`
* `.permission_classes`
* `.content_negotiation_class`

# Методы реализации API

Следующие методы используются в REST framework для реализации различных подключаемых компонентов API. Как правило эти методы не заменяются.

* `.get_renderers(self)`
* `.get_parsers(self)`
* `.get_authenticators(self)`
* `.get_throttles(self)`
* `.get_permissions(self)`
* `.get_content_negotiator(self)`
* `.get_exception_handler(self)`

# Методы применения компонентов API

Следующие методы вызываются до обрабатывающих методов.

* `.check_permissions(self, request)`
* `.check_throttles(self, request)`
* `.perform_content_negotiation(self, request, force=False)`

# Методы отправки

Следующие методы вызываюся напрямумю методом представления `.dispatch()`. Они осущестляют любые действия, которые должны произойти до или после обращения к методам обработки, таким как `.get()`, `.post()`, `put()`, `patch()` и `.delete()`.

## .initial(self, request, *args, **kwargs)

Осуществляет любые действия которые должны произойти перед вызовом методов обработки. Этот метод используется для примененя разрешений, а также для согласования содержимого контента.

Чаще всего вам не надо перегружать этот метод.

## .handle_exception(self, exc)

Любое исключение, вызваннное обрабатывающим методом, будет передано этому методу, который возвращает либо экземпляр `Response`, либо повторно выдает исключение.

В стандартном применении используется любой подкласс `rest_framework.exceptions.APIException`, а также исключения Django  `Http404` и `PermissionDenied` и возвращаются соответствующее сообщение об ошибке.

Если вам требуется изменить сообщения об ошибках API, то следует создать подкласс данного метода.

## .initialize_request(self, request, *args, **kwargs)

Проверяет, что объект запроса, который был передан обработчику, является экземпляром `Request`, а не обычным джанговским `HttpRequest`.

Чаще всего вам не надо перегружать этот метод.

## .finalize_response(self, request, response, *args, **kwargs)

Гарантирует, что любой метод `Response`, который вернулся от обрабатвающих методов, будет срендерен, как прописано в согласовании содержимого. Чаще всего вам не надо перегружать этот метод.

# Представления-функции
> Будет неверно утверждать, что представления-классы это всегда лучшее решение.
>
> — Ник Колан

REST framework позволяет работать с обычным представлениями на основе функций. В его составе есть набор простых декораторов, которые оборачивают ваши представления-функции для того, чтобы обеспечить получение экземпляра `Request` (вместо обычного джанговского `HttpRequest`) и позволяют возвращать Response (вместо `HttpResponse`), а также позволяют настроить каким образом обрабатывается запрос.

## @api_view()

Сигнатура: @api_view(http_method_names=['GET'])

Ключевая часть этого функционала заключается в декораторе `api_view`, который принимает саисок методов HTTP, которым отвечает ваше представление. Вот пример того как вы бы написале простое представление, которое вручную возвращает некоторые данные:

``` python
from rest_framework.decorators import api_view

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

Данное представление по умолчанию использует классы рендера, парсера, аутентификации и т.д., которые прописаны в настройках.
По умолчанию используются только методы `GET`. Другие методы вызовут сообщение "405 Method Not Allowed". Для того, чтобы изменить это, укажите методы в представлении:

``` python
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})
```

## Декораторы API

Для того, чтобы переписать настройки по умолчанию, в REST framework есть набор дополнительных декораторов, которые можно добавить к вашим представлениям. Они должны прописываться после декоратора `@api_view`. Например, чтобы создать представление, которое с помощью тротлинга делает так, что определенный пользователь может вызвать представление только один раз в день, можно воспользоваться декоратором `@throttle_classes`, который передает список классов тротлинга:

``` python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
        rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

Эти декораторы относятся к атрибутам подклассов `APIView`, описанных выше.

Доступные декораторы

* `@renderer_classes(...)`
* `@parser_classes(...)`
* `@authentication_classes(...)`
* `@throttle_classes(...)`
* `@permission_classes(...)`
Каждый из этих декораторов принимает единственный аргумент, который может быть списком или картежем классов.


# Декоратор View schema

Чтобы переписать стандартный генератор Schema для представлений-функций, вы можете воспользоваться декоратором `@schema`.

Вы должны прописать его после декоратора `@api_view`. Например:

``` python
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

Этот декоратор использует экземпляр `AutoSchema`, экземпляр подкласса `AutoSchema` или экземпляр `ManualSchema`, как описано в документации по Schema. Вы можете передать None, для того, чтобы исключить представление из генератора Schema.

``` python
@api_view(['GET'])
@schema(None)
def view(request):
    return Response({"message": "Will not appear in schema!"})
```