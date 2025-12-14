Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)

 - `.reference/api-guide/testing.md`

```
365d409adb43ebad7d8a42cab2407ec841d8038e -> e221d9a1d6638b936707efc390adff59511a6605
@@ -90,36 +90,32 @@ For example, when forcibly authenticating using a token, you might do something
     request = factory.get('/accounts/django-superstars/')
     force_authenticate(request, user=user, token=user.auth_token)
 
----
-
-**Note**: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are reusing the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`][refresh_from_db_docs] between tests.
-
----
-
-**Note**: When using `APIRequestFactory`, the object that is returned is Django's standard `HttpRequest`, and not REST framework's `Request` object, which is only generated once the view is called.
-
-This means that setting attributes directly on the request object may not always have the effect you expect.  For example, setting `.token` directly will have no effect, and setting `.user` directly will only work if session authentication is being used.
-
-    # Request will only authenticate if `SessionAuthentication` is in use.
-    request = factory.get('/accounts/django-superstars/')
-    request.user = user
-    response = view(request)
-
-If you want to test a request involving the REST framework’s 'Request' object, you’ll need to manually transform it first:
-
-    class DummyView(APIView):
-        ...
+!!! note
+    `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are reusing the same `user` instance across multiple tests that update the saved `user` state, you may need to call [`refresh_from_db()`][refresh_from_db_docs] between tests.
 
-    factory = APIRequestFactory()
-    request = factory.get('/', {'demo': 'test'})
-    drf_request = DummyView().initialize_request(request)
-    assert drf_request.query_params == {'demo': ['test']}
-
-    request = factory.post('/', {'example': 'test'})
-    drf_request = DummyView().initialize_request(request)
-    assert drf_request.data.get('example') == 'test'
+!!! note
+    When using `APIRequestFactory`, the object that is returned is Django's standard `HttpRequest`, and not REST framework's `Request` object, which is only generated once the view is called.
 
----
+    This means that setting attributes directly on the request object may not always have the effect you expect.  For example, setting `.token` directly will have no effect, and setting `.user` directly will only work if session authentication is being used.
+    
+        # Request will only authenticate if `SessionAuthentication` is in use.
+        request = factory.get('/accounts/django-superstars/')
+        request.user = user
+        response = view(request)
+    
+    If you want to test a request involving the REST framework’s 'Request' object, you’ll need to manually transform it first:
+    
+        class DummyView(APIView):
+            ...
+    
+        factory = APIRequestFactory()
+        request = factory.get('/', {'demo': 'test'})
+        drf_request = DummyView().initialize_request(request)
+        assert drf_request.query_params == {'demo': ['test']}
+    
+        request = factory.post('/', {'example': 'test'})
+        drf_request = DummyView().initialize_request(request)
+        assert drf_request.data.get('example') == 'test'
 
 ## Forcing CSRF validation
 
@@ -127,11 +123,8 @@ By default, requests created with `APIRequestFactory` will not have CSRF validat
 
     factory = APIRequestFactory(enforce_csrf_checks=True)
 
----
-
-**Note**: It's worth noting that Django's standard `RequestFactory` doesn't need to include this option, because when using regular Django the CSRF validation takes place in middleware, which is not run when testing views directly.  When using REST framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.
-
----
+!!! note
+    It's worth noting that Django's standard `RequestFactory` doesn't need to include this option, because when using regular Django the CSRF validation takes place in middleware, which is not run when testing views directly.  When using REST framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.
 
 # APIClient
```



 - `.reference/api-guide/generic-views.md`

```
653343cf32334a3d6e92872c0a7decdc7d8e9085 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -96,11 +96,8 @@ For example:
         user = self.request.user
         return user.accounts.all()
 
----
-
-**Note:** If the `serializer_class` used in the generic view spans orm relations, leading to an n+1 problem, you could optimize your queryset in this method using `select_related` and `prefetch_related`. To get more information about n+1 problem and use cases of the mentioned methods refer to related section in [django documentation][django-docs-select-related].
-
----
+!!! tip
+    If the `serializer_class` used in the generic view spans ORM relations, leading to an N+1 problem, you could optimize your queryset in this method using `select_related` and `prefetch_related`. To get more information about N+1 problem and use cases of the mentioned methods refer to related section in [django documentation][django-docs-select-related].
 
 ### Avoiding N+1 Queries
```



 - `.reference/api-guide/parsers.md`

```
c9e7b68a4c1db1ac60e962053380acda549609f3 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -17,15 +17,12 @@ REST framework includes a number of built-in Parser classes, that allow you to a
 
 The set of valid parsers for a view is always defined as a list of classes.  When `request.data` is accessed, REST framework will examine the `Content-Type` header on the incoming request, and determine which parser to use to parse the request content.
 
----
-
-**Note**: When developing client applications always remember to make sure you're setting the `Content-Type` header when sending data in an HTTP request.
+!!! note
+    When developing client applications always remember to make sure you're setting the `Content-Type` header when sending data in an HTTP request.
 
-If you don't set the content type, most clients will default to using `'application/x-www-form-urlencoded'`, which may not be what you wanted.
+    If you don't set the content type, most clients will default to using `'application/x-www-form-urlencoded'`, which may not be what you want.
 
-As an example, if you are sending `json` encoded data using jQuery with the [.ajax() method][jquery-ajax], you should make sure to include the `contentType: 'application/json'` setting.
-
----
+    As an example, if you are sending `json` encoded data using jQuery with the [.ajax() method][jquery-ajax], you should make sure to include the `contentType: 'application/json'` setting.
 
 ## Setting the parsers
```



 - `.reference/api-guide/caching.md`

