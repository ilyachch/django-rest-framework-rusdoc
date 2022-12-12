<!-- TRANSLATED by md-translate -->
# Browser enhancements

# Улучшения браузера

> "There are two noncontroversial uses for overloaded POST. The first is to *simulate* HTTP's uniform interface for clients like web browsers that don't support PUT or DELETE"
>
> — [RESTful Web Services](https://www.amazon.com/RESTful-Web-Services-Leonard-Richardson/dp/0596529260), Leonard Richardson & Sam Ruby.

> «Существует два неверных применения для перегруженного сообщения. Первое - это имитировать * единый интерфейс HTTP для клиентов, таких как веб -браузеры, которые не поддерживают или удаляют».
>
>-[Restful Web Services] (https://www.amazon.com/restful-web-services-leonard-richardson/dp/0596529260), Леонард Ричардсон и Сэм Руби.

In order to allow the browsable API to function, there are a couple of browser enhancements that REST framework needs to provide.

Чтобы позволить функционированию API, который можно просматривать, существует пара улучшений браузера, которые необходимо обеспечить структуре REST.

As of version 3.3.0 onwards these are enabled with javascript, using the [ajax-form](https://github.com/tomchristie/ajax-form) library.

Начиная с версии 3.3.0, они включены с помощью JavaScript, используя библиотеку [ajax-form] (https://github.com/tomchristie/ajax-form).

## Browser based PUT, DELETE, etc...

## на основе браузера Put, Delete и т. Д.

The [AJAX form library](https://github.com/tomchristie/ajax-form) supports browser-based `PUT`, `DELETE` and other methods on HTML forms.

[Ajax Form Library] (https://github.com/tomchristie/ajax-form) поддерживает на основе браузера `put`,` delete` и другие методы на HTML-формах.

After including the library, use the `data-method` attribute on the form, like so:

После включения библиотеки используйте атрибут «Data-Method» в форме, например, SO:

```
<form action="/" data-method="PUT">
    <input name='foo'/>
    ...
</form>
```

Note that prior to 3.3.0, this support was server-side rather than javascript based. The method overloading style (as used in [Ruby on Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-put-or-delete-methods-work)) is no longer supported due to subtle issues that it introduces in request parsing.

Обратите внимание, что до 3.3.0 эта поддержка была на стороне сервера, а не на основе JavaScript.
Стиль перегрузки метода (как используется в [Ruby on Rails] (https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-or-delete-methothods-pork))) больше не является))))))
Поддерживается из -за тонких проблем, которые он вводит в анализе запросов.

## Browser based submission of non-form content

## Основанный на основе браузера неформальный контент

Browser-based submission of content types such as JSON are supported by the [AJAX form library](https://github.com/tomchristie/ajax-form), using form fields with `data-override='content-type'` and `data-override='content'` attributes.

Основанная на браузерах представление типов контента, таких как JSON, поддерживается [библиотека AJAX Form] (https://github.com/tomchristie/ajax-form), используя поля формы с `data override = 'content-type'``
и `data-override = 'content'' 'Атрибуты.

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

Обратите внимание, что до 3.3.0 эта поддержка была на стороне сервера, а не на основе JavaScript.

## URL based format suffixes

## Суффиксы на основе URL -адреса на основе URL

REST framework can take `?format=json` style URL parameters, which can be a useful shortcut for determining which content type should be returned from the view.

Структура REST может занять параметры URL -адреса json 'Format = JSON

This behavior is controlled using the `URL_FORMAT_OVERRIDE` setting.

Это поведение контролируется с помощью настройки `url_format_override`.

## HTTP header based method overriding

## http -заголовок метод переоценки

Prior to version 3.3.0 the semi extension header `X-HTTP-Method-Override` was supported for overriding the request method. This behavior is no longer in core, but can be adding if needed using middleware.

Перед версией 3.3.0 заголовок полувыхнет `x-http-method-override 'был поддержан для переоценки метода запроса.
Такое поведение больше не находится в ядре, но может добавлять при необходимости с помощью промежуточного программного обеспечения.

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

## на основе URL -адресов заголовки принятия

Until version 3.3.0 REST framework included built-in support for `?accept=application/json` style URL parameters, which would allow the `Accept` header to be overridden.

До версии 3.3.0 Структура REST не включала встроенную поддержку для параметров URL-адреса `? Accept = Application/JSON

Since the introduction of the content negotiation API this behavior is no longer included in core, but may be added using a custom content negotiation class, if needed.

Поскольку введение в API переговоров по контенту, это поведение больше не включено в ядро, но может быть добавлено с использованием пользовательского класса согласования контента, если это необходимо.

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

## Разве HTML5 поддерживает и удаляет формы?

Nope. It was at one point intended to support `PUT` and `DELETE` forms, but was later [dropped from the spec](https://www.w3.org/TR/html5-diff/#changes-2010-06-24). There remains [ongoing discussion](http://amundsen.com/examples/put-delete-forms/) about adding support for `PUT` and `DELETE`, as well as how to support content types other than form-encoded data.

Неа.
В какой-то момент это было предназначено для поддержки форм `put` и` delete`, но позже было выброшено из Spec] (https://www.w3.org/tr/html5-diff/#changes-2010-06-
24).
Остается [продолжающееся обсуждение] (http://amundsen.com/examples/put-delete-forms/) о добавлении поддержки для `put` и` delete`, а также о том, как поддержать типы контента, отличные от кодируемых формами данных
Анкет