<!-- TRANSLATED by md-translate -->
# REST, Hypermedia & HATEOAS

# REST, гипермедиа и HATEOAS

> You keep using that word "REST". I do not think it means what you think it means.
>
> — Mike Amundsen, [REST fest 2012 keynote](https://vimeo.com/channels/restfest/49503453).

> Вы продолжаете использовать это слово "REST". Я не думаю, что оно означает то, что вы думаете, что оно означает.
>
> - Майк Амундсен, [REST fest 2012 keynote](https://vimeo.com/channels/restfest/49503453).

First off, the disclaimer. The name "Django REST framework" was decided back in early 2011 and was chosen simply to ensure the project would be easily found by developers. Throughout the documentation we try to use the more simple and technically correct terminology of "Web APIs".

Во-первых, отказ от ответственности. Название "Django REST framework" было принято еще в начале 2011 года и было выбрано просто для того, чтобы разработчики могли легко найти проект. Во всей документации мы стараемся использовать более простую и технически корректную терминологию "Web API".

If you are serious about designing a Hypermedia API, you should look to resources outside of this documentation to help inform your design choices.

Если вы серьезно относитесь к разработке Hypermedia API, вам следует обратиться к ресурсам за пределами этой документации, чтобы помочь в выборе дизайна.

The following fall into the "required reading" category.

Следующее относится к категории "обязательного чтения".

* Roy Fielding's dissertation - [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).
* Roy Fielding's "[REST APIs must be hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)" blog post.
* Leonard Richardson & Mike Amundsen's [RESTful Web APIs](http://restfulwebapis.org/).
* Mike Amundsen's [Building Hypermedia APIs with HTML5 and Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578).
* Steve Klabnik's [Designing Hypermedia APIs](http://designinghypermediaapis.com/).
* The [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html).

* Диссертация Роя Филдинга - [Архитектурные стили и проектирование сетевых архитектур программного обеспечения] (https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).
* Запись в блоге Роя Филдинга "[REST API должны быть гипертекстовыми](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)".
* Leonard Richardson & Mike Amundsen's [RESTful Web APIs](http://restfulwebapis.org/).
* Mike Amundsen's [Building Hypermedia APIs with HTML5 and Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578).
* Steve Klabnik's [Designing Hypermedia APIs](http://designinghypermediaapis.com/).
* [Модель зрелости Ричардсона](https://martinfowler.com/articles/richardsonMaturityModel.html).

For a more thorough background, check out Klabnik's [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list).

Для получения более подробной информации ознакомьтесь со списком [Hypermedia API reading list] (http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list) Клабника.

## Building Hypermedia APIs with REST framework

## Создание гипермедийных API с помощью REST-фреймворка

REST framework is an agnostic Web API toolkit. It does help guide you towards building well-connected APIs, and makes it easy to design appropriate media types, but it does not strictly enforce any particular design style.

REST framework - это агностический инструментарий Web API. Он помогает ориентироваться в создании хорошо связанных API и облегчает разработку соответствующих типов носителей, но не обеспечивает строгого соблюдения какого-либо определенного стиля оформления.

## What REST framework provides.

## Что предоставляет фреймворк REST.

It is self evident that REST framework makes it possible to build Hypermedia APIs. The browsable API that it offers is built on HTML - the hypermedia language of the web.

Само собой разумеется, что REST-фреймворк позволяет создавать гипермедийные API. Просматриваемый API, который он предлагает, построен на HTML - гипермедийном языке Интернета.

REST framework also includes [serialization](../api-guide/serializers.md) and [parser](../api-guide/parsers.md)/[renderer](../api-guide/renderers.md) components that make it easy to build appropriate media types, [hyperlinked relations](../api-guide/fields.md) for building well-connected systems, and great support for [content negotiation](../api-guide/content-negotiation.md).

REST framework также включает [serialization](../api-guide/serializers.md) и [parser](../api-guide/parsers.md)/[renderer](../api-guide/renderers. md), которые облегчают создание соответствующих типов медиа, [гиперсвязанные отношения](../api-guide/fields.md) для создания хорошо связанных систем, и отличная поддержка [согласования контента](../api-guide/content-negotiation.md).

## What REST framework doesn't provide.

## Чего не предоставляет REST-фреймворк.

What REST framework doesn't do is give you machine readable hypermedia formats such as [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) or HTML [microformats](http://microformats.org/wiki/Main_Page) by default, or the ability to auto-magically create fully HATEOAS style APIs that include hypermedia-based form descriptions and semantically labelled hyperlinks. Doing so would involve making opinionated choices about API design that should really remain outside of the framework's scope.

Чего REST framework не делает, так это не дает вам машиночитаемых гипермедийных форматов, таких как [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) или HTML [microformats](http://microformats.org/wiki/Main_Page) по умолчанию, или возможности автоматически создавать API в стиле HATEOAS, которые включают гипермедийные описания форм и семантически маркированные гиперссылки. Это потребует принятия решений о дизайне API, которые должны оставаться за пределами сферы применения фреймворка.