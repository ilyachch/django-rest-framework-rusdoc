<!-- TRANSLATED by md-translate -->
---

source:

источник:

* urlpatterns.py

* urlpatterns.py

---

# Format suffixes

# Форматировать суффиксы

> Section 6.2.1 does not say that content negotiation should be used all the time.
>
> — Roy Fielding, [REST discuss mailing list](http://tech.groups.yahoo.com/group/rest-discuss/message/5857)

> В разделе 6.2.1 не говорится, что согласование содержания должно использоваться постоянно.
>
> - Рой Филдинг, [список рассылки REST discuss](http://tech.groups.yahoo.com/group/rest-discuss/message/5857)

A common pattern for Web APIs is to use filename extensions on URLs to provide an endpoint for a given media type. For example, 'http://example.com/api/users.json' to serve a JSON representation.

Общим шаблоном для веб-интерфейсов является использование расширений имен файлов в URL-адресах для предоставления конечной точки для данного типа носителя. Например, 'http://example.com/api/users.json' для предоставления представления JSON.

Adding format-suffix patterns to each individual entry in the URLconf for your API is error-prone and non-DRY, so REST framework provides a shortcut to adding these patterns to your URLConf.

Добавление шаблонов суффиксов формата к каждой отдельной записи в URLconf для вашего API чревато ошибками и не соответствует стандарту DRY, поэтому REST framework предоставляет быстрый способ добавления этих шаблонов в URLConf.

## format_suffix_patterns

## format_suffix_patterns

**Signature**: format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)

**Подпись**: format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)

Returns a URL pattern list which includes format suffix patterns appended to each of the URL patterns provided.

Возвращает список шаблонов URL, который включает шаблоны суффиксов формата, добавленные к каждому из предоставленных шаблонов URL.

Arguments:

Аргументы:

* **urlpatterns**: Required. A URL pattern list.
* **suffix_required**: Optional. A boolean indicating if suffixes in the URLs should be optional or mandatory. Defaults to `False`, meaning that suffixes are optional by default.
* **allowed**: Optional. A list or tuple of valid format suffixes. If not provided, a wildcard format suffix pattern will be used.

* **urlpatterns**: Требуется. Список шаблонов URL.
* **suffix_required**: Необязательно. Булево значение, указывающее, должны ли суффиксы в URL быть необязательными или обязательными. По умолчанию `False`, что означает, что суффиксы по умолчанию необязательны.
* **разрешено**: Необязательно. Список или кортеж допустимых суффиксов формата. Если не указан, будет использоваться шаблон суффикса формата.

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

When using `format_suffix_patterns`, you must make sure to add the `'format'` keyword argument to the corresponding views. For example:

При использовании `format_suffix_patterns`, вы должны убедиться, что добавили аргумент ключевого слова `'format'` в соответствующие представления. Например:

```
@api_view(['GET', 'POST'])
def comment_list(request, format=None):
    # do stuff...
```

Or with class-based views:

Или с помощью взглядов, основанных на классах:

```
class CommentList(APIView):
    def get(self, request, format=None):
        # do stuff...

    def post(self, request, format=None):
        # do stuff...
```

The name of the kwarg used may be modified by using the `FORMAT_SUFFIX_KWARG` setting.

Имя используемого kwarg можно изменить с помощью параметра `FORMAT_SUFFIX_KWARG`.

Also note that `format_suffix_patterns` does not support descending into `include` URL patterns.

Также обратите внимание, что `format_suffix_patterns` не поддерживает спуск к шаблонам URL `include`.

### Using with `i18n_patterns`

### Использование с `i18n_patterns`.

If using the `i18n_patterns` function provided by Django, as well as `format_suffix_patterns` you should make sure that the `i18n_patterns` function is applied as the final, or outermost function. For example:

При использовании функции `i18n_patterns`, предоставляемой Django, а также `format_suffix_patterns` вы должны убедиться, что функция `i18n_patterns` применяется как конечная, или крайняя функция. Например:

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

Альтернативой суффиксам формата является включение запрашиваемого формата в параметр запроса. Фреймворк REST предоставляет этот параметр по умолчанию, и он используется в просматриваемом API для переключения между различными доступными представлениями.

To select a representation using its short format, use the `format` query parameter. For example: `http://example.com/organizations/?format=csv`.

Чтобы выбрать представление по его краткому формату, используйте параметр запроса `format`. Например: `http://example.com/organizations/?format=csv`.

The name of this query parameter can be modified using the `URL_FORMAT_OVERRIDE` setting. Set the value to `None` to disable this behavior.

Имя этого параметра запроса можно изменить с помощью параметра `URL_FORMAT_OVERRIDE`. Установите значение `None`, чтобы отключить это поведение.

---

## Accept headers vs. format suffixes

## Принимать заголовки против суффиксов формата

There seems to be a view among some of the Web community that filename extensions are not a RESTful pattern, and that `HTTP Accept` headers should always be used instead.

Похоже, некоторые представители веб-сообщества считают, что расширения имен файлов не являются шаблоном RESTful, и что вместо них всегда следует использовать заголовки `HTTP Accept`.

It is actually a misconception. For example, take the following quote from Roy Fielding discussing the relative merits of query parameter media-type indicators vs. file extension media-type indicators:

На самом деле это заблуждение. Например, возьмем следующую цитату Роя Филдинга, обсуждающего относительные достоинства индикаторов медиатипа параметров запроса по сравнению с индикаторами медиатипа расширений файлов:

“That's why I always prefer extensions. Neither choice has anything to do with REST.” — Roy Fielding, [REST discuss mailing list](https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/14844)

"Вот почему я всегда предпочитаю удлинители. Ни тот, ни другой выбор не имеют никакого отношения к REST". - Рой Филдинг, [Список рассылки REST discuss](https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/14844)

The quote does not mention Accept headers, but it does make it clear that format suffixes should be considered an acceptable pattern.

В цитате не упоминаются заголовки Accept, но она ясно дает понять, что суффиксы формата следует считать приемлемым шаблоном.