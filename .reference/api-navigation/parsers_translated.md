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

> Машины взаимодействия веб-сервисов, как правило, используют более структурированные форматы для отправки данных, чем кодируемые формой, поскольку они отправляют более сложные данные, чем простые формы
>
>-Malcom Tredinnick, [Django Developers Group] (https://groups.google.com/d/topic/django-developers/dxi4qvzrby4/discussion)

REST framework includes a number of built in Parser classes, that allow you to accept requests with various media types. There is also support for defining your own custom parsers, which gives you the flexibility to design the media types that your API accepts.

Структура REST включает в себя ряд встроенных классов анализаторов, которые позволяют вам принимать запросы с различными типами носителя.
Существует также поддержка определения ваших собственных пользовательских анализаторов, что дает вам гибкость для разработки типов мультимедиа, которые принимает ваш API.

## How the parser is determined

## Как определяется анализатор

The set of valid parsers for a view is always defined as a list of classes. When `request.data` is accessed, REST framework will examine the `Content-Type` header on the incoming request, and determine which parser to use to parse the request content.

Набор действительных анализаторов для представления всегда определяется как список классов.
Когда доступ к `request.data`, Framework REST рассмотрит заголовок« Контент-тип »в входящем запросе и определит, какой анализатор использовать для анализа контента запроса.

---

**Note**: When developing client applications always remember to make sure you're setting the `Content-Type` header when sending data in an HTTP request.

** ПРИМЕЧАНИЕ **: При разработке клиентских приложений всегда не забудьте убедиться, что вы устанавливаете заголовок «Контент-тип» при отправке данных в HTTP-запросе.

If you don't set the content type, most clients will default to using `'application/x-www-form-urlencoded'`, which may not be what you wanted.

Если вы не установите тип контента, большинство клиентов по умолчанию по умолчанию используют `'Application/x-Www-form-urlencoded'», что может не быть тем, что вы хотели.

As an example, if you are sending `json` encoded data using jQuery with the [.ajax() method](https://api.jquery.com/jQuery.ajax/), you should make sure to include the `contentType: 'application/json'` setting.

В качестве примера, если вы отправляете кодируемые данные json` с использованием jQuery с помощью method [.ajax ()] (https://api.jquery.com/jquery.ajax/), вы должны убедиться, что `contenttype
: 'Приложение/json'' настройка.

---

## Setting the parsers

## Установка анализаторов

The default set of parsers may be set globally, using the `DEFAULT_PARSER_CLASSES` setting. For example, the following settings would allow only requests with `JSON` content, instead of the default of JSON or form data.

Набор анализаторов по умолчанию может быть установлен по всему миру, используя настройку `default_parser_classes`.
Например, следующие настройки позволят только запросы с контентом `json`, а не по умолчанию данных JSON или формы.

```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

You can also set the parsers used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить анализаторы, используемые для отдельного представления, или Viewset, используя представления на основе класса Apiview`.

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

Или, если вы используете декоратор `@api_view` с видами на основе функций.

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

# Ссылка на API

## JSONParser

## jsonparser

Parses `JSON` request content. `request.data` will be populated with a dictionary of data.

Подготовки `json 'запросить контент.
`request.data` будет заполнен словарем данных.

**.media_type**: `application/json`

**. Media_type **: `Приложение/JSON`

## FormParser

## FormParser

Parses HTML form content. `request.data` will be populated with a `QueryDict` of data.

Подборна HTML формирует содержание.
`request.data` будет заполнен« QueryDict »данных.

You will typically want to use both `FormParser` and `MultiPartParser` together in order to fully support HTML form data.

Обычно вы захотите использовать как «FormParser», так и `MultyParperSer`, чтобы полностью поддержать данные формы HTML.

**.media_type**: `application/x-www-form-urlencoded`

**. Media_type **: `Приложение/X-WWW-FORM-URLENCODED`

## MultiPartParser

## MultipartParser

Parses multipart HTML form content, which supports file uploads. `request.data` and `request.FILES` will be populated with a `QueryDict` and `MultiValueDict` respectively.

SACLSES Multipart HTML Form Content, который поддерживает загрузки файлов.
`request.data` и` request.files` будет заполнен «QueryDict» и «Multivaluedict» соответственно.

You will typically want to use both `FormParser` and `MultiPartParser` together in order to fully support HTML form data.

Обычно вы захотите использовать как «FormParser», так и `MultyParperSer`, чтобы полностью поддержать данные формы HTML.

**.media_type**: `multipart/form-data`

**. media_type **: `multipart/form-data`

## FileUploadParser

## fileuploadParser

Parses raw file upload content. The `request.data` property will be a dictionary with a single key `'file'` containing the uploaded file.

SANASES RAW FILE Загрузить содержимое.
Свойство `request.data` будет словарем с одним ключом« файл », содержащим загруженный файл.

If the view used with `FileUploadParser` is called with a `filename` URL keyword argument, then that argument will be used as the filename.

Если представление, используемое с `fileuploadParser`, вызывается с аргументом ключевого слова« файл », то этот аргумент будет использоваться в качестве имени файла.

If it is called without a `filename` URL keyword argument, then the client must set the filename in the `Content-Disposition` HTTP header. For example `Content-Disposition: attachment; filename=upload.jpg`.

Если он вызывается без аргумента ключевого слова «файл», то клиент должен установить имя файла в заголовке http `http` content-disposition.
Например, «Контент-распада: вложение;
filename = upload.jpg`.

**.media_type**: `*/*`

**. media_type **: `*/*`

##### Notes:

##### Заметки:

* The `FileUploadParser` is for usage with native clients that can upload the file as a raw data request. For web-based uploads, or for native clients with multipart upload support, you should use the `MultiPartParser` instead.
* Since this parser's `media_type` matches any content type, `FileUploadParser` should generally be the only parser set on an API view.
* `FileUploadParser` respects Django's standard `FILE_UPLOAD_HANDLERS` setting, and the `request.upload_handlers` attribute. See the [Django documentation](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers) for more details.

* FileuploadParser` предназначен для использования с родными клиентами, которые могут загружать файл в качестве необработанного запроса данных.
Для веб-загрузки или для нативных клиентов с поддержкой загрузки Multipart вам следует вместо этого использовать `MultipartParser.
* Поскольку этот анализатор `media_type` соответствует любому типу контента,` fileuploadparser`, как правило, должен быть единственным набором анализатора в представлении API.
* `FileuploadParser` уважает стандартную настройку django` file_upload_handlers` и атрибут `request.upload_handlers`.
См. Документация Django] (https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers) для получения более подробной информации.

##### Basic usage example:

##### Пример базового использования:

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

# Пользовательские анализаторы

To implement a custom parser, you should override `BaseParser`, set the `.media_type` property, and implement the `.parse(self, stream, media_type, parser_context)` method.

Чтобы реализовать пользовательский анализатор, вы должны переопределить «BaseParser», установить свойство `.media_type` и реализовать метод` .parse (self, Stream, media_type, parser_context) `.

The method should return the data that will be used to populate the `request.data` property.

Метод должен вернуть данные, которые будут использоваться для заполнения свойства `request.data`.

The arguments passed to `.parse()` are:

Аргументы переданы `.parse ()` являются:

### stream

### ручей

A stream-like object representing the body of the request.

Поток, похожий на поток, представляющий корпус запроса.

### media_type

### media_type

Optional. If provided, this is the media type of the incoming request content.

По желанию.
Если предоставлено, это тип медиа входящего контента запроса.

Depending on the request's `Content-Type:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters. For example `"text/plain; charset=utf-8"`.

В зависимости от заголовка «Контент-тип:` », это может быть более конкретным, чем атрибут рендеринга` media_type`, и может включать параметры типа носителя.
Например, `" Text/plain; charset = utf-8 "`.

### parser_context

### parser_context

Optional. If supplied, this argument will be a dictionary containing any additional context that may be required to parse the request content.

По желанию.
В случае предоставления, этот аргумент будет словарем, содержащим любой дополнительный контекст, который может потребоваться для анализа содержания запроса.

By default this will include the following keys: `view`, `request`, `args`, `kwargs`.

По умолчанию это будет включать в себя следующие ключи: `view`,` request`, `args`,` kwargs`.

## Example

## Пример

The following is an example plaintext parser that will populate the `request.data` property with a string representing the body of the request.

Ниже приведен пример анализаторов открытого текста, который заполнит свойство `request.data` строкой, представляющей тело запроса.

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

# Сторонние пакеты

The following third party packages are also available.

Следующие сторонние пакеты также доступны.

## YAML

## yaml

[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/) provides [YAML](http://www.yaml.org/) parsing and rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[Rest Framework Yaml] (https://jpadilla.github.io/django-rest-framework-yaml/) предоставляет [yaml] (http://www.yaml.org/) поддержка и рендеринга.
Ранее он был включен непосредственно в пакет Framework REST и теперь вместо этого поддерживается как сторонний пакет.

#### Installation & configuration

#### Установка и конфигурация

Install using pip.

Установите с помощью PIP.

```
$ pip install djangorestframework-yaml
```

Modify your REST framework settings.

Измените настройки структуры REST.

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

## xml

[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/) provides a simple informal XML format. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[Framework REST XML] (https://jpadilla.github.io/django-rest-framework-xml/) предоставляет простой неформальный формат XML.
Ранее он был включен непосредственно в пакет Framework REST и теперь вместо этого поддерживается как сторонний пакет.

#### Installation & configuration

#### Установка и конфигурация

Install using pip.

Установите с помощью PIP.

```
$ pip install djangorestframework-xml
```

Modify your REST framework settings.

Измените настройки структуры REST.

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

[MessagePack] (https://github.com/juanriaza/django-rest-framework-msgpack) является быстрым, эффективным форматом бинарной сериализации.
[Juan Riaza] (https://github.com/juanriaza) поддерживает [djangestframework-msgpack] (https://github.com/juanriaza/django-rest-framework-msgpac
Структура отдыха.

## CamelCase JSON

## Camelcase Json

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) provides camel case JSON renderers and parsers for REST framework. This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names. It is maintained by [Vitaly Babiy](https://github.com/vbabiy).

[djangorestframework-camel-case] (https://github.com/vbabiy/djangorestframework-camel-case) обеспечивает визуализаторы и анализаторов верблюда для кабеля и анализаторов.
Это позволяет сериализаторам использовать имена поля в стиле Python, но в API выставлены в качестве имен поля для верблюжьего корпуса в стиле JavaScript.
Это поддерживается [Vitaly Babiy] (https://github.com/vbabiy).