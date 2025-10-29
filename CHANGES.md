Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)

 - `.reference/api-guide/testing.md`

```
089f6a697445af20f52832db99f2ab94baea4ece -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -92,7 +92,7 @@ For example, when forcibly authenticating using a token, you might do something
 
 ---
 
-**Note**: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are re-using the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`][refresh_from_db_docs] between tests.
+**Note**: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are reusing the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`][refresh_from_db_docs] between tests.
 
 ---
 
@@ -105,6 +105,20 @@ This means that setting attributes directly on the request object may not always
     request.user = user
     response = view(request)
 
+If you want to test a request involving the REST framework’s 'Request' object, you’ll need to manually transform it first:
+
+    class DummyView(APIView):
+        ...
+
+    factory = APIRequestFactory()
+    request = factory.get('/', {'demo': 'test'})
+    drf_request = DummyView().initialize_request(request)
+    assert drf_request.query_params == {'demo': ['test']}
+
+    request = factory.post('/', {'example': 'test'})
+    drf_request = DummyView().initialize_request(request)
+    assert drf_request.data.get('example') == 'test'
+
 ---
 
 ## Forcing CSRF validation
@@ -250,7 +264,7 @@ For example...
     csrftoken = response.cookies['csrftoken']
 
     # Interact with the API.
-    response = client.post('http://testserver/organisations/', json={
+    response = client.post('http://testserver/organizations/', json={
         'name': 'MegaCorp',
         'status': 'active'
     }, headers={'X-CSRFToken': csrftoken})
@@ -278,12 +292,12 @@ The CoreAPIClient allows you to interact with your API using the Python
     client = CoreAPIClient()
     schema = client.get('http://testserver/schema/')
 
-    # Create a new organisation
+    # Create a new organization
     params = {'name': 'MegaCorp', 'status': 'active'}
-    client.action(schema, ['organisations', 'create'], params)
+    client.action(schema, ['organizations', 'create'], params)
 
-    # Ensure that the organisation exists in the listing
-    data = client.action(schema, ['organisations', 'list'])
+    # Ensure that the organization exists in the listing
+    data = client.action(schema, ['organizations', 'list'])
     assert(len(data) == 1)
     assert(data == [{'name': 'MegaCorp', 'status': 'active'}])
 
@@ -417,5 +431,5 @@ For example, to add support for using `format='html'` in test requests, you migh
 [requestfactory]: https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.client.RequestFactory
 [configuration]: #configuration
 [refresh_from_db_docs]: https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.refresh_from_db
-[session_objects]: https://requests.readthedocs.io/en/master/user/advanced/#session-objects
+[session_objects]: https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
 [provided_test_case_classes]: https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes
```



 - `.reference/api-guide/responses.md`

```
5e8fe6edf0b25506c5bc3ce749c5b9d5cb9e7e7e -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -11,7 +11,7 @@ source:
 
 REST framework supports HTTP content negotiation by providing a `Response` class which allows you to return content that can be rendered into multiple content types, depending on the client request.
 
-The `Response` class subclasses Django's `SimpleTemplateResponse`.  `Response` objects are initialised with data, which should consist of native Python primitives.  REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.
+The `Response` class subclasses Django's `SimpleTemplateResponse`.  `Response` objects are initialized with data, which should consist of native Python primitives.  REST framework then uses standard HTTP content negotiation to determine how it should render the final response content.
 
 There's no requirement for you to use the `Response` class, you can also return regular `HttpResponse` or `StreamingHttpResponse` objects from your views if required.  Using the `Response` class simply provides a nicer interface for returning content-negotiated Web API responses, that can be rendered to multiple formats.
```



 - `.reference/api-guide/generic-views.md`

```
c0202a0aa5cbaf8573458b932878dfd5044c93ab -> 653343cf32334a3d6e92872c0a7decdc7d8e9085
@@ -102,6 +102,39 @@ For example:
 
 ---
 
+### Avoiding N+1 Queries
+
+When listing objects (e.g. using `ListAPIView` or `ModelViewSet`), serializers may trigger an N+1 query pattern if related objects are accessed individually for each item.
+
+To prevent this, optimize the queryset in `get_queryset()` or by setting the `queryset` class attribute using [`select_related()`](https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related) and [`prefetch_related()`](https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related), depending on the type of relationship.
+
+**For ForeignKey and OneToOneField**:
+
+Use `select_related()` to fetch related objects in the same query:
+
+    def get_queryset(self):
+        return Order.objects.select_related("customer", "billing_address")
+
+**For reverse and many-to-many relationships**:
+
+Use `prefetch_related()` to efficiently load collections of related objects:
+
+    def get_queryset(self):
+        return Book.objects.prefetch_related("categories", "reviews__user")
+
+**Combining both**:
+
+    def get_queryset(self):
+        return (
+            Order.objects
+            .select_related("customer")
+            .prefetch_related("items__product")
+        )
+
+These optimizations reduce repeated database access and improve list view performance.
+
+---
+
 #### `get_object(self)`
 
 Returns an object instance that should be used for detail views.  Defaults to using the `lookup_field` parameter to filter the base queryset.
@@ -374,8 +407,6 @@ Allowing `PUT` as create operations is problematic, as it necessarily exposes in
 
 Both styles "`PUT` as 404" and "`PUT` as create" can be valid in different circumstances, but from version 3.0 onwards we now use 404 behavior as the default, due to it being simpler and more obvious.
 
-If you need to generic PUT-as-create behavior you may want to include something like [this `AllowPUTAsCreateMixin` class](https://gist.github.com/tomchristie/a2ace4577eff2c603b1b) as a mixin to your views.
-
 ---
 
 # Third party packages
```



 - `.reference/api-guide/serializers.md`

```
9016efe3fc412488df92912c619f8f24fed2937c -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -48,7 +48,7 @@ We can now use `CommentSerializer` to serialize a comment, or list of comments.
     serializer.data
     # {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
 
-At this point we've translated the model instance into Python native datatypes.  To finalise the serialization process we render the data into `json`.
+At this point we've translated the model instance into Python native datatypes.  To finalize the serialization process we render the data into `json`.
 
     from rest_framework.renderers import JSONRenderer
 
@@ -155,7 +155,7 @@ When deserializing data, you always need to call `is_valid()` before attempting
     serializer.is_valid()
     # False
     serializer.errors
-    # {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
+    # {'email': ['Enter a valid email address.'], 'created': ['This field is required.']}
 
 Each key in the dictionary will be the field name, and the values will be lists of strings of any error messages corresponding to that field.  The `non_field_errors` key may also be present, and will list any general validation errors. The name of the `non_field_errors` key may be customized using the `NON_FIELD_ERRORS_KEY` REST framework setting.
 
@@ -298,7 +298,7 @@ When dealing with nested representations that support deserializing the data, an
     serializer.is_valid()
     # False
     serializer.errors
-    # {'user': {'email': ['Enter a valid e-mail address.']}, 'created': ['This field is required.']}
+    # {'user': {'email': ['Enter a valid email address.']}, 'created': ['This field is required.']}
 
 Similarly, the `.validated_data` property will include nested data structures.
 
@@ -430,7 +430,7 @@ The context dictionary can be used within any serializer field logic, such as a
 
 Often you'll want serializer classes that map closely to Django model definitions.
 
-The `ModelSerializer` class provides a shortcut that lets you automatically create a `Serializer` class with fields that correspond to the Model fields.
+The `ModelSerializer` class provides a shortcut that let's you automatically create a `Serializer` class with fields that correspond to the Model fields.
 
 **The `ModelSerializer` class is the same as a regular `Serializer` class, except that**:
 
@@ -1189,6 +1189,10 @@ The [drf-writable-nested][drf-writable-nested] package provides writable nested
 
 The [drf-encrypt-content][drf-encrypt-content] package helps you encrypt your data, serialized through ModelSerializer. It also contains some helper functions. Which helps you to encrypt your data.
 
+## Shapeless Serializers
+
+The [drf-shapeless-serializers][drf-shapeless-serializers] package provides dynamic serializer configuration capabilities, allowing runtime field selection, renaming, attribute modification, and nested relationship configuration without creating multiple serializer classes. It helps eliminate serializer boilerplate while providing flexible API responses.
+
 
 [cite]: https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion
 [relations]: relations.md
@@ -1212,3 +1216,4 @@ The [drf-encrypt-content][drf-encrypt-content] package helps you encrypt your da
 [djangorestframework-queryfields]: https://djangorestframework-queryfields.readthedocs.io/
 [drf-writable-nested]: https://github.com/beda-software/drf-writable-nested
 [drf-encrypt-content]: https://github.com/oguzhancelikarslan/drf-encrypt-content
+[drf-shapeless-serializers]: https://github.com/khaledsukkar2/drf-shapeless-serializers
```



 - `.reference/api-guide/pagination.md`

```
c9e7b68a4c1db1ac60e962053380acda549609f3 -> f74a44e850a685ac73c819ae7b96b0d68a8f734f
@@ -108,7 +108,7 @@ To set these attributes you should override the `PageNumberPagination` class, an
 * `page_query_param` - A string value indicating the name of the query parameter to use for the pagination control.
 * `page_size_query_param` - If set, this is a string value indicating the name of a query parameter that allows the client to set the page size on a per-request basis. Defaults to `None`, indicating that the client may not control the requested page size.
 * `max_page_size` - If set, this is a numeric value indicating the maximum allowable requested page size. This attribute is only valid if `page_size_query_param` is also set.
-* `last_page_strings` - A list or tuple of string values indicating values that may be used with the `page_query_param` to request the final page in the set. Defaults to `('last',)`
+* `last_page_strings` - A list or tuple of string values indicating values that may be used with the `page_query_param` to request the final page in the set. Defaults to `('last',)`. For example, use `?page=last` to go directly to the last page.
 * `template` - The name of a template to use when rendering pagination controls in the browsable API. May be overridden to modify the rendering style, or set to `None` to disable HTML pagination controls completely. Defaults to `"rest_framework/pagination/numbers.html"`.
 
 ---
```



 - `.reference/api-guide/relations.md`

```
fc98d3598d9c0762e0cb999992e954643e6dc091 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -300,7 +300,7 @@ For example, the following serializer:
 
 Would serialize to a nested representation like this:
 
-    >>> album = Album.objects.create(album_name="The Grey Album", artist='Danger Mouse')
+    >>> album = Album.objects.create(album_name="The Gray Album", artist='Danger Mouse')
     >>> Track.objects.create(album=album, order=1, title='Public Service Announcement', duration=245)
     <Track: Track object>
     >>> Track.objects.create(album=album, order=2, title='What More Can I Say', duration=264)
@@ -310,7 +310,7 @@ Would serialize to a nested representation like this:
     >>> serializer = AlbumSerializer(instance=album)
     >>> serializer.data
     {
-        'album_name': 'The Grey Album',
+        'album_name': 'The Gray Album',
         'artist': 'Danger Mouse',
         'tracks': [
             {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
@@ -344,7 +344,7 @@ By default nested serializers are read-only. If you want to support write-operat
             return album
 
     >>> data = {
-        'album_name': 'The Grey Album',
+        'album_name': 'The Gray Album',
         'artist': 'Danger Mouse',
         'tracks': [
             {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
```



 - `.reference/api-guide/metadata.md`

```
46be2ffd34e2118e905fa3f0cbcab918d482134f -> e045dc465270c18689dba4a970378cd9744e57b6
@@ -66,7 +66,7 @@ The REST framework package only includes a single metadata class implementation,
 
 ## Creating schema endpoints
 
-If you have specific requirements for creating schema endpoints that are accessed with regular `GET` requests, you might consider re-using the metadata API for doing so.
+If you have specific requirements for creating schema endpoints that are accessed with regular `GET` requests, you might consider reusing the metadata API for doing so.
 
 For example, the following additional route could be used on a viewset to provide a linkable schema endpoint.
```



 - `.reference/api-guide/filtering.md`

```
c0202a0aa5cbaf8573458b932878dfd5044c93ab -> a323cf7c0a33d7ffd395a6805019f613fb79f985
@@ -235,7 +235,7 @@ For example:
 
     search_fields = ['=username', '=email']
 
-By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting.
+By default, the search parameter is named `'search'`, but this may be overridden with the `SEARCH_PARAM` setting in the `REST_FRAMEWORK` configuration.
 
 To dynamically change search fields based on request content, it's possible to subclass the `SearchFilter` and override the `get_search_fields()` function. For example, the following subclass will only search on `title` if the query parameter `title_only` is in the request:
 
@@ -257,7 +257,7 @@ The `OrderingFilter` class supports simple query parameter controlled ordering o
 
 ![Ordering Filter](../img/ordering-filter.png)
 
-By default, the query parameter is named `'ordering'`, but this may be overridden with the `ORDERING_PARAM` setting.
+By default, the query parameter is named `'ordering'`, but this may be overridden with the `ORDERING_PARAM` setting in the `REST_FRAMEWORK` configuration.
 
 For example, to order users by username:
```



 - `.reference/api-guide/renderers.md`

