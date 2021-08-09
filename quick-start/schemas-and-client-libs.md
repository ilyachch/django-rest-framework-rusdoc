# Урок 7: Схемы и клиентские библиотеки

Схема представляет собой машиночитаемый документ, который описывает доступные конечные точки API, их адреса, и какие операции они поддерживают.

Схемы могут быть полезным инструментом для автоматически создаваемой документации, а также могут быть использованы для динамических клиентских библиотек, которые могут взаимодействовать с API.

## Core API

Для того, чтобы обеспечить поддержку схем DRF использует [Core API][coreapi].

Core API - это спецификация документа для описания интерфейсов. Она используется для того чтобы обеспечить внутреннее представление формата доступных конечных точек и возможные взаимодействия, которые предоставляет API. Она может быть использована на стороне сервера или на стороне клиента.

При использовании на сервере, Core API позволяет API поддерживать широкий спектр схем или форматов гипермедиа.

При использовании на стороне клиента, Core API позволяет динамически управляемым клиентским библиотекам, которые могут взаимодействовать с любым API, который предоставляет поддерживаемые схемы или формат гипермедиа.

## Добавление схемы

DRF поддерживает либо явно определенные представления схем, либо автоматически сгенерированные схемы. Поскольку мы используем viewsets и маршрутизаторы, мы можем просто использовать автоматическую генерацию схемы.

Вам потребуется установить python пакет `coreapi` для того, чтобы создать API-схемы и `pyyaml` для отображения схемы в наиболее часто используемом, основанном на YAML, формате OpenAPI.

```bash
$ pip install coreapi pyyaml
```

Теперь мы можем включить схему для нашего API, добавив автоматически созданную схему в нашу конфигурацию URL-адресов.

```python
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('schema/', schema_view),
    ...
]
```

Если вы посетите `/schema/` в браузере, теперь вы должны увидеть, что `corejson` представление станет доступено в качестве опции.

