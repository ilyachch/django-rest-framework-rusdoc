<!-- TRANSLATED by md-translate -->
---

источник:
- exceptions.py

---

# Исключения

> Исключения... позволяют чисто организовать обработку ошибок в центральном или высокоуровневом месте в структуре программы.
>
> &mdash; Doug Hellmann, [Python Exception Handling Techniques](https://doughellmann.com/blog/2009/06/19/python-exception-handling-techniques/)

## Обработка исключений в представлениях фреймворка REST

Представления фреймворка REST обрабатывают различные исключения и возвращают соответствующие ответы на ошибки.

Обрабатываемыми исключениями являются:

* Подклассы `APIException`, возникающие внутри фреймворка REST.
* Исключение Django `Http404`.
* Исключение Django `PermissionDenied`.

В каждом случае фреймворк REST вернет ответ с соответствующим кодом состояния и типом содержимого.  В теле ответа будут содержаться любые дополнительные сведения о характере ошибки.

Большинство ответов на ошибки будут содержать ключ `detail` в теле ответа.

Например, следующий запрос:

```
DELETE http://api.example.com/foo/bar HTTP/1.1
Accept: application/json
```

Может быть получен ответ об ошибке, указывающий на то, что метод `DELETE` не разрешен для данного ресурса:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 42

{"detail": "Method 'DELETE' not allowed."}
```

Ошибки валидации обрабатываются несколько иначе, и в качестве ключей в ответе будут указаны имена полей. Если ошибка валидации не относится к конкретному полю, то будет использоваться ключ "non_field_errors", или любое строковое значение, установленное для параметра `NON_FIELD_ERRORS_KEY`.

Пример ошибки валидации может выглядеть следующим образом:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 94

{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
```

## Пользовательская обработка исключений

Вы можете реализовать пользовательскую обработку исключений, создав функцию-обработчик, которая преобразует исключения, возникающие в ваших представлениях API, в объекты ответа.  Это позволяет вам контролировать стиль ответов на ошибки, используемый вашим API.

Функция должна принимать пару аргументов, первый из которых - обрабатываемое исключение, а второй - словарь, содержащий любой дополнительный контекст, например, обрабатываемое в данный момент представление. Функция обработчика исключения должна либо возвращать объект `Response`, либо возвращать `None`, если исключение не может быть обработано.  Если обработчик возвращает `None`, то исключение будет повторно поднято, и Django вернет стандартный ответ HTTP 500 "ошибка сервера".

Например, вы можете захотеть убедиться, что все ответы на ошибки включают код состояния HTTP в теле ответа, например, так:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 62

{"status_code": 405, "detail": "Method 'DELETE' not allowed."}
```

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

Аргумент context не используется обработчиком по умолчанию, но может быть полезен, если обработчику исключений нужна дополнительная информация, например, обрабатываемое в данный момент представление, доступ к которому можно получить как `context['view']`.

Обработчик исключений также должен быть настроен в ваших настройках, используя ключ настройки `EXCEPTION_HANDLER`. Например:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

Если параметр `'EXCEPTION_HANDLER'` не указан, по умолчанию используется стандартный обработчик исключений, предоставляемый фреймворком REST:

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

Обратите внимание, что обработчик исключений будет вызываться только для ответов, сгенерированных поднятыми исключениями.  Он не будет использоваться для ответов, возвращаемых непосредственно представлением, таких как ответы `HTTP_400_BAD_REQUEST`, которые возвращаются общими представлениями при неудачной проверке сериализатора.

---

# API Reference

## APIException

**Подпись:** `APIException()`.

**базовый класс** для всех исключений, возникающих внутри класса `APIView` или `@api_view`.

Чтобы предоставить пользовательское исключение, подкласс `APIException` и установите атрибуты `.status_code`, `.default_detail` и `default_code` для класса.

Например, если ваш API полагается на сторонний сервис, который иногда может быть недоступен, вы можете захотеть реализовать исключение для кода ответа HTTP "503 Service Unavailable".  Это можно сделать следующим образом:

```
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
```

#### Проверка исключений API

Существует ряд различных свойств, доступных для проверки состояния
исключения API. Вы можете использовать их для создания пользовательской обработки исключений
для вашего проекта.

Доступными атрибутами и методами являются:

* `.detail` - Возвращает текстовое описание ошибки.
* `.get_codes()` - Возвращает идентификатор кода ошибки.
* `.get_full_details()` - Возвращает как текстовое описание, так и идентификатор кода.

В большинстве случаев деталь ошибки будет простым элементом:

```
>>> print(exc.detail)
You do not have permission to perform this action.
>>> print(exc.get_codes())
permission_denied
>>> print(exc.get_full_details())
{'message':'You do not have permission to perform this action.','code':'permission_denied'}
```

В случае ошибок валидации деталь ошибки будет представлять собой либо список, либо
словарь элементов:

```
>>> print(exc.detail)
{"name":"This field is required.","age":"A valid integer is required."}
>>> print(exc.get_codes())
{"name":"required","age":"invalid"}
>>> print(exc.get_full_details())
{"name":{"message":"This field is required.","code":"required"},"age":{"message":"A valid integer is required.","code":"invalid"}}
```

## ParseError

**Описание:** `ParseError(detail=None, code=None)`.

Возникает, если запрос содержит неправильно сформированные данные при доступе к `request.data`.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "400 Bad Request".

## AuthenticationFailed

**Подпись:** `AuthenticationFailed(detail=None, code=None)`.

Возникает, когда входящий запрос содержит неправильную аутентификацию.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "401 Unauthenticated", но оно также может привести к ответу "403 Forbidden", в зависимости от используемой схемы аутентификации.  Более подробную информацию см. в документации [authentication documentation](authentication.md).

## NotAuthenticated

**Подпись:** `NotAuthenticated(detail=None, code=None)`.

Возникает, когда неаутентифицированный запрос не прошел проверку на разрешение.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "401 Unauthenticated", но оно также может привести к ответу "403 Forbidden", в зависимости от используемой схемы аутентификации.  Более подробную информацию см. в документации [authentication documentation](authentication.md).

## PermissionDenied

**Подпись:** `PermissionDenied(detail=None, code=None)`.

Возникает, когда аутентифицированный запрос не прошел проверку на разрешение.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "403 Forbidden".

## NotFound

**Подпись:** `NotFound(detail=None, code=None)`.

Возникает, когда ресурс не существует по указанному URL. Это исключение эквивалентно стандартному исключению `Http404` Django.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "404 Not Found".

## MethodNotAllowed

**Признак:** `MethodNotAllowed(method, detail=None, code=None)`.

Возникает, когда происходит входящий запрос, который не сопоставлен с методом обработчика на представлении.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "405 Method Not Allowed".

## Неприемлемо

**Подпись:** `NotAcceptable(detail=None, code=None)`.

Возникает, когда поступает запрос с заголовком `Accept`, который не может быть удовлетворен ни одним из доступных рендереров.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "406 Not Acceptable".

## UnsupportedMediaType

**Признак:** `UnsupportedMediaType(media_type, detail=None, code=None)`.

Возникает, если при обращении к `request.data` нет парсеров, способных обработать тип содержимого данных запроса.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "415 Unsupported Media Type".

## Дроссель

**Подпись:** `Throttled(wait=None, detail=None, code=None)`.

Возникает, когда входящий запрос не проходит проверку на дросселирование.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "429 Too Many Requests".

## ValidationError

**Подпись:** `ValidationError(detail=None, code=None)`.

Исключение `ValidationError` немного отличается от других классов `APIException`:

* Аргумент `detail` может быть списком или словарем деталей ошибки, а также может быть вложенной структурой данных. Используя словарь, вы можете указать ошибки на уровне полей при выполнении проверки на уровне объектов в методе `validate()` сериализатора. Например. `raise serializers.ValidationError({'name': 'Please enter a valid name.'})`.
* По соглашению вы должны импортировать модуль serializers и использовать полностью квалифицированный стиль `ValidationError`, чтобы отличить его от встроенной ошибки валидации Django. Например. `raise serializers.ValidationError('Это поле должно быть целочисленным значением.')`.

Класс `ValidationError` должен использоваться для сериализатора и валидации полей, а также классами валидаторов. Он также вызывается при вызове `serializer.is_valid` с аргументом ключевого слова `raise_exception`:

```
serializer.is_valid(raise_exception=True)
```

Общие представления используют флаг `raise_exception=True`, что означает, что вы можете переопределить стиль ответов на ошибки валидации глобально в вашем API. Для этого используйте пользовательский обработчик исключений, как описано выше.

По умолчанию это исключение приводит к ответу с кодом состояния HTTP "400 Bad Request".

---

# Общие представления об ошибках

Django REST Framework предоставляет два представления ошибок, подходящих для предоставления общих JSON `500` Server Error и
`400` Bad Request ответы. (Стандартные представления ошибок Django предоставляют HTML-ответы, которые могут не подходить для
только для приложений API).

Используйте их согласно [Django's Customizing error views documentation](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views).

## `rest_framework.exceptions.server_error`

Возвращает ответ с кодом состояния `500` и типом содержимого `application/json`.

Устанавливается как `handler500`:

```
handler500 = 'rest_framework.exceptions.server_error'
```

## `rest_framework.exceptions.bad_request`

Возвращает ответ с кодом статуса `400` и типом содержимого `application/json`.

Устанавливается как `handler400`:

```
handler400 = 'rest_framework.exceptions.bad_request'
```

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## Стандартизированные ошибки ДРФ

Пакет [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) предоставляет обработчик исключений, который генерирует одинаковый формат для всех ответов 4xx и 5xx. Он является заменой стандартного обработчика исключений и позволяет настраивать формат ответа на ошибку без переписывания всего обработчика исключений. Стандартизированный формат ответа на ошибку легче документировать и проще обрабатывать потребителям API.