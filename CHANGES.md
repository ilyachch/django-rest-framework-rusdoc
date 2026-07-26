Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)
 - `.reference/api-guide/filtering.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> afc9184e5033e0c80f6349dac85c1133c512f24c
@@ -237,6 +237,18 @@ For example:
 
 By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting in the `REST_FRAMEWORK` configuration.
 
+#### Accent-insensitive search
+
+The `UnaccentedSearchFilter` subclass performs accent-insensitive matching, so that a search for `Jeremy` also matches `Jérémy`. It behaves like `SearchFilter`, except the lookups are wrapped with the `unaccent` transform: the default lookup becomes `unaccent__icontains`, `^` becomes `unaccent__istartswith`, `=` becomes `unaccent__iexact`, and `$` becomes `unaccent__iregex`. The `@` (full-text search) prefix is left unchanged, as the `unaccent` transform cannot be combined with a full-text search lookup.
+
+    from rest_framework import filters
+
+    class MyView(generics.ListAPIView):
+        filter_backends = [filters.UnaccentedSearchFilter]
+        search_fields = ['name']
+
+This is currently only supported on Django's [PostgreSQL backend][postgres-lookups], and requires the `unaccent` extension to be installed and `django.contrib.postgres` to be present in `INSTALLED_APPS`.
+
 To dynamically change search fields based on request content, it's possible to subclass the `SearchFilter` and override the `get_search_fields()` function. For example, the following subclass will only search on `title` if the query parameter `title_only` is in the request:
 
     from rest_framework import filters
@@ -370,3 +382,4 @@ The [djangorestframework-word-filter][django-rest-framework-word-search-filter]
 [HStoreField]: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/fields/#hstorefield
 [JSONField]: https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.JSONField
 [postgres-search]: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/
+[postgres-lookups]: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/lookups/#unaccent
```


 - `.reference/api-guide/serializers.md`
```
dff3c8d622096d6f193b382452e056896d4ff885 -> 68859ac5eed8010ee7d8a3c47fd766f74ebbda6f
@@ -214,6 +214,26 @@ To do any other validation that requires access to multiple fields, add a method
                 raise serializers.ValidationError("finish must occur after start")
             return data
 
+!!! note
+    **Object-Level Validation and Partial Updates**
+
+    When performing a **partial update** (`PATCH`), the `data` dictionary passed to the `validate()` method will **only contain the fields** provided in the request. If your validation logic depends on multiple fields, you must account for cases where some fields are missing from `data`.
+
+    To access fields not included in the partial update, you should retrieve them from the existing object instance using `self.instance`:
+
+    ```python
+    def validate(self, data):
+        # Check if "status" is being updated, or use the existing value
+        status = data.get("status", self.instance.status)
+
+        # Check if "price" is being updated, or use the existing value
+        price = data.get("price", self.instance.price)
+
+        if status == "active" and price <= 0:
+            raise serializers.ValidationError("Active products must have a price.")
+        return data
+    ```
+
 #### Validators
 
 Individual fields on a serializer can include validators, by declaring them on the field instance, for example:
```


 - `.reference/api-guide/fields.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> 977d764dcfb29179d8153a9c49f372097c892400
@@ -330,7 +330,7 @@ Corresponds to `django.db.models.fields.DateTimeField`.
 
 * `format` - A string representing the output format. If not specified, this defaults to the same value as the `DATETIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `datetime` objects should be returned by `to_representation`. In this case the datetime encoding will be determined by the renderer.
 * `input_formats` - A list of strings representing the input formats which may be used to parse the date.  If not specified, the `DATETIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.
-* `default_timezone` - A `tzinfo` subclass (`zoneinfo` or `pytz`) representing the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone][django-current-timezone]. If `USE_TZ` is disabled, then datetime objects will be naive.
+* `default_timezone` - A `tzinfo` subclass (`zoneinfo`) representing the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone][django-current-timezone]. If `USE_TZ` is disabled, then datetime objects will be naive.
 
 #### `DateTimeField` format strings.
```


 - `.reference/README.md`
```
021ab5664b085594876032cf062c1220bc1ca03c -> 65066b326dc358aba87d7fba1101a94fc2dbf004
@@ -65,7 +65,7 @@ Some reasons you might want to use REST framework:
 
 REST framework requires the following:
 
-* Django (4.2, 5.0, 5.1, 5.2, 6.0)
+* Django (5.2, 6.0, 6.1)
 * Python (3.10, 3.11, 3.12, 3.13, 3.14)
 
 We **highly recommend** and only officially support the latest patch release of
```