![Schema format](https://github.com/encode/django-rest-framework/raw/master/docs/img/corejson-format.png)

Мы также можем запросить схему из командной строки, указав необходимый тип содержимого в заголовке `Accept`.

```bash
$ http http://127.0.0.1:8000/schema/ Accept:application/coreapi+json
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/coreapi+json

{
    "_meta": {
        "title": "Pastebin API"
    },
    "_type": "document",
    ...
```

По умолчанию, используется [Core JSON][corejson] формат.

Другие форматы схем, таких как [Open API][openapi] (ранее Swagger) также поддерживаются.

## Использование консольного клиента

Теперь, когда наш API предоставляет конечную точку схемы, мы можем использовать динамические клиентские библиотеки для взаимодействия с API. Чтобы продемонстрировать это, воспользуемся Core API CLI-утилитой.

Консольный клиент доступен как в пакете `coreapi-cli`:

```bash
$ pip install coreapi-cli
```

Теперь проверьте, что он доступен в командной строке...

```bash
$ coreapi
Usage: coreapi [OPTIONS] COMMAND [ARGS]...

    Command line client for interacting with CoreAPI services.

    Visit https://www.coreapi.org/ for more information.

Options:
    --version  Display the package version number.
    --help     Show this message and exit.

Commands:
...
```

Сначала мы загрузим схему API с помощью консольного клиента.

```bash
$ coreapi get http://127.0.0.1:8000/schema/
<Pastebin API "http://127.0.0.1:8000/schema/">
    snippets: {
        highlight(id)
        list()
        read(id)
    }
    users: {
        list()
        read(id)
    }
```

Мы еще не авторизовались, поэтому сейчас мы можем увидеть конечные точки, доступные только для чтения, в соответствии с тем, как мы настроели разрешения в API.

Давайте попробуем вывести список существующих фрагментов с помощью консольного клиента:

```bash
$ coreapi action snippets list
[
    {
        "url": "http://127.0.0.1:8000/snippets/1/",
        "id": 1,
        "highlight": "http://127.0.0.1:8000/snippets/1/highlight/",
        "owner": "lucy",
        "title": "Example",
        "code": "print('hello, world!')",
        "linenos": true,
        "language": "python",
        "style": "friendly"
    },
    ...
```

Некоторые из конечных точек API требуют именованные параметры. Например, чтобы вернуть подсвеченный HTML-код для конкретного сниппета нужно предоставить id.

```bash
$ coreapi action snippets highlight --param id=1
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
    <title>Example</title>
    ...
```

## Авторизация клиента

Если мы хотим иметь возможность создавать, редактировать и удалять сниппеты, нам понадобится авторизоваться. В этом случае мы будем использовать базовую аутентификацию.

Убедитесь в том, что вы заменили `<username>` и `<password>` вашими именем пользователя и паролем.

```bash
$ coreapi credentials add 127.0.0.1 <username>:<password> --auth basic
Added credentials
127.0.0.1 "Basic <...>"
```

Теперь, если мы снова запросим схему, мы должны быть в состоянии видеть полный набор имеющихся взаимодействий.

```bash
$ coreapi reload
Pastebin API "http://127.0.0.1:8000/schema/">
    snippets: {
        create(code, [title], [linenos], [language], [style])
        delete(id)
        highlight(id)
        list()
        partial_update(id, [title], [code], [linenos], [language], [style])
        read(id)
        update(id, code, [title], [linenos], [language], [style])
    }
    users: {
        list()
        read(id)
    }
```

Теперь мы можем взаимодействовать с этими конечными точками. Например, чтобы создать новый сниппет:

```bash
$ coreapi action snippets create --param title="Example" --param code="print('hello, world')"
{
    "url": "http://127.0.0.1:8000/snippets/7/",
    "id": 7,
    "highlight": "http://127.0.0.1:8000/snippets/7/highlight/",
    "owner": "lucy",
    "title": "Example",
    "code": "print('hello, world')",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

И чтобы удалить фрагмент:

```bash
$ coreapi action snippets delete --param id=7
```

Так же как и консольный клиент, разработчики могут взаимодействовать с API с помощью клиентских библиотек. Клиентская библиотека Python - первая из доступных, и клиентская библиотека JavaScript, как планируется, будет выпущена в ближайшее время.

Для получения более подробной информации о настройке формирования схем и использование базовых API клиентской библиотеки вам необходимо обратиться к полной документации.

## Оглядываясь назад

С помощью невероятно малого количества кода, теперь у нас есть полноценное Pastebin веб-API с возможностью просмотра в веб-браузере, которое включает в себя возможность управления клиентской библиотекой, поставляется в комплекте с авторизацией, разделением прав на объект, и несколькими форматами визуализации.

Мы прошли через каждый шаг процесса проектирования и видели, как, если нам нужно настроить все, мы можем постепенно спускаться вниз, чтобы просто использловать Django представления.

Вы можете просмотреть окончательной [код учебника][repo] на GitHub, или попробовать живой пример в [песочнице][sandbox].

## Вперед и вверх

Мы достигли конца нашего учебника. Если вы хотите принять более активное участие в развитии проекта DRF, вот несколько мест, с которых вы можете начать:

* Сделайте вклад на [GitHub][github] просматривая и создавая ишью, а так же создавая пулл-реквесты.
* Присоединяйтесь к [REST framework discussion group][group], и помогайте в создании и развитии сообщества.
* Подписывайтесь на [авторов][twitter] в Twitter и скажите "Привет"=).

**А теперь идите и создавайте крутые вещи.**

[coreapi]: https://www.coreapi.org/
[corejson]: https://www.coreapi.org/specification/encoding/#core-json-encoding
[openapi]: https://openapis.org/
[repo]: https://github.com/encode/rest-framework-tutorial
[sandbox]: https://restframework.herokuapp.com/
[github]: https://github.com/encode/django-rest-framework
[group]: https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework
[twitter]: https://twitter.com/_tomchristie
