# Парсеры

> При отправке данных используются более сложные форматы, чем основанные на простых формах.
> 
> — Malcom Tredinnick, Django developers group

REST framework включает некоторое количество встроенных классов парсеров, которые позволяют принимать запросы различных типов медиа. Также они дают возможность определять ваши собственные парсеры для гибкой настройки типов медиа, которые принимает ваш API. 

## Как происходит определение парсера

Набор валидных парсеров для представления всегда определяется как список классов. При обращении к `request.data` REST framework исследует заголовок `Content-Type` на наличие входящего запроса и определяет какой парсер использовать для пасрсинга содеражния запроса.

Примечание: При разработке клиентских приложений всегда проверяйте наличие заговолока `Content-Type` при отправке данных в HTTP запросе.

Если вы не уставновили тип контента, большинство клиентов буду по умолчанию использовать 'application/x-www-form-urlencoded' и возможно это не то, чего бы вы хотели.

К примеру, если вы используете json данные с помощью jQuery и метода `.ajax()`, то вы должны удостовериться, что указали настройку `contentType: 'application/json'`

## Установка парсеров

По умолчанию набор парсеров можно установить глобально, используя настройку `DEFAULT_PARSER_CLASSES`. Например, следующие настройки делают так, что допускаются лишь запросы, содержащие `JSON`, вместо парсеров по умолчанию, которые допускают как JSON, так и формы.

```python

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}
```

Вы также можете установить парсеры для индивидуальных представлений или viewset с помощью классов-представлений `APIView`.

```python

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    """
    Представление, которое может принимать запросы POST с контентом JSON.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        return Response({'received data': request.data})
```

Или, если вы используете декоратор `@api_view` с представлениями-функциямим.

```python

from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes((JSONParser,))
def example_view(request, format=None):
    """
    Представление, которое может принимать запросы POST с контентом JSON.
    """
    return Response({'received data': request.data})
```

# Обращение к API

## JSONParser

Парсит контент JSON.

**.media_type**: application/json

## FormParser

Парсит контент HTML форм. `request.data` будет заполнен данными из `QueryDict`.

Предпочтительнее использовать одновременно `FormParser` и `MultiPartParser` для того чтобы обеспечить наиболее полную поддержику данных форм HTML.

**.media_type**: `application/x-www-form-urlencoded`

## MultiPartParser

Парсит многокомпонентный контент HTML форм, который поддерживает загрузку файлов. Обе `request.data` буду заполнены из `QueryDict`.

Предпочтительнее использовать одновременно `FormParser` и `MultiPartParser` для того чтобы обеспечить наиболее полную поддержику данных форм HTML.

**.media_type**: `.media_type: multipart/form-data`

## FileUploadParser

Парсит необработанный контент. Свойство `request.data` является словарем с единственным ключом 'file', который содержит загруженный файл.

Если представление, использующееся с `FileUploadParser` вызывается с аргументом `filename` в ключе URL, то данный аргумент будет использоваться в качестве имени файла.

Если оно вызвано без аргумента `filename`, то клиент должен прописать имя файла в загаловке HTTP `Content-Disposition`. Например `Content-Disposition: attachment; filename=upload.jpg.`

**.media_type**: */*

Замечания:

* `FileUploadParser` используется с native клиентом, который может загружать файл в виде необработанных запросов. Для web-based загрузок, или для native клиентов с поддержкой многокомпонентной загрузки, вы должны использовать парсер `MultiPartParser`. 
* Так как `media_type` парсера согласуется с любым типом контента `FileUploadParser` по большому счету должен быть единственным парсером, установленным на представлении API.
* `FileUploadParser` не конфликтует с стандартной настройкой Джанго `FILE_UPLOAD_HANDLERS` и атрибутом `request.upload_handlers`. Для подробностей см [документацию Джанго](https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#upload-handlers).    

Пример основного использования:

```python

# views.py
class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

# urls.py
urlpatterns = [
    # ...
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
```
# Кастомные парсеры

Для того, чтобы применить кастомный парсер, вы должны переписать `BaseParser`, установить свойство `.media_type` и применить метод `.parse(self, stream, media_type, parser_context)`.

Метод должен возвращать данные, которые заполняют свойство `request.data`.

Следующие аргументы передаются `.parse()`:

### stream
Потоковый объект, представляющий тело запроса.

### media_type

Опционально. При наличии, представляет тип медиа контента входящего запроса.

В зависимости от заголовка  запроcа`Content-Type`: может включать параметры медиа типов. Например "text/plain; charset=utf-8".

### parser_context

Опционально. Если поддерживается, то этот аргумент представляет из себя словарь, содержащий любой дополнительный контекст, который может потребоваться для того, чтобы спарсить запрос.

По умочанию содержит следующие ключи: view, request, args, kwargs.

## Пример

Ниже следует пример plaintext парсера, который заполняет свойство `request.data` строкой, представляющей тело запроса.

```python
class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Возвращает строку, представляющую тело запроса.
        """
        return stream.read()
```

## Сторонние пакеты

Доступны следующие сторонние пакеты.

## YAML

[REST framework YAML](http://jpadilla.github.io/django-rest-framework-yaml/) поддерживает парсинг YAML и рендеринг. До этого он был установлен в REST framework по умолчанию, а теперь доступен в качестве стороннего пакета.

### Установка и настройка

Установка с помощью pip

```python
$ pip install djangorestframework-yaml
```

Изменение настроек REST framework

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_yaml.renderers.YAMLRenderer',
    ),
}
```

## XML

[REST Framework XML](http://jpadilla.github.io/django-rest-framework-xml/) поддерживает неформальный формат XML. До этого он был установлен в REST framework по умолчанию, а теперь доступен в качестве стороннего пакета.

### Установка и настройка

Установка с помощью pip

```python
$ pip install djangorestframework-xml
```

Изменение настроек REST framework

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_xml.renderers.XMLRenderer',
    ),
}
```

## MessagePack

[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack) это быстрый и эффектиный бинарный формат сериализации.

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет camel case рендеры и парсеры для JSON. Это позволит сериализаторам использовать имена полей в подчеркнутом стиле Питона, но при поля будут доступны в API в стиле camel case Javascript.
