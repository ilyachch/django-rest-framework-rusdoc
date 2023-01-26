<!-- TRANSLATED by md-translate -->
# Legacy CoreAPI Schemas Docs

# Наследие CoreAPI Schemas Docs

Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10.

Использование схем на базе CoreAPI было отменено с введением генерации схем на базе OpenAPI, начиная с Django REST Framework v3.10.

See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

Более подробную информацию см. в [Version 3.10 Release Announcement](../community/3.10-announcement.md).

---

You can continue to use CoreAPI schemas by setting the appropriate default schema class:

Вы можете продолжать использовать схемы CoreAPI, установив соответствующий класс схемы по умолчанию:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```

Under-the-hood, any subclass of `coreapi.AutoSchema` here will trigger use of the old CoreAPI schemas. **Otherwise** you will automatically be opted-in to the new OpenAPI schemas.

Под капотом, любой подкласс `coreapi.AutoSchema` здесь будет запускать использование старых схем CoreAPI. **В противном случае** вы автоматически перейдете на новые схемы OpenAPI.

All CoreAPI related code will be removed in Django REST Framework v3.12. Switch to OpenAPI schemas by then.

Весь код, связанный с CoreAPI, будет удален в Django REST Framework v3.12. К тому времени перейдите на схемы OpenAPI.

---

For reference this folder contains the old CoreAPI related documentation:

Для справки эта папка содержит старую документацию, связанную с CoreAPI:

* [Tutorial 7: Schemas & client libraries](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//7-schemas-and-client-libraries.md).
* [Excerpts from *Documenting your API* topic page](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//from-documenting-your-api.md).
* [`rest_framework.schemas` API Reference](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//schemas.md).

* [Учебник 7: Схемы и клиентские библиотеки](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//7-schemas-and-client-libraries.md).
* [Выдержки из *Documenting your API* topic page](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//from-documenting-your-api.md).
* [Справочник по API `rest_framework.schemas`](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//schemas.md).