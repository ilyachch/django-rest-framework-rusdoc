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

> В отличие от базовых объектов HttpResponse, объекты TemplateResponse сохраняют детали контекста, который был предоставлен представлением для вычисления ответа. Окончательный результат ответа не вычисляется до тех пор, пока он не понадобится, позже в процессе ответа.
>
> - [Django documentation][cite]

REST framework supports HTTP content negotiation by providing a `Response` class which allows you to return content that can be rendered into multiple content types, depending on the client request.

Фреймворк REST поддерживает согласование содержимого HTTP, предоставляя класс `Response`, который позволяет возвращать содержимое, которое может быть преобразовано в несколько типов содержимого, в зависимости от запроса клиента.

The `Response` class subclasses Django's `SimpleTemplateResponse`. `Response` objects are initialised with data, which should consist of native Python primitives. REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.

Класс `Response` является подклассом Django `SimpleTemplateResponse`. Объекты `Response` инициализируются данными, которые должны состоять из собственных примитивов Python. Затем фреймворк REST использует стандартное согласование содержимого HTTP для определения того, как он должен отображать конечное содержимое ответа.

There's no requirement for you to use the `Response` class, you can also return regular `HttpResponse` or `StreamingHttpResponse` objects from your views if required. Using the `Response` class simply provides a nicer interface for returning content-negotiated Web API responses, that can be rendered to multiple formats.

Нет необходимости использовать класс `Response`, при необходимости вы можете возвращать обычные объекты `HttpResponse` или `StreamingHttpResponse` из ваших представлений. Использование класса `Response` просто предоставляет более удобный интерфейс для возврата ответов Web API, согласованных по содержанию, которые могут быть преобразованы в различные форматы.

Unless you want to heavily customize REST framework for some reason, you should always use an `APIView` class or `@api_view` function for views that return `Response` objects. Doing so ensures that the view can perform content negotiation and select the appropriate renderer for the response, before it is returned from the view.

Если вы по каким-то причинам не хотите сильно настраивать REST-фреймворк, вы всегда должны использовать класс `APIView` или функцию `@api_view` для представлений, которые возвращают объекты `Response`. Это гарантирует, что представление сможет выполнить согласование содержимого и выбрать подходящий рендерер для ответа, прежде чем он будет возвращен из представления.

---

# Creating responses

# Создание ответов

## Response()

## Response()

**Signature:** `Response(data, status=None, template_name=None, headers=None, content_type=None)`

**Подпись:** `Response(data, status=None, template_name=None, headers=None, content_type=None)`.

Unlike regular `HttpResponse` objects, you do not instantiate `Response` objects with rendered content. Instead you pass in unrendered data, which may consist of any Python primitives.

В отличие от обычных объектов `HttpResponse`, вы не создаете объекты `Response` с отрисованным содержимым. Вместо этого вы передаете нерендерированные данные, которые могут состоять из любых примитивов Python.

The renderers used by the `Response` class cannot natively handle complex datatypes such as Django model instances, so you need to serialize the data into primitive datatypes before creating the `Response` object.

Рендереры, используемые классом `Response`, не могут нативно обрабатывать сложные типы данных, такие как экземпляры моделей Django, поэтому вам необходимо сериализовать данные в примитивные типы данных перед созданием объекта `Response`.

You can use REST framework's `Serializer` classes to perform this data serialization, or use your own custom serialization.

Вы можете использовать классы `Serializer` фреймворка REST для выполнения этой сериализации данных или использовать свою собственную сериализацию.

Arguments:

Аргументы:

* `data`: The serialized data for the response.
* `status`: A status code for the response. Defaults to 200. See also [status codes](status-codes.md).
* `template_name`: A template name to use if `HTMLRenderer` is selected.
* `headers`: A dictionary of HTTP headers to use in the response.
* `content_type`: The content type of the response. Typically, this will be set automatically by the renderer as determined by content negotiation, but there may be some cases where you need to specify the content type explicitly.

* `data`: Сериализованные данные для ответа.
* `status`: Код статуса для ответа. По умолчанию 200. См. также [коды статуса](status-codes.md).
* `template_name`: Имя шаблона, который будет использоваться, если выбран `HTMLRenderer`.
* `headers`: Словарь заголовков HTTP для использования в ответе.
* `content_type`: Тип содержимого ответа. Как правило, он устанавливается автоматически рендерером в результате согласования содержимого, но в некоторых случаях может потребоваться явное указание типа содержимого.

---

# Attributes

# Атрибуты

## .data

## .data

The unrendered, serialized data of the response.

Неотредактированные, сериализованные данные ответа.

## .status_code

## .status_code

The numeric status code of the HTTP response.

Цифровой код состояния ответа HTTP.

## .content

## .content

The rendered content of the response. The `.render()` method must have been called before `.content` can be accessed.

Отрисованное содержимое ответа. Метод `.render()` должен быть вызван, прежде чем можно будет получить доступ к `.content`.

## .template_name

## .template_name

The `template_name`, if supplied. Only required if `HTMLRenderer` or some other custom template renderer is the accepted renderer for the response.

Имя `шаблона`, если оно задано. Требуется, только если `HTMLRenderer` или другой пользовательский рендерер шаблона является принятым рендерером для ответа.

## .accepted_renderer

## .accepted_renderer

The renderer instance that will be used to render the response.

Экземпляр рендерера, который будет использоваться для рендеринга ответа.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Устанавливается автоматически `APIView` или `@api_view` непосредственно перед возвратом ответа из представления.

## .accepted_media_type

## .accepted_media_type

The media type that was selected by the content negotiation stage.

Тип носителя, который был выбран на этапе согласования содержимого.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Устанавливается автоматически `APIView` или `@api_view` непосредственно перед возвратом ответа из представления.

## .renderer_context

## .renderer_context

A dictionary of additional context information that will be passed to the renderer's `.render()` method.

Словарь дополнительной контекстной информации, которая будет передана в метод `.render()` рендерера.

Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.

Устанавливается автоматически `APIView` или `@api_view` непосредственно перед возвратом ответа из представления.

---

# Standard HttpResponse attributes

# Стандартные атрибуты HttpResponse

The `Response` class extends `SimpleTemplateResponse`, and all the usual attributes and methods are also available on the response. For example you can set headers on the response in the standard way:

Класс `Response` расширяет `SimpleTemplateResponse`, и все обычные атрибуты и методы также доступны для ответа. Например, вы можете установить заголовки для ответа стандартным способом:

```
response = Response()
response['Cache-Control'] = 'no-cache'
```

## .render()

## .render()

**Signature:** `.render()`

**Подпись:** `.render()`.

As with any other `TemplateResponse`, this method is called to render the serialized data of the response into the final response content. When `.render()` is called, the response content will be set to the result of calling the `.render(data, accepted_media_type, renderer_context)` method on the `accepted_renderer` instance.

Как и любой другой `TemplateResponse`, этот метод вызывается для преобразования сериализованных данных ответа в конечное содержимое ответа. Когда вызывается `.render()`, содержимое ответа будет установлено в результат вызова метода `.render(data, accepted_media_type, renderer_context)` на экземпляре `accepted_renderer`.

You won't typically need to call `.render()` yourself, as it's handled by Django's standard response cycle.

Обычно вам не нужно вызывать `.render()` самостоятельно, так как это обрабатывается стандартным циклом ответа Django.