<!-- TRANSLATED by md-translate -->
---

source:

источник:

* versioning.py

* versioning.py

---

# Versioning

# Версии

> Versioning an interface is just a "polite" way to kill deployed clients.
>
> — [Roy Fielding][cite].

> Версия Интерфейс - это просто «вежливый» способ убить развернутых клиентов.
>
> - [Roy Fielding] [цитирует].

API versioning allows you to alter behavior between different clients. REST framework provides for a number of different versioning schemes.

Версия API позволяет изменить поведение между различными клиентами.
Framework REST предусматривает ряд различных схем управления версиями.

Versioning is determined by the incoming client request, and may either be based on the request URL, or based on the request headers.

Разведение версий определяется входящим запросом клиента и может быть основано на URL -адресе запроса или на основе заголовков запроса.

There are a number of valid approaches to approaching versioning. [Non-versioned systems can also be appropriate][roy-fielding-on-versioning], particularly if you're engineering for very long-term systems with multiple clients outside of your control.

Существует ряд действительных подходов к приближению к версии.
[Неверсированные системы также могут быть подходящими] [Roy-пополнение на версии], особенно если вы разработаете для очень долгосрочных систем с несколькими клиентами вне вашего контроля.

## Versioning with REST framework

## версии с помощью Framework REST

When API versioning is enabled, the `request.version` attribute will contain a string that corresponds to the version requested in the incoming client request.

При включении версии API атрибут `request.version` будет содержать строку, которая соответствует версии, запрошенной в входящем клиентском запросе.

By default, versioning is not enabled, and `request.version` will always return `None`.

По умолчанию, управление версией не включено, а `request.version` всегда будет возвращать` none`.

#### Varying behavior based on the version

#### различное поведение на основе версии

How you vary the API behavior is up to you, but one example you might typically want is to switch to a different serialization style in a newer version. For example:

То, как вы варьируете поведение API, зависит от вас, но один из примеров, который вы обычно хотите, - это переключиться на другой стиль сериализации в более новой версии.
Например:

```
def get_serializer_class(self):
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
```

#### Reversing URLs for versioned APIs

#### Реверсирование URL -адресов для версий API

The `reverse` function included by REST framework ties in with the versioning scheme. You need to make sure to include the current `request` as a keyword argument, like so.

Функция `обратно, включенная в рамках REST Framework, связана со схемой версий.
Вам необходимо убедиться, что текущий аргумент «запрос» в качестве аргумента ключевого слова, как и так.

```
from rest_framework.reverse import reverse

reverse('bookings-list', request=request)
```

The above function will apply any URL transformations appropriate to the request version. For example:

Приведенная выше функция будет применять любые преобразования URL -адреса, соответствующие версии запроса.
Например:

* If `NamespaceVersioning` was being used, and the API version was 'v1', then the URL lookup used would be `'v1:bookings-list'`, which might resolve to a URL like `http://example.org/v1/bookings/`.
* If `QueryParameterVersioning` was being used, and the API version was `1.0`, then the returned URL might be something like `http://example.org/bookings/?version=1.0`

* Если бы использовался `namespaceversioning`, и версия API была« v1 », то использованный URL-поиск был бы« v1: list », который мог бы решить на URL, как` http://example.org
/v1/заказы/`.
* Если использовался `QueryParameterVeringing`, и версия API была` 1.0`, то возвращенный URL -адрес может быть чем -то вроде `http: //example.org/bookings/? Version = 1.0`

#### Versioned APIs and hyperlinked serializers

#### версии API и гиперссыщенные сериалы

When using hyperlinked serialization styles together with a URL based versioning scheme make sure to include the request as context to the serializer.

При использовании гиперсвязанных стилей сериализации вместе со схемой версий на основе URL -адресов обязательно включите запрос в качестве контекста для сериализатора.

```
def get(self, request):
    queryset = Booking.objects.all()
    serializer = BookingsSerializer(queryset, many=True, context={'request': request})
    return Response({'all_bookings': serializer.data})
```

Doing so will allow any returned URLs to include the appropriate versioning.

Это позволит любым возвращенным URL -адресам включать соответствующее управление версиями.

## Configuring the versioning scheme

## Настройка схемы управления версиями

The versioning scheme is defined by the `DEFAULT_VERSIONING_CLASS` settings key.

Схема управления версиями определяется ключом настройки `default_versioning_class`.

```
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
```

Unless it is explicitly set, the value for `DEFAULT_VERSIONING_CLASS` will be `None`. In this case the `request.version` attribute will always return `None`.

Если это не установлено явно, значение для `default_versioning_class` будет« нет ».
В этом случае атрибут `request.version` всегда будет возвращать« нет ».

