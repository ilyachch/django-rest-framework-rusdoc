<!-- TRANSLATED by md-translate -->
# REST, гипермедиа и HATEOAS

> Вы продолжаете использовать это слово "REST". Я не думаю, что оно означает то, что вы думаете, что оно означает.
>
> - Майк Амундсен, [REST fest 2012 keynote](https://vimeo.com/channels/restfest/49503453).

Во-первых, отказ от ответственности. Название "Django REST framework" было принято еще в начале 2011 года и было выбрано просто для того, чтобы разработчики могли легко найти проект. Во всей документации мы стараемся использовать более простую и технически корректную терминологию "Web API".

Если вы серьезно относитесь к разработке Hypermedia API, вам следует обратиться к ресурсам за пределами этой документации, чтобы помочь в выборе дизайна.

Следующее относится к категории "обязательного чтения".

- Диссертация Роя Филдинга - [Архитектурные стили и проектирование сетевых архитектур программного обеспечения](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).

- Запись в блоге Роя Филдинга "[REST API должны быть гипертекстовыми](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)".

- Leonard Richardson & Mike Amundsen's [RESTful Web APIs](http://restfulwebapis.org/).

- Mike Amundsen's [Building Hypermedia APIs with HTML5 and Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578).

- Steve Klabnik's [Designing Hypermedia APIs](http://designinghypermediaapis.com/).

- [Модель зрелости Ричардсона](https://martinfowler.com/articles/richardsonMaturityModel.html).

For a more thorough background, check out Klabnik's [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list).

Для получения более подробной информации ознакомьтесь со списком [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list) Клабника.

## Создание гипермедийных API с помощью DRF

DRF - это агностический инструментарий Web API. Он помогает ориентироваться в создании хорошо связанных API и облегчает разработку соответствующих типов носителей, но не обеспечивает строгого соблюдения какого-либо определенного стиля оформления.

## Что предоставляетсобой DRF.

Само собой разумеется, что DRF позволяет создавать гипермедийные API. Web-интерфейс API, который он предлагает, построен на HTML - гипермедийном языке Интернета.

DRF также включает [serialization](../api-guide/serializers.md) и [parser](../api-guide/parsers.md)/[renderer](../api-guide/renderers.md), которые облегчают создание соответствующих типов медиа, [гиперсвязанные отношения](../api-guide/fields.md) для создания хорошо связанных систем, и отличная поддержка [согласования контента](../api-guide/content-negotiation.md).

## Чего не предоставляет DRF.

Чего DRF не делает, так это не дает вам машиночитаемых гипермедийных форматов, таких как [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) или HTML [microformats](http://microformats.org/wiki/Main_Page) по умолчанию, или возможности автоматически создавать API в стиле HATEOAS, которые включают гипермедийные описания форм и семантически маркированные гиперссылки. Это потребует принятия решений о дизайне API, которые должны оставаться за пределами сферы применения фреймворка.
