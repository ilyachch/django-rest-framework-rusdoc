<!-- TRANSLATED by md-translate -->
---

source:

источник:

* exceptions.py

* exceptions.py

---

# Exceptions

# Исключения

> Exceptions… allow error handling to be organized cleanly in a central or high-level place within the program structure.
>
> — Doug Hellmann, [Python Exception Handling Techniques][cite]

> Исключения... позволяют чисто организовать обработку ошибок в центральном или высокоуровневом месте в структуре программы.
>
> - Даг Хеллманн, [Python Exception Handling Techniques][cite].

## Exception handling in REST framework views

## Обработка исключений в представлениях фреймворка REST

REST framework's views handle various exceptions, and deal with returning appropriate error responses.

Представления фреймворка REST обрабатывают различные исключения и возвращают соответствующие ответы на ошибки.

The handled exceptions are:

Обрабатываемыми исключениями являются:

* Subclasses of `APIException` raised inside REST framework.
* Django's `Http404` exception.
* Django's `PermissionDenied` exception.

* Подклассы `APIException`, возникающие внутри фреймворка REST.
* Исключение Django `Http404`.
* Исключение Django `PermissionDenied`.

In each case, REST framework will return a response with an appropriate status code and content-type. The body of the response will include any additional details regarding the nature of the error.

В каждом случае фреймворк REST вернет ответ с соответствующим кодом состояния и типом содержимого. В теле ответа будут содержаться любые дополнительные сведения о характере ошибки.

Most error responses will include a key `detail` in the body of the response.

Большинство ответов на ошибки будут содержать ключ `detail` в теле ответа.

For example, the following request:

Например, следующий запрос:

```
DELETE http://api.example.com/foo/bar HTTP/1.1
Accept: application/json
```

Might receive an error response indicating that the `DELETE` method is not allowed on that resource:

Может быть получен ответ об ошибке, указывающий на то, что метод `DELETE` не разрешен для данного ресурса:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 42

{"detail": "Method 'DELETE' not allowed."}
```

Validation errors are handled slightly differently, and will include the field names as the keys in the response. If the validation error was not specific to a particular field then it will use the "non_field_errors" key, or whatever string value has been set for the `NON_FIELD_ERRORS_KEY` setting.

Ошибки валидации обрабатываются несколько иначе, и в качестве ключей в ответе будут указаны имена полей. Если ошибка валидации не относится к конкретному полю, то будет использоваться ключ "non_field_errors", или любое строковое значение, установленное для параметра `NON_FIELD_ERRORS_KEY`.

An example validation error might look like this:

Пример ошибки валидации может выглядеть следующим образом:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 94

{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
```

## Custom exception handling

## Пользовательская обработка исключений

You can implement custom exception handling by creating a handler function that converts exceptions raised in your API views into response objects. This allows you to control the style of error responses used by your API.

Вы можете реализовать пользовательскую обработку исключений, создав функцию-обработчик, которая преобразует исключения, возникающие в ваших представлениях API, в объекты ответа. Это позволяет вам контролировать стиль ответов на ошибки, используемый вашим API.

The function must take a pair of arguments, the first is the exception to be handled, and the second is a dictionary containing any extra context such as the view currently being handled. The exception handler function should either return a `Response` object, or return `None` if the exception cannot be handled. If the handler returns `None` then the exception will be re-raised and Django will return a standard HTTP 500 'server error' response.

Функция должна принимать пару аргументов, первый из которых - обрабатываемое исключение, а второй - словарь, содержащий любой дополнительный контекст, например, обрабатываемое в данный момент представление. Функция обработчика исключения должна либо возвращать объект `Response`, либо возвращать `None`, если исключение не может быть обработано. Если обработчик возвращает `None`, то исключение будет повторно поднято, и Django вернет стандартный ответ HTTP 500 "ошибка сервера".

For example, you might want to ensure that all error responses include the HTTP status code in the body of the response, like so:

Например, вы можете захотеть убедиться, что все ответы на ошибки включают код состояния HTTP в теле ответа, например, так:

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

