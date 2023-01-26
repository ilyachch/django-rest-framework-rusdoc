# Урок 1: Сериализация

## Введение

Этот урок будет охватывать создание простого API для хранения и подстветки кода. В процессе вы познакомитесь с различными компонентами, которые составляют основу REST Frameword, и дадут вам полное понимание того, как все соединяется.

Учебное пособие довольно глубоко, поэтому вам, вероятно, стоит взять печенье и чашку вашего любимого напитка перед началом работы. Если вам просто нужен быстрый обзор, вам следует вместо этого перейти к документации [быстрый старт](quickstart.md).

---

**ПРИМЕЧАНИЕ**: Код для этого урока доступен в репозитории [encode/rest-framework-tutorial](https://github.com/encode/rest-framework-tutorial) на github. Завершенная реализация также есть онлайн как песочницы для тестирования, [доступно здесь](https://restframework.herokuapp.com/).

---

## Setting up a new environment

## Настройка нового окружения

Прежде чем мы сделаем что-либо, мы создадим новую виртуальную среду, используя [venv](https://docs.python.org/3/library/venv.html). Это гарантирует, что наша конфигурация пакетов будет хорошо изолирована от любых других проектов, над которыми мы работаем.

```
python3 -m venv env
source env/bin/activate
```

Теперь, когда мы находимся в виртуальной среде, мы можем установить наши зависимости.

```
pip install django
pip install djangorestframework
pip install pygments  # We'll be using this for the code highlighting
```

**Примечание:** Чтобы выйти из виртуальной среды в любое время, просто введите `deactivate`. Для получения дополнительной информации см. [документация VENV](https://docs.python.org/3/library/venv.html).

## Начало

Хорошо, мы готовы писать код. Чтобы начать, давайте создадим новый проект для работы.

```
cd ~
django-admin startproject tutorial
cd tutorial
```

Как только это будет сделано, мы сможем создать приложение, которое мы используем для создания простого веб-API.

```
python manage.py startapp snippets
```

Нам нужно добавить наше новое приложение `snippets` и приложение `rest_framework` в `INSTALLED_APPS`. Давайте отредактируем файл `turnerial/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'snippets',
]
```

Хорошо, мы готовы продложать.

## Создание модели для работы

Для целей этого урока мы собираемся начать с создания простой модели `Snippet`, которая используется для хранения фрагментов кода. Отредактируйте файл `snippets/models.py`. Примечание: хорошие практики программирования включают комментарии. Хотя вы найдете их в нашей версии репозитория этого учебного кода, мы пропустили их здесь, чтобы сосредоточиться на самом коде.

```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
```

Нам также нужно создать начальную миграцию для нашей модели `Snippet` и синхронизировать базу данных.

```
python manage.py makemigrations snippets
python manage.py migrate snippets
```

## Создание класса сериализатора

Первое, что нам нужно, чтобы начать с нашего веб-API, это предоставить способ сериализации и десеризации экземпляров `Snippet` в такие представления, как `json`. Мы можем сделать это, объявив сериализаторы, которые очень похожи на формы Джанго. Создайте файл в каталоге `snippet` с именем `serializers.py` и добавьте следующее.

```python
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```

Первая часть класса Serializer определяет поля, которые будут сериализованы/десериализированы. Методы `create()` и `update()` определяют, как создаются или изменяются экземпляры при вызове `serializer.save()`

Класс сериализатора очень похож на класс Django `Form` и включает в себя аналогичные флаги проверки и параметры в различных полях, такие как `required`, `max_length` и `default`.

Флаги и параметры полей также могут контролировать, как сериализатор должен отображаться в определенных обстоятельствах, например, при отображении в HTML. Параметр `style={'base_template': 'textarea.html'}` в примере выше эквивалентен использованию `widget = widgets.textarea` в классе django `Form`.Это особенно полезно для контроля того, как следует отображать интерфейс API, как мы увидим позже в этом учебнике.

На самом деле мы можем также сохранить себе время, используя класс `ModelSerializer`, как мы увидим позже, но сейчас мы сохраним четкое определение сериализатора.

## Работа с сериализаторами

Прежде чем мы пойдем дальше, мы ознакомьтесь с использованием нашего нового класса сериализатора. Давайте перейдем в оболочку Django.

```
python manage.py shell
```

Хорошо, после того, как мы сделали несколько импортов, давайте создадим пару фрагментов кода для работы.

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()
```

Теперь у нас есть несколько экземпляров `Snippet`, с которыми можно поиграть. Давайте посмотрим на сериализацию одного из этих объектов.

```python
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

На этом этапе мы перевели экземпляр модели в нативные типы данных Python. Чтобы завершить процесс сериализации, мы отобразим данные в виде `json`.

```python
content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```

Десериализация похожа. Сначала мы переведем входящие данные в нативные типы данных Python ...

```python
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```

...Затем мы восстанавливаем эти типы данных в полностью заполненный объект.

```python
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```

Обратите внимание, насколько похожа работа с API на работу с формами. Сходство должно стать еще более очевидным, когда мы начинаем писать представления, которые используют наш сериализатор.

Мы также можем сериализовать запросы вместо экземпляров модели. Для этого мы просто добавляем параметр `many=True` в сериализатор.

```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## Использование ModelSerializers

Наш класс `SnippetSerializer` дублирует много информации, которая также содержится в модели `Snippet`. Было бы неплохо, если бы мы могли оставить наш код более кратким.

Точно так же, как Django предоставляет как классы `Form`, и `ModelForm`, REST Framework включает в себя как классы `Serializer`, `ModelSerializer`.

Давайте отрефакторим наш сериализатор, используя класс `ModelSerializer`. Откройте файл `snippets/serializers.py` и замените класс` SnippetSerializer` на следующее.

```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

Одно приятное свойство, которым обладают сериализаторы, состоит в том, что вы можете увидеть все поля в экземпляре сериализатора, печатая его представление. Откройте оболочку Django с помощью `python manage.py shell` и введите следующее:

```python
from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```

Важно помнить, что классы `ModelSerializer` не делают ничего особенно волшебного, они являются просто синтаксическим сахаром для создания классов сериализатора:

* Автоматически определенный набор полей.
* Простые реализации по умолчанию для методов `create()` и `update()`.

## Написание обычных представлений Django с использованием нашего сериализатора

Давайте посмотрим, как мы можем написать некоторые представления API с помощью нашего нового класса сериализатора. На данный момент мы не будем использовать какие-либо другие функции REST Framework, мы просто напишем представления как обычные представления Django.

Отредактируйте файл `snippets/views.py` и добавьте следующее.

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

Корень нашего API станет представлением, которое поддерживает перечисление всех существующих фрагментов и создание нового фрагмента.

```python
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```

Обратите внимание, что, поскольку мы хотим иметь возможность обрабатывать POST запросы в этом представлении от клиентов, у которых не будет токена CSRF, нам нужно отметить представление как `csrf_exempt`. Это не то, что вы обычно хотели бы делать, и представления REST Framework действительно используют более разумное поведение, чем это, но сейчас нам этого будет достаточно.

Нам также понадобится представление, которое соответствует отдельному фрагменту, и может использоваться для извлечения, обновления или удаления фрагмента.

```python
@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
```

Наконец, нам нужно подключить эти представления. Создайте файл `snippets/urls.py`:

```python
from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]
```

We also need to wire up the root urlconf, in the `tutorial/urls.py` file, to include our snippet app's URLs.

Нам также необходимо подключить корневой urlconf в файле `tutorial/urls.py`, чтобы подключить URL-адреса нашего приложения для фрагмента.

```python
from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
]
```

Стоит отметить, что есть несколько краевых случаев, которые мы не обрабатываем должным образом в настоящее время. Если мы отправим некорректный `json`, или если запрос сделан с помощью метода, который представление не обрабатывает, то мы получим в ответ ошибку сервера 500. Тем не менее, сейчас этого будет достаточно.

## Тестирование нашего первого Web API

Теперь мы можем запустить сервер, который обслуживает наше API.

Уйти из оболочки ...

```
quit()
```

...и запустите локальный сервер разработки Django.

```
python manage.py runserver

Validating models...

0 errors found
Django version 4.0, using settings 'tutorial.settings'
Starting Development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

В другом окне терминала мы можем проверить сервер.

We can test our API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/httpie/httpie#installation). Httpie is a user friendly http client that's written in Python. Let's install that.

Мы можем проверить наш API, используя [curl](https://curl.haxx.se/) или [httpie](https://github.com/httpie/httpie#installation). Httpie - простой HTTP-клиент, написанный на Python. Давайте установим его.

Вы можете установить httpie с помощью PIP:

```
pip install httpie
```

Наконец, мы можем получить список всех фрагментов:

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

Или мы можем получить конкретный фрагмент, ссылаясь на его идентификатор:

```
http http://127.0.0.1:8000/snippets/2/

HTTP/1.1 200 OK
...
{
  "id": 2,
  "title": "",
  "code": "print(\"hello, world\")\n",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}
```

Также, вы можете получить тот же JSON, открыв эти URL-адреса в веб-браузере.

## Что мы имеем на данный момент

До сих пор у нас все в порядке, у нас есть API сериализации, который очень похож на API Django's Forms, и некоторые обычные представления Django.

Наши представления API в данный момент не делают ничего особенного, помимо обработки `json` запросов, нет обработки ошибок, но это уже функционирующий веб-API.

Мы посмотрим, что можно улучшить в [части 2 учебника](2-requests-and-responses.md).
