<!-- TRANSLATED by md-translate -->
---

source:

источник:

* parsers.py

* parsers.py

---

# Parsers

# Парсеры

> Machine interacting web services tend to use more structured formats for sending data than form-encoded, since they're sending more complex data than simple forms
>
> — Malcom Tredinnick, [Django developers group](https://groups.google.com/d/topic/django-developers/dxI4qVzrBY4/discussion)

> Взаимодействующие с машинами веб-сервисы, как правило, используют более структурированные форматы для отправки данных, чем кодированные формы, поскольку они отправляют более сложные данные, чем простые формы
>
> - Малком Трединник, [группа разработчиков Django](https://groups.google.com/d/topic/django-developers/dxI4qVzrBY4/discussion)

REST framework includes a number of built in Parser classes, that allow you to accept requests with various media types. There is also support for defining your own custom parsers, which gives you the flexibility to design the media types that your API accepts.

Фреймворк REST включает ряд встроенных классов Parser, которые позволяют принимать запросы с различными типами носителей. Также имеется поддержка определения собственных парсеров, что дает вам гибкость в определении типов медиа, которые принимает ваш API.

## How the parser is determined

## Как определяется синтаксический анализатор

The set of valid parsers for a view is always defined as a list of classes. When `request.data` is accessed, REST framework will examine the `Content-Type` header on the incoming request, and determine which parser to use to parse the request content.

Набор допустимых парсеров для представления всегда определяется как список классов. Когда происходит обращение к `request.data`, REST framework изучает заголовок `Content-Type` входящего запроса и определяет, какой парсер использовать для разбора содержимого запроса.

---

**Note**: When developing client applications always remember to make sure you're setting the `Content-Type` header when sending data in an HTTP request.

**Примечание**: При разработке клиентских приложений всегда помните о том, что при отправке данных в HTTP-запросе нужно обязательно устанавливать заголовок `Content-Type`.

If you don't set the content type, most clients will default to using `'application/x-www-form-urlencoded'`, which may not be what you wanted.

Если вы не зададите тип содержимого, большинство клиентов по умолчанию будут использовать `'application/x-www-form-urlencoded'', что может оказаться не тем, чего вы хотели.

As an example, if you are sending `json` encoded data using jQuery with the [.ajax() method](https://api.jquery.com/jQuery.ajax/), you should make sure to include the `contentType: 'application/json'` setting.

В качестве примера, если вы отправляете закодированные данные `json` с помощью jQuery с методом [.ajax()] (https://api.jquery.com/jQuery.ajax/), вы должны обязательно включить параметр `contentType: 'application/json'`.

---

## Setting the parsers

## Настройка парсеров

The default set of parsers may be set globally, using the `DEFAULT_PARSER_CLASSES` setting. For example, the following settings would allow only requests with `JSON` content, instead of the default of JSON or form data.

Набор парсеров по умолчанию можно задать глобально, используя параметр `DEFAULT_PARSER_CLASSES`. Например, следующие настройки разрешают только запросы с содержимым `JSON`, вместо стандартного JSON или данных формы.

```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

You can also set the parsers used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить парсеры, используемые для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        return Response({'received data': request.data})
```

Or, if you're using the `@api_view` decorator with function based views.

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes([JSONParser])
def example_view(request, format=None):
    """
    A view that can accept POST requests with JSON content.
    """
    return Response({'received data': request.data})
```

---

# API Reference

# API Reference

## JSONParser

## JSONParser

Parses `JSON` request content. `request.data` will be populated with a dictionary of data.

Разбирает `JSON` содержимое запроса. `request.data` будет заполнен словарем данных.

**.media_type**: `application/json`

**.media_type**: `application/json`.

## FormParser

## FormParser

Parses HTML form content. `request.data` will be populated with a `QueryDict` of data.

Разбирает содержимое HTML-формы. `request.data` будет заполнен `QueryDict` данных.

You will typically want to use both `FormParser` and `MultiPartParser` together in order to fully support HTML form data.

Для полной поддержки данных HTML-формы обычно требуется использовать `FormParser` и `MultiPartParser` вместе.

**.media_type**: `application/x-www-form-urlencoded`

**.media_type**: `application/x-www-form-urlencoded`.

## MultiPartParser

## MultiPartParser

Parses multipart HTML form content, which supports file uploads. `request.data` and `request.FILES` will be populated with a `QueryDict` and `MultiValueDict` respectively.

Разбирает содержимое многокомпонентной HTML-формы, которая поддерживает загрузку файлов. `request.data` и `request.FILES` будут заполнены `QueryDict` и `MultiValueDict` соответственно.

You will typically want to use both `FormParser` and `MultiPartParser` together in order to fully support HTML form data.

Для полной поддержки данных HTML-формы обычно требуется использовать `FormParser` и `MultiPartParser` вместе.

**.media_type**: `multipart/form-data`

**.media_type**: `multipart/form-data`.

## FileUploadParser

## FileUploadParser

Parses raw file upload content. The `request.data` property will be a dictionary with a single key `'file'` containing the uploaded file.

Разбирает необработанное содержимое загружаемого файла. Свойство `request.data` будет представлять собой словарь с единственным ключом `'file'`, содержащим загруженный файл.

If the view used with `FileUploadParser` is called with a `filename` URL keyword argument, then that argument will be used as the filename.

Если представление, используемое с `FileUploadParser`, вызывается с аргументом ключевого слова URL `filename`, то этот аргумент будет использоваться в качестве имени файла.

If it is called without a `filename` URL keyword argument, then the client must set the filename in the `Content-Disposition` HTTP header. For example `Content-Disposition: attachment; filename=upload.jpg`.

Если он вызывается без ключевого аргумента URL `filename`, то клиент должен установить имя файла в HTTP-заголовке `Content-Disposition`. Например, `Content-Disposition: attachment; filename=upload.jpg`.

**.media_type**: `*/*`

**.media_type**: `*/*`

##### Notes:

##### Примечания:

* The `FileUploadParser` is for usage with native clients that can upload the file as a raw data request. For web-based uploads, or for native clients with multipart upload support, you should use the `MultiPartParser` instead.
* Since this parser's `media_type` matches any content type, `FileUploadParser` should generally be the only parser set on an API view.
* `FileUploadParser` respects Django's standard `FILE_UPLOAD_HANDLERS` setting, and the `request.upload_handlers` attribute. See the [Django documentation](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers) for more details.

* `FileUploadParser` предназначен для использования с собственными клиентами, которые могут загружать файл как запрос необработанных данных. Для веб-загрузки или для собственных клиентов с поддержкой многочастной загрузки вместо него следует использовать `MultiPartParser`.
* Поскольку `media_type` этого парсера соответствует любому типу содержимого, `FileUploadParser` обычно должен быть единственным парсером, установленным в представлении API.
* `FileUploadParser` уважает стандартную настройку Django `FILE_UPLOAD_HANDLERS` и атрибут `request.upload_handlers`. Более подробную информацию смотрите в [документации Django](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers).

##### Basic usage example:

##### Базовый пример использования:

```
# views.py
class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

# urls.py
urlpatterns = [
    # ...
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
```

---

# Custom parsers

# Пользовательские синтаксические анализаторы

To implement a custom parser, you should override `BaseParser`, set the `.media_type` property, and implement the `.parse(self, stream, media_type, parser_context)` method.

Для реализации пользовательского парсера необходимо переопределить `BaseParser`, установить свойство `.media_type` и реализовать метод `.parse(self, stream, media_type, parser_context)`.

The method should return the data that will be used to populate the `request.data` property.

Метод должен возвращать данные, которые будут использоваться для заполнения свойства `request.data`.

The arguments passed to `.parse()` are:

Аргументами, передаваемыми в `.parse()`, являются:

### stream

### поток

A stream-like object representing the body of the request.

Потокоподобный объект, представляющий тело запроса.

### media_type

### media_type

Optional. If provided, this is the media type of the incoming request content.

Дополнительно. Если указано, это тип носителя содержимого входящего запроса.

Depending on the request's `Content-Type:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters. For example `"text/plain; charset=utf-8"`.

В зависимости от заголовка `Content-Type:` запроса, он может быть более конкретным, чем атрибут `media_type` рендерера, и может включать параметры типа медиа. Например, `"text/plain; charset=utf-8"`.

### parser_context

### parser_context

Optional. If supplied, this argument will be a dictionary containing any additional context that may be required to parse the request content.

Дополнительно. Если этот аргумент указан, то он будет представлять собой словарь, содержащий любой дополнительный контекст, который может потребоваться для разбора содержимого запроса.

By default this will include the following keys: `view`, `request`, `args`, `kwargs`.

По умолчанию сюда входят следующие ключи: `view`, `request`, `args`, `kwargs`.

## Example

## Пример

The following is an example plaintext parser that will populate the `request.data` property with a string representing the body of the request.

Ниже приведен пример анализатора обычного текста, который заполнит свойство `request.data` строкой, представляющей тело запроса.

```
class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
```

---

# Third party packages

# Пакеты сторонних производителей

The following third party packages are also available.

Также доступны следующие пакеты сторонних производителей.

## YAML

## YAML

[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/) provides [YAML](http://www.yaml.org/) parsing and rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/) обеспечивает поддержку разбора и рендеринга [YAML](http://www.yaml.org/). Ранее он был включен непосредственно в пакет REST framework, а теперь поддерживается как сторонний пакет.

#### Installation & configuration

#### Установка и настройка

Install using pip.

Установите с помощью pip.

```
$ pip install djangorestframework-yaml
```

Modify your REST framework settings.

Измените настройки фреймворка REST.

```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_yaml.parsers.YAMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_yaml.renderers.YAMLRenderer',
    ],
}
```

## XML

## XML

[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/) provides a simple informal XML format. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/) предоставляет простой неформальный формат XML. Ранее он был включен непосредственно в пакет REST Framework, а теперь поддерживается как сторонний пакет.

#### Installation & configuration

#### Установка и настройка

Install using pip.

Установите с помощью pip.

```
$ pip install djangorestframework-xml
```

Modify your REST framework settings.

Измените настройки фреймворка REST.

```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_xml.parsers.XMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_xml.renderers.XMLRenderer',
    ],
}
```

## MessagePack

## MessagePack

[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack) is a fast, efficient binary serialization format. [Juan Riaza](https://github.com/juanriaza) maintains the [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack) package which provides MessagePack renderer and parser support for REST framework.

[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack) - это быстрый и эффективный формат двоичной сериализации. [Juan Riaza](https://github.com/juanriaza) поддерживает пакет [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack), который обеспечивает поддержку рендеринга и парсера MessagePack для фреймворка REST.

## CamelCase JSON

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) provides camel case JSON renderers and parsers for REST framework. This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names. It is maintained by [Vitaly Babiy](https://github.com/vbabiy).

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет рендереры и парсеры JSON в верблюжьем регистре для REST-фреймворка. Это позволяет сериализаторам использовать имена полей в стиле Python с подчеркиванием, но отображать их в API как имена полей в верблюжьем регистре в стиле Javascript. Поддерживается [Виталием Бабием](https://github.com/vbabiy).