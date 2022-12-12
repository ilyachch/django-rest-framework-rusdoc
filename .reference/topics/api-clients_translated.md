<!-- TRANSLATED by md-translate -->
# API Clients

# Клиенты API

An API client handles the underlying details of how network requests are made
and how responses are decoded. They present the developer with an application
interface to work against, rather than working directly with the network interface.

Клиент API обрабатывает основные данные о том, как выполняются сетевые запросы
и как ответы декодированы.
Они представляют разработчику приложение
Интерфейс для работы, вместо того, чтобы работать напрямую с сетевым интерфейсом.

The API clients documented here are not restricted to APIs built with Django REST framework.
 They can be used with any API that exposes a supported schema format.

Клиенты API, задокументированные здесь, не ограничены API, построенными в рамках Django Rest.
Их можно использовать с любым API, который разоблачает подтвержденный формат схемы.

For example, [the Heroku platform API](https://devcenter.heroku.com/categories/platform-api) exposes a schema in the JSON
Hyperschema format. As a result, the Core API command line client and Python
client library can be [used to interact with the Heroku API](https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

Например, [API платформы Heroku] (https://devcenter.heroku.com/categories/platform-api) раскрывает схему в JSON
Гипершема формат.
В результате, Core API Command Line Client и Python
Клиентская библиотека может быть [используется для взаимодействия с API Heroku] (https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

## Client-side Core API

## Client Side Core API

[Core API](https://www.coreapi.org/) is a document specification that can be used to describe APIs. It can
be used either server-side, as is done with REST framework's [schema generation](../api-guide/schemas.md),
or used client-side, as described here.

[Core API] (https://www.coreapi.org/) - это спецификация документа, которую можно использовать для описания API.
Может
использовать любую сторону сервера, как это делается с помощью Framework [Generation] (../ API-Guide/Schemas.md),
или использованный клиент, как описано здесь.

When used client-side, Core API allows for *dynamically driven client libraries*
that can interact with any API that exposes a supported schema or hypermedia
format.

При использовании на стороне клиента, Core API позволяет *динамически управляемым клиентским библиотекам *
Это может взаимодействовать с любым API, который обнажает поддерживаемую схему или гипермедию
формат.

Using a dynamically driven client has a number of advantages over interacting
with an API by building HTTP requests directly.

Использование динамически управляемого клиента имеет ряд преимуществ по сравнению с взаимодействием
с API, создавая HTTP -запросы напрямую.

#### More meaningful interaction

#### более значимое взаимодействие

API interactions are presented in a more meaningful way. You're working at
the application interface layer, rather than the network interface layer.

Взаимодействия API представлены более значимым образом.
Вы работаете над
уровень интерфейса приложения, а не уровень сетевого интерфейса.

#### Resilience & evolvability

#### Устойчивость и развитие

The client determines what endpoints are available, what parameters exist
against each particular endpoint, and how HTTP requests are formed.

Клиент определяет, какие конечные точки доступны, какие параметры существуют
против каждой конкретной конечной точки и как формируются HTTP -запросы.

This also allows for a degree of API evolvability. URLs can be modified
without breaking existing clients, or more efficient encodings can be used
on-the-wire, with clients transparently upgrading.

Это также позволяет получить степень эволюции API.
URL -адреса могут быть изменены
без нарушения существующих клиентов или более эффективных кодировки могут быть использованы
В ходе провода, клиенты прозрачно обновляются.

#### Self-descriptive APIs

#### самоопределяющие API

A dynamically driven client is able to present documentation on the API to the
end user. This documentation allows the user to discover the available endpoints
and parameters, and better understand the API they are working with.

Динамически управляемый клиент может представлять документацию на API в
конечный пользователь.
Эта документация позволяет пользователю обнаружить доступные конечные точки
и параметры, и лучше понять API, с которым они работают.

Because this documentation is driven by the API schema it will always be fully
up to date with the most recently deployed version of the service.

Поскольку эта документация обусловлена схемой API, она всегда будет полностью
в курсе последней развернутой версии Сервиса.

---

# Command line client

# Клиент командной строки

The command line client allows you to inspect and interact with any API that
exposes a supported schema format.

Клиент командной строки позволяет проверять и взаимодействовать с любым API, который
разоблачает подтвержденный формат схемы.

## Getting started

## Начиная

To install the Core API command line client, use `pip`.

Чтобы установить клиент командной строки Core API, используйте `pip`.

Note that the command-line client is a separate package to the
python client library. Make sure to install `coreapi-cli`.

Обратите внимание, что клиент командной строки является отдельным пакетом для
Клиентская библиотека Python.
Обязательно установите `coreapi-cli`.

```
$ pip install coreapi-cli
```

To start inspecting and interacting with an API the schema must first be loaded
from the network.

Чтобы начать проверку и взаимодействие с API, схема должна сначала загружаться
из сети.

```
$ coreapi get http://api.example.org/
<Pastebin API "http://127.0.0.1:8000/">
snippets: {
    create(code, [title], [linenos], [language], [style])
    destroy(pk)
    highlight(pk)
    list([page])
    partial_update(pk, [title], [code], [linenos], [language], [style])
    retrieve(pk)
    update(pk, code, [title], [linenos], [language], [style])
}
users: {
    list([page])
    retrieve(pk)
}
```

This will then load the schema, displaying the resulting `Document`. This
`Document` includes all the available interactions that may be made against the API.

Затем это загрузит схему, отображая полученный «документ».
Этот
`Document` включает в себя все доступные взаимодействия, которые могут быть сделаны против API.

To interact with the API, use the `action` command. This command requires a list
of keys that are used to index into the link.

Чтобы взаимодействовать с API, используйте команду `Action`.
Эта команда требует списка
ключей, которые используются для индекса в ссылку.

```
$ coreapi action users list
[
    {
        "url": "http://127.0.0.1:8000/users/2/",
        "id": 2,
        "username": "aziz",
        "snippets": []
    },
    ...
]
```

To inspect the underlying HTTP request and response, use the `--debug` flag.

Чтобы осмотреть базовый HTTP-запрос и ответ, используйте флаг `-debug`.

```
$ coreapi action users list --debug
> GET /users/ HTTP/1.1
> Accept: application/vnd.coreapi+json, */*
> Authorization: Basic bWF4Om1heA==
> Host: 127.0.0.1
> User-Agent: coreapi
< 200 OK
< Allow: GET, HEAD, OPTIONS
< Content-Type: application/json
< Date: Thu, 30 Jun 2016 10:51:46 GMT
< Server: WSGIServer/0.1 Python/2.7.10
< Vary: Accept, Cookie
<
< [{"url":"http://127.0.0.1/users/2/","id":2,"username":"aziz","snippets":[]},{"url":"http://127.0.0.1/users/3/","id":3,"username":"amy","snippets":["http://127.0.0.1/snippets/3/"]},{"url":"http://127.0.0.1/users/4/","id":4,"username":"max","snippets":["http://127.0.0.1/snippets/4/","http://127.0.0.1/snippets/5/","http://127.0.0.1/snippets/6/","http://127.0.0.1/snippets/7/"]},{"url":"http://127.0.0.1/users/5/","id":5,"username":"jose","snippets":[]},{"url":"http://127.0.0.1/users/6/","id":6,"username":"admin","snippets":["http://127.0.0.1/snippets/1/","http://127.0.0.1/snippets/2/"]}]

[
    ...
]
```

Some actions may include optional or required parameters.

Некоторые действия могут включать дополнительные или требуемые параметры.

```
$ coreapi action users create --param username=example
```

When using `--param`, the type of the input will be determined automatically.

При использовании `-param` тип входа будет определяться автоматически.

If you want to be more explicit about the parameter type then use `--data` for
any null, numeric, boolean, list, or object inputs, and use `--string` for string inputs.

Если вы хотите быть более явным в отношении типа параметра, то используйте `-data` для
Любые нулевые, числовые, логические, списки или входы объекта и используйте `-String` для вводов строк.

```
$ coreapi action users edit --string username=tomchristie --data is_admin=true
```

## Authentication & headers

## Аутентификация и заголовки

The `credentials` command is used to manage the request `Authentication:` header.
Any credentials added are always linked to a particular domain, so as to ensure
that credentials are not leaked across differing APIs.

Команда «учетные данные» используется для управления запросом `Аутентификация:` Заголовок.
Любые добавленные учетные данные всегда связаны с определенным доменом, чтобы обеспечить
Эти полномочия не протекают в разных API.

The format for adding a new credential is:

Формат для добавления новых учетных данных - это:

```
$ coreapi credentials add <domain> <credentials string>
```

For instance:

Например:

```
$ coreapi credentials add api.example.org "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

The optional `--auth` flag also allows you to add specific types of authentication,
handling the encoding for you. Currently only `"basic"` is supported as an option here.
For example:

Необязательный флаг `-Auth` также позволяет добавлять конкретные типы аутентификации,
обрабатывать кодирование для вас.
В настоящее время только «Basic» `поддерживается здесь как вариант.
Например:

```
$ coreapi credentials add api.example.org tomchristie:foobar --auth basic
```

You can also add specific request headers, using the `headers` command:

Вы также можете добавить конкретные заголовки запросов, используя команду `headers`:

```
$ coreapi headers add api.example.org x-api-version 2
```

For more information and a listing of the available subcommands use `coreapi credentials --help` or `coreapi headers --help`.

Для получения дополнительной информации и списка доступных подкомандов используют `coreapi учетные данные -Help` или` coreapi заголовки -help`.

## Codecs

## Кодеки

By default the command line client only includes support for reading Core JSON
schemas, however it includes a plugin system for installing additional codecs.

По умолчанию клиент командной строки включает только поддержку чтения Core JSON
Схемы, однако, включает в себя систему плагинов для установки дополнительных кодеков.

```
$ pip install openapi-codec jsonhyperschema-codec hal-codec
$ coreapi codecs show
Codecs
corejson        application/vnd.coreapi+json encoding, decoding
hal             application/hal+json         encoding, decoding
openapi         application/openapi+json     encoding, decoding
jsonhyperschema application/schema+json      decoding
json            application/json             data
text            text/*                       data
```

## Utilities

## утилиты

The command line client includes functionality for bookmarking API URLs
under a memorable name. For example, you can add a bookmark for the
existing API, like so...

Клиент командной строки включает в себя функциональность для URL -адресов API закладки
под запоминающимся именем.
Например, вы можете добавить закладку для
Существующий API, как ...

```
$ coreapi bookmarks add accountmanagement
```

There is also functionality for navigating forward or backward through the
history of which API URLs have been accessed.

Существует также функциональность для навигации вперед или назад через
История, доступ к которой были доступны.

```
$ coreapi history show
$ coreapi history back
```

For more information and a listing of the available subcommands use
`coreapi bookmarks --help` or `coreapi history --help`.

Для получения дополнительной информации и списка доступных подкомандов используется
`coreapi закладки -Help` или` coreapi ystory -help`.

## Other commands

## Другие команды

To display the current `Document`:

Чтобы отобразить текущий `document`:

```
$ coreapi show
```

To reload the current `Document` from the network:

Чтобы перезагрузить текущий «документ» из сети:

```
$ coreapi reload
```

To load a schema file from disk:

Чтобы загрузить файл схемы с диска:

```
$ coreapi load my-api-schema.json --format corejson
```

To dump the current document to console in a given format:

Чтобы сбросить текущий документ в консоли в данном формате:

```
$ coreapi dump --format openapi
```

To remove the current document, along with all currently saved history,
credentials, headers and bookmarks:

Чтобы удалить текущий документ, наряду со всеми в настоящее время сохраненной историей,
Условия, заголовки и закладки:

```
$ coreapi clear
```

---

# Python client library

# Клиентская библиотека Python

The `coreapi` Python package allows you to programmatically interact with any
API that exposes a supported schema format.

Пакет Python `coreapi`s позволяет программно взаимодействовать с любым
API, который раскрывает подтверждаемый формат схемы.

## Getting started

## Начиная

You'll need to install the `coreapi` package using `pip` before you can get
started.

Вам нужно будет установить пакет «coreapi», используя `pip`, прежде чем вы сможете получить
начал.

```
$ pip install coreapi
```

In order to start working with an API, we first need a `Client` instance. The
client holds any configuration around which codecs and transports are supported
when interacting with an API, which allows you to provide for more advanced
kinds of behaviour.

Чтобы начать работу с API, нам сначала нужен экземпляр «клиент».
А
Клиент держит любую конфигурацию, вокруг которой поддерживаются кодеки и транспорты
При взаимодействии с API, который позволяет вам обеспечить более продвинутые
виды поведения.

```
import coreapi
client = coreapi.Client()
```

Once we have a `Client` instance, we can fetch an API schema from the network.

Как только у нас появится экземпляр «клиента», мы можем получить схему API из сети.

```
schema = client.get('https://api.example.org/')
```

The object returned from this call will be a `Document` instance, which is
a representation of the API schema.

Объект, возвращенный из этого вызова, будет экземпляр «документ», который
представление схемы API.

## Authentication

## Аутентификация

Typically you'll also want to provide some authentication credentials when
instantiating the client.

Как правило, вы также захотите предоставить некоторые учетные данные, когда
создание клиента.

#### Token authentication

#### Аутентификация токена

The `TokenAuthentication` class can be used to support REST framework's built-in
`TokenAuthentication`, as well as OAuth and JWT schemes.

Класс `tokenauthentication можно использовать для поддержки встроенной структуры Rest Framework
`Tokenauthentication ', а также схемы OAuth и JWT.

```
auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token='<token>'
)
client = coreapi.Client(auth=auth)
```

When using TokenAuthentication you'll probably need to implement a login flow
using the CoreAPI client.

При использовании Tokenauthentication вам, вероятно, нужно реализовать поток входа в систему
Используя клиент Coreapi.

A suggested pattern for this would be to initially make an unauthenticated client
request to an "obtain token" endpoint

Предлагаемой схемой для этого было бы изначально сделать неавентицитированного клиента
запрос на конечную точку «получить токен»

For example, using the "Django REST framework JWT" package

Например, использование пакета "Django Rest Framework JWT"

```
client = coreapi.Client()
schema = client.get('https://api.example.org/')

action = ['api-token-auth', 'create']
params = {"username": "example", "password": "secret"}
result = client.action(schema, action, params)

auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token=result['token']
)
client = coreapi.Client(auth=auth)
```

#### Basic authentication

#### Базовая аутентификация

The `BasicAuthentication` class can be used to support HTTP Basic Authentication.

Класс `basicauthentication можно использовать для поддержки базовой аутентификации HTTP.

```
auth = coreapi.auth.BasicAuthentication(
    username='<username>',
    password='<password>'
)
client = coreapi.Client(auth=auth)
```

## Interacting with the API

## взаимодействие с API

Now that we have a client and have fetched our schema `Document`, we can now
start to interact with the API:

Теперь, когда у нас есть клиент, и мы получили нашу схему «документ», мы теперь можем
Начните взаимодействовать с API:

```
users = client.action(schema, ['users', 'list'])
```

Some endpoints may include named parameters, which might be either optional or required:

Некоторые конечные точки могут включать названные параметры, которые могут быть либо необязательными, либо необходимыми:

```
new_user = client.action(schema, ['users', 'create'], params={"username": "max"})
```

## Codecs

## Кодеки

Codecs are responsible for encoding or decoding Documents.

Кодеки несут ответственность за кодирование или декодирование документов.

The decoding process is used by a client to take a bytestring of an API schema
definition, and returning the Core API `Document` that represents that interface.

Процесс декодирования используется клиентом для проведения схемы API
Определение и возвращение основного API `Document`, который представляет этот интерфейс.

A codec should be associated with a particular media type, such as `'application/coreapi+json'`.

Кодек должен быть связан с конкретным типом носителя, таким как «Приложение/Coreapi+json'».

This media type is used by the server in the response `Content-Type` header,
in order to indicate what kind of data is being returned in the response.

Этот тип мультимедиа используется сервером в заголовке ответа `Контент-тип,
Чтобы указать, какие данные возвращаются в ответе.

#### Configuring codecs

#### Настройка кодеков

The codecs that are available can be configured when instantiating a client.
The keyword argument used here is `decoders`, because in the context of a
client the codecs are only for *decoding* responses.

Доступные кодеки могут быть настроены при создании клиента.
Аргумент ключевого слова, используемый здесь, - «декодеры», потому что в контексте
Клиент Кодеки предназначены только для * декодирования * ответов.

In the following example we'll configure a client to only accept `Core JSON`
and `JSON` responses. This will allow us to receive and decode a Core JSON schema,
and subsequently to receive JSON responses made against the API.

В следующем примере мы настроим клиента, чтобы принять только `core json`
и `json 'ответы.
Это позволит нам получить и декодировать схему основной JSON,
и впоследствии получить ответы JSON, сделанные против API.

```
from coreapi import codecs, Client

decoders = [codecs.CoreJSONCodec(), codecs.JSONCodec()]
client = Client(decoders=decoders)
```

#### Loading and saving schemas

#### Схемы загрузки и сохранения

You can use a codec directly, in order to load an existing schema definition,
and return the resulting `Document`.

Вы можете использовать кодек напрямую, чтобы загрузить существующую определение схемы,
и вернуть полученный «документ».

```
input_file = open('my-api-schema.json', 'rb')
schema_definition = input_file.read()
codec = codecs.CoreJSONCodec()
schema = codec.load(schema_definition)
```

You can also use a codec directly to generate a schema definition given a `Document` instance:

Вы также можете использовать кодек непосредственно для создания определения схемы, учитывая экземпляр «Document»:

```
schema_definition = codec.dump(schema)
output_file = open('my-api-schema.json', 'rb')
output_file.write(schema_definition)
```

## Transports

## транспорт

Transports are responsible for making network requests. The set of transports
that a client has installed determines which network protocols it is able to
support.

Транспорт несет ответственность за выполнение сетевых запросов.
Набор транспортов
что установил клиент, определяет, какие сетевые протоколы он может
поддерживать.

Currently the `coreapi` library only includes an HTTP/HTTPS transport, but
other protocols can also be supported.

В настоящее время библиотека Coreapi 'включает только транспорт HTTP/HTTPS, но
Другие протоколы также могут быть поддержаны.

#### Configuring transports

#### Настройка транспорта

The behavior of the network layer can be customized by configuring the
transports that the client is instantiated with.

Поведение сетевого уровня можно настроить путем настройки
Транспорт, с которыми клиент создается.

```
import requests
from coreapi import transports, Client

credentials = {'api.example.org': 'Token 3bd44a009d16ff'}
transports = transports.HTTPTransport(credentials=credentials)
client = Client(transports=transports)
```

More complex customizations can also be achieved, for example modifying the
underlying `requests.Session` instance to [attach transport adaptors](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters)
that modify the outgoing requests.

Также могут быть достигнуты более сложные настройки, например, изменение
Базовый экземпляр `requests.session` к [Прикреплять транспортные адаптеры] (http://docs.python-requests.org/en/master/user/advanced/#transport-adapters)
это изменяет исходящие запросы.

---

# JavaScript Client Library

# Клиентская библиотека JavaScript

The JavaScript client library allows you to interact with your API either from a browser, or using node.

Клиентская библиотека JavaScript позволяет вам взаимодействовать с вашим API либо из браузера, либо с помощью узла.

## Installing the JavaScript client

## Установка клиента JavaScript

There are two separate JavaScript resources that you need to include in your HTML pages in order to use the JavaScript client library. These are a static `coreapi.js` file, which contains the code for the dynamic client library, and a templated `schema.js` resource, which exposes your API schema.

Есть два отдельных ресурса JavaScript, которые вам необходимо включить в свои HTML -страницы, чтобы использовать клиентскую библиотеку JavaScript.
Это статический файл `coreapi.js`, который содержит код для динамической клиентской библиотеки, и ресурс« Schema.js`, который разоблачает вашу схему API.

First, install the API documentation views. These will include the schema resource that'll allow you to load the schema directly from an HTML page, without having to make an asynchronous AJAX call.

Во -первых, установите представления документации API.
Они будут включать в себя ресурс схемы, который позволит вам загрузить схему непосредственно с HTML -страницы, без необходимости делать асинхронный вызов Ajax.

```
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
]
```

Once the API documentation URLs are installed, you'll be able to include both the required JavaScript resources. Note that the ordering of these two lines is important, as the schema loading requires CoreAPI to already be installed.

После установки URL -адресов документации API вы сможете включить оба необходимые ресурсы JavaScript.
Обратите внимание, что упорядочение этих двух линий важно, так как загрузка схемы требует, чтобы Coreapi уже была установлена.

```
<!--
    Load the CoreAPI library and the API schema.

    /static/rest_framework/js/coreapi-0.1.1.js
    /docs/schema.js
-->
{% load static %}
<script src="{% static 'rest_framework/js/coreapi-0.1.1.js' %}"></script>
<script src="{% url 'api-docs:schema-js' %}"></script>
```

The `coreapi` library, and the `schema` object will now both be available on the `window` instance.

Библиотека Coreapi` и объект `schema 'теперь будут доступны в экземпляре` window'.

```
const coreapi = window.coreapi;
const schema = window.schema;
```

## Instantiating a client

## создание клиента

In order to interact with the API you'll need a client instance.

Чтобы взаимодействовать с API, вам понадобится экземпляр клиента.

```
var client = new coreapi.Client();
```

Typically you'll also want to provide some authentication credentials when
instantiating the client.

Как правило, вы также захотите предоставить некоторые учетные данные, когда
создание клиента.

#### Session authentication

#### Аутентификация сеанса

The `SessionAuthentication` class allows session cookies to provide the user
authentication. You'll want to provide a standard HTML login flow, to allow
the user to login, and then instantiate a client using session authentication:

Класс `sessionAuthentication 'позволяет сеансу файлы cookie предоставлять пользователя
аутентификация.
Вы захотите предоставить стандартный поток входа в систему HTML, чтобы разрешить
Пользователь для входа в систему, а затем создает экземпляр клиента, используя аутентификацию сеанса:

```
let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken',
});
let client = new coreapi.Client({auth: auth});
```

The authentication scheme will handle including a CSRF header in any outgoing
requests for unsafe HTTP methods.

Схема аутентификации будет обрабатываться, включая заголовок CSRF в любом исходящем
Запросы на небезопасные методы HTTP.

#### Token authentication

#### Аутентификация токена

The `TokenAuthentication` class can be used to support REST framework's built-in
`TokenAuthentication`, as well as OAuth and JWT schemes.

Класс `tokenauthentication можно использовать для поддержки встроенной структуры Rest Framework
`Tokenauthentication ', а также схемы OAuth и JWT.

```
let auth = new coreapi.auth.TokenAuthentication({
    scheme: 'JWT',
    token: '<token>',
});
let client = new coreapi.Client({auth: auth});
```

When using TokenAuthentication you'll probably need to implement a login flow
using the CoreAPI client.

При использовании Tokenauthentication вам, вероятно, нужно реализовать поток входа в систему
Используя клиент Coreapi.

A suggested pattern for this would be to initially make an unauthenticated client
request to an "obtain token" endpoint

Предлагаемой схемой для этого было бы изначально сделать неавентицитированного клиента
запрос на конечную точку «получить токен»

For example, using the "Django REST framework JWT" package

Например, использование пакета "Django Rest Framework JWT"

```
// Setup some globally accessible state
window.client = new coreapi.Client();
window.loggedIn = false;

function loginUser(username, password) {
    let action = ["api-token-auth", "obtain-token"];
    let params = {username: username, password: password};
    client.action(schema, action, params).then(function(result) {
        // On success, instantiate an authenticated client.
        let auth = window.coreapi.auth.TokenAuthentication({
            scheme: 'JWT',
            token: result['token'],
        })
        window.client = coreapi.Client({auth: auth});
        window.loggedIn = true;
    }).catch(function (error) {
        // Handle error case where eg. user provides incorrect credentials.
    })
}
```

#### Basic authentication

#### Базовая аутентификация

The `BasicAuthentication` class can be used to support HTTP Basic Authentication.

Класс `basicauthentication можно использовать для поддержки базовой аутентификации HTTP.

```
let auth = new coreapi.auth.BasicAuthentication({
    username: '<username>',
    password: '<password>',
})
let client = new coreapi.Client({auth: auth});
```

## Using the client

## с помощью клиента

Making requests:

Делать запросы:

```
let action = ["users", "list"];
client.action(schema, action).then(function(result) {
    // Return value is in 'result'
})
```

Including parameters:

В том числе параметры:

```
let action = ["users", "create"];
let params = {username: "example", email: "example@example.com"};
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
})
```

Handling errors:

Ошибки обработки:

```
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
}).catch(function (error) {
    // Error value is in 'error'
})
```

## Installation with node

## установка с узлом

The coreapi package is available on NPM.

Пакет Coreapi доступен на NPM.

```
$ npm install coreapi
$ node
const coreapi = require('coreapi')
```

You'll either want to include the API schema in your codebase directly, by copying it from the `schema.js` resource, or else load the schema asynchronously. For example:

Вы либо захотите включить схему API в свою кодовую базу напрямую, копировав ее из ресурса `schema.js ', либо загрузите схему асинхронно.
Например:

```
let client = new coreapi.Client();
let schema = null;
client.get("https://api.example.org/").then(function(data) {
    // Load a CoreJSON API schema.
    schema = data;
    console.log('schema loaded');
})
```