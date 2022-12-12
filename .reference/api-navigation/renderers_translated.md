<!-- TRANSLATED by md-translate -->
---

source:

источник:

* renderers.py

* рендереры.py

---

# Renderers

# Рендереры

> Before a TemplateResponse instance can be returned to the client, it must be rendered. The rendering process takes the intermediate representation of template and context, and turns it into the final byte stream that can be served to the client.
>
> — [Django documentation](https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process)

> До того, как экземпляр Templateresponse может быть возвращен клиенту, он должен быть отображен.
Процесс рендеринга принимает промежуточное представление шаблона и контекста и превращает его в конечный байтовый поток, который может быть подан клиенту.
>
>-[документация Django] (https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process)

REST framework includes a number of built in Renderer classes, that allow you to return responses with various media types. There is also support for defining your own custom renderers, which gives you the flexibility to design your own media types.

Структура REST включает в себя ряд встроенных классов рендеринга, которые позволяют возвращать ответы с различными типами медиа.
Существует также поддержка определения ваших собственных пользовательских рендеров, что дает вам гибкость для разработки собственных типов мультимедиа.

## How the renderer is determined

## Как определяется рендерера

The set of valid renderers for a view is always defined as a list of classes. When a view is entered REST framework will perform content negotiation on the incoming request, and determine the most appropriate renderer to satisfy the request.

Набор действительных рендеров для представления всегда определяется как список классов.
Когда введена представление, структура REST будет выполнять согласование контента по входящему запросу и определить наиболее подходящий рендер для удовлетворения запроса.

The basic process of content negotiation involves examining the request's `Accept` header, to determine which media types it expects in the response. Optionally, format suffixes on the URL may be used to explicitly request a particular representation. For example the URL `http://example.com/api/users_count.json` might be an endpoint that always returns JSON data.

Основной процесс переговоров о контенте включает в себя изучение заголовка «Принять» запроса, чтобы определить, какие типы средств массовой информации он ожидает в ответе.
Необязательно, суффиксы формата на URL могут использоваться для явного запроса конкретного представления.
Например, URL `http: // example.com/api/users_count.json` может быть конечной точкой, которая всегда возвращает данные JSON.

For more information see the documentation on [content negotiation](content-negotiation.md).

Для получения дополнительной информации см. Документацию по [согласованию контента] (Content-negotiation.md).

## Setting the renderers

## Установка рендеристов

The default set of renderers may be set globally, using the `DEFAULT_RENDERER_CLASSES` setting. For example, the following settings would use `JSON` as the main media type and also include the self describing API.

Набор визуализаторов по умолчанию может быть установлен по всему миру, используя настройку `default_renderer_classes`.
Например, следующие настройки будут использовать `json` в качестве основного типа медиа, а также включать в себя API, описывающий самоопределение.

```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

You can also set the renderers used for an individual view, or viewset, using the `APIView` class-based views.

Вы также можете установить рендеристы, используемые для индивидуального представления, или Viewset, используя на основе классов представлений `Apiview.

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

Или, если вы используете декоратор `@api_view` с видами на основе функций.

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

## Заказ классов рендеринга

It's important when specifying the renderer classes for your API to think about what priority you want to assign to each media type. If a client underspecifies the representations it can accept, such as sending an `Accept: */*` header, or not including an `Accept` header at all, then REST framework will select the first renderer in the list to use for the response.

Важно при указании классов рендеринга для вашего API, чтобы подумать о том, какой приоритет вы хотите назначить каждому типу медиа.
Если клиент подчеркивает представления, которые он может принять, например, отправка заголовка `chack: */ *` или не включать заголовок `Accept`, то Framework REST выберет первый рендеринг в списке для использования для ответа
Анкет

For example if your API serves JSON responses and the HTML browsable API, you might want to make `JSONRenderer` your default renderer, in order to send `JSON` responses to clients that do not specify an `Accept` header.

