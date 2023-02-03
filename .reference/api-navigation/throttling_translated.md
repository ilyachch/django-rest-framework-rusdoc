<!-- TRANSLATED by md-translate -->
---

source:

источник:

* throttling.py

* throttling.py

---

# Throttling

# Дросселирование

> HTTP/1.1 420 Enhance Your Calm
>
> [Twitter API rate limiting response](https://developer.twitter.com/en/docs/basics/rate-limiting)

> HTTP/1.1 420 Повышение спокойствия
>
> [Twitter API ограничение скорости ответа](https://developer.twitter.com/en/docs/basics/rate-limiting)

Throttling is similar to [permissions](permissions.md), in that it determines if a request should be authorized. Throttles indicate a temporary state, and are used to control the rate of requests that clients can make to an API.

Дросселирование аналогично [permissions](permissions.md), поскольку оно определяет, должен ли запрос быть авторизован. Дроссели обозначают временное состояние и используются для контроля скорости запросов, которые клиенты могут делать к API.

As with permissions, multiple throttles may be used. Your API might have a restrictive throttle for unauthenticated requests, and a less restrictive throttle for authenticated requests.

Как и в случае с разрешениями, можно использовать несколько дросселей. Ваш API может иметь ограничительный дроссель для неаутентифицированных запросов и менее ограничительный дроссель для аутентифицированных запросов.

Another scenario where you might want to use multiple throttles would be if you need to impose different constraints on different parts of the API, due to some services being particularly resource-intensive.

Еще один сценарий, в котором вам может понадобиться использовать несколько дросселей, - это если вам нужно наложить различные ограничения на разные части API, поскольку некоторые сервисы являются особенно ресурсоемкими.

Multiple throttles can also be used if you want to impose both burst throttling rates, and sustained throttling rates. For example, you might want to limit a user to a maximum of 60 requests per minute, and 1000 requests per day.

Несколько дросселей также можно использовать, если вы хотите наложить дросселирование как на скорость разрыва, так и на скорость устойчивого дросселирования. Например, вы можете ограничить пользователя максимум 60 запросами в минуту и 1000 запросами в день.

Throttles do not necessarily only refer to rate-limiting requests. For example a storage service might also need to throttle against bandwidth, and a paid data service might want to throttle against a certain number of a records being accessed.

Дроссели не обязательно относятся только к запросам на ограничение скорости. Например, служба хранения данных может также нуждаться в ограничении пропускной способности, а платная служба данных может захотеть ограничить доступ к определенному количеству записей.

**The application-level throttling that REST framework provides should not be considered a security measure or protection against brute forcing or denial-of-service attacks. Deliberately malicious actors will always be able to spoof IP origins. In addition to this, the built-in throttling implementations are implemented using Django's cache framework, and use non-atomic operations to determine the request rate, which may sometimes result in some fuzziness.

**Дросселирование на уровне приложения, которое обеспечивает REST framework, не следует рассматривать как меру безопасности или защиту от перебора или атак типа "отказ в обслуживании". Намеренно злоумышленники всегда смогут подделать IP-адреса. В дополнение к этому, встроенная реализация дросселирования реализована с использованием кэш-фреймворка Django и использует неатомарные операции для определения скорости запросов, что иногда может привести к некоторой нечеткости.

The application-level throttling provided by REST framework is intended for implementing policies such as different business tiers and basic protections against service over-use.**

Дросселирование на уровне приложений, предоставляемое REST-фреймворком, предназначено для реализации таких политик, как различные бизнес-уровни и базовая защита от чрезмерного использования услуг**.

## How throttling is determined

## Как определяется дросселирование

As with permissions and authentication, throttling in REST framework is always defined as a list of classes.

Как и в случае с разрешениями и аутентификацией, дросселирование в REST-фреймворке всегда определяется как список классов.

Before running the main body of the view each throttle in the list is checked. If any throttle check fails an `exceptions.Throttled` exception will be raised, and the main body of the view will not run.

Перед запуском основной части представления проверяется каждый дроссель в списке. Если какая-либо проверка дросселя не прошла, будет вызвано исключение `exceptions.Throttled`, и основное тело представления не будет запущено.

## Setting the throttling policy

## Установка политики дросселирования

The default throttling policy may be set globally, using the `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES` settings. For example.

Политика дросселирования по умолчанию может быть установлена глобально, с помощью параметров `DEFAULT_THROTTLE_CLASSES` и `DEFAULT_THROTTLE_RATES`. Например.

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

The rate descriptions used in `DEFAULT_THROTTLE_RATES` may include `second`, `minute`, `hour` or `day` as the throttle period.

Описания тарифов, используемые в `DEFAULT_THROTTLE_RATES`, могут включать `second`, `minute`, `hour` или `day` в качестве периода дросселирования.

You can also set the throttling policy on a per-view or per-viewset basis, using the `APIView` class-based views.

Вы также можете установить политику дросселирования на основе каждого представления или каждого набора представлений, используя представления на основе класса `APIView`.

```
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

If you're using the `@api_view` decorator with function based views you can use the following decorator.

Если вы используете декоратор `@api_view` с представлениями, основанными на функциях, вы можете использовать следующий декоратор.

```
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

It's also possible to set throttle classes for routes that are created using the `@action` decorator. Throttle classes set in this way will override any viewset level class settings.

Также можно установить классы дросселей для маршрутов, которые создаются с помощью декоратора `@action`. Установленные таким образом классы дросселирования будут переопределять любые настройки классов на уровне набора представлений.

```
@action(detail=True, methods=["post"], throttle_classes=[UserRateThrottle])
def example_adhoc_method(request, pk=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

## How clients are identified

## Как определяются клиенты

The `X-Forwarded-For` HTTP header and `REMOTE_ADDR` WSGI variable are used to uniquely identify client IP addresses for throttling. If the `X-Forwarded-For` header is present then it will be used, otherwise the value of the `REMOTE_ADDR` variable from the WSGI environment will be used.

HTTP-заголовок `X-Forwarded-For` и WSGI-переменная `REMOTE_ADDR` используются для уникальной идентификации IP-адресов клиентов для дросселирования. Если заголовок `X-Forwarded-For` присутствует, то он будет использоваться, иначе будет использоваться значение переменной `REMOTE_ADDR` из среды WSGI.

If you need to strictly identify unique client IP addresses, you'll need to first configure the number of application proxies that the API runs behind by setting the `NUM_PROXIES` setting. This setting should be an integer of zero or more. If set to non-zero then the client IP will be identified as being the last IP address in the `X-Forwarded-For` header, once any application proxy IP addresses have first been excluded. If set to zero, then the `REMOTE_ADDR` value will always be used as the identifying IP address.

Если вам необходимо строго идентифицировать уникальные IP-адреса клиентов, вам нужно сначала настроить количество прокси-серверов приложений, за которыми работает API, установив параметр `NUM_PROXIES`. Это значение должно быть целым числом, равным нулю или больше. Если значение ненулевое, то IP-адрес клиента будет идентифицироваться как последний IP-адрес в заголовке `X-Forwarded-For`, после того как IP-адреса прокси приложений будут исключены. Если установлено в ноль, то значение `REMOTE_ADDR` всегда будет использоваться в качестве идентифицирующего IP-адреса.

It is important to understand that if you configure the `NUM_PROXIES` setting, then all clients behind a unique [NAT'd](https://en.wikipedia.org/wiki/Network_address_translation) gateway will be treated as a single client.

Важно понимать, что если вы настроите параметр `NUM_PROXIES`, то все клиенты за уникальным [NAT'd](https://en.wikipedia.org/wiki/Network_address_translation) шлюзом будут рассматриваться как один клиент.

Further context on how the `X-Forwarded-For` header works, and identifying a remote client IP can be [found here](http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster).

Дополнительную информацию о том, как работает заголовок `X-Forwarded-For` и как определить IP удаленного клиента, можно найти [здесь] (http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster).

## Setting up the cache

## Настройка кэша

The throttle classes provided by REST framework use Django's cache backend. You should make sure that you've set appropriate [cache settings](https://docs.djangoproject.com/en/stable/ref/settings/#caches). The default value of `LocMemCache` backend should be okay for simple setups. See Django's [cache documentation](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) for more details.

Классы дросселирования, предоставляемые фреймворком REST, используют бэкенд кэша Django. Вы должны убедиться, что установили соответствующие настройки [cache settings](https://docs.djangoproject.com/en/stable/ref/settings/#caches). Значение по умолчанию бэкенда `LocMemCache` должно быть приемлемым для простых настроек. Более подробную информацию можно найти в [документации по кэшу](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) Django.

If you need to use a cache other than `'default'`, you can do so by creating a custom throttle class and setting the `cache` attribute. For example:

Если вам нужно использовать кэш, отличный от `'default`, вы можете сделать это, создав пользовательский класс дросселя и установив атрибут `cache`. Например:

```
from django.core.cache import caches

class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```

You'll need to remember to also set your custom throttle class in the `'DEFAULT_THROTTLE_CLASSES'` settings key, or using the `throttle_classes` view attribute.

Вам нужно будет не забыть также установить ваш пользовательский класс дросселя в ключе настроек `'DEFAULT_THROTTLE_CLASSES'` или с помощью атрибута представления `throttle_classes`.

## A note on concurrency

## Заметка о параллелизме

The built-in throttle implementations are open to [race conditions](https://en.wikipedia.org/wiki/Race_condition#Data_race), so under high concurrency they may allow a few extra requests through.

Встроенные реализации дросселей открыты для [условий гонки] (https://en.wikipedia.org/wiki/Race_condition#Data_race), поэтому при высоком параллелизме они могут пропустить несколько лишних запросов.

If your project relies on guaranteeing the number of requests during concurrent requests, you will need to implement your own throttle class. See [issue #5181](https://github.com/encode/django-rest-framework/issues/5181) for more details.

Если ваш проект полагается на гарантию количества запросов во время одновременных запросов, вам необходимо реализовать свой собственный класс throttle. Более подробную информацию смотрите в [issue #5181](https://github.com/encode/django-rest-framework/issues/5181).

---

# API Reference

# API Reference

## AnonRateThrottle

## AnonRateThrottle

The `AnonRateThrottle` will only ever throttle unauthenticated users. The IP address of the incoming request is used to generate a unique key to throttle against.

Дроссель `AnonRateThrottle` будет дросселировать только неаутентифицированных пользователей. IP-адрес входящего запроса используется для генерации уникального ключа для дросселирования.

The allowed request rate is determined from one of the following (in order of preference).

Допустимая скорость запроса определяется по одному из следующих параметров (в порядке предпочтения).

* The `rate` property on the class, which may be provided by overriding `AnonRateThrottle` and setting the property.
* The `DEFAULT_THROTTLE_RATES['anon']` setting.

* Свойство `rate` класса, которое может быть предоставлено путем переопределения `AnonRateThrottle` и установки свойства.
* Настройка `DEFAULT_THROTTLE_RATES['anon']`.

`AnonRateThrottle` is suitable if you want to restrict the rate of requests from unknown sources.

`AnonRateThrottle` подходит, если вы хотите ограничить скорость запросов от неизвестных источников.

## UserRateThrottle

## UserRateThrottle

The `UserRateThrottle` will throttle users to a given rate of requests across the API. The user id is used to generate a unique key to throttle against. Unauthenticated requests will fall back to using the IP address of the incoming request to generate a unique key to throttle against.

Дроссель `UserRateThrottle` будет дросселировать пользователей до заданной скорости запросов через API. Идентификатор пользователя используется для генерации уникального ключа для дросселирования. Неаутентифицированные запросы будут возвращаться к использованию IP-адреса входящего запроса для генерации уникального ключа для дросселирования.

The allowed request rate is determined from one of the following (in order of preference).

Допустимая скорость запроса определяется по одному из следующих параметров (в порядке предпочтения).

* The `rate` property on the class, which may be provided by overriding `UserRateThrottle` and setting the property.
* The `DEFAULT_THROTTLE_RATES['user']` setting.

* Свойство `rate` класса, которое может быть предоставлено путем переопределения `UserRateThrottle` и установки свойства.
* Настройка `DEFAULT_THROTTLE_RATES['user']`.

An API may have multiple `UserRateThrottles` in place at the same time. To do so, override `UserRateThrottle` and set a unique "scope" for each class.

API может иметь несколько `UserRateThrottles` одновременно. Для этого переопределите `UserRateThrottle` и установите уникальный "scope" для каждого класса.

For example, multiple user throttle rates could be implemented by using the following classes...

Например, несколько пользовательских дросселей могут быть реализованы с помощью следующих классов...

```
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

...and the following settings.

...и следующие настройки.

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

`UserRateThrottle` is suitable if you want simple global rate restrictions per-user.

`UserRateThrottle` подходит, если вам нужны простые глобальные ограничения скорости для каждого пользователя.

## ScopedRateThrottle

## ScopedRateThrottle

The `ScopedRateThrottle` class can be used to restrict access to specific parts of the API. This throttle will only be applied if the view that is being accessed includes a `.throttle_scope` property. The unique throttle key will then be formed by concatenating the "scope" of the request with the unique user id or IP address.

Класс `ScopedRateThrottle` можно использовать для ограничения доступа к определенным частям API. Этот дроссель будет применяться, только если представление, к которому осуществляется доступ, включает свойство `.throttle_scope`. Уникальный ключ дросселя будет сформирован путем соединения "scope" запроса с уникальным идентификатором пользователя или IP-адресом.

The allowed request rate is determined by the `DEFAULT_THROTTLE_RATES` setting using a key from the request "scope".

Допустимая скорость запроса определяется настройкой `DEFAULT_THROTTLE_RATES`, используя ключ из "области действия" запроса.

For example, given the following views...

Например, учитывая следующие представления...

```
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...

class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
```

...and the following settings.

...и следующие настройки.

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```

User requests to either `ContactListView` or `ContactDetailView` would be restricted to a total of 1000 requests per-day. User requests to `UploadView` would be restricted to 20 requests per day.

Запросы пользователей к `ContactListView` или `ContactDetailView` будут ограничены до 1000 запросов в день. Запросы пользователей к `UploadView` будут ограничены 20 запросами в день.

---

# Custom throttles

# Пользовательские дроссели

To create a custom throttle, override `BaseThrottle` and implement `.allow_request(self, request, view)`. The method should return `True` if the request should be allowed, and `False` otherwise.

Чтобы создать пользовательский дроссель, переопределите `BaseThrottle` и реализуйте `.allow_request(self, request, view)`. Метод должен возвращать `True`, если запрос должен быть разрешен, и `False` в противном случае.

Optionally you may also override the `.wait()` method. If implemented, `.wait()` should return a recommended number of seconds to wait before attempting the next request, or `None`. The `.wait()` method will only be called if `.allow_request()` has previously returned `False`.

По желанию вы также можете переопределить метод `.wait()`. Если он реализован, `.wait()` должен возвращать рекомендуемое количество секунд ожидания перед попыткой следующего запроса или `None`. Метод `.wait()` будет вызван только в том случае, если `.allow_request()` ранее вернул `False`.

If the `.wait()` method is implemented and the request is throttled, then a `Retry-After` header will be included in the response.

Если реализован метод `.wait()` и запрос дросселируется, то в ответ будет включен заголовок `Retry-After`.

## Example

## Пример

The following is an example of a rate throttle, that will randomly throttle 1 in every 10 requests.

Ниже приведен пример дросселирования скорости, которое будет случайным образом дросселировать 1 из каждых 10 запросов.

```
import random

class RandomRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
```