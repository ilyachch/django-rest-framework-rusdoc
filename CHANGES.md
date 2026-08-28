Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)
 - `.reference/api-guide/pagination.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> f0d95c2df066e163553f7d19b33d724e988744cc
@@ -62,6 +62,83 @@ Or apply the style globally, using the `DEFAULT_PAGINATION_CLASS` settings key.
         'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
     }
 
+## Details and limitations
+
+Proper use of pagination requires a little attention to detail. You'll need to think about what ordering you want the scheme to be applied against.
+
+You can modify the ordering in multiple ways:
+
+* Using the `OrderingFilter` filter class together with the pagination class in the view definition. 
+* Setting the `ordering` attribute on the `Meta` class of the model whose records are being paginated.
+* Explicitly calling `order_by` on the view's `queryset`.
+* If using the [`CursorPagination`](#cursorpagination) class, overriding the `ordering` attribute 
+
+When using `OrderingFilter`, you should strongly consider restricting the fields that the user may order by.
+
+For `CursorPagination`, the default is to order by `"-created"`. This assumes that **there must be a 'created' timestamp field** on the model instances, and will present a "timeline" style paginated view, with the most recently added items first.
+
+Proper usage of pagination should have an ordering field that satisfies the following:
+
+* Should be an unchanging value, such as a timestamp, slug, or other field that is only set once, on creation.
+* Should be unique, or nearly unique if using `CursorPagination`. The `CursorPagination` implementation uses a smart "position plus offset" style that allows it to properly support not-strictly-unique values as the ordering. Millisecond precision timestamps are a good example.
+* Should be a non-nullable value that can be coerced to a string.
+* Should not be a float. Precision errors easily lead to incorrect results. Hint: use decimals instead. (If you already have a float field and must paginate on that, an [example `CursorPagination` subclass that uses decimals to limit precision is available here][float_cursor_pagination_example].)
+* The field should have a database index.
+
+Using an ordering field that does not satisfy these constraints will generally still work, but the results might be suboptimal or outright inconsistent depending on the chosen scheme. These inconsistencies might manifest as either missing records or duplicate records:
+     
+    class Product(models.Model):
+        name = models.CharField(max_length=100)
+        category = models.CharField(max_length=100)
+        # No unique/indexed field used for ordering
+    
+    class ProductSerializer(serializers.ModelSerializer):
+        class Meta:
+            model = Product
+            fields = '__all__'
+    
+    # 1. Inconsistent LimitOffsetPagination
+    class UnreliableProductViewSet(viewsets.ModelViewSet):
+        # Many duplicates, inconsistent pages
+        queryset = Product.objects.all().order_by('category')
+        serializer_class = ProductSerializer
+        pagination_class = pagination.LimitOffsetPagination
+    
+    # 2. Inconsistent CursorPagination (Will fail or be buggy)
+    class RiskyCursorPagination(pagination.CursorPagination):
+        page_size = 10
+        # Problematic: 'name' is not unique and can change
+        ordering = 'name'
+
+By ensuring the final ordering field is unique and indexed (like id or a created timestamp), we guarantee that the cursor position remains stable:
+ 
+    class SecureProduct(models.Model):
+        name = models.CharField(max_length=100)
+        created_at = models.DateTimeField(auto_now_add=True, db_index=True)
+    
+    class SecureProductSerializer(serializers.ModelSerializer):
+        class Meta:
+            model = SecureProduct
+            fields = '__all__'
+    
+    # 1. Consistent PageNumberPagination with Multiple Ordering
+    class ReliableProductViewSet(viewsets.ModelViewSet):
+        # Combining a non-unique field with a unique ID ensures consistency
+        queryset = SecureProduct.objects.all().order_by('name', 'id')
+        serializer_class = SecureProductSerializer
+        pagination_class = pagination.PageNumberPagination
+    
+    # 2. Recommended CursorPagination Usage
+    class StandardCursorPagination(pagination.CursorPagination):
+        page_size = 10
+         # Unique-ish, indexed, and unchanging
+        ordering = '-created_at'
+    
+    class AccurateProductViewSet(viewsets.ModelViewSet):
+        queryset = SecureProduct.objects.all()
+        serializer_class = SecureProductSerializer
+        pagination_class = StandardCursorPagination
+
 ---
 
 ## API Reference
@@ -183,25 +260,6 @@ Cursor based pagination is more complex than other schemes. It also requires tha
 * Provides a consistent pagination view. When used properly `CursorPagination` ensures that the client will never see the same item twice when paging through records, even when new items are being inserted by other clients during the pagination process.
 * Supports usage with very large datasets. With extremely large datasets pagination using offset-based pagination styles may become inefficient or unusable. Cursor based pagination schemes instead have fixed-time properties, and do not slow down as the dataset size increases.
 
-#### Details and limitations
-
-Proper use of cursor based pagination requires a little attention to detail. You'll need to think about what ordering you want the scheme to be applied against. The default is to order by `"-created"`. This assumes that **there must be a 'created' timestamp field** on the model instances, and will present a "timeline" style paginated view, with the most recently added items first.
-
-You can modify the ordering by overriding the `'ordering'` attribute on the pagination class, or by using the `OrderingFilter` filter class together with `CursorPagination`. When used with `OrderingFilter` you should strongly consider restricting the fields that the user may order by.
-
-Proper usage of cursor pagination should have an ordering field that satisfies the following:
-
-* Should be an unchanging value, such as a timestamp, slug, or other field that is only set once, on creation.
-* Should be unique, or nearly unique. Millisecond precision timestamps are a good example. This implementation of cursor pagination uses a smart "position plus offset" style that allows it to properly support not-strictly-unique values as the ordering.
-* Should be a non-nullable value that can be coerced to a string.
-* Should not be a float. Precision errors easily lead to incorrect results.
-  Hint: use decimals instead.
-  (If you already have a float field and must paginate on that, an
-  [example `CursorPagination` subclass that uses decimals to limit precision is available here][float_cursor_pagination_example].)
-* The field should have a database index.
-
-Using an ordering field that does not satisfy these constraints will generally still work, but you'll be losing some of the benefits of cursor pagination.
-
 For more technical details on the implementation we use for cursor pagination, the ["Building cursors for the Disqus API"][disqus-cursor-api] blog post gives a good overview of the basic approach.
 
 #### Setup
```


 - `.reference/api-guide/renderers.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> d346a8c3c92a36fdb462c992331e238d0a737305
@@ -171,6 +171,8 @@ Renders data into HTML for the Browsable API:
 
 This renderer will determine which other renderer would have been given highest priority, and use that to display an API style response within the HTML page.
 
+It also renders an HTML form for each method the view allows, which involves calling back into the view with the request method overridden.  See [form rendering][browsable-api-form-rendering] for the implications of this.
+
 **.media_type**: `text/html`
 
 **.format**: `'api'`
@@ -513,6 +515,7 @@ Comma-separated values are a plain-text tabular data format, that can be easily
 
 
 [cite]: https://docs.djangoproject.com/en/stable/ref/template-response/#the-rendering-process
+[browsable-api-form-rendering]: ../topics/browsable-api.md#form-rendering
 [conneg]: content-negotiation.md
 [html-and-forms]: ../topics/html-and-forms.md
 [browser-accept-headers]: http://www.gethifi.com/blog/browser-rest-http-accept-headers
```


 - `.reference/api-guide/fields.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> aa1876b8b6009a618e6241f91e2c2d6dfbacb5d9
@@ -84,6 +84,22 @@ When serializing fields with dotted notation, it may be necessary to provide a `
 
 This case would require user object to be fetched from database when it is not prefetched. If that is not wanted, be sure to be using `prefetch_related` and `select_related` methods appropriately. For more information about the methods refer to [django documentation][django-docs-select-related].
 
