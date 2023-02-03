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

> Если вы занимаетесь веб-сервисами на основе REST... вам следует игнорировать request.POST.
>
> - Malcom Tredinnick, [Django developers group](https://groups.google.com/d/topic/django-developers/dxI4qVzrBY4/discussion)

REST framework's `Request` class extends the standard `HttpRequest`, adding support for REST framework's flexible request parsing and request authentication.

Класс `Request` фреймворка REST расширяет стандартный `HttpRequest`, добавляя поддержку гибкого разбора запросов фреймворка REST и аутентификации запросов.

---

# Request parsing

# Разбор запроса

REST framework's Request objects provide flexible request parsing that allows you to treat requests with JSON data or other media types in the same way that you would normally deal with form data.

Объекты Request фреймворка REST обеспечивают гибкий разбор запросов, что позволяет обрабатывать запросы с данными JSON или другими типами медиа таким же образом, как вы обычно обрабатываете данные формы.

## .data

## .data

`request.data` returns the parsed content of the request body. This is similar to the standard `request.POST` and `request.FILES` attributes except that:

`request.data` возвращает разобранное содержимое тела запроса. Это похоже на стандартные атрибуты `request.POST` и `request.FILES`, за исключением того, что:

* It includes all parsed content, including *file and non-file* inputs.
* It supports parsing the content of HTTP methods other than `POST`, meaning that you can access the content of `PUT` and `PATCH` requests.
* It supports REST framework's flexible request parsing, rather than just supporting form data. For example you can handle incoming [JSON data](parsers.md#jsonparser) similarly to how you handle incoming [form data](parsers.md#formparser).

* Он включает в себя все разобранное содержимое, включая *файловые и нефайловые* входы.
* Поддерживается разбор содержимого методов HTTP, отличных от `POST`, что означает, что вы можете получить доступ к содержимому запросов `PUT` и `PATCH`.
* Поддерживается гибкий разбор запросов фреймворка REST, а не только поддержка данных формы. Например, вы можете обрабатывать входящие [JSON-данные](parsers.md#jsonparser) аналогично тому, как вы обрабатываете входящие [данные формы](parsers.md#formparser).

For more details see the [parsers documentation](parsers.md).

Более подробную информацию можно найти в [документации по парсерам] (parsers.md).

## .query_params

## .query_params

`request.query_params` is a more correctly named synonym for `request.GET`.

`request.query_params` - это более правильно названный синоним `request.GET`.

For clarity inside your code, we recommend using `request.query_params` instead of the Django's standard `request.GET`. Doing so will help keep your codebase more correct and obvious - any HTTP method type may include query parameters, not just `GET` requests.

Для ясности внутри вашего кода мы рекомендуем использовать `request.query_params` вместо стандартного для Django `request.GET`. Это поможет сохранить вашу кодовую базу более корректной и очевидной - любой тип HTTP метода может включать параметры запроса, а не только `GET` запросы.

## .parsers

## .parsers

The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Parser` instances, based on the `parser_classes` set on the view or based on the `DEFAULT_PARSER_CLASSES` setting.

Класс `APIView` или декоратор `@api_view` обеспечат автоматическую установку этого свойства в список экземпляров `Parser` на основе `parser_classes`, установленных в представлении, или на основе настройки `DEFAULT_PARSER_CLASSES`.

You won't typically need to access this property.

Обычно вам не требуется доступ к этой собственности.

---

**Note:** If a client sends malformed content, then accessing `request.data` may raise a `ParseError`. By default REST framework's `APIView` class or `@api_view` decorator will catch the error and return a `400 Bad Request` response.

**Примечание:** Если клиент посылает недостоверное содержимое, то при доступе к `request.data` может возникнуть ошибка `ParseError`. По умолчанию класс `APIView` или декоратор `@api_view` REST framework поймает ошибку и вернет ответ `400 Bad Request`.

If a client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised, which by default will be caught and return a `415 Unsupported Media Type` response.

Если клиент посылает запрос с типом содержимого, который не может быть разобран, то возникает исключение `UnsupportedMediaType`, которое по умолчанию будет поймано и вернет ответ `415 Unsupported Media Type`.

---

# Content negotiation

# Переговоры по содержанию

The request exposes some properties that allow you to determine the result of the content negotiation stage. This allows you to implement behavior such as selecting a different serialization schemes for different media types.

Запрос раскрывает некоторые свойства, которые позволяют определить результат этапа согласования содержимого. Это позволяет вам реализовать такое поведение, как выбор различных схем сериализации для различных типов носителей.

## .accepted_renderer

## .accepted_renderer

The renderer instance that was selected by the content negotiation stage.

Экземпляр рендерера, который был выбран на этапе согласования содержимого.

## .accepted_media_type

## .accepted_media_type

A string representing the media type that was accepted by the content negotiation stage.

Строка, представляющая тип носителя, который был принят на этапе согласования содержимого.

---

# Authentication

# Аутентификация

REST framework provides flexible, per-request authentication, that gives you the ability to:

Структура REST обеспечивает гибкую аутентификацию по каждому запросу, что дает вам возможность:

* Use different authentication policies for different parts of your API.
* Support the use of multiple authentication policies.
* Provide both user and token information associated with the incoming request.

* Используйте различные политики аутентификации для разных частей вашего API.
* Поддерживайте использование нескольких политик аутентификации.
* Предоставлять информацию о пользователе и маркере, связанную с входящим запросом.

## .user

## .user

`request.user` typically returns an instance of `django.contrib.auth.models.User`, although the behavior depends on the authentication policy being used.

`request.user` обычно возвращает экземпляр `django.contrib.auth.models.User`, хотя поведение зависит от используемой политики аутентификации.

If the request is unauthenticated the default value of `request.user` is an instance of `django.contrib.auth.models.AnonymousUser`.

Если запрос не аутентифицирован, значением по умолчанию для `request.user` будет экземпляр `django.contrib.auth.models.AnonymousUser`.

For more details see the [authentication documentation](authentication.md).

Более подробную информацию можно найти в [документации по аутентификации] (authentication.md).

## .auth

## .auth

`request.auth` returns any additional authentication context. The exact behavior of `request.auth` depends on the authentication policy being used, but it may typically be an instance of the token that the request was authenticated against.

`request.auth` возвращает любой дополнительный контекст аутентификации. Точное поведение `request.auth` зависит от используемой политики аутентификации, но обычно это может быть экземпляр токена, по которому был аутентифицирован запрос.

If the request is unauthenticated, or if no additional context is present, the default value of `request.auth` is `None`.

Если запрос не аутентифицирован, или если отсутствует дополнительный контекст, значение по умолчанию `request.auth` равно `None`.

For more details see the [authentication documentation](authentication.md).

Более подробную информацию можно найти в [документации по аутентификации] (authentication.md).

## .authenticators

## .authenticators

The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Authentication` instances, based on the `authentication_classes` set on the view or based on the `DEFAULT_AUTHENTICATORS` setting.

Класс `APIView` или декоратор `@api_view` обеспечат автоматическую установку этого свойства в список экземпляров `Authentication` на основе `authentication_classes`, установленных для представления, или на основе параметра `DEFAULT_AUTHENTICATORS`.

You won't typically need to access this property.

Обычно вам не требуется доступ к этой собственности.

---

**Note:** You may see a `WrappedAttributeError` raised when calling the `.user` or `.auth` properties. These errors originate from an authenticator as a standard `AttributeError`, however it's necessary that they be re-raised as a different exception type in order to prevent them from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from the authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. The authenticator will need to be fixed.

**Примечание:** При вызове свойств `.user` или `.auth` может возникнуть ошибка `WrappedAttributeError`. Эти ошибки исходят от аутентификатора как стандартные `AttributeError`, однако необходимо, чтобы они были повторно вызваны как исключение другого типа, чтобы предотвратить их подавление внешним доступом к свойству. Python не распознает, что `AttributeError` исходит от аутентификатора, и вместо этого будет считать, что объект запроса не имеет свойства `.user` или `.auth`. Аутентификатор необходимо будет исправить.

---

# Browser enhancements

# Улучшения в браузере

REST framework supports a few browser enhancements such as browser-based `PUT`, `PATCH` and `DELETE` forms.

REST framework поддерживает несколько улучшений для браузеров, таких как браузерные формы `PUT`, `PATCH` и `DELETE`.

## .method

## .метод

`request.method` returns the **uppercased** string representation of the request's HTTP method.

`request.method` возвращает **упрощенное** строковое представление HTTP-метода запроса.

Browser-based `PUT`, `PATCH` and `DELETE` forms are transparently supported.

Формы `PUT`, `PATCH` и `DELETE`, основанные на браузере, поддерживаются прозрачно.

For more information see the [browser enhancements documentation](../topics/browser-enhancements.md).

Для получения дополнительной информации см. документацию [browser enhancements documentation](../topics/browser-enhancements.md).

## .content_type

## .content_type

`request.content_type`, returns a string object representing the media type of the HTTP request's body, or an empty string if no media type was provided.

`request.content_type`, возвращает строковый объект, представляющий тип медиа тела HTTP запроса, или пустую строку, если тип медиа не был предоставлен.

You won't typically need to directly access the request's content type, as you'll normally rely on REST framework's default request parsing behavior.

Обычно вам не нужно напрямую обращаться к типу содержимого запроса, поскольку вы обычно полагаетесь на стандартное поведение REST-фреймворка при разборе запроса.

If you do need to access the content type of the request you should use the `.content_type` property in preference to using `request.META.get('HTTP_CONTENT_TYPE')`, as it provides transparent support for browser-based non-form content.

Если вам необходимо получить доступ к типу содержимого запроса, вам следует использовать свойство `.content_type`, а не `request.META.get('HTTP_CONTENT_TYPE')`, так как оно обеспечивает прозрачную поддержку неформенного содержимого в браузере.

For more information see the [browser enhancements documentation](../topics/browser-enhancements.md).

Для получения дополнительной информации см. документацию [browser enhancements documentation](../topics/browser-enhancements.md).

## .stream

## .stream

`request.stream` returns a stream representing the content of the request body.

`request.stream` возвращает поток, представляющий содержимое тела запроса.

You won't typically need to directly access the request's content, as you'll normally rely on REST framework's default request parsing behavior.

Как правило, вам не понадобится прямой доступ к содержимому запроса, поскольку вы обычно полагаетесь на стандартное поведение REST-фреймворка при разборе запроса.

---

# Standard HttpRequest attributes

# Стандартные атрибуты HttpRequest

As REST framework's `Request` extends Django's `HttpRequest`, all the other standard attributes and methods are also available. For example the `request.META` and `request.session` dictionaries are available as normal.

Поскольку `Request` фреймворка REST расширяет `HttpRequest` фреймворка Django, все остальные стандартные атрибуты и методы также доступны. Например, словари `request.META` и `request.session` доступны как обычно.

Note that due to implementation reasons the `Request` class does not inherit from `HttpRequest` class, but instead extends the class using composition.

Обратите внимание, что по причинам реализации класс `Request` не наследуется от класса `HttpRequest`, а вместо этого расширяет его, используя композицию.