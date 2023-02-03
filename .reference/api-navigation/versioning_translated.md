<!-- TRANSLATED by md-translate -->
---

source:

источник:

* versioning.py

* versioning.py

---

# Versioning

# Версионирование

> Versioning an interface is just a "polite" way to kill deployed clients.
>
> — [Roy Fielding][cite].

> Версионирование интерфейса - это просто "вежливый" способ убить развернутых клиентов.
>
> - [Рой Филдинг][cite].

API versioning allows you to alter behavior between different clients. REST framework provides for a number of different versioning schemes.

Версионность API позволяет изменять поведение различных клиентов. Фреймворк REST предусматривает несколько различных схем версионирования.

Versioning is determined by the incoming client request, and may either be based on the request URL, or based on the request headers.

Версионность определяется входящим запросом клиента и может быть основана либо на URL запроса, либо на заголовках запроса.

There are a number of valid approaches to approaching versioning. [Non-versioned systems can also be appropriate][roy-fielding-on-versioning], particularly if you're engineering for very long-term systems with multiple clients outside of your control.

Существует несколько правильных подходов к определению версий. [Неверсионные системы также могут быть уместны][roy-fielding-on-versioning], особенно если вы разрабатываете очень долгосрочные системы с множеством клиентов вне вашего контроля.

## Versioning with REST framework

## Версионирование с помощью REST-фреймворка

When API versioning is enabled, the `request.version` attribute will contain a string that corresponds to the version requested in the incoming client request.

Если версионность API включена, атрибут `request.version` будет содержать строку, соответствующую версии, запрошенной во входящем клиентском запросе.

By default, versioning is not enabled, and `request.version` will always return `None`.

По умолчанию версионность не включена, и `request.version` всегда будет возвращать `None`.

#### Varying behavior based on the version

#### Различное поведение в зависимости от версии

How you vary the API behavior is up to you, but one example you might typically want is to switch to a different serialization style in a newer version. For example:

Как вы будете изменять поведение API, зависит от вас, но один из примеров, который обычно может понадобиться, - это переход на другой стиль сериализации в новой версии. Например:

```
def get_serializer_class(self):
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
```

#### Reversing URLs for versioned APIs

#### Обратные URL для версионных API

The `reverse` function included by REST framework ties in with the versioning scheme. You need to make sure to include the current `request` as a keyword argument, like so.

Функция `reverse`, включенная во фреймворк REST, связана со схемой версионирования. Вам нужно убедиться, что вы включили текущий `request` в качестве аргумента ключевого слова, как, например.

```
from rest_framework.reverse import reverse

reverse('bookings-list', request=request)
```

The above function will apply any URL transformations appropriate to the request version. For example:

Приведенная выше функция будет применять любые преобразования URL, соответствующие версии запроса. Например:

* If `NamespaceVersioning` was being used, and the API version was 'v1', then the URL lookup used would be `'v1:bookings-list'`, which might resolve to a URL like `http://example.org/v1/bookings/`.
* If `QueryParameterVersioning` was being used, and the API version was `1.0`, then the returned URL might be something like `http://example.org/bookings/?version=1.0`

* Если используется `NamespaceVersioning`, и версия API равна 'v1', то для поиска URL используется `'v1:bookings-list'`, что может привести к URL типа `http://example.org/v1/bookings/`.
* Если используется `QueryParameterVersioning', и версия API была `1.0', то возвращаемый URL может быть чем-то вроде `http://example.org/bookings/?version=1.0'.

#### Versioned APIs and hyperlinked serializers

#### Версифицированные API и сериализаторы с гиперссылками

When using hyperlinked serialization styles together with a URL based versioning scheme make sure to include the request as context to the serializer.

При использовании стилей сериализации с гиперссылками вместе со схемой версионирования на основе URL обязательно включайте запрос в качестве контекста для сериализатора.