Например, если ваш API служит ответам JSON и HTML Browsable API, вы можете сделать `jsonrenderer` рендеринг по умолчанию, чтобы отправить ответы json` на клиентах, которые не указывают заголовок« Принять ».

If your API includes views that can serve both regular webpages and API responses depending on the request, then you might consider making `TemplateHTMLRenderer` your default renderer, in order to play nicely with older browsers that send [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers).

Если ваш API включает в себя представления, которые могут служить как регулярные веб -страницы, так и ответы API в зависимости от запроса, то вы можете рассмотреть возможность создания «TemplateHtmlRenderer» вашего по умолчанию, чтобы хорошо играть со старыми браузерами, которые отправляют [сломанные заголовки принятия] (http://
/www.gethifi.com/blog/browser-rest-http-accecte-ders).

---

# API Reference

# Ссылка на API

## JSONRenderer

## jsonrenderer

Renders the request data into `JSON`, using utf-8 encoding.

Отдает данные запроса в `json`, используя кодирование UTF-8.

Note that the default style is to include unicode characters, and render the response using a compact style with no unnecessary whitespace:

Обратите внимание, что стиль по умолчанию состоит в том, чтобы включать символы Unicode и отображать ответ, используя компактный стиль без ненужных пробелов:

```
{"unicode black star":"★","value":999}
```

The client may additionally include an `'indent'` media type parameter, in which case the returned `JSON` will be indented. For example `Accept: application/json; indent=4`.

Клиент может дополнительно включать параметр типа Media '' '' '' '' ', и в этом случае возвращаемый `json' будет отступать.
Например, `Принять: приложение/json;
adpent = 4`.

```
{
    "unicode black star": "★",
    "value": 999
}
```

The default JSON encoding style can be altered using the `UNICODE_JSON` and `COMPACT_JSON` settings keys.

Стиль кодирования JSON по умолчанию может быть изменен с использованием клавиш настройки `Unicode_json` и` compact_json`.

**.media_type**: `application/json`

**. Media_type **: `Приложение/JSON`

**.format**: `'json'`

**. Формат **: `json'`

**.charset**: `None`

**. Charset **: `none

## TemplateHTMLRenderer

## шаблон

Renders data to HTML, using Django's standard template rendering. Unlike other renderers, the data passed to the `Response` does not need to be serialized. Also, unlike other renderers, you may want to include a `template_name` argument when creating the `Response`.

Образует данные в HTML, используя стандартный шаблон Django.
В отличие от других рендереров, данные, передаваемые «ответу», не должны быть сериализованы.
Кроме того, в отличие от других визуализаторов, вы можете включить аргумент «template_name» при создании «ответа».

The TemplateHTMLRenderer will create a `RequestContext`, using the `response.data` as the context dict, and determine a template name to use to render the context.

Templatehtmlrenderer создаст `requestContext`, используя` recsion.data` в качестве контекста, и определит имя шаблона для использования для визуализации контекста.

---

**Note:** When used with a view that makes use of a serializer the `Response` sent for rendering may not be a dictionary and will need to be wrapped in a dict before returning to allow the `TemplateHTMLRenderer` to render it. For example:

** ПРИМЕЧАНИЕ.
Например:

```
response.data = {'results': response.data}
```

---

The template name is determined by (in order of preference):

Имя шаблона определяется (в порядке предпочтения):

1. An explicit `template_name` argument passed to the response.
2. An explicit `.template_name` attribute set on this class.
3. The return result of calling `view.get_template_names()`.

1. Явный аргумент `template_name` передан ответу.
2. Явный атрибут `.template_name` на этом классе.
3. Результат возвращения вызова `view.get_template_names ()`.

An example of a view that uses `TemplateHTMLRenderer`:

Пример представления, в котором используется `templatehtmlrenderer`:

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

Вы можете использовать `templatehtmlrenderer` либо для возврата обычных HTML -страниц, используя структуру REST, либо для возврата ответов HTML и API из одной конечной точки.

If you're building websites that use `TemplateHTMLRenderer` along with other renderer classes, you should consider listing `TemplateHTMLRenderer` as the first class in the `renderer_classes` list, so that it will be prioritised first even for browsers that send poorly formed `ACCEPT:` headers.

Если вы строите веб -сайты, которые используют `templatehtmlrenderer` вместе с другими классами рендеринга, вам следует рассмотреть вопрос о перечислении« TemplateHtmlRenderer` как первый класс в списке `renderer_classes», так что он будет сначала приоритет, даже для броузеров, которые отправляют плохо сформированные ``
Принять: `Заголовки.