```
a4f6059d500efbe25e889862d12f5f7a87cba8fe -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -134,7 +134,7 @@ An example of a view that uses `TemplateHTMLRenderer`:
 
 You can use `TemplateHTMLRenderer` either to return regular HTML pages using REST framework, or to return both HTML and API responses from a single endpoint.
 
-If you're building websites that use `TemplateHTMLRenderer` along with other renderer classes, you should consider listing `TemplateHTMLRenderer` as the first class in the `renderer_classes` list, so that it will be prioritised first even for browsers that send poorly formed `ACCEPT:` headers.
+If you're building websites that use `TemplateHTMLRenderer` along with other renderer classes, you should consider listing `TemplateHTMLRenderer` as the first class in the `renderer_classes` list, so that it will be prioritized first even for browsers that send poorly formed `ACCEPT:` headers.
 
 See the [_HTML & Forms_ Topic Page][html-and-forms] for further examples of `TemplateHTMLRenderer` usage.
```



 - `.reference/api-guide/validators.md`

```
ffadde930ef23983f123477964d201c278f107e9 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -5,7 +5,7 @@ source:
 
 # Validators
 
-> Validators can be useful for re-using validation logic between different types of fields.
+> Validators can be useful for reusing validation logic between different types of fields.
 >
 > &mdash; [Django documentation][cite]
 
@@ -13,7 +13,7 @@ Most of the time you're dealing with validation in REST framework you'll simply
 
 However, sometimes you'll want to place your validation logic into reusable components, so that it can easily be reused throughout your codebase. This can be achieved by using validator functions and validator classes.
 
-## Validation in REST framework
+## Validation in REST framework
 
 Validation in Django REST framework serializers is handled a little differently to how validation works in Django's `ModelForm` class.
 
@@ -75,7 +75,7 @@ This validator should be applied to *serializer fields*, like so:
         validators=[UniqueValidator(queryset=BlogPost.objects.all())]
     )
 
-## UniqueTogetherValidator
+## UniqueTogetherValidator
 
 This validator can be used to enforce `unique_together` constraints on model instances.
 It has two required arguments, and a single optional `messages` argument:
@@ -92,7 +92,7 @@ The validator should be applied to *serializer classes*, like so:
         # ...
         class Meta:
             # ToDo items belong to a parent list, and have an ordering defined
-            # by the 'position' field. No two items in a given list may share
+            # by the 'position' field. No two items in a given list may share
             # the same position.
             validators = [
                 UniqueTogetherValidator(
@@ -166,7 +166,7 @@ If you want the date field to be entirely hidden from the user, then use `Hidden
 
 ---
 
-**Note:** `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request).
+**Note:** `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request). 
 
 ---
 
@@ -175,7 +175,7 @@ If you want the date field to be entirely hidden from the user, then use `Hidden
 Validators that are applied across multiple fields in the serializer can sometimes require a field input that should not be provided by the API client, but that *is* available as input to the validator.
 For this purposes use `HiddenField`. This field will be present in `validated_data` but *will not* be used in the serializer output representation.
 
-**Note:** Using a `read_only=True` field is excluded from writable fields so it won't use a `default=…` argument. Look [3.8 announcement](https://www.django-rest-framework.org/community/3.8-announcement/#altered-the-behaviour-of-read_only-plus-default-on-field).
+**Note:** Using a `read_only=True` field is excluded from writable fields so it won't use a `default=…` argument. Look [3.8 announcement](https://www.django-rest-framework.org/community/3.8-announcement/#altered-the-behavior-of-read_only-plus-default-on-field).
 
 REST framework includes a couple of defaults that may be useful in this context.
```



 - `.reference/api-guide/authentication.md`

```
32dbd3525dc16bf51883be23f5fba129acdcf1c1 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -416,7 +416,7 @@ JSON Web Token is a fairly new standard which can be used for token-based authen
 
 ## Hawk HTTP Authentication
 
-The [HawkREST][hawkrest] library builds on the [Mohawk][mohawk] library to let you work with [Hawk][hawk] signed requests and responses in your API. [Hawk][hawk] lets two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication][mac] (which was based on parts of [OAuth 1.0][oauth-1.0a]).
+The [HawkREST][hawkrest] library builds on the [Mohawk][mohawk] library to let you work with [Hawk][hawk] signed requests and responses in your API. [Hawk][hawk] let's two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication][mac] (which was based on parts of [OAuth 1.0][oauth-1.0a]).
 
 ## HTTP Signature Authentication
 
@@ -426,6 +426,11 @@ HTTP Signature (currently a [IETF draft][http-signature-ietf-draft]) provides a
 
 [Djoser][djoser] library provides a set of views to handle basic actions such as registration, login, logout, password reset and account activation. The package works with a custom user model and uses token-based authentication. This is a ready to use REST implementation of the Django authentication system.
 
+## DRF Auth Kit
+
+[DRF Auth Kit][drf-auth-kit] library provides a modern REST authentication solution with JWT cookies, social login, multi-factor authentication, and comprehensive user management. The package offers full type safety, automatic OpenAPI schema generation with DRF Spectacular. It supports multiple authentication types (JWT, DRF Token, or Custom) and includes built-in internationalization for 50+ languages.
+
+
 ## django-rest-auth / dj-rest-auth
 
 This library provides a set of REST API endpoints for registration, authentication (including social media authentication), password reset, retrieve and update user details, etc. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for user management.
@@ -454,7 +459,7 @@ There are currently two forks of this project.
 
 More information can be found in the [Documentation](https://django-rest-durin.readthedocs.io/en/latest/index.html).
 
-## django-pyoidc
+## django-pyoidc
 
 [dango-pyoidc][django_pyoidc] adds support for OpenID Connect (OIDC) authentication. This allows you to delegate user management to an Identity Provider, which can be used to implement Single-Sign-On (SSO). It provides support for most uses-cases, such as customizing how token info are mapped to user models, using OIDC audiences for access control, etc.
 
@@ -497,4 +502,5 @@ More information can be found in the [Documentation](https://django-pyoidc.readt
 [django-rest-authemail]: https://github.com/celiao/django-rest-authemail
 [django-rest-durin]: https://github.com/eshaan7/django-rest-durin
 [login-required-middleware]: https://docs.djangoproject.com/en/stable/ref/middleware/#django.contrib.auth.middleware.LoginRequiredMiddleware
-[django-pyoidc] : https://github.com/makinacorpus/django_pyoidc
+[django-pyoidc]: https://github.com/makinacorpus/django_pyoidc
+[drf-auth-kit]: https://github.com/huynguyengl99/drf-auth-kit
```



 - `.reference/api-guide/throttling.md`

```
ffadde930ef23983f123477964d201c278f107e9 -> 64c3d9ef63bc073d01063934ab952cd1b990ecf2
@@ -110,7 +110,7 @@ You'll need to remember to also set your custom throttle class in the `'DEFAULT_
 
 The built-in throttle implementations are open to [race conditions][race], so under high concurrency they may allow a few extra requests through.
 
