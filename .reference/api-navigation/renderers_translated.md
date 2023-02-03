<!-- TRANSLATED by md-translate -->
---

source:

источник:

* renderers.py

* renderers.py

---

# Renderers

# Рендереры

> Before a TemplateResponse instance can be returned to the client, it must be rendered. The rendering process takes the intermediate representation of template and context, and turns it into the final byte stream that can be served to the client.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process)

> Прежде чем экземпляр TemplateResponse будет возвращен клиенту, он должен быть отрисован. Процесс рендеринга принимает промежуточное представление шаблона и контекста и превращает его в конечный поток байтов, который может быть передан клиенту.
>
> - [Django documentation](https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process)

REST framework includes a number of built in Renderer classes, that allow you to return responses with various media types. There is also support for defining your own custom renderers, which gives you the flexibility to design your own media types.

Фреймворк REST включает ряд встроенных классов Renderer, которые позволяют возвращать ответы с различными типами медиа. Также имеется поддержка определения собственных пользовательских рендереров, что дает вам гибкость в разработке собственных типов медиа.

## How the renderer is determined

## Как определяется рендерер

The set of valid renderers for a view is always defined as a list of classes. When a view is entered REST framework will perform content negotiation on the incoming request, and determine the most appropriate renderer to satisfy the request.

Набор допустимых рендерингов для представления всегда определяется как список классов. При входе в представление фреймворк REST будет выполнять согласование содержимого входящего запроса и определять наиболее подходящий рендерер для удовлетворения запроса.

The basic process of content negotiation involves examining the request's `Accept` header, to determine which media types it expects in the response. Optionally, format suffixes on the URL may be used to explicitly request a particular representation. For example the URL `http://example.com/api/users_count.json` might be an endpoint that always returns JSON data.

Основной процесс согласования содержимого включает в себя изучение заголовка `Accept` запроса, чтобы определить, какие типы медиа ожидаются в ответе. По желанию, суффиксы формата в URL могут быть использованы для явного запроса определенного представления. Например, URL `http://example.com/api/users_count.json` может быть конечной точкой, которая всегда возвращает данные в формате JSON.

For more information see the documentation on [content negotiation](content-negotiation.md).

Для получения дополнительной информации смотрите документацию по [content negotiation] (content-negotiation.md).

## Setting the renderers

## Установка рендереров

The default set of renderers may be set globally, using the `DEFAULT_RENDERER_CLASSES` setting. For example, the following settings would use `JSON` as the main media type and also include the self describing API.

Набор рендеров по умолчанию можно задать глобально, используя параметр `DEFAULT_RENDERER_CLASSES`. Например, следующие настройки будут использовать `JSON` в качестве основного типа медиа, а также включать API самоописания.

```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

You can also set the renderers used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить рендереры, используемые для отдельного представления или набора представлений, используя представления на основе класса `APIView`.

```
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

Or, if you're using the `@api_view` decorator with function based views.

Или, если вы используете декоратор `@api_view` с представлениями, основанными на функциях.

