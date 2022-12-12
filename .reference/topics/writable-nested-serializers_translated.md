<!-- TRANSLATED by md-translate -->
> To save HTTP requests, it may be convenient to send related documents along with the request.
>
> — [JSON API specification for Ember Data](http://jsonapi.org/format/#url-based-json-api).

> Чтобы сохранить HTTP -запросы, может быть удобно отправлять связанные документы вместе с запросом.
>
>-[JSON API-спецификация для данных Ember] (http://jsonapi.org/format/#url на основе json-api).

# Writable nested serializers

# Вложенные сериалы для записи

Although flat data structures serve to properly delineate between the individual entities in your service, there are cases where it may be more appropriate or convenient to use nested data structures.

Хотя плоские структуры данных служат для правильного разграничения между отдельными объектами в вашей службе, есть случаи, когда может быть более подходящим или удобным для использования вложенных структур данных.

Nested data structures are easy enough to work with if they're read-only - simply nest your serializer classes and you're good to go. However, there are a few more subtleties to using writable nested serializers, due to the dependencies between the various model instances, and the need to save or delete multiple instances in a single action.

Вложенные структуры данных достаточно просты для работы, если они только для чтения - просто гнездируйте классы сериализатора, и все готово.
Тем не менее, есть еще несколько тонкостей использования вложенных сериалов с записи, из -за зависимостей между различными экземплярами модели и необходимостью сохранения или удаления нескольких экземпляров в одном действии.

## One-to-many data structures

## Структуры данных One-More

*Example of a **read-only** nested serializer. Nothing complex to worry about here.*

*Пример ** только для чтения ** вложенного сериализатора.
Здесь не о чем беспокоиться.*

```
class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ['text', 'is_completed']

class ToDoListSerializer(serializers.ModelSerializer):
    items = ToDoItemSerializer(many=True, read_only=True)

    class Meta:
        model = ToDoList
        fields = ['title', 'items']
```

Some example output from our serializer.

Некоторый пример вывода из нашего сериализатора.

```
{
    'title': 'Leaving party preparations',
    'items': [
        {'text': 'Compile playlist', 'is_completed': True},
        {'text': 'Send invites', 'is_completed': False},
        {'text': 'Clean house', 'is_completed': False}
    ]
}
```

Let's take a look at updating our nested one-to-many data structure.

Давайте посмотрим на обновление нашей вложенной структуры данных с одним ко многим.

### Validation errors

### Ошибки проверки

### Adding and removing items

### Добавление и удаление элементов

### Making PATCH requests

### Запросы на патч