<!-- TRANSLATED by md-translate -->
# Версионирование

> Версионирование интерфейса - это просто "вежливый" способ убить развернутых клиентов.
>
> - [Рой Филдинг](https://www.slideshare.net/evolve_conference/201308-fielding-evolve/31).

Версионность API позволяет изменять поведение различных клиентов. DRF предусматривает несколько различных схем версионирования.

Версионность определяется входящим запросом клиента и может быть основана либо на URL запроса, либо на заголовках запроса.

Существует несколько правильных подходов к определению версий. [Неверсионированные системы также могут быть уместны](https://www.infoq.com/articles/roy-fielding-on-versioning), особенно если вы разрабатываете очень долгосрочные системы с множеством клиентов вне вашего контроля.

## Версионирование с помощью DRF

Если версионность API включена, атрибут `request.version` будет содержать строку, соответствующую версии, запрошенной во входящем клиентском запросе.

По умолчанию версионность не включена, и `request.version` всегда будет возвращать `None`.

#### Различное поведение в зависимости от версии

Как вы будете изменять поведение API, зависит от вас, но один из примеров, который обычно может понадобиться, - это переход на другой стиль сериализации в новой версии. Например:

```python
def get_serializer_class(self):
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
```

#### Обратные URL для версионных API

Функция `reverse`, включенная в DRF, связана со схемой версионирования. Вам нужно убедиться, что вы включили текущий `request` в качестве именованного аргумента, как, например.

```python
from rest_framework.reverse import reverse

reverse('bookings-list', request=request)
```

Приведенная выше функция будет применять любые преобразования URL, соответствующие версии запроса. Например:

* Если используется `NamespaceVersioning`, и версия API равна 'v1', то для поиска URL используется `'v1:bookings-list'`, что может привести к URL типа `http://example.org/v1/bookings/`.
* Если используется `QueryParameterVersioning`, и версия API была '1.0', то возвращаемый URL может быть чем-то вроде `http://example.org/bookings/?version=1.0`.

#### Версифицированные API и сериализаторы с гиперссылками

При использовании стилей сериализации с гиперссылками вместе со схемой версионирования на основе URL обязательно включайте запрос в качестве контекста для сериализатора.

```python
def get(self, request):
    queryset = Booking.objects.all()
    serializer = BookingsSerializer(queryset, many=True, context={'request': request})
    return Response({'all_bookings': serializer.data})
```

Это позволит всем возвращаемым URL-адресам включать соответствующие версии.

## Настройка схемы версионирования

Схема версионирования определяется ключом настройки `DEFAULT_VERSIONING_CLASS`.

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
```

Если оно не задано явно, значение для `DEFAULT_VERSIONING_CLASS` будет равно `None`. В этом случае атрибут `request.version` всегда будет возвращать `None`.

Вы также можете установить схему версионирования для отдельного представления. Обычно вам не нужно этого делать, поскольку логичнее иметь единую схему версионирования, используемую глобально. Если это необходимо, используйте атрибут `versioning_class`.

```python
class ProfileList(APIView):
    versioning_class = versioning.QueryParameterVersioning
```

#### Другие параметры версионирования

Следующие ключи настроек также используются для управления версионированием:

* `DEFAULT_VERSION`. Значение, которое должно использоваться для `request.version`, когда информация о версиях отсутствует. По умолчанию `None`.
* `ALLOWED_VERSIONS`. Если задано, это значение ограничивает набор версий, которые могут быть возвращены схемой версионирования, и выдает ошибку, если предоставленная версия не входит в этот набор. Обратите внимание, что значение, используемое для параметра `DEFAULT_VERSION`, всегда считается частью набора `ALLOWED_VERSIONS` (если оно не равно `None`). По умолчанию `None`.
* `VERSION_PARAM`. Строка, которая должна использоваться для любых параметров версионирования, например, в типе медиа или параметрах запроса URL. По умолчанию имеет значение `'version'`.

Вы также можете установить свой класс версионности плюс эти три значения на основе каждого представления или каждого набора представлений, определив свою собственную схему версионности и используя переменные класса `default_version`, `allowed_versions` и `version_param`. Например, если вы хотите использовать `URLPathVersioning`:

```python
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

## AcceptHeaderVersioning

Эта схема требует от клиента указать версию как часть типа медиа в заголовке `Accept`. Версия включается в качестве параметра медиатипа, дополняющего основной медиатип.

Вот пример HTTP-запроса с использованием стиля версионирования заголовка accept.

```http
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

В приведенном выше примере запроса атрибут `request.version` вернет строку `'1.0'`.

Версионирование на основе принимаемых заголовков [обычно рассматривается](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned) как [лучшая практика](https://github.com/interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md), хотя в зависимости от требований клиента могут подойти и другие стили.

#### Использование заголовков accept с медиатипами поставщиков

Строго говоря, медиатип `json` не указан как [включающий дополнительные параметры](https://tools.ietf.org/html/rfc4627#section-6). Если вы создаете хорошо специфицированный публичный API, вы можете рассмотреть возможность использования [vendor media type](https://en.wikipedia.org/wiki/Internet_media_type#Vendor_tree). Для этого настройте свои рендереры на использование рендерера на основе JSON с пользовательским медиатипом:

```python
class BookingsAPIRenderer(JSONRenderer):
    media_type = 'application/vnd.megacorp.bookings+json'
```

Теперь ваши клиентские запросы будут выглядеть следующим образом:

```http
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/vnd.megacorp.bookings+json; version=1.0
```

## URLPathVersioning

Эта схема требует, чтобы клиент указывал версию как часть пути URL.

```http
GET /v1/bookings/ HTTP/1.1
Host: example.com
Accept: application/json
```

Ваш URL conf должен включать шаблон, соответствующий версии, с именованным аргументом `'version'`, чтобы эта информация была доступна схеме версионирования.

```python
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

Для клиента эта схема аналогична `URLPathVersioning`. Единственное различие заключается в том, как она настраивается в вашем приложении Django, поскольку она использует интервалы между именами URL, вместо именованных аргументов URL.

```http
GET /v1/something/ HTTP/1.1
Host: example.com
Accept: application/json
```

При такой схеме атрибут `request.version` определяется на основе `namespace`, соответствующего пути входящего запроса.

В следующем примере мы даем набору представлений два различных возможных префикса URL, каждый из которых относится к разным пространствам имен:

```python
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

И `URLPathVersioning`, и `NamespaceVersioning` разумны, если вам нужна простая схема версионирования. Подход `URLPathVersioning` может лучше подойти для небольших специальных проектов, а `NamespaceVersioning`, вероятно, проще в управлении для больших проектов.

## HostNameVersioning

Схема версионности имени хоста требует от клиента указать запрашиваемую версию как часть имени хоста в URL.

Например, ниже приведен HTTP-запрос к URL `http://v1.example.com/bookings/`:

```http
GET /bookings/ HTTP/1.1
Host: v1.example.com
Accept: application/json
```

По умолчанию эта реализация ожидает, что имя хоста будет соответствовать этому простому регулярному выражению:

```python
^([a-zA-Z0-9]+)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+$
```

Обратите внимание, что первая группа заключена в скобки, что указывает на то, что это совпадающая часть имени хоста.

Схема `HostNameVersioning` может быть неудобна для использования в режиме отладки, так как обычно вы обращаетесь к необработанному IP-адресу, например, `127.0.0.1`. Существуют различные онлайн-уроки о том, как [получить доступ к localhost с пользовательским поддоменом](https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains), которые могут оказаться полезными в этом случае.

Версионность на основе имени хоста может быть особенно полезна, если у вас есть требования направлять входящие запросы на разные серверы в зависимости от версии, поскольку вы можете настроить разные записи DNS для разных версий API.

## QueryParameterVersioning

Эта схема представляет собой простой стиль, который включает версию в качестве параметра запроса в URL. Например:

```http
GET /something/?version=0.1 HTTP/1.1
Host: example.com
Accept: application/json
```

---

# Пользовательские схемы версионирования

Для реализации пользовательской схемы версионирования, подкласс `BaseVersioning` и переопределите метод `.determine_version`.

## Пример

В следующем примере используется пользовательский заголовок `X-API-Version` для определения запрашиваемой версии.

```python
class XAPIVersionScheme(versioning.BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get('HTTP_X_API_VERSION', None)
```

Если ваша схема версионирования основана на URL запроса, вы также захотите изменить способ определения версионированных URL. Для этого вам следует переопределить метод `.reverse()` в классе. Примеры см. в исходном коде.
