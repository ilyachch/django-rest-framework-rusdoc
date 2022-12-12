<!-- TRANSLATED by md-translate -->
---

source:

источник:

* response.py

* response.py

---

# Responses

# Ответы

> Unlike basic HttpResponse objects, TemplateResponse objects retain the details of the context that was provided by the view to compute the response. The final output of the response is not computed until it is needed, later in the response process.
>
> — [Django documentation][cite]

> В отличие от основных объектов httpresponse, объекты TemplaterSponse сохраняют детали контекста, который был предоставлен представлением для вычисления ответа.
Окончательный результат ответа не будет рассчитан до тех пор, пока он не будет необходим, позже в процессе отклика.
>
> - [документация Django] [цитирует]

REST framework supports HTTP content negotiation by providing a `Response` class which allows you to return content that can be rendered into multiple content types, depending on the client request.

Структура REST поддерживает согласование контента HTTP, предоставляя класс «ответа», который позволяет возвращать контент, который можно представить в несколько типов контента, в зависимости от запроса клиента.

The `Response` class subclasses Django's `SimpleTemplateResponse`. `Response` objects are initialised with data, which should consist of native Python primitives. REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.

Подкласс класса `ответы Django« SimpleTemplateReSponse ».
`Объекты ответа инициализируются с помощью данных, которые должны состоять из нативных примитивов Python.
Затем Framework REST использует стандартные переговоры о контенте HTTP, чтобы определить, как оно должно представить конечный контент ответа.

There's no requirement for you to use the `Response` class, you can also return regular `HttpResponse` or `StreamingHttpResponse` objects from your views if required. Using the `Response` class simply provides a nicer interface for returning content-negotiated Web API responses, that can be rendered to multiple formats.

Вам не требуется использовать класс `repless ', вы также можете вернуть регулярные объекты` httpresponse' или `streaminghttpresponse` из ваших представлений, если это необходимо.
Использование класса `response` просто предоставляет более приятный интерфейс для возврата ответов на веб-API-отрицательных контента, который можно представить в нескольких форматах.

Unless you want to heavily customize REST framework for some reason, you should always use an `APIView` class or `@api_view` function for views that return `Response` objects. Doing so ensures that the view can perform content negotiation and select the appropriate renderer for the response, before it is returned from the view.

Если вы не хотите сильно настраивать структуру REST по какой -то причине, вам всегда следует использовать класс `apiview` или функцию`@api_view` для представлений, которые возвращают объекты ответа.
Это гарантирует, что представление может выполнять согласование контента и выбрать соответствующий рендеринг для ответа, прежде чем оно будет возвращено из представления.

---

# Creating responses

# Создание ответов

## Response()

## Ответ()

**Signature:** `Response(data, status=None, template_name=None, headers=None, content_type=None)`

** Подпись: ** `response (data, status = none, template_name = none, headers = none, content_type = none)`

Unlike regular `HttpResponse` objects, you do not instantiate `Response` objects with rendered content. Instead you pass in unrendered data, which may consist of any Python primitives.