```
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

## Ordering of renderer classes

## Упорядочивание классов рендеринга

It's important when specifying the renderer classes for your API to think about what priority you want to assign to each media type. If a client underspecifies the representations it can accept, such as sending an `Accept: */*` header, or not including an `Accept` header at all, then REST framework will select the first renderer in the list to use for the response.

Важно при определении классов рендеринга для вашего API подумать о том, какой приоритет вы хотите присвоить каждому типу медиа. Если клиент недоопределяет представления, которые он может принимать, например, посылает заголовок `Accept: */*` заголовок, или вообще не включает заголовок `Accept`, то REST framework выберет первый рендерер в списке для использования в ответе.

For example if your API serves JSON responses and the HTML browsable API, you might want to make `JSONRenderer` your default renderer, in order to send `JSON` responses to clients that do not specify an `Accept` header.

Например, если ваш API обслуживает JSON-ответы и HTML-просмотр, вы можете сделать `JSONRenderer` рендерером по умолчанию, чтобы отправлять `JSON` ответы клиентам, которые не указывают заголовок `Accept`.

If your API includes views that can serve both regular webpages and API responses depending on the request, then you might consider making `TemplateHTMLRenderer` your default renderer, in order to play nicely with older browsers that send [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers).

Если ваш API включает представления, которые могут обслуживать как обычные веб-страницы, так и ответы API в зависимости от запроса, то вы можете сделать `TemplateHTMLRenderer` рендерером по умолчанию, чтобы хорошо играть со старыми браузерами, которые отправляют [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers).

---

# API Reference

# API Reference

## JSONRenderer

## JSONRenderer

Renders the request data into `JSON`, using utf-8 encoding.

Переводит данные запроса в `JSON`, используя кодировку utf-8.

Note that the default style is to include unicode characters, and render the response using a compact style with no unnecessary whitespace:

Обратите внимание, что стиль по умолчанию включает символы юникода и отображает ответ, используя компактный стиль без лишних пробелов:

```
{"unicode black star":"★","value":999}
```

The client may additionally include an `'indent'` media type parameter, in which case the returned `JSON` will be indented. For example `Accept: application/json; indent=4`.

Клиент может дополнительно включить параметр медиатипа ``отступ``, в этом случае возвращаемый ``JSON`` будет иметь отступ. Например, `Accept: application/json; indent=4`.

```
{
    "unicode black star": "★",
    "value": 999
}
```

The default JSON encoding style can be altered using the `UNICODE_JSON` and `COMPACT_JSON` settings keys.

Стиль кодировки JSON по умолчанию может быть изменен с помощью ключей настроек `UNICODE_JSON` и `COMPACT_JSON`.

**.media_type**: `application/json`

**.media_type**: `application/json`.

**.format**: `'json'`

**.format**: ``json``.

**.charset**: `None`

**.charset**: `None`.

## TemplateHTMLRenderer

## TemplateHTMLRenderer

Renders data to HTML, using Django's standard template rendering. Unlike other renderers, the data passed to the `Response` does not need to be serialized. Also, unlike other renderers, you may want to include a `template_name` argument when creating the `Response`.

Рендерит данные в HTML, используя стандартный шаблонный рендеринг Django. В отличие от других рендерингов, данные, передаваемые в `Response`, не нужно сериализовать. Также, в отличие от других рендереров, вы можете включить аргумент `имя_шаблона` при создании `Response`.

The TemplateHTMLRenderer will create a `RequestContext`, using the `response.data` as the context dict, and determine a template name to use to render the context.

TemplateHTMLRenderer создаст `RequestContext`, используя `response.data` в качестве диктанта контекста, и определит имя шаблона, который будет использоваться для рендеринга контекста.

---

**Note:** When used with a view that makes use of a serializer the `Response` sent for rendering may not be a dictionary and will need to be wrapped in a dict before returning to allow the `TemplateHTMLRenderer` to render it. For example:

**Примечание:** При использовании с представлением, которое использует сериализатор, `Response`, отправленный для рендеринга, может не быть словарем и должен быть обернут в dict перед возвратом, чтобы `TemplateHTMLRenderer` смог его отрендерить. Например:

```
response.data = {'results': response.data}
```

---

The template name is determined by (in order of preference):

Имя шаблона определяется (в порядке предпочтения):

1. An explicit `template_name` argument passed to the response.
2. An explicit `.template_name` attribute set on this class.
3. The return result of calling `view.get_template_names()`.

1. Явный аргумент `имя_шаблона`, передаваемый в ответ.
2. Явный атрибут `.template_name`, установленный для этого класса.
3. Результат вызова `view.get_template_names()`.

An example of a view that uses `TemplateHTMLRenderer`:

Пример представления, использующего `TemplateHTMLRenderer`:

```
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

You can use `TemplateHTMLRenderer` either to return regular HTML pages using REST framework, or to return both HTML and API responses from a single endpoint.

Вы можете использовать `TemplateHTMLRenderer` либо для возврата обычных HTML-страниц с помощью фреймворка REST, либо для возврата HTML и API ответов с одной конечной точки.

