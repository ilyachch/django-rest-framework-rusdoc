# Урок 1: Сериализация

## Введение

В данном руководстве вы узнаете как создать простое Web-приложение для хранения сниппетов. В процессе мы расскажем про различные компоненты, из которых состоит DRF и дадим полное понимание, как все части работают вместе.

Руководство достаточно подробное, так что если вы хотите только поверхностный обзор, воспользуйтесь руководством по [быстрому старту](quick-start.md).

Важно: код данного руководства доступен на репозитории [tomchristie/rest-framework-tutorial](https://github.com/encode/rest-framework-tutorial) на GitHub. Готовая реализация так же доступна [здесь](http://restframework.herokuapp.com/).

## Настройка нового окружения

Прежде чем что-то начать делать, мы должны создать новое виртуальное окружение. Это изолирует среду выполнения от остальных проектов

```bash
virtualenv env
source env/bin/activate    # Для Windows envScriptsactivate
```

Теперь мы в виртуальном окружении и можем установить наши зависимости.

```bash
pip install django
pip install djangorestframework
pip install pygments  # Мы будем использовать это для подсветки синтаксиса
```

Важно: для выхода из виртуального окружения достаточно выполнить команду `deactivate`. Для более полной информации читайте [документацию virtualenv](http://www.virtualenv.org/en/latest/index.html).

## Начинаем

Для начала давайте создадим новый проект, с которым нам предстоит работать.

```bash
cd ~
django-admin.py startproject tutorial
cd tutorial
```

Создав проект, мы можем создать приложение, в котором мы будем создавать Web API.

```bash
python manage.py startapp snippets
```

Для продолжения работы мы должны добавить наше новое приложение snippets и `rest_framework` в секцию `INSTALLED_APPS`. Измените модуль `settings.py`:

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
    'snippets',
)

```

## Создание модели для работы

Для целей данного руководства мы начнем с создания простой модели `Snippet`, которая будет использоваться для хранения блоков кода(Сниппетов).

```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)
```

Так же нам необходимо сделать начальную миграцию для данной модели и синхронизировать базу данных. 


```bash
python manage.py makemigrations snippets
python manage.py migrate
```

## Создание класса сериализатора

Первая вещь, которую нам надо сделать для нашего API, это создать способ сериализации и десериализации объектов модели `Snippet` в такие формы, как, например, JSON. Мы можем сделать это описав сериализатор и работать с ним подобно тому, как мы работаем с Django формами.

Создайте модуль `serializers.py` в пакете `snippets`.

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

Первая часть класса сериализатора определяет поля, которые будут сериализованы/десериализованы. Методы `create()` и `update()` определяют, как работает создание и обновление объекта модели.

Класс сериализатора очень похож на класс формы в Django и включает такие же проверочные механизмы на различные поля, такие как `requireq`, `max_length`, `default`.

Параметры полей так же могут управлять тем, как сериализатор должен бтыь отображен в различных обстоятельствах, таких, как рендеринг HTML. Параметр `{'base_template': 'textarea.html'}` походит на определение виджета в поле формы Django. Это полезно для контроля за тем, как браузерная версия API будет отображаться, что мы пронаблюдаем дальше.

Так же мы можем сохранить время, использовав класс `ModelSerializer`, применение которого будет показано позже, а пока мы оставим описание нашего сериализатора развернутым.

## Работа с Сериализаторами

Прежде чем двигаться дальше, давайте освоимся с классом `Serializer`. Для этого перейдем в консоль Django.

```bash
python manage.py shell
```

Теперь нам необходимо импортировать несколько пакетов. Так же давайте сделаем пару сниппетов, с которыми будем работать.

```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"n')
snippet.save()

snippet = Snippet(code='print "hello, world"n')
snippet.save()
```

Теперь у нас есть несколько объектов `Snippet`, с которыми мы можем поиграть. Давайте посмотрим на сериализацию одного из объектов.

```python
serializer = SnippetSerializer(snippet)
serializer.data

# {'id': 2, 'title': u'', 'code': u'print "hello, world"n', 'linenos': False, 'language': u'python', 'style': u'friendly'}
```

Сейчас мы перевели объект модели во встроенные типы данных Python. Для завершения сериализации мы сформируем из этих данных JSON.

```python
content = JSONRenderer().render(serializer.data)
content

# '{"id": 2, "title": "", "code": "print "hello, world"n", "linenos": false, "language": "python", "style": "friendly"}'
```

Десериализация - подобна сериализации. Сначала мы парсим данные во встроенные типы данных Python.

```python
from io import BytesIO

