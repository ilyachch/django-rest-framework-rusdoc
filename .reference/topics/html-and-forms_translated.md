<!-- TRANSLATED by md-translate -->
# HTML & Forms

# Html & forms

REST framework is suitable for returning both API style responses, and regular HTML pages. Additionally, serializers can be used as HTML forms and rendered in templates.

Структура REST подходит для возврата как ответов в стиле API, так и обычных HTML -страниц.
Кроме того, сериализаторы могут использоваться в качестве HTML -форм и отображаться в шаблонах.

## Rendering HTML

## рендеринг HTML

In order to return HTML responses you'll need to use either `TemplateHTMLRenderer`, or `StaticHTMLRenderer`.

Чтобы вернуть ответы HTML, вам нужно использовать либо `templatehtmlrenderer`, либо` statichtmlrenderer`.

The `TemplateHTMLRenderer` class expects the response to contain a dictionary of context data, and renders an HTML page based on a template that must be specified either in the view or on the response.

Класс `Templatehtmlrenderer` ожидает, что ответ содержит словарь данных контекста и отдает HTML -страницу на основе шаблона, который должен быть указан либо в представлении, либо на ответе.

The `StaticHTMLRender` class expects the response to contain a string of the pre-rendered HTML content.

Класс `statichtmlrender` ожидает, что ответ содержит строку предварительно Рендерного содержимого HTML.

Because static HTML pages typically have different behavior from API responses you'll probably need to write any HTML views explicitly, rather than relying on the built-in generic views.

Поскольку статические HTML-страницы обычно имеют отличное поведение от ответов API, вам, вероятно, необходимо явно написать какие-либо виды HTML, а не полагаться на встроенные общие представления.

Here's an example of a view that returns a list of "Profile" instances, rendered in an HTML template:

Вот пример представления, который возвращает список экземпляров «профиля», представленного в шаблоне HTML:

**views.py**:

** views.py **:

```
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

** profile_list.html **:

```
<html><body>
<h1>Profiles</h1>
<ul>
    {% for profile in profiles %}
    <li>{{ profile.name }}</li>
    {% endfor %}
</ul>
</body></html>
```

## Rendering Forms

## рендеринг форм

Serializers may be rendered as forms by using the `render_form` template tag, and including the serializer instance as context to the template.

Сериализаторы могут быть отображены в виде форм с помощью шаблона `render_form` и включать экземпляр сериализатора в качестве контекста для шаблона.

The following view demonstrates an example of using a serializer in a template for viewing and updating a model instance:

Следующее представление демонстрирует пример использования сериализатора в шаблоне для просмотра и обновления экземпляра модели:

**views.py**:

** views.py **:

```
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

** profile_detail.html **:

```
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

### Using template packs

### Использование пакетов шаблонов

The `render_form` tag takes an optional `template_pack` argument, that specifies which template directory should be used for rendering the form and form fields.

Тег `render_form` принимает необязательный аргумент` template_pack`, который указывает, какой каталог шаблонов следует использовать для визуализации полей формы и формы.

REST framework includes three built-in template packs, all based on Bootstrap 3. The built-in styles are `horizontal`, `vertical`, and `inline`. The default style is `horizontal`. To use any of these template packs you'll want to also include the Bootstrap 3 CSS.

Структура REST включает в себя три встроенных пакета шаблонов, все это на основе Bootstrap 3. Встроенные стили-«горизонтальные», «вертикальные» и «inline».
Стиль по умолчанию «горизонтальный».
Чтобы использовать любой из этих пакетов шаблонов, вы захотите включить Bootstrap 3 CSS.

The following HTML will link to a CDN hosted version of the Bootstrap 3 CSS:

Следующий HTML будет ссылаться на CDN, размещенную версию Bootstrap 3 CSS:

```
<head>
    …
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>
```

Third party packages may include alternate template packs, by bundling a template directory containing the necessary form and field templates.

Сторонние пакеты могут включать в себя альтернативные пакеты шаблонов путем объединения каталога шаблонов, содержащего необходимую форму и шаблоны полевых полетов.

Let's take a look at how to render each of the three available template packs. For these examples we'll use a single serializer class to present a "Login" form.

Давайте посмотрим, как отобразить каждый из трех доступных шаблонов.
Для этих примеров мы будем использовать один класс сериализатора, чтобы представить форму «логин».

```
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

#### `rest_framework/vertical`

#### `rest_framework/vertical

Presents form labels above their corresponding control inputs, using the standard Bootstrap layout.

Представляет ярлыки формы над соответствующими входами управления, используя стандартную компоновку Bootstrap.

*This is the default template pack.*

*Это пакет шаблонов по умолчанию.*

```
{% load rest_framework %}

...

<form action="{% url 'login' %}" method="post" novalidate>
    {% csrf_token %}
    {% render_form serializer template_pack='rest_framework/vertical' %}
    <button type="submit" class="btn btn-default">Sign in</button>
</form>
```