If you're building websites that use `TemplateHTMLRenderer` along with other renderer classes, you should consider listing `TemplateHTMLRenderer` as the first class in the `renderer_classes` list, so that it will be prioritised first even for browsers that send poorly formed `ACCEPT:` headers.

Если вы создаете сайты, использующие `TemplateHTMLRenderer` наряду с другими классами рендереров, вам следует рассмотреть возможность включения `TemplateHTMLRenderer` в качестве первого класса в список `renderer_classes`, чтобы он был приоритетным даже для браузеров, которые посылают плохо сформированные заголовки `ACCEPT:`.

See the [*HTML & Forms* Topic Page](../topics/html-and-forms.md) for further examples of `TemplateHTMLRenderer` usage.

Дополнительные примеры использования `TemplateHTMLRenderer` смотрите в [*HTML & Forms* Topic Page](../topics/html-and-forms.md).

**.media_type**: `text/html`

**.media_type**: `text/html`.

**.format**: `'html'`

**.format**: `'html``.

**.charset**: `utf-8`

**.charset**: `utf-8`

See also: `StaticHTMLRenderer`

См. также: `StaticHTMLRenderer`

## StaticHTMLRenderer

## StaticHTMLRenderer

A simple renderer that simply returns pre-rendered HTML. Unlike other renderers, the data passed to the response object should be a string representing the content to be returned.

Простой рендерер, который просто возвращает предварительно отрендеренный HTML. В отличие от других рендереров, данные, передаваемые в объект ответа, должны быть строкой, представляющей возвращаемое содержимое.

An example of a view that uses `StaticHTMLRenderer`:

Пример представления, использующего `StaticHTMLRenderer`:

```
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```

You can use `StaticHTMLRenderer` either to return regular HTML pages using REST framework, or to return both HTML and API responses from a single endpoint.

Вы можете использовать `StaticHTMLRenderer` либо для возврата обычных HTML-страниц с помощью фреймворка REST, либо для возврата HTML- и API-ответов с одной конечной точки.

**.media_type**: `text/html`

**.media_type**: `text/html`.

**.format**: `'html'`

**.format**: `'html``.

**.charset**: `utf-8`

**.charset**: `utf-8`

See also: `TemplateHTMLRenderer`

См. также: `TemplateHTMLRenderer`.

## BrowsableAPIRenderer

## BrowsableAPIRenderer

Renders data into HTML for the Browsable API:

Рендерит данные в HTML для Browsable API:

![The BrowsableAPIRenderer](../img/quickstart.png)

![The BrowsableAPIRenderer](../img/quickstart.png)

This renderer will determine which other renderer would have been given highest priority, and use that to display an API style response within the HTML page.

Этот рендерер определяет, какой другой рендерер имел бы наивысший приоритет, и использует его для отображения ответа в стиле API на HTML-странице.

**.media_type**: `text/html`

**.media_type**: `text/html`.

**.format**: `'api'`

**.format**: `'api``.

**.charset**: `utf-8`

**.charset**: `utf-8`

**.template**: `'rest_framework/api.html'`

**.template**: `'rest_framework/api.html'`.

#### Customizing BrowsableAPIRenderer

#### Настройка BrowsableAPIRenderer

By default the response content will be rendered with the highest priority renderer apart from `BrowsableAPIRenderer`. If you need to customize this behavior, for example to use HTML as the default return format, but use JSON in the browsable API, you can do so by overriding the `get_default_renderer()` method. For example:

По умолчанию содержимое ответа будет отображаться рендерером с наивысшим приоритетом, кроме `BrowsableAPIRenderer`. Если вам нужно настроить это поведение, например, использовать HTML в качестве формата возврата по умолчанию, но использовать JSON в просматриваемом API, вы можете сделать это, переопределив метод `get_default_renderer()`. Например:

```
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer

## AdminRenderer

Renders data into HTML for an admin-like display:

Рендерит данные в HTML для отображения в стиле администратора:

![The AdminRender view](../img/admin.png)

![Вид AdminRender](../img/admin.png)

This renderer is suitable for CRUD-style web APIs that should also present a user-friendly interface for managing the data.

Этот рендерер подходит для веб-интерфейсов в стиле CRUD, которые также должны представлять удобный интерфейс для управления данными.

