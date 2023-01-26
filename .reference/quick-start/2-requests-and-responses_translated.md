<!-- TRANSLATED by md-translate -->
# Tutorial 2: Requests and Responses

# Учебник 2: Запросы и ответы

From this point we're going to really start covering the core of REST framework. Let's introduce a couple of essential building blocks.

Начиная с этого момента мы действительно начнем освещать суть фреймворка REST. Давайте представим несколько основных строительных блоков.

## Request objects

## Объекты запроса

REST framework introduces a `Request` object that extends the regular `HttpRequest`, and provides more flexible request parsing. The core functionality of the `Request` object is the `request.data` attribute, which is similar to `request.POST`, but more useful for working with Web APIs.

Фреймворк REST вводит объект `Request`, который расширяет обычный `HttpRequest` и обеспечивает более гибкий разбор запроса. Основной функциональностью объекта `Request` является атрибут `request.data`, который аналогичен `request.POST`, но более полезен для работы с Web API.

```
request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
```

## Response objects

## Объекты реагирования

REST framework also introduces a `Response` object, which is a type of `TemplateResponse` that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.

Рамка REST также вводит объект `Response`, который является типом `TemplateResponse`, который принимает нерендерированное содержимое и использует согласование содержимого для определения правильного типа содержимого для возврата клиенту.

```
return Response(data)  # Renders to content type as requested by the client.
```

## Status codes

## Коды состояния

Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as `HTTP_400_BAD_REQUEST` in the `status` module. It's a good idea to use these throughout rather than using numeric identifiers.

Использование числовых кодов состояния HTTP в представлениях не всегда удобно для чтения, и легко не заметить, если вы ошиблись с кодом ошибки. REST framework предоставляет более явные идентификаторы для каждого кода состояния, такие как `HTTP_400_BAD_REQUEST` в модуле `status`. Хорошая идея - использовать их повсеместно, а не использовать числовые идентификаторы.

## Wrapping API views

## Обертывание представлений API

REST framework provides two wrappers you can use to write API views.

Фреймворк REST предоставляет две обертки, которые можно использовать для написания представлений API.

1. The `@api_view` decorator for working with function based views.
2. The `APIView` class for working with class-based views.

1. Декоратор `@api_view` для работы с представлениями, основанными на функциях.
2. Класс `APIView` для работы с представлениями на основе классов.

These wrappers provide a few bits of functionality such as making sure you receive `Request` instances in your view, and adding context to `Response` objects so that content negotiation can be performed.

Эти обертки предоставляют несколько функциональных возможностей, таких как обеспечение получения экземпляров `Request` в вашем представлении и добавление контекста к объектам `Response`, чтобы можно было выполнить согласование содержимого.

The wrappers also provide behavior such as returning `405 Method Not Allowed` responses when appropriate, and handling any `ParseError` exceptions that occur when accessing `request.data` with malformed input.

Обертки также обеспечивают такое поведение, как возврат ответов `405 Method Not Allowed`, когда это необходимо, и обработку любых исключений `ParseError`, возникающих при доступе к `request.data` с неправильно сформированным вводом.

## Pulling it all together

## Собираем все вместе

Okay, let's go ahead and start using these new components to refactor our views slightly.

Итак, давайте начнем использовать эти новые компоненты, чтобы немного рефакторизовать наши представления.

```
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Our instance view is an improvement over the previous example. It's a little more concise, and the code now feels very similar to if we were working with the Forms API. We're also using named status codes, which makes the response meanings more obvious.

Наше представление экземпляра является улучшенным по сравнению с предыдущим примером. Оно немного лаконичнее, и код теперь очень похож на тот, который мы использовали при работе с Forms API. Мы также используем именованные коды состояния, что делает значения ответов более очевидными.

Here is the view for an individual snippet, in the `views.py` module.

Вот представление для отдельного фрагмента в модуле `views.py`.

```
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

This should all feel very familiar - it is not a lot different from working with regular Django views.

Все это должно казаться очень знакомым - это не сильно отличается от работы с обычными представлениями Django.

Notice that we're no longer explicitly tying our requests or responses to a given content type. `request.data` can handle incoming `json` requests, but it can also handle other formats. Similarly we're returning response objects with data, but allowing REST framework to render the response into the correct content type for us.

Обратите внимание, что мы больше не привязываем наши запросы или ответы к определенному типу содержимого. `request.data` может обрабатывать входящие запросы `json`, но может обрабатывать и другие форматы. Точно так же мы возвращаем объекты ответа с данными, но позволяем REST-фреймворку преобразовать ответ в нужный нам тип содержимого.

## Adding optional format suffixes to our URLs

## Добавление необязательных суффиксов формата к нашим URL-адресам

