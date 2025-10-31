<!-- TRANSLATED by md-translate -->
# Учебник 2: Запросы и ответы

Начиная с этого момента мы действительно начнем освещать суть DRF. Давайте представим несколько основных строительных блоков.

## Объекты запроса

DRF вводит объект `Request`, который расширяет обычный `HttpRequest` и обеспечивает более гибкий разбор запроса. Основной функциональностью объекта `Request` является атрибут `request.data`, который аналогичен `request.POST`, но более полезен для работы с Web API.

```python
request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
```

## Объекты ответа

DRF также вводит объект `Response`, который является типом `TemplateResponse`, который принимает неотрендерреное содержимое и использует согласование содержимого для определения правильного типа содержимого для возврата клиенту.

```python
return Response(data)  # Renders to content type as requested by the client.
```

## Коды состояния

Использование числовых кодов состояния HTTP в представлениях не всегда удобно для чтения, и легко не заметить, если вы ошиблись с кодом ошибки. DRF предоставляет более явные идентификаторы для каждого кода состояния, такие как `HTTP_400_BAD_REQUEST` в модуле `status`. Хорошая идея - использовать их повсеместно, а не использовать числовые идентификаторы.

## Оборачивание представлений API

DRF предоставляет две обертки, которые можно использовать для написания представлений API.

1. Декоратор `@api_view` для работы с представлениями, основанными на функциях.
2. Класс `APIView` для работы с представлениями на основе классов.

Эти обертки предоставляют несколько функциональных возможностей, таких как обеспечение получения экземпляров `Request` в вашем представлении и добавление контекста к объектам `Response`, чтобы можно было выполнить согласование содержимого.

Обертки также обеспечивают такое поведение, как возврат ответов `405 Method Not Allowed`, когда это необходимо, и обработку любых исключений `ParseError`, возникающих при доступе к `request.data` с неправильно сформированным вводом.

## Собираем все вместе

Итак, давайте начнем использовать эти новые компоненты, чтобы немного отрефакторить наши представления.

```python
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

Наше представление экземпляра улучшилось по сравнению с предыдущим примером. Оно немного лаконичнее, и код теперь очень похож на тот, который мы использовали при работе с Forms API. Мы также используем именованные коды состояния, что делает значения ответов более очевидными.

Вот представление для отдельного фрагмента в модуле `views.py`.

```python
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

Все это должно казаться очень знакомым - это не сильно отличается от работы с обычными представлениями Django.

Обратите внимание, что мы больше не привязываем наши запросы или ответы к определенному типу содержимого. `request.data` может обрабатывать входящие запросы `json`, но может обрабатывать и другие форматы. Точно так же мы возвращаем объекты ответа с данными, но позволяем DRF преобразовать ответ в нужный нам тип содержимого.

## Добавление необязательных суффиксов формата к нашим URL-адресам

Чтобы воспользоваться тем, что наши ответы больше не привязаны к одному типу содержимого, давайте добавим поддержку суффиксов формата в наши конечные точки API. Использование суффиксов формата дает нам URL, которые явно ссылаются на определенный формат, и означает, что наш API сможет обрабатывать такие URL, как [<http://example.com/api/items/4.json>](http://example.com/api/items/4.json).

Начните с добавления именованного аргумента `format` к обоим представлениям, как показано ниже.

```python
def snippet_list(request, format=None):
```

и

```python
def snippet_detail(request, pk, format=None):
```

Теперь немного обновите файл `snippets/urls.py`, чтобы добавить набор `format_suffix_patterns` в дополнение к существующим URL.

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Нам необязательно добавлять эти дополнительные шаблоны url, но это дает нам простой и чистый способ ссылаться на определенный формат.

## Как это выглядит?

Перейдите к тестированию API из командной строки, как мы это делали в [учебнике часть 1](1-serialization.md). Все работает примерно так же, хотя мы получили более удобную обработку ошибок при отправке некорректных запросов.

Мы можем получить список всех сниппетов, как и раньше.

```bash
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

Мы можем контролировать формат ответа, который мы получаем, либо используя заголовок `Accept`:

```bash
http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
```

Либо путем добавления суффикса формата:

```bash
http http://127.0.0.1:8000/snippets.json  # JSON suffix
http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
```

Аналогично, мы можем контролировать формат отправляемого запроса, используя заголовок `Content-Type`.

```bash
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

Если вы добавите переключатель `--debug` к вышеуказанным запросам `http`, вы сможете увидеть тип запроса в заголовках запросов.

Теперь откройте API в веб-браузере, посетив [<http://127.0.0.1:8000/snippets/>](http://127.0.0.1:8000/snippets/).

### Возможность просмотра

Поскольку API выбирает тип содержимого ответа на основе запроса клиента, он по умолчанию возвращает представление ресурса в формате HTML, когда ресурс запрашивается веб-браузером. Это позволяет API возвращать полностью доступное для веб-браузера представление HTML.

Наличие browsable API - это огромный выигрыш в удобстве использования, он значительно упрощает разработку и использование вашего API. Это также значительно снижает барьер для входа в систему для других разработчиков, желающих ознакомиться с вашим API и работать с ним.

Дополнительную информацию о функции browsable API и ее настройке см. в теме [browsable api](../topics/browsable-api.md).

## Что дальше?

В [уроке 3](3-class-based-views.md) мы начнем использовать представления на основе классов и увидим, как общие представления уменьшают количество кода, который нам нужно писать.