Note that views that have nested or list serializers for their input won't work well with the `AdminRenderer`, as the HTML forms are unable to properly support them.

Обратите внимание, что представления, которые имеют вложенные или списковые сериализаторы для своего ввода, не будут хорошо работать с `AdminRenderer`, так как HTML-формы не могут должным образом поддерживать их.

**Note**: The `AdminRenderer` is only able to include links to detail pages when a properly configured `URL_FIELD_NAME` (`url` by default) attribute is present in the data. For `HyperlinkedModelSerializer` this will be the case, but for `ModelSerializer` or plain `Serializer` classes you'll need to make sure to include the field explicitly. For example here we use models `get_absolute_url` method:

**Примечание**: `AdminRenderer` способен включать ссылки на детальные страницы только в том случае, если в данных присутствует правильно настроенный атрибут `URL_FIELD_NAME` (по умолчанию `url`). Для `HyperlinkedModelSerializer` так и будет, но для классов `ModelSerializer` или простого `Serializer` вам нужно будет убедиться, что поле включено явно. Например, здесь мы используем метод модели `get_absolute_url`:

```
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Account
```

**.media_type**: `text/html`

**.media_type**: `text/html`.

**.format**: `'admin'`

**.format**: `'admin``.

**.charset**: `utf-8`

**.charset**: `utf-8`

**.template**: `'rest_framework/admin.html'`

**.template**: `'rest_framework/admin.html'`.

## HTMLFormRenderer

## HTMLFormRenderer

Renders data returned by a serializer into an HTML form. The output of this renderer does not include the enclosing `<form>` tags, a hidden CSRF input or any submit buttons.

Переводит данные, возвращаемые сериализатором, в форму HTML. Вывод этого рендерера не включает заключающие теги `<form>`, скрытый CSRF-вход или какие-либо кнопки отправки.

This renderer is not intended to be used directly, but can instead be used in templates by passing a serializer instance to the `render_form` template tag.

Этот рендерер не предназначен для прямого использования, но может быть использован в шаблонах путем передачи экземпляра сериализатора в тег шаблона `render_form`.

```
{% load rest_framework %}

<form action="/submit-report/" method="post">
    {% csrf_token %}
    {% render_form serializer %}
    <input type="submit" value="Save" />
</form>
```

For more information see the [HTML & Forms](../topics/html-and-forms.md) documentation.

Для получения дополнительной информации смотрите документацию [HTML & Forms](../topics/html-and-forms.md).

**.media_type**: `text/html`

**.media_type**: `text/html`.

**.format**: `'form'`

**.format**: ``формат``.

**.charset**: `utf-8`

**.charset**: `utf-8`

**.template**: `'rest_framework/horizontal/form.html'`

**.template**: `'rest_framework/horizontal/form.html'`.

## MultiPartRenderer

## MultiPartRenderer

This renderer is used for rendering HTML multipart form data. **It is not suitable as a response renderer**, but is instead used for creating test requests, using REST framework's [test client and test request factory](testing.md).

Этот рендерер используется для рендеринга данных многочастной формы HTML. **Он не подходит для рендеринга ответов**, а используется для создания тестовых запросов, используя [тестовый клиент и фабрику тестовых запросов] (testing.md) фреймворка REST.

**.media_type**: `multipart/form-data; boundary=BoUnDaRyStRiNg`

**.media_type**: `multipart/form-data; border=BoUnDaRyStRiNg`.

**.format**: `'multipart'`

**.format**: ``многосторонний``.

**.charset**: `utf-8`

**.charset**: `utf-8`

---

# Custom renderers

# Пользовательские рендеры

To implement a custom renderer, you should override `BaseRenderer`, set the `.media_type` and `.format` properties, and implement the `.render(self, data, accepted_media_type=None, renderer_context=None)` method.

Для реализации пользовательского рендерера необходимо переопределить `BaseRenderer`, установить свойства `.media_type` и `.format` и реализовать метод `.render(self, data, accepted_media_type=None, renderer_context=None)`.

The method should return a bytestring, which will be used as the body of the HTTP response.

Метод должен возвращать байтстринг, который будет использоваться в качестве тела ответа HTTP.

The arguments passed to the `.render()` method are:

Аргументы, передаваемые методу `.render()`, следующие:

### `data`

### `data`

The request data, as set by the `Response()` instantiation.

Данные запроса, заданные инстанцией `Response()`.

### `accepted_media_type=None`

### `accepted_media_type=None`

Optional. If provided, this is the accepted media type, as determined by the content negotiation stage.

Дополнительно. Если указано, то это принятый тип носителя, определенный на этапе согласования содержимого.

Depending on the client's `Accept:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters. For example `"application/json; nested=true"`.

