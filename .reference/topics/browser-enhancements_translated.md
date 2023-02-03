<!-- TRANSLATED by md-translate -->
# Browser enhancements

# Улучшения в браузере

> "There are two noncontroversial uses for overloaded POST. The first is to *simulate* HTTP's uniform interface for clients like web browsers that don't support PUT or DELETE"
>
> — [RESTful Web Services](https://www.amazon.com/RESTful-Web-Services-Leonard-Richardson/dp/0596529260), Leonard Richardson & Sam Ruby.

> "Есть два не вызывающих споров варианта использования перегруженного POST. Первое - это *имитация* унифицированного интерфейса HTTP для клиентов, таких как веб-браузеры, которые не поддерживают PUT или DELETE".
>
> - [RESTful Web Services](https://www.amazon.com/RESTful-Web-Services-Leonard-Richardson/dp/0596529260), Leonard Richardson & Sam Ruby.

In order to allow the browsable API to function, there are a couple of browser enhancements that REST framework needs to provide.

Для того чтобы API с возможностью просмотра функционировал, есть несколько усовершенствований для браузеров, которые должны быть предоставлены REST-фреймворком.

As of version 3.3.0 onwards these are enabled with javascript, using the [ajax-form](https://github.com/tomchristie/ajax-form) library.

Начиная с версии 3.3.0 и далее они включаются с помощью javascript, используя библиотеку [ajax-form](https://github.com/tomchristie/ajax-form).

## Browser based PUT, DELETE, etc...

## PUT, DELETE и т.д. на основе браузера.

The [AJAX form library](https://github.com/tomchristie/ajax-form) supports browser-based `PUT`, `DELETE` and other methods on HTML forms.

Библиотека [AJAX form library](https://github.com/tomchristie/ajax-form) поддерживает браузерные методы `PUT`, `DELETE` и другие методы на HTML формах.

After including the library, use the `data-method` attribute on the form, like so:

После включения библиотеки используйте атрибут `data-method` на форме, как показано ниже:

```
<form action="/" data-method="PUT">
    <input name='foo'/>
    ...
</form>
```

Note that prior to 3.3.0, this support was server-side rather than javascript based. The method overloading style (as used in [Ruby on Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-put-or-delete-methods-work)) is no longer supported due to subtle issues that it introduces in request parsing.

Обратите внимание, что до версии 3.3.0 эта поддержка осуществлялась на стороне сервера, а не на основе javascript. Стиль перегрузки методов (используемый в [Ruby on Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-put-or-delete-methods-work)) больше не поддерживается из-за тонких проблем, возникающих при разборе запросов.

## Browser based submission of non-form content

## Представление неформального контента с помощью браузера

Browser-based submission of content types such as JSON are supported by the [AJAX form library](https://github.com/tomchristie/ajax-form), using form fields with `data-override='content-type'` and `data-override='content'` attributes.

Отправка через браузер таких типов содержимого, как JSON, поддерживается [библиотекой форм AJAX](https://github.com/tomchristie/ajax-form), используя поля формы с атрибутами `data-override='content-type'` и `data-override='content'`.

For example:

Например:

```
<form action="/">
        <input data-override='content-type' value='application/json' type='hidden'/>
        <textarea data-override='content'>{}</textarea>
        <input type="submit"/>
    </form>
```

Note that prior to 3.3.0, this support was server-side rather than javascript based.

Обратите внимание, что до версии 3.3.0 эта поддержка осуществлялась на стороне сервера, а не на основе javascript.

## URL based format suffixes

## Суффиксы формата на основе URL

REST framework can take `?format=json` style URL parameters, which can be a useful shortcut for determining which content type should be returned from the view.

Фреймворк REST может принимать параметры URL в стиле `?format=json`, что может быть полезным сокращением для определения типа содержимого, которое должно быть возвращено из представления.

This behavior is controlled using the `URL_FORMAT_OVERRIDE` setting.

Это поведение контролируется с помощью параметра `URL_FORMAT_OVERRIDE`.

## HTTP header based method overriding

## Переопределение метода на основе заголовка HTTP

Prior to version 3.3.0 the semi extension header `X-HTTP-Method-Override` was supported for overriding the request method. This behavior is no longer in core, but can be adding if needed using middleware.

До версии 3.3.0 поддерживался полузаголовок расширения `X-HTTP-Method-Override` для переопределения метода запроса. Это поведение больше не используется в ядре, но может быть добавлено при необходимости с помощью промежуточного ПО.

For example:

Например:

```
METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'

class MethodOverrideMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and METHOD_OVERRIDE_HEADER in request.META:
            request.method = request.META[METHOD_OVERRIDE_HEADER]
        return self.get_response(request)
```

## URL based accept headers

## Прием заголовков на основе URL

Until version 3.3.0 REST framework included built-in support for `?accept=application/json` style URL parameters, which would allow the `Accept` header to be overridden.

До версии 3.3.0 REST framework включал встроенную поддержку параметров URL в стиле `?accept=application/json`, что позволяло переопределять заголовок `Accept`.

Since the introduction of the content negotiation API this behavior is no longer included in core, but may be added using a custom content negotiation class, if needed.

После внедрения API согласования контента это поведение больше не включено в ядро, но может быть добавлено с помощью пользовательского класса согласования контента, если это необходимо.

For example:

Например:

```
class AcceptQueryParamOverride()
    def get_accept_list(self, request):
       header = request.META.get('HTTP_ACCEPT', '*/*')
       header = request.query_params.get('_accept', header)
       return [token.strip() for token in header.split(',')]
```

## Doesn't HTML5 support PUT and DELETE forms?

## Разве HTML5 не поддерживает формы PUT и DELETE?

Nope. It was at one point intended to support `PUT` and `DELETE` forms, but was later [dropped from the spec](https://www.w3.org/TR/html5-diff/#changes-2010-06-24). There remains [ongoing discussion](http://amundsen.com/examples/put-delete-forms/) about adding support for `PUT` and `DELETE`, as well as how to support content types other than form-encoded data.

Нет. Одно время предполагалось, что он будет поддерживать формы `PUT` и `DELETE`, но позже он был [исключен из спецификации] (https://www.w3.org/TR/html5-diff/#changes-2010-06-24). Остается [продолжающееся обсуждение] (http://amundsen.com/examples/put-delete-forms/) добавления поддержки `PUT` и `DELETE`, а также того, как поддерживать типы содержимого, отличные от закодированных в форме данных.