-If your project relies on guaranteeing the number of requests during concurrent requests, you will need to implement your own throttle class.
+If your project relies on guaranteeing the number of requests during concurrent requests, you will need to implement your own throttle class. See [issue #5181][gh5181] for more details.
 
 ---
 
@@ -220,4 +220,5 @@ The following is an example of a rate throttle, that will randomly throttle 1 in
 [identifying-clients]: http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster
 [cache-setting]: https://docs.djangoproject.com/en/stable/ref/settings/#caches
 [cache-docs]: https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache
+[gh5181]: https://github.com/encode/django-rest-framework/issues/5181
 [race]: https://en.wikipedia.org/wiki/Race_condition#Data_race
```



 - `.reference/api-guide/schemas.md`

```
985dd732e058644f6e875de76205a392ce4241dd -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -20,7 +20,7 @@ package and then subsequently retired over the next releases.
 
 As a full-fledged replacement, we recommend the [drf-spectacular] package.
 It has extensive support for generating OpenAPI 3 schemas from
-REST framework APIs, with both automatic and customisable options available.
+REST framework APIs, with both automatic and customizable options available.
 For further information please refer to
 [Documenting your API](../topics/documenting-your-api.md#drf-spectacular).
 
@@ -392,7 +392,7 @@ introspection.
 
 #### `get_operation_id()`
 
-There must be a unique [operationid](openapi-operationid) for each operation.
+There must be a unique [operationid][openapi-operationid] for each operation.
 By default the `operationId` is deduced from the model name, serializer name or
 view name. The operationId looks like "listItems", "retrieveItem",
 "updateItem", etc. The `operationId` is camelCase by convention.
@@ -453,12 +453,12 @@ create a base `AutoSchema` subclass for your project that takes additional
 
 [cite]: https://www.heroku.com/blog/json_schema_for_heroku_platform_api/
 [openapi]: https://github.com/OAI/OpenAPI-Specification
-[openapi-specification-extensions]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#specification-extensions
-[openapi-operation]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject
+[openapi-specification-extensions]: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#specification-extensions
+[openapi-operation]: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#operationObject
 [openapi-tags]: https://swagger.io/specification/#tagObject
-[openapi-operationid]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#fixed-fields-17
-[openapi-components]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject
-[openapi-reference]: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#referenceObject
+[openapi-operationid]: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#fixed-fields-17
+[openapi-components]: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#componentsObject
+[openapi-reference]: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#referenceObject
 [openapi-generator]: https://github.com/OpenAPITools/openapi-generator
 [swagger-codegen]: https://github.com/swagger-api/swagger-codegen
 [info-object]: https://swagger.io/specification/#infoObject
```



 - `.reference/api-guide/settings.md`

```
b483179b93ade3ffbec7f1a7569a1c1c516666d4 -> c8b6d3dcdf0a9fe04eb914e29e18efa42fe59a6c
@@ -314,6 +314,15 @@ May be a list including the string `'iso-8601'` or Python [strftime format][strf
 
 Default: `['iso-8601']`
 
+
+#### DURATION_FORMAT
+
+Indicates the default format that should be used for rendering the output of `DurationField` serializer fields.  If `None`, then `DurationField` serializer fields will return Python `timedelta` objects, and the duration encoding will be determined by the renderer.
+
+May be any of `None`, `'iso-8601'` or `'django'` (the format accepted by `django.utils.dateparse.parse_duration`).
+
+Default: `'django'`
+
 ---
 
 ## Encodings
```



 - `.reference/api-guide/viewsets.md`

```
f8dbea1a4559dd8635ac877a9bffb3599d336132 -> 9b3d03a3d257bca3eb99ca82770908adc7486a37
@@ -231,7 +231,7 @@ Using the example from the previous section:
 Alternatively, you can use the `url_name` attribute set by the `@action` decorator.
 
 ```pycon
->>> view.reverse_action(view.set_password.url_name, args=['1'])
+>>> view.reverse_action(view.set_password.url_name, args=["1"])
 'http://localhost:8000/api/users/1/set_password'
 ```
```



 - `.reference/api-guide/fields.md`

```
30384947053b1f2b2c9e82cafd1da934d3442a61 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -180,7 +180,7 @@ The `allow_null` option is also available for string fields, although its usage
 
 ## EmailField
 
-A text representation, validates the text to be a valid e-mail address.
+A text representation, validates the text to be a valid email address.
 
 Corresponds to `django.db.models.fields.EmailField`
 
@@ -377,13 +377,16 @@ A Duration representation.
 Corresponds to `django.db.models.fields.DurationField`
 
 The `validated_data` for these fields will contain a `datetime.timedelta` instance.
-The representation is a string following this format `'[DD] [HH:[MM:]]ss[.uuuuuu]'`.
 
-**Signature:** `DurationField(max_value=None, min_value=None)`
+**Signature:** `DurationField(format=api_settings.DURATION_FORMAT, max_value=None, min_value=None)`
 
+* `format` - A string representing the output format.  If not specified, this defaults to the same value as the `DURATION_FORMAT` settings key, which will be `'django'` unless set. Formats are described below. Setting this value to `None` indicates that Python `timedelta` objects should be returned by `to_representation`. In this case the date encoding will be determined by the renderer.
 * `max_value` Validate that the duration provided is no greater than this value.
 * `min_value` Validate that the duration provided is no less than this value.
 
+#### `DurationField` formats
+Format may either be the special string `'iso-8601'`, which indicates that [ISO 8601][iso8601] style intervals should be used (eg `'P4DT1H15M20S'`), or `'django'` which indicates that Django interval format `'[DD] [HH:[MM:]]ss[.uuuuuu]'` should be used (eg: `'4 1:15:20'`).
+
 ---
 
 # Choice selection fields
@@ -759,7 +762,7 @@ suitable for updating our target object. With `source='*'`, the return from
                      ('y_coordinate', 4),
                      ('x_coordinate', 3)])
 
-For completeness lets do the same thing again but with the nested serializer
+For completeness let's do the same thing again but with the nested serializer
 approach suggested above:
 
     class NestedCoordinateSerializer(serializers.Serializer):
```



 - `.reference/api-guide/views.md`

```
041b88f8bbb48d9688ebd5add294eee2dfc93d1c -> cf923511e7bbd1d05b6919af9af4e5edd81f5b71
@@ -186,8 +186,13 @@ The available decorators are:
 * `@authentication_classes(...)`
 * `@throttle_classes(...)`
 * `@permission_classes(...)`
+* `@content_negotiation_class(...)`
+* `@metadata_class(...)`
+* `@versioning_class(...)`
 
-Each of these decorators takes a single argument which must be a list or tuple of classes.
+Each of these decorators is equivalent to setting their respective [api policy attributes][api-policy-attributes].
+
+All decorators take a single argument. The ones that end with `_class` expect a single class while the ones ending in `_classes` expect a list or tuple of classes.
 
 
 ## View schema decorator
@@ -224,4 +229,5 @@ You may pass `None` in order to exclude the view from schema generation.
 [throttling]: throttling.md
 [schemas]: schemas.md
 [classy-drf]: http://www.cdrf.co
+[api-policy-attributes]: views.md#api-policy-attributes
```



 - `.reference/tutorial/1-serialization.md`

```
d3dd45b3f48856c3513ab1eb5354194fa9898f39 -> c0f3649224117609d19e79c77242b525570d25c0
@@ -16,14 +16,18 @@ The tutorial is fairly in-depth, so you should probably get a cookie and a cup o
 
 Before we do anything else we'll create a new virtual environment, using [venv]. This will make sure our package configuration is kept nicely isolated from any other projects we're working on.
 
-    python3 -m venv env
-    source env/bin/activate
+```bash
+python3 -m venv env
+source env/bin/activate
+```
 
 Now that we're inside a virtual environment, we can install our package requirements.
 
-    pip install django
-    pip install djangorestframework
-    pip install pygments  # We'll be using this for the code highlighting
+```bash
+pip install django
+pip install djangorestframework
+pip install pygments  # We'll be using this for the code highlighting
+```
 
 **Note:** To exit the virtual environment at any time, just type `deactivate`.  For more information see the [venv documentation][venv].
 
@@ -32,21 +36,27 @@ Now that we're inside a virtual environment, we can install our package requirem
 Okay, we're ready to get coding.
 To get started, let's create a new project to work with.
 
-    cd ~
-    django-admin startproject tutorial
-    cd tutorial
+```bash
+cd ~
+django-admin startproject tutorial
+cd tutorial
+```
 
 Once that's done we can create an app that we'll use to create a simple Web API.
 
-    python manage.py startapp snippets
+```bash
+python manage.py startapp snippets
+```
 
 We'll need to add our new `snippets` app and the `rest_framework` app to `INSTALLED_APPS`. Let's edit the `tutorial/settings.py` file:
 
-    INSTALLED_APPS = [
-        ...
-        'rest_framework',
-        'snippets',
-    ]
+```text
+INSTALLED_APPS = [
+    ...
+    'rest_framework',
+    'snippets',
+]
+```
 
 Okay, we're ready to roll.
 
@@ -54,64 +64,72 @@ Okay, we're ready to roll.
 
 For the purposes of this tutorial we're going to start by creating a simple `Snippet` model that is used to store code snippets.  Go ahead and edit the `snippets/models.py` file.  Note: Good programming practices include comments.  Although you will find them in our repository version of this tutorial code, we have omitted them here to focus on the code itself.
 
-    from django.db import models
-    from pygments.lexers import get_all_lexers
-    from pygments.styles import get_all_styles
+```python
+from django.db import models
+from pygments.lexers import get_all_lexers
+from pygments.styles import get_all_styles
 
-    LEXERS = [item for item in get_all_lexers() if item[1]]
-    LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
-    STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
+LEXERS = [item for item in get_all_lexers() if item[1]]
+LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
+STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
 
 
-    class Snippet(models.Model):
-        created = models.DateTimeField(auto_now_add=True)
-        title = models.CharField(max_length=100, blank=True, default='')
-        code = models.TextField()
-        linenos = models.BooleanField(default=False)
-        language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
-        style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
+class Snippet(models.Model):
+    created = models.DateTimeField(auto_now_add=True)
+    title = models.CharField(max_length=100, blank=True, default="")
+    code = models.TextField()
+    linenos = models.BooleanField(default=False)
+    language = models.CharField(
+        choices=LANGUAGE_CHOICES, default="python", max_length=100
+    )
+    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
 
-        class Meta:
-            ordering = ['created']
+    class Meta:
+        ordering = ["created"]
+```
 
 We'll also need to create an initial migration for our snippet model, and sync the database for the first time.
 
-    python manage.py makemigrations snippets
-    python manage.py migrate snippets
+```bash
+python manage.py makemigrations snippets
+python manage.py migrate snippets
+```
 
 ## Creating a Serializer class
 
 The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the snippet instances into representations such as `json`.  We can do this by declaring serializers that work very similar to Django's forms.  Create a file in the `snippets` directory named `serializers.py` and add the following.
 
-    from rest_framework import serializers
-    from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
-
-
-    class SnippetSerializer(serializers.Serializer):
-        id = serializers.IntegerField(read_only=True)
-        title = serializers.CharField(required=False, allow_blank=True, max_length=100)
-        code = serializers.CharField(style={'base_template': 'textarea.html'})
-        linenos = serializers.BooleanField(required=False)
-        language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
-        style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
-
-        def create(self, validated_data):
-            """
-            Create and return a new `Snippet` instance, given the validated data.
-            """
-            return Snippet.objects.create(**validated_data)
-
-        def update(self, instance, validated_data):
-            """
-            Update and return an existing `Snippet` instance, given the validated data.
-            """
-            instance.title = validated_data.get('title', instance.title)
-            instance.code = validated_data.get('code', instance.code)
-            instance.linenos = validated_data.get('linenos', instance.linenos)
-            instance.language = validated_data.get('language', instance.language)
-            instance.style = validated_data.get('style', instance.style)
-            instance.save()
-            return instance
+```python
+from rest_framework import serializers
+from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
+
+
+class SnippetSerializer(serializers.Serializer):
+    id = serializers.IntegerField(read_only=True)
+    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
+    code = serializers.CharField(style={"base_template": "textarea.html"})
+    linenos = serializers.BooleanField(required=False)
+    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
+    style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")
+
+    def create(self, validated_data):
+        """
+        Create and return a new `Snippet` instance, given the validated data.
+        """
+        return Snippet.objects.create(**validated_data)
+
+    def update(self, instance, validated_data):
+        """
+        Update and return an existing `Snippet` instance, given the validated data.
+        """
+        instance.title = validated_data.get("title", instance.title)
+        instance.code = validated_data.get("code", instance.code)
+        instance.linenos = validated_data.get("linenos", instance.linenos)
+        instance.language = validated_data.get("language", instance.language)
+        instance.style = validated_data.get("style", instance.style)
+        instance.save()
+        return instance
+```
 
 The first part of the serializer class defines the fields that get serialized/deserialized.  The `create()` and `update()` methods define how fully fledged instances are created or modified when calling `serializer.save()`
 
@@ -125,57 +143,71 @@ We can actually also save ourselves some time by using the `ModelSerializer` cla
 
 Before we go any further we'll familiarize ourselves with using our new Serializer class.  Let's drop into the Django shell.
 
-    python manage.py shell
+```bash
+python manage.py shell
+```
 
 Okay, once we've got a few imports out of the way, let's create a couple of code snippets to work with.
 
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
-    from rest_framework.renderers import JSONRenderer
-    from rest_framework.parsers import JSONParser
+```pycon
+>>> from snippets.models import Snippet
+>>> from snippets.serializers import SnippetSerializer
+>>> from rest_framework.renderers import JSONRenderer
+>>> from rest_framework.parsers import JSONParser
 
-    snippet = Snippet(code='foo = "bar"\n')
-    snippet.save()
+>>> snippet = Snippet(code='foo = "bar"\n')
+>>> snippet.save()
 
-    snippet = Snippet(code='print("hello, world")\n')
-    snippet.save()
+>>> snippet = Snippet(code='print("hello, world")\n')
+>>> snippet.save()
+```
 
 We've now got a few snippet instances to play with.  Let's take a look at serializing one of those instances.
 
-    serializer = SnippetSerializer(snippet)
-    serializer.data
-    # {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
+```pycon
+>>> serializer = SnippetSerializer(snippet)
+>>> serializer.data
+{'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
+```
 
 At this point we've translated the model instance into Python native datatypes.  To finalize the serialization process we render the data into `json`.
 
-    content = JSONRenderer().render(serializer.data)
-    content
-    # b'{"id":2,"title":"","code":"print(\\"hello, world\\")\\n","linenos":false,"language":"python","style":"friendly"}'
+```pycon
+>>> content = JSONRenderer().render(serializer.data)
+>>> content
+b'{"id":2,"title":"","code":"print(\\"hello, world\\")\\n","linenos":false,"language":"python","style":"friendly"}'
+```
 
 Deserialization is similar.  First we parse a stream into Python native datatypes...
 
-    import io
+```pycon
+>>> import io
 
-    stream = io.BytesIO(content)
-    data = JSONParser().parse(stream)
+>>> stream = io.BytesIO(content)
+>>> data = JSONParser().parse(stream)
+```
 
 ...then we restore those native datatypes into a fully populated object instance.
 
-    serializer = SnippetSerializer(data=data)
-    serializer.is_valid()
-    # True
-    serializer.validated_data
-    # {'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}
-    serializer.save()
-    # <Snippet: Snippet object>
+```pycon
+>>> serializer = SnippetSerializer(data=data)
+>>> serializer.is_valid()
+True
+>>> serializer.validated_data
+{'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}
+>>> serializer.save()
+<Snippet: Snippet object>
+```
 
 Notice how similar the API is to working with forms.  The similarity should become even more apparent when we start writing views that use our serializer.
 
 We can also serialize querysets instead of model instances.  To do so we simply add a `many=True` flag to the serializer arguments.
 
-    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
-    serializer.data
-    # [{'id': 1, 'title': '', 'code': 'foo = "bar"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
+```pycon
+>>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
+>>> serializer.data
+[{'id': 1, 'title': '', 'code': 'foo = "bar"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
+```
 
 ## Using ModelSerializers
 
@@ -186,23 +218,28 @@ In the same way that Django provides both `Form` classes and `ModelForm` classes
 Let's look at refactoring our serializer using the `ModelSerializer` class.
 Open the file `snippets/serializers.py` again, and replace the `SnippetSerializer` class with the following.
 
-    class SnippetSerializer(serializers.ModelSerializer):
-        class Meta:
-            model = Snippet
-            fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
+```python
+class SnippetSerializer(serializers.ModelSerializer):
+    class Meta:
+        model = Snippet
+        fields = ["id", "title", "code", "linenos", "language", "style"]
+```
 
 One nice property that serializers have is that you can inspect all the fields in a serializer instance, by printing its representation. Open the Django shell with `python manage.py shell`, then try the following:
 
-    from snippets.serializers import SnippetSerializer
-    serializer = SnippetSerializer()
-    print(repr(serializer))
-    # SnippetSerializer():
-    #    id = IntegerField(label='ID', read_only=True)
-    #    title = CharField(allow_blank=True, max_length=100, required=False)
-    #    code = CharField(style={'base_template': 'textarea.html'})
-    #    linenos = BooleanField(required=False)
-    #    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
-    #    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
+```pycon
+>>> from snippets.serializers import SnippetSerializer
+
+>>> serializer = SnippetSerializer()
+>>> print(repr(serializer))
+SnippetSerializer():
+    id = IntegerField(label='ID', read_only=True)
+    title = CharField(allow_blank=True, max_length=100, required=False)
+    code = CharField(style={'base_template': 'textarea.html'})
+    linenos = BooleanField(required=False)
+    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'), ('abap', 'ABAP'), ('ada', 'Ada')...
+    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')...
+```
 
 It's important to remember that `ModelSerializer` classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:
 
@@ -216,79 +253,89 @@ For the moment we won't use any of REST framework's other features, we'll just w
 
 Edit the `snippets/views.py` file, and add the following.
 
-    from django.http import HttpResponse, JsonResponse
-    from django.views.decorators.csrf import csrf_exempt
-    from rest_framework.parsers import JSONParser
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
+```python
+from django.http import HttpResponse, JsonResponse
+from django.views.decorators.csrf import csrf_exempt
+from rest_framework.parsers import JSONParser
+from snippets.models import Snippet
+from snippets.serializers import SnippetSerializer
+```
 
 The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
 
-    @csrf_exempt
-    def snippet_list(request):
-        """
-        List all code snippets, or create a new snippet.
-        """
-        if request.method == 'GET':
-            snippets = Snippet.objects.all()
-            serializer = SnippetSerializer(snippets, many=True)
-            return JsonResponse(serializer.data, safe=False)
-
-        elif request.method == 'POST':
-            data = JSONParser().parse(request)
-            serializer = SnippetSerializer(data=data)
-            if serializer.is_valid():
-                serializer.save()
-                return JsonResponse(serializer.data, status=201)
-            return JsonResponse(serializer.errors, status=400)
+```python
+@csrf_exempt
+def snippet_list(request):
+    """
+    List all code snippets, or create a new snippet.
+    """
+    if request.method == "GET":
+        snippets = Snippet.objects.all()
+        serializer = SnippetSerializer(snippets, many=True)
+        return JsonResponse(serializer.data, safe=False)
+
+    elif request.method == "POST":
+        data = JSONParser().parse(request)
+        serializer = SnippetSerializer(data=data)
+        if serializer.is_valid():
+            serializer.save()
+            return JsonResponse(serializer.data, status=201)
+        return JsonResponse(serializer.errors, status=400)
+```
 
 Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as `csrf_exempt`.  This isn't something that you'd normally want to do, and REST framework views actually use more sensible behavior than this, but it'll do for our purposes right now.
 
 We'll also need a view which corresponds to an individual snippet, and can be used to retrieve, update or delete the snippet.
 
-    @csrf_exempt
-    def snippet_detail(request, pk):
-        """
-        Retrieve, update or delete a code snippet.
-        """
-        try:
-            snippet = Snippet.objects.get(pk=pk)
-        except Snippet.DoesNotExist:
-            return HttpResponse(status=404)
-
-        if request.method == 'GET':
-            serializer = SnippetSerializer(snippet)
+```python
+@csrf_exempt
+def snippet_detail(request, pk):
+    """
+    Retrieve, update or delete a code snippet.
+    """
+    try:
+        snippet = Snippet.objects.get(pk=pk)
+    except Snippet.DoesNotExist:
+        return HttpResponse(status=404)
+
+    if request.method == "GET":
+        serializer = SnippetSerializer(snippet)
+        return JsonResponse(serializer.data)
+
+    elif request.method == "PUT":
+        data = JSONParser().parse(request)
+        serializer = SnippetSerializer(snippet, data=data)
+        if serializer.is_valid():
+            serializer.save()
             return JsonResponse(serializer.data)
+        return JsonResponse(serializer.errors, status=400)
 
-        elif request.method == 'PUT':
-            data = JSONParser().parse(request)
-            serializer = SnippetSerializer(snippet, data=data)
-            if serializer.is_valid():
-                serializer.save()
-                return JsonResponse(serializer.data)
-            return JsonResponse(serializer.errors, status=400)
-
-        elif request.method == 'DELETE':
-            snippet.delete()
-            return HttpResponse(status=204)
+    elif request.method == "DELETE":
+        snippet.delete()
+        return HttpResponse(status=204)
+```
 
 Finally we need to wire these views up.  Create the `snippets/urls.py` file:
 
-    from django.urls import path
-    from snippets import views
+```python
+from django.urls import path
+from snippets import views
 
-    urlpatterns = [
-        path('snippets/', views.snippet_list),
-        path('snippets/<int:pk>/', views.snippet_detail),
-    ]
+urlpatterns = [
+    path("snippets/", views.snippet_list),
+    path("snippets/<int:pk>/", views.snippet_detail),
+]
+```
 
 We also need to wire up the root urlconf, in the `tutorial/urls.py` file, to include our snippet app's URLs.
 
-    from django.urls import path, include
+```python
+from django.urls import path, include
 
-    urlpatterns = [
-        path('', include('snippets.urls')),
-    ]
+urlpatterns = [
+    path("", include("snippets.urls")),
+]
+```
 
 It's worth noting that there are a couple of edge cases we're not dealing with properly at the moment.  If we send malformed `json`, or if a request is made with a method that the view doesn't handle, then we'll end up with a 500 "server error" response.  Still, this'll do for now.
 
@@ -298,18 +345,22 @@ Now we can start up a sample server that serves our snippets.
 
 Quit out of the shell...
 
-    quit()
+```pycon
+>>> quit()
+```
 
 ...and start up Django's development server.
 
-    python manage.py runserver
+```bash
+python manage.py runserver
 
-    Validating models...
+Validating models...
 
-    0 errors found
-    Django version 5.0, using settings 'tutorial.settings'
-    Starting Development server at http://127.0.0.1:8000/
-    Quit the server with CONTROL-C.
+0 errors found
+Django version 5.0, using settings 'tutorial.settings'
+Starting Development server at http://127.0.0.1:8000/
+Quit the server with CONTROL-C.
+```
 
 In another terminal window, we can test the server.
 
@@ -317,47 +368,26 @@ We can test our API using [curl][curl] or [httpie][httpie]. Httpie is a user fri
 
 You can install httpie using pip:
 
-    pip install httpie
+```bash
+pip install httpie
+```
 
 Finally, we can get a list of all of the snippets:
 
-    http GET http://127.0.0.1:8000/snippets/ --unsorted
-
-    HTTP/1.1 200 OK
-    ...
-    [
-        {
-            "id": 1,
-            "title": "",
-            "code": "foo = \"bar\"\n",
-            "linenos": false,
-            "language": "python",
-            "style": "friendly"
-        },
-        {
-            "id": 2,
-            "title": "",
-            "code": "print(\"hello, world\")\n",
-            "linenos": false,
-            "language": "python",
-            "style": "friendly"
-        },
-        {
-            "id": 3,
-            "title": "",
-            "code": "print(\"hello, world\")",
-            "linenos": false,
-            "language": "python",
-            "style": "friendly"
-        }
-    ]
+```bash
+http GET http://127.0.0.1:8000/snippets/ --unsorted
 
-Or we can get a particular snippet by referencing its id:
-
-    http GET http://127.0.0.1:8000/snippets/2/ --unsorted
-
-    HTTP/1.1 200 OK
-    ...
+HTTP/1.1 200 OK
+...
+[
+    {
+        "id": 1,
+        "title": "",
+        "code": "foo = \"bar\"\n",
+        "linenos": false,
+        "language": "python",
+        "style": "friendly"
+    },
     {
         "id": 2,
         "title": "",
@@ -365,7 +395,34 @@ Or we can get a particular snippet by referencing its id:
         "linenos": false,
         "language": "python",
         "style": "friendly"
+    },
+    {
+        "id": 3,
+        "title": "",
+        "code": "print(\"hello, world\")",
+        "linenos": false,
+        "language": "python",
+        "style": "friendly"
     }
+]
+```
+
+Or we can get a particular snippet by referencing its id:
+
+```bash
+http GET http://127.0.0.1:8000/snippets/2/ --unsorted
+
+HTTP/1.1 200 OK
+...
+{
+    "id": 2,
+    "title": "",
+    "code": "print(\"hello, world\")\n",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+}
+```
 
 Similarly, you can have the same json displayed by visiting these URLs in a web browser.
```



 - `.reference/tutorial/3-class-based-views.md`

```
041b88f8bbb48d9688ebd5add294eee2dfc93d1c -> c0f3649224117609d19e79c77242b525570d25c0
@@ -6,74 +6,82 @@ We can also write our API views using class-based views, rather than function ba
 
 We'll start by rewriting the root view as a class-based view.  All this involves is a little bit of refactoring of `views.py`.
 
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
-    from django.http import Http404
-    from rest_framework.views import APIView
-    from rest_framework.response import Response
-    from rest_framework import status
-
-
-    class SnippetList(APIView):
-        """
-        List all snippets, or create a new snippet.
-        """
-        def get(self, request, format=None):
-            snippets = Snippet.objects.all()
-            serializer = SnippetSerializer(snippets, many=True)
-            return Response(serializer.data)
-
-        def post(self, request, format=None):
-            serializer = SnippetSerializer(data=request.data)
-            if serializer.is_valid():
-                serializer.save()
-                return Response(serializer.data, status=status.HTTP_201_CREATED)
-            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
+```python
+from snippets.models import Snippet
+from snippets.serializers import SnippetSerializer
+from django.http import Http404
+from rest_framework.views import APIView
+from rest_framework.response import Response
+from rest_framework import status
+
+
+class SnippetList(APIView):
+    """
+    List all snippets, or create a new snippet.
+    """
+
+    def get(self, request, format=None):
+        snippets = Snippet.objects.all()
+        serializer = SnippetSerializer(snippets, many=True)
+        return Response(serializer.data)
+
+    def post(self, request, format=None):
+        serializer = SnippetSerializer(data=request.data)
+        if serializer.is_valid():
+            serializer.save()
+            return Response(serializer.data, status=status.HTTP_201_CREATED)
+        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
+```
 
 So far, so good.  It looks pretty similar to the previous case, but we've got better separation between the different HTTP methods.  We'll also need to update the instance view in `views.py`.
 
-    class SnippetDetail(APIView):
-        """
-        Retrieve, update or delete a snippet instance.
-        """
-        def get_object(self, pk):
-            try:
-                return Snippet.objects.get(pk=pk)
-            except Snippet.DoesNotExist:
-                raise Http404
-
-        def get(self, request, pk, format=None):
-            snippet = self.get_object(pk)
-            serializer = SnippetSerializer(snippet)
+```python
+class SnippetDetail(APIView):
+    """
+    Retrieve, update or delete a snippet instance.
+    """
+
+    def get_object(self, pk):
+        try:
+            return Snippet.objects.get(pk=pk)
+        except Snippet.DoesNotExist:
+            raise Http404
+
+    def get(self, request, pk, format=None):
+        snippet = self.get_object(pk)
+        serializer = SnippetSerializer(snippet)
+        return Response(serializer.data)
+
+    def put(self, request, pk, format=None):
+        snippet = self.get_object(pk)
+        serializer = SnippetSerializer(snippet, data=request.data)
+        if serializer.is_valid():
+            serializer.save()
             return Response(serializer.data)
+        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
-        def put(self, request, pk, format=None):
-            snippet = self.get_object(pk)
-            serializer = SnippetSerializer(snippet, data=request.data)
-            if serializer.is_valid():
-                serializer.save()
-                return Response(serializer.data)
-            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
-
-        def delete(self, request, pk, format=None):
-            snippet = self.get_object(pk)
-            snippet.delete()
-            return Response(status=status.HTTP_204_NO_CONTENT)
+    def delete(self, request, pk, format=None):
+        snippet = self.get_object(pk)
+        snippet.delete()
+        return Response(status=status.HTTP_204_NO_CONTENT)
+```
 
 That's looking good.  Again, it's still pretty similar to the function based view right now.
 
 We'll also need to refactor our `snippets/urls.py` slightly now that we're using class-based views.
 
-    from django.urls import path
-    from rest_framework.urlpatterns import format_suffix_patterns
-    from snippets import views
+```python
+from django.urls import path
+from rest_framework.urlpatterns import format_suffix_patterns
+from snippets import views
 
-    urlpatterns = [
-        path('snippets/', views.SnippetList.as_view()),
-        path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
-    ]
+urlpatterns = [
+    path("snippets/", views.SnippetList.as_view()),
+    path("snippets/<int:pk>/", views.SnippetDetail.as_view()),
+]
 
-    urlpatterns = format_suffix_patterns(urlpatterns)
+urlpatterns = format_suffix_patterns(urlpatterns)
+```
 
 Okay, we're done.  If you run the development server everything should be working just as before.
 
@@ -85,42 +93,49 @@ The create/retrieve/update/delete operations that we've been using so far are go
 
 Let's take a look at how we can compose the views by using the mixin classes.  Here's our `views.py` module again.
 
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
-    from rest_framework import mixins
-    from rest_framework import generics
+```python
+from snippets.models import Snippet
+from snippets.serializers import SnippetSerializer
+from rest_framework import mixins
+from rest_framework import generics
+
 
-    class SnippetList(mixins.ListModelMixin,
-                      mixins.CreateModelMixin,
-                      generics.GenericAPIView):
-        queryset = Snippet.objects.all()
-        serializer_class = SnippetSerializer
+class SnippetList(
+    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
+):
+    queryset = Snippet.objects.all()
+    serializer_class = SnippetSerializer
 
-        def get(self, request, *args, **kwargs):
-            return self.list(request, *args, **kwargs)
+    def get(self, request, *args, **kwargs):
+        return self.list(request, *args, **kwargs)
 
-        def post(self, request, *args, **kwargs):
-            return self.create(request, *args, **kwargs)
+    def post(self, request, *args, **kwargs):
+        return self.create(request, *args, **kwargs)
+```
 
 We'll take a moment to examine exactly what's happening here.  We're building our view using `GenericAPIView`, and adding in `ListModelMixin` and `CreateModelMixin`.
 
 The base class provides the core functionality, and the mixin classes provide the `.list()` and `.create()` actions.  We're then explicitly binding the `get` and `post` methods to the appropriate actions.  Simple enough stuff so far.
 
-    class SnippetDetail(mixins.RetrieveModelMixin,
-                        mixins.UpdateModelMixin,
-                        mixins.DestroyModelMixin,
-                        generics.GenericAPIView):
-        queryset = Snippet.objects.all()
-        serializer_class = SnippetSerializer
+```python
+class SnippetDetail(
+    mixins.RetrieveModelMixin,
+    mixins.UpdateModelMixin,
+    mixins.DestroyModelMixin,
+    generics.GenericAPIView,
+):
+    queryset = Snippet.objects.all()
+    serializer_class = SnippetSerializer
 
-        def get(self, request, *args, **kwargs):
-            return self.retrieve(request, *args, **kwargs)
+    def get(self, request, *args, **kwargs):
+        return self.retrieve(request, *args, **kwargs)
 
-        def put(self, request, *args, **kwargs):
-            return self.update(request, *args, **kwargs)
+    def put(self, request, *args, **kwargs):
+        return self.update(request, *args, **kwargs)
 
-        def delete(self, request, *args, **kwargs):
-            return self.destroy(request, *args, **kwargs)
+    def delete(self, request, *args, **kwargs):
+        return self.destroy(request, *args, **kwargs)
+```
 
 Pretty similar.  Again we're using the `GenericAPIView` class to provide the core functionality, and adding in mixins to provide the `.retrieve()`, `.update()` and `.destroy()` actions.
 
@@ -128,19 +143,21 @@ Pretty similar.  Again we're using the `GenericAPIView` class to provide the cor
 
 Using the mixin classes we've rewritten the views to use slightly less code than before, but we can go one step further.  REST framework provides a set of already mixed-in generic views that we can use to trim down our `views.py` module even more.
 
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
-    from rest_framework import generics
+```python
+from snippets.models import Snippet
+from snippets.serializers import SnippetSerializer
+from rest_framework import generics
 
 
-    class SnippetList(generics.ListCreateAPIView):
-        queryset = Snippet.objects.all()
-        serializer_class = SnippetSerializer
+class SnippetList(generics.ListCreateAPIView):
+    queryset = Snippet.objects.all()
+    serializer_class = SnippetSerializer
 
 
-    class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
-        queryset = Snippet.objects.all()
-        serializer_class = SnippetSerializer
+class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
+    queryset = Snippet.objects.all()
+    serializer_class = SnippetSerializer
+```
 
 Wow, that's pretty concise.  We've gotten a huge amount for free, and our code looks like good, clean, idiomatic Django.
```



 - `.reference/tutorial/quickstart.md`

```
f4daa98f48f9a25079531058fba4387949a4b54f -> c0f3649224117609d19e79c77242b525570d25c0
@@ -6,57 +6,65 @@ We're going to create a simple API to allow admin users to view and edit the use
 
 Create a new Django project named `tutorial`, then start a new app called `quickstart`.
 
-    # Create the project directory
-    mkdir tutorial
-    cd tutorial
+```bash
+# Create the project directory
+mkdir tutorial
+cd tutorial
 
-    # Create a virtual environment to isolate our package dependencies locally
-    python3 -m venv env
-    source env/bin/activate  # On Windows use `env\Scripts\activate`
+# Create a virtual environment to isolate our package dependencies locally
+python3 -m venv env
+source env/bin/activate  # On Windows use `env\Scripts\activate`
 
-    # Install Django and Django REST framework into the virtual environment
-    pip install djangorestframework
+# Install Django and Django REST framework into the virtual environment
+pip install djangorestframework
 
-    # Set up a new project with a single application
-    django-admin startproject tutorial .  # Note the trailing '.' character
-    cd tutorial
-    django-admin startapp quickstart
-    cd ..
+# Set up a new project with a single application
+django-admin startproject tutorial .  # Note the trailing '.' character
+cd tutorial
+django-admin startapp quickstart
+cd ..
+```
 
 The project layout should look like:
 
-    $ pwd
-    <some path>/tutorial
-    $ find .
-    .
-    ./tutorial
-    ./tutorial/asgi.py
-    ./tutorial/__init__.py
-    ./tutorial/quickstart
-    ./tutorial/quickstart/migrations
-    ./tutorial/quickstart/migrations/__init__.py
-    ./tutorial/quickstart/models.py
-    ./tutorial/quickstart/__init__.py
-    ./tutorial/quickstart/apps.py
-    ./tutorial/quickstart/admin.py
-    ./tutorial/quickstart/tests.py
-    ./tutorial/quickstart/views.py
-    ./tutorial/settings.py
-    ./tutorial/urls.py
-    ./tutorial/wsgi.py
-    ./env
-    ./env/...
-    ./manage.py
+```bash
+$ pwd
+<some path>/tutorial
+$ find .
+.
+./tutorial
+./tutorial/asgi.py
+./tutorial/__init__.py
+./tutorial/quickstart
+./tutorial/quickstart/migrations
+./tutorial/quickstart/migrations/__init__.py
+./tutorial/quickstart/models.py
+./tutorial/quickstart/__init__.py
+./tutorial/quickstart/apps.py
+./tutorial/quickstart/admin.py
+./tutorial/quickstart/tests.py
+./tutorial/quickstart/views.py
+./tutorial/settings.py
+./tutorial/urls.py
+./tutorial/wsgi.py
+./env
+./env/...
+./manage.py
+```
 
 It may look unusual that the application has been created within the project directory. Using the project's namespace avoids name clashes with external modules (a topic that goes outside the scope of the quickstart).
 
 Now sync your database for the first time:
 
-    python manage.py migrate
+```bash
+python manage.py migrate
+```
 
 We'll also create an initial user named `admin` with a password. We'll authenticate as that user later in our example.
 
-    python manage.py createsuperuser --username admin --email admin@example.com
+```bash
+python manage.py createsuperuser --username admin --email admin@example.com
+```
 
 Once you've set up a database and the initial user is created and ready to go, open up the app's directory and we'll get coding...
 
@@ -64,20 +72,22 @@ Once you've set up a database and the initial user is created and ready to go, o
 
 First up we're going to define some serializers. Let's create a new module named `tutorial/quickstart/serializers.py` that we'll use for our data representations.
 
-    from django.contrib.auth.models import Group, User
-    from rest_framework import serializers
+```python
+from django.contrib.auth.models import Group, User
+from rest_framework import serializers
 
 
-    class UserSerializer(serializers.HyperlinkedModelSerializer):
-        class Meta:
-            model = User
-            fields = ['url', 'username', 'email', 'groups']
+class UserSerializer(serializers.HyperlinkedModelSerializer):
+    class Meta:
+        model = User
+        fields = ["url", "username", "email", "groups"]
 
 
-    class GroupSerializer(serializers.HyperlinkedModelSerializer):
-        class Meta:
-            model = Group
-            fields = ['url', 'name']
+class GroupSerializer(serializers.HyperlinkedModelSerializer):
+    class Meta:
+        model = Group
+        fields = ["url", "name"]
+```
 
 Notice that we're using hyperlinked relations in this case with `HyperlinkedModelSerializer`.  You can also use primary key and various other relationships, but hyperlinking is good RESTful design.
 
@@ -85,28 +95,32 @@ Notice that we're using hyperlinked relations in this case with `HyperlinkedMode
 
 Right, we'd better write some views then.  Open `tutorial/quickstart/views.py` and get typing.
 
-    from django.contrib.auth.models import Group, User
-    from rest_framework import permissions, viewsets
+```python
+from django.contrib.auth.models import Group, User
+from rest_framework import permissions, viewsets
 
-    from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
+from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
 
 
-    class UserViewSet(viewsets.ModelViewSet):
-        """
-        API endpoint that allows users to be viewed or edited.
-        """
-        queryset = User.objects.all().order_by('-date_joined')
-        serializer_class = UserSerializer
-        permission_classes = [permissions.IsAuthenticated]
+class UserViewSet(viewsets.ModelViewSet):
+    """
+    API endpoint that allows users to be viewed or edited.
+    """
 
+    queryset = User.objects.all().order_by("-date_joined")
+    serializer_class = UserSerializer
+    permission_classes = [permissions.IsAuthenticated]
 
-    class GroupViewSet(viewsets.ModelViewSet):
-        """
-        API endpoint that allows groups to be viewed or edited.
-        """
-        queryset = Group.objects.all().order_by('name')
-        serializer_class = GroupSerializer
-        permission_classes = [permissions.IsAuthenticated]
+
+class GroupViewSet(viewsets.ModelViewSet):
+    """
+    API endpoint that allows groups to be viewed or edited.
+    """
+
+    queryset = Group.objects.all().order_by("name")
+    serializer_class = GroupSerializer
+    permission_classes = [permissions.IsAuthenticated]
+```
 
 Rather than write multiple views we're grouping together all the common behavior into classes called `ViewSets`.
 
@@ -116,21 +130,23 @@ We can easily break these down into individual views if we need to, but using vi
 
 Okay, now let's wire up the API URLs.  On to `tutorial/urls.py`...
 
-    from django.urls import include, path
-    from rest_framework import routers
+```python
+from django.urls import include, path
+from rest_framework import routers
 
-    from tutorial.quickstart import views
+from tutorial.quickstart import views
 
-    router = routers.DefaultRouter()
-    router.register(r'users', views.UserViewSet)
-    router.register(r'groups', views.GroupViewSet)
+router = routers.DefaultRouter()
+router.register(r"users", views.UserViewSet)
+router.register(r"groups", views.GroupViewSet)
 
-    # Wire up our API using automatic URL routing.
-    # Additionally, we include login URLs for the browsable API.
-    urlpatterns = [
-        path('', include(router.urls)),
-        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
-    ]
+# Wire up our API using automatic URL routing.
+# Additionally, we include login URLs for the browsable API.
+urlpatterns = [
+    path("", include(router.urls)),
+    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
+]
+```
 
 Because we're using viewsets instead of views, we can automatically generate the URL conf for our API, by simply registering the viewsets with a router class.
 
@@ -139,21 +155,26 @@ Again, if we need more control over the API URLs we can simply drop down to usin
 Finally, we're including default login and logout views for use with the browsable API.  That's optional, but useful if your API requires authentication and you want to use the browsable API.
 
 ## Pagination
+
 Pagination allows you to control how many objects per page are returned. To enable it add the following lines to `tutorial/settings.py`
 
-    REST_FRAMEWORK = {
-        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
-        'PAGE_SIZE': 10
-    }
+```python
+REST_FRAMEWORK = {
+    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
+    "PAGE_SIZE": 10,
+}
+```
 
 ## Settings
 
 Add `'rest_framework'` to `INSTALLED_APPS`. The settings module will be in `tutorial/settings.py`
 
-    INSTALLED_APPS = [
-        ...
-        'rest_framework',
-    ]
+```text
+INSTALLED_APPS = [
+    ...
+    'rest_framework',
+]
+```
 
 Okay, we're done.
 
@@ -163,46 +184,51 @@ Okay, we're done.
 
 We're now ready to test the API we've built.  Let's fire up the server from the command line.
 
-    python manage.py runserver
+```bash
+python manage.py runserver
+```
 
 We can now access our API, both from the command-line, using tools like `curl`...
 
-    bash: curl -u admin -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/users/
-    Enter host password for user 'admin':
-    {
-        "count": 1,
-        "next": null,
-        "previous": null,
-        "results": [
-            {
-                "url": "http://127.0.0.1:8000/users/1/",
-                "username": "admin",
-                "email": "admin@example.com",
-                "groups": []
-            }
-        ]
-    }
+```bash
+bash: curl -u admin -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/users/
+Enter host password for user 'admin':
+{
+    "count": 1,
+    "next": null,
+    "previous": null,
+    "results": [
+        {
+            "url": "http://127.0.0.1:8000/users/1/",
+            "username": "admin",
+            "email": "admin@example.com",
+            "groups": []
+        }
+    ]
+}
+```
 
 Or using the [httpie][httpie], command line tool...
 
-    bash: http -a admin http://127.0.0.1:8000/users/
-    http: password for admin@127.0.0.1:8000:: 
-    $HTTP/1.1 200 OK
-    ...
-    {
-        "count": 1,
-        "next": null,
-        "previous": null,
-        "results": [
-            {
-                "email": "admin@example.com",
-                "groups": [],
-                "url": "http://127.0.0.1:8000/users/1/",
-                "username": "admin"
-            }
-        ]
-    }
-
+```bash
+bash: http -a admin http://127.0.0.1:8000/users/
+http: password for admin@127.0.0.1:8000:: 
+$HTTP/1.1 200 OK
+...
+{
+    "count": 1,
+    "next": null,
+    "previous": null,
+    "results": [
+        {
+            "email": "admin@example.com",
+            "groups": [],
+            "url": "http://127.0.0.1:8000/users/1/",
+            "username": "admin"
+        }
+    ]
+}
+```
 
 Or directly through the browser, by going to the URL `http://127.0.0.1:8000/users/`...
```



 - `.reference/tutorial/4-authentication-and-permissions.md`

```
380ac8e79dd85e6798eb00a730b7d4c4c4a86ebd -> c0f3649224117609d19e79c77242b525570d25c0
@@ -14,81 +14,103 @@ First, let's add a couple of fields.  One of those fields will be used to repres
 
 Add the following two fields to the `Snippet` model in `models.py`.
 
-    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
-    highlighted = models.TextField()
+```python
+owner = models.ForeignKey(
+    "auth.User", related_name="snippets", on_delete=models.CASCADE
+)
+highlighted = models.TextField()
+```
 
 We'd also need to make sure that when the model is saved, that we populate the highlighted field, using the `pygments` code highlighting library.
 
 We'll need some extra imports:
 
-    from pygments.lexers import get_lexer_by_name
-    from pygments.formatters.html import HtmlFormatter
-    from pygments import highlight
+```python
+from pygments.lexers import get_lexer_by_name
+from pygments.formatters.html import HtmlFormatter
+from pygments import highlight
+```
 
 And now we can add a `.save()` method to our model class:
 
-    def save(self, *args, **kwargs):
-        """
-        Use the `pygments` library to create a highlighted HTML
-        representation of the code snippet.
-        """
-        lexer = get_lexer_by_name(self.language)
-        linenos = 'table' if self.linenos else False
-        options = {'title': self.title} if self.title else {}
-        formatter = HtmlFormatter(style=self.style, linenos=linenos,
-                                  full=True, **options)
-        self.highlighted = highlight(self.code, lexer, formatter)
-        super().save(*args, **kwargs)
+```python
+def save(self, *args, **kwargs):
+    """
+    Use the `pygments` library to create a highlighted HTML
+    representation of the code snippet.
+    """
+    lexer = get_lexer_by_name(self.language)
+    linenos = "table" if self.linenos else False
+    options = {"title": self.title} if self.title else {}
+    formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
+    self.highlighted = highlight(self.code, lexer, formatter)
+    super().save(*args, **kwargs)
+```
 
 When that's all done we'll need to update our database tables.
 Normally we'd create a database migration in order to do that, but for the purposes of this tutorial, let's just delete the database and start again.
 
-    rm -f db.sqlite3
-    rm -r snippets/migrations
-    python manage.py makemigrations snippets
-    python manage.py migrate
+```bash
+rm -f db.sqlite3
+rm -r snippets/migrations
+python manage.py makemigrations snippets
+python manage.py migrate
+```
 
 You might also want to create a few different users, to use for testing the API.  The quickest way to do this will be with the `createsuperuser` command.
 
-    python manage.py createsuperuser
+```bash
+python manage.py createsuperuser
+```
 
 ## Adding endpoints for our User models
 
 Now that we've got some users to work with, we'd better add representations of those users to our API.  Creating a new serializer is easy. In `serializers.py` add:
 
-    from django.contrib.auth.models import User
+```python
+from django.contrib.auth.models import User
 
-    class UserSerializer(serializers.ModelSerializer):
-        snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
 
-        class Meta:
-            model = User
-            fields = ['id', 'username', 'snippets']
+class UserSerializer(serializers.ModelSerializer):
+    snippets = serializers.PrimaryKeyRelatedField(
+        many=True, queryset=Snippet.objects.all()
+    )
+
+    class Meta:
+        model = User
+        fields = ["id", "username", "snippets"]
+```
 
 Because `'snippets'` is a *reverse* relationship on the User model, it will not be included by default when using the `ModelSerializer` class, so we needed to add an explicit field for it.
 
 We'll also add a couple of views to `views.py`.  We'd like to just use read-only views for the user representations, so we'll use the `ListAPIView` and `RetrieveAPIView` generic class-based views.
 
-    from django.contrib.auth.models import User
+```python
+from django.contrib.auth.models import User
 
 
-    class UserList(generics.ListAPIView):
-        queryset = User.objects.all()
-        serializer_class = UserSerializer
+class UserList(generics.ListAPIView):
+    queryset = User.objects.all()
+    serializer_class = UserSerializer
 
 
-    class UserDetail(generics.RetrieveAPIView):
-        queryset = User.objects.all()
-        serializer_class = UserSerializer
+class UserDetail(generics.RetrieveAPIView):
+    queryset = User.objects.all()
+    serializer_class = UserSerializer
+```
 
 Make sure to also import the `UserSerializer` class
 
-    from snippets.serializers import UserSerializer
+```python
+from snippets.serializers import UserSerializer
+```
 
 Finally we need to add those views into the API, by referencing them from the URL conf. Add the following to the patterns in `snippets/urls.py`.
 
-    path('users/', views.UserList.as_view()),
-    path('users/<int:pk>/', views.UserDetail.as_view()),
+```python
+path("users/", views.UserList.as_view()),
+path("users/<int:pk>/", views.UserDetail.as_view()),
+```
 
 ## Associating Snippets with Users
 
@@ -98,8 +120,10 @@ The way we deal with that is by overriding a `.perform_create()` method on our s
 
 On the `SnippetList` view class, add the following method:
 
-    def perform_create(self, serializer):
-        serializer.save(owner=self.request.user)
+```python
+def perform_create(self, serializer):
+    serializer.save(owner=self.request.user)
+```
 
 The `create()` method of our serializer will now be passed an additional `'owner'` field, along with the validated data from the request.
 
@@ -107,7 +131,9 @@ The `create()` method of our serializer will now be passed an additional `'owner
 
 Now that snippets are associated with the user that created them, let's update our `SnippetSerializer` to reflect that.  Add the following field to the serializer definition in `serializers.py`:
 
-    owner = serializers.ReadOnlyField(source='owner.username')
+```python
+owner = serializers.ReadOnlyField(source="owner.username")
+```
 
 **Note**: Make sure you also add `'owner',` to the list of fields in the inner `Meta` class.
 
@@ -123,11 +149,15 @@ REST framework includes a number of permission classes that we can use to restri
 
 First add the following import in the views module
 
-    from rest_framework import permissions
+```python
+from rest_framework import permissions
+```
 
 Then, add the following property to **both** the `SnippetList` and `SnippetDetail` view classes.
 
-    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
+```python
+permission_classes = [permissions.IsAuthenticatedOrReadOnly]
+```
 
 ## Adding login to the Browsable API
 
@@ -137,13 +167,17 @@ We can add a login view for use with the browsable API, by editing the URLconf i
 
 Add the following import at the top of the file:
 
-    from django.urls import path, include
+```python
+from django.urls import path, include
+```
 
 And, at the end of the file, add a pattern to include the login and logout views for the browsable API.
 
-    urlpatterns += [
-        path('api-auth/', include('rest_framework.urls')),
-    ]
+```python
+urlpatterns += [
+    path("api-auth/", include("rest_framework.urls")),
+]
+```
 
 The `'api-auth/'` part of pattern can actually be whatever URL you want to use.
 
@@ -159,31 +193,36 @@ To do that we're going to need to create a custom permission.
 
 In the snippets app, create a new file, `permissions.py`
 
-    from rest_framework import permissions
+```python
+from rest_framework import permissions
 
 
-    class IsOwnerOrReadOnly(permissions.BasePermission):
-        """
-        Custom permission to only allow owners of an object to edit it.
-        """
+class IsOwnerOrReadOnly(permissions.BasePermission):
+    """
+    Custom permission to only allow owners of an object to edit it.
+    """
 
-        def has_object_permission(self, request, view, obj):
-            # Read permissions are allowed to any request,
-            # so we'll always allow GET, HEAD or OPTIONS requests.
-            if request.method in permissions.SAFE_METHODS:
-                return True
+    def has_object_permission(self, request, view, obj):
+        # Read permissions are allowed to any request,
+        # so we'll always allow GET, HEAD or OPTIONS requests.
+        if request.method in permissions.SAFE_METHODS:
+            return True
 
-            # Write permissions are only allowed to the owner of the snippet.
-            return obj.owner == request.user
+        # Write permissions are only allowed to the owner of the snippet.
+        return obj.owner == request.user
+```
 
 Now we can add that custom permission to our snippet instance endpoint, by editing the `permission_classes` property on the `SnippetDetail` view class:
 
-    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
-                          IsOwnerOrReadOnly]
+```python
+permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
+```
 
 Make sure to also import the `IsOwnerOrReadOnly` class.
 
-    from snippets.permissions import IsOwnerOrReadOnly
+```python
+from snippets.permissions import IsOwnerOrReadOnly
+```
 
 Now, if you open a browser again, you find that the 'DELETE' and 'PUT' actions only appear on a snippet instance endpoint if you're logged in as the same user that created the code snippet.
 
@@ -197,25 +236,29 @@ If we're interacting with the API programmatically we need to explicitly provide
 
 If we try to create a snippet without authenticating, we'll get an error:
 
-    http POST http://127.0.0.1:8000/snippets/ code="print(123)"
+```bash
+http POST http://127.0.0.1:8000/snippets/ code="print(123)"
 
-    {
-        "detail": "Authentication credentials were not provided."
-    }
+{
+    "detail": "Authentication credentials were not provided."
+}
+```
 
 We can make a successful request by including the username and password of one of the users we created earlier.
 
-    http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
-
-    {
-        "id": 1,
-        "owner": "admin",
-        "title": "foo",
-        "code": "print(789)",
-        "linenos": false,
-        "language": "python",
-        "style": "friendly"
-    }
+```bash
+http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
+
+{
+    "id": 1,
+    "owner": "admin",
+    "title": "foo",
+    "code": "print(789)",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+}
+```
 
 ## Summary
```



 - `.reference/tutorial/2-requests-and-responses.md`

```
041b88f8bbb48d9688ebd5add294eee2dfc93d1c -> c0f3649224117609d19e79c77242b525570d25c0
@@ -7,14 +7,18 @@ Let's introduce a couple of essential building blocks.
 
 REST framework introduces a `Request` object that extends the regular `HttpRequest`, and provides more flexible request parsing.  The core functionality of the `Request` object is the `request.data` attribute, which is similar to `request.POST`, but more useful for working with Web APIs.
 
-    request.POST  # Only handles form data.  Only works for 'POST' method.
-    request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
+```python
+request.POST  # Only handles form data.  Only works for 'POST' method.
+request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
+```
 
 ## Response objects
 
 REST framework also introduces a `Response` object, which is a type of `TemplateResponse` that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.
 
-    return Response(data)  # Renders to content type as requested by the client.
+```python
+return Response(data)  # Renders to content type as requested by the client.
+```
 
 ## Status codes
 
@@ -35,58 +39,62 @@ The wrappers also provide behavior such as returning `405 Method Not Allowed` re
 
 Okay, let's go ahead and start using these new components to refactor our views slightly.
 
-    from rest_framework import status
-    from rest_framework.decorators import api_view
-    from rest_framework.response import Response
-    from snippets.models import Snippet
-    from snippets.serializers import SnippetSerializer
-
-
-    @api_view(['GET', 'POST'])
-    def snippet_list(request):
-        """
-        List all code snippets, or create a new snippet.
-        """
-        if request.method == 'GET':
-            snippets = Snippet.objects.all()
-            serializer = SnippetSerializer(snippets, many=True)
-            return Response(serializer.data)
-
-        elif request.method == 'POST':
-            serializer = SnippetSerializer(data=request.data)
-            if serializer.is_valid():
-                serializer.save()
-                return Response(serializer.data, status=status.HTTP_201_CREATED)
-            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
+```python
+from rest_framework import status
+from rest_framework.decorators import api_view
+from rest_framework.response import Response
+from snippets.models import Snippet
+from snippets.serializers import SnippetSerializer
+
+
+@api_view(["GET", "POST"])
+def snippet_list(request):
+    """
+    List all code snippets, or create a new snippet.
+    """
+    if request.method == "GET":
+        snippets = Snippet.objects.all()
+        serializer = SnippetSerializer(snippets, many=True)
+        return Response(serializer.data)
+
+    elif request.method == "POST":
+        serializer = SnippetSerializer(data=request.data)
+        if serializer.is_valid():
+            serializer.save()
+            return Response(serializer.data, status=status.HTTP_201_CREATED)
+        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
+```
 
 Our instance view is an improvement over the previous example.  It's a little more concise, and the code now feels very similar to if we were working with the Forms API.  We're also using named status codes, which makes the response meanings more obvious.
 
 Here is the view for an individual snippet, in the `views.py` module.
 
-    @api_view(['GET', 'PUT', 'DELETE'])
-    def snippet_detail(request, pk):
-        """
-        Retrieve, update or delete a code snippet.
-        """
-        try:
-            snippet = Snippet.objects.get(pk=pk)
-        except Snippet.DoesNotExist:
-            return Response(status=status.HTTP_404_NOT_FOUND)
-
-        if request.method == 'GET':
-            serializer = SnippetSerializer(snippet)
+```python
+@api_view(["GET", "PUT", "DELETE"])
+def snippet_detail(request, pk):
+    """
+    Retrieve, update or delete a code snippet.
+    """
+    try:
+        snippet = Snippet.objects.get(pk=pk)
+    except Snippet.DoesNotExist:
+        return Response(status=status.HTTP_404_NOT_FOUND)
+
+    if request.method == "GET":
+        serializer = SnippetSerializer(snippet)
+        return Response(serializer.data)
+
+    elif request.method == "PUT":
+        serializer = SnippetSerializer(snippet, data=request.data)
+        if serializer.is_valid():
+            serializer.save()
             return Response(serializer.data)
+        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
-        elif request.method == 'PUT':
-            serializer = SnippetSerializer(snippet, data=request.data)
-            if serializer.is_valid():
-                serializer.save()
-                return Response(serializer.data)
-            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
-
-        elif request.method == 'DELETE':
-            snippet.delete()
-            return Response(status=status.HTTP_204_NO_CONTENT)
+    elif request.method == "DELETE":
+        snippet.delete()
+        return Response(status=status.HTTP_204_NO_CONTENT)
+```
 
 This should all feel very familiar - it is not a lot different from working with regular Django views.
 
@@ -94,28 +102,27 @@ Notice that we're no longer explicitly tying our requests or responses to a give
 
 ## Adding optional format suffixes to our URLs
 
-To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints.  Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as [http://example.com/api/items/4.json][json-url].
+To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints.  Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as [<http://example.com/api/items/4.json>][json-url].
 
 Start by adding a `format` keyword argument to both of the views, like so.
-
-    def snippet_list(request, format=None):
-
+`def snippet_list(request, format=None):`
 and
-
-    def snippet_detail(request, pk, format=None):
+`def snippet_detail(request, pk, format=None):`
 
 Now update the `snippets/urls.py` file slightly, to append a set of `format_suffix_patterns` in addition to the existing URLs.
 
-    from django.urls import path
-    from rest_framework.urlpatterns import format_suffix_patterns
-    from snippets import views
+```python
+from django.urls import path
+from rest_framework.urlpatterns import format_suffix_patterns
+from snippets import views
 
-    urlpatterns = [
-        path('snippets/', views.snippet_list),
-        path('snippets/<int:pk>/', views.snippet_detail),
-    ]
+urlpatterns = [
+    path("snippets/", views.snippet_list),
+    path("snippets/<int:pk>/", views.snippet_detail),
+]
 
-    urlpatterns = format_suffix_patterns(urlpatterns)
+urlpatterns = format_suffix_patterns(urlpatterns)
+```
 
 We don't necessarily need to add these extra url patterns in, but it gives us a simple, clean way of referring to a specific format.
 
@@ -125,68 +132,76 @@ Go ahead and test the API from the command line, as we did in [tutorial part 1][
 
 We can get a list of all of the snippets, as before.
 
-    http http://127.0.0.1:8000/snippets/
-
-    HTTP/1.1 200 OK
-    ...
-    [
-      {
-        "id": 1,
-        "title": "",
-        "code": "foo = \"bar\"\n",
-        "linenos": false,
-        "language": "python",
-        "style": "friendly"
-      },
-      {
-        "id": 2,
-        "title": "",
-        "code": "print(\"hello, world\")\n",
-        "linenos": false,
-        "language": "python",
-        "style": "friendly"
-      }
-    ]
+```bash
+http http://127.0.0.1:8000/snippets/
+
+HTTP/1.1 200 OK
+...
+[
+    {
+    "id": 1,
+    "title": "",
+    "code": "foo = \"bar\"\n",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+    },
+    {
+    "id": 2,
+    "title": "",
+    "code": "print(\"hello, world\")\n",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+    }
+]
+```
 
 We can control the format of the response that we get back, either by using the `Accept` header:
 
-    http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
-    http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
+```bash
+http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
+http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML
+```
 
 Or by appending a format suffix:
 
-    http http://127.0.0.1:8000/snippets.json  # JSON suffix
-    http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
+```bash
+http http://127.0.0.1:8000/snippets.json  # JSON suffix
+http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
+```
 
 Similarly, we can control the format of the request that we send, using the `Content-Type` header.
 
-    # POST using form data
-    http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"
-
-    {
-      "id": 3,
-      "title": "",
-      "code": "print(123)",
-      "linenos": false,
-      "language": "python",
-      "style": "friendly"
-    }
-
-    # POST using JSON
-    http --json POST http://127.0.0.1:8000/snippets/ code="print(456)"
-
-    {
-        "id": 4,
-        "title": "",
-        "code": "print(456)",
-        "linenos": false,
-        "language": "python",
-        "style": "friendly"
-    }
+```bash
+# POST using form data
+http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"
+
+{
+    "id": 3,
+    "title": "",
+    "code": "print(123)",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+}
+
+# POST using JSON
+http --json POST http://127.0.0.1:8000/snippets/ code="print(456)"
+
+{
+    "id": 4,
+    "title": "",
+    "code": "print(456)",
+    "linenos": false,
+    "language": "python",
+    "style": "friendly"
+}
+```
 
 If you add a `--debug` switch to the `http` requests above, you will be able to see the request type in request headers.
 
-Now go and open the API in a web browser, by visiting [http://127.0.0.1:8000/snippets/][devserver].
+Now go and open the API in a web browser, by visiting [<http://127.0.0.1:8000/snippets/>][devserver].
 
 ### Browsability
```



 - `.reference/tutorial/6-viewsets-and-routers.md`

```
4c231d5b97bcc1769ba5a6f41c16f011200300b8 -> c0f3649224117609d19e79c77242b525570d25c0
@@ -12,45 +12,50 @@ Let's take our current set of views, and refactor them into view sets.
 
 First of all let's refactor our `UserList` and `UserDetail` classes into a single `UserViewSet` class. In the `snippets/views.py` file, we can remove the two view classes and replace them with a single ViewSet class:
 
-    from rest_framework import viewsets
+```python
+from rest_framework import viewsets
 
 
-    class UserViewSet(viewsets.ReadOnlyModelViewSet):
-        """
-        This viewset automatically provides `list` and `retrieve` actions.
-        """
-        queryset = User.objects.all()
-        serializer_class = UserSerializer
+class UserViewSet(viewsets.ReadOnlyModelViewSet):
+    """
+    This viewset automatically provides `list` and `retrieve` actions.
+    """
+
+    queryset = User.objects.all()
+    serializer_class = UserSerializer
+```
 
 Here we've used the `ReadOnlyModelViewSet` class to automatically provide the default 'read-only' operations.  We're still setting the `queryset` and `serializer_class` attributes exactly as we did when we were using regular views, but we no longer need to provide the same information to two separate classes.
 
 Next we're going to replace the `SnippetList`, `SnippetDetail` and `SnippetHighlight` view classes.  We can remove the three views, and again replace them with a single class.
 
-    from rest_framework import permissions
-    from rest_framework import renderers
-    from rest_framework.decorators import action
-    from rest_framework.response import Response
+```python
+from rest_framework import permissions
+from rest_framework import renderers
+from rest_framework.decorators import action
+from rest_framework.response import Response
+
 
+class SnippetViewSet(viewsets.ModelViewSet):
+    """
+    This ViewSet automatically provides `list`, `create`, `retrieve`,
+    `update` and `destroy` actions.
 
-    class SnippetViewSet(viewsets.ModelViewSet):
-        """
-        This ViewSet automatically provides `list`, `create`, `retrieve`,
-        `update` and `destroy` actions.
+    Additionally we also provide an extra `highlight` action.
+    """
 
-        Additionally we also provide an extra `highlight` action.
-        """
-        queryset = Snippet.objects.all()
-        serializer_class = SnippetSerializer
-        permission_classes = [permissions.IsAuthenticatedOrReadOnly,
-                              IsOwnerOrReadOnly]
+    queryset = Snippet.objects.all()
+    serializer_class = SnippetSerializer
+    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
 
-        @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
-        def highlight(self, request, *args, **kwargs):
-            snippet = self.get_object()
-            return Response(snippet.highlighted)
+    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
+    def highlight(self, request, *args, **kwargs):
+        snippet = self.get_object()
+        return Response(snippet.highlighted)
 
-        def perform_create(self, serializer):
-            serializer.save(owner=self.request.user)
+    def perform_create(self, serializer):
+        serializer.save(owner=self.request.user)
+```
 
 This time we've used the `ModelViewSet` class in order to get the complete set of default read and write operations.
 
@@ -67,42 +72,40 @@ To see what's going on under the hood let's first explicitly create a set of vie
 
 In the `snippets/urls.py` file we bind our `ViewSet` classes into a set of concrete views.
 
-    from rest_framework import renderers
-
-    from snippets.views import api_root, SnippetViewSet, UserViewSet
-
-    snippet_list = SnippetViewSet.as_view({
-        'get': 'list',
-        'post': 'create'
-    })
-    snippet_detail = SnippetViewSet.as_view({
-        'get': 'retrieve',
-        'put': 'update',
-        'patch': 'partial_update',
-        'delete': 'destroy'
-    })
-    snippet_highlight = SnippetViewSet.as_view({
-        'get': 'highlight'
-    }, renderer_classes=[renderers.StaticHTMLRenderer])
-    user_list = UserViewSet.as_view({
-        'get': 'list'
-    })
-    user_detail = UserViewSet.as_view({
-        'get': 'retrieve'
-    })
+```python
+from rest_framework import renderers
+
+from snippets.views import api_root, SnippetViewSet, UserViewSet
+
+snippet_list = SnippetViewSet.as_view({"get": "list", "post": "create"})
+snippet_detail = SnippetViewSet.as_view(
+    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
+)
+snippet_highlight = SnippetViewSet.as_view(
+    {"get": "highlight"}, renderer_classes=[renderers.StaticHTMLRenderer]
+)
+user_list = UserViewSet.as_view({"get": "list"})
+user_detail = UserViewSet.as_view({"get": "retrieve"})
+```
 
 Notice how we're creating multiple views from each `ViewSet` class, by binding the HTTP methods to the required action for each view.
 
 Now that we've bound our resources into concrete views, we can register the views with the URL conf as usual.
 
-    urlpatterns = format_suffix_patterns([
-        path('', api_root),
-        path('snippets/', snippet_list, name='snippet-list'),
-        path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
-        path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
-        path('users/', user_list, name='user-list'),
-        path('users/<int:pk>/', user_detail, name='user-detail')
-    ])
+```python
+urlpatterns = format_suffix_patterns(
+    [
+        path("", api_root),
+        path("snippets/", snippet_list, name="snippet-list"),
+        path("snippets/<int:pk>/", snippet_detail, name="snippet-detail"),
+        path(
+            "snippets/<int:pk>/highlight/", snippet_highlight, name="snippet-highlight"
+        ),
+        path("users/", user_list, name="user-list"),
+        path("users/<int:pk>/", user_detail, name="user-detail"),
+    ]
+)
+```
 
 ## Using Routers
 
@@ -110,20 +113,22 @@ Because we're using `ViewSet` classes rather than `View` classes, we actually do
 
 Here's our re-wired `snippets/urls.py` file.
 
-    from django.urls import path, include
-    from rest_framework.routers import DefaultRouter
+```python
+from django.urls import path, include
+from rest_framework.routers import DefaultRouter
 
-    from snippets import views
+from snippets import views
 
-    # Create a router and register our ViewSets with it.
-    router = DefaultRouter()
-    router.register(r'snippets', views.SnippetViewSet, basename='snippet')
-    router.register(r'users', views.UserViewSet, basename='user')
+# Create a router and register our ViewSets with it.
+router = DefaultRouter()
+router.register(r"snippets", views.SnippetViewSet, basename="snippet")
+router.register(r"users", views.UserViewSet, basename="user")
 
-    # The API URLs are now determined automatically by the router.
-    urlpatterns = [
-        path('', include(router.urls)),
-    ]
+# The API URLs are now determined automatically by the router.
+urlpatterns = [
+    path("", include(router.urls)),
+]
+```
 
 Registering the ViewSets with the router is similar to providing a urlpattern.  We include two arguments - the URL prefix for the views, and the view set itself.
```



 - `.reference/tutorial/5-relationships-and-hyperlinked-apis.md`

```
2ae8c117dae5d7912760492a1df397e2fcd8c7a4 -> c0f3649224117609d19e79c77242b525570d25c0
@@ -6,17 +6,21 @@ At the moment relationships within our API are represented by using primary keys
 
 Right now we have endpoints for 'snippets' and 'users', but we don't have a single entry point to our API.  To create one, we'll use a regular function-based view and the `@api_view` decorator we introduced earlier. In your `snippets/views.py` add:
 
-    from rest_framework.decorators import api_view
-    from rest_framework.response import Response
-    from rest_framework.reverse import reverse
-
-
-    @api_view(['GET'])
-    def api_root(request, format=None):
-        return Response({
-            'users': reverse('user-list', request=request, format=format),
-            'snippets': reverse('snippet-list', request=request, format=format)
-        })
+```python
+from rest_framework.decorators import api_view
+from rest_framework.response import Response
+from rest_framework.reverse import reverse
+
+
+@api_view(["GET"])
+def api_root(request, format=None):
+    return Response(
+        {
+            "users": reverse("user-list", request=request, format=format),
+            "snippets": reverse("snippet-list", request=request, format=format),
+        }
+    )
+```
 
 Two things should be noticed here. First, we're using REST framework's `reverse` function in order to return fully-qualified URLs; second, URL patterns are identified by convenience names that we will declare later on in our `snippets/urls.py`.
 
@@ -30,24 +34,31 @@ The other thing we need to consider when creating the code highlight view is tha
 
 Instead of using a concrete generic view, we'll use the base class for representing instances, and create our own `.get()` method.  In your `snippets/views.py` add:
 
-    from rest_framework import renderers
+```python
+from rest_framework import renderers
 
-    class SnippetHighlight(generics.GenericAPIView):
-        queryset = Snippet.objects.all()
-        renderer_classes = [renderers.StaticHTMLRenderer]
 
-        def get(self, request, *args, **kwargs):
-            snippet = self.get_object()
-            return Response(snippet.highlighted)
+class SnippetHighlight(generics.GenericAPIView):
+    queryset = Snippet.objects.all()
+    renderer_classes = [renderers.StaticHTMLRenderer]
+
+    def get(self, request, *args, **kwargs):
+        snippet = self.get_object()
+        return Response(snippet.highlighted)
+```
 
 As usual we need to add the new views that we've created in to our URLconf.
 We'll add a url pattern for our new API root in `snippets/urls.py`:
 
-    path('', views.api_root),
+```python
+path("", views.api_root),
+```
 
 And then add a url pattern for the snippet highlights:
 
-    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
+```python
+path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view()),
+```
 
 ## Hyperlinking our API
 
@@ -73,22 +84,37 @@ The `HyperlinkedModelSerializer` has the following differences from `ModelSerial
 
 We can easily re-write our existing serializers to use hyperlinking. In your `snippets/serializers.py` add:
 