To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as [http://example.com/api/items/4.json](http://example.com/api/items/4.json).

Чтобы воспользоваться тем, что наши ответы больше не привязаны к одному типу содержимого, давайте добавим поддержку суффиксов формата в наши конечные точки API. Использование суффиксов формата дает нам URL, которые явно ссылаются на определенный формат, и означает, что наш API сможет обрабатывать такие URL, как [http://example.com/api/items/4.json](http://example.com/api/items/4.json).

Start by adding a `format` keyword argument to both of the views, like so.

Начните с добавления аргумента ключевого слова `format` к обоим представлениям, как показано ниже.

```
def snippet_list(request, format=None):
```

and

и

```
def snippet_detail(request, pk, format=None):
```

Now update the `snippets/urls.py` file slightly, to append a set of `format_suffix_patterns` in addition to the existing URLs.

Теперь немного обновите файл `snippets/urls.py`, чтобы добавить набор `format_suffix_patterns` в дополнение к существующим URL.

```
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

We don't necessarily need to add these extra url patterns in, but it gives us a simple, clean way of referring to a specific format.

Нам не обязательно добавлять эти дополнительные шаблоны url, но это дает нам простой и чистый способ ссылаться на определенный формат.

## How's it looking?

## Как это выглядит?

Go ahead and test the API from the command line, as we did in [tutorial part 1](1-serialization.md). Everything is working pretty similarly, although we've got some nicer error handling if we send invalid requests.

Перейдите к тестированию API из командной строки, как мы это делали в [учебнике часть 1](1-serialization.md). Все работает примерно так же, хотя мы получили более удобную обработку ошибок при отправке некорректных запросов.

We can get a list of all of the snippets, as before.

Мы можем получить список всех сниппетов, как и раньше.

```
http http://127.0.0.1:8000/snippets/

HTTP/1.1 200 OK
...
[
  {
    "id": 1,
    "title": "",
    "code": "foo = \"bar\"\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  },
  {
    "id": 2,
    "title": "",
    "code": "print(\"hello, world\")\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  }
]
```

We can control the format of the response that we get back, either by using the `Accept` header:

Мы можем контролировать формат ответа, который мы получаем, либо используя заголовок `Accept`:

```
http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
```

Or by appending a format suffix:

Или путем добавления суффикса формата:

```
http http://127.0.0.1:8000/snippets.json  # JSON suffix
http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
```

Similarly, we can control the format of the request that we send, using the `Content-Type` header.

Аналогично, мы можем контролировать формат отправляемого запроса, используя заголовок `Content-Type`.

```
# POST using form data
http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"

{
  "id": 3,
  "title": "",
  "code": "print(123)",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

# POST using JSON
http --json POST http://127.0.0.1:8000/snippets/ code="print(456)"

{
    "id": 4,
    "title": "",
    "code": "print(456)",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

If you add a `--debug` switch to the `http` requests above, you will be able to see the request type in request headers.

Если вы добавите переключатель `--debug` к вышеуказанным запросам `http`, вы сможете увидеть тип запроса в заголовках запросов.

Now go and open the API in a web browser, by visiting [http://127.0.0.1:8000/snippets/](http://127.0.0.1:8000/snippets/).

Теперь откройте API в веб-браузере, посетив сайт [http://127.0.0.1:8000/snippets/](http://127.0.0.1:8000/snippets/).

### Browsability

### Browsability

Because the API chooses the content type of the response based on the client request, it will, by default, return an HTML-formatted representation of the resource when that resource is requested by a web browser. This allows for the API to return a fully web-browsable HTML representation.

Поскольку API выбирает тип содержимого ответа на основе запроса клиента, он по умолчанию возвращает представление ресурса в формате HTML, когда ресурс запрашивается веб-браузером. Это позволяет API возвращать полностью доступное для веб-браузера представление HTML.

Having a web-browsable API is a huge usability win, and makes developing and using your API much easier. It also dramatically lowers the barrier-to-entry for other developers wanting to inspect and work with your API.

Наличие веб-браузерного API - это огромный выигрыш в удобстве использования, он значительно упрощает разработку и использование вашего API. Это также значительно снижает барьер для входа в систему для других разработчиков, желающих ознакомиться с вашим API и работать с ним.

See the [browsable api](../topics/browsable-api.md) topic for more information about the browsable API feature and how to customize it.

Дополнительную информацию о функции browsable API и ее настройке см. в теме [browsable api](../topics/browsable-api.md).

## What's next?

## Что дальше?

In [tutorial part 3](3-class-based-views.md), we'll start using class-based views, and see how generic views reduce the amount of code we need to write.

В [учебнике часть 3](3-class-based-views.md) мы начнем использовать представления на основе классов и увидим, как общие представления уменьшают количество кода, который нам нужно писать.