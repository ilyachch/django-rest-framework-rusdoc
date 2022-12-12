<!-- TRANSLATED by md-translate -->
---

source:
    - exceptions.py

источник:
- Exceptions.py

---

# Exceptions

# Исключения

> Exceptions… allow error handling to be organized cleanly in a central or high-level place within the program structure.
>
> &mdash; Doug Hellmann, [Python Exception Handling Techniques](https://doughellmann.com/blog/2009/06/19/python-exception-handling-techniques/)

> Исключения ... позволяйте обработке ошибок быть организованной чистого в центральном или высоком уровне в структуре программы.
>
> & mdash;
Даг Хеллманн, [Методы обработки исключений Python] (https://doughellmann.com/blog/2009/06/19/python-exception-handling-techniques/)

## Exception handling in REST framework views

## Обработка исключений в видах Framework Framework

REST framework's views handle various exceptions, and deal with returning appropriate error responses.

Представления REST Framework обрабатывают различные исключения и имеют дело с возвращением соответствующих ответов на ошибку.

The handled exceptions are:

Обработанные исключения:

* Subclasses of `APIException` raised inside REST framework.
* Django's `Http404` exception.
* Django's `PermissionDenied` exception.

* Подклассы `apiexception` подняты внутри структуры REST.
* Исключение Джанго `http404`.
* Исключение Django `ormissised '.

In each case, REST framework will return a response with an appropriate status code and content-type.  The body of the response will include any additional details regarding the nature of the error.

В каждом случае Framework REST вернет ответ с соответствующим кодом состояния и типом контента.
Тело ответа будет включать любую дополнительную информацию о природе ошибки.

Most error responses will include a key `detail` in the body of the response.

Большинство ответов на ошибки будут включать ключ «деталь» в теле ответа.

For example, the following request:

Например, следующий запрос:

```
DELETE http://api.example.com/foo/bar HTTP/1.1
Accept: application/json
```

Might receive an error response indicating that the `DELETE` method is not allowed on that resource:

Может получить ответ ошибки, указывающий, что метод `delete` не допускается на этот ресурс:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 42

{"detail": "Method 'DELETE' not allowed."}
```

Validation errors are handled slightly differently, and will include the field names as the keys in the response. If the validation error was not specific to a particular field then it will use the "non_field_errors" key, or whatever string value has been set for the `NON_FIELD_ERRORS_KEY` setting.

Ошибки проверки обрабатываются немного по -разному и будут включать имена поля в качестве ключей в ответе.
Если ошибка проверки не была определенной для конкретного поля, то она будет использовать клавишу «non_field_errors» или любое строковое значение, которое было установлено для настройки `non_field_errors_key`.

An example validation error might look like this:

Пример ошибка проверки может выглядеть так:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 94

{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
```

## Custom exception handling

## Пользовательская обработка исключений

You can implement custom exception handling by creating a handler function that converts exceptions raised in your API views into response objects.  This allows you to control the style of error responses used by your API.

Вы можете реализовать пользовательскую обработку исключений, создав функцию обработчика, которая преобразует исключения, поднятые в ваших представлениях API в объекты ответа.
Это позволяет вам контролировать стиль ответов на ошибки, используемые вашим API.

The function must take a pair of arguments, the first is the exception to be handled, and the second is a dictionary containing any extra context such as the view currently being handled. The exception handler function should either return a `Response` object, or return `None` if the exception cannot be handled.  If the handler returns `None` then the exception will be re-raised and Django will return a standard HTTP 500 'server error' response.

Функция должна принимать пару аргументов, первым является исключение, которое нужно обрабатывать, а второй - это словарь, содержащий любой дополнительный контекст, такой как представление, которое в настоящее время обрабатывается.
Функция обработчика исключений должна либо вернуть объект `recsess`, либо вернуть` none`, если исключение не может быть обработано.
Если обработчик возвращает «нет», то исключение будет повторно повторно, и Django вернет стандартный ответ на сервер HTTP 500 «Ошибка».

For example, you might want to ensure that all error responses include the HTTP status code in the body of the response, like so:

Например, вы можете убедиться, что все ответы по ошибкам включали код состояния HTTP в органе ответа, например, так:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 62

{"status_code": 405, "detail": "Method 'DELETE' not allowed."}
```

In order to alter the style of the response, you could write the following custom exception handler:

Чтобы изменить стиль ответа, вы можете написать следующий пользовательский обработчик исключений:

```
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
```

The context argument is not used by the default handler, but can be useful if the exception handler needs further information such as the view currently being handled, which can be accessed as `context['view']`.

Аргумент контекста не используется обработчиком по умолчанию, но может быть полезен, если обработчик исключений нуждается в дополнительной информации, такой как обрабатывается в настоящее время представление, к которому можно получить доступ как `context ['view']`.

The exception handler must also be configured in your settings, using the `EXCEPTION_HANDLER` setting key. For example:

Обработчик исключений также должен быть настроен в ваших настройках, используя ключ настройки `exception_handler`.
Например:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

If not specified, the `'EXCEPTION_HANDLER'` setting defaults to the standard exception handler provided by REST framework:

Если не указано, настройка `'exception_handler'`` по умолчанию в стандартный обработчик исключений, предоставленный Framework REST:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

Note that the exception handler will only be called for responses generated by raised exceptions.  It will not be used for any responses returned directly by the view, such as the `HTTP_400_BAD_REQUEST` responses that are returned by the generic views when serializer validation fails.

Обратите внимание, что обработчик исключений будет вызвана только для ответов, сгенерированных поднятыми исключениями.
Он не будет использоваться для каких -либо ответов, возвращаемых непосредственно с помощью представления, таких как ответы `http_400_bad_request

---

# API Reference

# Ссылка на API

## APIException

## apiexception

**Signature:** `APIException()`

** Подпись: ** `apiexception ()`

The **base class** for all exceptions raised inside an `APIView` class or `@api_view`.

** базовый класс ** для всех исключений, поднятых в классе `apiview` или`@api_view`.

To provide a custom exception, subclass `APIException` and set the `.status_code`, `.default_detail`, and `default_code` attributes on the class.

Чтобы предоставить пользовательское исключение, подкласс `apiexception` и установил атрибуты` .status_code`, `.default_detail` и` default_code` в классе.

For example, if your API relies on a third party service that may sometimes be unreachable, you might want to implement an exception for the "503 Service Unavailable" HTTP response code.  You could do this like so:

Например, если ваш API опирается на стороннюю службу, которая иногда может быть недоступна, вы можете реализовать исключение для кода ответа «503 Service Navailable» HTTP.
Вы могли бы сделать это так:

```
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
```

#### Inspecting API exceptions

#### Проверка исключений API

There are a number of different properties available for inspecting the status
of an API exception. You can use these to build custom exception handling
for your project.

Есть ряд различных свойств, доступных для проверки статуса
исключения API.
Вы можете использовать их для создания пользовательской обработки исключений
для вашего проекта.

The available attributes and methods are:

Доступные атрибуты и методы:

* `.detail` - Return the textual description of the error.
* `.get_codes()` - Return the code identifier of the error.
* `.get_full_details()` - Return both the textual description and the code identifier.

* `.detail` - вернуть текстовое описание ошибки.
* `.get_codes ()` - вернуть идентификатор кода ошибки.
* `.get_full_details ()` - вернуть как текстовое описание, так и идентификатор кода.

In most cases the error detail will be a simple item:

В большинстве случаев детализация ошибки будет простым элементом:

```
>>> print(exc.detail)
You do not have permission to perform this action.
>>> print(exc.get_codes())
permission_denied
>>> print(exc.get_full_details())
{'message':'You do not have permission to perform this action.','code':'permission_denied'}
```

In the case of validation errors the error detail will be either a list or
dictionary of items:

В случае ошибок проверки детализация ошибки будет либо списком, либо
Словарь предметов:

```
>>> print(exc.detail)
{"name":"This field is required.","age":"A valid integer is required."}
>>> print(exc.get_codes())
{"name":"required","age":"invalid"}
>>> print(exc.get_full_details())
{"name":{"message":"This field is required.","code":"required"},"age":{"message":"A valid integer is required.","code":"invalid"}}
```

## ParseError

## parseerror

**Signature:** `ParseError(detail=None, code=None)`

** Подпись: ** `parseerror (detail = none, code = none)`

Raised if the request contains malformed data when accessing `request.data`.

Поднят, если запрос содержит узолотые данные при доступе к `request.data`.

By default this exception results in a response with the HTTP status code "400 Bad Request".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «400 Bad Request».

## AuthenticationFailed

## аутентификация

**Signature:** `AuthenticationFailed(detail=None, code=None)`

** Подпись: ** `AuthenticationFailed (detail = none, code = none)`

Raised when an incoming request includes incorrect authentication.

Повышен, когда входящий запрос включает в себя неправильную аутентификацию.

By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use.  See the [authentication documentation](authentication.md) for more details.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «401 unathenticated», но это также может привести к ответу «403 запрещенный», в зависимости от используемой схемы аутентификации.
См. Документацию по аутентификации] (Authentication.md) для получения более подробной информации.

## NotAuthenticated

## notauthenticated

**Signature:** `NotAuthenticated(detail=None, code=None)`

** Подпись: ** `notauthenticated (detail = none, code = none)`

Raised when an unauthenticated request fails the permission checks.

Поднят, когда несаутентированный запрос не выполняет проверку разрешений.

By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use.  See the [authentication documentation](authentication.md) for more details.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «401 unathenticated», но это также может привести к ответу «403 запрещенный», в зависимости от используемой схемы аутентификации.
См. Документацию по аутентификации] (Authentication.md) для получения более подробной информации.

## PermissionDenied

## В доступе отказано

**Signature:** `PermissionDenied(detail=None, code=None)`

** Подпись: ** `разрешение

Raised when an authenticated request fails the permission checks.

Повышен, когда аутентифицированный запрос не выполняет проверку разрешений.

By default this exception results in a response with the HTTP status code "403 Forbidden".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «403 FOBIDED».

## NotFound

## Не обнаружена

**Signature:** `NotFound(detail=None, code=None)`

** Подпись: ** `notfound (detail = none, code = none)`

Raised when a resource does not exists at the given URL. This exception is equivalent to the standard `Http404` Django exception.

Поднят, когда ресурс не существует при данном URL.
Это исключение эквивалентно стандартному исключению `http404` django.

By default this exception results in a response with the HTTP status code "404 Not Found".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «404 не найден».

## MethodNotAllowed

## Метод не разрешен

**Signature:** `MethodNotAllowed(method, detail=None, code=None)`

** Подпись: ** `methodNotAllowed (метод, detail = none, code = none)`

Raised when an incoming request occurs that does not map to a handler method on the view.

Поднимается, когда возникает входящий запрос, который не сопоставляется с методом обработчика в представлении.

By default this exception results in a response with the HTTP status code "405 Method Not Allowed".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «Метод 405 не разрешен».

## NotAcceptable

## Неприемлимо

**Signature:** `NotAcceptable(detail=None, code=None)`

** Подпись: ** `notecpectable (detail = none, code = none)`

Raised when an incoming request occurs with an `Accept` header that cannot be satisfied by any of the available renderers.

Поднят, когда входящий запрос возникает с заголовком «принять», который не может быть удовлетворен ни одним из доступных визуализаторов.

By default this exception results in a response with the HTTP status code "406 Not Acceptable".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «406 недопустимо».

## UnsupportedMediaType

## UnsupportedMediatype

**Signature:** `UnsupportedMediaType(media_type, detail=None, code=None)`

** Подпись: ** `unsupportedMediatype (media_type, detail = none, code = none)`

Raised if there are no parsers that can handle the content type of the request data when accessing `request.data`.

Повышен, если нет анализаторов, которые могут обрабатывать тип контента данных запроса при доступе к `request.data`.

By default this exception results in a response with the HTTP status code "415 Unsupported Media Type".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «415 Неподдерживаемый тип носителя».

## Throttled

## дроссель

**Signature:** `Throttled(wait=None, detail=None, code=None)`

** Подпись: ** `дроссельная (подожди = нет, detail = none, code = none)`

Raised when an incoming request fails the throttling checks.

Повышен, когда входящий запрос не проходит проверку дросселирования.

By default this exception results in a response with the HTTP status code "429 Too Many Requests".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «429 Слишком много запросов».

## ValidationError

## Ошибка проверки

**Signature:** `ValidationError(detail, code=None)`

** Подпись: ** `validationError (detail, code = none)`

The `ValidationError` exception is slightly different from the other `APIException` classes:

Исключение `valyationError` немного отличается от других классов` apiexception`:

* The `detail` argument is mandatory, not optional.
* The `detail` argument may be a list or dictionary of error details, and may also be a nested data structure. By using a dictionary, you can specify field-level errors while performing object-level validation in the `validate()` method of a serializer. For example. `raise serializers.ValidationError({'name': 'Please enter a valid name.'})`
* By convention you should import the serializers module and use a fully qualified `ValidationError` style, in order to differentiate it from Django's built-in validation error. For example. `raise serializers.ValidationError('This field must be an integer value.')`

* Аргумент `detail` является обязательным, а не необязательным.
* Аргумент `detail` может быть списком или словарем сведений об ошибках, а также может быть вложенной структурой данных.
Используя словарь, вы можете указать ошибки на уровне поля при выполнении проверки на уровне объектов в методе `validate ()` сериализатора.
Например.
`Raise Serializers.validationError ({'name': 'Пожалуйста, введите действительное имя.'})`
* По соглашению вы должны импортировать модуль Serializers и использовать полностью квалифицированный стиль `valyationError
Например.
`Raise Serializers.validationError (« Это поле должно быть целочисленным значением. »)`

The `ValidationError` class should be used for serializer and field validation, and by validator classes. It is also raised when calling `serializer.is_valid` with the `raise_exception` keyword argument:

Класс `valyationError 'должен использоваться для сериализатора и проверки поля, а также классами валидатора.
Это также повышается при вызове `serializer.is_valid` с аргументом ключевого слова` rate_exception`:

```
serializer.is_valid(raise_exception=True)
```

The generic views use the `raise_exception=True` flag, which means that you can override the style of validation error responses globally in your API. To do so, use a custom exception handler, as described above.

Общие представления используют флаг `rate_exception = true`, что означает, что вы можете переопределить стиль ответов на ошибку проверки в мире в своем API.
Для этого используйте пользовательский обработчик исключений, как описано выше.

By default this exception results in a response with the HTTP status code "400 Bad Request".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP «400 Bad Request».

---

# Generic Error Views

# Общие виды ошибок

Django REST Framework provides two error views suitable for providing generic JSON `500` Server Error and
`400` Bad Request responses. (Django's default error views provide HTML responses, which may not be appropriate for an
API-only application.)

Django Rest Framework предоставляет два представления об ошибках, подходящие для предоставления общей ошибки сервера json `500` и
`400` Ответы с плохими запросами.
(Просмотры ошибок по умолчанию Django предоставляют HTML -ответы, которые могут не подходить для
Приложение только для API.)

Use these as per [Django's Customizing error views documentation](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views).

Используйте их в соответствии с [Документация по ошибке настройки Django.

## `rest_framework.exceptions.server_error`

## `rest_framework.exceptions.server_error`

Returns a response with status code `500` and `application/json` content type.

Возвращает ответ с кодом состояния `500` и` Приложение/JSON` Тип контента.

Set as `handler500`:

Установить как `handler500`:

```
handler500 = 'rest_framework.exceptions.server_error'
```

## `rest_framework.exceptions.bad_request`

## `rest_framework.exceptions.bad_request`

Returns a response with status code `400` and `application/json` content type.

Возвращает ответ с кодом состояния `400` и` Приложение/JSON` Тип контента.

Set as `handler400`:

Установить как `handler400`:

```
handler400 = 'rest_framework.exceptions.bad_request'
```

# Third party packages

# Сторонние пакеты

The following third-party packages are also available.

Следующие сторонние пакеты также доступны.

## DRF Standardized Errors

## Стандартизированные ошибки DRF

The [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) package provides an exception handler that generates the same format for all 4xx and 5xx responses. It is a drop-in replacement for the default exception handler and allows customizing the error response format without rewriting the whole exception handler. The standardized error response format is easier to document and easier to handle by API consumers.

Пакет [https://github.com/ghazi-standardable-errors) (https://github.com/ghazi-git/drf-standardized-errors).
Это замена для обработки исключений по умолчанию и позволяет настроить формат ответа ошибки без переписывания всего обработчика исключений.
Стандартизированный формат ответа на ошибку легче документировать, и его легче обрабатывать потребителями API.