+Also note that when dotted notation is used, after serializer validation the `.validated_data` attribute will _not_ include a flat `"<fieldname>": <value>` item. Instead, it will include a nested dictionary derived by expanding the dotted path value of the `source` argument. So, for the previous serializer example, `.validated_data` would be:
+
+    {
+        "user": {
+            "email": ...
+        }
+    }
+
+instead of:
+
+    {
+        "email": ...
+    }
+
+This works this way because, in DRF's philosophy, the `.data` attribute represents the external API representation (where key names equal field names), while the `.validated_data` attribute represents the internal object structure (where the nesting and key names follow the `source` path).
+
 The value `source='*'` has a special meaning, and is used to indicate that the entire object should be passed through to the field.  This can be useful for creating nested representations, or for fields which require access to the complete object in order to determine the output representation.
 
 Defaults to the name of the field.
@@ -330,7 +346,7 @@ Corresponds to `django.db.models.fields.DateTimeField`.
 
 * `format` - A string representing the output format. If not specified, this defaults to the same value as the `DATETIME_FORMAT` settings key, which will be `'iso-8601'` unless set. Setting to a format string indicates that `to_representation` return values should be coerced to string output. Format strings are described below. Setting this value to `None` indicates that Python `datetime` objects should be returned by `to_representation`. In this case the datetime encoding will be determined by the renderer.
 * `input_formats` - A list of strings representing the input formats which may be used to parse the date.  If not specified, the `DATETIME_INPUT_FORMATS` setting will be used, which defaults to `['iso-8601']`.
-* `default_timezone` - A `tzinfo` subclass (`zoneinfo` or `pytz`) representing the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone][django-current-timezone]. If `USE_TZ` is disabled, then datetime objects will be naive.
+* `default_timezone` - A `tzinfo` subclass (`zoneinfo`) representing the timezone. If not specified and the `USE_TZ` setting is enabled, this defaults to the [current timezone][django-current-timezone]. If `USE_TZ` is disabled, then datetime objects will be naive.
 
 #### `DateTimeField` format strings.