```
c0202a0aa5cbaf8573458b932878dfd5044c93ab -> e221d9a1d6638b936707efc390adff59511a6605
@@ -82,8 +82,8 @@ def get_user_list(request):
 ```
 
 
-**NOTE:** The [`cache_page`][page] decorator only caches the
-`GET` and `HEAD` responses with status 200.
+!!! note
+    The [`cache_page`][page] decorator only caches the `GET` and `HEAD` responses with status 200.
 
 [page]: https://docs.djangoproject.com/en/stable/topics/cache/#the-per-view-cache
 [cookie]: https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.vary.vary_on_cookie
```



 - `.reference/api-guide/serializers.md`

```
40172399afcc60510a78bdae39818ee6686b72e4 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -192,11 +192,8 @@ Your `validate_<field_name>` methods should return the validated value or raise
                 raise serializers.ValidationError("Blog post is not about Django")
             return value
 
----
-
-**Note:** If your `<field_name>` is declared on your serializer with the parameter `required=False` then this validation step will not take place if the field is not included.
-
----
+!!! note
+    If your `<field_name>` is declared on your serializer with the parameter `required=False` then this validation step will not take place if the field is not included.
 
 #### Object-level validation
 
@@ -542,20 +539,16 @@ This option should be a list or tuple of field names, and is declared as follows
 
 Model fields which have `editable=False` set, and `AutoField` fields will be set to read-only by default, and do not need to be added to the `read_only_fields` option.
 
----
+!!! note
+    There is a special-case where a read-only field is part of a `unique_together` constraint at the model level. In this case the field is required by the serializer class in order to validate the constraint, but should also not be editable by the user.
 
-**Note**: There is a special-case where a read-only field is part of a `unique_together` constraint at the model level. In this case the field is required by the serializer class in order to validate the constraint, but should also not be editable by the user.
+    The right way to deal with this is to specify the field explicitly on the serializer, providing both the `read_only=True` and `default=…` keyword arguments.
 
-The right way to deal with this is to specify the field explicitly on the serializer, providing both the `read_only=True` and `default=…` keyword arguments.
+    One example of this is a read-only relation to the currently authenticated `User` which is `unique_together` with another identifier. In this case you would declare the user field like so:
 