В зависимости от заголовка `Accept:` клиента, он может быть более конкретным, чем атрибут `media_type` рендерера, и может включать параметры типа медиа. Например, `"application/json; nested=true"`.

### `renderer_context=None`

### `renderer_context=None`

Optional. If provided, this is a dictionary of contextual information provided by the view.

Дополнительно. Если предоставляется, то это словарь контекстной информации, предоставляемой представлением.

By default this will include the following keys: `view`, `request`, `response`, `args`, `kwargs`.

По умолчанию сюда входят следующие ключи: `view`, `request`, `response`, `args`, `kwargs`.

## Example

## Пример

The following is an example plaintext renderer that will return a response with the `data` parameter as the content of the response.

Ниже приведен пример рендеринга обычного текста, который вернет ответ с параметром `data` в качестве содержимого ответа.

```
from django.utils.encoding import smart_text
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
```

## Setting the character set

## Установка набора символов

By default renderer classes are assumed to be using the `UTF-8` encoding. To use a different encoding, set the `charset` attribute on the renderer.

По умолчанию предполагается, что классы рендеринга используют кодировку `UTF-8`. Чтобы использовать другую кодировку, установите атрибут `charset` для рендерера.

```
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

Note that if a renderer class returns a unicode string, then the response content will be coerced into a bytestring by the `Response` class, with the `charset` attribute set on the renderer used to determine the encoding.

Обратите внимание, что если класс рендерера возвращает строку unicode, то содержимое ответа будет преобразовано в байтстринг классом `Response`, при этом атрибут `charset`, установленный на рендерере, будет использоваться для определения кодировки.

If the renderer returns a bytestring representing raw binary content, you should set a charset value of `None`, which will ensure the `Content-Type` header of the response will not have a `charset` value set.

Если рендерер возвращает байтстринг, представляющий необработанное двоичное содержимое, вам следует установить значение charset равное `None`, что обеспечит отсутствие в заголовке `Content-Type` ответа значения `charset`.

In some cases you may also want to set the `render_style` attribute to `'binary'`. Doing so will also ensure that the browsable API will not attempt to display the binary content as a string.

В некоторых случаях вы также можете установить атрибут `render_style` на `'binary'`. Это также гарантирует, что просматриваемый API не будет пытаться отобразить двоичное содержимое в виде строки.

```
class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
```

---

# Advanced renderer usage

# Расширенное использование рендеринга

You can do some pretty flexible things using REST framework's renderers. Some examples...

Вы можете делать довольно гибкие вещи, используя рендереры фреймворка REST. Некоторые примеры...

* Provide either flat or nested representations from the same endpoint, depending on the requested media type.
* Serve both regular HTML webpages, and JSON based API responses from the same endpoints.
* Specify multiple types of HTML representation for API clients to use.
* Underspecify a renderer's media type, such as using `media_type = 'image/*'`, and use the `Accept` header to vary the encoding of the response.

* Предоставление плоских или вложенных представлений из одной и той же конечной точки, в зависимости от запрашиваемого типа носителя.
* Предоставлять как обычные веб-страницы HTML, так и ответы API на основе JSON с одной и той же конечной точки.
* Указывать несколько типов представления HTML для использования клиентами API.
* Недоопределять медиатип рендерера, например, используя `media_type = 'image/*'`, и использовать заголовок `Accept` для изменения кодировки ответа.

## Varying behavior by media type

## Различное поведение в зависимости от типа носителя

In some cases you might want your view to use different serialization styles depending on the accepted media type. If you need to do this you can access `request.accepted_renderer` to determine the negotiated renderer that will be used for the response.

В некоторых случаях вы можете захотеть, чтобы ваше представление использовало различные стили сериализации в зависимости от принятого типа носителя. Если вам нужно сделать это, вы можете обратиться к `request.accepted_renderer`, чтобы определить согласованный рендерер, который будет использоваться для ответа.

For example:

Например:

```
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

