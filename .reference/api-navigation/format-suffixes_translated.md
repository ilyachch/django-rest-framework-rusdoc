<!-- TRANSLATED by md-translate -->
---

source:
    - urlpatterns.py

источник:
- urlpatterns.py

---

# Format suffixes

# Формат суффиксы

> Section 6.2.1 does not say that content negotiation should be

> Раздел 6.2.1 не говорит, что переговоры о контенте должны быть

used all the time.

использовал все время.

>
>
> &mdash; Roy Fielding, [REST discuss mailing list](http://tech.groups.yahoo.com/group/rest-discuss/message/5857)

>
>
> & mdash;
Рой Филдинг, [REST DISCED DISCEAL LISHING] (http://tech.groups.yahoo.com/group/rest-discuss/message/5857)

A common pattern for Web APIs is to use filename extensions on URLs to provide an endpoint for a given media type.  For example, 'http://example.com/api/users.json' to serve a JSON representation.

Общим шаблоном для веб -API является использование расширений имени файла на URL -адресах, чтобы обеспечить конечную точку для данного типа носителя.
Например, 'http://example.com/api/users.json', чтобы служить представлению JSON.

Adding format-suffix patterns to each individual entry in the URLconf for your API is error-prone and non-DRY, so REST framework provides a shortcut to adding these patterns to your URLConf.

Добавление шаблонов Format-Suffix к каждой отдельной записи в URLConf для вашего API является подверженным ошибкам и не сухим, поэтому структура REST обеспечивает ярлык для добавления этих шаблонов в ваш URLConf.

## format_suffix_patterns

## format_suffix_patterns

**Signature**: format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)

** Подпись **: format_suffix_patterns (urlpatterns, суффикс_ареал = false, разрешен = нет)

Returns a URL pattern list which includes format suffix patterns appended to each of the URL patterns provided.

Возвращает список шаблонов URL, который включает в себя шаблоны суффиксов формата, добавленные к каждому из предоставленных шаблонов URL.

Arguments:

Аргументы:

* **urlpatterns**: Required.  A URL pattern list.
* **suffix_required**:  Optional.  A boolean indicating if suffixes in the URLs should be optional or mandatory.  Defaults to `False`, meaning that suffixes are optional by default.
* **allowed**:  Optional.  A list or tuple of valid format suffixes.  If not provided, a wildcard format suffix pattern will be used.

*** urlpatterns **: требуется.
Список рисунков URL.
*** Суффикс_Рикл **: необязательно.
Логический, указывающий, должны ли суффиксы в URL -адресах быть необязательными или обязательными.
По умолчанию «false», что означает, что суффиксы являются необязательными по умолчанию.
*** разрешено **: необязательно.
Список или кортеж действительных суффиксов формата.
Если не предоставлено, будет использоваться шаблон суффикса формата подстановочного знака.

Example:

Пример:

```
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views

urlpatterns = [
    path('', views.apt_root),
    path('comments/', views.comment_list),
    path('comments/<int:pk>/', views.comment_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
```

When using `format_suffix_patterns`, you must make sure to add the `'format'` keyword argument to the corresponding views.  For example:

При использовании `format_suffix_patterns` вы должны убедиться, что в соответствующих представлениях есть аргумент ключевого слова« Format ».
Например:

```
@api_view(['GET', 'POST'])
def comment_list(request, format=None):
    # do stuff...
```

Or with class-based views:

Или с классовыми взглядами:

```
class CommentList(APIView):
    def get(self, request, format=None):
        # do stuff...

    def post(self, request, format=None):
        # do stuff...
```

The name of the kwarg used may be modified by using the `FORMAT_SUFFIX_KWARG` setting.

Имя используемого Kwarg может быть изменено с помощью настройки `format_suffix_kwarg`.

Also note that `format_suffix_patterns` does not support descending into `include` URL patterns.

Также обратите внимание, что `format_suffix_patterns` не поддерживает спуск в` include` url -шаблоны.

### Using with `i18n_patterns`

### с помощью `i18n_patterns`

If using the `i18n_patterns` function provided by Django, as well as `format_suffix_patterns` you should make sure that the `i18n_patterns` function is applied as the final, or outermost function. For example:

При использовании функции `i18n_patterns`, предоставленной Django, а также` format_suffix_patterns`, вы должны убедиться, что функция `i18n_patterns 'применяется как конечная или внешняя функция.
Например:

```
urlpatterns = [
    …
]

urlpatterns = i18n_patterns(
    format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
)
```

---

## Query parameter formats

## Форматы параметров запроса

An alternative to the format suffixes is to include the requested format in a query parameter. REST framework provides this option by default, and it is used in the browsable API to switch between differing available representations.

Альтернативой корматным суффиксам является включение запрошенного формата в параметр запроса.
Framework REST предоставляет эту опцию по умолчанию, и он используется в API -файлах для просмотра для переключения между различными доступными представлениями.

To select a representation using its short format, use the `format` query parameter. For example: `http://example.com/organizations/?format=csv`.

Чтобы выбрать представление, используя его короткий формат, используйте параметр запроса `format '.
Например: `http: //example.com/organizations/? Format = csv`.

The name of this query parameter can be modified using the `URL_FORMAT_OVERRIDE` setting. Set the value to `None` to disable this behavior.

Имя этого параметра запроса можно изменить с помощью настройки `url_format_override`.
Установите значение «Нет», чтобы отключить это поведение.

---

## Accept headers vs. format suffixes

## Принять заголовки против корматных суффиксов

There seems to be a view among some of the Web community that filename extensions are not a RESTful pattern, and that `HTTP Accept` headers should always be used instead.

Похоже, что среди некоторых веб -сообщества есть мнение о том, что расширения имени файла не являются спокойным шаблоном, и что вместо этого следует использовать заголовки http Accept`.

It is actually a misconception.  For example, take the following quote from Roy Fielding discussing the relative merits of query parameter media-type indicators vs. file extension media-type indicators:

Это на самом деле заблуждение.
Например, возьмите следующую цитату от Роя Филдинга, обсуждая относительные достоинства показателей параметров Mediy-Type по сравнению с индикаторами расширения среднего типа:

&ldquo;That's why I always prefer extensions.  Neither choice has anything to do with REST.&rdquo; &mdash; Roy Fielding, [REST discuss mailing list](https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/14844)

& ldquo; вот почему я всегда предпочитаю расширения.
Ни один выбор не имеет ничего общего с отдыхом. & Rdquo;
& mdash;
Рой Филдинг, [REST DISCED DISCEAL LISHING] (https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/14844)

The quote does not mention Accept headers, but it does make it clear that format suffixes should be considered an acceptable pattern.

В цитате не упоминается принять заголовки, но она дает понять, что суффиксы формата следует считать приемлемым шаблоном.