You can also set the versioning scheme on an individual view. Typically you won't need to do this, as it makes more sense to have a single versioning scheme used globally. If you do need to do so, use the `versioning_class` attribute.

Вы также можете установить схему управления версиями в отдельном представлении.
Как правило, вам не нужно это делать, так как имеет смысл использовать одну схему управления версиями, используемая во всем мире.
Если вам нужно это сделать, используйте атрибут `versioning_class`.

```
class ProfileList(APIView):
    versioning_class = versioning.QueryParameterVersioning
```

#### Other versioning settings

#### Другие настройки управления версиями

The following settings keys are also used to control versioning:

Следующие клавиши настроек также используются для управления инициацией версий:

* `DEFAULT_VERSION`. The value that should be used for `request.version` when no versioning information is present. Defaults to `None`.
* `ALLOWED_VERSIONS`. If set, this value will restrict the set of versions that may be returned by the versioning scheme, and will raise an error if the provided version is not in this set. Note that the value used for the `DEFAULT_VERSION` setting is always considered to be part of the `ALLOWED_VERSIONS` set (unless it is `None`). Defaults to `None`.
* `VERSION_PARAM`. The string that should be used for any versioning parameters, such as in the media type or URL query parameters. Defaults to `'version'`.

* `Default_version`.
Значение, которое следует использовать для `request.version`, когда информация об управлении версией не присутствует.
По умолчанию «нет».
* `Alling_versions`.
Если установлено, это значение ограничит набор версий, которые могут быть возвращены схемой версий, и вынесет ошибку, если предоставленная версия не будет в этом наборе.
Обратите внимание, что значение, используемое для параметра `default_version
По умолчанию «нет».
* `Version_param`.
Строка, которая должна использоваться для любых параметров управления версией, например, в параметрах типа среды или параметров запроса URL.
По умолчанию к «версии».

You can also set your versioning class plus those three values on a per-view or a per-viewset basis by defining your own versioning scheme and using the `default_version`, `allowed_versions` and `version_param` class variables. For example, if you want to use `URLPathVersioning`:

Вы также можете установить свой класс версий плюс эти три значения для каждого просмотра или на основе для каждого размер, определив свою собственную схему управления версией и используя переменные класса `default_version`,` allow_versions` и `version_param`.
Например, если вы хотите использовать `urlPathversioning`:

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

# Ссылка на API

## AcceptHeaderVersioning

## accomtheaderversioning

This scheme requires the client to specify the version as part of the media type in the `Accept` header. The version is included as a media type parameter, that supplements the main media type.

Эта схема требует, чтобы клиент указал версию как часть типа носителя в заголовке `Accept`.
Версия включена в качестве параметра типа носителя, который дополняет основной тип носителя.

Here's an example HTTP request using the accept header versioning style.

Вот пример HTTP -запрос, используя стиль версии версии Accept.

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

In the example request above `request.version` attribute would return the string `'1.0'`.

В примере запроса выше `request.version` attribute вернет строку` '1.0'.

