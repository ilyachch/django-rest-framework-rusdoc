<!-- TRANSLATED by md-translate -->
# API Clients

# Клиенты API

An API client handles the underlying details of how network requests are made and how responses are decoded. They present the developer with an application interface to work against, rather than working directly with the network interface.

Клиент API обрабатывает основные детали того, как выполняются сетевые запросы и как декодируются ответы. Они предоставляют разработчику интерфейс приложения для работы, а не работают непосредственно с сетевым интерфейсом.

The API clients documented here are not restricted to APIs built with Django REST framework. They can be used with any API that exposes a supported schema format.

Клиенты API, описанные здесь, не ограничиваются API, построенными с помощью фреймворка Django REST. Их можно использовать с любым API, который предоставляет поддерживаемый формат схемы.

For example, [the Heroku platform API](https://devcenter.heroku.com/categories/platform-api) exposes a schema in the JSON Hyperschema format. As a result, the Core API command line client and Python client library can be [used to interact with the Heroku API](https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

Например, [API платформы Heroku](https://devcenter.heroku.com/categories/platform-api) предоставляет схему в формате JSON Hyperschema. В результате клиент командной строки Core API и клиентская библиотека Python могут быть [использованы для взаимодействия с API Heroku](https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

## Client-side Core API

## Основной API на стороне клиента

[Core API](https://www.coreapi.org/) is a document specification that can be used to describe APIs. It can be used either server-side, as is done with REST framework's [schema generation](../api-guide/schemas.md), or used client-side, as described here.

[Core API](https://www.coreapi.org/) - это спецификация документа, который может быть использован для описания API. Она может использоваться либо на стороне сервера, как это делается с помощью [schema generation](../api-guide/schemas.md) фреймворка REST, либо на стороне клиента, как описано здесь.

When used client-side, Core API allows for *dynamically driven client libraries* that can interact with any API that exposes a supported schema or hypermedia format.

При использовании на стороне клиента, Core API позволяет создавать *динамически управляемые клиентские библиотеки*, которые могут взаимодействовать с любым API, раскрывающим поддерживаемую схему или формат гипермедиа.

Using a dynamically driven client has a number of advantages over interacting with an API by building HTTP requests directly.

Использование динамически управляемого клиента имеет ряд преимуществ перед взаимодействием с API путем создания HTTP-запросов напрямую.

#### More meaningful interaction

#### Более содержательное взаимодействие

API interactions are presented in a more meaningful way. You're working at the application interface layer, rather than the network interface layer.

Взаимодействие API представлено в более осмысленном виде. Вы работаете на уровне интерфейса приложения, а не на уровне сетевого интерфейса.

#### Resilience & evolvability

#### Устойчивость и эволюционность

The client determines what endpoints are available, what parameters exist against each particular endpoint, and how HTTP requests are formed.

Клиент определяет, какие конечные точки доступны, какие параметры существуют для каждой конкретной конечной точки, и как формируются HTTP-запросы.

This also allows for a degree of API evolvability. URLs can be modified without breaking existing clients, or more efficient encodings can be used on-the-wire, with clients transparently upgrading.

Это также позволяет в определенной степени эволюционировать API. URL-адреса могут быть изменены без нарушения работы существующих клиентов, или более эффективные кодировки могут быть использованы по проводам, с прозрачным обновлением клиентов.

#### Self-descriptive APIs

#### Самоописывающиеся API

A dynamically driven client is able to present documentation on the API to the end user. This documentation allows the user to discover the available endpoints and parameters, and better understand the API they are working with.

Динамически управляемый клиент способен представить конечному пользователю документацию по API. Эта документация позволяет пользователю обнаружить доступные конечные точки и параметры, а также лучше понять API, с которым он работает.

Because this documentation is driven by the API schema it will always be fully up to date with the most recently deployed version of the service.

Поскольку эта документация определяется схемой API, она всегда будет полностью соответствовать последней развернутой версии сервиса.

---

# Command line client

# Клиент командной строки

The command line client allows you to inspect and interact with any API that exposes a supported schema format.

Клиент командной строки позволяет вам проверять и взаимодействовать с любым API, который раскрывает поддерживаемый формат схемы.

## Getting started

## Начало работы

To install the Core API command line client, use `pip`.

Чтобы установить клиент командной строки Core API, используйте `pip`.

Note that the command-line client is a separate package to the python client library. Make sure to install `coreapi-cli`.

Обратите внимание, что клиент командной строки является отдельным пакетом по отношению к клиентской библиотеке python. Обязательно установите `coreapi-cli`.

```
$ pip install coreapi-cli
```

To start inspecting and interacting with an API the schema must first be loaded from the network.

Чтобы начать осмотр и взаимодействие с API, схема должна быть сначала загружена из сети.

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

This will then load the schema, displaying the resulting `Document`. This `Document` includes all the available interactions that may be made against the API.

После этого будет загружена схема и отображен результирующий `Документ`. Этот `документ` включает все доступные взаимодействия, которые могут быть выполнены с API.

To interact with the API, use the `action` command. This command requires a list of keys that are used to index into the link.

Чтобы взаимодействовать с API, используйте команду `action`. Эта команда требует список ключей, которые используются для индексации в ссылке.

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

Чтобы просмотреть основной HTTP-запрос и ответ, используйте флаг `--debug`.

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

Некоторые действия могут включать необязательные или требуемые параметры.

```
$ coreapi action users create --param username=example
```

When using `--param`, the type of the input will be determined automatically.

При использовании `--param` тип входных данных будет определен автоматически.

If you want to be more explicit about the parameter type then use `--data` for any null, numeric, boolean, list, or object inputs, and use `--string` for string inputs.

Если вы хотите более четко определить тип параметра, используйте `--data` для любых нулевых, числовых, булевых, списковых или объектных входных данных, и используйте `--string` для строковых входных данных.

```
$ coreapi action users edit --string username=tomchristie --data is_admin=true
```

## Authentication & headers

## Аутентификация и заголовки

The `credentials` command is used to manage the request `Authentication:` header. Any credentials added are always linked to a particular domain, so as to ensure that credentials are not leaked across differing APIs.

Команда `credentials` используется для управления заголовком запроса `Authentication:`. Любые добавленные учетные данные всегда привязаны к определенному домену, чтобы гарантировать, что учетные данные не будут утекать через различные API.

The format for adding a new credential is:

Формат добавления новой учетной записи следующий:

```
$ coreapi credentials add <domain> <credentials string>
```

For instance:

Например:

```
$ coreapi credentials add api.example.org "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

The optional `--auth` flag also allows you to add specific types of authentication, handling the encoding for you. Currently only `"basic"` is supported as an option here. For example:

Дополнительный флаг `--auth` также позволяет вам добавлять определенные типы аутентификации, обрабатывая кодировку за вас. В настоящее время в качестве опции здесь поддерживается только `` basic``. Например:

```
$ coreapi credentials add api.example.org tomchristie:foobar --auth basic
```

You can also add specific request headers, using the `headers` command:

Вы также можете добавить определенные заголовки запроса, используя команду `headers`:

```
$ coreapi headers add api.example.org x-api-version 2
```

For more information and a listing of the available subcommands use `coreapi credentials --help` or `coreapi headers --help`.

Для получения дополнительной информации и списка доступных подкоманд используйте `coreapi credentials --help` или `coreapi headers --help`.

## Codecs

## Кодеки

By default the command line client only includes support for reading Core JSON schemas, however it includes a plugin system for installing additional codecs.

По умолчанию клиент командной строки включает только поддержку чтения схем Core JSON, однако он включает систему плагинов для установки дополнительных кодеков.

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

## Утилиты

The command line client includes functionality for bookmarking API URLs under a memorable name. For example, you can add a bookmark for the existing API, like so...

Клиент командной строки включает функциональность для создания закладок URL API под запоминающимся именем. Например, вы можете добавить закладку для существующего API следующим образом...

```
$ coreapi bookmarks add accountmanagement
```

There is also functionality for navigating forward or backward through the history of which API URLs have been accessed.

Также имеется функциональность для навигации вперед или назад по истории обращений к URL-адресам API.

```
$ coreapi history show
$ coreapi history back
```

For more information and a listing of the available subcommands use `coreapi bookmarks --help` or `coreapi history --help`.

Для получения дополнительной информации и списка доступных подкоманд используйте `coreapi bookmarks --help` или `coreapi history --help`.

## Other commands

## Другие команды

To display the current `Document`:

Для отображения текущего `документа`:

```
$ coreapi show
```

To reload the current `Document` from the network:

Перезагрузить текущий `Документ` из сети:

```
$ coreapi reload
```

To load a schema file from disk:

Чтобы загрузить файл схемы с диска:

```
$ coreapi load my-api-schema.json --format corejson
```

To dump the current document to console in a given format:

Вывод текущего документа на консоль в заданном формате:

```
$ coreapi dump --format openapi
```

To remove the current document, along with all currently saved history, credentials, headers and bookmarks:

Удаление текущего документа вместе со всей сохраненной историей, учетными данными, заголовками и закладками:

```
$ coreapi clear
```

---

# Python client library

# Клиентская библиотека Python

The `coreapi` Python package allows you to programmatically interact with any API that exposes a supported schema format.

Пакет `coreapi` Python позволяет вам программно взаимодействовать с любым API, который раскрывает поддерживаемый формат схемы.

## Getting started

## Начало работы

You'll need to install the `coreapi` package using `pip` before you can get started.

Перед началом работы вам необходимо установить пакет `coreapi` с помощью `pip`.

```
$ pip install coreapi
```

In order to start working with an API, we first need a `Client` instance. The client holds any configuration around which codecs and transports are supported when interacting with an API, which allows you to provide for more advanced kinds of behaviour.

Для того чтобы начать работу с API, нам сначала нужен экземпляр `Client`. Клиент содержит любую конфигурацию, определяющую, какие кодеки и транспорты поддерживаются при взаимодействии с API, что позволяет вам обеспечить более продвинутые типы поведения.

```
import coreapi
client = coreapi.Client()
```

Once we have a `Client` instance, we can fetch an API schema from the network.

Когда у нас есть экземпляр `Client`, мы можем получить схему API из сети.

```
schema = client.get('https://api.example.org/')
```

The object returned from this call will be a `Document` instance, which is a representation of the API schema.

Объект, возвращаемый этим вызовом, будет экземпляром `Document`, который является представлением схемы API.

## Authentication

## Аутентификация

Typically you'll also want to provide some authentication credentials when instantiating the client.

Как правило, при инстанцировании клиента вы также захотите предоставить некоторые учетные данные для аутентификации.

#### Token authentication

#### Аутентификация с помощью токенов

The `TokenAuthentication` class can be used to support REST framework's built-in `TokenAuthentication`, as well as OAuth and JWT schemes.

Класс `TokenAuthentication` можно использовать для поддержки встроенной в REST-фреймворк `TokenAuthentication`, а также схем OAuth и JWT.

```
auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token='<token>'
)
client = coreapi.Client(auth=auth)
```

When using TokenAuthentication you'll probably need to implement a login flow using the CoreAPI client.

При использовании TokenAuthentication вам, вероятно, потребуется реализовать поток входа в систему с помощью клиента CoreAPI.

A suggested pattern for this would be to initially make an unauthenticated client request to an "obtain token" endpoint

Предлагаемая схема для этого может заключаться в первоначальном запросе неаутентифицированного клиента к конечной точке "получения токена"

For example, using the "Django REST framework JWT" package

Например, используя пакет "Django REST framework JWT"

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

Класс `BasicAuthentication` можно использовать для поддержки HTTP Basic Authentication.

```
auth = coreapi.auth.BasicAuthentication(
    username='<username>',
    password='<password>'
)
client = coreapi.Client(auth=auth)
```

## Interacting with the API

## Взаимодействие с API

Now that we have a client and have fetched our schema `Document`, we can now start to interact with the API:

Теперь, когда у нас есть клиент и мы получили нашу схему `Document`, мы можем начать взаимодействовать с API:

```
users = client.action(schema, ['users', 'list'])
```

Some endpoints may include named parameters, which might be either optional or required:

Некоторые конечные точки могут включать именованные параметры, которые могут быть как необязательными, так и обязательными:

```
new_user = client.action(schema, ['users', 'create'], params={"username": "max"})
```

## Codecs

## Кодеки

Codecs are responsible for encoding or decoding Documents.

Кодеки отвечают за кодирование или декодирование документов.

The decoding process is used by a client to take a bytestring of an API schema definition, and returning the Core API `Document` that represents that interface.

Процесс декодирования используется клиентом для получения байтовой строки определения схемы API и возврата Core API `Document`, который представляет этот интерфейс.

A codec should be associated with a particular media type, such as `'application/coreapi+json'`.

Кодек должен быть связан с определенным типом медиа, например `'application/coreapi+json'`.

This media type is used by the server in the response `Content-Type` header, in order to indicate what kind of data is being returned in the response.

Этот тип медиа используется сервером в заголовке ответа `Content-Type`, чтобы указать, какой тип данных возвращается в ответе.

#### Configuring codecs

#### Конфигурирование кодеков

The codecs that are available can be configured when instantiating a client. The keyword argument used here is `decoders`, because in the context of a client the codecs are only for *decoding* responses.

Доступные кодеки можно настроить при инстанцировании клиента. Здесь используется ключевое слово `декодеры`, потому что в контексте клиента кодеки предназначены только для *декодирования* ответов.

In the following example we'll configure a client to only accept `Core JSON` and `JSON` responses. This will allow us to receive and decode a Core JSON schema, and subsequently to receive JSON responses made against the API.

В следующем примере мы настроим клиента на прием только ответов `Core JSON` и `JSON`. Это позволит нам получать и декодировать схему Core JSON, а затем получать ответы JSON, сделанные с помощью API.

```
from coreapi import codecs, Client

decoders = [codecs.CoreJSONCodec(), codecs.JSONCodec()]
client = Client(decoders=decoders)
```

#### Loading and saving schemas

#### Загрузка и сохранение схем

You can use a codec directly, in order to load an existing schema definition, and return the resulting `Document`.

Вы можете использовать кодек напрямую, чтобы загрузить существующее определение схемы и вернуть полученный `документ`.

```
input_file = open('my-api-schema.json', 'rb')
schema_definition = input_file.read()
codec = codecs.CoreJSONCodec()
schema = codec.load(schema_definition)
```

You can also use a codec directly to generate a schema definition given a `Document` instance:

Вы также можете использовать кодек непосредственно для генерации определения схемы, заданного экземпляром `Document`:

```
schema_definition = codec.dump(schema)
output_file = open('my-api-schema.json', 'rb')
output_file.write(schema_definition)
```

## Transports

## Транспорты

Transports are responsible for making network requests. The set of transports that a client has installed determines which network protocols it is able to support.

Транспорты отвечают за выполнение сетевых запросов. Набор транспортов, установленных у клиента, определяет, какие сетевые протоколы он может поддерживать.

Currently the `coreapi` library only includes an HTTP/HTTPS transport, but other protocols can also be supported.

В настоящее время библиотека `coreapi` включает только транспорт HTTP/HTTPS, но могут поддерживаться и другие протоколы.

#### Configuring transports

#### Конфигурирование транспортов

The behavior of the network layer can be customized by configuring the transports that the client is instantiated with.

Поведение сетевого уровня может быть настроено путем конфигурирования транспортов, с которыми инстанцируется клиент.

```
import requests
from coreapi import transports, Client

credentials = {'api.example.org': 'Token 3bd44a009d16ff'}
transports = transports.HTTPTransport(credentials=credentials)
client = Client(transports=transports)
```

More complex customizations can also be achieved, for example modifying the underlying `requests.Session` instance to [attach transport adaptors](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters) that modify the outgoing requests.

Можно добиться и более сложной настройки, например, модифицировать базовый экземпляр `requests.Session` для [присоединения транспортных адаптеров](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters), которые изменяют исходящие запросы.

---

# JavaScript Client Library

# Клиентская библиотека JavaScript

The JavaScript client library allows you to interact with your API either from a browser, or using node.

Клиентская библиотека JavaScript позволяет вам взаимодействовать с API либо через браузер, либо с помощью node.

## Installing the JavaScript client

## Установка клиента JavaScript

There are two separate JavaScript resources that you need to include in your HTML pages in order to use the JavaScript client library. These are a static `coreapi.js` file, which contains the code for the dynamic client library, and a templated `schema.js` resource, which exposes your API schema.

Существует два отдельных ресурса JavaScript, которые необходимо включить в ваши HTML-страницы, чтобы использовать клиентскую библиотеку JavaScript. Это статический файл `coreapi.js`, который содержит код для динамической клиентской библиотеки, и шаблонный ресурс `chema.js`, который раскрывает схему вашего API.

First, install the API documentation views. These will include the schema resource that'll allow you to load the schema directly from an HTML page, without having to make an asynchronous AJAX call.

Сначала установите представления документации API. Они будут включать ресурс схемы, который позволит вам загружать схему непосредственно с HTML-страницы, без необходимости выполнять асинхронный вызов AJAX.

```
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
]
```

Once the API documentation URLs are installed, you'll be able to include both the required JavaScript resources. Note that the ordering of these two lines is important, as the schema loading requires CoreAPI to already be installed.

Как только URL-адреса документации API будут установлены, вы сможете включить оба необходимых ресурса JavaScript. Обратите внимание, что порядок этих двух строк важен, поскольку для загрузки схемы требуется, чтобы CoreAPI уже был установлен.

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

Библиотека `coreapi` и объект `schema` теперь будут доступны на экземпляре `window`.

```
const coreapi = window.coreapi;
const schema = window.schema;
```

## Instantiating a client

## Создание клиента

In order to interact with the API you'll need a client instance.

Для взаимодействия с API вам понадобится экземпляр клиента.

```
var client = new coreapi.Client();
```

Typically you'll also want to provide some authentication credentials when instantiating the client.

Как правило, при инстанцировании клиента вы также захотите предоставить некоторые учетные данные для аутентификации.

#### Session authentication

#### Аутентификация сеанса

The `SessionAuthentication` class allows session cookies to provide the user authentication. You'll want to provide a standard HTML login flow, to allow the user to login, and then instantiate a client using session authentication:

Класс `SessionAuthentication` позволяет сессионным файлам cookie обеспечивать аутентификацию пользователя. Y

```
let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken',
});
let client = new coreapi.Client({auth: auth});
```

The authentication scheme will handle including a CSRF header in any outgoing requests for unsafe HTTP methods.

Схема аутентификации будет обрабатывать включение заголовка CSRF в любые исходящие запросы для небезопасных методов HTTP.

#### Token authentication

#### Аутентификация с помощью токенов

The `TokenAuthentication` class can be used to support REST framework's built-in `TokenAuthentication`, as well as OAuth and JWT schemes.

Класс `TokenAuthentication` можно использовать для поддержки встроенной в REST-фреймворк `TokenAuthentication`, а также схем OAuth и JWT.

```
let auth = new coreapi.auth.TokenAuthentication({
    scheme: 'JWT',
    token: '<token>',
});
let client = new coreapi.Client({auth: auth});
```

When using TokenAuthentication you'll probably need to implement a login flow using the CoreAPI client.

При использовании TokenAuthentication вам, вероятно, потребуется реализовать поток входа в систему с помощью клиента CoreAPI.

A suggested pattern for this would be to initially make an unauthenticated client request to an "obtain token" endpoint

Предлагаемая схема для этого может заключаться в первоначальном запросе неаутентифицированного клиента к конечной точке "получения токена"

For example, using the "Django REST framework JWT" package

Например, используя пакет "Django REST framework JWT"

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

Класс `BasicAuthentication` можно использовать для поддержки базовой аутентификации HTTP.

```
let auth = new coreapi.auth.BasicAuthentication({
    username: '<username>',
    password: '<password>',
})
let client = new coreapi.Client({auth: auth});
```

## Using the client

## Использование клиента

Making requests:

Выполнение запросов:

```
let action = ["users", "list"];
client.action(schema, action).then(function(result) {
    // Return value is in 'result'
})
```

Including parameters:

Включая параметры:

```
let action = ["users", "create"];
let params = {username: "example", email: "example@example.com"};
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
})
```

Handling errors:

Обработка ошибок:

```
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
}).catch(function (error) {
    // Error value is in 'error'
})
```

## Installation with node

## Установка с помощью node

The coreapi package is available on NPM.

Пакет coreapi доступен на NPM.

```
$ npm install coreapi
$ node
const coreapi = require('coreapi')
```

You'll either want to include the API schema in your codebase directly, by copying it from the `schema.js` resource, or else load the schema asynchronously. For example:

Вы захотите либо включить схему API в свою кодовую базу напрямую, скопировав ее из ресурса `schema.js`, либо загрузить схему асинхронно. Например:

```
let client = new coreapi.Client();
let schema = null;
client.get("https://api.example.org/").then(function(data) {
    // Load a CoreJSON API schema.
    schema = data;
    console.log('schema loaded');
})
```