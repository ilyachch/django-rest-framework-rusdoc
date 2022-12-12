<!-- TRANSLATED by md-translate -->
# REST, Hypermedia & HATEOAS

# Rest, Hypermedia & Hateoas

> You keep using that word "REST". I do not think it means what you think it means.
>
> — Mike Amundsen, [REST fest 2012 keynote](https://vimeo.com/channels/restfest/49503453).

> Вы продолжаете использовать это слово «отдых».
Я не думаю, что это означает, что вы думаете, это означает.
>
> - Майк Амундсен, [Rest Fest 2012 Keynote] (https://vimeo.com/channels/restfest/49503453).

First off, the disclaimer. The name "Django REST framework" was decided back in early 2011 and was chosen simply to ensure the project would be easily found by developers. Throughout the documentation we try to use the more simple and technically correct terminology of "Web APIs".

Во -первых, отказ от ответственности.
Название «Django Rest Framework» было решено еще в начале 2011 года и было выбрано просто для того, чтобы разработчики были легко найдены.
На протяжении всей документации мы стараемся использовать более простую и технически правильную терминологию «веб -API».

If you are serious about designing a Hypermedia API, you should look to resources outside of this documentation to help inform your design choices.

Если вы серьезно относитесь к разработке API Hypermedia, вам следует обратить внимание на ресурсы за пределами этой документации, чтобы помочь сообщить ваш дизайн.

The following fall into the "required reading" category.

Следующее попадает в категорию «Требуемое чтение».

* Roy Fielding's dissertation - [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).
* Roy Fielding's "[REST APIs must be hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)" blog post.
* Leonard Richardson & Mike Amundsen's [RESTful Web APIs](http://restfulwebapis.org/).
* Mike Amundsen's [Building Hypermedia APIs with HTML5 and Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578).
* Steve Klabnik's [Designing Hypermedia APIs](http://designinghypermediaapis.com/).
* The [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html).

* Диссертация Роя Филдинга - [архитектурные стили и дизайн сетевых программных архитектур] (https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).
* Рой Филдинг "[Rest API должен быть гипертекстовым] (https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-vinged)" в блоге.
* Леонард Ричардсон и Майк Амундсен [Restful Web API] (http://restfulwebapis.org/).
* Mike Amundsen's [Строительство гипермедиа API с html5 и node] (https://www.amazon.com/building-hypermedia-apis-html5-node/dp/1449306578).
* [Designing Hypermedia APIS Стива Клабника (http://designinghypermediaapis.com/).
* [Модель зрелости Ричардсона] (https://martinfowler.com/articles/richardsonmaturitymodel.html).

For a more thorough background, check out Klabnik's [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list).

Чтобы получить более тщательный фон, ознакомьтесь с списком чтения API Klabnik [http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list).

## Building Hypermedia APIs with REST framework

## Создание API -интерфейсов гипермедиа с рамками REST

REST framework is an agnostic Web API toolkit. It does help guide you towards building well-connected APIs, and makes it easy to design appropriate media types, but it does not strictly enforce any particular design style.

Framework REST - это агностический веб -инструментарий API.
Это помогает вам направить вас к созданию хорошо связанных API, и позволяет легко разработать соответствующие типы носителей, но он не строго соблюдает какой-либо конкретный стиль дизайна.

## What REST framework provides.

## Что обеспечивает структура REST.

It is self evident that REST framework makes it possible to build Hypermedia APIs. The browsable API that it offers is built on HTML - the hypermedia language of the web.

Само очевидно, что структура REST позволяет создавать API -интерфейсы гипермедиа.
Производительный API, который он предлагает, построен на HTML - языке гипермедиа в Интернете.

REST framework also includes [serialization](../api-guide/serializers.md) and [parser](../api-guide/parsers.md)/[renderer](../api-guide/renderers.md) components that make it easy to build appropriate media types, [hyperlinked relations](../api-guide/fields.md) for building well-connected systems, and great support for [content negotiation](../api-guide/content-negotiation.md).

Структура REST также включает в себя [Serialization] (../ API-Guide/Serializers.md) и [Parser] (../ API-Guide/Parsers.md)/[renderer] (../ api-guide/renderers.md
) Компоненты, которые облегчают создание соответствующих типов средств массовой информации, [гиперсвязанные отношения] (../ API-Guide/Fields.md) для создания хорошо связанных систем и большую поддержку [переговоры о контенте] (../ api-guide
/content-negotiation.md).

## What REST framework doesn't provide.

## ЧТО ПРИМЕНЕНИ НЕ ДОЛЖЕН.

What REST framework doesn't do is give you machine readable hypermedia formats such as [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) or HTML [microformats](http://microformats.org/wiki/Main_Page) by default, or the ability to auto-magically create fully HATEOAS style APIs that include hypermedia-based form descriptions and semantically labelled hyperlinks. Doing so would involve making opinionated choices about API design that should really remain outside of the framework's scope.

Что не делает каркас REST, так это дает вам машинный гипермедиа, такие как [hal] (http://statess.co/hal_speciation.html), [collection+json] (http://www.amundsen.com/media
-types/collection/), [json api] (http://jsonapi.org/) или html [microformats] (http://microformats.org/wiki/main_page) по умолчанию или способность автомагически создавать
Полностью API-интерфейсы в стиле Hateoas, которые включают описания форм на основе гипермедиа и семантически маркированные гиперссылки.
Это будет включать в себя самоуверенный выбор в отношении дизайна API, который действительно должен оставаться вне сферы действия структуры.