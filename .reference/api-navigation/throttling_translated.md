<!-- TRANSLATED by md-translate -->
---

source:
    - throttling.py

источник:
- Throttling.py

---

# Throttling

# Дросселя

> HTTP/1.1 420 Enhance Your Calm
>
> [Twitter API rate limiting response](https://developer.twitter.com/en/docs/basics/rate-limiting)

> Http/1.1 420 Улучшите свое спокойствие
>
> [Ответ с ограничением скорости API Twitter] (https://developer.twitter.com/en/docs/basics/rate-limiting)

Throttling is similar to [permissions](permissions.md), in that it determines if a request should be authorized.  Throttles indicate a temporary state, and are used to control the rate of requests that clients can make to an API.

Дросселирование аналогично [разрешениям] (разрешения. MD), поскольку он определяет, должен ли запрос быть разрешен.
Дростники указывают на временное состояние и используются для контроля скорости запросов, которые клиенты могут сделать в API.

As with permissions, multiple throttles may be used.  Your API might have a restrictive throttle for unauthenticated requests, and a less restrictive throttle for authenticated requests.

Как и в случае с разрешениями, можно использовать несколько дросселей.
Ваш API может иметь ограничительный газ для несаутентированных запросов и менее ограничивающий дроссель для аутентифицированных запросов.

Another scenario where you might want to use multiple throttles would be if you need to impose different constraints on different parts of the API, due to some services being particularly resource-intensive.

Еще один сценарий, в котором вы можете использовать несколько дросселей, если вам нужно наложить различные ограничения на разные части API, из-за того, что некоторые услуги были особенно ресурсными.

Multiple throttles can also be used if you want to impose both burst throttling rates, and sustained throttling rates.  For example, you might want to limit a user to a maximum of 60 requests per minute, and 1000 requests per day.

Многочисленные дроссели также могут быть использованы, если вы хотите навязать как скорость взрыва, так и устойчивые скорости дросселя.
Например, вы можете ограничить пользователя максимум 60 запросов в минуту и 1000 запросов в день.

Throttles do not necessarily only refer to rate-limiting requests.  For example a storage service might also need to throttle against bandwidth, and a paid data service might want to throttle against a certain number of a records being accessed.

Дроноты не обязательно относятся только к запросам ограничивающих ставок.
Например, служба хранения также может потребоваться захлопнуть от пропускной способности, и платная служба данных может захотеть запустить на определенное количество записей, доступных.

**The application-level throttling that REST framework provides should not be considered a security measure or protection against brute forcing or denial-of-service attacks. Deliberately malicious actors will always be able to spoof IP origins. In addition to this, the built-in throttling implementations are implemented using Django's cache framework, and use non-atomic operations to determine the request rate, which may sometimes result in some fuzziness.

** Дросляция на уровне приложения, которую обеспечивает структура REST, не должна рассматриваться как мера безопасности или защиту от грубого воздействия или атак отказа в службе.
Узнательно злонамеренные актеры всегда смогут подделать IP Origins.
В дополнение к этому, встроенные реализации дросселирования реализуются с использованием кеша Django и используют неатомические операции для определения скорости запроса, что иногда может привести к некоторой нечеткости.

The application-level throttling provided by REST framework is intended for implementing policies such as different business tiers and basic protections against service over-use.**

Дросселя на уровне приложения, предоставленная Framework REST, предназначена для реализации таких политик, как различные бизнес-уровни и базовая защита от чрезмерного использования услуг. **

## How throttling is determined

## как определяется дроссельная

As with permissions and authentication, throttling in REST framework is always defined as a list of classes.

Как и в случае с разрешениями и аутентификацией, дросселирование в рамках REST всегда определяется как список классов.

Before running the main body of the view each throttle in the list is checked.
If any throttle check fails an `exceptions.Throttled` exception will be raised, and the main body of the view will not run.

Перед запуском основного корпуса вида каждая дроссельная заслонка в списке проверяется.
Если какая -либо проверка дроссельной заслонки не удастся, будет поднято исключение.

## Setting the throttling policy

## Установка политики дросселирования

The default throttling policy may be set globally, using the `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES` settings.  For example.

Политика дросселя по умолчанию может быть установлена во всем мире, используя параметры `default_throttle_class` и` default_throttle_rates`.
Например.

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

Описания ставок, используемые в `default_throttle_rates`, могут включать в себя` second`, `minute`,` `` или `day 'в качестве периода дроссельной заслонки.

You can also set the throttling policy on a per-view or per-viewset basis,
using the `APIView` class-based views.

Вы также можете установить политику дросселирования на основе просмотра или на расстояние на расстоянии,
Использование просмотров на основе класса Apiview`.

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

Если вы используете декоратор `@API_VIEW` с видами на основе функций, вы можете использовать следующий декоратор.

```
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

It's also possible to set throttle classes for routes that are created using the `@action` decorator.
Throttle classes set in this way will override any viewset level class settings.

Также можно установить классы дроссельной заслонки для маршрутов, которые создаются с использованием декоратора `@Action`.
Занятия дроссельной заслонки, установленные таким образом, переопределят любые настройки класса уровня вида.

```
@action(detail=True, methods=["post"], throttle_classes=[UserRateThrottle])
def example_adhoc_method(request, pk=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

## How clients are identified

## как идентифицируются клиенты

The `X-Forwarded-For` HTTP header and `REMOTE_ADDR` WSGI variable are used to uniquely identify client IP addresses for throttling.  If the `X-Forwarded-For` header is present then it will be used, otherwise the value of the `REMOTE_ADDR` variable from the WSGI environment will be used.

Заголовок HTTP `x-forwarded-For` и` wsgi-переменная halte_addr` используется для однозначного идентификации IP-адресов клиента для дросселирования.
Если присутствует заголовок `x-forwarded-for

If you need to strictly identify unique client IP addresses, you'll need to first configure the number of application proxies that the API runs behind by setting the `NUM_PROXIES` setting.  This setting should be an integer of zero or more.  If set to non-zero then the client IP will be identified as being the last IP address in the `X-Forwarded-For` header, once any application proxy IP addresses have first been excluded.  If set to zero, then the `REMOTE_ADDR` value will always be used as the identifying IP address.

Если вам нужно строго идентифицировать уникальные IP -адреса клиента, вам нужно сначала настроить количество прокси приложения, которые API работает позади, установив настройку `num_proxies.
Эта настройка должна быть целым числом нуля или более.
Если установлено в Nonero, то IP-адрес клиента будет идентифицирован как последний IP-адрес в заголовке `x-forwarded-For`, после того, как любые прокси-адреса приложения впервые были исключены.
Если установить на ноль, то значение `remote_addr` всегда будет использоваться в качестве идентификационного IP -адреса.

It is important to understand that if you configure the `NUM_PROXIES` setting, then all clients behind a unique [NAT'd](https://en.wikipedia.org/wiki/Network_address_translation) gateway will be treated as a single client.

Важно понимать, что если вы настраиваете настройку `num_proxies`, то все клиенты, стоящие за уникальным [nat'd] (https://en.wikipedia.org/wiki/network_address_translation), будут рассматриваться как один клиент.

Further context on how the `X-Forwarded-For` header works, and identifying a remote client IP can be [found here](http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster).

Дополнительный контекст о том, как работает заголовок `x-forwarded-for`, и идентификация удаленного клиента IP может быть [найдено здесь] (http://oxpedia.org/wiki/index.php?title=plsuites
Анкет

## Setting up the cache

## Настройка кэша

The throttle classes provided by REST framework use Django's cache backend.  You should make sure that you've set appropriate [cache settings](https://docs.djangoproject.com/en/stable/ref/settings/#caches).  The default value of `LocMemCache` backend should be okay for simple setups.  See Django's [cache documentation](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) for more details.

Классы дроссельной заслонки, предоставленные Framework REST, используют бэкэнд кэша Джанго.
Вы должны убедиться, что вы установили соответствующие [настройки кэша] (https://docs.djangoproject.com/en/stable/ref/settings/#caches).
Значение по умолчанию бэкэнд «locmemcache» должно быть в порядке для простых настроек.
См. Django's [Documentation] (https://docs.djangoproject.com/en/stable/topics/cache/#setting-the-cache) для получения более подробной информации.

If you need to use a cache other than `'default'`, you can do so by creating a custom throttle class and setting the `cache` attribute.  For example:

Если вам нужно использовать кэш, отличный от «по умолчанию», вы можете сделать это, создав пользовательский класс дроссельной заслонки и установив атрибут `cache '.
Например:

```
from django.core.cache import caches

class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```

You'll need to remember to also set your custom throttle class in the `'DEFAULT_THROTTLE_CLASSES'` settings key, or using the `throttle_classes` view attribute.

Вам нужно будет помнить, чтобы также установить свой пользовательский класс дроссельной заслонки в клавише «DEFAULT_THROTTLE_CLASSES» или использование атрибута View `THOTTLE_CLASSES`.

## A note on concurrency

## записка о параллелизме

The built-in throttle implementations are open to [race conditions](https://en.wikipedia.org/wiki/Race_condition#Data_race), so under high concurrency they may allow a few extra requests through.

Встроенные реализации дроссельной заслонки открыты для [условий гонки] (https://en.wikipedia.org/wiki/race_condition#data_race), поэтому при высоком параллеле они могут разрешить несколько дополнительных запросов.

If your project relies on guaranteeing the number of requests during concurrent requests, you will need to implement your own throttle class. See [issue #5181](https://github.com/encode/django-rest-framework/issues/5181) for more details.

Если ваш проект полагается на гарантирование количества запросов во время параллельных запросов, вам нужно будет внедрить свой собственный класс дроссельной заслонки.
См. [Выпуск № 5181] (https://github.com/encode/django-rest-framework/issues/5181) для получения дополнительной информации.

---

# API Reference

# Ссылка на API

## AnonRateThrottle

## anonratethrottle

The `AnonRateThrottle` will only ever throttle unauthenticated users.  The IP address of the incoming request is used to generate a unique key to throttle against.

`Anonratethrottle 'будет только что -либо газовать пользователей.
IP -адрес входящего запроса используется для генерации уникального ключа для дросселя.

The allowed request rate is determined from one of the following (in order of preference).

Разрешенная ставка запроса определяется по одному из следующих (в порядке предпочтения).

* The `rate` property on the class, which may be provided by overriding `AnonRateThrottle` and setting the property.
* The `DEFAULT_THROTTLE_RATES['anon']` setting.

* Свойство `` `на классе, которое может быть предоставлено, переопределив` anonratethrottle 'и установив свойство.
* Настройка `default_throttle_rates ['anon']`.

`AnonRateThrottle` is suitable if you want to restrict the rate of requests from unknown sources.

`Anonratethrottle 'подходит, если вы хотите ограничить скорость запросов из неизвестных источников.

## UserRateThrottle

## userratethrottle

The `UserRateThrottle` will throttle users to a given rate of requests across the API.  The user id is used to generate a unique key to throttle against.  Unauthenticated requests will fall back to using the IP address of the incoming request to generate a unique key to throttle against.

`Userratethrottle 'приведет пользователей до заданного ставки запросов по всему API.
Идентификатор пользователя используется для генерации уникального ключа для дросселя.
Неавтотимированные запросы вернутся к использованию IP -адреса входящего запроса для создания уникального ключа для дросселя.

The allowed request rate is determined from one of the following (in order of preference).

Разрешенная ставка запроса определяется по одному из следующих (в порядке предпочтения).

* The `rate` property on the class, which may be provided by overriding `UserRateThrottle` and setting the property.
* The `DEFAULT_THROTTLE_RATES['user']` setting.

* Свойство `` `на классе, которое может быть предоставлено, переопределив` userratethrottle 'и установив свойство.
* Настройка `default_throttle_rates ['user']`.

An API may have multiple `UserRateThrottles` in place at the same time.  To do so, override `UserRateThrottle` and set a unique "scope" for each class.

API может иметь несколько `userratethrottles 'на месте одновременно.
Для этого переопределите `userratethrottle` и установите уникальный« сферу »для каждого класса.

For example, multiple user throttle rates could be implemented by using the following classes...

Например, несколько ставок дроссельной заслонки пользователя могут быть реализованы с помощью следующих классов ...

```
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

...and the following settings.

... и следующие настройки.

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

`Userratethrottle 'подходит, если вы хотите простые глобальные ограничения на тарифную на пользователя.

## ScopedRateThrottle

## scopedratethrottle

The `ScopedRateThrottle` class can be used to restrict access to specific parts of the API.  This throttle will only be applied if the view that is being accessed includes a `.throttle_scope` property.  The unique throttle key will then be formed by concatenating the "scope" of the request with the unique user id or IP address.

Класс `scopedratethrottle можно использовать для ограничения доступа к определенным частям API.
Этот дроссель будет применяться только в том случае, если доступ к доступу, включает свойство `.Throttle_scope`.
Затем уникальный ключ дроссельной заслонки будет сформирован путем объединения «область» запроса с уникальным идентификатором пользователя или IP -адресом.

The allowed request rate is determined by the `DEFAULT_THROTTLE_RATES` setting using a key from the request "scope".

Разрешенная скорость запроса определяется с помощью настройки `default_throttle_rates` с использованием клавиши из запроса" Scope ".

For example, given the following views...

Например, учитывая следующие представления ...

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

... и следующие настройки.

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

User requests to either `ContactListView` or `ContactDetailView` would be restricted to a total of 1000 requests per-day.  User requests to `UploadView` would be restricted to 20 requests per day.

Запросы пользователя либо `contactListView`, либо` contactDetailView` будут ограничены в общей сложности до 1000 запросов в день.
Запросы пользователя на `uploadView` будут ограничены 20 запросами в день.

---

# Custom throttles

# Пользовательские дроссели

To create a custom throttle, override `BaseThrottle` and implement `.allow_request(self, request, view)`.  The method should return `True` if the request should be allowed, and `False` otherwise.

Чтобы создать пользовательский газ, переопределите `basethrottle` и реализуйте` .ally_request (self, запрос, просмотр) `.
Метод должен вернуть `true`, если запрос должен быть разрешен, и иначе` false.

Optionally you may also override the `.wait()` method.  If implemented, `.wait()` should return a recommended number of seconds to wait before attempting the next request, or `None`.  The `.wait()` method will only be called if `.allow_request()` has previously returned `False`.

При желании вы также можете переопределить метод `.wait ()`.
В случае реализации `.wait ()` должен вернуть рекомендуемое количество секунд, чтобы подождать, прежде чем попытаться сделать следующий запрос, или «нет».
Метод `.wait ()` будет вызван только если `.Allow_Request ()` ранее возвращал `false`.

If the `.wait()` method is implemented and the request is throttled, then a `Retry-After` header will be included in the response.

Если метод `.wait ()` реализован, и запрос запускается, то заголовок `retry-after 'будет включен в ответ.

## Example

## Пример

The following is an example of a rate throttle, that will randomly throttle 1 in every 10 requests.

Ниже приведен пример дроссельной заслонки скорости, который случайным образом гаснет 1 за каждые 10 запросов.

```
import random

class RandomRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
```