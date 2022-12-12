<!-- TRANSLATED by md-translate -->
# Working with AJAX, CSRF & CORS

# Работа с AJAX, CSRF и CORS

> "Take a close look at possible CSRF / XSRF vulnerabilities on your own websites.  They're the worst kind of vulnerability &mdash; very easy to exploit by attackers, yet not so intuitively easy to understand for software developers, at least until you've been bitten by one."
>
> &mdash; [Jeff Atwood](https://blog.codinghorror.com/preventing-csrf-and-xsrf-attacks/)

> «Внимательно посмотрите на возможные уязвимости CSRF / XSRF на ваших собственных веб -сайтах. Это худший вид уязвимости и MDASH; очень легко использовать злоумышленники, но не так интуитивно легко понять для разработчиков программного обеспечения, по крайней мере, пока вы.
был укушен одним ".
>
> & mdash;
[Джефф Этвуд] (https://blog.codinghorror.com/preventing-csrf-and-xsrf-attacks/)

## Javascript clients

## javascript клиенты

If you’re building a JavaScript client to interface with your Web API, you'll need to consider if the client can use the same authentication policy that is used by the rest of the website, and also determine if you need to use CSRF tokens or CORS headers.

Если вы создаете клиент JavaScript для взаимодействия с вашим веб -API, вам нужно рассмотреть, может ли клиент использовать ту же политику аутентификации, которая используется остальной частью веб -сайта, а также определить, нужно ли вам использовать токены CSRF
или заголовки CORS.

AJAX requests that are made within the same context as the API they are interacting with will typically use `SessionAuthentication`.  This ensures that once a user has logged in, any AJAX requests made can be authenticated using the same session-based authentication that is used for the rest of the website.

Запросы AJAX, которые выполняются в том же контексте, что и API, с которым они взаимодействуют, обычно используют `sessionAuthentication '.
Это гарантирует, что после того, как пользователь вошел в систему, любые сделанные запросы AJAX могут быть аутентифицированы с использованием той же аутентификации на основе сеанса, которая используется для остальной части веб-сайта.

AJAX requests that are made on a different site from the API they are communicating with will typically need to use a non-session-based authentication scheme, such as `TokenAuthentication`.

Запросы AJAX, которые выполняются на другом сайте, от API, с которым они общаются, обычно необходимо использовать не-сессию схему аутентификации, такую как «Tokenauthentication».

## CSRF protection

## защита CSRF

[Cross Site Request Forgery](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) protection is a mechanism of guarding against a particular type of attack, which can occur when a user has not logged out of a web site, and continues to have a valid session.   In this circumstance a malicious site may be able to perform actions against the target site, within the context of the logged-in session.

[Перекрестная подделка запроса запроса] (https://www.owasp.org/index.php/cross-site_request_forgery_ (csrf)) Защита-это механизм охраны от определенного типа атаки, который может возникнуть, когда пользователь не зарегистрировался
Из веб -сайта и продолжает иметь действительный сеанс.
В этом случае злонамеренный сайт может выполнять действия против целевого сайта, в контексте регистрации сеанса.

To guard against these type of attacks, you need to do two things:

Чтобы защитить от такого типа атак, вам нужно сделать две вещи:

1. Ensure that the 'safe' HTTP operations, such as `GET`, `HEAD` and `OPTIONS` cannot be used to alter any server-side state.
2. Ensure that any 'unsafe' HTTP operations, such as `POST`, `PUT`, `PATCH` and `DELETE`, always require a valid CSRF token.

1. Убедитесь, что операции «безопасные» HTTP, такие как «get», `head 'и` options' не могут быть использованы для изменения любого состояния на стороне сервера.
2. Убедитесь, что любые «небезопасные» HTTP -операции, такие как «post», «put», «patch» и «Delete», всегда требуют действительного токена CSRF.

If you're using `SessionAuthentication` you'll need to include valid CSRF tokens for any `POST`, `PUT`, `PATCH` or `DELETE` operations.

Если вы используете `sessionAuthentication`, вам нужно будет включить допустимые токены CSRF для любых операций` post`, `put ',` patch` или `delete`.

In order to make AJAX requests, you need to include CSRF token in the HTTP header, as [described in the Django documentation](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

Чтобы сделать запросы AJAX, вам необходимо включить токен CSRF в заголовок HTTP, как [описано в документации Django] (https://docs.djangoproject.com/en/stable/ref/csrf/#ajax).

## CORS

## cors

[Cross-Origin Resource Sharing](https://www.w3.org/TR/cors/) is a mechanism for allowing clients to interact with APIs that are hosted on a different domain.  CORS works by requiring the server to include a specific set of headers that allow a browser to determine if and when cross-domain requests should be allowed.

[Обмен ресурсами кросс-аоригина] (https://www.w3.org/tr/cors/)-это механизм, позволяющий клиентам взаимодействовать с API, которые размещены в другом домене.
CORS работает, требуя, чтобы сервер включал определенный набор заголовков, которые позволяют браузеру определять, должны ли и когда перекрестные запросы должны быть разрешены.

The best way to deal with CORS in REST framework is to add the required response headers in middleware.  This ensures that CORS is supported transparently, without having to change any behavior in your views.

Лучший способ справиться с CORS в рамках REST - это добавить необходимые заголовки ответов в промежуточном программном обеспечении.
Это гарантирует, что CORS поддерживается прозрачно, без необходимости менять какое -либо поведение в ваших взглядах.

[Adam Johnson](https://github.com/adamchainz) maintains the [django-cors-headers](https://github.com/adamchainz/django-cors-headers) package, which is known to work correctly with REST framework APIs.

[Adam Johnson] (https://github.com/adamchainz) поддерживает пакет [django-cors-horers] (https://github.com/adamchainz/django-cors headers), который, как известно, работает правильно с
REST FRACEWORD API.