```


 - `.reference/api-guide/generic-views.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> d346a8c3c92a36fdb462c992331e238d0a737305
@@ -184,6 +184,9 @@ For example:
             return FullAccountSerializer
         return BasicAccountSerializer
 
+!!! note
+    If your implementation branches on `self.request.method`, note that the browsable API calls this method with the request method overridden while [rendering its forms][browsable-api-form-rendering].
+
 **Save and deletion hooks**:
 
 The following methods are provided by the mixin classes, and provide easy overriding of the object save or deletion behavior.
@@ -416,6 +419,7 @@ The following third party packages provide additional generic view implementatio
 
 
 [cite]: https://docs.djangoproject.com/en/stable/ref/class-based-views/#base-vs-generic-views
+[browsable-api-form-rendering]: ../topics/browsable-api.md#form-rendering
 [GenericAPIView]: #genericapiview
 [ListModelMixin]: #listmodelmixin
 [CreateModelMixin]: #createmodelmixin
```


 - `.reference/api-guide/filtering.md`
```
f56ec9546c846acddde7013cfc3aae9ddc40c6f0 -> 751a19fe1b237beca9af7d587fce55d3e09d3741
@@ -227,7 +227,7 @@ The search behavior may be specified by prefixing field names in `search_fields`
 | ------ | --------------| ------------------ |
 | `^`    | `istartswith` | Starts-with search.|
 | `=`    | `iexact`      | Exact matches.     |
-| `$`    | `iregex`      | Regex search.      |
+| `$`    | `iregex`      | Regex search (see warning below).      |
 | `@`    | `search`      | Full-text search (Currently only supported Django's [PostgreSQL backend][postgres-search]). |
 | None   | `icontains`   | Contains search (Default).  |
 
@@ -237,6 +237,21 @@ For example:
 
 By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting in the `REST_FRAMEWORK` configuration.
 
+!!! warning
+    When passing a regex to the filter via the `$` prefix or performing a `iregex` lookup, beware of maliciously crafted regular expressions that may lead to excessive CPU consumption and denial of service (DoS). Consider avoiding regex search for untrusted clients, and familiarize yourself with risky patterns (e.g., catastrophic backtracking).
+
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
@@ -370,3 +385,4 @@ The [djangorestframework-word-filter][django-rest-framework-word-search-filter]
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


 - `.reference/api-guide/views.md`
```
7f8ad25e15f911ef2afd54d91dcffb29ca1022f9 -> e3a3bc6c9ba941fa195c5608468ad537466019c6
@@ -219,12 +219,26 @@ You may pass `None` in order to exclude the view from schema generation.
     def view(request):
         return Response({"message": "Will not appear in schema!"})
 
+### Throttle scope decorator
+
+To set the throttle scope of function based views you may use the `@throttle_scope` decorator:
+
+    from rest_framework.decorators import api_view, throttle_scope
+
+    @api_view(['GET'])
+    @throttle_scope("hello")
+    def view(request):
+        return Response({"message": "Hello for today! See you tomorrow!"})
+
+See [ScopedRateThrottle documentation][scoped-rate-throttle] for more details.
+
 
 [cite]: https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-usage.html
 [cite2]: http://www.boredomandlaziness.org/2012/05/djangos-cbvs-are-not-mistake-but.html
 [settings]: settings.md
 [throttling]: throttling.md
 [schemas]: schemas.md
+[scoped-rate-throttle]: throttling.md#scopedratethrottle
 [classy-drf]: http://www.cdrf.co
 [api-policy-attributes]: views.md#api-policy-attributes
```


 - `.reference/topics/browsable-api.md`
```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> d346a8c3c92a36fdb462c992331e238d0a737305
@@ -29,6 +29,12 @@ urlpatterns = [
 ```
 
 
+## Form rendering
+
+In order to render the HTML forms, the browsable API needs to know which fields each form should contain, so it asks the view for a serializer once per form.  Each of those calls is made with the request method overridden to match the form being rendered, rather than the method that was actually used for the request.
+
+This means that during a `GET` request the view may be called again with `self.request.method` set to `POST`, `PUT`, `PATCH`, `DELETE` or `OPTIONS`.  Any code that branches on the request method will observe the overridden value.  Two common cases are a `get_serializer_class()` implementation that returns a different serializer for read and write operations, and permission classes, which are checked for each method before its form is rendered.  This is expected behavior, and only affects rendering of the browsable API.
+
 ## Customizing
 
 The browsable API is built with [Twitter's Bootstrap][bootstrap] (v 3.4.1), making it easy to customize the look-and-feel.
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


