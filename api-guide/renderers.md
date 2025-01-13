<!-- TRANSLATED by md-translate -->
# Рендереры

> Прежде чем экземпляр `TemplateResponse` будет возвращен клиенту, он должен быть отрендерен. Процесс рендеринга принимает промежуточное представление шаблона и контекста и превращает его в конечный поток байтов, который может быть передан клиенту.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process)

DRF включает ряд встроенных классов Renderer, которые позволяют возвращать ответы с различными типами медиа. Также имеется поддержка определения собственных пользовательских рендереров, что дает вам гибкость в разработке собственных типов медиа.

## Как определяется рендерер

Набор допустимых рендерингов для представления всегда определяется как список классов. При входе в представление DRF будет выполнять согласование содержимого входящего запроса и определять наиболее подходящий рендерер для удовлетворения запроса.

Основной процесс согласования содержимого включает в себя изучение заголовка `Accept` запроса, чтобы определить, какие типы медиа ожидаются в ответе. По желанию, суффиксы формата в URL могут быть использованы для явного запроса определенного представления. Например, URL `http://example.com/api/users_count.json` может быть конечной точкой, которая всегда возвращает данные в формате JSON.

Для получения дополнительной информации смотрите документацию по [согласованию контента](content-negotiation.md).

## Установка рендереров

Набор рендеров по умолчанию можно задать глобально, используя параметр `DEFAULT_RENDERER_CLASSES`. Например, следующие настройки будут использовать `JSON` в качестве основного типа медиа, а также включать API самоописания.

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

Вы также можете установить рендереры, используемые для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```python
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
```

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```python
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_count_view(request, format=None):
    """
    A view that returns the count of active users in JSON.
    """
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
```

## Упорядочивание классов рендеринга

Важно при определении классов рендеринга для вашего API подумать о том, какой приоритет вы хотите присвоить каждому типу медиа. Если клиент недоопределяет представления, которые он может принимать, например, посылает заголовок `Accept: */*` заголовок, или вообще не включает заголовок `Accept`, то DRF выберет первый рендерер в списке для использования в ответе.

Например, если ваш API обслуживает JSON-ответы и HTML-просмотр, вы можете сделать `JSONRenderer` рендерером по умолчанию, чтобы отправлять `JSON` ответы клиентам, которые не указывают заголовок `Accept`.

Если ваш API включает представления, которые могут обслуживать как обычные веб-страницы, так и ответы API в зависимости от запроса, то вы можете сделать `TemplateHTMLRenderer` рендерером по умолчанию, чтобы хорошо работать со старыми браузерами, которые отправляют [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers).

---

# API Reference

## JSONRenderer

Переводит данные запроса в `JSON`, используя кодировку `utf-8`.

Обратите внимание, что стиль по умолчанию включает символы юникода и отображает ответ, используя компактный стиль без лишних пробелов:

```python
{"unicode black star":"★","value":999}
```

Клиент может дополнительно включить параметр медиатипа `'indent'`, в этом случае возвращаемый `JSON` будет иметь отступ. Например, `Accept: application/json; indent=4`.

```python
{
    "unicode black star": "★",
    "value": 999
}
```

Стиль кодировки JSON по умолчанию может быть изменен с помощью ключей настроек `UNICODE_JSON` и `COMPACT_JSON`.

**.media_type**: `application/json`.

**.format**: `'json'`.

**.charset**: `None`.

## TemplateHTMLRenderer

Рендерит данные в HTML, используя стандартный шаблонный рендеринг Django. В отличие от других рендерингов, данные, передаваемые в `Response`, не нужно сериализовать. Также, в отличие от других рендереров, вы можете включить аргумент `template_name` при создании `Response`.

TemplateHTMLRenderer создаст `RequestContext`, используя `response.data` в качестве диктанта контекста, и определит имя шаблона, который будет использоваться для рендеринга контекста.

---

**Примечание:** При использовании с представлением, которое использует сериализатор, `Response`, отправленный для рендеринга, может не быть словарем и должен быть обернут в `dict` перед возвратом, чтобы `TemplateHTMLRenderer` смог его отрендерить. Например:

```python
response.data = {'results': response.data}
```

---

Имя шаблона определяется (в порядке предпочтения):

1. Явный аргумент `template_name`, передаваемый в ответ.
2. Явный атрибут `.template_name`, установленный для этого класса.
3. Результат вызова `view.get_template_names()`.

Пример представления, использующего `TemplateHTMLRenderer`:

```python
class UserDetail(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')
```

Вы можете использовать `TemplateHTMLRenderer` либо для возврата обычных HTML-страниц с помощью DRF, либо для возврата HTML и API ответов с одной конечной точки.

Если вы создаете сайты, использующие `TemplateHTMLRenderer` наряду с другими классами рендереров, вам следует рассмотреть возможность включения `TemplateHTMLRenderer` в качестве первого класса в список `renderer_classes`, чтобы он был приоритетным даже для браузеров, которые посылают плохо сформированные заголовки `ACCEPT:`.

Дополнительные примеры использования `TemplateHTMLRenderer` смотрите в [*HTML & Forms* Topic Page](../topics/html-and-forms.md).

**.media_type**: `text/html`.

**.format**: `'html'`.

**.charset**: `utf-8`

См. также: `StaticHTMLRenderer`

## StaticHTMLRenderer

Простой рендерер, который просто возвращает предварительно отрендеренный HTML. В отличие от других рендереров, данные, передаваемые в объект ответа, должны быть строкой, представляющей возвращаемое содержимое.

Пример представления, использующего `StaticHTMLRenderer`:

```python
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```

Вы можете использовать `StaticHTMLRenderer` либо для возврата обычных HTML-страниц с помощью DRF, либо для возврата HTML- и API-ответов с одной конечной точки.

**.media_type**: `text/html`.

**.format**: `'html'`.

**.charset**: `utf-8`

См. также: `TemplateHTMLRenderer`.

## BrowsableAPIRenderer

Рендерит данные в HTML для Browsable API:

![The BrowsableAPIRenderer](https://github.com/encode/django-rest-framework/raw/master/docs/img/quickstart.png)

Этот рендерер определяет, какой другой рендерер имел бы наивысший приоритет, и использует его для отображения ответа в стиле API на HTML-странице.

**.media_type**: `text/html`.

**.format**: `'api'`.

**.charset**: `utf-8`

**.template**: `'rest_framework/api.html'`.

#### Настройка BrowsableAPIRenderer

По умолчанию содержимое ответа будет отображаться рендерером с наивысшим приоритетом, кроме `BrowsableAPIRenderer`. Если вам нужно настроить это поведение, например, использовать HTML в качестве формата возврата по умолчанию, но использовать JSON в Web-интерфейсе API, вы можете сделать это, переопределив метод `get_default_renderer()`. Например:

```python
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer

Рендерит данные в HTML для отображения в стиле администратора:

![Вид AdminRender](https://github.com/encode/django-rest-framework/raw/master/docs/img/quickstart.png)

Этот рендерер подходит для веб-интерфейсов в стиле CRUD, которые также должны представлять удобный интерфейс для управления данными.

Обратите внимание, что представления, которые имеют вложенные или списковые сериализаторы для своего ввода, не будут хорошо работать с `AdminRenderer`, так как HTML-формы не могут должным образом поддерживать их.

**Примечание**: `AdminRenderer` способен включать ссылки на детальные страницы только в том случае, если в данных присутствует правильно настроенный атрибут `URL_FIELD_NAME` (по умолчанию `url`). Для `HyperlinkedModelSerializer` так и будет, но для классов `ModelSerializer` или простого `Serializer` вам нужно будет убедиться, что поле включено явно. Например, здесь мы используем метод модели `get_absolute_url`:

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Account
```

**.media_type**: `text/html`.

**.format**: `'admin'`.

**.charset**: `utf-8`

**.template**: `'rest_framework/admin.html'`.

## HTMLFormRenderer

Переводит данные, возвращаемые сериализатором, в форму HTML. Вывод этого рендерера не включает заключающие теги `<form>`, скрытый CSRF-вход или какие-либо кнопки отправки.

Этот рендерер не предназначен для прямого использования, но может быть использован в шаблонах путем передачи экземпляра сериализатора в тег шаблона `render_form`.

```html
{% load rest_framework %}

<form action="/submit-report/" method="post">
    {% csrf_token %}
    {% render_form serializer %}
    <input type="submit" value="Save" />
</form>
```

Для получения дополнительной информации смотрите документацию [HTML & Forms](../topics/html-and-forms.md).

**.media_type**: `text/html`.

**.format**: `'format'`.

**.charset**: `utf-8`

**.template**: `'rest_framework/horizontal/form.html'`.

## MultiPartRenderer

Этот рендерер используется для рендеринга данных многочастной формы HTML. **Он не подходит для рендеринга ответов**, а используется для создания тестовых запросов, используя [тестовый клиент и фабрику тестовых запросов](testing.md) DRF.

**.media_type**: `multipart/form-data; border=BoUnDaRyStRiNg`.

**.format**: `'multipart'`.

**.charset**: `utf-8`

---

# Пользовательские рендеры

Для реализации пользовательского рендерера необходимо отнаследоваться от `BaseRenderer`, установить свойства `.media_type` и `.format` и реализовать метод `.render(self, data, accepted_media_type=None, renderer_context=None)`.

Метод должен возвращать строку байт, которая будет использоваться в качестве тела ответа HTTP.

Аргументы, передаваемые методу `.render()`, следующие:

### `data`

Данные запроса, заданные инстанцией `Response()`.

### `accepted_media_type=None`

Дополнительно. Если указано, то это принятый тип носителя, определенный на этапе согласования содержимого.

В зависимости от заголовка `Accept:` клиента, он может быть более конкретным, чем атрибут `media_type` рендерера, и может включать параметры типа медиа. Например, `'application/json; nested=true'`.

### `renderer_context=None`

Опционально. Если предоставляется, то это словарь контекстной информации, предоставляемой представлением.

По умолчанию сюда входят следующие ключи: `view`, `request`, `response`, `args`, `kwargs`.

## Пример

Ниже приведен пример рендеринга обычного текста, который вернет ответ с параметром `data` в качестве содержимого ответа.

```python
from django.utils.encoding import smart_str
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)
```

## Установка набора символов

По умолчанию предполагается, что классы рендеринга используют кодировку `UTF-8`. Чтобы использовать другую кодировку, установите атрибут `charset` для рендерера.

```python
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

Обратите внимание, что если класс рендерера возвращает строку unicode, то содержимое ответа будет преобразовано в строку байт классом `Response`, при этом атрибут `charset`, установленный на рендерере, будет использоваться для определения кодировки.

Если рендерер возвращает строку байт, представляющую необработанное двоичное содержимое, вам следует установить значение charset равное `None`, что обеспечит отсутствие в заголовке `Content-Type` ответа значения `charset`.

В некоторых случаях вы также можете установить атрибут `render_style` на `'binary'`. Это также гарантирует, что Web-интерфейс API не будет пытаться отобразить двоичное содержимое в виде строки.

```python
class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
```

---

# Расширенное использование рендеринга

Вы можете делать довольно гибкие вещи, используя рендереры DRF. Некоторые примеры...

* Предоставление плоских или вложенных представлений из одной и той же конечной точки, в зависимости от запрашиваемого типа носителя.
* Предоставлять как обычные веб-страницы HTML, так и ответы API на основе JSON с одной и той же конечной точки.
* Указывать несколько типов представления HTML для использования клиентами API.
* Недоопределять медиатип рендерера, например, используя `media_type = 'image/*'`, и использовать заголовок `Accept` для изменения кодировки ответа.

## Различное поведение в зависимости от типа носителя

В некоторых случаях вы можете захотеть, чтобы ваше представление использовало различные стили сериализации в зависимости от принятого типа носителя. Если вам нужно сделать это, вы можете обратиться к `request.accepted_renderer`, чтобы определить согласованный рендерер, который будет использоваться для ответа.

Например:

```python
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def list_users(request):
    """
    A view that can return JSON or HTML representations
    of the users in the system.
    """
    queryset = Users.objects.filter(active=True)

    if request.accepted_renderer.format == 'html':
        # TemplateHTMLRenderer takes a context dict,
        # and additionally requires a 'template_name'.
        # It does not require serialization.
        data = {'users': queryset}
        return Response(data, template_name='list_users.html')

    # JSONRenderer requires serialized data as normal.
    serializer = UserSerializer(instance=queryset)
    data = serializer.data
    return Response(data)
```

## Недоопределение типа носителя.

В некоторых случаях вы можете захотеть, чтобы рендерер обслуживал различные типы медиа. В этом случае вы можете не указывать типы медиа, на которые он должен реагировать, используя значение `media_type`, такое как `image/*`, или `*/*`.

Если вы недоопределили медиатип рендерера, вы должны убедиться, что указали медиатип явно, когда возвращаете ответ, используя атрибут `content_type`. Например:

```python
return Response(data, content_type='image/png')
```

## Проектирование типов носителей

Для целей многих Web API может быть достаточно простых ответов `JSON` с гиперссылками на отношения. Если вы хотите полностью внедрить RESTful дизайн и [HATEOAS](http://timelessrepo.com/haters-gonna-hateoas), вам необходимо более детально продумать дизайн и использование типов медиа.

По словам [Роя Филдинга](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven), "REST API должен потратить почти все свои усилия по описанию на определение типа(ов) медиа, используемых для представления ресурсов и управления состоянием приложения, или на определение расширенных имен отношений и/или гипертекстовой разметки для существующих стандартных типов медиа".

Хорошими примерами пользовательских типов медиа являются использование GitHub пользовательского типа медиа [application/vnd.github+json](https://developer.github.com/v3/media/) и одобренная IANA гипермедиа на основе JSON [application/vnd.collection+json](http://www.amundsen.com/media-types/collection/) Майка Амундсена.

## HTML представления ошибок

Обычно рендерер ведет себя одинаково независимо от того, имеет ли он дело с обычным ответом или с ответом, вызванным возникшим исключением, например, исключением `Http404` или `PermissionDenied`, или подклассом `APIException`.

Если вы используете `TemplateHTMLRenderer` или `StaticHTMLRenderer` и при этом возникает исключение, поведение немного отличается и является зеркальным отражением [Django's default handling of error views](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views).

Исключения, возникающие и обрабатываемые средством рендеринга HTML, будут пытаться отобразить с помощью одного из следующих методов, в порядке старшинства.

* Загрузите и отобразите шаблон с именем `{status_code}.html`.
* Загрузите и отобразите шаблон с именем `api_exception.html`.
* Вывести код статуса HTTP и текст, например, "404 Not Found".

Шаблоны будут отображаться с `RequestContext`, который включает ключи `status_code` и `details`.

**Примечание**: Если `DEBUG=True`, то вместо отображения кода статуса HTTP и текста будет отображаться стандартная страница ошибки трассировки Django.

---

# Пакеты сторонних производителей

Также доступны следующие пакеты сторонних производителей.

## YAML

[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/) обеспечивает поддержку разбора и рендеринга [YAML](http://www.yaml.org/). Ранее он был включен непосредственно в пакет DRF, но теперь поддерживается как сторонний пакет.

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

[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/) предоставляет простой неформальный формат XML. Ранее он был включен непосредственно в пакет DRF, но теперь поддерживается как сторонний пакет.

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

## JSONP

[REST framework JSONP](https://jpadilla.github.io/django-rest-framework-jsonp/) обеспечивает поддержку рендеринга JSONP. Ранее он был включен непосредственно в пакет DRF, но теперь поддерживается как сторонний пакет.

---

**Предупреждение**: Если вам требуются междоменные AJAX-запросы, вам следует использовать более современный подход [CORS](https://www.w3.org/TR/cors/) в качестве альтернативы `JSONP`. Более подробную информацию смотрите в документации [CORS](https://www.django-rest-framework.org/topics/ajax-csrf-cors/).

Подход `jsonp` по сути является хаком для браузера и подходит [только для глобально читаемых конечных точек API](https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use), где запросы `GET` являются неаутентифицированными и не требуют никаких разрешений пользователя.

---

#### Установка и настройка

Установите с помощью pip.

```bash
$ pip install djangorestframework-jsonp
```

Измените настройки DRF.

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ],
}
```

## MessagePack

[MessagePack](https://msgpack.org/) - это быстрый и эффективный формат двоичной сериализации. [Juan Riaza](https://github.com/juanriaza) поддерживает пакет [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack), который обеспечивает поддержку рендеринга и парсера MessagePack для DRF.

## Microsoft Excel: XLSX (Двоичные конечные точки электронных таблиц)

XLSX - это самый популярный в мире формат двоичных электронных таблиц. [Тим Аллен](https://github.com/flipperpa) из [The Wharton School](https://github.com/wharton) поддерживает [drf-excel](https://github.com/wharton/drf-excel), который отображает конечную точку в виде электронной таблицы XLSX с помощью OpenPyXL и позволяет клиенту загрузить ее. Электронные таблицы могут быть стилизованы для каждого вида.

#### Установка и настройка

Установите с помощью pip.

```bash
$ pip install drf-excel
```

Измените настройки DRF.

```python
REST_FRAMEWORK = {
    ...

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'drf_excel.renderers.XLSXRenderer',
    ],
}
```

Чтобы избежать потоковой передачи файла без имени (при этом браузер часто принимает по умолчанию имя файла "download" без расширения), нам необходимо использовать миксин для переопределения заголовка `Content-Disposition`. Если имя файла не указано, то по умолчанию будет задано `export.xlsx`. Например:

```python
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from .models import MyExampleModel
from .serializers import MyExampleSerializer

class MyExampleViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = MyExampleModel.objects.all()
    serializer_class = MyExampleSerializer
    renderer_classes = [XLSXRenderer]
    filename = 'my_export.xlsx'
```

## CSV

Значения, разделенные запятыми, - это формат табличных данных в виде обычного текста, который легко импортируется в приложения электронных таблиц. [Mjumbe Poe](https://github.com/mjumbewu) поддерживает пакет [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv), который обеспечивает поддержку CSV-рендеринга для DRF.

## UltraJSON

[UltraJSON](https://github.com/esnme/ultrajson) - это оптимизированный кодировщик JSON на языке C, который может значительно ускорить рендеринг JSON. [Adam Mertz](https://github.com/Amertz08) поддерживает [drf_ujson2](https://github.com/Amertz08/drf_ujson2), форк ныне не поддерживаемого [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer), который реализует рендеринг JSON с использованием пакета UJSON.

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет рендереры и парсеры JSON в верблюжьем регистре для DRF. Это позволяет сериализаторам использовать имена полей в стиле Python с подчеркиванием, но отображать их в API как имена полей в верблюжьем регистре в стиле Javascript. Поддерживается [Виталием Бабием](https://github.com/vbabiy).

## Pandas (CSV, Excel, PNG)

[Django REST Pandas](https://github.com/wq/django-rest-pandas) предоставляет сериализатор и рендереры, которые поддерживают дополнительную обработку и вывод данных через [Pandas](https://pandas.pydata.org/) DataFrame API. Django REST Pandas включает рендереры для файлов CSV в стиле Pandas, рабочих книг Excel (как `.xls`, так и `.xlsx`) и ряда [других форматов](https://github.com/wq/django-rest-pandas#supported-formats). Он поддерживается [S. Andrew Sheppard](https://github.com/sheppard) в рамках проекта [wq Project](https://github.com/wq).

## LaTeX

[Rest Framework Latex](https://github.com/mypebble/rest-framework-latex) предоставляет рендерер, который выводит PDF-файлы с использованием Lualatex. Он поддерживается [Pebble (S/F Software)](https://github.com/mypebble).