В отличие от регулярных объектов `httpresponse`, вы не создаете экземпляры объектов ответа` с визуализированным контентом.
Вместо этого вы передаете непревзойденные данные, которые могут состоять из любых примитивов Python.

The renderers used by the `Response` class cannot natively handle complex datatypes such as Django model instances, so you need to serialize the data into primitive datatypes before creating the `Response` object.

Рендеры, используемые классом «ответ», не могут быть изначально обрабатывать сложные данные дата, такие как экземпляры модели Django, поэтому вам необходимо сериализовать данные на примитивные данные дата, прежде чем создавать объект `replect`.

You can use REST framework's `Serializer` classes to perform this data serialization, or use your own custom serialization.

Вы можете использовать классы REST Framework `serializer` для выполнения этой сериализации данных или использовать собственную пользовательскую сериализацию.

Arguments:

Аргументы:

* `data`: The serialized data for the response.
* `status`: A status code for the response. Defaults to 200. See also [status codes](status-codes.md).
* `template_name`: A template name to use if `HTMLRenderer` is selected.
* `headers`: A dictionary of HTTP headers to use in the response.
* `content_type`: The content type of the response. Typically, this will be set automatically by the renderer as determined by content negotiation, but there may be some cases where you need to specify the content type explicitly.

* `data`: сериализованные данные для ответа.
* `status`: код состояния для ответа.
По умолчанию до 200. См. Также [Коды статуса] (Status-codes.md).
* `template_name`: имя шаблона для использования, если выбрано` htmlrenderer`.
* `Headers`: словарь заголовков HTTP для использования в ответе.
* `content_type`: тип контента ответа.
Как правило, это будет автоматически установлено рендерером, определяемым в соответствии с согласованием контента, но могут быть некоторые случаи, когда вам необходимо явно указать тип контента.

---

# Attributes

# Атрибуты

## .data

## .данные

The unrendered, serialized data of the response.

Несоблюдения, сериализованные данные ответа.

## .status_code

## .status_code

The numeric status code of the HTTP response.

Числовой код состояния ответа HTTP.

## .content

## .содержание

The rendered content of the response. The `.render()` method must have been called before `.content` can be accessed.

Визуализированное содержание ответа.
Метод `.render ()` должен быть вызван до `.content` можно получить доступ.

## .template_name

## .Имя Шаблона

The `template_name`, if supplied. Only required if `HTMLRenderer` or some other custom template renderer is the accepted renderer for the response.

`Template_name`, если он поставляется.
Требуется только в том случае, если `htmlrenderer` или какой -либо другой пользовательский визуализатор шаблона является принятым визуализацией для ответа.

## .accepted_renderer

## .accepted_renderer

The renderer instance that will be used to render the response.

Экземпляр рендерера, который будет использоваться для отображения ответа.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Установите автоматически `apiview` или`@api_view` непосредственно перед возвращением ответа из представления.

## .accepted_media_type

## .accepted_media_type

The media type that was selected by the content negotiation stage.

Тип СМИ, который был выбран на стадии переговоров по контенту.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Установите автоматически `apiview` или`@api_view` непосредственно перед возвращением ответа из представления.

## .renderer_context

## .renderer_context

A dictionary of additional context information that will be passed to the renderer's `.render()` method.

Словарь дополнительной контекстной информации, которая будет передана методу рендерера `.render ()`.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Установите автоматически `apiview` или`@api_view` непосредственно перед возвращением ответа из представления.

---

# Standard HttpResponse attributes

# Стандартные атрибуты httpresponse

The `Response` class extends `SimpleTemplateResponse`, and all the usual attributes and methods are also available on the response. For example you can set headers on the response in the standard way:

Класс `replect 'расширяет` SimpleTemplaterSponse`, и все обычные атрибуты и методы также доступны в ответе.
Например, вы можете установить заголовки на ответ стандартным способом:

```
response = Response()
response['Cache-Control'] = 'no-cache'
```

## .render()

## .оказывать()

**Signature:** `.render()`

** Подпись: ** `.render ()`

As with any other `TemplateResponse`, this method is called to render the serialized data of the response into the final response content. When `.render()` is called, the response content will be set to the result of calling the `.render(data, accepted_media_type, renderer_context)` method on the `accepted_renderer` instance.

Как и в случае любого другого «TemplaterSponse», этот метод вызывается для представления сериализованных данных ответа в конечный содержимое ответа.
Когда называется `.render ()`, содержимое ответа будет установлено на результат вызова метода `.render (data, accomted_media_type, renderer_context)` на экземпляре `adcockted_renderer`.

You won't typically need to call `.render()` yourself, as it's handled by Django's standard response cycle.

Обычно вам не нужно будет вызывать `.render ()` сами, так как он обрабатывается стандартным циклом ответа Джанго.