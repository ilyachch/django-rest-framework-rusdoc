<!-- TRANSLATED by md-translate -->
# Internationalization

# Интернационализация

> Supporting internationalization is not optional. It must be a core feature.
>
> — [Jannis Leidel, speaking at Django Under the Hood, 2015](https://youtu.be/Wa0VfS2q94Y).

> Поддержка интернационализации не является необязательной. Она должна быть основной функцией.
>
> - [Яннис Лейдель, выступая на Django Under the Hood, 2015](https://youtu.be/Wa0VfS2q94Y).

REST framework ships with translatable error messages. You can make these appear in your language enabling [Django's standard translation mechanisms](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

REST-фреймворк поставляется с переводимыми сообщениями об ошибках. Вы можете сделать так, чтобы они отображались на вашем языке, используя [стандартные механизмы перевода Django](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

Doing so will allow you to:

Это позволит вам:

* Select a language other than English as the default, using the standard `LANGUAGE_CODE` Django setting.
* Allow clients to choose a language themselves, using the `LocaleMiddleware` included with Django. A typical usage for API clients would be to include an `Accept-Language` request header.

* Выберите язык по умолчанию, отличный от английского, используя стандартную настройку Django `LANGUAGE_CODE`.
* Позволить клиентам самим выбирать язык, используя `LocaleMiddleware`, включенный в Django. Типичное использование для клиентов API - включение заголовка запроса `Accept-Language`.

## Enabling internationalized APIs

## Включение интернационализированных API

You can change the default language by using the standard Django `LANGUAGE_CODE` setting:

Вы можете изменить язык по умолчанию с помощью стандартной настройки Django `LANGUAGE_CODE`:

```
LANGUAGE_CODE = "es-es"
```

You can turn on per-request language requests by adding `LocalMiddleware` to your `MIDDLEWARE` setting:

Вы можете включить языковые запросы на каждый запрос, добавив `LocalMiddleware` в настройку `MIDDLEWARE`:

```
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware'
]
```

When per-request internationalization is enabled, client requests will respect the `Accept-Language` header where possible. For example, let's make a request for an unsupported media type:

Когда интернационализация по каждому запросу включена, клиентские запросы будут соблюдать заголовок `Accept-Language`, где это возможно. Например, давайте сделаем запрос для неподдерживаемого типа медиа:

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

REST framework включает эти встроенные переводы как для стандартных случаев исключений, так и для ошибок валидации сериализатора.

Note that the translations only apply to the error strings themselves. The format of error messages, and the keys of field names will remain the same. An example `400 Bad Request` response body might look like this:

Обратите внимание, что переводы относятся только к самим строкам ошибок. Формат сообщений об ошибках и ключи имен полей останутся неизменными. Пример тела ответа `400 Bad Request` может выглядеть следующим образом:

```
{"detail": {"username": ["Esse campo deve ser único."]}}
```

If you want to use different string for parts of the response such as `detail` and `non_field_errors` then you can modify this behavior by using a [custom exception handler](../api-guide/exceptions.md#custom-exception-handling).

Если вы хотите использовать разные строки для таких частей ответа, как `detail` и `non_field_errors`, вы можете изменить это поведение, используя [пользовательский обработчик исключений](../api-guide/exceptions.md#custom-exception-handling).

#### Specifying the set of supported languages.

#### Указание набора поддерживаемых языков.

By default all available languages will be supported.

По умолчанию поддерживаются все доступные языки.

If you only wish to support a subset of the available languages, use Django's standard `LANGUAGES` setting:

Если вы хотите поддерживать только часть доступных языков, используйте стандартную настройку Django `LANGUAGES`:

```
LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
```

## Adding new translations

## Добавление новых переводов

REST framework translations are managed online using [Transifex](https://www.transifex.com/projects/p/django-rest-framework/). You can use the Transifex service to add new translation languages. The maintenance team will then ensure that these translation strings are included in the REST framework package.

Управление переводами фреймворка REST осуществляется в режиме онлайн с помощью [Transifex](https://www.transifex.com/projects/p/django-rest-framework/). Вы можете использовать сервис Transifex для добавления новых языков перевода. Команда сопровождения обеспечит включение этих строк перевода в пакет фреймворка REST.

Sometimes you may need to add translation strings to your project locally. You may need to do this if:

Иногда вам может понадобиться добавить строки перевода в ваш проект локально. Это может понадобиться, если:

* You want to use REST Framework in a language which has not been translated yet on Transifex.
* Your project includes custom error messages, which are not part of REST framework's default translation strings.

* Вы хотите использовать REST Framework на языке, который еще не переведен на Transifex.
* Ваш проект включает пользовательские сообщения об ошибках, которые не входят в строки перевода REST Framework по умолчанию.

#### Translating a new language locally

#### Перевод нового языка на местном уровне

This guide assumes you are already familiar with how to translate a Django app. If you're not, start by reading [Django's translation docs](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

Это руководство предполагает, что вы уже знакомы с тем, как перевести приложение Django. Если это не так, начните с чтения [Django's translation docs](https://docs.djangoproject.com/en/stable/topics/i18n/translation).

If you're translating a new language you'll need to translate the existing REST framework error messages:

Если вы переводите новый язык, вам нужно будет перевести существующие сообщения об ошибках фреймворка REST:

1. Make a new folder where you want to store the internationalization resources. Add this path to your [`LOCALE_PATHS`](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-LOCALE_PATHS) setting.
2. Now create a subfolder for the language you want to translate. The folder should be named using [locale name](https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name) notation. For example: `de`, `pt_BR`, `es_AR`.
3. Now copy the [base translations file](https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_US/LC_MESSAGES/django.po) from the REST framework source code into your translations folder.
4. Edit the `django.po` file you've just copied, translating all the error messages.
5. Run `manage.py compilemessages -l pt_BR` to make the translations available for Django to use. You should see a message like `processing file django.po in <...>/locale/pt_BR/LC_MESSAGES`.
6. Restart your development server to see the changes take effect.

1. Создайте новую папку, в которой вы хотите хранить ресурсы интернационализации. Добавьте этот путь в настройку [`LOCALE_PATHS`](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-LOCALE_PATHS).
2. Теперь создайте подпапку для языка, который вы хотите перевести. Папка должна быть названа с использованием нотации [имя локали](https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name). Например: `de`, `pt_BR`, `es_AR`.
3. Теперь скопируйте файл [base translations file](https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_US/LC_MESSAGES/django.po) из исходного кода REST framework в папку translations.
4. Отредактируйте только что скопированный файл `django.po`, переведя все сообщения об ошибках.
5. Запустите `manage.py compilemessages -l pt_BR`, чтобы сделать переводы доступными для использования Django. Вы должны увидеть сообщение типа `processing file django.po in <...>/locale/pt_BR/LC_MESSAGES`.
6. Перезапустите ваш сервер разработки, чтобы увидеть, что изменения вступили в силу.

If you're only translating custom error messages that exist inside your project codebase you don't need to copy the REST framework source `django.po` file into a `LOCALE_PATHS` folder, and can instead simply run Django's standard `makemessages` process.

Если вы переводите только пользовательские сообщения об ошибках, которые существуют в кодовой базе вашего проекта, вам не нужно копировать исходный файл REST-фреймворка `django.po` в папку `LOCALE_PATHS`, а можно просто запустить стандартный процесс Django `makemessages`.

## How the language is determined

## Как определяется язык

If you want to allow per-request language preferences you'll need to include `django.middleware.locale.LocaleMiddleware` in your `MIDDLEWARE` setting.

Если вы хотите разрешить языковые предпочтения для каждого запроса, вам нужно включить `django.middleware.locale.LocaleMiddleware` в настройку `MIDDLEWARE`.

You can find more information on how the language preference is determined in the [Django documentation](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference). For reference, the method is:

Более подробную информацию о том, как определяется предпочтение языка, вы можете найти в [документации Django](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference). Для справки, метод следующий:

1. First, it looks for the language prefix in the requested URL.
2. Failing that, it looks for the `LANGUAGE_SESSION_KEY` key in the current user’s session.
3. Failing that, it looks for a cookie.
4. Failing that, it looks at the `Accept-Language` HTTP header.
5. Failing that, it uses the global `LANGUAGE_CODE` setting.

1. Во-первых, он ищет префикс языка в запрашиваемом URL.
2. Если это не удается, он ищет ключ `LANGUAGE_SESSION_KEY` в текущей сессии пользователя.
3. Если это не удается, выполняется поиск куки.
4. В противном случае просматривается HTTP-заголовок `Accept-Language`.
5. В противном случае используется глобальная настройка `LANGUAGE_CODE`.

For API clients the most appropriate of these will typically be to use the `Accept-Language` header; Sessions and cookies will not be available unless using session authentication, and generally better practice to prefer an `Accept-Language` header for API clients rather than using language URL prefixes.

Для клиентов API наиболее подходящим из них обычно является использование заголовка `Accept-Language`; сеансы и cookies будут недоступны, если не используется аутентификация сеанса, и вообще лучше предпочесть заголовок `Accept-Language` для клиентов API, а не использовать языковые префиксы URL.