```
def get(self, request):
    queryset = Booking.objects.all()
    serializer = BookingsSerializer(queryset, many=True, context={'request': request})
    return Response({'all_bookings': serializer.data})
```

Doing so will allow any returned URLs to include the appropriate versioning.

Это позволит всем возвращаемым URL-адресам включать соответствующие версии.

## Configuring the versioning scheme

## Настройка схемы версионирования

The versioning scheme is defined by the `DEFAULT_VERSIONING_CLASS` settings key.

Схема версионирования определяется ключом настройки `DEFAULT_VERSIONING_CLASS`.

```
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
```

Unless it is explicitly set, the value for `DEFAULT_VERSIONING_CLASS` will be `None`. In this case the `request.version` attribute will always return `None`.

Если оно не задано явно, значение для `DEFAULT_VERSIONING_CLASS` будет равно `None`. В этом случае атрибут `request.version` всегда будет возвращать `None`.

You can also set the versioning scheme on an individual view. Typically you won't need to do this, as it makes more sense to have a single versioning scheme used globally. If you do need to do so, use the `versioning_class` attribute.

Вы также можете установить схему версионирования для отдельного представления. Обычно вам не нужно этого делать, поскольку логичнее иметь единую схему версионирования, используемую глобально. Если это необходимо, используйте атрибут `versioning_class`.

```
class ProfileList(APIView):
    versioning_class = versioning.QueryParameterVersioning
```

#### Other versioning settings

#### Другие параметры версионирования

The following settings keys are also used to control versioning:

Следующие ключи настроек также используются для управления версионированием:

* `DEFAULT_VERSION`. The value that should be used for `request.version` when no versioning information is present. Defaults to `None`.
* `ALLOWED_VERSIONS`. If set, this value will restrict the set of versions that may be returned by the versioning scheme, and will raise an error if the provided version is not in this set. Note that the value used for the `DEFAULT_VERSION` setting is always considered to be part of the `ALLOWED_VERSIONS` set (unless it is `None`). Defaults to `None`.
* `VERSION_PARAM`. The string that should be used for any versioning parameters, such as in the media type or URL query parameters. Defaults to `'version'`.

* `DEFAULT_VERSION`. Значение, которое должно использоваться для `request.version`, когда информация о версиях отсутствует. По умолчанию `None`.
* ``РАЗРЕШЕННЫЕ_ВЕРСИИ``. Если задано, это значение ограничивает набор версий, которые могут быть возвращены схемой версионирования, и выдает ошибку, если предоставленная версия не входит в этот набор. Обратите внимание, что значение, используемое для параметра `DEFAULT_VERSION`, всегда считается частью набора `ALLOWED_VERSIONS` (если оно не равно `None`). По умолчанию `None`.
* `VERSION_PARAM`. Строка, которая должна использоваться для любых параметров версионирования, например, в типе медиа или параметрах запроса URL. По умолчанию имеет значение `'version'`.

You can also set your versioning class plus those three values on a per-view or a per-viewset basis by defining your own versioning scheme and using the `default_version`, `allowed_versions` and `version_param` class variables. For example, if you want to use `URLPathVersioning`:

Вы также можете установить свой класс версионности плюс эти три значения на основе каждого представления или каждого набора представлений, определив свою собственную схему версионности и используя переменные класса `default_version`, `allowed_versions` и `version_param`. Например, если вы хотите использовать `URLPathVersioning`:

```
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView

class ExampleVersioning(URLPathVersioning):
    default_version = ...
    allowed_versions = ...
    version_param = ...

class ExampleView(APIVIew):
    versioning_class = ExampleVersioning
```

---

# API Reference

# API Reference

## AcceptHeaderVersioning

## AcceptHeaderVersioning

This scheme requires the client to specify the version as part of the media type in the `Accept` header. The version is included as a media type parameter, that supplements the main media type.