Аргумент context не используется обработчиком по умолчанию, но может быть полезен, если обработчику исключений нужна дополнительная информация, например, обрабатываемое в данный момент представление, доступ к которому можно получить как `context['view']`.

The exception handler must also be configured in your settings, using the `EXCEPTION_HANDLER` setting key. For example:

Обработчик исключений также должен быть настроен в ваших настройках, используя ключ настройки `EXCEPTION_HANDLER`. Например:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

If not specified, the `'EXCEPTION_HANDLER'` setting defaults to the standard exception handler provided by REST framework:

Если параметр `'EXCEPTION_HANDLER'` не указан, по умолчанию используется стандартный обработчик исключений, предоставляемый фреймворком REST:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

Note that the exception handler will only be called for responses generated by raised exceptions. It will not be used for any responses returned directly by the view, such as the `HTTP_400_BAD_REQUEST` responses that are returned by the generic views when serializer validation fails.

Обратите внимание, что обработчик исключений будет вызываться только для ответов, сгенерированных поднятыми исключениями. Он не будет использоваться для ответов, возвращаемых непосредственно представлением, таких как ответы `HTTP_400_BAD_REQUEST`, которые возвращаются общими представлениями при неудачной проверке сериализатора.

---

# API Reference

# API Reference

## APIException

## APIException

**Signature:** `APIException()`

**Подпись:** `APIException()`.

The **base class** for all exceptions raised inside an `APIView` class or `@api_view`.

**базовый класс** для всех исключений, возникающих внутри класса `APIView` или `@api_view`.

To provide a custom exception, subclass `APIException` and set the `.status_code`, `.default_detail`, and `default_code` attributes on the class.

Чтобы предоставить пользовательское исключение, подкласс `APIException` и установите атрибуты `.status_code`, `.default_detail` и `default_code` для класса.

For example, if your API relies on a third party service that may sometimes be unreachable, you might want to implement an exception for the "503 Service Unavailable" HTTP response code. You could do this like so:

Например, если ваш API полагается на сторонний сервис, который иногда может быть недоступен, вы можете захотеть реализовать исключение для кода ответа HTTP "503 Service Unavailable". Это можно сделать следующим образом:

```
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
```

#### Inspecting API exceptions

#### Проверка исключений API

There are a number of different properties available for inspecting the status of an API exception. You can use these to build custom exception handling for your project.

Существует несколько различных свойств, доступных для проверки состояния исключения API. Вы можете использовать их для создания пользовательской обработки исключений в вашем проекте.

The available attributes and methods are:

Доступными атрибутами и методами являются:

* `.detail` - Return the textual description of the error.
* `.get_codes()` - Return the code identifier of the error.
* `.get_full_details()` - Return both the textual description and the code identifier.

* `.detail` - Возвращает текстовое описание ошибки.
* `.get_codes()` - Возвращает идентификатор кода ошибки.
* `.get_full_details()` - Возвращает как текстовое описание, так и идентификатор кода.

In most cases the error detail will be a simple item:

В большинстве случаев деталь ошибки будет простым элементом:

```
>>> print(exc.detail)
You do not have permission to perform this action.
>>> print(exc.get_codes())
permission_denied
>>> print(exc.get_full_details())
{'message':'You do not have permission to perform this action.','code':'permission_denied'}
```

In the case of validation errors the error detail will be either a list or dictionary of items:

В случае ошибок валидации деталь ошибки будет представлять собой список или словарь элементов:

```
>>> print(exc.detail)
{"name":"This field is required.","age":"A valid integer is required."}
>>> print(exc.get_codes())
{"name":"required","age":"invalid"}
>>> print(exc.get_full_details())
{"name":{"message":"This field is required.","code":"required"},"age":{"message":"A valid integer is required.","code":"invalid"}}
```

## ParseError

## ParseError

**Signature:** `ParseError(detail=None, code=None)`

**Описание:** `ParseError(detail=None, code=None)`.

Raised if the request contains malformed data when accessing `request.data`.

Возникает, если запрос содержит неправильно сформированные данные при доступе к `request.data`.

By default this exception results in a response with the HTTP status code "400 Bad Request".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "400 Bad Request".

## AuthenticationFailed

## AuthenticationFailed

