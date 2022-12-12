<!-- TRANSLATED by md-translate -->
---

source:

источник:

* request.py

* request.py

---

# Requests

# Запросы

> If you're doing REST-based web service stuff ... you should ignore request.POST.
>
> — Malcom Tredinnick, [Django developers group](https://groups.google.com/d/topic/django-developers/dxI4qVzrBY4/discussion)

> Если вы делаете материал веб-службы на основе REST ... вы должны игнорировать запрос. POST.
>
>-Malcom Tredinnick, [Django Developers Group] (https://groups.google.com/d/topic/django-developers/dxi4qvzrby4/discussion)

REST framework's `Request` class extends the standard `HttpRequest`, adding support for REST framework's flexible request parsing and request authentication.

Класс REST Framework `request` расширяет стандартный` httprequest`, добавляя поддержку гибкого анализа и аутентификации запроса Framework Framework.

---

# Request parsing

# Запрос на диапазон

REST framework's Request objects provide flexible request parsing that allows you to treat requests with JSON data or other media types in the same way that you would normally deal with form data.

Объекты запроса REST Framework обеспечивают гибкий анализ запросов, который позволяет вам обрабатывать запросы с помощью данных JSON или других типов мультимедиа так же, как обычно с данными форм.

## .data

## .данные

`request.data` returns the parsed content of the request body. This is similar to the standard `request.POST` and `request.FILES` attributes except that:

`request.data` Возвращает анализируемое содержание органа запроса.
Это похоже на стандартные атрибуты `request.post` и` request.files`, за исключением этого:

* It includes all parsed content, including *file and non-file* inputs.
* It supports parsing the content of HTTP methods other than `POST`, meaning that you can access the content of `PUT` and `PATCH` requests.
* It supports REST framework's flexible request parsing, rather than just supporting form data. For example you can handle incoming [JSON data](parsers.md#jsonparser) similarly to how you handle incoming [form data](parsers.md#formparser).

* Он включает в себя все проанализированное содержание, в том числе * файл и не файл * входы *.
* Он поддерживает анализ содержания методов HTTP, отличных от «post», что означает, что вы можете получить доступ к содержанию запросов `put` и` patch '.
* Он поддерживает гибкий анализ запросов REST Framework, а не просто поддерживает данные формы.
Например, вы можете обрабатывать входящие [JSON Data] (parsers.md#jsonparser) аналогично тому, как вы обрабатываете входящие [form data] (parsers.md#formparser).

For more details see the [parsers documentation](parsers.md).

Для получения более подробной информации см. Документацию [Parsers] (parsers.md).

## .query_params

## .query_params

`request.query_params` is a more correctly named synonym for `request.GET`.

`request.query_params` - более правильно назван синоним для` request.get`.

For clarity inside your code, we recommend using `request.query_params` instead of the Django's standard `request.GET`. Doing so will help keep your codebase more correct and obvious - any HTTP method type may include query parameters, not just `GET` requests.

Для ясности в вашем коде мы рекомендуем использовать `request.query_params` вместо стандартного` ‘request.get`st` geting '.
Это поможет сохранить вашу кодовую базу более правильной и очевидной - любой тип метода HTTP может включать параметры запроса, а не только запросы `get`.

## .parsers

## .parsers

The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Parser` instances, based on the `parser_classes` set on the view or based on the `DEFAULT_PARSER_CLASSES` setting.

Класс `apiview` или декоратор@@api_view` убедится, что это свойство автоматически устанавливается в список экземпляров` parser` на основе установки `parser_classes` или на основе настройки` default_parser_classes.

You won't typically need to access this property.

Обычно вам не нужно получить доступ к этому свойству.

---

**Note:** If a client sends malformed content, then accessing `request.data` may raise a `ParseError`. By default REST framework's `APIView` class or `@api_view` decorator will catch the error and return a `400 Bad Request` response.

** ПРИМЕЧАНИЕ: ** Если клиент отправляет необработанный контент, то доступ к `request.data` может повысить` parseerror '.
По умолчанию класс REST Framework `apiview` или`@@api_view` Decorator поймает ошибку и вернет ответ `400 Bad Request`.

If a client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised, which by default will be caught and return a `415 Unsupported Media Type` response.

Если клиент отправляет запрос с типом контента, который не может быть проанализирован, будет поднято исключение «UnsupportedMediatype», что по умолчанию будет пойман и вернет ответ на тип медиа 415.

---

# Content negotiation

# Переговоры о контенте

The request exposes some properties that allow you to determine the result of the content negotiation stage. This allows you to implement behavior such as selecting a different serialization schemes for different media types.

Запрос раскрывает некоторые свойства, которые позволяют вам определить результат стадии согласования контента.
Это позволяет вам реализовать поведение, такое как выбор различных схем сериализации для разных типов носителей.

## .accepted_renderer

## .accepted_renderer

The renderer instance that was selected by the content negotiation stage.

Экземпляр рендеринга, который был выбран на стадии переговоров по контенту.

## .accepted_media_type

## .accepted_media_type

A string representing the media type that was accepted by the content negotiation stage.

Строка, представляющая тип медиа, который был принят на стадии переговоров по контенту.

---

# Authentication

# Аутентификация

REST framework provides flexible, per-request authentication, that gives you the ability to:

Структура REST обеспечивает гибкую аутентификацию для каждого запроса, которая дает вам возможность:

* Use different authentication policies for different parts of your API.
* Support the use of multiple authentication policies.
* Provide both user and token information associated with the incoming request.

* Используйте различные политики аутентификации для разных частей вашего API.
* Поддерживайте использование нескольких политик аутентификации.
* Предоставьте информацию о пользователе и токен, связанную с входящим запросом.

## .user

## .пользователь

`request.user` typically returns an instance of `django.contrib.auth.models.User`, although the behavior depends on the authentication policy being used.

`request.user` обычно возвращает экземпляр` django.contrib.auth.models.user`, хотя поведение зависит от используемой политики аутентификации.

If the request is unauthenticated the default value of `request.user` is an instance of `django.contrib.auth.models.AnonymousUser`.

Если запрос не является несаутентированным, значение по умолчанию `request.user` является экземпляром` django.contrib.auth.models.anonymoususer`.

For more details see the [authentication documentation](authentication.md).

Для получения более подробной информации см. [Документация по аутентификации] (Authentication.md).

## .auth

## .auth

`request.auth` returns any additional authentication context. The exact behavior of `request.auth` depends on the authentication policy being used, but it may typically be an instance of the token that the request was authenticated against.

`request.auth` возвращает любой дополнительный контекст аутентификации.
Точное поведение `request.auth` зависит от используемой политики аутентификации, но обычно это может быть экземпляром токена, против которого был аутентифицирован запрос.

If the request is unauthenticated, or if no additional context is present, the default value of `request.auth` is `None`.

Если запрос не является несаутентированным, или если нет дополнительного контекста, значение по умолчанию `request.auth` - none`.

For more details see the [authentication documentation](authentication.md).

Для получения более подробной информации см. [Документация по аутентификации] (Authentication.md).

## .authenticators

##. Authenticators

The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Authentication` instances, based on the `authentication_classes` set on the view or based on the `DEFAULT_AUTHENTICATORS` setting.

Класс `apiview` или декоратор@@api_view` гарантирует, что это свойство автоматически устанавливается в список экземпляров` authentication ', на основе настройки `wituretication_classes

You won't typically need to access this property.

Обычно вам не нужно получить доступ к этому свойству.

---

**Note:** You may see a `WrappedAttributeError` raised when calling the `.user` or `.auth` properties. These errors originate from an authenticator as a standard `AttributeError`, however it's necessary that they be re-raised as a different exception type in order to prevent them from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from the authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. The authenticator will need to be fixed.

** ПРИМЕЧАНИЕ: ** Вы можете увидеть `wrappedattributeerror`, поднятый при вызове свойств` .user` или `.auth`.
Эти ошибки возникают из аутентификатора как стандартного «атрибутарера», однако необходимо, чтобы они были повторно заработаны как другой тип исключения, чтобы не дать их подавлять доступ к внешнему имуществу.
Python не признает, что `attributeerror's происходит от аутентификатора и вместо этого предполагает, что объект запроса не имеет свойства` .user` или `.auth`.
Аутентитор должен быть исправлен.

---

# Browser enhancements

# Улучшения браузера

REST framework supports a few browser enhancements such as browser-based `PUT`, `PATCH` and `DELETE` forms.

Структура REST поддерживает несколько улучшений браузера, таких как формы на основе браузера `put`,` patch` и `delete`.

## .method

## .method

`request.method` returns the **uppercased** string representation of the request's HTTP method.

`request.method` Возвращает ** Опорное ** строковое представление метода HTTP запроса.

Browser-based `PUT`, `PATCH` and `DELETE` forms are transparently supported.

Формы на основе браузера `put`,` patch` и `delete` прозрачно поддерживаются.

For more information see the [browser enhancements documentation](../topics/browser-enhancements.md).

Для получения дополнительной информации см. Документацию по усовершенствованиям браузера] (../ Темы/браузер-enhancements.md).

## .content_type

## .Тип содержимого

`request.content_type`, returns a string object representing the media type of the HTTP request's body, or an empty string if no media type was provided.

`request.content_type`, возвращает строковый объект, представляющий тип носителя тела HTTP -запроса, или пустую строку, если не было предоставлено тип носителя.

You won't typically need to directly access the request's content type, as you'll normally rely on REST framework's default request parsing behavior.

Обычно вам не нужно будет напрямую доступ к типу контента запроса, так как вы обычно полагаетесь на поведение запроса по умолчанию REST Framework.

If you do need to access the content type of the request you should use the `.content_type` property in preference to using `request.META.get('HTTP_CONTENT_TYPE')`, as it provides transparent support for browser-based non-form content.

Если вам нужно получить доступ к типу контента запроса, который вы должны использовать свойство `.content_type` в предпочтениях к использованию` request.meta.get ('http_content_type') `, поскольку он обеспечивает прозрачную поддержку для некисформы на основе браузера.
содержание.

For more information see the [browser enhancements documentation](../topics/browser-enhancements.md).

Для получения дополнительной информации см. Документацию по усовершенствованиям браузера] (../ Темы/браузер-enhancements.md).

## .stream

## .ручей

`request.stream` returns a stream representing the content of the request body.

`request.stream` возвращает поток, представляющий содержание корпуса запроса.

You won't typically need to directly access the request's content, as you'll normally rely on REST framework's default request parsing behavior.

Обычно вам не нужно будет иметь непосредственный доступ к контенту запроса, так как вы обычно полагаетесь на поведение запроса по умолчанию REST Framework.

---

# Standard HttpRequest attributes

# Стандартные атрибуты httprequest

As REST framework's `Request` extends Django's `HttpRequest`, all the other standard attributes and methods are also available. For example the `request.META` and `request.session` dictionaries are available as normal.

Поскольку `request` от Rest Framework расширяет` httprequest Django, также доступны все другие стандартные атрибуты и методы.
Например, словарры `request.meta` и` request.session` доступны как обычно.

Note that due to implementation reasons the `Request` class does not inherit from `HttpRequest` class, but instead extends the class using composition.

Обратите внимание, что по причинам реализации класс `request` не наследует от класса` httprequest`, а вместо этого расширяет класс с помощью композиции.