See the [*HTML & Forms* Topic Page](../topics/html-and-forms.md) for further examples of `TemplateHTMLRenderer` usage.

См. Страницу [* html & forms* Topic] (../ Темы/html-and-forms.md) для дальнейших примеров использования `templatehtmlrenderer.

**.media_type**: `text/html`

**. media_type **: `text/html`

**.format**: `'html'`

**. Формат **: `'html'`

**.charset**: `utf-8`

**. Charset **: `utf-8`

See also: `StaticHTMLRenderer`

См. Также: `statichtmlrenderer`

## StaticHTMLRenderer

## statichtmlrenderer

A simple renderer that simply returns pre-rendered HTML. Unlike other renderers, the data passed to the response object should be a string representing the content to be returned.

Простой рендерер, который просто возвращает предварительно рендерированный HTML.
В отличие от других рендеристов, данные, передаваемые объекту ответа, должны быть строкой, представляющей содержание, которое будет возвращено.

An example of a view that uses `StaticHTMLRenderer`:

Пример представления, который использует `statichtmlrenderer`:

```
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```

You can use `StaticHTMLRenderer` either to return regular HTML pages using REST framework, or to return both HTML and API responses from a single endpoint.

Вы можете использовать `statichtmlrenderer` либо для возврата обычных HTML -страниц, используя структуру REST, либо для возврата ответов HTML и API из одной конечной точки.

**.media_type**: `text/html`

**. media_type **: `text/html`

**.format**: `'html'`

**. Формат **: `'html'`

**.charset**: `utf-8`

**. Charset **: `utf-8`

See also: `TemplateHTMLRenderer`

См. Также: `templatehtmlrenderer`

## BrowsableAPIRenderer

## browableApirenderer

Renders data into HTML for the Browsable API:

Образует данные в HTML для API, который можно просматривать:

![The BrowsableAPIRenderer](../img/quickstart.png)

! [BrowsableApirenderer] (../ img/QuickStart.png)

This renderer will determine which other renderer would have been given highest priority, and use that to display an API style response within the HTML page.

Этот рендерер будет определять, какой другой рендерер был бы указан наивысшим приоритетом, и использовать его для отображения ответа в стиле API на странице HTML.

**.media_type**: `text/html`

**. media_type **: `text/html`

**.format**: `'api'`

**. Формат **: `'api'

**.charset**: `utf-8`

**. Charset **: `utf-8`

**.template**: `'rest_framework/api.html'`

**. Шаблон **: `'rest_framework/api.html'`

#### Customizing BrowsableAPIRenderer

#### Настройка BrowsableApirenderer

By default the response content will be rendered with the highest priority renderer apart from `BrowsableAPIRenderer`. If you need to customize this behavior, for example to use HTML as the default return format, but use JSON in the browsable API, you can do so by overriding the `get_default_renderer()` method. For example:

По умолчанию содержимое ответа будет отображаться с самым приоритетным рендерером, кроме «BrowableApirenderer».
Если вам нужно настроить это поведение, например, для использования HTML в качестве формата возврата по умолчанию, но используйте JSON в API, который можно просмотреть, вы можете сделать это, переоценив метод `get_default_renderer ()`.
Например:

```
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer

## adminrenderer

Renders data into HTML for an admin-like display:

Отправляет данные в HTML для административного дисплея:

![The AdminRender view](../img/admin.png)

! [Представление администратора] (../ img/admin.png)

This renderer is suitable for CRUD-style web APIs that should also present a user-friendly interface for managing the data.

Этот рендерер подходит для веб-API в стиле CRUD, которые также должны представлять удобный интерфейс для управления данными.

Note that views that have nested or list serializers for their input won't work well with the `AdminRenderer`, as the HTML forms are unable to properly support them.

Обратите внимание, что представления, которые вложены или перечисляют сериализаторы для их вклада, не будут хорошо работать с `adminrenderer ', поскольку формы HTML не могут должным образом поддержать их.