-    class SnippetSerializer(serializers.HyperlinkedModelSerializer):
-        owner = serializers.ReadOnlyField(source='owner.username')
-        highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
-
-        class Meta:
-            model = Snippet
-            fields = ['url', 'id', 'highlight', 'owner',
-                      'title', 'code', 'linenos', 'language', 'style']
-
-
-    class UserSerializer(serializers.HyperlinkedModelSerializer):
-        snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
-
-        class Meta:
-            model = User
-            fields = ['url', 'id', 'username', 'snippets']
+```python
+class SnippetSerializer(serializers.HyperlinkedModelSerializer):
+    owner = serializers.ReadOnlyField(source="owner.username")
+    highlight = serializers.HyperlinkedIdentityField(
+        view_name="snippet-highlight", format="html"
+    )
+
+    class Meta:
+        model = Snippet
+        fields = [
+            "url",
+            "id",
+            "highlight",
+            "owner",
+            "title",
+            "code",
+            "linenos",
+            "language",
+            "style",
+        ]
+
+
+class UserSerializer(serializers.HyperlinkedModelSerializer):
+    snippets = serializers.HyperlinkedRelatedField(
+        many=True, view_name="snippet-detail", read_only=True
+    )
+
+    class Meta:
+        model = User
+        fields = ["url", "id", "username", "snippets"]
+```
 
 Notice that we've also added a new `'highlight'` field.  This field is of the same type as the `url` field, except that it points to the `'snippet-highlight'` url pattern, instead of the `'snippet-detail'` url pattern.
 
