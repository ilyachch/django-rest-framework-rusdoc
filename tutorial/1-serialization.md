<!-- TRANSLATED by md-translate -->
# Урок 1: Сериализация

## Введение

В этом уроке мы рассмотрим создание простого Web API с подсветкой кода для фрагментов кода. Попутно будут представлены различные компоненты, составляющие DRF, и вы получите полное представление о том, как все это сочетается друг с другом.

Учебник довольно подробный, поэтому перед началом работы вам, вероятно, стоит взять печенье и выпить чашку любимого напитка. Если вам нужен лишь краткий обзор, лучше обратиться к документации [quickstart](../quickstart.md).

---

**Примечание**: Код для этого руководства доступен в репозитории [encode/rest-framework-tutorial](https://github.com/encode/rest-framework-tutorial) на GitHub. Не стесняйтесь клонировать репозиторий и посмотреть код в действии.

---

## Настройка новой среды

Прежде чем приступить к чему-либо, мы создадим новую виртуальную среду с именем `.venv` с помощью [venv](https://docs.python.org/3/library/venv.html). Это позволит обеспечить полную изоляцию конфигурации нашего пакета от других проектов, над которыми мы работаем.

```bash
python3 -m venv env
source env/bin/activate
```

Теперь, когда мы находимся в виртуальной среде, мы можем установить наши зависимости.

```bash
pip install django
pip install djangorestframework
pip install pygments  # We'll be using this for the code highlighting
```

---

**Совет**: Чтобы выйти из виртуальной среды в любое время, просто введите `deactivate`. Для получения дополнительной информации смотрите [документацию venv](https://docs.python.org/3/library/venv.html).

---

## Начало работы

Итак, мы готовы приступить к кодированию. Чтобы начать, давайте создадим новый проект для работы.

```bash
cd ~
django-admin startproject tutorial
cd tutorial
```

После этого мы можем создать приложение, которое мы будем использовать для создания простого Web API.

```bash
python manage.py startapp snippets
```

Нам нужно добавить наше новое приложение `snippets` и приложение `rest_framework` в `INSTALLED_APPS`. Давайте отредактируем файл `tutorial/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'snippets',
]
```

Хорошо, мы готовы к работе.

## Создание модели для работы

Для целей этого руководства мы начнем с создания простой модели `Snippet`, которая используется для хранения фрагментов кода. Перейдите к редактированию файла `snippets/models.py`. Примечание: Хорошая практика программирования включает комментарии. Хотя вы найдете их в нашей версии этого учебного кода в репозитории, здесь мы их опустили, чтобы сосредоточиться на самом коде.

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
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python', max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
```

Нам также потребуется создать начальную миграцию для нашей модели сниппетов и впервые синхронизировать базу данных.

```bash
python manage.py makemigrations snippets
python manage.py migrate snippets
```

## Создание класса Serializer

Первое, что нам нужно для начала работы над нашим Web API, это обеспечить способ сериализации и десериализации экземпляров сниппетов в такие форматы, как `json`. Мы можем сделать это, объявив сериализаторы, которые работают очень похоже на формы Django. Создайте файл в каталоге `snippets` с именем `serializers.py` и добавьте следующее.

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

В первой части класса сериализатора определяются поля, которые подлежат сериализации/десериализации. Методы `create()` и `update()` определяют, как создаются или изменяются полноценные экземпляры при вызове `serializer.save()`

Класс сериализатора очень похож на класс `Form` в Django и включает аналогичные флаги валидации для различных полей, такие как `required`, `max_length` и `default`.

Флаги полей также могут контролировать, как сериализатор должен отображаться в определенных обстоятельствах, например, при рендеринге в HTML. Флаг `{"base_template": "textarea.html"}` выше эквивалентен использованию `widget=widgets.Textarea` в классе `Form` в Django. Это особенно полезно для управления отображением API просмотра, как мы увидим позже в этом руководстве.

На самом деле мы также можем сэкономить время, используя класс `ModelSerializer`, как мы увидим позже, но пока что оставим определение нашего сериализатора явным.

## Работа с сериализаторами

Прежде чем двигаться дальше, мы ознакомимся с использованием нашего нового класса Serializer. Давайте зайдем в оболочку Django.

```bash
python manage.py shell
```

Хорошо, раз мы уже разобрались с импортами, давайте создадим пару фрагментов кода, с которыми будем работать.

```pycon
>>> from snippets.models import Snippet
>>> from snippets.serializers import SnippetSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser

>>> snippet = Snippet(code='foo = "bar"\n')
>>> snippet.save()

>>> snippet = Snippet(code='print("hello, world")\n')
>>> snippet.save()
```

Теперь у нас есть несколько экземпляров фрагментов, с которыми можно поработать.  Давайте посмотрим, как сериализовать один из этих экземпляров.

```pycon
>>> serializer = SnippetSerializer(snippet)
>>> serializer.data
{'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

На данном этапе мы преобразовали экземпляр модели в нативные типы данных Python. Чтобы завершить процесс сериализации, мы преобразуем данные в формат `json`.

```pycon
>>> content = JSONRenderer().render(serializer.data)
>>> content
b'{'id':2,'title':'','code':'print(\\"hello, world\\")\\n','linenos':false,'language':'python','style':'friendly'}'
```

Десериализация происходит аналогичным образом. Сначала мы преобразуем поток данных в нативные типы данных Python...

```pycon
>>> import io
>>> stream = io.BytesIO(content)
>>> data = JSONParser().parse(stream)
```

...затем мы восстанавливаем эти встроенные типы данных в экземпляр объекта с заполненными данными.

```pycon
>>> serializer = SnippetSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
{'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}
>>> serializer.save()
<Snippet: Snippet object>
```

Обратите внимание, насколько этот API похож на работу с формами.  Это сходство станет ещё более очевидным, когда мы начнём писать представления, использующие наш сериализатор.

Мы также можем сериализовать наборы записей вместо экземпляров моделей.  Для этого достаточно просто добавить флаг `many=True` в аргументы сериализатора.

```pycon
>>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
>>> serializer.data
[{'id': 1, 'title': '', 'code': 'foo = "bar"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
```

## Использование сериализаторов моделей

Наш класс `SnippetSerializer` дублирует большую часть информации, которая уже содержится в модели `Snippet`. Было бы неплохо сделать наш код немного лаконичнее.

Точно так же, как Django предоставляет как классы `Form`, так и классы `ModelForm`, REST Framework включает в себя как классы `Serializer`, так и классы `ModelSerializer`.

Давайте посмотрим, как можно рефакторировать наш сериализатор с помощью класса `ModelSerializer`. Снова откройте файл `snippets/serializers.py` и замените класс `SnippetSerializer` следующим кодом.

```python
from rest_framework import serializers
from snippets.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

Одной из удобных особенностей сериализаторов является то, что вы можете просмотреть все поля экземпляра сериализатора, выведя его представление. Откройте оболочку Django с помощью команды `python manage.py shell`, а затем попробуйте выполнить следующее:

```pycon
>>> from snippets.serializers import SnippetSerializer
>>> serializer = SnippetSerializer()
>>> print(repr(serializer))
SnippetSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(allow_blank=True, max_length=100, required=False)
    code = CharField(style={'base_template': 'textarea.html'})
    linenos = BooleanField(required=False)
    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
```

Важно помнить, что классы `ModelSerializer` не обладают какими-то особыми волшебными свойствами — они просто представляют собой удобный способ создания классов сериализаторов:

* Автоматически определяемый набор полей.
* Простые реализации по умолчанию для методов `create()` и `update()`.

## Написание обычных представлений Django с использованием нашего сериализатора

Давайте посмотрим, как можно создать несколько представлений API с помощью нашего нового класса `Serializer`. Пока что мы не будем использовать другие возможности REST Framework, а просто напишем эти представления как обычные представления Django.

Отредактируйте файл `snippets/views.py` и добавьте следующее.

```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

Корнем нашего API будет представление, которое поддерживает вывод списка всех существующих сниппетов или создание нового сниппета.

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

Обратите внимание: поскольку мы хотим, чтобы клиенты, не имеющие токена CSRF, могли отправлять запросы POST в этот вид, нам необходимо пометить его как `csrf_exempt`. Обычно это не рекомендуется, и виды в REST Framework на самом деле используют более разумное поведение, но в данный момент для наших целей этого будет достаточно.

Нам также понадобится представление, соответствующее отдельному фрагменту, с помощью которого можно будет извлекать, обновлять или удалять этот фрагмент.

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

Нам также нужно настроить корневой urlconf в файле `tutorial/urls.py`, чтобы включить в нее URL нашего приложения-фрагмента.

```python
from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
]
```

Стоит отметить, что есть несколько крайних случаев, которые мы не обрабатываем должным образом в настоящее время. Если мы отправим неверно сформированный `json`, или если запрос будет сделан с методом, который представление не обрабатывает, то мы получим ответ 500 "ошибка сервера". Тем не менее это пока сойдет.

## Тестирование нашей первой попытки создания Web API

Теперь мы можем запустить отладочный сервер, который будет обслуживать наши фрагменты.

Выйти из оболочки...

```pycon
>>> quit()
```

...и запустите сервер разработки Django.

```bash
python manage.py runserver

Validating models...

0 errors found
Django version 5.0, using settings 'tutorial.settings'
Starting Development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

В другом окне терминала мы можем протестировать сервер.

Мы можем протестировать наш API с помощью [curl](https://curl.haxx.se/) или [HTTPie](https://github.com/httpie/httpie#installation). HTTPie — это удобный HTTP-клиент, написанный на Python. Давайте его установим.

Вы можете установить HTTPie с помощью pip:

```bash
pip install httpie
```

Наконец, мы можем получить список всех сниппетов:

```bash
http GET http://127.0.0.1:8000/snippets/ --unsorted

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
    },
    {
        "id": 3,
        "title": "",
        "code": "print(\"hello, world\")",
        "linenos": false,
        "language": "python",
        "style": "friendly"
    }
]
```

Или мы можем получить конкретный фрагмент, обратившись к нему по id:

```bash
http GET http://127.0.0.1:8000/snippets/2/ --unsorted

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

Аналогично, вы можете получить тот же json, посетив эти URL-адреса в веб-браузере.

## Где мы сейчас

Пока что у нас все в порядке, у нас есть API сериализации, который очень похож на Django Forms API, и несколько обычных представлений Django.

Наши представления API на данный момент не делают ничего особенного, кроме как обслуживают `json` ответы, и есть несколько крайних случаев обработки ошибок, которые мы хотели бы убрать, но это функционирующий Web API.

В [части 2 учебника](2-requests-and-responses.md) мы посмотрим, как можно начать улучшать ситуацию.
