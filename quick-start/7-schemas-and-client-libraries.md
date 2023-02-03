<!-- TRANSLATED by md-translate -->
# Урок 7: Схемы и клиентские библиотеки

---

**УВЕДОМЛЕНИЕ О УСТАРЕВАНИИ:** Использование схем на базе CoreAPI было отмечено устаревшим с введением генерации схем на базе OpenAPI в Django REST Framework v3.10. Более подробную информацию смотрите в [Version 3.10 Release Announcement](https://github.com/encode/django-rest-framework/blob/master/docs/community/3.10-announcement.md).

Если вы ищете информацию о схемах, обратите внимание на эти обновленные ресурсы:

1. [Схемы](../api-guide/schemas.md)
2. [Документирование вашего API](../topics/documenting-your-api.md)

---

Схема - это машиночитаемый документ, который описывает доступные конечные точки API, их URL-адреса и операции, которые они поддерживают.

Схемы могут быть полезным инструментом для автоматической генерации документации, а также могут использоваться для создания динамических клиентских библиотек, которые могут взаимодействовать с API.

## Core API

Для обеспечения поддержки схем REST framework использует [Core API](https://www.coreapi.org/).

Core API - это спецификация документа для описания API. Спецификация используется для обеспечения внутреннего формата представления доступных конечных точек и возможных взаимодействий, которые API раскрывает. Документ может использоваться как на стороне сервера, так и на стороне клиента.

При использовании на стороне сервера Core API позволяет API поддерживать рендеринг в широкий спектр форматов схем или гипермедиа.

При использовании на стороне клиента, Core API позволяет создавать динамически управляемые клиентские библиотеки, которые могут взаимодействовать с любым API, раскрывающим поддерживаемую схему или формат гипермедиа.

## Добавление схемы

REST framework поддерживает либо явно определенные представления схем, либо автоматически сгенерированные схемы. Поскольку мы используем наборы представлений и маршрутизаторы, мы можем просто использовать автоматическую генерацию схем.

Вам потребуется установить пакет `coreapi` python, чтобы включить схему API, и `pyyaml` для преобразования схемы в широко используемый формат OpenAPI на основе YAML.

```bash
$ pip install coreapi pyyaml
```

Теперь мы можем включить схему для нашего API, включив автогенерируемое представление схемы в конфигурацию URL.

```python
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('schema/', schema_view),
    ...
]
```

Если вы посетите конечную точку `/schema/` в браузере, вы должны увидеть, что представление `corejson` стало доступно в качестве опции.

![Формат схемы](https://github.com/encode/django-rest-framework/blob/master/docs/img/corejson-format.png?raw=true)

Мы также можем запросить схему из командной строки, указав желаемый тип содержимого в заголовке `Accept`.

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

По умолчанию используется формат [Core JSON](https://www.coreapi.org/specification/encoding/#core-json-encoding).

Поддерживаются и другие форматы схем, такие как [Open API](https://openapis.org/) (ранее Swagger).

## Использование клиента командной строки

Теперь, когда наш API открывает конечную точку схемы, мы можем использовать динамическую клиентскую библиотеку для взаимодействия с API. Чтобы продемонстрировать это, давайте воспользуемся клиентом командной строки Core API.

Клиент командной строки доступен в виде пакета `coreapi-cli`:

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

Сначала мы загрузим схему API с помощью клиента командной строки.

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

Мы еще не аутентифицировались, поэтому сейчас мы можем видеть только конечные точки, доступные только для чтения, в соответствии с тем, как мы установили разрешения на API.

Давайте попробуем перечислить существующие фрагменты, используя клиент командной строки:

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

Некоторые конечные точки API требуют именованных параметров. Например, чтобы получить HTML-выделение для конкретного фрагмента, необходимо указать его идентификатор.

```bash
$ coreapi action snippets highlight --param id=1
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
  <title>Example</title>
  ...
```

## Аутентификация нашего клиента

Если мы хотим иметь возможность создавать, редактировать и удалять сниппеты, нам необходимо пройти аутентификацию в качестве валидного пользователя. В данном случае мы просто используем базовую авторизацию.

Обязательно замените указанные ниже `<username>` и `<password>` на ваши реальные имя пользователя и пароль.

```bash
$ coreapi credentials add 127.0.0.1 <username>:<password> --auth basic
Added credentials
127.0.0.1 "Basic <...>"
```

Теперь, если мы снова получим схему, мы сможем увидеть полный набор доступных взаимодействий.

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

И удалить фрагмент:

```bash
$ coreapi action snippets delete --param id=7
```

Помимо клиента командной строки, разработчики могут взаимодействовать с вашим API с помощью клиентских библиотек. Клиентская библиотека для Python является первой из них, а в ближайшее время планируется выпуск клиентской библиотеки для Javascript.

Для получения более подробной информации о настройке генерации схем и использовании клиентских библиотек Core API вам необходимо обратиться к полной документации.

## Обзор нашей работы

С невероятно малым количеством кода мы теперь имеем полноценный веб-интерфейс API pastebin, который полностью доступен для просмотра в Интернете, включает клиентскую библиотеку, управляемую схемой, и поставляется в комплекте с аутентификацией, разрешениями для каждого объекта и несколькими форматами рендеринга.

Мы прошли через каждый шаг процесса проектирования и увидели, что если нам нужно что-то изменить, мы можем постепенно перейти к использованию обычных представлений Django.

You can review the final [tutorial code](https://github.com/encode/rest-framework-tutorial) on GitHub, or try out a live example in [the sandbox](https://restframework.herokuapp.com/).

Вы можете просмотреть окончательный [код учебного проекта](https://github.com/encode/rest-framework-tutorial) на GitHub или опробовать живой пример в [песочнице](https://restframework.herokuapp.com/).

## Вперед и вверх

Мы подошли к концу нашего учебника. Если вы хотите принять более активное участие в проекте REST framework, вот несколько мест, с которых вы можете начать:

* Вносите свой вклад на [GitHub](https://github.com/encode/django-rest-framework), просматривая и отправляя проблемы, а также делая запросы на исправление.
* Присоединяйтесь к [группе обсуждения REST-фреймворка](https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework) и помогайте развивать сообщество.
* Следите за [автором](https://twitter.com/_tomchristie) в Twitter и передавайте привет.

**А теперь идите и делайте удивительные вещи.**