stream = BytesIO(content)
data = JSONParser().parse(stream)
```

Затем переводим эти данные в полностью сформированный объект.

```python
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print "hello, world"n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>;
```

Обратите внимание, насколько похожа работа с API на работу с формами. Эта схожесть должна стать более заметной, когда мы начнем писать представления, использующие наш сериализатор.

Так же мы можем сериализовать запрос(`Queryset`), а не отдельный объект модели. для этого необходимо добавить параметр `many=True` в аргументы сериализатора.

```python
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data

# [OrderedDict([('id', 1), ('title', u''), ('code', u'foo = "bar"n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', u''), ('code', u'print "hello, world"n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', u''), ('code', u'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## Использование модельных сериализаторов

Наш класс `SnippetSerializer` дублирует множество информации, которую уже содержит модель `Snippet`. Было бы не плохо, если бы мы могли оставлять наш код кратким.

Так же, как Django предоставляет классы `Form` и `ModelForm`, DRF предоставляет классы `Serializer` и `ModelSerializer`.

Давайте перепишем наш класс сериализатора, используя класс `ModelSerializer`. Для этого перейдите в модуль `snippets/serializers.py` и измените код, как описано ниже.

```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```

У сериализаторов есть одно интересное свойство - вы можете узнать все поля в объекта сериализатора, выведя его представление. Чтобы попробовать это, откройте консоль Django и выполните следующее:

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

Важно помнить, что класс ModelSerializer не делает ничего магического. Это всего лишь синтаксический сахар для создания классов сериализаторов:
1. Автоматически определяет набор полей;
2. Простая и стандартная реализация методов create() и update().

## Создание стандартных Django представлений используя сериализатор

Давайте посмотрим, как мы можем написать несколько представлений API, используя наш новый класс `Serializer`. На данный момент мы не будем использовать возможности, предоставляемые DRF, мы просто напишем обычные Django представления.

Для этого откройте `snippets/views.py` и добавьте следующее:

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

Корнем нашего API должно быть представление, которое поддерживает вывод всех существующих сниппетов, а так же создание новых.

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

Помните, что, поскольку мы хотим использовать POST запрос в данном представлении от клиентов, у которых не будет CSRF токена, необходимо добавить декоратор `csrf_exempt`. Это, конечно, не то, что бы вы стали делать в нормальных условиях, но в текущих условиях, этого будет достаточно.

Так же нам нужно представление, которое обрабатывает отдельный сниппет и позволяет получаеть, обновлять и удалять сниппет.

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

В конце, мы должны привязать данные представления. Создайте `snippets/urls.py` со следующим содержимым:  

```python
from django.conf.urls import url
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
```

Так же мы должны привязать данный диспетчер URL к корневому. Для этого зайдите в `urls.py` и подключите URL диспетчер нашего приложения:

```python
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('snippets.urls')),
]
```

Ничего страшного в том, что есть несколько непродуманных моментов. Например, если мы пришлем неправильно сформированный JSON, или если запрос будет сделан с помощью метода, не поддерживаемого представлением, мы получим ошибку 500 'Server error'. Однако, пока нам этого достаточно.

## Пытаемся обратиться к Web API

Теперь мы можем запустить сервер и поработать с нашими сниппетами.

Выйдите из консоли Django...

```python
quit()
```

...и запустите сервер Django.

```bash
python manage.py runserver

Validating models...
0 errors found

Django version 1.11, using settings 'tutorial.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
In another terminal window, we can test the server.
```

Мы можем протестировать наше API использя `curl` или `httpie`. `Httpie` - дружественный http клиент, написанный на Python.

Вы можете установить `httpie` использя `pip`:

```bash
pip install httpie
```

Теперь мы, наконец, можем получить список всех сниппетов:

```bash
http http://127.0.0.1:8000/snippets/

HTTP/1.1 200 OK
...
[
  {
    "id": 1,
    "title": "",
    "code": "foo = "bar"n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  },
  {
    "id": 2,
    "title": "",
    "code": "print "hello, world"n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  }
]
```

Или мы можем получить отдельный сниппет, запросив его по id:

```bash
http http://127.0.0.1:8000/snippets/2/

HTTP/1.1 200 OK
...
{
  "id": 2,
  "title": "",
  "code": "print "hello, world"n",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}
```

Так же вы можете увидеть тот же JSON, перейдя по вышеуказанному [адресу](http://127.0.0.1:8000/snippets/2/) в браузере.

## Итак, где мы сейчас

Итак, у нас есть API, которое очень походит на Django форму и несколько обычных Django представлений.

Наше API не будет делать ничего особенного, кроме вывода json ответов, а так же у нас есть ошибки при обработке тех или иных запросов, но это уже работающее API.

Как это все улучшить, мы увидим в [уроке 2](request-response.md) этого руководства.
