<!-- TRANSLATED by md-translate -->
# Парсеры

> Взаимодействующие с машинами веб-сервисы, как правило, используют более структурированные форматы для отправки данных, чем кодированные формы, поскольку они отправляют более сложные данные, чем простые формы
>
> - Малком Трединник, [группа разработчиков Django](https://groups.google.com/d/topic/django-developers/dxI4qVzrBY4/discussion)

DRF включает ряд встроенных классов `Parser`, которые позволяют принимать запросы с различными типами носителей. Также имеется возможность определения собственных парсеров, что дает вам гибкость в определении типов медиа, которые принимает ваш API.

## Как определяется парсер

Набор допустимых парсеров для представления всегда определяется как список классов. Когда происходит обращение к `request.data`, DRF изучает заголовок `Content-Type` входящего запроса и определяет, какой парсер использовать для разбора содержимого запроса.

---

**Примечание**: При разработке клиентских приложений всегда помните о том, что при отправке данных в HTTP-запросе нужно обязательно устанавливать заголовок `Content-Type`.

Если вы не зададите тип содержимого, большинство клиентов по умолчанию будут использовать `'application/x-www-form-urlencoded'', что может оказаться не тем, чего вы хотели.

В качестве примера, если вы отправляете закодированные данные `json` с помощью jQuery с методом [.ajax()](https://api.jquery.com/jQuery.ajax/), вы должны обязательно включить параметр `contentType: 'application/json'`.

---

## Настройка парсеров

Набор парсеров по умолчанию можно задать глобально, используя параметр `DEFAULT_PARSER_CLASSES`. Например, следующие настройки разрешают только запросы с содержимым `JSON`, вместо стандартного JSON или данных формы.

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

Вы также можете установить парсеры, используемые для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```python
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

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```python
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

## JSONParser

Разбирает `JSON` содержимое запроса. `request.data` будет заполнен словарем данных.

**.media_type**: `application/json`.

## FormParser

Разбирает содержимое HTML-формы. `request.data` будет заполнен `QueryDict` данных.

Для полной поддержки данных HTML-формы обычно требуется использовать `FormParser` и `MultiPartParser` вместе.

**.media_type**: `application/x-www-form-urlencoded`.

## MultiPartParser

Разбирает содержимое многокомпонентной HTML-формы, которая поддерживает загрузку файлов. `request.data` и `request.FILES` будут заполнены `QueryDict` и `MultiValueDict` соответственно.

Для полной поддержки данных HTML-формы обычно требуется использовать `FormParser` и `MultiPartParser` вместе.

**.media_type**: `multipart/form-data`.

## FileUploadParser

Разбирает необработанное содержимое загружаемого файла. Свойство `request.data` будет представлять собой словарь с единственным ключом `'file'`, содержащим загруженный файл.

Если представление, используемое с `FileUploadParser`, вызывается с именованным аргументом URL `filename`, то этот аргумент будет использоваться в качестве имени файла.

Если он вызывается без именованного аргумента URL `filename`, то клиент должен установить имя файла в HTTP-заголовке `Content-Disposition`. Например, `Content-Disposition: attachment; filename=upload.jpg`.

**.media_type**: `*/*`

##### Примечания:

* `FileUploadParser` предназначен для использования с собственными клиентами, которые могут загружать файл как запрос необработанных данных. Для веб-загрузки или для собственных клиентов с поддержкой многочастной загрузки вместо него следует использовать `MultiPartParser`.
* Поскольку `media_type` этого парсера соответствует любому типу содержимого, `FileUploadParser` обычно должен быть единственным парсером, установленным в представлении API.
* `FileUploadParser` учитывает стандартную настройку Django `FILE_UPLOAD_HANDLERS` и атрибут `request.upload_handlers`. Более подробную информацию смотрите в [документации Django](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers).

##### Базовый пример использования:

```python
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

# Пользовательские синтаксические анализаторы

Для реализации пользовательского парсера необходимо переопределить `BaseParser`, установить свойство `.media_type` и реализовать метод `.parse(self, stream, media_type, parser_context)`.

Метод должен возвращать данные, которые будут использоваться для заполнения свойства `request.data`.

Аргументами, передаваемыми в `.parse()`, являются:

### stream

Потокоподобный объект, представляющий тело запроса.

### media_type

Необзательно. Если указано, это тип носителя содержимого входящего запроса.

В зависимости от заголовка `Content-Type:` запроса, он может быть более конкретным, чем атрибут `media_type` рендерера, и может включать параметры типа медиа. Например, `"text/plain; charset=utf-8"`.

### parser_context

Необзательно. Если этот аргумент указан, то он будет представлять собой словарь, содержащий любой дополнительный контекст, который может потребоваться для разбора содержимого запроса.

По умолчанию сюда входят следующие ключи: `view`, `request`, `args`, `kwargs`.

## Пример

Ниже приведен пример анализатора обычного текста, который заполнит свойство `request.data` строкой, представляющей тело запроса.

```python
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

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## YAML

[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/) обеспечивает поддержку разбора и рендеринга [YAML](http://www.yaml.org/). Ранее он был включен непосредственно в пакет DRF, а теперь поддерживается как сторонний пакет.

#### Установка и настройка

Установите с помощью pip.

```bash
$ pip install djangorestframework-yaml
```

Измените настройки DRF.

```python
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

[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/) предоставляет простой неформальный формат XML. Ранее он был включен непосредственно в пакет DRF, а теперь поддерживается как сторонний пакет.

#### Установка и настройка

Установите с помощью pip.

```bash
$ pip install djangorestframework-xml
```

Измените настройки DRF.

```python
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

[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack) - это быстрый и эффективный формат двоичной сериализации. [Juan Riaza](https://github.com/juanriaza) поддерживает пакет [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack), который обеспечивает поддержку рендеринга и парсера MessagePack для DRF.

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет рендереры и парсеры JSON в верблюжьем регистре для DRF. Это позволяет сериализаторам использовать имена полей в стиле Python с подчеркиванием, но отображать их в API как имена полей в верблюжьем регистре в стиле Javascript. Поддерживается [Виталием Бабием](https://github.com/vbabiy).
