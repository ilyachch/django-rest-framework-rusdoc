<!-- TRANSLATED by md-translate -->
# HTML и формы

REST framework подходит для возврата как ответов в стиле API, так и обычных HTML-страниц. Кроме того, сериализаторы могут использоваться в качестве HTML-форм и отображаться в шаблонах.

## Рендеринг HTML

Для возврата HTML-ответов вам нужно использовать либо `TemplateHTMLRenderer`, либо `StaticHTMLRenderer`.

Класс `TemplateHTMLRenderer` ожидает, что ответ будет содержать словарь данных контекста, и создает HTML-страницу на основе шаблона, который должен быть указан либо в представлении, либо в ответе.

Класс `StaticHTMLRender` ожидает, что ответ будет содержать строку предварительно отрендеренного HTML-содержимого.

Поскольку поведение статических HTML-страниц обычно отличается от поведения ответов API, вам, вероятно, придется писать любые HTML-представления явно, а не полагаться на встроенные типовые представления.

Вот пример представления, которое возвращает список экземпляров "Profile", отображенный в шаблоне HTML:

**views.py**:

```python
from my_project.example.models import Profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'

    def get(self, request):
        queryset = Profile.objects.all()
        return Response({'profiles': queryset})
```

**profile_list.html**:

```html
<html><body>
<h1>Profiles</h1>
<ul>
    {% for profile in profiles %}
    <li>{{ profile.name }}</li>
    {% endfor %}
</ul>
</body></html>
```

## Рендеринг форм

Сериализаторы можно отображать в виде форм, используя тег шаблона `render_form` и включая экземпляр сериализатора в качестве контекста в шаблон.

Следующее представление демонстрирует пример использования сериализатора в шаблоне для просмотра и обновления экземпляра модели:

**views.py**:

```python
from django.shortcuts import get_object_or_404
from my_project.example.models import Profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')
```

**profile_detail.html**:

```html
{% load rest_framework %}

<html><body>

<h1>Profile - {{ profile.name }}</h1>

<form action="{% url 'profile-detail' pk=profile.pk %}" method="POST">
    {% csrf_token %}
    {% render_form serializer %}
    <input type="submit" value="Save">
</form>

</body></html>
```

### Использование пакетов шаблонов

Тег `render_form` принимает необязательный аргумент `template_pack`, который указывает, какой каталог шаблонов должен использоваться для рендеринга формы и полей формы.

REST framework включает три встроенных пакета шаблонов, все они основаны на Bootstrap 3. Встроенные стили: `horizontal`, `vertical` и `inline`. По умолчанию используется стиль `horizontal`. Чтобы использовать любой из этих пакетов шаблонов, вам необходимо также включить CSS Bootstrap 3.

Следующий HTML будет ссылаться на версию CSS Bootstrap 3, размещенную в CDN:

```html
<head>
    …
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>
```

Сторонние пакеты могут включать альтернативные пакеты шаблонов, в которые входит каталог шаблонов, содержащий необходимые шаблоны форм и полей.

Давайте рассмотрим, как визуализировать каждый из трех доступных пакетов шаблонов. В этих примерах мы будем использовать один класс сериализатора для представления формы "Вход в систему".

```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()
```

---

#### `rest_framework/vertical`.

Представляет ярлыки формы над соответствующими входами элементов управления, используя стандартный макет Bootstrap.

*Это пакет шаблонов по умолчанию.*

```html
{% load rest_framework %}

...

<form action="{% url 'login' %}" method="post" novalidate>
    {% csrf_token %}
    {% render_form serializer template_pack='rest_framework/vertical' %}
    <button type="submit" class="btn btn-default">Sign in</button>
</form>
```

![Пример вертикальной формы](https://github.com/encode/django-rest-framework/blob/master/docs/img/vertical.png?raw=true)

---

#### `rest_framework/horizontal`.

Представляет ярлыки и элементы управления рядом друг с другом, используя разделение колонок 2/10.

*Это стиль формы, используемый в просматриваемых API и администраторских рендерах.*

```html
{% load rest_framework %}

...

<form class="form-horizontal" action="{% url 'login' %}" method="post" novalidate>
    {% csrf_token %}
    {% render_form serializer %}
    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
            <button type="submit" class="btn btn-default">Sign in</button>
        </div>
    </div>
</form>
```

![Пример горизонтальной формы](https://github.com/encode/django-rest-framework/blob/master/docs/img/horizontal.png?raw=true)

---

#### `rest_framework/inline`.

Компактный стиль формы, который представляет все элементы управления в линию.

```html
{% load rest_framework %}

...

<form class="form-inline" action="{% url 'login' %}" method="post" novalidate>
    {% csrf_token %}
    {% render_form serializer template_pack='rest_framework/inline' %}
    <button type="submit" class="btn btn-default">Sign in</button>
</form>
```

![Пример инлайн-формы](https://github.com/encode/django-rest-framework/blob/master/docs/img/inline.png?raw=true)

## Стили полей

Поля сериализатора могут иметь свой стиль рендеринга, настроенный с помощью аргумента ключевого слова `style`. Этот аргумент представляет собой словарь опций, которые управляют используемым шаблоном и макетом.

Наиболее распространенным способом настройки стиля поля является использование ключевого аргумента стиля `base_template`, чтобы выбрать, какой шаблон из пакета шаблонов следует использовать.

Например, чтобы отобразить `CharField` как HTML textarea, а не как HTML input по умолчанию, вы должны использовать что-то вроде этого:

```python
details = serializers.CharField(
    max_length=1000,
    style={'base_template': 'textarea.html'}
)
```

Если вы хотите, чтобы поле отображалось с использованием пользовательского шаблона, который *не является частью включенного пакета шаблонов*, вы можете использовать опцию стиля `template`, чтобы полностью указать имя шаблона:

```python
details = serializers.CharField(
    max_length=1000,
    style={'template': 'my-field-templates/custom-input.html'}
)
```

Шаблоны полей также могут использовать дополнительные свойства стиля, в зависимости от их типа. Например, шаблон `textarea.html` также принимает свойство `rows`, которое можно использовать для изменения размера элемента управления.

```python
details = serializers.CharField(
    max_length=1000,
    style={'base_template': 'textarea.html', 'rows': 10}
)
```

Полный список опций `base_template` и связанных с ними опций стиля приведен ниже.

| base_template          | Правильные типы полей                                    | Дополнительные параметры стиля                   |
| ---------------------- | -------------------------------------------------------- | ------------------------------------------------ |
| input.html             | Любое строковое, числовое или поле даты/времени          | input_type, placeholder, hide_label, autofocus   |
| textarea.html          | `CharField`                                              | rows, placeholder, hide_label                    |
| select.html            | `ChoiceField` или типы реляционных полей                 | hide_label                                       |
| radio.html             | `ChoiceField` или реляционные типы поля                  | inline, hide_label                               |
| select_multiple.html   | `MultipleChoiceField` или реляционные поля с `many=True` | hide_label                                       |
| checkbox_multiple.html | `MultipleChoiceField` или реляционные поля с `many=True` | inline, hide_label                               |
| checkbox.html          | `BooleanField`                                           | hide_label                                       |
| fieldset.html          | Вложенный сериализатор                                   | hide_label                                       |
| list_fieldset.html     | `ListField` или вложенный сериализатор с `many=True`     | hide_label                                       |
