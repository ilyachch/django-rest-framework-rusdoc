<!-- TRANSLATED by md-translate -->
# Коды состояния

> 418 Я чайник - Любая попытка сварить кофе с помощью чайника должна привести к коду ошибки "418 I'm a teapot". Результирующее тело сущности МОЖЕТ быть коротким и крепким.
>
> - [RFC 2324](https://www.ietf.org/rfc/rfc2324.txt), Hyper Text Coffee Pot Control Protocol

Не рекомендуется использовать в ответах "голые" коды состояния. DRF включает набор именованных констант, которые вы можете использовать, чтобы сделать ваш код более очевидным и читаемым.

```python
from rest_framework import status
from rest_framework.response import Response

def empty_view(self):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)
```

Полный набор кодов состояния HTTP, включенных в модуль `status`, приведен ниже.

Модуль также включает набор вспомогательных функций для проверки того, находится ли код состояния в заданном диапазоне.

```python
from rest_framework import status
from rest_framework.test import APITestCase

class ExampleTestCase(APITestCase):
    def test_url_root(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
```

Более подробную информацию о правильном использовании кодов состояния HTTP смотрите в [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) и [RFC 6585](https://tools.ietf.org/html/rfc6585).

## Информационный - 1xx

Этот класс кода состояния указывает на предварительный ответ. По умолчанию в DRF не используются коды состояния 1xx.

```python
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
HTTP_102_PROCESSING
HTTP_103_EARLY_HINTS
```

## Успешно - 2xx

Этот класс кода состояния указывает на то, что запрос клиента был успешно получен, понят и принят.

```python
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

## Перенаправление - 3xx

Этот класс кода состояния указывает на то, что агенту пользователя необходимо предпринять дополнительные действия для выполнения запроса.

```python
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

## Ошибка клиента - 4xx

Код состояния класса 4xx предназначен для случаев, когда клиент, похоже, ошибся. За исключением ответа на запрос HEAD, сервер ДОЛЖЕН включать объект, содержащий объяснение ситуации с ошибкой, а также то, является ли она временной или постоянной.

```python
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
HTTP_421_MISDIRECTED_REQUEST
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_425_TOO_EARLY
HTTP_426_UPGRADE_REQUIRED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
```

## Ошибка сервера - 5xx

Коды состояния ответа, начинающиеся с цифры "5", указывают на случаи, когда сервер знает, что он ошибся или не в состоянии выполнить запрос. За исключением ответа на запрос HEAD, сервер ДОЛЖЕН включать объект, содержащий объяснение ситуации с ошибкой, а также то, является ли она временной или постоянной.

```python
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

## Вспомогательные функции

Для определения категории кода ответа доступны следующие вспомогательные функции.

```python
is_informational()  # 1xx
is_success()        # 2xx
is_redirect()       # 3xx
is_client_error()   # 4xx
is_server_error()   # 5xx
```