-One example of this is a read-only relation to the currently authenticated `User` which is `unique_together` with another identifier. In this case you would declare the user field like so:
-
-    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
-
-Please review the [Validators Documentation](/api-guide/validators/) for details on the [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) and [CurrentUserDefault](/api-guide/validators/#currentuserdefault) classes.
-
----
+        user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
 
+    Please review the [Validators Documentation](/api-guide/validators/) for details on the [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) and [CurrentUserDefault](/api-guide/validators/#currentuserdefault) classes.
 
 ## Additional keyword arguments
```



 - `.reference/api-guide/relations.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -11,42 +11,36 @@ source:
 
 Relational fields are used to represent model relationships.  They can be applied to `ForeignKey`, `ManyToManyField` and `OneToOneField` relationships, as well as to reverse relationships, and custom relationships such as `GenericForeignKey`.
 
----
-
-**Note:** The relational fields are declared in `relations.py`, but by convention you should import them from the `serializers` module, using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.
-
----
-
----
-
-**Note:** REST Framework does not attempt to automatically optimize querysets passed to serializers in terms of `select_related` and `prefetch_related` since it would be too much magic. A serializer with a field spanning an orm relation through its source attribute could require an additional database hit to fetch related objects from the database. It is the programmer's responsibility to optimize queries to avoid additional database hits which could occur while using such a serializer.
-
-For example, the following serializer would lead to a database hit each time evaluating the tracks field if it is not prefetched:
-
-    class AlbumSerializer(serializers.ModelSerializer):
-        tracks = serializers.SlugRelatedField(
-            many=True,
-            read_only=True,
-            slug_field='title'
-        )
-
-        class Meta:
-            model = Album
-            fields = ['album_name', 'artist', 'tracks']
-
-    # For each album object, tracks should be fetched from database
-    qs = Album.objects.all()
-    print(AlbumSerializer(qs, many=True).data)
-
-If `AlbumSerializer` is used to serialize a fairly large queryset with `many=True` then it could be a serious performance problem. Optimizing the queryset passed to `AlbumSerializer` with:
-
-    qs = Album.objects.prefetch_related('tracks')
-    # No additional database hits required
-    print(AlbumSerializer(qs, many=True).data)
-
-would solve the issue.
-
----
+!!! note
+    The relational fields are declared in `relations.py`, but by convention you should import them from the `serializers` module, using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.
+
+!!! note
+    REST Framework does not attempt to automatically optimize querysets passed to serializers in terms of `select_related` and `prefetch_related` since it would be too much magic. A serializer with a field spanning an ORM relation through its source attribute could require an additional database hit to fetch related objects from the database. It is the programmer's responsibility to optimize queries to avoid additional database hits which could occur while using such a serializer.
+
+    For example, the following serializer would lead to a database hit each time evaluating the tracks field if it is not prefetched:
+    
+        class AlbumSerializer(serializers.ModelSerializer):
+            tracks = serializers.SlugRelatedField(
+                many=True,
+                read_only=True,
+                slug_field='title'
+            )
+    
+            class Meta:
+                model = Album
+                fields = ['album_name', 'artist', 'tracks']
+    
+        # For each album object, tracks should be fetched from database
+        qs = Album.objects.all()
+        print(AlbumSerializer(qs, many=True).data)
+    
+    If `AlbumSerializer` is used to serialize a fairly large queryset with `many=True` then it could be a serious performance problem. Optimizing the queryset passed to `AlbumSerializer` with:
+    
+        qs = Album.objects.prefetch_related('tracks')
+        # No additional database hits required
+        print(AlbumSerializer(qs, many=True).data)
+    
+    would solve the issue.
 
 #### Inspecting relationships.
 
@@ -183,15 +177,12 @@ Would serialize to a representation like this:
 
 By default this field is read-write, although you can change this behavior using the `read_only` flag.
 
----
+!!! note
+    This field is designed for objects that map to a URL that accepts a single URL keyword argument, as set using the `lookup_field` and `lookup_url_kwarg` arguments.
 
-**Note**: This field is designed for objects that map to a URL that accepts a single URL keyword argument, as set using the `lookup_field` and `lookup_url_kwarg` arguments.
+    This is suitable for URLs that contain a single primary key or slug argument as part of the URL.
 
-This is suitable for URLs that contain a single primary key or slug argument as part of the URL.
-
-If you require more complex hyperlinked representation you'll need to customize the field, as described in the [custom hyperlinked fields](#custom-hyperlinked-fields) section, below.
-
----
+    If you require more complex hyperlinked representation you'll need to customize the field, as described in the [custom hyperlinked fields](#custom-hyperlinked-fields) section, below.
 
 **Arguments**:
```



 - `.reference/api-guide/renderers.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -103,15 +103,10 @@ Unlike other renderers, the data passed to the `Response` does not need to be se
 
 The TemplateHTMLRenderer will create a `RequestContext`, using the `response.data` as the context dict, and determine a template name to use to render the context.
 
----
-
-**Note:** When used with a view that makes use of a serializer the `Response` sent for rendering may not be a dictionary and will need to be wrapped in a dict before returning to allow the `TemplateHTMLRenderer` to render it. For example:
+!!! note
+    When used with a view that makes use of a serializer the `Response` sent for rendering may not be a dictionary and will need to be wrapped in a dict before returning to allow the `TemplateHTMLRenderer` to render it. For example:
 
-```
-response.data = {'results': response.data}
-```
-
----
+        response.data = {'results': response.data}
 
 The template name is determined by (in order of preference):
 
@@ -202,13 +197,16 @@ This renderer is suitable for CRUD-style web APIs that should also present a use
 
 Note that views that have nested or list serializers for their input won't work well with the `AdminRenderer`, as the HTML forms are unable to properly support them.
 
-**Note**: The `AdminRenderer` is only able to include links to detail pages when a properly configured `URL_FIELD_NAME` (`url` by default) attribute is present in the data. For `HyperlinkedModelSerializer` this will be the case, but for `ModelSerializer` or plain `Serializer` classes you'll need to make sure to include the field explicitly. For example here we use models `get_absolute_url` method:
+!!! note
+    The `AdminRenderer` is only able to include links to detail pages when a properly configured `URL_FIELD_NAME` (`url` by default) attribute is present in the data. For `HyperlinkedModelSerializer` this will be the case, but for `ModelSerializer` or plain `Serializer` classes you'll need to make sure to include the field explicitly. 
 
-    class AccountSerializer(serializers.ModelSerializer):
-        url = serializers.CharField(source='get_absolute_url', read_only=True)
+    For example here we use models `get_absolute_url` method:
 
-        class Meta:
-            model = Account
+        class AccountSerializer(serializers.ModelSerializer):
+            url = serializers.CharField(source='get_absolute_url', read_only=True)
+    
+            class Meta:
+                model = Account
 
 
 **.media_type**: `text/html`
@@ -390,9 +388,8 @@ Exceptions raised and handled by an HTML renderer will attempt to render using o
 
 Templates will render with a `RequestContext` which includes the `status_code` and `details` keys.
 
-**Note**: If `DEBUG=True`, Django's standard traceback error page will be displayed instead of rendering the HTTP status code and text.
-
----
+!!! note
+    If `DEBUG=True`, Django's standard traceback error page will be displayed instead of rendering the HTTP status code and text.
 
 # Third party packages
 
@@ -444,13 +441,10 @@ Modify your REST framework settings.
 
 [REST framework JSONP][rest-framework-jsonp] provides JSONP rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
----
-
-**Warning**: If you require cross-domain AJAX requests, you should generally be using the more modern approach of [CORS][cors] as an alternative to `JSONP`. See the [CORS documentation][cors-docs] for more details.
+!!! warning
+    If you require cross-domain AJAX requests, you should generally be using the more modern approach of [CORS][cors] as an alternative to `JSONP`. See the [CORS documentation][cors-docs] for more details.
 
-The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally readable API endpoints][jsonp-security], where `GET` requests are unauthenticated and do not require any user permissions.
-
----
+    The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally readable API endpoints][jsonp-security], where `GET` requests are unauthenticated and do not require any user permissions.
 
 #### Installation & configuration
```



 - `.reference/api-guide/validators.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -101,11 +101,8 @@ The validator should be applied to *serializer classes*, like so:
                 )
             ]
 
