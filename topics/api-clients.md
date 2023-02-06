<!-- TRANSLATED by md-translate -->
# Клиенты API

Клиент API обрабатывает основные детали того, как выполняются сетевые запросы и как декодируются ответы. Они предоставляют разработчику интерфейс приложения для работы, а не работают непосредственно с сетевым интерфейсом.

Клиенты API, описанные здесь, не ограничиваются API, построенными с помощью REST framework. Их можно использовать с любым API, который предоставляет поддерживаемый формат схемы.

Например, [API платформа Heroku](https://devcenter.heroku.com/categories/platform-api) предоставляет схему в формате JSON Hyperschema. В результате клиент командной строки Core API и клиентская библиотека Python могут быть [использованы для взаимодействия с API Heroku](https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

## Core API на стороне клиента

[Core API](https://www.coreapi.org/) - это спецификация документа, который может быть использован для описания API. Она может использоваться либо на стороне сервера, как это делается с помощью [schema generation](../api-guide/schemas.md) REST framework, либо на стороне клиента, как описано здесь.

При использовании на стороне клиента, Core API позволяет создавать *динамически управляемые клиентские библиотеки*, которые могут взаимодействовать с любым API, раскрывающим поддерживаемую схему или формат гипермедиа.

Использование динамически управляемого клиента имеет ряд преимуществ перед взаимодействием с API путем создания HTTP-запросов напрямую.

#### Более понятное взаимодействие

Взаимодействие API представлено в более осмысленном виде. Вы работаете на уровне интерфейса приложения, а не на уровне сетевого интерфейса.

#### Устойчивость и эволюционность

Клиент определяет, какие конечные точки доступны, какие параметры существуют для каждой конкретной конечной точки, и как формируются HTTP-запросы.

Это также позволяет в определенной степени обновлять API. URL-адреса могут быть изменены без нарушения работы существующих клиентов, или более эффективные кодировки могут быть использованы на ходу, с прозрачным обновлением клиентов.

#### Самоописывающиеся API

Динамически управляемый клиент способен представить конечному пользователю документацию по API. Эта документация позволяет пользователю обнаружить доступные конечные точки и параметры, а также лучше понять API, с которым он работает.

Поскольку эта документация определяется схемой API, она всегда будет полностью соответствовать последней развернутой версии сервиса.

---

# Клиент командной строки

Клиент командной строки позволяет вам проверять и взаимодействовать с любым API, который раскрывает поддерживаемый формат схемы.

## Начало работы

Чтобы установить клиент командной строки Core API, используйте `pip`.

Обратите внимание, что клиент командной строки является отдельным пакетом по отношению к клиентской библиотеке python. Обязательно установите `coreapi-cli`.

```bash
$ pip install coreapi-cli
```

Чтобы начать осмотр и взаимодействие с API, схема должна быть сначала загружена из сети.

```bash
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

После этого будет загружена схема и отображен результирующий `Документ схемы`. Этот `документ схемы` включает все доступные взаимодействия, которые могут быть выполнены с API.

Чтобы взаимодействовать с API, используйте команду `action`. Эта команда требует список ключей, которые используются для индексации в ссылке.

```bash
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

Чтобы просмотреть основной HTTP-запрос и ответ, используйте флаг `--debug`.

```bash
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

Некоторые действия могут включать необязательные или требуемые параметры.

```bash
$ coreapi action users create --param username=example
```

При использовании `--param` тип входных данных будет определен автоматически.

Если вы хотите более четко определить тип параметра, используйте `--data` для любых нулевых, числовых, булевых, списковых или объектных входных данных, и используйте `--string` для строковых входных данных.

```bash
$ coreapi action users edit --string username=tomchristie --data is_admin=true
```

## Аутентификация и заголовки

Команда `credentials` используется для управления заголовком запроса `Authentication:`. Любые добавленные учетные данные всегда привязаны к определенному домену, чтобы гарантировать, что учетные данные не будут утекать через различные API.

Формат добавления новой учетной записи следующий:

```bash
$ coreapi credentials add <domain> <credentials string>
```

Например:

```bash
$ coreapi credentials add api.example.org "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

Дополнительный флаг `--auth` также позволяет вам добавлять определенные типы аутентификации, обрабатывая кодировку за вас. В настоящее время в качестве опции здесь поддерживается только `"basic"`. Например:

```bash
$ coreapi credentials add api.example.org tomchristie:foobar --auth basic
```

Вы также можете добавить определенные заголовки запроса, используя команду `headers`:

```bash
$ coreapi headers add api.example.org x-api-version 2
```

Для получения дополнительной информации и списка доступных подкоманд используйте `coreapi credentials --help` или `coreapi headers --help`.

## Кодеки

По умолчанию клиент командной строки включает только поддержку чтения схем Core JSON, однако он включает систему плагинов для установки дополнительных кодеков.

```bash
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

## Утилиты

Клиент командной строки включает функциональность для создания закладок URL API под запоминающимся именем. Например, вы можете добавить закладку для существующего API следующим образом...

```bash
$ coreapi bookmarks add accountmanagement
```

Также имеется функциональность для навигации вперед или назад по истории обращений к URL-адресам API.

```bash
$ coreapi history show
$ coreapi history back
```

Для получения дополнительной информации и списка доступных подкоманд используйте `coreapi bookmarks --help` или `coreapi history --help`.

## Другие команды

Для отображения текущего `документа схемы`:

```bash
$ coreapi show
```

Перезагрузить текущий `документ схемы` из сети:

```bash
$ coreapi reload
```

Чтобы загрузить файл схемы с диска:

```bash
$ coreapi load my-api-schema.json --format corejson
```

Вывод текущего `документа схемы` на консоль в заданном формате:

```bash
$ coreapi dump --format openapi
```

Удаление текущего `документа схемы` вместе со всей сохраненной историей, учетными данными, заголовками и закладками:

```bash
$ coreapi clear
```

---

# Клиентская библиотека Python

Пакет `coreapi` Python позволяет вам программно взаимодействовать с любым API, который раскрывает поддерживаемый формат схемы.

## Начало работы

Перед началом работы вам необходимо установить пакет `coreapi` с помощью `pip`.

```bash
$ pip install coreapi
```

Для того чтобы начать работу с API, нам сначала нужен экземпляр `Client`. Клиент содержит любую конфигурацию, определяющую, какие кодеки и транспорты поддерживаются при взаимодействии с API, что позволяет вам обеспечить более продвинутые типы поведения.

```python
import coreapi
client = coreapi.Client()
```

Когда у нас есть экземпляр `Client`, мы можем получить схему API из сети.

```python
schema = client.get('https://api.example.org/')
```

Объект, возвращаемый этим вызовом, будет экземпляром `Document`, который является представлением схемы API.

## Аутентификация

Как правило, при инстанцировании клиента вы также захотите предоставить некоторые учетные данные для аутентификации.

#### Аутентификация с помощью токенов

Класс `TokenAuthentication` можно использовать для поддержки встроенной в REST-фреймворк `TokenAuthentication`, а также схем OAuth и JWT.

```python
auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token='<token>'
)
client = coreapi.Client(auth=auth)
```

При использовании `TokenAuthentication` вам, вероятно, потребуется реализовать процесс входа в систему с помощью клиента CoreAPI.

Предлагаемая схема для этого может заключаться в первоначальном запросе неаутентифицированного клиента к конечной точке "получения токена"

Например, используя пакет "Django REST framework JWT"

```python
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

#### Базовая аутентификация

Класс `BasicAuthentication` можно использовать для поддержки HTTP Basic Authentication.

```python
auth = coreapi.auth.BasicAuthentication(
    username='<username>',
    password='<password>'
)
client = coreapi.Client(auth=auth)
```

## Взаимодействие с API

Теперь, когда у нас есть клиент и мы получили `документ схемы`, мы можем начать взаимодействовать с API:

```python
users = client.action(schema, ['users', 'list'])
```

Некоторые конечные точки могут включать именованные параметры, которые могут быть как необязательными, так и обязательными:

```python
new_user = client.action(schema, ['users', 'create'], params={"username": "max"})
```

## Кодеки

Кодеки отвечают за кодирование или декодирование документов.

Процесс декодирования используется клиентом для получения байтовой строки определения схемы API и возврата Core API `Document`, который представляет этот интерфейс.

Кодек должен быть связан с определенным типом медиа, например `'application/coreapi+json'`.

Этот тип медиа используется сервером в заголовке ответа `Content-Type`, чтобы указать, какой тип данных возвращается в ответе.

#### Конфигурирование кодеков

Доступные кодеки можно настроить при инстанцировании клиента. Здесь используется ключевое слово `декодеры`, потому что в контексте клиента кодеки предназначены только для *декодирования* ответов.

В следующем примере мы настроим клиента на прием только ответов `Core JSON` и `JSON`. Это позволит нам получать и декодировать схему Core JSON, а затем получать ответы JSON, сделанные с помощью API.

```python
from coreapi import codecs, Client

decoders = [codecs.CoreJSONCodec(), codecs.JSONCodec()]
client = Client(decoders=decoders)
```

#### Загрузка и сохранение схем

Вы можете использовать кодек напрямую, чтобы загрузить существующее определение схемы и вернуть полученный `Document`.

```python
input_file = open('my-api-schema.json', 'rb')
schema_definition = input_file.read()
codec = codecs.CoreJSONCodec()
schema = codec.load(schema_definition)
```

Вы также можете использовать кодек непосредственно для генерации определения схемы, заданного экземпляром `Document`:

```python
schema_definition = codec.dump(schema)
output_file = open('my-api-schema.json', 'rb')
output_file.write(schema_definition)
```

## Транспорты

Транспорты отвечают за выполнение сетевых запросов. Набор транспортов, установленных у клиента, определяет, какие сетевые протоколы он может поддерживать.

В настоящее время библиотека `coreapi` включает только транспорт HTTP/HTTPS, но могут поддерживаться и другие протоколы.

#### Конфигурирование транспортов

Поведение сетевого уровня может быть настроено путем конфигурирования транспортов, с которыми инстанцируется клиент.

```python
import requests
from coreapi import transports, Client

credentials = {'api.example.org': 'Token 3bd44a009d16ff'}
transports = transports.HTTPTransport(credentials=credentials)
client = Client(transports=transports)
```

Можно добиться и более сложной настройки, например, модифицировав базовый экземпляр `requests.Session` для [присоединения транспортных адаптеров](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters), которые изменяют исходящие запросы.

---

# Клиентская библиотека JavaScript

Клиентская библиотека JavaScript позволяет вам взаимодействовать с API либо через браузер, либо с помощью node.

## Установка клиента JavaScript

Существует два отдельных ресурса JavaScript, которые необходимо включить в ваши HTML-страницы, чтобы использовать клиентскую библиотеку JavaScript. Это статический файл `coreapi.js`, который содержит код для динамической клиентской библиотеки, и шаблонный ресурс `chema.js`, который описывает схему вашего API.

Сначала добавьте представления документации API. Они будут включать ресурс схемы, который позволит вам загружать схему непосредственно с HTML-страницы, без необходимости выполнять асинхронный вызов AJAX.

```python
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
]
```

Как только URL-адреса документации API будут добавлены, вы сможете включить оба необходимых ресурса JavaScript. Обратите внимание, что порядок этих двух строк важен, поскольку для загрузки схемы требуется, чтобы CoreAPI уже был установлен.

```html
<!--
    Load the CoreAPI library and the API schema.

    /static/rest_framework/js/coreapi-0.1.1.js
    /docs/schema.js
-->
{% load static %}
<script src="{% static 'rest_framework/js/coreapi-0.1.1.js' %}"></script>
<script src="{% url 'api-docs:schema-js' %}"></script>
```

Библиотека `coreapi` и объект `schema` теперь будут доступны на экземпляре `window`.

```javascript
const coreapi = window.coreapi;
const schema = window.schema;
```

## Создание клиента

Для взаимодействия с API вам понадобится экземпляр клиента.

```javascript
var client = new coreapi.Client();
```

Как правило, при инстанцировании клиента вы также захотите предоставить некоторые учетные данные для аутентификации.

#### Аутентификация сеанса

Класс `SessionAuthentication` позволяет сессионным файлам cookie обеспечивать аутентификацию пользователя. Вероятно, вам понадобится стандартный HTML-процесс аутентификации, чтобы позволить пользователю войти в систему, а затем создать клиент, используя сессию:

```javascript
let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken',
});
let client = new coreapi.Client({auth: auth});
```

Схема аутентификации будет обрабатывать включение заголовка CSRF в любые исходящие запросы для небезопасных методов HTTP.

#### Аутентификация с помощью токенов

Класс `TokenAuthentication` можно использовать для поддержки встроенной в REST-фреймворк `TokenAuthentication`, а также схем OAuth и JWT.

```javascript
let auth = new coreapi.auth.TokenAuthentication({
    scheme: 'JWT',
    token: '<token>',
});
let client = new coreapi.Client({auth: auth});
```

При использовании `TokenAuthentication` вам, вероятно, потребуется реализовать процесс входа в систему с помощью клиента CoreAPI.

Предлагаемая схема для этого может заключаться в первоначальном запросе неаутентифицированного клиента к конечной точке "получения токена"

Например, используя пакет "Django REST framework JWT"

```javascript
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

#### Базовая аутентификация

Класс `BasicAuthentication` можно использовать для поддержки базовой аутентификации HTTP.

```javascript
let auth = new coreapi.auth.BasicAuthentication({
    username: '<username>',
    password: '<password>',
})
let client = new coreapi.Client({auth: auth});
```

## Использование клиента

Выполнение запросов:

```javascript
let action = ["users", "list"];
client.action(schema, action).then(function(result) {
    // Return value is in 'result'
})
```

Включая параметры:

```javascript
let action = ["users", "create"];
let params = {username: "example", email: "example@example.com"};
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
})
```

Обработка ошибок:

```javascript
client.action(schema, action, params).then(function(result) {
    // Return value is in 'result'
}).catch(function (error) {
    // Error value is in 'error'
})
```

## Установка с помощью node

Пакет coreapi доступен в NPM.

```bash
$ npm install coreapi
$ node
const coreapi = require('coreapi')
```

Вы захотите либо включить схему API в свою кодовую базу напрямую, скопировав ее из ресурса `schema.js`, либо загрузить схему асинхронно. Например:

```javascript
let client = new coreapi.Client();
let schema = null;
client.get("https://api.example.org/").then(function(data) {
    // Load a CoreJSON API schema.
    schema = data;
    console.log('schema loaded');
})
```