Эта схема требует от клиента указать версию как часть типа медиа в заголовке `Accept`. Версия включается в качестве параметра медиатипа, дополняющего основной медиатип.

Here's an example HTTP request using the accept header versioning style.

Вот пример HTTP-запроса с использованием стиля версионирования заголовка accept.

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

In the example request above `request.version` attribute would return the string `'1.0'`.

В приведенном выше примере запроса атрибут `request.version` вернет строку `'1.0'`.

Versioning based on accept headers is [generally considered](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned) as [best practice](https://github.com/interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md), although other styles may be suitable depending on your client requirements.

Версионирование на основе принимаемых заголовков [обычно рассматривается](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned) как [лучшая практика](https://github.com/interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md), хотя в зависимости от требований клиента могут подойти и другие стили.

#### Using accept headers with vendor media types

#### Использование заголовков accept с медиатипами поставщиков

Strictly speaking the `json` media type is not specified as [including additional parameters](https://tools.ietf.org/html/rfc4627#section-6). If you are building a well-specified public API you might consider using a [vendor media type](https://en.wikipedia.org/wiki/Internet_media_type#Vendor_tree). To do so, configure your renderers to use a JSON based renderer with a custom media type:

Строго говоря, медиатип `json` не указан как [включающий дополнительные параметры](https://tools.ietf.org/html/rfc4627#section-6). Если вы создаете хорошо специфицированный публичный API, вы можете рассмотреть возможность использования [vendor media type](https://en.wikipedia.org/wiki/Internet_media_type#Vendor_tree). Для этого настройте свои рендереры на использование рендерера на основе JSON с пользовательским медиатипом:

```
class BookingsAPIRenderer(JSONRenderer):
    media_type = 'application/vnd.megacorp.bookings+json'
```

Your client requests would now look like this:

Теперь ваши клиентские запросы будут выглядеть следующим образом:

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/vnd.megacorp.bookings+json; version=1.0
```

## URLPathVersioning

## URLPathVersioning

This scheme requires the client to specify the version as part of the URL path.

Эта схема требует, чтобы клиент указывал версию как часть пути URL.

```
GET /v1/bookings/ HTTP/1.1
Host: example.com
Accept: application/json
```

Your URL conf must include a pattern that matches the version with a `'version'` keyword argument, so that this information is available to the versioning scheme.

Ваш URL conf должен включать шаблон, соответствующий версии, с аргументом ключевого слова `'version'`, чтобы эта информация была доступна схеме версионирования.

```
urlpatterns = [
    re_path(
        r'^(?P<version>(v1|v2))/bookings/$',
        bookings_list,
        name='bookings-list'
    ),
    re_path(
        r'^(?P<version>(v1|v2))/bookings/(?P<pk>[0-9]+)/$',
        bookings_detail,
        name='bookings-detail'
    )
]
```

## NamespaceVersioning

## NamespaceVersioning

To the client, this scheme is the same as `URLPathVersioning`. The only difference is how it is configured in your Django application, as it uses URL namespacing, instead of URL keyword arguments.

Для клиента эта схема аналогична `URLPathVersioning`. Единственное различие заключается в том, как она настраивается в вашем приложении Django, поскольку она использует интервалы между именами URL, вместо аргументов ключевых слов URL.

```
GET /v1/something/ HTTP/1.1
Host: example.com
Accept: application/json
```

With this scheme the `request.version` attribute is determined based on the `namespace` that matches the incoming request path.

При такой схеме атрибут `request.version` определяется на основе `namespace`, соответствующего пути входящего запроса.

In the following example we're giving a set of views two different possible URL prefixes, each under a different namespace:

В следующем примере мы даем набору представлений два различных возможных префикса URL, каждый из которых относится к разным пространствам имен:

```
# bookings/urls.py
urlpatterns = [
    re_path(r'^$', bookings_list, name='bookings-list'),
    re_path(r'^(?P<pk>[0-9]+)/$', bookings_detail, name='bookings-detail')
]

# urls.py
urlpatterns = [
    re_path(r'^v1/bookings/', include('bookings.urls', namespace='v1')),
    re_path(r'^v2/bookings/', include('bookings.urls', namespace='v2'))
]
```

Both `URLPathVersioning` and `NamespaceVersioning` are reasonable if you just need a simple versioning scheme. The `URLPathVersioning` approach might be better suitable for small ad-hoc projects, and the `NamespaceVersioning` is probably easier to manage for larger projects.

И `URLPathVersioning`, и `NamespaceVersioning` разумны, если вам нужна простая схема версионирования. Подход `URLPathVersioning` может лучше подойти для небольших специальных проектов, а `NamespaceVersioning`, вероятно, проще в управлении для больших проектов.

## HostNameVersioning

## HostNameVersioning

The hostname versioning scheme requires the client to specify the requested version as part of the hostname in the URL.

Схема версионности имени хоста требует от клиента указать запрашиваемую версию как часть имени хоста в URL.

For example the following is an HTTP request to the `http://v1.example.com/bookings/` URL:

Например, ниже приведен HTTP-запрос к URL `http://v1.example.com/bookings/`:

```
GET /bookings/ HTTP/1.1
Host: v1.example.com
Accept: application/json
```

By default this implementation expects the hostname to match this simple regular expression:

По умолчанию эта реализация ожидает, что имя хоста будет соответствовать этому простому регулярному выражению:

```
^([a-zA-Z0-9]+)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+$
```

Note that the first group is enclosed in brackets, indicating that this is the matched portion of the hostname.

Обратите внимание, что первая группа заключена в скобки, что указывает на то, что это совпадающая часть имени хоста.

The `HostNameVersioning` scheme can be awkward to use in debug mode as you will typically be accessing a raw IP address such as `127.0.0.1`. There are various online tutorials on how to [access localhost with a custom subdomain](https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains) which you may find helpful in this case.

Схема `HostNameVersioning` может быть неудобна для использования в режиме отладки, так как обычно вы обращаетесь к необработанному IP-адресу, например, `127.0.0.1`. Существуют различные онлайн-уроки о том, как [получить доступ к localhost с пользовательским поддоменом](https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains), которые могут оказаться полезными в этом случае.

Hostname based versioning can be particularly useful if you have requirements to route incoming requests to different servers based on the version, as you can configure different DNS records for different API versions.

Версионность на основе имени хоста может быть особенно полезна, если у вас есть требования направлять входящие запросы на разные серверы в зависимости от версии, поскольку вы можете настроить разные записи DNS для разных версий API.

## QueryParameterVersioning

## QueryParameterVersioning

This scheme is a simple style that includes the version as a query parameter in the URL. For example:

Эта схема представляет собой простой стиль, который включает версию в качестве параметра запроса в URL. Например:

```
GET /something/?version=0.1 HTTP/1.1
Host: example.com
Accept: application/json
```

---

# Custom versioning schemes

# Пользовательские схемы версионирования

To implement a custom versioning scheme, subclass `BaseVersioning` and override the `.determine_version` method.

Для реализации пользовательской схемы версионирования, подкласс `BaseVersioning` и переопределите метод `.determine_version`.

## Example

## Пример

The following example uses a custom `X-API-Version` header to determine the requested version.

В следующем примере используется пользовательский заголовок `X-API-Version` для определения запрашиваемой версии.

```
class XAPIVersionScheme(versioning.BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get('HTTP_X_API_VERSION', None)
```

If your versioning scheme is based on the request URL, you will also want to alter how versioned URLs are determined. In order to do so you should override the `.reverse()` method on the class. See the source code for examples.

Если ваша схема версионирования основана на URL запроса, вы также захотите изменить способ определения версионированных URL. Для этого вам следует переопределить метод `.reverse()` в классе. Примеры см. в исходном коде.