**Note**: The `AdminRenderer` is only able to include links to detail pages when a properly configured `URL_FIELD_NAME` (`url` by default) attribute is present in the data. For `HyperlinkedModelSerializer` this will be the case, but for `ModelSerializer` or plain `Serializer` classes you'll need to make sure to include the field explicitly. For example here we use models `get_absolute_url` method:

** ПРИМЕЧАНИЕ **: `adminrenderer` способен включать ссылки на детали страниц только при правильном настроенном атрибуте` url_field_name` (`url` по умолчанию) присутствует в данных.
Для `‘ HyperlinkedModelserializer` это будет иметь место, но для классов `modelerializer 'или простых классов« serializer », которые вам необходимо, чтобы убедиться, что это поле явно.
Например, здесь мы используем модели `get_absolute_url` Метод:

```
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Account
```

**.media_type**: `text/html`

**. media_type **: `text/html`

**.format**: `'admin'`

**. Формат **: `'admin'

**.charset**: `utf-8`

**. Charset **: `utf-8`

**.template**: `'rest_framework/admin.html'`

**. Шаблон **: `'rest_framework/admin.html'

## HTMLFormRenderer

## htmlformrenderer

Renders data returned by a serializer into an HTML form. The output of this renderer does not include the enclosing `<form>` tags, a hidden CSRF input or any submit buttons.

Отправляет данные, возвращаемые сериализатором в форму HTML.
Вывод этого рендеринга не включает в себя вкладывание `<Form>` теги, скрытый ввод CSRF или любые кнопки отправки.

This renderer is not intended to be used directly, but can instead be used in templates by passing a serializer instance to the `render_form` template tag.

Этот визуализатор не предназначен для использования напрямую, но вместо этого может использоваться в шаблонах путем передачи экземпляра сериализатора в тег шаблона `render_form`.

```
{% load rest_framework %}

<form action="/submit-report/" method="post">
    {% csrf_token %}
    {% render_form serializer %}
    <input type="submit" value="Save" />
</form>
```

For more information see the [HTML & Forms](../topics/html-and-forms.md) documentation.

Для получения дополнительной информации см. Документацию [html & forms] (../ Themes/html-and-forms.md).

**.media_type**: `text/html`

**. media_type **: `text/html`

**.format**: `'form'`

**. Формат **: `'Форма

**.charset**: `utf-8`

**. Charset **: `utf-8`

**.template**: `'rest_framework/horizontal/form.html'`

**.

## MultiPartRenderer

## multiprterenderer

This renderer is used for rendering HTML multipart form data. **It is not suitable as a response renderer**, but is instead used for creating test requests, using REST framework's [test client and test request factory](testing.md).

Этот рендерер используется для отображения данных Multipart Form HTML.
** Он не подходит в качестве рендеринга ответа **, но вместо этого используется для создания тестовых запросов, используя Framework Framework [тестовый клиент и завод по запросу тестирования] (testing.md).

**.media_type**: `multipart/form-data; boundary=BoUnDaRyStRiNg`

**. Media_type **: `multipart/form-data;
Boundary = BoundaryString`

**.format**: `'multipart'`

**. Формат **: `'multipart'`

**.charset**: `utf-8`

**. Charset **: `utf-8`

---

# Custom renderers

# Пользовательские визуализации

To implement a custom renderer, you should override `BaseRenderer`, set the `.media_type` and `.format` properties, and implement the `.render(self, data, accepted_media_type=None, renderer_context=None)` method.

Чтобы реализовать пользовательский рендеринг, вы должны переопределить «baserenderer», установить свойства `.media_type` и` .format` и реализовать метод.

