<!-- TRANSLATED by md-translate -->
> To save HTTP requests, it may be convenient to send related documents along with the request.
>
> — [JSON API specification for Ember Data](http://jsonapi.org/format/#url-based-json-api).

> Для экономии HTTP-запросов может быть удобно отправлять вместе с запросом сопутствующие документы.
>
> - [Спецификация JSON API для Ember Data](http://jsonapi.org/format/#url-based-json-api).

# Writable nested serializers

# Вложенные сериализаторы с возможностью записи

Although flat data structures serve to properly delineate between the individual entities in your service, there are cases where it may be more appropriate or convenient to use nested data structures.

Хотя плоские структуры данных служат для правильного разграничения отдельных сущностей в вашем сервисе, бывают случаи, когда более целесообразно или удобно использовать вложенные структуры данных.

Nested data structures are easy enough to work with if they're read-only - simply nest your serializer classes and you're good to go. However, there are a few more subtleties to using writable nested serializers, due to the dependencies between the various model instances, and the need to save or delete multiple instances in a single action.

С вложенными структурами данных достаточно легко работать, если они доступны только для чтения - просто вложите классы сериализатора, и все готово. Однако при использовании вложенных сериализаторов с возможностью записи есть еще несколько тонкостей, связанных с зависимостями между различными экземплярами модели и необходимостью сохранения или удаления нескольких экземпляров одним действием.

## One-to-many data structures

## Структуры данных "один ко многим

*Example of a **read-only** nested serializer. Nothing complex to worry about here.*

*Пример вложенного сериализатора **только для чтения**. Здесь нет ничего сложного.*

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

Некоторые примеры вывода нашего сериализатора.

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

Давайте рассмотрим обновление нашей вложенной структуры данных "один ко многим".

### Validation errors

### Ошибки валидации

### Adding and removing items

### Добавление и удаление элементов

### Making PATCH requests

### Выполнение PATCH-запросов