----
-
-**Note**: The `UniqueTogetherValidator` class always imposes an implicit constraint that all the fields it applies to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.
-
----
+!!! note
+    The `UniqueTogetherValidator` class always imposes an implicit constraint that all the fields it applies to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.
 
 ## UniqueForDateValidator
 
@@ -158,24 +155,19 @@ If you want the date field to be entirely hidden from the user, then use `Hidden
 
     published = serializers.HiddenField(default=timezone.now)
 
----
-
-**Note**: The `UniqueFor<Range>Validator` classes impose an implicit constraint that the fields they are applied to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.
+!!! note
+    The `UniqueFor<Range>Validator` classes impose an implicit constraint that the fields they are applied to are always treated as required. Fields with `default` values are an exception to this as they always supply a value even when omitted from user input.
 
----
-
----
-
-**Note:** `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request). 
-
----
+!!! note
+    `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request). 
 
 # Advanced field defaults
 
 Validators that are applied across multiple fields in the serializer can sometimes require a field input that should not be provided by the API client, but that *is* available as input to the validator.
 For this purposes use `HiddenField`. This field will be present in `validated_data` but *will not* be used in the serializer output representation.
 
-**Note:** Using a `read_only=True` field is excluded from writable fields so it won't use a `default=…` argument. Look [3.8 announcement](https://www.django-rest-framework.org/community/3.8-announcement/#altered-the-behavior-of-read_only-plus-default-on-field).
+!!! note
+    Using a `read_only=True` field is excluded from writable fields so it won't use a `default=…` argument. Look [3.8 announcement](https://www.django-rest-framework.org/community/3.8-announcement/#altered-the-behavior-of-read_only-plus-default-on-field).
 
 REST framework includes a couple of defaults that may be useful in this context.
```



 - `.reference/api-guide/authentication.md`

```
442444f0bedc55af7ea1fcdc5755a343de1b1c57 -> d0a5d5e7cad7f1032b4d0a36cab1596076f705ad
@@ -19,13 +19,10 @@ The `request.user` property will typically be set to an instance of the `contrib
 
 The `request.auth` property is used for any additional authentication information, for example, it may be used to represent an authentication token that the request was signed with.
 
----
-
-**Note:** Don't forget that **authentication by itself won't allow or disallow an incoming request**, it simply identifies the credentials that the request was made with.
+!!! note
+    Don't forget that **authentication by itself won't allow or disallow an incoming request**, it simply identifies the credentials that the request was made with.
 
-For information on how to set up the permission policies for your API please see the [permissions documentation][permission].
-
----
+    For information on how to set up the permission policies for your API please see the [permissions documentation][permission].
 
 ## How authentication is determined
 
@@ -122,17 +119,15 @@ Unauthenticated responses that are denied permission will result in an `HTTP 401
 
     WWW-Authenticate: Basic realm="api"
 
-**Note:** If you use `BasicAuthentication` in production you must ensure that your API is only available over `https`.  You should also ensure that your API clients will always re-request the username and password at login, and will never store those details to persistent storage.
+!!! note
+    If you use `BasicAuthentication` in production you must ensure that your API is only available over `https`.  You should also ensure that your API clients will always re-request the username and password at login, and will never store those details to persistent storage.
 
 ## TokenAuthentication
 
----
-
-**Note:** The token authentication provided by Django REST framework is a fairly simple implementation.
+!!! note
+    The token authentication provided by Django REST framework is a fairly simple implementation.
 
-For an implementation which allows more than one token per user, has some tighter security implementation details, and supports token expiry, please see the [Django REST Knox][django-rest-knox] third party package.
-
----
+    For an implementation which allows more than one token per user, has some tighter security implementation details, and supports token expiry, please see the [Django REST Knox][django-rest-knox] third party package.
 
 This authentication scheme uses a simple token-based HTTP Authentication scheme.  Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.
 
@@ -173,11 +168,8 @@ The `curl` command line tool may be useful for testing token authenticated APIs.
 
     curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
 
----
-
-**Note:** If you use `TokenAuthentication` in production you must ensure that your API is only available over `https`.
-
----
+!!! note
+    If you use `TokenAuthentication` in production you must ensure that your API is only available over `https`.
 
 ### Generating Tokens
 
@@ -293,7 +285,8 @@ Unauthenticated responses that are denied permission will result in an `HTTP 403
 
 If you're using an AJAX-style API with SessionAuthentication, you'll need to make sure you include a valid CSRF token for any "unsafe" HTTP method calls, such as `PUT`, `PATCH`, `POST` or `DELETE` requests.  See the [Django CSRF documentation][csrf-ajax] for more details.
 
-**Warning**: Always use Django's standard login view when creating login pages. This will ensure your login views are properly protected.
+!!! warning
+    Always use Django's standard login view when creating login pages. This will ensure your login views are properly protected.
 
 CSRF validation in REST framework works slightly differently from standard Django due to the need to support both session and non-session based authentication to the same views. This means that only authenticated requests require CSRF tokens, and anonymous requests may be sent without CSRF tokens. This behavior is not suitable for login views, which should always have CSRF validation applied.
 
@@ -334,11 +327,8 @@ You *may* also override the `.authenticate_header(self, request)` method.  If im
 
 If the `.authenticate_header()` method is not overridden, the authentication scheme will return `HTTP 403 Forbidden` responses when an unauthenticated request is denied access.
 