The method should return a bytestring, which will be used as the body of the HTTP response.

Метод должен вернуть Bytestring, который будет использоваться в качестве тела ответа HTTP.

The arguments passed to the `.render()` method are:

Аргументы, передаваемые методу `.render ()`:

### `data`

### `data`

The request data, as set by the `Response()` instantiation.

Данные запроса, установленные `response ()` экземпляром.

### `accepted_media_type=None`

### `pressted_media_type = нет

Optional. If provided, this is the accepted media type, as determined by the content negotiation stage.

По желанию.
Если предоставлено, это принятый тип носителя, как определяется этапом согласования контента.

Depending on the client's `Accept:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters. For example `"application/json; nested=true"`.

В зависимости от заголовка клиента: «Заголовок», это может быть более конкретным, чем атрибут рендеринга `media_type`, и может включать параметры типа носителя.
Например, `" Приложение/json; insed = true "`.

### `renderer_context=None`

### `renderer_context = нет

Optional. If provided, this is a dictionary of contextual information provided by the view.

По желанию.
Если предоставлено, это словарь контекстной информации, предоставленной представлением.

By default this will include the following keys: `view`, `request`, `response`, `args`, `kwargs`.

По умолчанию это будет включать в себя следующие ключи: `view`,` request`, `response`,` args`, `kwargs`.

## Example

## Пример

The following is an example plaintext renderer that will return a response with the `data` parameter as the content of the response.

Ниже приведен пример обратного текста, который вернет ответ с параметром «Data» в качестве содержимого ответа.

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

Предполагается, что классы рендеринга по умолчанию используют кодирование `UTF-8`.
Чтобы использовать другую кодировку, установите атрибут `charset` на рендерере.

```
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

Note that if a renderer class returns a unicode string, then the response content will be coerced into a bytestring by the `Response` class, with the `charset` attribute set on the renderer used to determine the encoding.

Обратите внимание, что если класс рендеринга возвращает строку Unicode, то содержимое ответа будет принуждено к байетрированию с помощью класса `recsess 'с набором атрибута` charset` на рендерере, используемом для определения кодирования.

If the renderer returns a bytestring representing raw binary content, you should set a charset value of `None`, which will ensure the `Content-Type` header of the response will not have a `charset` value set.

Если рендерерат возвращает байтэгринг, представляющий необработанное двоичное содержание, вам следует установить значение charset `none`, что обеспечит заголовок типа контента.

In some cases you may also want to set the `render_style` attribute to `'binary'`. Doing so will also ensure that the browsable API will not attempt to display the binary content as a string.

В некоторых случаях вы также можете установить атрибут `render_style` на« двоичный ».
Это также гарантирует, что API Browsable не будет пытаться отобразить двоичный контент в качестве строки.

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

# Усовершенствованное использование рендерера

You can do some pretty flexible things using REST framework's renderers. Some examples...

Вы можете сделать несколько довольно гибких вещей, используя рендеринги REST Framework.
Некоторые примеры...