## Underspecifying the media type

## Недоопределение типа носителя.

In some cases you might want a renderer to serve a range of media types. In this case you can underspecify the media types it should respond to, by using a `media_type` value such as `image/*`, or `*/*`.

В некоторых случаях вы можете захотеть, чтобы рендерер обслуживал различные типы медиа. В этом случае вы можете не указывать типы медиа, на которые он должен реагировать, используя значение `media_type`, такое как `image/*`, или `*/*`.

If you underspecify the renderer's media type, you should make sure to specify the media type explicitly when you return the response, using the `content_type` attribute. For example:

Если вы недоопределили медиатип рендерера, вы должны убедиться, что указали медиатип явно, когда возвращаете ответ, используя атрибут `content_type`. Например:

```
return Response(data, content_type='image/png')
```

## Designing your media types

## Проектирование типов носителей

For the purposes of many Web APIs, simple `JSON` responses with hyperlinked relations may be sufficient. If you want to fully embrace RESTful design and [HATEOAS](http://timelessrepo.com/haters-gonna-hateoas) you'll need to consider the design and usage of your media types in more detail.

Для целей многих Web API может быть достаточно простых ответов `JSON` с гиперссылками на отношения. Если вы хотите полностью внедрить RESTful дизайн и [HATEOAS](http://timelessrepo.com/haters-gonna-hateoas), вам необходимо более детально продумать дизайн и использование типов медиа.

In [the words of Roy Fielding](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven), "A REST API should spend almost all of its descriptive effort in defining the media type(s) used for representing resources and driving application state, or in defining extended relation names and/or hypertext-enabled mark-up for existing standard media types.".

По словам [Роя Филдинга] (https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven), "REST API должен потратить почти все свои усилия по описанию на определение типа(ов) медиа, используемых для представления ресурсов и управления состоянием приложения, или на определение расширенных имен отношений и/или гипертекстовой разметки для существующих стандартных типов медиа".

For good examples of custom media types, see GitHub's use of a custom [application/vnd.github+json](https://developer.github.com/v3/media/) media type, and Mike Amundsen's IANA approved [application/vnd.collection+json](http://www.amundsen.com/media-types/collection/) JSON-based hypermedia.

Хорошими примерами пользовательских типов медиа являются использование GitHub пользовательского типа медиа [application/vnd.github+json](https://developer.github.com/v3/media/) и одобренная IANA гипермедиа на основе JSON [application/vnd.collection+json](http://www.amundsen.com/media-types/collection/) Майка Амундсена.

## HTML error views

## HTML представления ошибок

Typically a renderer will behave the same regardless of if it's dealing with a regular response, or with a response caused by an exception being raised, such as an `Http404` or `PermissionDenied` exception, or a subclass of `APIException`.

Обычно рендерер ведет себя одинаково независимо от того, имеет ли он дело с обычным ответом или с ответом, вызванным возникшим исключением, например, исключением `Http404` или `PermissionDenied`, или подклассом `APIException`.

If you're using either the `TemplateHTMLRenderer` or the `StaticHTMLRenderer` and an exception is raised, the behavior is slightly different, and mirrors [Django's default handling of error views](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views).

Если вы используете `TemplateHTMLRenderer` или `StaticHTMLRenderer` и при этом возникает исключение, поведение немного отличается и является зеркальным отражением [Django's default handling of error views](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views).

Exceptions raised and handled by an HTML renderer will attempt to render using one of the following methods, by order of precedence.

Исключения, возникающие и обрабатываемые средством рендеринга HTML, будут пытаться отобразить с помощью одного из следующих методов, в порядке старшинства.

* Load and render a template named `{status_code}.html`.
* Load and render a template named `api_exception.html`.
* Render the HTTP status code and text, for example "404 Not Found".

* Загрузите и отобразите шаблон с именем `{status_code}.html`.
* Загрузите и отобразите шаблон с именем `api_exception.html`.
* Вывести код статуса HTTP и текст, например, "404 Not Found".

Templates will render with a `RequestContext` which includes the `status_code` and `details` keys.

Шаблоны будут отображаться с `RequestContext`, который включает ключи `status_code` и `details`.

**Note**: If `DEBUG=True`, Django's standard traceback error page will be displayed instead of rendering the HTTP status code and text.

**Примечание**: Если `DEBUG=True`, то вместо отображения кода статуса HTTP и текста будет отображаться стандартная страница ошибки трассировки Django.

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

## JSONP

## JSONP

[REST framework JSONP](https://jpadilla.github.io/django-rest-framework-jsonp/) provides JSONP rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[REST framework JSONP](https://jpadilla.github.io/django-rest-framework-jsonp/) обеспечивает поддержку рендеринга JSONP. Ранее он был включен непосредственно в пакет REST framework, а теперь поддерживается как сторонний пакет.

---

**Warning**: If you require cross-domain AJAX requests, you should generally be using the more modern approach of [CORS](https://www.w3.org/TR/cors/) as an alternative to `JSONP`. See the [CORS documentation](https://www.django-rest-framework.org/topics/ajax-csrf-cors/) for more details.

**Предупреждение**: Если вам требуются междоменные AJAX-запросы, вам следует использовать более современный подход [CORS](https://www.w3.org/TR/cors/) в качестве альтернативы `JSONP`. Более подробную информацию смотрите в документации [CORS](https://www.django-rest-framework.org/topics/ajax-csrf-cors/).

The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally readable API endpoints](https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use), where `GET` requests are unauthenticated and do not require any user permissions.

Подход `jsonp` по сути является хаком для браузера и подходит [только для глобально читаемых конечных точек API] (https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use), где запросы `GET` являются неаутентифицированными и не требуют никаких разрешений пользователя.

---

#### Installation & configuration

#### Установка и настройка

Install using pip.

Установите с помощью pip.

```
$ pip install djangorestframework-jsonp
```

Modify your REST framework settings.

Измените настройки фреймворка REST.

```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ],
}
```

## MessagePack

## MessagePack

[MessagePack](https://msgpack.org/) is a fast, efficient binary serialization format. [Juan Riaza](https://github.com/juanriaza) maintains the [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack) package which provides MessagePack renderer and parser support for REST framework.

[MessagePack](https://msgpack.org/) - это быстрый и эффективный формат двоичной сериализации. [Juan Riaza](https://github.com/juanriaza) поддерживает пакет [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack), который обеспечивает поддержку рендеринга и парсера MessagePack для фреймворка REST.

## Microsoft Excel: XLSX (Binary Spreadsheet Endpoints)

## Microsoft Excel: XLSX (Двоичные конечные точки электронных таблиц)

XLSX is the world's most popular binary spreadsheet format. [Tim Allen](https://github.com/flipperpa) of [The Wharton School](https://github.com/wharton) maintains [drf-excel](https://github.com/wharton/drf-excel), which renders an endpoint as an XLSX spreadsheet using OpenPyXL, and allows the client to download it. Spreadsheets can be styled on a per-view basis.

XLSX - это самый популярный в мире формат двоичных электронных таблиц. [Тим Аллен](https://github.com/flipperpa) из [The Wharton School](https://github.com/wharton) поддерживает [drf-excel](https://github.com/wharton/drf-excel), который отображает конечную точку в виде электронной таблицы XLSX с помощью OpenPyXL и позволяет клиенту загрузить ее. Электронные таблицы могут быть стилизованы для каждого вида.

#### Installation & configuration

#### Установка и настройка

Install using pip.

Установите с помощью pip.

```
$ pip install drf-excel
```

Modify your REST framework settings.

Измените настройки фреймворка REST.

```
REST_FRAMEWORK = {
    ...

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'drf_excel.renderers.XLSXRenderer',
    ],
}
```

To avoid having a file streamed without a filename (which the browser will often default to the filename "download", with no extension), we need to use a mixin to override the `Content-Disposition` header. If no filename is provided, it will default to `export.xlsx`. For example:

Чтобы избежать потоковой передачи файла без имени (при этом браузер часто принимает по умолчанию имя файла "download" без расширения), нам необходимо использовать миксин для переопределения заголовка `Content-Disposition`. Если имя файла не указано, то по умолчанию будет задано `export.xlsx`. Например:

```
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

## CSV

Comma-separated values are a plain-text tabular data format, that can be easily imported into spreadsheet applications. [Mjumbe Poe](https://github.com/mjumbewu) maintains the [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv) package which provides CSV renderer support for REST framework.

Значения, разделенные запятыми, - это формат табличных данных в виде обычного текста, который легко импортируется в приложения электронных таблиц. [Mjumbe Poe](https://github.com/mjumbewu) поддерживает пакет [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv), который обеспечивает поддержку CSV-рендеринга для REST-фреймворка.

## UltraJSON

## UltraJSON

[UltraJSON](https://github.com/esnme/ultrajson) is an optimized C JSON encoder which can give significantly faster JSON rendering. [Adam Mertz](https://github.com/Amertz08) maintains [drf_ujson2](https://github.com/Amertz08/drf_ujson2), a fork of the now unmaintained [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer), which implements JSON rendering using the UJSON package.

[UltraJSON](https://github.com/esnme/ultrajson) - это оптимизированный кодировщик JSON на языке C, который может значительно ускорить рендеринг JSON. [Adam Mertz](https://github.com/Amertz08) поддерживает [drf_ujson2](https://github.com/Amertz08/drf_ujson2), форк ныне не поддерживаемого [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer), который реализует рендеринг JSON с использованием пакета UJSON.

## CamelCase JSON

## CamelCase JSON

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) provides camel case JSON renderers and parsers for REST framework. This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names. It is maintained by [Vitaly Babiy](https://github.com/vbabiy).

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) предоставляет рендереры и парсеры JSON в верблюжьем регистре для REST-фреймворка. Это позволяет сериализаторам использовать имена полей в стиле Python с подчеркиванием, но отображать их в API как имена полей в верблюжьем регистре в стиле Javascript. Поддерживается [Виталием Бабием](https://github.com/vbabiy).

## Pandas (CSV, Excel, PNG)

## Pandas (CSV, Excel, PNG)

[Django REST Pandas](https://github.com/wq/django-rest-pandas) provides a serializer and renderers that support additional data processing and output via the [Pandas](https://pandas.pydata.org/) DataFrame API. Django REST Pandas includes renderers for Pandas-style CSV files, Excel workbooks (both `.xls` and `.xlsx`), and a number of [other formats](https://github.com/wq/django-rest-pandas#supported-formats). It is maintained by [S. Andrew Sheppard](https://github.com/sheppard) as part of the [wq Project](https://github.com/wq).

[Django REST Pandas](https://github.com/wq/django-rest-pandas) предоставляет сериализатор и рендереры, которые поддерживают дополнительную обработку и вывод данных через [Pandas](https://pandas.pydata.org/) DataFrame API. Django REST Pandas включает рендереры для файлов CSV в стиле Pandas, рабочих книг Excel (как `.xls`, так и `.xlsx`) и ряда [других форматов](https://github.com/wq/django-rest-pandas#supported-formats). Он поддерживается [S. Andrew Sheppard](https://github.com/sheppard) в рамках проекта [wq Project](https://github.com/wq).

## LaTeX

## LaTeX

[Rest Framework Latex](https://github.com/mypebble/rest-framework-latex) provides a renderer that outputs PDFs using Laulatex. It is maintained by [Pebble (S/F Software)](https://github.com/mypebble).

[Rest Framework Latex](https://github.com/mypebble/rest-framework-latex) предоставляет рендерер, который выводит PDF-файлы с использованием Laulatex. Он поддерживается [Pebble (S/F Software)](https://github.com/mypebble).