![Vertical form example](../img/vertical.png)

! [Пример вертикальной формы] (../ img/vertical.png)

---

#### `rest_framework/horizontal`

#### `rest_framework/horizontal`

Presents labels and controls alongside each other, using a 2/10 column split.

Представляет этикетки и элементы управления рядом друг с другом, используя разделение колонны 2/10.

*This is the form style used in the browsable API and admin renderers.*

*Это стиль формы, используемый в API и администраторах.

```
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

![Horizontal form example](../img/horizontal.png)

! [Горизонтальная форма пример] (../ img/horizontal.png)

---

#### `rest_framework/inline`

#### `rest_framework/inline`

A compact form style that presents all the controls inline.

Стиль компактной формы, который представляет все элементы управления встроенными.

```
{% load rest_framework %}

...

<form class="form-inline" action="{% url 'login' %}" method="post" novalidate>
    {% csrf_token %}
    {% render_form serializer template_pack='rest_framework/inline' %}
    <button type="submit" class="btn btn-default">Sign in</button>
</form>
```

![Inline form example](../img/inline.png)

! [Пример встроенной формы] (../ img/inline.png)

## Field styles

## Полевые стили

Serializer fields can have their rendering style customized by using the `style` keyword argument. This argument is a dictionary of options that control the template and layout used.

Поля сериализатора могут иметь свой стиль рендеринга, настроенный с использованием аргумента ключевого слова «стиль».
Этот аргумент является словарем опций, которые управляют используемым шаблоном и макетом.

The most common way to customize the field style is to use the `base_template` style keyword argument to select which template in the template pack should be use.

Наиболее распространенным способом настройки стиля поля является использование аргумента ключевого слова в стиле `base_template`, чтобы выбрать, какой шаблон в пакете шаблона должен использоваться.

For example, to render a `CharField` as an HTML textarea rather than the default HTML input, you would use something like this:

Например, чтобы отобразить `charfield` как HTML Textarea, а не HTML -ввод по умолчанию, вы бы использовали что -то вроде этого:

```
details = serializers.CharField(
    max_length=1000,
    style={'base_template': 'textarea.html'}
)
```

If you instead want a field to be rendered using a custom template that is *not part of an included template pack*, you can instead use the `template` style option, to fully specify a template name:

Если вместо этого вы хотите, чтобы поле было отобрано, используя пользовательский шаблон, который не является частью включенного пакета шаблонов *, вы можете вместо этого использовать параметр «Шаблон», чтобы полностью указать имя шаблона:

```
details = serializers.CharField(
    max_length=1000,
    style={'template': 'my-field-templates/custom-input.html'}
)
```

Field templates can also use additional style properties, depending on their type. For example, the `textarea.html` template also accepts a `rows` property that can be used to affect the sizing of the control.

Шаблоны поля также могут использовать дополнительные свойства стиля, в зависимости от их типа.
Например, шаблон `textarea.html` также принимает свойство« строк », которое можно использовать для повлиять на размеры

```
details = serializers.CharField(
    max_length=1000,
    style={'base_template': 'textarea.html', 'rows': 10}
)
```

The complete list of `base_template` options and their associated style options is listed below.

Полный список вариантов `base_template` и их связанных вариантов стиля указан ниже.

base_template  | Valid field types  | Additional style options
----|----|----
input.html     | Any string, numeric or date/time field | input_type, placeholder, hide_label, autofocus
textarea.html |  `CharField` | rows, placeholder, hide_label
select.html | `ChoiceField` or relational field types | hide_label
radio.html | `ChoiceField` or relational field types | inline, hide_label
select_multiple.html | `MultipleChoiceField` or relational fields with `many=True` | hide_label
checkbox_multiple.html | `MultipleChoiceField` or relational fields with `many=True` | inline, hide_label
checkbox.html | `BooleanField` | hide_label
fieldset.html | Nested serializer | hide_label
list_fieldset.html | `ListField` or nested serializer with `many=True` |   hide_label

base_template |
Действительные типы поля |
Дополнительные варианты стиля
---- | ---- | ------
input.html |
Любая строка, числовая или поля даты/времени |
input_type, Placeholder, hide_label, AutoFocus
Textarea.html |
`Charfield` |
ряды, заполнитель, hide_label
select.html |
`Choicefield` или реляционные типы поля |
hide_label
Radio.html |
`Choicefield` или реляционные типы поля |
Встроенный, hide_label
select_multiple.html |
`Multiplechoicefield` или реляционные поля с` my in-wry '|
hide_label
CHACEBOX_MULTIPLE.HTML |
`Multiplechoicefield` или реляционные поля с` my in-wry '|
Встроенный, hide_label
Facebox.html |
`Booleanfield` |
hide_label
fieldset.html |
Вложенный сериализатор |
hide_label
list_fieldset.html |
`Listfield` или вложенный сериализатор с` mysome = true` |
hide_label