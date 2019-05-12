# Рендереры

Перед тем как экземпляр `TemplateResponse` будет возвращен клиенту, он должен быть срендерен. В процессе рендеринга шаблон и контекст превращаются в байтовый поток, который отправляется клиенту.

— документация Django

REST framework включает несколько встроенных классов рендера, которые позволяют возвращать ответы с различными типами медиа. Также есть возможность определить ваш собственный рендер для гибкой настройки ваших собственных типов медиа.

## Как определяется рендер
 
Набор валдиных рендеров представления всегда имеет вид списка классов. REST framework определяет наиболее подходящий рендер для запроса, анализирует заголовок `Accept` запроса для того, чтобы выяснить какой тип медиа ожидается в ответе.

Вы также можете использовать форматирующий суффикс с URL, чтобы добиться желаемого отображения. Например URL  http://example.com/api/users_count.json на конечной точке всегда будет возвращать данные JSON.

Для дополнительной информации см документацию по согласованию [содержимого контента](http://www.django-rest-framework.org/api-guide/content-negotiation/)

## Настройка рендеров

Стандартный набор рендеров можно установить глобально с помощью настройки `DEFAULT_RENDERER_CLASSES`. Например, следующие настройки будут использовать JSON в качестве главного типа медиа, а также будут включать самоописываемый API.

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
```

Помимо этого вы можете устанавливать рендеры для конкретных представлений или наборов представлений, используя представления-классы `APIView`.

```python
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
```

Или, если вы используете декоратор  `@api_view` с представлениями-функциями.

```python
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def user_count_view(request, format=None):
    """
    A view that returns the count of active users in JSON.
    """
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
```

## Сортировка классов рендера

При указании классов рендера для вашего API важно подумать о приоритете для каждого типа медиа. Если клиент не уточняет нужное ему представление, указав в заголовке `Accept: */*`  или вовсе не указав заголовка `Accept`, тогда  для ответа REST framework выберет первый рендер в списке.

Например, если ваш API обслуживает JSON ответы и webbrowsable API, то по умолчанию лучше указать `JSONRenderer`, для того, чтобы присылать JSON ответы клиентам, которые не указали заголовок `Accept`.

Если ваш API включает представления, которые обслуживает как обычные вебстраницы, так и API ответы, в зависимости от запросов, то тогда имеет смысл указать `TemplateHTMLRenderer` в качестве рендера по умочанию, для нормальной работы со старыми бразуерами, которые присылают [битые заголовки](https://www.newmediacampaigns.com/blog/browser-rest-http-accept-headers).

# Обращение к API
## JSONRenderer

Рендерит данные запроса в формате JSON, используя кодировку utf-8.

Обратите внимание, что стиль по умолчанию включает символы unicode и рендерит ответ, используя сжатый стиль, без лишних пробелов:
```python
{"unicode black star":"★","value":999}
```

Дополнительно клиент может включать параметр `'indent'` медиа типов, в этом случае возвращаемый JSON будет с отступами.

Например `Accept: application/json; indent=4.`

```python
{
    "unicode black star": "★",
    "value": 999
}
```

Стандартный стиль кодировки JSON можно изменит с помощью настроек `UNICODE_JSON` и `COMPACT_JSON`.

**.media_type:** `application/json`

**.format:** `'.json'`

**.charset:** `None`

## TemplateHTMLRenderer

Рендерит данные в HTML, используя стандартный генератор шаблонов Джанго. В отличие от других рендеров, данные, переданные в Response не требуют сериализации. Также, в отличие от других рендеров, вам может понадобиться указать аргумент `template_name` при создании `Response`.

TemplateHTMLRenderer создает `RequestContext`, используя `response.data` в качестве словаря контекста и определяет имя шаблона , который используется для рендера контекста.

Имя шаблона определяется следующим (в порядке предпочтения):
1. явная передача аргумента `template_name` в ответе.
2. явная передача `.template_name `указанного в данном классе.
3. возвращает результат вызова `view.get_template_names()`

Пример представления с использованием `TemplateHTMLRenderer`:

```python
class UserDetail(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    queryset = User.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')
```

Вы можете использовать  `TemplateHTMLRenderer` либо для того чтобы возвращать обычные HTML страницы с использованием REST framework, или для того чтобы возвращать как HTML, так и API ответы из одной конечной точки.

Если вы конструируете веб страницы, которые используют `TemplateHTMLRenderer` наравне с другими классами рендеров, то вы должны разместить `TemplateHTMLRenderer` на первое месо в списке `renderer_classes`, таким образом он будет иметь главный приоритет даже для браузеров, которые некорректно формируют заговлоки `ACCEPT:`.

**.media_type**: `text/html`

**.format:** `'.html'`

**.charset:** `utf-8`

## StaticHTMLRenderer

Простой рендер, который возвращает пре-рендеренный HTML. В отличие от других рендеров, данные, переданные объекту ответа должны представлять собой строку возвращаемого контента.

Пример представления, которое исопользует `StaticHTMLRenderer`:

```python
api_view(('GET',))
@renderer_classes((StaticHTMLRenderer,))
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```
Вы можете использовать  `StaticHTMLRenderer` либо для того чтобы возвращать обычные HTML страницы с использованием REST framework, или для того чтобы возвращать как HTML, так и API ответы из одной конечной точки.

**.media_type**: `text/html`

**.format:** `'.html'`

**.charset:** `utf-8`

## BrowsableAPIRenderer

Рендерит данные в HTML для Browsable API:

![BrowsableAPIRenderer](img/quickstart.png)

Данный рендер определяет какой иной рендер получит главный приоритет и использует его для отображения ответа API на HTML странице.

**.media_type:** `text/html`

**.format:** `'.api'`

**.charset:** `utf-8`

**.template:** `'rest_framework/api.html'`

## Кастомизация BrowsableAPIRenderer

По умолчанию контент ответа будет генерироваться с помощью рендера с самым высоким приоритетом, за исключением `BrowsableAPIRenderer`. Если вам нужно кастомизировать это поведение, например указать HTML как возвращаемый формат по умолчнию, но при этом использовать JSON в browsable API, вы можете переписть метод ` get_default_renderer()`. Например:

```python
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer

Рендерит данные в HTML для отображения админки:

![AdminRenderer](img/admin.png)

Этот рендер подходи для веб API в стиле CRUD, которые должны иметь простой и понятный интерфейс пользователя для управления данными. 

Обратите внимание, что представления, которые были вложены или список сериализаторов ну будут работать корректно с `AdminRenderer` так как HTML формы не поддерживают их.

Замечание: `AdminRenderer` может только включать ссылки на страницы с единственной точкой входа, при наличии правильно настроенного атрибута URL_FIELD_NAME(url по умолчанию) в данных. Это верно для `HyperlinkedModelSerializer`, но для классов
`ModelSerializer` или простых классов `Serializer` вы должны явно включить поле. Например здесь мы используем метод модели 
`get_absolute_url`:

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Account
```

**.media_type**: `text/html`

**.format**: `'.admin'`

**.charset**: `utf-8`

**.template**: `'rest_framework/admin.html'`

## HTMLFormRenderer

Данные рендера вовзвращаются сериализатором в форме HTML. Результат этого рендера не включает теги ё, скрытое поле CSRF или кнопки submit. 
Этот рендер не предназначен для прямого использования, но может быть задействован в шаблонах путем передачи экземпляра сериализатора в тег шаблога `render_form`.

```python
{% load rest_framework %}

<form action="/submit-report/" method="post">
    {% csrf_token %}
    {% render_form serializer %}
    <input type="submit" value="Save" />
</form>
```

**.media_type**: `text/html`

**.format**: `'.form'`

**.charset**: `utf-8`

**.template**: `'rest_framework/horizontal/form.html'`

## MultiPartRenderer

Этот рендер используется для рендера многокомпонентных данных форм HTML. Он не подходит для рендера ответа, но используется для создания тестовых запросов с помощью инструментов для теста REST framework.

**.media_type**: `multipart/form-data; boundary=BoUnDaRyStRiNg`

**.format**: `'.multipart'`

**.charset**: `utf-8`

# Кастомные рендеры

Для того, чтобы применить кастомный рендер, вы должны переписать `BaseRenderer`, установить свойства `.media_type` и `.format`, а также применить метод `.render(self, data, media_type=None, renderer_context=None)`.

Этот метод должен вернуть байтовую строку, которая будет использоваться как тело HTTP ответа.

 `.render()` передаются следующие аргументы:

`data`

Данные запроса, как установлено при инициализации `Response()` 

```python
media_type=None
```

Опционально. Если указано, обозначает приемлемый тип медиа, согласно тому, как он определяется на стадии согласования содержимого контента.

В зависимости от клиентского заголовка `Accept:` помимо атрибута `media_type` рендера могут также указываться параметры типов меда. Например `"application/json; nested=true"`.

```python
renderer_context=None
```

Опционально. Если указано, то принимает вид словаря с контекстной информацией из представления.

По умолчнию включает следующие ключи: `view`, `request`, `response`, `args`, `kwargs`.

## Пример

Ниже следует пример plaintext рендера, который возвращает ответ с параметрамми данных в виде контекста ответа.

```python
from django.utils.encoding import smart_unicode
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

## Установка кодировки

По умолчанию классы рендеров используют кодировку UTF-8. Для того, чтобы воспользоваться другой кодировкой, укажите атрибут `charset`.

```python
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

Обратите внимание, что если класс рендера возвращает строку unicode, то контент ответа будет приводится к виду байтовой строки с помощью Response class, при этом атрибут `charset` будет указан в рендере, который и будет определять кодировку.

Если рендер возвращает байтовую строку, представляющую неформатированный бинарный контент, вам следует указать `None` в значении `charset`. Тем самым вы добьетесь того что заголовок` Content-Type` ответа не будет иметь значение `charset`.

В некоторых случаях вам потребуется установить атрибут `'binary'` в `render_style`. Таким образом вы тоже удостоверитесь, что browsable API не будет предпринимать попыток отобразить бинарный контент в качестве строки.

```python
class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data
```

# Использование продвинутых рендеров

С помощью рендеров REST framework можно производить тонкую настройку. Например...
* Предоставлять flat или nested представления с одной и той же конченой точки, в зависимости от запрашиваемого типа медиа.
* Работать как с обычными HTML страницами, так и с API на основе JSON с одних и тех же конечных точек.
* Устанавливать множество типов представления HTML для клиента API.
* Для того, чтобы изменять кодировку запроса можно опустить медиа тип рендера, например `media_type = 'image/*'` и использовать заголовок `Accept`.

## Изменение поведения в зависимости от типа медиа

В некоторых случаях нужно, чтобы в представлении использовались разные стили сериализации, в зависимости от принимаемого типа медиа. Для этого можно обратиться к `request.accepted_renderer` и определить рендер, который будет использоваться для запроса.

Например:
``` python
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def list_users(request):
    """
    view, которое может возвращать JSON или HTML 
    представление пользователей в системе

    """
    queryset = Users.objects.filter(active=True)

    if request.accepted_renderer.format == 'html':
        # TemplateHTMLRenderer принимает контекстный словарь,
        # и дополнительно требует 'template_name'.
        # Сериализация не требуется.
        data = {'users': queryset}
        return Response(data, template_name='list_users.html')

    # JSONRenderer требует сериализированные данные.
    serializer = UserSerializer(instance=queryset)
    data = serializer.data
    return Response(data)
```

## Опущение  типов медиа

В некоторых случаях требуется, чтобы рендер обрабатывал некоторое число типов медиа. В этом случае можно опустить типы, на которые он будет реагировать, используя подобные значения `image/*` или ` */*` в `media_type`. Если вы опустили медиа тип рендера, то должны удостовериться, что прописали его явно при возвращении ответа, используя атрибут `content_type`. к примеру: 

```python
return Response(data, content_type='image/png')
```

## Проектирование собственных типов медиа

Для многих веб API достаточно лишь JSON отвтетов с гиперссылочными связями. Если вы хотите в полной мере овладеть принципом RESTful и HATEOAS, то вам придется детальнее изучить структуру и использование медиа данных.

Как сказал Рой Филдинг: «почти все свои силы REST API тратит на определение типов мультимедиа, используемых для представления ресурсов и управления состоянием приложения, или для определения расширенных имен отношений и / или гипертекстовой разметки для существующих стандартных типов медиа.».

Для хороших примеро кастомных типов медиа посмотрите как GitHub используется кастомные типы [`application/vnd.github+json`](https://developer.github.com/v3/media/) и [JSON приложение Майкла Амундсена](http://www.amundsen.com/media-types/collection/)

## Представления с HTML ошибками

Как правило рендер будет действовать одинаково, независимо от того сталкивается ли он с обычнм ответом, или с ответом, вызванным исключением, таким как `Http404` или `PermissionDenied` подкласса `APIException`.

Если вы используете TemplateHTMLRenderer либо StaticHTMLRenderer и словили исключение, то поведение будет немного отличаться и повторять стандартную обработку ошибок представления Джанго.

Исключения, которые вызывает и обрабатывает HTML рендер будут рендериться с помощью одного из следующиз рендеров, отсортированных ниже в порядке предпочтение.
* Загрузка и рендеринг шаблона под именем {status_code}.html.
* Загрузка и рендеринг шаблона под именем api_exception.html.
* Рендеринг кода состояния HTTP и текста, например "404 Not Found".

Шаблоны будут рендериться с помощью `RequestContext`, в который входят ключи со status_code и подробностями.

Заметка: если `DEBUG=True`, то будет отображаться стандатная страница ошибок Джанго вместо рендеринга кода состояния HTTP и текста.

# Сторонние пакеты

Доступны следующие сторонние пакеты.

## YAML

[REST framework YAML](http://jpadilla.github.io/django-rest-framework-yaml/)поддерживает YAML парсинг и рендеринг. Раньше он был установлен в REST framework по умолчанию, а теперь доступен в качестве стороннего пакета.

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

[REST Framework XML](http://jpadilla.github.io/django-rest-framework-xml/) поддерживает неформальный формат XML. Раньше он был установлен в REST framework по умолчанию, а теперь доступен в качестве стороннего пакета.

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

##JSONP

[REST framework JSONP](http://jpadilla.github.io/django-rest-framework-jsonp/) предоставляет поддержку JSONP рендеринга. Раньше он был установлен в REST framework по умолчанию, а теперь доступен в качестве стороннего пакета.

**Внимание**: если вам нужны междоменные AJAX запросы, то в качестве альтернативы JSONP вы должны использовать более современный подход CORS. См документацию по [CORS](https://www.w3.org/TR/cors/) для подробностей.

По сути `jsonp` это такой hack браузера, и он подходит лишь для глобальных читаемых конечных точек API, когда запросы GET недостоврены и не требуют права доступа от пользователя. 

### Установка и настройка

Установка с помощью pip

```python

$ pip install djangorestframework-jsonp
```

Изменение настроек REST framework

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ),
}

```

## MessagePack

[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack) это быстрый и эффектиный бинарный формат сериализации. Предоставляет рендер и парсер для REST framework.

## CSV

CSV формат текстового файла, в котором значения данных разделены запятыми, может легко быить импортироват в приложения с электронными таблицами. Пакет [djangorestframework-csv ](https://github.com/mjumbewu/django-rest-framework-csv)предоставляет поддрежку CSV для REST framework.

## UltraJSON

UltraJSON это оптимизрованый кодировщик  C JSON, который обеспечивает более быстрый рендеринг JSON. Пакет [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer) включает рендеринг JSON с использованием UJSON.

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет camel case рендеры и парсеры для JSON. Это позволит сериализаторам использовать имена полей в подчеркнутом стиле Питона, но при поля будут доступны в API в стиле camel case Javascript.

## Pandas (CSV, Excel, PNG)

[Django REST Pandas](https://github.com/wq/django-rest-pandas) предоставляет сериализаторы и рендеры, которые поддреживаеют дополнительную обработку данных с помощью [Pandas DataFrame API](http://pandas.pydata.org/). Django REST Pandas включает рендеры для файлов CSV в формате Pandas, форматов Excel (.xls и .xlsx), а также ряд других форматов.

## LaTeX

[Rest Framework Latex](https://github.com/mypebble/rest-framework-latex) предоставляет рендер, который на выходе отдает PDF с использованием Laulatex.
