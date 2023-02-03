<!-- TRANSLATED by md-translate -->
# Working with AJAX, CSRF & CORS

# Работа с AJAX, CSRF и CORS

> "Take a close look at possible CSRF / XSRF vulnerabilities on your own websites. They're the worst kind of vulnerability — very easy to exploit by attackers, yet not so intuitively easy to understand for software developers, at least until you've been bitten by one."
>
> — [Jeff Atwood](https://blog.codinghorror.com/preventing-csrf-and-xsrf-attacks/)

> "Внимательно изучите возможные уязвимости CSRF / XSRF на ваших собственных сайтах. Это худший вид уязвимостей - их очень легко использовать злоумышленникам, но не так просто интуитивно понять разработчикам программного обеспечения, по крайней мере, пока вас не укусит одна из них."
>
> - [Jeff Atwood](https://blog.codinghorror.com/preventing-csrf-and-xsrf-attacks/)

## Javascript clients

## Клиенты Javascript

If you’re building a JavaScript client to interface with your Web API, you'll need to consider if the client can use the same authentication policy that is used by the rest of the website, and also determine if you need to use CSRF tokens or CORS headers.

Если вы создаете JavaScript-клиент для взаимодействия с вашим Web API, вам нужно подумать, может ли клиент использовать ту же политику аутентификации, которая используется остальной частью сайта, а также определить, нужно ли вам использовать CSRF-токены или CORS-заголовки.

AJAX requests that are made within the same context as the API they are interacting with will typically use `SessionAuthentication`. This ensures that once a user has logged in, any AJAX requests made can be authenticated using the same session-based authentication that is used for the rest of the website.

AJAX-запросы, выполняемые в том же контексте, что и API, с которым они взаимодействуют, обычно используют `SessionAuthentication`. Это гарантирует, что после того, как пользователь вошел в систему, любые запросы AJAX могут быть аутентифицированы с помощью той же сеансовой аутентификации, которая используется для остальной части сайта.

AJAX requests that are made on a different site from the API they are communicating with will typically need to use a non-session-based authentication scheme, such as `TokenAuthentication`.

AJAX-запросы, которые выполняются на сайте, отличном от сайта API, с которым они взаимодействуют, обычно должны использовать схему аутентификации, не основанную на сеансах, например `TokenAuthentication`.

## CSRF protection

## Защита от CSRF

[Cross Site Request Forgery](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) protection is a mechanism of guarding against a particular type of attack, which can occur when a user has not logged out of a web site, and continues to have a valid session. In this circumstance a malicious site may be able to perform actions against the target site, within the context of the logged-in session.

[Защита от подделки межсайтовых запросов (https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) - это механизм защиты от определенного типа атак, которые могут возникнуть, когда пользователь не вышел с веб-сайта и продолжает иметь действующую сессию. В этом случае вредоносный сайт может выполнить действия против целевого сайта в контексте вошедшей сессии.

To guard against these type of attacks, you need to do two things:

Чтобы защититься от такого рода атак, вам нужно сделать две вещи:

1. Ensure that the 'safe' HTTP operations, such as `GET`, `HEAD` and `OPTIONS` cannot be used to alter any server-side state.
2. Ensure that any 'unsafe' HTTP operations, such as `POST`, `PUT`, `PATCH` and `DELETE`, always require a valid CSRF token.

1. Убедитесь, что "безопасные" операции HTTP, такие как `GET`, `HEAD` и `OPTIONS`, не могут быть использованы для изменения состояния на стороне сервера.
2. Убедитесь, что для любых "небезопасных" операций HTTP, таких как `POST`, `PUT`, `PATCH` и `DELETE`, всегда требуется действительный токен CSRF.

If you're using `SessionAuthentication` you'll need to include valid CSRF tokens for any `POST`, `PUT`, `PATCH` or `DELETE` operations.

Если вы используете `SessionAuthentication`, вам необходимо включить действительные CSRF-токены для любых операций `POST`, `PUT`, `PATCH` или `DELETE`.

In order to make AJAX requests, you need to include CSRF token in the HTTP header, as [described in the Django documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

Чтобы выполнять AJAX-запросы, необходимо включить CSRF-токен в HTTP-заголовок, как [описано в документации Django](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

## CORS

## CORS

[Cross-Origin Resource Sharing](https://www.w3.org/TR/cors/) is a mechanism for allowing clients to interact with APIs that are hosted on a different domain. CORS works by requiring the server to include a specific set of headers that allow a browser to determine if and when cross-domain requests should be allowed.

[Cross-Origin Resource Sharing] (https://www.w3.org/TR/cors/) - это механизм, позволяющий клиентам взаимодействовать с API, размещенными на другом домене. CORS работает, требуя от сервера включения определенного набора заголовков, которые позволяют браузеру определить, разрешены ли междоменные запросы и когда они должны быть разрешены.

The best way to deal with CORS in REST framework is to add the required response headers in middleware. This ensures that CORS is supported transparently, without having to change any behavior in your views.

Лучший способ справиться с CORS в REST-фреймворке - добавить необходимые заголовки ответа в промежуточное ПО. Это гарантирует, что CORS поддерживается прозрачно, без необходимости изменять какое-либо поведение в ваших представлениях.

[Adam Johnson](https://github.com/adamchainz) maintains the [django-cors-headers](https://github.com/adamchainz/django-cors-headers) package, which is known to work correctly with REST framework APIs.

[Adam Johnson](https://github.com/adamchainz) поддерживает пакет [django-cors-headers](https://github.com/adamchainz/django-cors-headers), который, как известно, корректно работает с API REST-фреймворков.