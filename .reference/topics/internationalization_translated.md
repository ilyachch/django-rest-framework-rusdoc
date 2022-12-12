<!-- TRANSLATED by md-translate -->
# Internationalization

# Интернационализация

> Supporting internationalization is not optional. It must be a core feature.
>
> &mdash; [Jannis Leidel, speaking at Django Under the Hood, 2015](https://youtu.be/Wa0VfS2q94Y).

> Поддержка интернационализации не является обязательной.
Это должно быть основной функцией.
>
> & mdash;
[Джаннис Лейдель, выступая в Django под капюшоном, 2015] (https://youtu.be/wa0vfs2q94y).

REST framework ships with translatable error messages. You can make these appear in your language enabling [Django's standard translation mechanisms](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

Структура REST сочетается с переводящими сообщениями об ошибках.
Вы можете сделать это на вашем языке, позволяя [стандартные механизмы перевода Django] (https://docs.djangoproject.com/en/stable/topics/i18n/translation).

Doing so will allow you to:

Это позволит вам:

* Select a language other than English as the default, using the standard `LANGUAGE_CODE` Django setting.
* Allow clients to choose a language themselves, using the `LocaleMiddleware` included with Django. A typical usage for API clients would be to include an `Accept-Language` request header.

* Выберите язык, отличный от английского в качестве по умолчанию, используя стандартную настройку `language_code` django.
* Позвольте клиентам выбирать язык сами, используя «Localemiddleware», включенную в Django.
Типичным использованием для клиентов API было бы включить заголовок запроса «принять».

## Enabling internationalized APIs

## включение интернационализированных API

You can change the default language by using the standard Django `LANGUAGE_CODE` setting:

Вы можете изменить язык по умолчанию, используя стандартную настройку django `language_code`:

```
LANGUAGE_CODE = "es-es"
```

You can turn on per-request language requests by adding `LocalMiddleware` to your `MIDDLEWARE` setting:

Вы можете включить запросы на языковые запросы, добавив «LocalMiddleware» в свою настройку «промежуточное программное обеспечение»:

```
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware'
]
```

When per-request internationalization is enabled, client requests will respect the `Accept-Language` header where possible. For example, let's make a request for an unsupported media type:

При включении интернационализации для первого рассмотрения, запросы клиентов будут уважать заголовок «Принятия», где это возможно.
Например, давайте сделаем запрос на неподдерживаемый тип носителя:

**Request**

**Запрос**

```
GET /api/users HTTP/1.1
Accept: application/xml
Accept-Language: es-es
Host: example.org
```

**Response**

**Ответ**

```
HTTP/1.0 406 NOT ACCEPTABLE

{"detail": "No se ha podido satisfacer la solicitud de cabecera de Accept."}
```

REST framework includes these built-in translations both for standard exception cases, and for serializer validation errors.

Структура REST включает в себя эти встроенные переводы как для стандартных случаев исключения, так и для ошибок проверки сериализатора.

Note that the translations only apply to the error strings themselves. The format of error messages, and the keys of field names will remain the same. An example `400 Bad Request` response body might look like this:

Обратите внимание, что переводы применимы только к самим строкам ошибок.
Формат сообщений об ошибках, а клавиши имен полей останутся прежними.
Пример `400 Bad Predch 'Body ответа может выглядеть следующим образом:

```
{"detail": {"username": ["Esse campo deve ser único."]}}
```

If you want to use different string for parts of the response such as `detail` and `non_field_errors` then you can modify this behavior by using a [custom exception handler](../api-guide/exceptions.md#custom-exception-handling).

Если вы хотите использовать другую строку для частей ответа, такие как `detail` и` non_field_errors
-умение обращаться).

#### Specifying the set of supported languages.

#### Определение набора поддерживаемых языков.

By default all available languages will be supported.

По умолчанию все доступные языки будут поддерживаться.

If you only wish to support a subset of the available languages, use Django's standard `LANGUAGES` setting:

Если вы хотите только поддержать подмножество доступных языков, используйте стандартную настройку Django «Языки»:

```
LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
```

## Adding new translations

## Добавление новых переводов

REST framework translations are managed online using [Transifex](https://www.transifex.com/projects/p/django-rest-framework/). You can use the Transifex service to add new translation languages. The maintenance team will then ensure that these translation strings are included in the REST framework package.

Переводы Framework Framework управляются онлайн с использованием [transifex] (https://www.transifex.com/projects/p/django-rest-framework/).
Вы можете использовать сервис Transifex для добавления новых языков перевода.
Затем команда по техническому обслуживанию гарантирует, что эти строки перевода включены в пакет Framework.

Sometimes you may need to add translation strings to your project locally. You may need to do this if:

Иногда вам может потребоваться добавить строки перевода в свой проект на местном уровне.
Вам может придется сделать это, если:

* You want to use REST Framework in a language which has not been translated yet on Transifex.
* Your project includes custom error messages, which are not part of REST framework's default translation strings.

* Вы хотите использовать структуру отдыха на языке, который еще не был переведен на Transifex.
* Ваш проект включает в себя пользовательские сообщения об ошибках, которые не являются частью строк перевода по умолчанию REST Framework.

#### Translating a new language locally

#### Перевод нового языка локально

This guide assumes you are already familiar with how to translate a Django app.  If you're not, start by reading [Django's translation docs](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

Это руководство предполагает, что вы уже знакомы с тем, как перевести приложение Django.
Если нет, начните с чтения [Django's Translation Docs] (https://docs.djangoproject.com/en/stable/topics/i18n/translation).

If you're translating a new language you'll need to translate the existing REST framework error messages:

Если вы переводите новый язык, вам нужно перевести существующие сообщения об ошибках Framework:

1. Make a new folder where you want to store the internationalization resources. Add this path to your [`LOCALE_PATHS`](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-LOCALE_PATHS) setting.
2. Now create a subfolder for the language you want to translate. The folder should be named using [locale name](https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name) notation. For example: `de`, `pt_BR`, `es_AR`.
3. Now copy the [base translations file](https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_US/LC_MESSAGES/django.po) from the REST framework source code into your translations folder.
4. Edit the `django.po` file you've just copied, translating all the error messages.
5. Run `manage.py compilemessages -l pt_BR` to make the translations

1. Сделайте новую папку, где вы хотите хранить ресурсы интернационализации.
Добавьте этот путь к вашей [`` locale_paths`] (https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-locale_paths).
2. Теперь создайте подпапку для языка, который вы хотите перевести.
Папка должна быть названа с помощью [locale name] (https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name).
Например: `de`,` pt_br`, `es_ar`.
3. Теперь скопируйте [Файл базовых переводов] (https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_us/lc_messages/django.po) из исходного кода Framework Framewour
ваша папка переводов.
4. Измените файл `django.po`, который вы только что скопировали, переведя все сообщения об ошибках.
5. Запустите `Manage.py Compilemessages -l PT_BR`, чтобы сделать переводы

available for Django to use. You should see a message like `processing file django.po in <...>/locale/pt_BR/LC_MESSAGES`.

Доступно для Django для использования.
Вы должны увидеть сообщение, например, `обработка файла django.po в <...>/locale/pt_br/lc_messages`.

6. Restart your development server to see the changes take effect.

6. Перезагрузите сервер разработки, чтобы увидеть, как изменения вступают в силу.

If you're only translating custom error messages that exist inside your project codebase you don't need to copy the REST framework source `django.po` file into a `LOCALE_PATHS` folder, and can instead simply run Django's standard `makemessages` process.

Если вы переводите только пользовательские сообщения об ошибках, которые существуют в кодовой базе проекта, вам не нужно копировать файл Framework Framework `django.po` в папку` locale_paths` и вместо этого может просто запустить стандартный процесс Django `makemessages`
Анкет

## How the language is determined

## Как определяется язык

If you want to allow per-request language preferences you'll need to include `django.middleware.locale.LocaleMiddleware` in your `MIDDLEWARE` setting.

Если вы хотите разрешить предпочтения в отношении языка для первой проверки, вам необходимо включить `django.middleware.locale.localemiddleware` в настройку« промежуточное программное обеспечение ».

You can find more information on how the language preference is determined in the [Django documentation](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference). For reference, the method is:

Вы можете найти больше информации о том, как якосие определяется в [Django Documentation] (https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference)
Анкет
Для справки, метод:

1. First, it looks for the language prefix in the requested URL.
2. Failing that, it looks for the `LANGUAGE_SESSION_KEY` key in the current user’s session.
3. Failing that, it looks for a cookie.
4. Failing that, it looks at the `Accept-Language` HTTP header.
5. Failing that, it uses the global `LANGUAGE_CODE` setting.

1. Во -первых, он ищет префикс языка в запрошенном URL.
2. В сборе этого он ищет ключ `ranguage_session_key` в сеансе текущего пользователя.
3. Смущая это, он ищет печенье.
4. Смущая это, он смотрит на заголовок http `принять.
5. Не имея этого, он использует глобальную настройку `language_code`.

For API clients the most appropriate of these will typically be to use the `Accept-Language` header; Sessions and cookies will not be available unless using session authentication, and generally better practice to prefer an `Accept-Language` header for API clients rather than using language URL prefixes.

Для клиентов API наиболее подходящими из них обычно будет использование заголовка «Принятие языка»;
Сеансы и файлы cookie не будут доступны, если только не будет использоваться аутентификация сеанса, и, как правило, лучшая практика, чтобы предпочесть заголовок «Принятия» для клиентов API, а не использование префиксов языка URL.