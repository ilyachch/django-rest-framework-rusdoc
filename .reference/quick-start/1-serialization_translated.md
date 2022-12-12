<!-- TRANSLATED by md-translate -->
# Tutorial 1: Serialization

# Учебник 1: сериализация

## Introduction

## Введение

This tutorial will cover creating a simple pastebin code highlighting Web API. Along the way it will introduce the various components that make up REST framework, and give you a comprehensive understanding of how everything fits together.

Этот урок будет охватывать создание простого кода Pastebin, выделяющего веб -API.
По пути он представит различные компоненты, которые составляют основу для отдыха, и даст вам полное понимание того, как все соединяется.

The tutorial is fairly in-depth, so you should probably get a cookie and a cup of your favorite brew before getting started. If you just want a quick overview, you should head over to the [quickstart](quickstart.md) documentation instead.

Учебное пособие довольно глубоко, поэтому вы, вероятно, должны получить печенье и чашку вашего любимого варева перед началом работы.
Если вам просто нужен быстрый обзор, вам следует вместо этого перейти к документации [QuickStart] (QuickStart.md).

---

**Note**: The code for this tutorial is available in the [encode/rest-framework-tutorial](https://github.com/encode/rest-framework-tutorial) repository on GitHub. The completed implementation is also online as a sandbox version for testing, [available here](https://restframework.herokuapp.com/).

** ПРИМЕЧАНИЕ **: Код для этого урока доступен в [Encode/Rest-Framework-tutorial] (https://github.com/encode/rest-framework-tutorial) на github.
Завершенная реализация также онлайн как версия для тестирования песочницы, [доступно здесь] (https://restframework.herokuapp.com/).

---

## Setting up a new environment

## Настройка новой среды

Before we do anything else we'll create a new virtual environment, using [venv](https://docs.python.org/3/library/venv.html). This will make sure our package configuration is kept nicely isolated from any other projects we're working on.

Прежде чем мы сделаем что -нибудь еще, мы создадим новую виртуальную среду, используя [venv] (https://docs.python.org/3/library/venv.html).
Это убедится, что наша конфигурация пакета будет хорошо изолирована от любых других проектов, над которыми мы работаем.

```
python3 -m venv env
source env/bin/activate
```

Now that we're inside a virtual environment, we can install our package requirements.

Теперь, когда мы находимся в виртуальной среде, мы можем установить наши требования к пакетам.

```
pip install django
pip install djangorestframework
pip install pygments  # We'll be using this for the code highlighting
```

**Note:** To exit the virtual environment at any time, just type `deactivate`. For more information see the [venv documentation](https://docs.python.org/3/library/venv.html).

** Примечание: ** Чтобы выйти из виртуальной среды в любое время, просто введите `deactivate`.
Для получения дополнительной информации см. [Документация VENV] (https://docs.python.org/3/library/venv.html).

## Getting started

## Начиная

Okay, we're ready to get coding. To get started, let's create a new project to work with.

Хорошо, мы готовы получить кодирование.
Чтобы начать, давайте создадим новый проект для работы.

```
cd ~
django-admin startproject tutorial
cd tutorial
```

Once that's done we can create an app that we'll use to create a simple Web API.

Как только это будет сделано, мы сможем создать приложение, которое мы используем для создания простого веб -API.

```
python manage.py startapp snippets
```

We'll need to add our new `snippets` app and the `rest_framework` app to `INSTALLED_APPS`. Let's edit the `tutorial/settings.py` file:

Нам нужно добавить наше новое приложение `Snippets` и приложение` rest_framework` в `staded_apps`.
Давайте отредактируем файл `turnerial/settings.py`:

```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'snippets',
]
```

Okay, we're ready to roll.

Хорошо, мы готовы катиться.

## Creating a model to work with

## Создание модели для работы с

For the purposes of this tutorial we're going to start by creating a simple `Snippet` model that is used to store code snippets. Go ahead and edit the `snippets/models.py` file. Note: Good programming practices include comments. Although you will find them in our repository version of this tutorial code, we have omitted them here to focus on the code itself.

Для целей этого урока мы собираемся начать с создания простой модели «фрагмента», которая используется для хранения фрагментов кода.
Идите вперед и отредактируйте файл `Snippets/Models.py`.
Примечание: хорошие методы программирования включают комментарии.
Хотя вы найдете их в нашей версии репозитория этого учебного кода, мы пропустили их здесь, чтобы сосредоточиться на самом коде.

```
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

We'll also need to create an initial migration for our snippet model, and sync the database for the first time.

Нам также нужно создать начальную миграцию для нашей модели фрагмента и впервые синхронизировать базу данных.

```
python manage.py makemigrations snippets
python manage.py migrate snippets
```

## Creating a Serializer class

## Создание класса сериализатора

The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the snippet instances into representations such as `json`. We can do this by declaring serializers that work very similar to Django's forms. Create a file in the `snippets` directory named `serializers.py` and add the following.

Первое, что нам нужно, чтобы начать с нашего веб -API, - это предоставить способ сериализации и десеризации экземпляров фрагмента в такие представления, как «json».
Мы можем сделать это, объявив сериалы, которые очень похожи на формы Джанго.
Создайте файл в каталоге «Snippets» с именем `serializers.py` и добавьте следующее.

```
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

The first part of the serializer class defines the fields that get serialized/deserialized. The `create()` and `update()` methods define how fully fledged instances are created or modified when calling `serializer.save()`

Первая часть класса Serializer определяет поля, которые сериализованы/десериализированы.
Методы `create ()` и `update ()` определяют, насколько полностью создаются экземпляры или изменены при вызове `serializer.save ()`

A serializer class is very similar to a Django `Form` class, and includes similar validation flags on the various fields, such as `required`, `max_length` and `default`.

Класс сериализатора очень похож на класс Django `form` и включает в себя аналогичные флаги проверки в различных полях, таких как` required`, `max_length` и` default`.

The field flags can also control how the serializer should be displayed in certain circumstances, such as when rendering to HTML. The `{'base_template': 'textarea.html'}` flag above is equivalent to using `widget=widgets.Textarea` on a Django `Form` class. This is particularly useful for controlling how the browsable API should be displayed, as we'll see later in the tutorial.

Полевые флаги также могут контролировать, как сериализатор должен отображаться в определенных обстоятельствах, например, когда приведено в HTML.
`{'Base_template': 'textarea.html'}` флаг выше эквивалентен использованию `widget = widgets.textarea` в классе django` form`.
Это особенно полезно для контроля того, как следует отображать API, который можно найти, как мы увидим позже в учебном пособии.

We can actually also save ourselves some time by using the `ModelSerializer` class, as we'll see later, but for now we'll keep our serializer definition explicit.

На самом деле мы можем также сохранить себя некоторое время, используя класс «ModelseRializer», как мы увидим позже, но сейчас мы сохраним четкое определение сериализатора.

## Working with Serializers

## Работа с сериализаторами

Before we go any further we'll familiarize ourselves with using our new Serializer class. Let's drop into the Django shell.

Прежде чем мы пойдем дальше, мы ознакомьтесь с использованием нашего нового класса сериализатора.
Давайте бросим в оболочку Джанго.

```
python manage.py shell
```

Okay, once we've got a few imports out of the way, let's create a couple of code snippets to work with.

Хорошо, как только у нас есть несколько импорта, давайте создадим пару фрагментов кода для работы.

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()
```

We've now got a few snippet instances to play with. Let's take a look at serializing one of those instances.

Теперь у нас есть несколько экземпляров фрагмента, с которыми можно играть.
Давайте посмотрим на сериализацию одного из этих случаев.

```
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```

At this point we've translated the model instance into Python native datatypes. To finalize the serialization process we render the data into `json`.

На этом этапе мы перевели экземпляр модели в нативные данные Python.
Чтобы завершить процесс сериализации, мы переводим данные в `json '.

```
content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```

Deserialization is similar. First we parse a stream into Python native datatypes...

Десериализация похожа.
Сначала мы проанализируем поток в народные дата дата Python ...

```
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```

...then we restore those native datatypes into a fully populated object instance.

... Затем мы восстанавливаем эти собственные данные дата в полностью населенный экземпляр объекта.

```
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```

Notice how similar the API is to working with forms. The similarity should become even more apparent when we start writing views that use our serializer.

Обратите внимание, насколько похож API для работы с формами.
Сходство должно стать еще более очевидным, когда мы начинаем писать представления, которые используют наш сериализатор.

We can also serialize querysets instead of model instances. To do so we simply add a `many=True` flag to the serializer arguments.

Мы также можем сериализовать запросы вместо экземпляров модели.
Для этого мы просто добавляем флаг `много = true` в аргументы сериализатора.

```
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```

## Using ModelSerializers

## Использование моделейализаторов

Our `SnippetSerializer` class is replicating a lot of information that's also contained in the `Snippet` model. It would be nice if we could keep our code a bit more concise.

Наш класс «Snippetserializer» воспроизводит много информации, которая также содержится в модели «фрагмент».
Было бы неплохо, если бы мы могли сохранить наш код более кратким.

In the same way that Django provides both `Form` classes and `ModelForm` classes, REST framework includes both `Serializer` classes, and `ModelSerializer` classes.

Точно так же, как Django предоставляет как классы «формы», так и классы «Modelform», Framework REST включает в себя как классы «сериализатора», так и классы `modelerializer.

Let's look at refactoring our serializer using the `ModelSerializer` class. Open the file `snippets/serializers.py` again, and replace the `SnippetSerializer` class with the following.

Давайте посмотрим на рефакторинг нашего сериализатора, используя класс `modelerializer.
Откройте файл `Snippets/Serializers.py` снова и замените класс` Snippetserializer` на следующее.

```
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

One nice property that serializers have is that you can inspect all the fields in a serializer instance, by printing its representation. Open the Django shell with `python manage.py shell`, then try the following:

Одно приятное свойство, которое обладает сериалами, состоит в том, что вы можете осмотреть все поля в экземпляре сериализатора, печатая его представление.
Откройте оболочку Django с помощью `python Manage.py Shell`, затем попробуйте следующее:

```
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

It's important to remember that `ModelSerializer` classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:

Важно помнить, что классы «Modelerializer» не делают ничего особенно волшебного, они являются просто ярлыком для создания классов сериализатора:

* An automatically determined set of fields.
* Simple default implementations for the `create()` and `update()` methods.

* Автоматически определенный набор полей.
* Простые реализации по умолчанию для методов `create ()` и `update ()`.

## Writing regular Django views using our Serializer

## Написание обычных просмотров Django с использованием нашего сериализатора

Let's see how we can write some API views using our new Serializer class. For the moment we won't use any of REST framework's other features, we'll just write the views as regular Django views.

Давайте посмотрим, как мы можем написать некоторые представления API с помощью нашего нового класса сериализатора.
На данный момент мы не будем использовать какие -либо другие функции REST Framework, мы просто напишем представления в качестве обычных просмотров Django.

Edit the `snippets/views.py` file, and add the following.

Отредактируйте файл `Snippets/Views.py` и добавьте следующее.

```
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
```

The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.

Корень нашего API станет представлением, которая поддерживает перечисление всех существующих фрагментов или создание нового фрагмента.

```
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

Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as `csrf_exempt`. This isn't something that you'd normally want to do, and REST framework views actually use more sensible behavior than this, but it'll do for our purposes right now.

Обратите внимание, что, поскольку мы хотим иметь возможность публиковать в этом представлении от клиентов, у которых не будет токена CSRF, нам нужно отметить представление как `csrf_exept`.
Это не то, что вы обычно хотели бы делать, и представления REST Framework действительно используют более разумное поведение, чем это, но это будет делать для наших целей прямо сейчас.

We'll also need a view which corresponds to an individual snippet, and can be used to retrieve, update or delete the snippet.

Нам также понадобится представление, которое соответствует отдельному фрагменту, и может использоваться для извлечения, обновления или удаления фрагмента.

```
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

Finally we need to wire these views up. Create the `snippets/urls.py` file:

Наконец, нам нужно подключить эти виды.
Создайте файл `Snippets/urls.py`:

```
from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]
```

We also need to wire up the root urlconf, in the `tutorial/urls.py` file, to include our snippet app's URLs.

Нам также необходимо подключить корневой urlConf в файле `turniorm/urls.py`, чтобы включить URL -адреса нашего приложения для фрагмента.

```
from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
]
```

It's worth noting that there are a couple of edge cases we're not dealing with properly at the moment. If we send malformed `json`, or if a request is made with a method that the view doesn't handle, then we'll end up with a 500 "server error" response. Still, this'll do for now.

Стоит отметить, что есть несколько краевых случаев, с которыми мы сейчас не имеем дело должным образом.
Если мы отправим Malformed `json`, или если запрос сделан с помощью метода, который представление не обрабатывает, то мы получим ответ на ошибку сервера 500.
Тем не менее, это пока подойдет.

## Testing our first attempt at a Web API

## тестирование нашей первой попытки веб -API

Now we can start up a sample server that serves our snippets.

Теперь мы можем запустить образец сервера, который обслуживает наши фрагменты.

Quit out of the shell...

Уйти из раковины ...

```
quit()
```

...and start up Django's development server.

... и запустите сервер разработки Django.

```
python manage.py runserver

Validating models...

0 errors found
Django version 4.0, using settings 'tutorial.settings'
Starting Development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

In another terminal window, we can test the server.

В другом окне терминала мы можем проверить сервер.

We can test our API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/httpie/httpie#installation). Httpie is a user friendly http client that's written in Python. Let's install that.

Мы можем проверить наш API, используя [curl] (https://curl.haxx.se/) или [httpie] (https://github.com/httpie/httpie#installation).
Httpie - удобный для пользователя HTTP -клиент, который написан на Python.
Давайте установим это.

You can install httpie using pip:

Вы можете установить httpie с помощью PIP:

```
pip install httpie
```

Finally, we can get a list of all of the snippets:

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

Or we can get a particular snippet by referencing its id:

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

Similarly, you can have the same json displayed by visiting these URLs in a web browser.

Точно так же вы можете отобразить тот же JSON, посещая эти URL -адреса в веб -браузере.

## Where are we now

## Где мы сейчас

We're doing okay so far, we've got a serialization API that feels pretty similar to Django's Forms API, and some regular Django views.

До сих пор у нас все в порядке, у нас есть сериализационный API, который очень похож на API Django's Forms, и некоторые обычные взгляды Django.

Our API views don't do anything particularly special at the moment, beyond serving `json` responses, and there are some error handling edge cases we'd still like to clean up, but it's a functioning Web API.

Наши представления API в данный момент не делают ничего особенного, помимо службы «JSON», и есть некоторые случаи обработки ошибок, которые мы все еще хотели бы очистить, но это функционирующий веб -API.

We'll see how we can start to improve things in [part 2 of the tutorial](2-requests-and-responses.md).

Мы посмотрим, как мы сможем начать улучшать вещи в [Часть 2 учебника] (2-re-responses.md).