**Signature:** `AuthenticationFailed(detail=None, code=None)`

**Подпись:** `AuthenticationFailed(detail=None, code=None)`.

Raised when an incoming request includes incorrect authentication.

Возникает, когда входящий запрос содержит неправильную аутентификацию.

By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use. See the [authentication documentation](authentication.md) for more details.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "401 Unauthenticated", но оно также может привести к ответу "403 Forbidden", в зависимости от используемой схемы аутентификации. Более подробную информацию см. в документации [authentication documentation](authentication.md).

## NotAuthenticated

## NotAuthenticated

**Signature:** `NotAuthenticated(detail=None, code=None)`

**Подпись:** `NotAuthenticated(detail=None, code=None)`.

Raised when an unauthenticated request fails the permission checks.

Возникает, когда неаутентифицированный запрос не прошел проверку на разрешение.

By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use. See the [authentication documentation](authentication.md) for more details.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "401 Unauthenticated", но оно также может привести к ответу "403 Forbidden", в зависимости от используемой схемы аутентификации. Более подробную информацию см. в документации [authentication documentation](authentication.md).

## PermissionDenied

## PermissionDenied

**Signature:** `PermissionDenied(detail=None, code=None)`

**Подпись:** `PermissionDenied(detail=None, code=None)`.

Raised when an authenticated request fails the permission checks.

Возникает, когда аутентифицированный запрос не прошел проверку на разрешение.

By default this exception results in a response with the HTTP status code "403 Forbidden".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "403 Forbidden".

## NotFound

## NotFound

**Signature:** `NotFound(detail=None, code=None)`

**Подпись:** `NotFound(detail=None, code=None)`.

Raised when a resource does not exists at the given URL. This exception is equivalent to the standard `Http404` Django exception.

Возникает, когда ресурс не существует по заданному URL. Это исключение эквивалентно стандартному исключению `Http404` Django.

By default this exception results in a response with the HTTP status code "404 Not Found".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "404 Not Found".

## MethodNotAllowed

## MethodNotAllowed

**Signature:** `MethodNotAllowed(method, detail=None, code=None)`

**Признак:** `MethodNotAllowed(method, detail=None, code=None)`.

Raised when an incoming request occurs that does not map to a handler method on the view.

Возникает, когда происходит входящий запрос, который не сопоставлен с методом-обработчиком на представлении.

By default this exception results in a response with the HTTP status code "405 Method Not Allowed".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "405 Method Not Allowed".

## NotAcceptable

## Неприемлемо

**Signature:** `NotAcceptable(detail=None, code=None)`

**Подпись:** `NotAcceptable(detail=None, code=None)`.

Raised when an incoming request occurs with an `Accept` header that cannot be satisfied by any of the available renderers.

Возникает, когда поступает запрос с заголовком `Accept`, который не может быть удовлетворен ни одним из доступных рендереров.

By default this exception results in a response with the HTTP status code "406 Not Acceptable".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "406 Not Acceptable".

## UnsupportedMediaType

## UnsupportedMediaType

**Signature:** `UnsupportedMediaType(media_type, detail=None, code=None)`

**Признак:** `UnsupportedMediaType(media_type, detail=None, code=None)`.

Raised if there are no parsers that can handle the content type of the request data when accessing `request.data`.

Возникает, если при обращении к `request.data` нет парсеров, способных обработать тип содержимого данных запроса.

By default this exception results in a response with the HTTP status code "415 Unsupported Media Type".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "415 Unsupported Media Type".

## Throttled

## Дроссель

**Signature:** `Throttled(wait=None, detail=None, code=None)`

**Подпись:** `Throttled(wait=None, detail=None, code=None)`.

Raised when an incoming request fails the throttling checks.

Возникает, когда входящий запрос не проходит проверку на дросселирование.

By default this exception results in a response with the HTTP status code "429 Too Many Requests".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "429 Too Many Requests".

## ValidationError

## ValidationError

**Signature:** `ValidationError(detail, code=None)`

**Подпись:** `ValidationError(detail, code=None)`.

The `ValidationError` exception is slightly different from the other `APIException` classes:

