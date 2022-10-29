# Legacy CoreAPI Schemas Docs

# Regacy coreapi схемы документов

Use of CoreAPI-based schemas were deprecated with the introduction of native OpenAPI-based schema generation as of Django REST Framework v3.10.

Использование схем на основе Coreapi установилось с внедрением нативного генерации схем на основе OpenAPI по состоянию на Django Rest Framework v3.10.

See the [Version 3.10 Release Announcement](../community/3.10-announcement.md) for more details.

См. Объявление [версия 3.10 выпуска] (../ Community/3.10-Annoument.md) для получения более подробной информации.

---

You can continue to use CoreAPI schemas by setting the appropriate default schema class:

Вы можете продолжать использовать схемы Coreapi, установив соответствующий класс схемы по умолчанию:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```


Under-the-hood, any subclass of `coreapi.AutoSchema` here will trigger use of the old CoreAPI schemas.
**Otherwise** you will automatically be opted-in to the new OpenAPI schemas.

Любой подкласс `coreapi.autoschema` здесь вызовет использование старых схем Coreapi.
** В противном случае ** вы будете автоматически выбраны в новые схемы OpenAPI.

All CoreAPI related code will be removed in Django REST Framework v3.12. Switch to OpenAPI schemas by then.

Весь код, связанный с Coreapi, будет удален в Django Rest Framework v3.12.
Переключитесь на схемы OpenAPI к тому времени.

---

For reference this folder contains the old CoreAPI related documentation:

Для справки, эта папка содержит старую документацию, связанную с Coreapi:

* [Tutorial 7: Schemas & client libraries](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//7-schemas-and-client-libraries.md).
* [Excerpts from *Documenting your API* topic page](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//from-documenting-your-api.md).
* [`rest_framework.schemas` API Reference](https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//schemas.md).

* [Учебное пособие 7: схемы и клиентские библиотеки] (https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//7-schemas-and-client-libraries.md).
* [Выдержки из * документирования вашей страницы API * темы] (https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//from-documenting-your-api.md).
* [`REST_FRAMEWORD.SCHEMAS` Ссылка API] (https://github.com/encode/django-rest-framework/blob/master/docs/coreapi//schemas.md).