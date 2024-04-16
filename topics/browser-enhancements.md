<!-- TRANSLATED by md-translate -->
# Улучшения в браузере

> "Есть два не вызывающих споров варианта использования перегруженного POST. Первое - это *имитация* унифицированного интерфейса HTTP для клиентов, таких как веб-браузеры, которые не поддерживают PUT или DELETE".
>
> - [RESTful Web Services](https://www.amazon.com/RESTful-Web-Services-Leonard-Richardson/dp/0596529260), Leonard Richardson & Sam Ruby.

Для того чтобы Web-интерфейс API функционировал, есть несколько усовершенствований для браузеров, которые должны быть предоставлены REST-фреймворком.

Начиная с версии 3.3.0 и далее они включаются с помощью javascript, используя библиотеку [ajax-form](https://github.com/tomchristie/ajax-form).

## PUT, DELETE и т.д. на основе браузера.

Библиотека [AJAX form library](https://github.com/tomchristie/ajax-form) поддерживает браузерные методы `PUT`, `DELETE` и другие методы на HTML формах.

После включения библиотеки используйте атрибут `data-method` на форме, как показано ниже:

```html
<form action="/" data-method="PUT">
    <input name='foo'/>
    ...
</form>
```

Обратите внимание, что до версии 3.3.0 эта поддержка осуществлялась на стороне сервера, а не на основе javascript. Стиль перегрузки методов (используемый в [Ruby on Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-put-or-delete-methods-work)) больше не поддерживается из-за некоторых проблем, возникающих при разборе запросов.

## Отправка контента вне формы с помощью браузера

Отправка через браузер таких типов содержимого, как JSON, поддерживается [библиотекой форм AJAX](https://github.com/tomchristie/ajax-form), используя поля формы с атрибутами `data-override='content-type'` и `data-override='content'`.

Например:

```html
<form action="/">
        <input data-override='content-type' value='application/json' type='hidden'/>
        <textarea data-override='content'>{}</textarea>
        <input type="submit"/>
    </form>
```

Обратите внимание, что до версии 3.3.0 эта поддержка осуществлялась на стороне сервера, а не на основе javascript.

## Суффиксы формата на основе URL

DRF может принимать параметры URL в стиле `?format=json`, что может быть полезным сокращением для определения типа содержимого, которое должно быть возвращено из представления.

Это поведение контролируется с помощью параметра `URL_FORMAT_OVERRIDE`.

## Переопределение метода на основе заголовка HTTP

До версии 3.3.0 поддерживался заголовок расширения `X-HTTP-Method-Override` для переопределения метода запроса. Это поведение больше не используется в ядре, но может быть добавлено при необходимости с помощью middleware.

Например:

```python
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

## Заголовки accept на основе URL

До версии 3.3.0 DRF включал встроенную поддержку параметров URL в стиле `?accept=application/json`, что позволяло переопределять заголовок `Accept`.

После внедрения API согласования контента это поведение больше не включено в ядро, но может быть добавлено с помощью пользовательского класса согласования контента, если это необходимо.

Например:

```python
class AcceptQueryParamOverride()
    def get_accept_list(self, request):
       header = request.META.get('HTTP_ACCEPT', '*/*')
       header = request.query_params.get('_accept', header)
       return [token.strip() for token in header.split(',')]
```

## Разве HTML5 не поддерживает формы PUT и DELETE?

Нет. Одно время предполагалось, что HTML5 будет поддерживать формы `PUT` и `DELETE`, но позже это было [исключено из спецификации](https://www.w3.org/TR/html5-diff/#changes-2010-06-24). Остается [продолжающееся обсуждение](http://amundsen.com/examples/put-delete-forms/) добавления поддержки `PUT` и `DELETE`, а также того, как поддерживать типы содержимого, отличные от закодированных в форме данных.