Исключение `ValidationError` немного отличается от других классов `APIException`:

* The `detail` argument is mandatory, not optional.
* The `detail` argument may be a list or dictionary of error details, and may also be a nested data structure. By using a dictionary, you can specify field-level errors while performing object-level validation in the `validate()` method of a serializer. For example. `raise serializers.ValidationError({'name': 'Please enter a valid name.'})`
* By convention you should import the serializers module and use a fully qualified `ValidationError` style, in order to differentiate it from Django's built-in validation error. For example. `raise serializers.ValidationError('This field must be an integer value.')`

* Аргумент `detail` является обязательным, а не опциональным.
* Аргумент `detail` может представлять собой список или словарь сведений об ошибке, а также может быть вложенной структурой данных. Используя словарь, вы можете указать ошибки на уровне полей при выполнении проверки на уровне объектов в методе `validate()` сериализатора. Например. `raise serializers.ValidationError({'name': 'Please enter a valid name.'})`.
* По соглашению вы должны импортировать модуль serializers и использовать полностью квалифицированный стиль `ValidationError`, чтобы отличить его от встроенной ошибки валидации Django. Например. `raise serializers.ValidationError('Это поле должно быть целочисленным значением.')`.

The `ValidationError` class should be used for serializer and field validation, and by validator classes. It is also raised when calling `serializer.is_valid` with the `raise_exception` keyword argument:

Класс `ValidationError` должен использоваться для сериализатора и валидации полей, а также классами валидаторов. Он также вызывается при вызове `serializer.is_valid` с аргументом ключевого слова `raise_exception`:

```
serializer.is_valid(raise_exception=True)
```

The generic views use the `raise_exception=True` flag, which means that you can override the style of validation error responses globally in your API. To do so, use a custom exception handler, as described above.

Общие представления используют флаг `raise_exception=True`, что означает, что вы можете переопределить стиль ответов на ошибки валидации глобально в вашем API. Для этого используйте пользовательский обработчик исключений, как описано выше.

By default this exception results in a response with the HTTP status code "400 Bad Request".

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "400 Bad Request".

---

# Generic Error Views

# Общие представления об ошибках

Django REST Framework provides two error views suitable for providing generic JSON `500` Server Error and `400` Bad Request responses. (Django's default error views provide HTML responses, which may not be appropriate for an API-only application.)

Django REST Framework предоставляет два представления ошибок, подходящих для предоставления общих JSON ответов `500` Server Error и `400` Bad Request. (Стандартные представления ошибок Django предоставляют HTML-ответы, которые могут не подойти для приложения, использующего только API).

Use these as per [Django's Customizing error views documentation](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views).

Используйте их согласно [Django's Customizing error views documentation](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views).

## `rest_framework.exceptions.server_error`

## `rest_framework.exceptions.server_error`

Returns a response with status code `500` and `application/json` content type.

Возвращает ответ с кодом состояния `500` и типом содержимого `application/json`.

Set as `handler500`:

Устанавливается как `handler500`:

```
handler500 = 'rest_framework.exceptions.server_error'
```

## `rest_framework.exceptions.bad_request`

## `rest_framework.exceptions.bad_request`

Returns a response with status code `400` and `application/json` content type.

Возвращает ответ с кодом статуса `400` и типом содержимого `application/json`.

Set as `handler400`:

Устанавливается как `handler400`:

```
handler400 = 'rest_framework.exceptions.bad_request'
```

# Third party packages

# Пакеты сторонних производителей

The following third-party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## DRF Standardized Errors

## Стандартизированные ошибки ДРФ

The [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) package provides an exception handler that generates the same format for all 4xx and 5xx responses. It is a drop-in replacement for the default exception handler and allows customizing the error response format without rewriting the whole exception handler. The standardized error response format is easier to document and easier to handle by API consumers.

Пакет [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) предоставляет обработчик исключений, который генерирует одинаковый формат для всех ответов 4xx и 5xx. Он является заменой стандартного обработчика исключений и позволяет настраивать формат ответа на ошибку без переписывания всего обработчика исключений. Стандартизированный формат ответа на ошибку легче документировать и проще обрабатывать потребителям API.