Versioning based on accept headers is [generally considered](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned) as [best practice](https://github.com/interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md), although other styles may be suitable depending on your client requirements.

Разведение версий, основанное на заголовках принятия, [как правило,] (http://blog.steveklabnik.com/posts/2011-07-03-nobody-sronstands-rest-or-http#i_want_my_api_to_bersed) как [наилучшая практика] (https://
/github.com/Interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md), хотя другие стили могут подходить в зависимости от требований вашего клиента.

#### Using accept headers with vendor media types

#### Использование заголовков Accept с типами медиа -поставщиков

Strictly speaking the `json` media type is not specified as [including additional parameters](https://tools.ietf.org/html/rfc4627#section-6). If you are building a well-specified public API you might consider using a [vendor media type](https://en.wikipedia.org/wiki/Internet_media_type#Vendor_tree). To do so, configure your renderers to use a JSON based renderer with a custom media type:

Строго говоря, тип медиа json` не указан как [включая дополнительные параметры] (https://tools.ietf.org/html/rfc4627#section-6).
Если вы создаете хорошо указанный публичный API, вы можете рассмотреть возможность использования [типа поставщика медиа] (https://en.wikipedia.org/wiki/internet_media_type#vendor_tree).
Для этого настройте рендериторы для использования рендеринга на основе JSON с помощью пользовательского типа носителя:

```
class BookingsAPIRenderer(JSONRenderer):
    media_type = 'application/vnd.megacorp.bookings+json'
```

Your client requests would now look like this:

Ваши запросы клиента теперь будут выглядеть так:

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/vnd.megacorp.bookings+json; version=1.0
```

## URLPathVersioning

## urlpathversioning

This scheme requires the client to specify the version as part of the URL path.

Эта схема требует от клиента указать версию как часть пути URL.

```
GET /v1/bookings/ HTTP/1.1
Host: example.com
Accept: application/json
```

Your URL conf must include a pattern that matches the version with a `'version'` keyword argument, so that this information is available to the versioning scheme.

Ваш URL Conf должен включать шаблон, который соответствует версии с аргументом ключевого слова «версия», чтобы эта информация была доступна для схемы управления версиями.

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

## namespaceversioning

To the client, this scheme is the same as `URLPathVersioning`. The only difference is how it is configured in your Django application, as it uses URL namespacing, instead of URL keyword arguments.

Для клиента эта схема такая же, как и `urlpathversioning.
Единственное отличие заключается в том, как он настроен в вашем приложении Django, поскольку он использует пространство имен URL, вместо аргументов ключевых слов URL.

```
GET /v1/something/ HTTP/1.1
Host: example.com
Accept: application/json
```

With this scheme the `request.version` attribute is determined based on the `namespace` that matches the incoming request path.

С этой схемой атрибут `request.version` определяется на основе« пространства имен », который соответствует входящему пути запроса.

In the following example we're giving a set of views two different possible URL prefixes, each under a different namespace:

В следующем примере мы даем набор представлений о двух разных возможных префиксах URL, каждый из которых находится под другим пространством имен:

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

Как `urlPathversioning, так и` namespaceversioning` являются разумными, если вам просто нужна простая схема управления версиями.
Подход `urlpathversioning 'может быть лучше подходит для небольших специальных проектов, а« именам пространства », вероятно, легче управлять для более крупных проектов.

## HostNameVersioning

## hostnameversioning

The hostname versioning scheme requires the client to specify the requested version as part of the hostname in the URL.

Схема управления версиями HostName требует, чтобы клиент указал запрошенную версию как часть имени HOSTN в URL.

For example the following is an HTTP request to the `http://v1.example.com/bookings/` URL:

Например, следующее приведено http -запрос на `http: // v1.example.com/bookings/` url:

```
GET /bookings/ HTTP/1.1
Host: v1.example.com
Accept: application/json
```

By default this implementation expects the hostname to match this simple regular expression:

По умолчанию эта реализация ожидает, что имя хоста соответствует этому простому регулярному выражению:

```
^([a-zA-Z0-9]+)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+$
```

Note that the first group is enclosed in brackets, indicating that this is the matched portion of the hostname.

Обратите внимание, что первая группа заключена в скобки, что указывает на то, что это соответствующая часть имени хоста.

The `HostNameVersioning` scheme can be awkward to use in debug mode as you will typically be accessing a raw IP address such as `127.0.0.1`. There are various online tutorials on how to [access localhost with a custom subdomain](https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains) which you may find helpful in this case.

Схема `hostnameversioning` может быть неловко использовать в режиме отладки, так как вы обычно получаете доступ к необработанному IP -адресу, такому как` 127.0.0.1`.
Существуют различные онлайн-учебники о том, как [получить доступ к Localhost с помощью пользовательского субдомена] (https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains), которые вы можете найти в этом
кейс.

Hostname based versioning can be particularly useful if you have requirements to route incoming requests to different servers based on the version, as you can configure different DNS records for different API versions.

Использование версий на основе HostName может быть особенно полезным, если у вас есть требования к маршрутизации входящих запросов на разные серверы на основе версии, поскольку вы можете настроить различные записи DNS для различных версий API.

## QueryParameterVersioning

## Queryparameterversioning

This scheme is a simple style that includes the version as a query parameter in the URL. For example:

Эта схема - простой стиль, который включает в себя версию как параметр запроса в URL.
Например:

```
GET /something/?version=0.1 HTTP/1.1
Host: example.com
Accept: application/json
```

---

# Custom versioning schemes

# Индивидуальные схемы управления версиями

To implement a custom versioning scheme, subclass `BaseVersioning` and override the `.determine_version` method.

Чтобы реализовать пользовательскую схему управления версиями, подкласс `baseversioning` и переопределить метод` .determine_version '.

## Example

## Пример

The following example uses a custom `X-API-Version` header to determine the requested version.

В следующем примере используется пользовательский заголовок `x-api-version` для определения запрошенной версии.

```
class XAPIVersionScheme(versioning.BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get('HTTP_X_API_VERSION', None)
```

If your versioning scheme is based on the request URL, you will also want to alter how versioned URLs are determined. In order to do so you should override the `.reverse()` method on the class. See the source code for examples.

Если ваша схема управления версиями основана на URL -адресе запроса, вы также захотите изменить определение версий URL -адресов.
Чтобы сделать это, вы должны переопределить метод `.reverse ()` на классе.
Смотрите исходный код для примеров.