* Provide either flat or nested representations from the same endpoint, depending on the requested media type.
* Serve both regular HTML webpages, and JSON based API responses from the same endpoints.
* Specify multiple types of HTML representation for API clients to use.
* Underspecify a renderer's media type, such as using `media_type = 'image/*'`, and use the `Accept` header to vary the encoding of the response.

* Предоставьте либо плоские, либо вложенные представления с одной и той же конечной точки, в зависимости от запрошенного типа носителя.
* Подают как обычные веб -страницы HTML, так и ответы API на основе JSON из одних и тех же конечных точек.
* Укажите несколько типов HTML -представления для использования клиентами API.
* Подчеркните тип медиа -рендеры, например, использование `media_type = 'image/*'` `, и используйте заголовок` Accept`, чтобы изменить кодирование ответа.

## Varying behavior by media type

## различное поведение по типу медиа

In some cases you might want your view to use different serialization styles depending on the accepted media type. If you need to do this you can access `request.accepted_renderer` to determine the negotiated renderer that will be used for the response.

В некоторых случаях вы можете хотеть, чтобы ваше мнение использовало различные стили сериализации в зависимости от принятого типа носителя.
Если вам нужно сделать это, вы можете получить доступ к `request.accepted_renderer`, чтобы определить согласованный рендерер, который будет использоваться для ответа.

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

## подчеркивает тип медиа

In some cases you might want a renderer to serve a range of media types. In this case you can underspecify the media types it should respond to, by using a `media_type` value such as `image/*`, or `*/*`.

В некоторых случаях вы можете захотеть, чтобы рендерер обслуживал ряд типов средств массовой информации.
В этом случае вы можете подчеркнуть типы носителей, на которые он должен отвечать, используя значение `media_type`, такое как` Image/*`или`*/*`.

If you underspecify the renderer's media type, you should make sure to specify the media type explicitly when you return the response, using the `content_type` attribute. For example:

Если вы подчеркиваете тип медиа -типа рендеринга, вы должны явно указать тип носителя при возврате ответа, используя атрибут `content_type`.
Например:

```
return Response(data, content_type='image/png')
```

## Designing your media types

## Проектирование ваших типов мультимедиа

For the purposes of many Web APIs, simple `JSON` responses with hyperlinked relations may be sufficient. If you want to fully embrace RESTful design and [HATEOAS](http://timelessrepo.com/haters-gonna-hateoas) you'll need to consider the design and usage of your media types in more detail.

Для целей многих веб -API -интерфейсов могут быть достаточными простыми ответами `json` с гиперссыщенными отношениями.
Если вы хотите полностью принять Restful Design и [Hateoas] (http://timelessrepo.com/haters-gonna-hateoas), вам нужно более подробно рассмотреть дизайн и использование ваших типов средств массовой информации.

In [the words of Roy Fielding](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven), "A REST API should spend almost all of its descriptive effort in defining the media type(s) used for representing resources and driving application state, or in defining extended relation names and/or hypertext-enabled mark-up for existing standard media types.".

В [словах Роя Филдинга] (https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-управляемый), «API отдыха должен тратить почти все свои описательные усилия в определении
Тип медиа, используемые для представления ресурсов и состояния приложения, или для определения имен расширенных отношений и/или наценки с поддержкой гипертекста для существующих стандартных типов носителей ».

For good examples of custom media types, see GitHub's use of a custom [application/vnd.github+json](https://developer.github.com/v3/media/) media type, and Mike Amundsen's IANA approved [application/vnd.collection+json](http://www.amundsen.com/media-types/collection/) JSON-based hypermedia.

Хорошие примеры пользовательских типов средств массовой информации, см. Использование GitHub пользовательского [Application/vnd.github+json] (https://developer.github.com/v3/media/) Тип медиа и одобренность Mike Amundsen Iana [Приложение/
Vnd.Collection+JSON] (http://www.amundsen.com/media-types/collection/) json на основе гипермедиа на основе JSON.

## HTML error views

## html -виды ошибок

Typically a renderer will behave the same regardless of if it's dealing with a regular response, or with a response caused by an exception being raised, such as an `Http404` or `PermissionDenied` exception, or a subclass of `APIException`.

Как правило, рендерер будет вести себя так же, независимо от того, имеет ли это дело с регулярным ответом, или с ответом, вызванным исключением, таким как `http404` или` recissionDied` или подкласс «apiexception».

If you're using either the `TemplateHTMLRenderer` or the `StaticHTMLRenderer` and an exception is raised, the behavior is slightly different, and mirrors [Django's default handling of error views](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views).

Если вы используете либо `templatehtmlrenderer`, либо` statichtmlrenderer` и исключение поднято, поведение немного отличается, и отражает [Django по умолчанию видов ошибок] (https://docs.djangoproject.com/en/.
Стабильные/Темы/http/views/#настраивающие версии-виды).

Exceptions raised and handled by an HTML renderer will attempt to render using one of the following methods, by order of precedence.

Исключения, поднятые и обработанные рендерером HTML, будут пытаться отображать, используя один из следующих методов по порядку приоритета.

* Load and render a template named `{status_code}.html`.
* Load and render a template named `api_exception.html`.
* Render the HTTP status code and text, for example "404 Not Found".

* Загрузите и визуализируйте шаблон с именем `{status_code} .html`.
* Загрузите и отображайте шаблон с именем `api_exception.html`.
* Оформлена код состояния HTTP и текст, например, «404 не найден».

Templates will render with a `RequestContext` which includes the `status_code` and `details` keys.

Шаблоны будут отображаться с `requestContext`, который включает в себя ключи` status_code` и `details`.

**Note**: If `DEBUG=True`, Django's standard traceback error page will be displayed instead of rendering the HTTP status code and text.

** Примечание **: Если `debug = true`, вместо того, чтобы отобразить код состояния HTTP и текст, будет отображаться стандартная страница ошибки Traceback.

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

## JSONP

## jsonp

[REST framework JSONP](https://jpadilla.github.io/django-rest-framework-jsonp/) provides JSONP rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

[Framework rest jsonp] (https://jpadilla.github.io/django-rest-framework-jsonp/) предоставляет поддержку рендеринга jsonp.
Ранее он был включен непосредственно в пакет Framework REST и теперь вместо этого поддерживается как сторонний пакет.

---

**Warning**: If you require cross-domain AJAX requests, you should generally be using the more modern approach of [CORS](https://www.w3.org/TR/cors/) as an alternative to `JSONP`. See the [CORS documentation](https://www.django-rest-framework.org/topics/ajax-csrf-cors/) for more details.

** Предупреждение **: Если вам нужны запросы Ajax Cross-Domain, вы, как правило, должны использовать более современный подход [cors] (https://www.w3.org/tr/cors/) в качестве альтернативы `jsonp
`.
См. Документация CORS] (https://www.django-rest-framework.org/topics/ajax-csrf-cors/) для получения более подробной информации.

The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally readable API endpoints](https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use), where `GET` requests are unauthenticated and do not require any user permissions.

Подход `jsonp`, по сути, является взломом браузера и [только подходит для глобально читаемых API конечных точек] (https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use), где` get`
Запросы не являются несанкционированными и не требуют никаких разрешений пользователей.

---

#### Installation & configuration

#### Установка и конфигурация

Install using pip.

Установите с помощью PIP.

```
$ pip install djangorestframework-jsonp
```

Modify your REST framework settings.

Измените настройки структуры REST.

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

[MessagePack] (https://msgpack.org/) является быстрым, эффективным форматом бинарной сериализации.
[Juan Riaza] (https://github.com/juanriaza) поддерживает [djangestframework-msgpack] (https://github.com/juanriaza/django-rest-framework-msgpac
Структура отдыха.

## Microsoft Excel: XLSX (Binary Spreadsheet Endpoints)

## Microsoft Excel: XLSX (Двоичная таблица конечных точек)

XLSX is the world's most popular binary spreadsheet format. [Tim Allen](https://github.com/flipperpa) of [The Wharton School](https://github.com/wharton) maintains [drf-excel](https://github.com/wharton/drf-excel), which renders an endpoint as an XLSX spreadsheet using OpenPyXL, and allows the client to download it. Spreadsheets can be styled on a per-view basis.

XLSX является самым популярным в мире бинарным форматом таблицы.
[Тим Аллен] (https://github.com/flipperpa) [The Wharton School] (https://github.com/wharton) поддерживает [drf-excel] (https://github.com/wharton/drf
-excel), которая делает конечную точку как электронную таблицу XLSX с использованием OpenPyxl, и позволяет клиенту загрузить ее.
Электронные таблицы могут быть стилизованы для каждого вида.

#### Installation & configuration

#### Установка и конфигурация

Install using pip.

Установите с помощью PIP.

```
$ pip install drf-excel
```

Modify your REST framework settings.

Измените настройки структуры REST.

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

Чтобы избежать потокового файла без имени файла (который браузер часто по умолчанию по умолчанию в имя файла «загрузка», без расширения), нам нужно использовать микшин для переопределения заголовка «Контент-дискозиа».
Если имя файла не будет предоставлено, оно по умолчанию будет `export.xlsx`.
Например:

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

## csv

Comma-separated values are a plain-text tabular data format, that can be easily imported into spreadsheet applications. [Mjumbe Poe](https://github.com/mjumbewu) maintains the [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv) package which provides CSV renderer support for REST framework.

Значения, разделенные за запятой, представляют собой простой текст табличного формата данных, который можно легко импортировать в приложения для электронных таблиц.
[Mjumbe poe] (https://github.com/mjumbewu) поддерживает [djangestframework-csv] (https://github.com/mjumbewu/django-rest-framework-csv), который обеспечивает поддержку кари-носителя CSV для Framework RET
Анкет

## UltraJSON

## Ultrajson

[UltraJSON](https://github.com/esnme/ultrajson) is an optimized C JSON encoder which can give significantly faster JSON rendering. [Adam Mertz](https://github.com/Amertz08) maintains [drf_ujson2](https://github.com/Amertz08/drf_ujson2), a fork of the now unmaintained [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer), which implements JSON rendering using the UJSON package.

[Ultrajson] (https://github.com/esnme/ultrajson) - это оптимизированный энкодер C json, который может дать значительно более быстрый рендеринг JSON.
[Adam Mertz] (https://github.com/amertz08) поддерживает [drf_ujson2] (https://github.com/amertz08/drf_ujson2), вилка ныне неосвященного [drf-ujson-renderer] (https:/
/github.com/gizmag/drf-ujson-renderer), который реализует json рендеринг с использованием пакета UJSON.

## CamelCase JSON

## Camelcase Json

[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) provides camel case JSON renderers and parsers for REST framework. This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names. It is maintained by [Vitaly Babiy](https://github.com/vbabiy).

[djangorestframework-camel-case] (https://github.com/vbabiy/djangorestframework-camel-case) обеспечивает визуализаторы и анализаторов верблюда для кабеля и анализаторов.
Это позволяет сериализаторам использовать имена поля в стиле Python, но в API выставлены в качестве имен поля для верблюжьего корпуса в стиле JavaScript.
Это поддерживается [Vitaly Babiy] (https://github.com/vbabiy).

## Pandas (CSV, Excel, PNG)

## pandas (CSV, Excel, Png)

[Django REST Pandas](https://github.com/wq/django-rest-pandas) provides a serializer and renderers that support additional data processing and output via the [Pandas](https://pandas.pydata.org/) DataFrame API. Django REST Pandas includes renderers for Pandas-style CSV files, Excel workbooks (both `.xls` and `.xlsx`), and a number of [other formats](https://github.com/wq/django-rest-pandas#supported-formats). It is maintained by [S. Andrew Sheppard](https://github.com/sheppard) as part of the [wq Project](https://github.com/wq).

[Django Rest Pandas] (https://github.com/wq/django-rest-pandas) предоставляет сериализатор и рендеринг, которые поддерживают дополнительную обработку и вывод данных через [pandas] (https://pandas.pydata.org/
) DataFrame API.
Django Rest Pandas включает в себя рендеристы для файлов CSV в стиле Pandas, рабочих книг Excel (оба `.xls` и` .xlsx`) и ряд [других форматов] (https://github.com/wq/django-rest-
Панды#поддерживаемые форматы).
Это поддерживается [S.
Эндрю Шеппард] (https://github.com/sheppard) как часть проекта [WQ] (https://github.com/wq).

## LaTeX

## латекс

[Rest Framework Latex](https://github.com/mypebble/rest-framework-latex) provides a renderer that outputs PDFs using Laulatex. It is maintained by [Pebble (S/F Software)](https://github.com/mypebble).

[LATEX LATEX REST] (https://github.com/mypebble/rest-framework-latex) предоставляет рендеринг, который выводит PDF с использованием Laulatex.
Он поддерживается [Pebble (S/F Software)] (https://github.com/mypebble).