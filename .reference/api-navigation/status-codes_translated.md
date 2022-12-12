<!-- TRANSLATED by md-translate -->
---

source:
    - status.py

источник:
- status.py

---

# Status Codes

# Коды статуса

> 418 I'm a teapot - Any attempt to brew coffee with a teapot should result in the error code "418 I'm a teapot".  The resulting entity body MAY be short and stout.
>
> &mdash; [RFC 2324](https://www.ietf.org/rfc/rfc2324.txt), Hyper Text Coffee Pot Control Protocol

> 418 Я чайник - любая попытка варить кофе с чайником должна привести к коду ошибки «418 Я чайник».
Полученное тело сущности может быть коротким и прочным.
>
> & mdash;
[RFC 2324] (https://www.ietf.org/rfc/rfc2324.txt), гипер текстовый протокол контроля кофейного горшка

Using bare status codes in your responses isn't recommended.  REST framework includes a set of named constants that you can use to make your code more obvious and readable.

Использование кодов статуса в ваших ответах не рекомендуется.
Структура REST включает набор именованных констант, которые вы можете использовать, чтобы сделать ваш код более очевидным и читаемым.

```
from rest_framework import status
from rest_framework.response import Response

def empty_view(self):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)
```

The full set of HTTP status codes included in the `status` module is listed below.

Полный набор кодов состояния HTTP, включенных в модуль `Status`, указан ниже.

The module also includes a set of helper functions for testing if a status code is in a given range.

Модуль также включает набор вспомогательных функций для тестирования, если код состояния находится в данном диапазоне.

```
from rest_framework import status
from rest_framework.test import APITestCase

class ExampleTestCase(APITestCase):
    def test_url_root(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
```

For more information on proper usage of HTTP status codes see [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
and [RFC 6585](https://tools.ietf.org/html/rfc6585).

Для получения дополнительной информации о правильном использовании кодов состояния HTTP см.
и [RFC 6585] (https://tools.ietf.org/html/rfc6585).

## Informational - 1xx

## Информационный - 1xx

This class of status code indicates a provisional response.  There are no 1xx status codes used in REST framework by default.

Этот класс кода состояния указывает на предварительный ответ.
По умолчанию нет кодов состояния 1xx, используемых в структуре REST.

```
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
```

## Successful - 2xx

## успешно - 2xx

This class of status code indicates that the client's request was successfully received, understood, and accepted.

Этот класс кода состояния указывает на то, что запрос клиента был успешно получен, понят и принят.

```
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS
HTTP_208_ALREADY_REPORTED
HTTP_226_IM_USED
```

## Redirection - 3xx

## перенаправление - 3xx

This class of status code indicates that further action needs to be taken by the user agent in order to fulfill the request.

Этот класс кода состояния указывает на то, что пользовательский агент должен предпринять дальнейшие действия для выполнения запроса.

```
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT
HTTP_308_PERMANENT_REDIRECT
```

## Client Error - 4xx

## Клиентская ошибка - 4xx

The 4xx class of status code is intended for cases in which the client seems to have erred.  Except when responding to a HEAD request, the server SHOULD include an entity containing an explanation of the error situation, and whether it is a temporary or permanent condition.

Класс кода состояния 4xx предназначен для случаев, когда клиент, похоже, допустил ошибку.
За исключением случаев, когда он отвечает на запрос на головы, сервер должен включать сущность, содержащую объяснение ситуации с ошибкой, и является ли это временным или постоянным условием.

```
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_426_UPGRADE_REQUIRED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
```

## Server Error - 5xx

## Ошибка сервера - 5xx

Response status codes beginning with the digit "5" indicate cases in which the server is aware that it has erred or is incapable of performing the request.  Except when responding to a HEAD request, the server SHOULD include an entity containing an explanation of the error situation, and whether it is a temporary or permanent condition.

Коды состояния ответа, начиная с цифры «5», указывают на случаи, когда сервер знает, что он ошибился или не способен выполнить запрос.
За исключением случаев, когда он отвечает на запрос на головы, сервер должен включать сущность, содержащую объяснение ситуации с ошибкой, и является ли это временным или постоянным условием.

```
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_506_VARIANT_ALSO_NEGOTIATES
HTTP_507_INSUFFICIENT_STORAGE
HTTP_508_LOOP_DETECTED
HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
HTTP_510_NOT_EXTENDED
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
```

## Helper functions

## вспомогательные функции

The following helper functions are available for identifying the category of the response code.

Следующие вспомогательные функции доступны для определения категории кода ответа.

```
is_informational()  # 1xx
is_success()        # 2xx
is_redirect()       # 3xx
is_client_error()   # 4xx
is_server_error()   # 5xx
```