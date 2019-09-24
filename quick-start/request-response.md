# Урок 2: Запросы и ответы

С этого момента мы начнем изучать ядро DRF. Давайте рассмотрим пару основных блоков.

## Объект запроса

DRF использует объект `Request`, расширяющий функционал стандартного `HttpRequest` и позволяющий более гибко разбирать запросы. Основной функицонал `Request` в том, что он предоставляет аттрибут `request.data`, который схож с `request.POST`, однако более полезен при работе с API.

```py
request.POST  # Содрежит только данные из формы.  Работает только с методом POST.
request.data  # Обрабатывает произвольные данные.  Работает с POST, PUT и PATCH методами.
```

## Объект ответа

Также DRF предоставляет объект Response, являющийся расширением TemplateResponse, который берет сырые данные и использует их для определения и формирование правильного типа контента, возвращаемого клиенту.

```py
return Response(data)  # Формирует тип ответа, согласно запросу клиента.
```

## Коды статусов

Использование числовых кодов HTTP статуса в ваших представлениях не всегда очевидно и легко пропустить место, где была допущена ошибка. DRF предоставляет более явные идентификаторы для каждого кода статуса, такие как `HTTP_400_BAD_REQUEST` в модуле `status`. Мы рекомендуем использовать их, а не числовые коды.

## Обертка представлений 

DRF предоставляет два способа обозначения представлений API:
- декоратор `@api_view` для работы с представлениями-функциями;
- класс `APIView` для наследования при работе с представлениями-классами.

Эти способы обозначения добавляют некоторый функционал в представления. Например, они всегда преобразуют запрос в объект `Request`, или добавляют контекст в объект `Response`, чтобы можно было согласовать контент. 

Так же они предоставляют такой функционал, как возврат `405 Method Not Allowed` ответа, когда надо и обработка ошибок `ParseError`, когда данные в `request.data` неверно сформированы.

## Собираем все вместе

Давайте начнем использовать эти компоненты, чтобы написать несколько представлений.

Мы больше не нуждаемся в классе `JSONResponse` в модуле `views.py`, так что можно его удалить. Когда это будет сделано, мы можем продолжить переписывать наши представления.

```py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all snippets, or create a new snippet.
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

Это более корректное описание нашего представления. Теперь оно более понятно и код стал больше походить на то, как мы работаем с формами. Также мы используем коды статусов, что делает код более наглядным.

Здесь у нас предствление отдельного сниппета. 

```py
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
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

Это не должно быть слишком сложным для понимания - оно практически не отличается от работы с обычными Django представлениями.

Обратите внимание, что мы больше не привязываем наши запросы и ответы к определенному типу контента. `Request.data` может обрабатывать входящие запросы как в формате json, так и в других форматах. Точно так же мы возвращаем объекты `Response` с данными, но позволяем DRF формировать данные в правильный тип.

## Добавление определителей формата в URL

Чтобы использовать премущество, что наши представления больше не привязаны к одному формату данных, давайте добавим поддержку определителей формата. Используя эти определители мы можем сообщать представлениям, какой формат данных мы от них ожидаем. Это позволит нам использовать URL-ы такого вида http://example.com/api/items/4.json.

Начем с того, что добавим именованный параметр к нашим представлениям
```py
def snippet_list(request, format=None):
```

и

```py
def snippet_detail(request, pk, format=None):
```

Теперь необходимо обновить `urls.py`, добавив `format_suffix_patterns` в дополнение к уже имеющимся представлениям.

```py
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Нам не нужно добавлять еще один параметр URL - у нас есть возможность просто и аккуратно сослаться на необходимый формат.

## Как это выглядит

Проверьте работу API из командной строки, как это делалось в [Уроке 1](serialization.md). Все работает одинаково, при этом мы получили улучшеную обработку ошибок в случае отправки неверных запросов.

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
    "code": "print \"hello, world\"\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  }
]
```
Мы можем управлять форматом ответа, используя заголовок `Accept`:

```
http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
```

Или с помощью добавления в конец суффикса формата:

```
http http://127.0.0.1:8000/snippets.json  # JSON Формат
http http://127.0.0.1:8000/snippets.api   # Формат браузерной версии API
```

Так же мы можем управлять форматом запроса, который мы отправили, используя заголовок `Content-Type`.

```py
# POST запрос используя данные формы
http --form POST http://127.0.0.1:8000/snippets/ code="print 123"

{
  "id": 3,
  "title": "",
  "code": "print 123",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

# POST запрос используя JSON
http --json POST http://127.0.0.1:8000/snippets/ code="print 456"

{
    "id": 4,
    "title": "",
    "code": "print 456",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

Если вы используете ключ `--debug`, вы сможете увидеть тип запроса в заголовках запроса. 

А теперь откройте браузер и пройдите по адресу [http://127.0.0.1:8000/snippets/](http://127.0.0.1:8000/snippets/).

## Браузерная версия

Поскольку API выбирает тип ответа, основываясь на запросе клиента, оно будет, по умолчанию, возвращать HTML версию запрашиваемого ресурса, когда запрос будет просиходить из браузера. Это позволяет API формировать полностью браузерную версию данных.

Иметь браузерную версию API - огромное преимущество, поскольку значительно облегчает разработку. Также, это снижает порог входа в разработку как разрабатывающим API, так и разрабатывающим клиенты на основе этого API.

<!-- See the browsable api topic for more information about the browsable API feature and how to customize it. -->
## Что дальше?

В [уроке 3](class-based-views.md), мы будем использовать представления-классы(class-based views, CBV) и посмотрим, как встроенные представления уменьшат количесво необходимого кода.