----
-
-**Note:** When your custom authenticator is invoked by the request object's `.user` or `.auth` properties, you may see an `AttributeError` re-raised as a `WrappedAttributeError`. This is necessary to prevent the original exception from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from your custom authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. These errors should be fixed or otherwise handled by your authenticator.
-
----
+!!! note
+    When your custom authenticator is invoked by the request object's `.user` or `.auth` properties, you may see an `AttributeError` re-raised as a `WrappedAttributeError`. This is necessary to prevent the original exception from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from your custom authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. These errors should be fixed or otherwise handled by your authenticator.
 
 ## Example
 
@@ -461,7 +451,7 @@ More information can be found in the [Documentation](https://django-rest-durin.r
 
 ## django-pyoidc
 
-[dango-pyoidc][django_pyoidc] adds support for OpenID Connect (OIDC) authentication. This allows you to delegate user management to an Identity Provider, which can be used to implement Single-Sign-On (SSO). It provides support for most uses-cases, such as customizing how token info are mapped to user models, using OIDC audiences for access control, etc.
+[django_pyoidc][django-pyoidc] adds support for OpenID Connect (OIDC) authentication. This allows you to delegate user management to an Identity Provider, which can be used to implement Single-Sign-On (SSO). It provides support for most uses-cases, such as customizing how token info are mapped to user models, using OIDC audiences for access control, etc.
 
 More information can be found in the [Documentation](https://django-pyoidc.readthedocs.io/latest/index.html).
```



 - `.reference/api-guide/throttling.md`

```
64c3d9ef63bc073d01063934ab952cd1b990ecf2 -> d0a5d5e7cad7f1032b4d0a36cab1596076f705ad
@@ -19,9 +19,9 @@ Multiple throttles can also be used if you want to impose both burst throttling
 
 Throttles do not necessarily only refer to rate-limiting requests.  For example a storage service might also need to throttle against bandwidth, and a paid data service might want to throttle against a certain number of a records being accessed.
 
-**The application-level throttling that REST framework provides should not be considered a security measure or protection against brute forcing or denial-of-service attacks. Deliberately malicious actors will always be able to spoof IP origins. In addition to this, the built-in throttling implementations are implemented using Django's cache framework, and use non-atomic operations to determine the request rate, which may sometimes result in some fuzziness.
+**The application-level throttling that REST framework provides should not be considered a security measure or protection against brute forcing or denial-of-service attacks. Deliberately malicious actors will always be able to spoof IP origins. In addition to this, the built-in throttling implementations are implemented using Django's cache framework, and use non-atomic operations to determine the request rate, which may sometimes result in some fuzziness.**
 
-The application-level throttling provided by REST framework is intended for implementing policies such as different business tiers and basic protections against service over-use.**
+**The application-level throttling provided by REST framework is intended for implementing policies such as different business tiers and basic protections against service over-use.**
 
 ## How throttling is determined
```



 - `.reference/api-guide/schemas.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -238,15 +238,12 @@ operation = auto_schema.get_operation(...)
 In compiling the schema, `SchemaGenerator` calls `get_components()` and
 `get_operation()` for each view, allowed method, and path.
 
-----
-
-**Note**: The automatic introspection of components, and many operation
-parameters relies on the relevant attributes and methods of
-`GenericAPIView`: `get_serializer()`, `pagination_class`, `filter_backends`,
-etc. For basic `APIView` subclasses, default introspection is essentially limited to
-the URL kwarg path parameters for this reason.
-
-----
+!!! note
+    The automatic introspection of components, and many operation
+    parameters relies on the relevant attributes and methods of
+    `GenericAPIView`: `get_serializer()`, `pagination_class`, `filter_backends`,
+    etc. For basic `APIView` subclasses, default introspection is essentially limited to
+    the URL kwarg path parameters for this reason.
 
 `AutoSchema` encapsulates the view introspection needed for schema generation.
 Because of this all the schema generation logic is kept in a single place,
```



 - `.reference/api-guide/routers.md`

```
c0202a0aa5cbaf8573458b932878dfd5044c93ab -> e221d9a1d6638b936707efc390adff59511a6605
@@ -40,17 +40,14 @@ The example above would generate the following URL patterns:
 * URL pattern: `^accounts/$`  Name: `'account-list'`
 * URL pattern: `^accounts/{pk}/$`  Name: `'account-detail'`
 
----
-
-**Note**: The `basename` argument is used to specify the initial part of the view name pattern.  In the example above, that's the `user` or `account` part.
+!!! note
+    The `basename` argument is used to specify the initial part of the view name pattern.  In the example above, that's the `user` or `account` part.
 
-Typically you won't *need* to specify the `basename` argument, but if you have a viewset where you've defined a custom `get_queryset` method, then the viewset may not have a `.queryset` attribute set.  If you try to register that viewset you'll see an error like this:
+    Typically you won't *need* to specify the `basename` argument, but if you have a viewset where you've defined a custom `get_queryset` method, then the viewset may not have a `.queryset` attribute set.  If you try to register that viewset you'll see an error like this:
 
-    'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
+        'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
 
-This means you'll need to explicitly set the `basename` argument when registering the viewset, as it could not be automatically determined from the model name.
-
----
+    This means you'll need to explicitly set the `basename` argument when registering the viewset, as it could not be automatically determined from the model name.
 
 ### Using `include` with routers
 
@@ -91,16 +88,13 @@ Or both an application and instance namespace:
 
 See Django's [URL namespaces docs][url-namespace-docs] and the [`include` API reference][include-api-reference] for more details.
 
----
-
-**Note**: If using namespacing with hyperlinked serializers you'll also need to ensure that any `view_name` parameters
-on the serializers correctly reflect the namespace. In the examples above you'd need to include a parameter such as
-`view_name='app_name:user-detail'` for serializer fields hyperlinked to the user detail view.
-
-The automatic `view_name` generation uses a pattern like `%(model_name)-detail`. Unless your models names actually clash
-you may be better off **not** namespacing your Django REST Framework views when using hyperlinked serializers.
-
----
+!!! note
+    If using namespacing with hyperlinked serializers you'll also need to ensure that any `view_name` parameters
+    on the serializers correctly reflect the namespace. In the examples above you'd need to include a parameter such as
+    `view_name='app_name:user-detail'` for serializer fields hyperlinked to the user detail view.
+    
+    The automatic `view_name` generation uses a pattern like `%(model_name)-detail`. Unless your models names actually clash
+    you may be better off **not** namespacing your Django REST Framework views when using hyperlinked serializers.
 
 ### Routing for extra actions
```



 - `.reference/api-guide/viewsets.md`

```
9b3d03a3d257bca3eb99ca82770908adc7486a37 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -57,6 +57,9 @@ Typically we wouldn't do this, but would instead register the viewset with a rou
     router.register(r'users', UserViewSet, basename='user')
     urlpatterns = router.urls
 
+!!! warning
+    Do not use `.as_view()` with `@action` methods. It bypasses router setup and may ignore action settings like `permission_classes`. Use `DefaultRouter` for actions.
+
 Rather than writing your own viewsets, you'll often want to use the existing base classes that provide a default set of behavior.  For example:
 
     class UserViewSet(viewsets.ModelViewSet):
@@ -128,7 +131,8 @@ You may inspect these attributes to adjust behavior based on the current action.
             permission_classes = [IsAdminUser]
         return [permission() for permission in permission_classes]
 
-**Note**: the `action` attribute is not available in the `get_parsers`, `get_authenticators` and `get_content_negotiator` methods, as it is set _after_ they are called in the framework lifecycle. If you override one of these methods and try to access the `action` attribute in them, you will get an `AttributeError` error.
+!!! note
+    The `action` attribute is not available in the `get_parsers`, `get_authenticators` and `get_content_negotiator` methods, as it is set _after_ they are called in the framework lifecycle. If you override one of these methods and try to access the `action` attribute in them, you will get an `AttributeError` error.
 
 ## Marking extra actions for routing
```



 - `.reference/api-guide/requests.md`

```
041b88f8bbb48d9688ebd5add294eee2dfc93d1c -> e221d9a1d6638b936707efc390adff59511a6605
@@ -39,13 +39,10 @@ The `APIView` class or `@api_view` decorator will ensure that this property is a
 
 You won't typically need to access this property.
 
----
-
-**Note:** If a client sends malformed content, then accessing `request.data` may raise a `ParseError`.  By default REST framework's `APIView` class or `@api_view` decorator will catch the error and return a `400 Bad Request` response.
+!!! note
+    If a client sends malformed content, then accessing `request.data` may raise a `ParseError`.  By default REST framework's `APIView` class or `@api_view` decorator will catch the error and return a `400 Bad Request` response.
 
-If a client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised, which by default will be caught and return a `415 Unsupported Media Type` response.
-
----
+    If a client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised, which by default will be caught and return a `415 Unsupported Media Type` response.
 
 # Content negotiation
 
@@ -91,11 +88,8 @@ The `APIView` class or `@api_view` decorator will ensure that this property is a
 
 You won't typically need to access this property.
 
----
-
-**Note:** You may see a `WrappedAttributeError` raised when calling the `.user` or `.auth` properties. These errors originate from an authenticator as a standard `AttributeError`, however it's necessary that they be re-raised as a different exception type in order to prevent them from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from the authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. The authenticator will need to be fixed.
-
----
+!!! note
+    You may see a `WrappedAttributeError` raised when calling the `.user` or `.auth` properties. These errors originate from an authenticator as a standard `AttributeError`, however it's necessary that they be re-raised as a different exception type in order to prevent them from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from the authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. The authenticator will need to be fixed.
 
 # Browser enhancements
```



 - `.reference/api-guide/content-negotiation.md`

```
20d347a806baa0dd481b31a7f847386574882d5b -> e221d9a1d6638b936707efc390adff59511a6605
@@ -34,13 +34,11 @@ If the requested view was only configured with renderers for `YAML` and `HTML`,
 
 For more information on the `HTTP Accept` header, see [RFC 2616][accept-header]
 
----
-
-**Note**: "q" values are not taken into account by REST framework when determining preference.  The use of "q" values negatively impacts caching, and in the author's opinion they are an unnecessary and overcomplicated approach to content negotiation.
 
-This is a valid approach as the HTTP spec deliberately underspecifies how a server should weight server-based preferences against client-based preferences.
+!!! note
+    "q" values are not taken into account by REST framework when determining preference.  The use of "q" values negatively impacts caching, and in the author's opinion they are an unnecessary and overcomplicated approach to content negotiation.
 
----
+    This is a valid approach as the HTTP spec deliberately underspecifies how a server should weight server-based preferences against client-based preferences.
 
 # Custom content negotiation
```



 - `.reference/api-guide/permissions.md`

```
363dbba4137fe488f33ed24e0a9025228e66301f -> e221d9a1d6638b936707efc390adff59511a6605
@@ -51,18 +51,15 @@ For example:
         self.check_object_permissions(self.request, obj)
         return obj
 
----
-
-**Note**: With the exception of `DjangoObjectPermissions`, the provided
-permission classes in `rest_framework.permissions` **do not** implement the
-methods necessary to check object permissions.
+!!! note
+    With the exception of `DjangoObjectPermissions`, the provided
+    permission classes in `rest_framework.permissions` **do not** implement the
+    methods necessary to check object permissions.
 
-If you wish to use the provided permission classes in order to check object
-permissions, **you must** subclass them and implement the
-`has_object_permission()` method described in the [_Custom
-permissions_](#custom-permissions) section (below).
-
----
+    If you wish to use the provided permission classes in order to check object
+    permissions, **you must** subclass them and implement the
+    `has_object_permission()` method described in the [_Custom
+    permissions_](#custom-permissions) section (below).
 
 #### Limitations of object level permissions
 
@@ -118,7 +115,8 @@ Or, if you're using the `@api_view` decorator with function based views.
         }
         return Response(content)
 
-__Note:__ when you set new permission classes via the class attribute or decorators you're telling the view to ignore the default list set in the __settings.py__ file.
+!!! note
+    When you set new permission classes via the class attribute or decorators you're telling the view to ignore the default list set in the ``settings.py`` file.
 
 Provided they inherit from `rest_framework.permissions.BasePermission`, permissions can be composed using standard Python bitwise operators. For example, `IsAuthenticatedOrReadOnly` could be written:
 
@@ -131,7 +129,7 @@ Provided they inherit from `rest_framework.permissions.BasePermission`, permissi
             return request.method in SAFE_METHODS
 
     class ExampleView(APIView):
-        permission_classes = [IsAuthenticated|ReadOnly]
+        permission_classes = [IsAuthenticated | ReadOnly]
 
         def get(self, request, format=None):
             content = {
@@ -139,9 +137,8 @@ Provided they inherit from `rest_framework.permissions.BasePermission`, permissi
             }
             return Response(content)
 
-__Note:__ it supports & (and), | (or) and ~ (not).
-
----
+!!! note
+    Composition of permissions supports `&` (and), `|` (or) and `~` (not) operators.
 
 # API Reference
 
@@ -185,7 +182,7 @@ To use custom model permissions, override `DjangoModelPermissions` and set the `
 
 Similar to `DjangoModelPermissions`, but also allows unauthenticated users to have read-only access to the API.
 
-## DjangoObjectPermissions
+## DjangoObjectPermissions
 
 This permission class ties into Django's standard [object permissions framework][objectpermissions] that allows per-object permissions on models.  In order to use this permission class, you'll also need to add a permission backend that supports object-level permissions, such as [django-guardian][guardian].
 
@@ -199,11 +196,8 @@ Note that `DjangoObjectPermissions` **does not** require the `django-guardian` p
 
 As with `DjangoModelPermissions` you can use custom model permissions by overriding `DjangoObjectPermissions` and setting the `.perms_map` property.  Refer to the source code for details.
 
----
-
-**Note**: If you need object level `view` permissions for `GET`, `HEAD` and `OPTIONS` requests and are using django-guardian for your object-level permissions backend, you'll want to consider using the `DjangoObjectPermissionsFilter` class provided by the [`djangorestframework-guardian` package][django-rest-framework-guardian]. It ensures that list endpoints only return results including objects for which the user has appropriate view permissions.
-
----
+!!! note
+    If you need object level `view` permissions for `GET`, `HEAD` and `OPTIONS` requests and are using django-guardian for your object-level permissions backend, you'll want to consider using the `DjangoObjectPermissionsFilter` class provided by the [`djangorestframework-guardian` package][django-rest-framework-guardian]. It ensures that list endpoints only return results including objects for which the user has appropriate view permissions.
 
 # Custom permissions
 
@@ -221,11 +215,8 @@ If you need to test if a request is a read operation or a write operation, you s
     else:
         # Check permissions for write request
 
----
-
-**Note**: The instance-level `has_object_permission` method will only be called if the view-level `has_permission` checks have already passed. Also note that in order for the instance-level checks to run, the view code should explicitly call `.check_object_permissions(request, obj)`. If you are using the generic views then this will be handled for you by default. (Function-based views will need to check object permissions explicitly, raising `PermissionDenied` on failure.)
-
----
+!!! note
+    The instance-level `has_object_permission` method will only be called if the view-level `has_permission` checks have already passed. Also note that in order for the instance-level checks to run, the view code should explicitly call `.check_object_permissions(request, obj)`. If you are using the generic views then this will be handled for you by default. (Function-based views will need to check object permissions explicitly, raising `PermissionDenied` on failure.)
 
 Custom permissions will raise a `PermissionDenied` exception if the test fails. To change the error message associated with the exception, implement a `message` attribute directly on your custom permission. Otherwise the `default_detail` attribute from `PermissionDenied` will be used. Similarly, to change the code identifier associated with the exception, implement a `code` attribute directly on your custom permission - otherwise the `default_code` attribute from `PermissionDenied` will be used.
```



 - `.reference/api-guide/fields.md`

```
f9f10e041f9b2a2c936ee54a437d4c255f76e626 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -11,11 +11,8 @@ source:
 
 Serializer fields handle converting between primitive values and internal datatypes.  They also deal with validating input values, as well as retrieving and setting the values from their parent objects.
 
----
-
-**Note:** The serializer fields are declared in `fields.py`, but by convention you should import them using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.
-
----
+!!! note
+    The serializer fields are declared in `fields.py`, but by convention you should import them using `from rest_framework import serializers` and refer to fields as `serializers.<FieldName>`.
 
 ## Core arguments
 
@@ -565,11 +562,8 @@ The `HiddenField` class is usually only needed if you have some validation that
 
 For further examples on `HiddenField` see the [validators](validators.md) documentation.
 
----
-
-**Note:** `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request).
-
----
+!!! note
+    `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request).
 
 ## ModelField
```



 - `.reference/api-guide/views.md`

```
cf923511e7bbd1d05b6919af9af4e5edd81f5b71 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -45,11 +45,8 @@ For example:
             usernames = [user.username for user in User.objects.all()]
             return Response(usernames)
 
----
-
-**Note**: The full methods, attributes on, and relations between Django REST Framework's `APIView`, `GenericAPIView`, various `Mixins`, and `Viewsets` can be initially complex. In addition to the documentation here, the [Classy Django REST Framework][classy-drf] resource provides a browsable reference, with full methods and attributes, for each of Django REST Framework's class-based views.
-
----
+!!! note
+    The full methods, attributes on, and relations between Django REST Framework's `APIView`, `GenericAPIView`, various `Mixins`, and `Viewsets` can be initially complex. In addition to the documentation here, the [Classy Django REST Framework][classy-drf] resource provides a browsable reference, with full methods and attributes, for each of Django REST Framework's class-based views.
 
 
 ## API policy attributes
```



 - `.reference/tutorial/1-serialization.md`

```
c0f3649224117609d19e79c77242b525570d25c0 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -6,11 +6,8 @@ This tutorial will cover creating a simple pastebin code highlighting Web API.
 
 The tutorial is fairly in-depth, so you should probably get a cookie and a cup of your favorite brew before getting started.  If you just want a quick overview, you should head over to the [quickstart] documentation instead.
 
----
-
-**Note**: The code for this tutorial is available in the [encode/rest-framework-tutorial][repo] repository on GitHub. Feel free to clone the repository and see the code in action.
-
----
+!!! note
+    The code for this tutorial is available in the [encode/rest-framework-tutorial][repo] repository on GitHub. Feel free to clone the repository and see the code in action.
 
 ## Setting up a new environment
 
@@ -29,7 +26,8 @@ pip install djangorestframework
 pip install pygments  # We'll be using this for the code highlighting
 ```
 
-**Note:** To exit the virtual environment at any time, just type `deactivate`.  For more information see the [venv documentation][venv].
+!!! tip
+    To exit the virtual environment at any time, just type `deactivate`.  For more information see the [venv documentation][venv].
 
 ## Getting started
```



 - `.reference/tutorial/4-authentication-and-permissions.md`

```
c0f3649224117609d19e79c77242b525570d25c0 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -135,7 +135,8 @@ Now that snippets are associated with the user that created them, let's update o
 owner = serializers.ReadOnlyField(source="owner.username")
 ```
 
-**Note**: Make sure you also add `'owner',` to the list of fields in the inner `Meta` class.
+!!! note
+    Make sure you also add `'owner',` to the list of fields in the inner `Meta` class.
 
 This field is doing something quite interesting.  The `source` argument controls which attribute is used to populate a field, and can point at any attribute on the serialized instance.  It can also take the dotted notation shown above, in which case it will traverse the given attributes, in a similar way as it is used with Django's template language.
```



 - `.reference/tutorial/5-relationships-and-hyperlinked-apis.md`

```
c0f3649224117609d19e79c77242b525570d25c0 -> e221d9a1d6638b936707efc390adff59511a6605
@@ -120,25 +120,16 @@ Notice that we've also added a new `'highlight'` field.  This field is of the sa
 
 Because we've included format suffixed URLs such as `'.json'`, we also need to indicate on the `highlight` field that any format suffixed hyperlinks it returns should use the `'.html'` suffix.
 
----
+!!! note
+    When you are manually instantiating these serializers inside your views (e.g., in `SnippetDetail` or `SnippetList`), you **must** pass `context={'request': request}` so the serializer knows how to build absolute URLs. For example, instead of:
 
-**Note:**
+        serializer = SnippetSerializer(snippet)
+    
+    You must write:
 
-When you are manually instantiating these serializers inside your views (e.g., in `SnippetDetail` or `SnippetList`), you **must** pass `context={'request': request}` so the serializer knows how to build absolute URLs. For example, instead of:
-
-```python
-serializer = SnippetSerializer(snippet)
-```
-
-You must write:
-
-```python
-serializer = SnippetSerializer(snippet, context={"request": request})
-```
-
-If your view is a subclass of `GenericAPIView`, you may use the `get_serializer_context()` as a convenience method.
-
----
+        serializer = SnippetSerializer(snippet, context={"request": request})
+    
+    If your view is a subclass of `GenericAPIView`, you may use the `get_serializer_context()` as a convenience method.
 
 ## Making sure our URL patterns are named
```