@@ -100,11 +126,15 @@ Because we've included format suffixed URLs such as `'.json'`, we also need to i
 
 When you are manually instantiating these serializers inside your views (e.g., in `SnippetDetail` or `SnippetList`), you **must** pass `context={'request': request}` so the serializer knows how to build absolute URLs. For example, instead of:
 
-    serializer = SnippetSerializer(snippet)
+```python
+serializer = SnippetSerializer(snippet)
+```
 
 You must write:
 
-    serializer = SnippetSerializer(snippet, context={'request': request})
+```python
+serializer = SnippetSerializer(snippet, context={"request": request})
+```
 
 If your view is a subclass of `GenericAPIView`, you may use the `get_serializer_context()` as a convenience method.
 
@@ -121,29 +151,29 @@ If we're going to have a hyperlinked API, we need to make sure we name our URL p
 
 After adding all those names into our URLconf, our final `snippets/urls.py` file should look like this:
 
-    from django.urls import path
-    from rest_framework.urlpatterns import format_suffix_patterns
-    from snippets import views
-
-    # API endpoints
-    urlpatterns = format_suffix_patterns([
-        path('', views.api_root),
-        path('snippets/',
-            views.SnippetList.as_view(),
-            name='snippet-list'),
-        path('snippets/<int:pk>/',
-            views.SnippetDetail.as_view(),
-            name='snippet-detail'),
-        path('snippets/<int:pk>/highlight/',
+```python
+from django.urls import path
+from rest_framework.urlpatterns import format_suffix_patterns
+from snippets import views
+
+# API endpoints
+urlpatterns = format_suffix_patterns(
+    [
+        path("", views.api_root),
+        path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
+        path(
+            "snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"
+        ),
+        path(
+            "snippets/<int:pk>/highlight/",
             views.SnippetHighlight.as_view(),
-            name='snippet-highlight'),
-        path('users/',
-            views.UserList.as_view(),
-            name='user-list'),
-        path('users/<int:pk>/',
-            views.UserDetail.as_view(),
-            name='user-detail')
-    ])
+            name="snippet-highlight",
+        ),
+        path("users/", views.UserList.as_view(), name="user-list"),
+        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
+    ]
+)
+```
 
 ## Adding pagination
 
@@ -151,10 +181,12 @@ The list views for users and code snippets could end up returning quite a lot of
 
 We can change the default list style to use pagination, by modifying our `tutorial/settings.py` file slightly. Add the following setting:
 
-    REST_FRAMEWORK = {
-        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
-        'PAGE_SIZE': 10
-    }
+```python
+REST_FRAMEWORK = {
+    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
+    "PAGE_SIZE": 10,
+}
+```
 
 Note that settings in REST framework are all namespaced into a single dictionary setting, named `REST_FRAMEWORK`, which helps keep them well separated from your other project settings.
```



 - `.reference/topics/internationalization.md`

```
9921c7554f3d8ce435e45bafd27f4b241beb66f1 -> 2ca3b7f9c449145156f0b0e2d9ea58a2295f8fbf
@@ -60,11 +60,12 @@ If you only wish to support a subset of the available languages, use Django's st
 
 ## Adding new translations
 
-REST framework translations are managed online using [Transifex][transifex-project]. You can use the Transifex service to add new translation languages. The maintenance team will then ensure that these translation strings are included in the REST framework package.
+REST framework translations are managed on GitHub. You can contribute new translation languages or update existing ones
+by following the guidelines in the [Contributing to REST Framework] section and submitting a pull request.
 
 Sometimes you may need to add translation strings to your project locally. You may need to do this if:
 
-* You want to use REST Framework in a language which has not been translated yet on Transifex.
+* You want to use REST Framework in a language which is not supported by the project.
 * Your project includes custom error messages, which are not part of REST framework's default translation strings.
 
 #### Translating a new language locally
@@ -103,10 +104,10 @@ You can find more information on how the language preference is determined in th
 For API clients the most appropriate of these will typically be to use the `Accept-Language` header; Sessions and cookies will not be available unless using session authentication, and generally better practice to prefer an `Accept-Language` header for API clients rather than using language URL prefixes.
 
 [cite]: https://youtu.be/Wa0VfS2q94Y
+[Contributing to REST Framework]: ../community/contributing.md#development
 [django-translation]: https://docs.djangoproject.com/en/stable/topics/i18n/translation
 [custom-exception-handler]: ../api-guide/exceptions.md#custom-exception-handling
-[transifex-project]: https://explore.transifex.com/django-rest-framework-1/django-rest-framework/
-[django-po-source]: https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_US/LC_MESSAGES/django.po
+[django-po-source]: https://raw.githubusercontent.com/encode/django-rest-framework/main/rest_framework/locale/en_US/LC_MESSAGES/django.po
 [django-language-preference]: https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference
 [django-locale-paths]: https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-LOCALE_PATHS
 [django-locale-name]: https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name
```



 - `.reference/topics/rest-hypermedia-hateoas.md`

```
e354331743dd6e8999371b0055d61967c78da859 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -32,7 +32,7 @@ REST framework also includes [serialization] and [parser]/[renderer] components
 
 ## What REST framework doesn't provide.
 
-What REST framework doesn't do is give you machine readable hypermedia formats such as [HAL][hal], [Collection+JSON][collection], [JSON API][json-api] or HTML [microformats] by default, or the ability to auto-magically create fully HATEOAS style APIs that include hypermedia-based form descriptions and semantically labelled hyperlinks. Doing so would involve making opinionated choices about API design that should really remain outside of the framework's scope.
+What REST framework doesn't do is give you machine readable hypermedia formats such as [HAL][hal], [Collection+JSON][collection], [JSON API][json-api] or HTML [microformats] by default, or the ability to auto-magically create fully HATEOAS style APIs that include hypermedia-based form descriptions and semantically labeled hyperlinks. Doing so would involve making opinionated choices about API design that should really remain outside of the framework's scope.
 
 [cite]: https://vimeo.com/channels/restfest/49503453
 [dissertation]: https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
```



 - `.reference/topics/browsable-api.md`

```
2fbfaae5078caed98c1447cd2b8f7a3ebf210f68 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -181,7 +181,7 @@ The context that's available to the template:
 * `FORMAT_PARAM`        : The view can accept a format override
 * `METHOD_PARAM`        : The view can accept a method override
 
-You can override the `BrowsableAPIRenderer.get_context()` method to customise the context that gets passed to the template.
+You can override the `BrowsableAPIRenderer.get_context()` method to customize the context that gets passed to the template.
 
 #### Not using base.html
```



 - `.reference/README.md`

```
e96b8e49cd0a3392cfc67615d91b4914c2f65599 -> ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3
@@ -53,7 +53,7 @@ Some reasons you might want to use REST framework:
 * [Serialization][serializers] that supports both [ORM][modelserializer-section] and [non-ORM][serializer-section] data sources.
 * Customizable all the way down - just use [regular function-based views][functionview-section] if you don't need the [more][generic-views] [powerful][viewsets] [features][routers].
 * Extensive documentation, and [great community support][group].
-* Used and trusted by internationally recognised companies including [Mozilla][mozilla], [Red Hat][redhat], [Heroku][heroku], and [Eventbrite][eventbrite].
+* Used and trusted by internationally recognized companies including [Mozilla][mozilla], [Red Hat][redhat], [Heroku][heroku], and [Eventbrite][eventbrite].
 
 ---
 
@@ -88,7 +88,7 @@ continued development by **[signing up for a paid plan][funding]**.
 REST framework requires the following:
 
 * Django (4.2, 5.0, 5.1, 5.2)
-* Python (3.9, 3.10, 3.11, 3.12, 3.13)
+* Python (3.10, 3.11, 3.12, 3.13, 3.14)
 
 We **highly recommend** and only officially support the latest patch release of
 each Python and Django series.
```


