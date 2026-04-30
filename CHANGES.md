Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)
 - `.reference/api-guide/validators.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -25,7 +25,7 @@ With `ModelForm` the validation is performed partially on the form, and partiall
 
 When you're using `ModelSerializer` all of this is handled automatically for you. If you want to drop down to using `Serializer` classes instead, then you need to define the validation rules explicitly.
 
-#### Example
+### Example
 
 As an example of how REST framework uses explicit validation, we'll take a simple model class that has a field with a uniqueness constraint.
 
@@ -137,19 +137,19 @@ The date field that is used for the validation is always required to be present
 
 There are a couple of styles you may want to use for this depending on how you want your API to behave. If you're using `ModelSerializer` you'll probably simply rely on the defaults that REST framework generates for you, but if you are using `Serializer` or simply want more explicit control, use on of the styles demonstrated below.
 
-#### Using with a writable date field.
+### Using with a writable date field.
 
 If you want the date field to be writable the only thing worth noting is that you should ensure that it is always available in the input data, either by setting a `default` argument, or by setting `required=True`.
 
     published = serializers.DateTimeField(required=True)
 
-#### Using with a read-only date field.
+### Using with a read-only date field.
 
 If you want the date field to be visible, but not editable by the user, then set `read_only=True` and additionally set a `default=...` argument.
 
     published = serializers.DateTimeField(read_only=True, default=timezone.now)
 
-#### Using with a hidden date field.
+### Using with a hidden date field.
 
 If you want the date field to be entirely hidden from the user, then use `HiddenField`. This field type does not accept user input, but instead always returns its default value to the `validated_data` in the serializer.
 
@@ -161,7 +161,7 @@ If you want the date field to be entirely hidden from the user, then use `Hidden
 !!! note
     `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request). 
 
-# Advanced field defaults
+## Advanced field defaults
 
 Validators that are applied across multiple fields in the serializer can sometimes require a field input that should not be provided by the API client, but that *is* available as input to the validator.
 For this purposes use `HiddenField`. This field will be present in `validated_data` but *will not* be used in the serializer output representation.
@@ -171,7 +171,7 @@ For this purposes use `HiddenField`. This field will be present in `validated_da
 
 REST framework includes a couple of defaults that may be useful in this context.
 
-#### CurrentUserDefault
+### CurrentUserDefault
 
 A default class that can be used to represent the current user. In order to use this, the 'request' must have been provided as part of the context dictionary when instantiating the serializer.
 
@@ -179,7 +179,7 @@ A default class that can be used to represent the current user. In order to use
         default=serializers.CurrentUserDefault()
     )
 
-#### CreateOnlyDefault
+### CreateOnlyDefault
 
 A default class that can be used to *only set a default argument during create operations*. During updates the field is omitted.
 
@@ -191,7 +191,7 @@ It takes a single argument, which is the default value or callable that should b
 
 ---
 
-# Limitations of validators
+## Limitations of validators
 
 There are some ambiguous cases where you'll need to instead handle validation
 explicitly, rather than relying on the default serializer classes that
@@ -200,7 +200,7 @@ explicitly, rather than relying on the default serializer classes that
 In these cases you may want to disable the automatically generated validators,
 by specifying an empty list for the serializer `Meta.validators` attribute.
 
-## Optional fields
+### Optional fields
 
 By default "unique together" validation enforces that all fields be
 `required=True`. In some cases, you might want to explicit apply
@@ -222,7 +222,7 @@ For example:
             extra_kwargs = {'client': {'required': False}}
             validators = []  # Remove a default "unique together" constraint.
 
-## Updating nested serializers
+### Updating nested serializers
 
 When applying an update to an existing instance, uniqueness validators will
 exclude the current instance from the uniqueness check. The current instance
@@ -237,7 +237,7 @@ Again, you'll probably want to explicitly remove the validator from the
 serializer class, and write the code for the validation constraint
 explicitly, in a `.validate()` method, or in the view.
 
-## Debugging complex cases
+### Debugging complex cases
 
 If you're not sure exactly what behavior a `ModelSerializer` class will
 generate it is usually a good idea to run `manage.py shell`, and print
@@ -256,11 +256,11 @@ that the resulting behavior is more transparent.
 
 ---
 
-# Writing custom validators
+## Writing custom validators
 
 You can use any of Django's existing validators, or write your own custom validators.
 
-## Function based
+### Function based
 
 A validator may be any callable that raises a `serializers.ValidationError` on failure.
 
@@ -274,7 +274,7 @@ You can specify custom field-level validation by adding `.validate_<field_name>`
 to your `Serializer` subclass. This is documented in the
 [Serializer docs](https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation)
 
-## Class-based
+### Class-based
 
 To write a class-based validator, use the `__call__` method. Class-based validators are useful as they allow you to parameterize and reuse behavior.
```


 - `.reference/api-guide/parsers.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -66,15 +66,15 @@ Or, if you're using the `@api_view` decorator with function based views.
 
 ---
 
-# API Reference
+## API Reference
 
-## JSONParser
+### JSONParser
 
 Parses `JSON` request content. `request.data` will be populated with a dictionary of data.
 
 **.media_type**: `application/json`
 
-## FormParser
+### FormParser
 
 Parses HTML form content.  `request.data` will be populated with a `QueryDict` of data.
 
@@ -82,7 +82,7 @@ You will typically want to use both `FormParser` and `MultiPartParser` together
 
 **.media_type**: `application/x-www-form-urlencoded`
 
-## MultiPartParser
+### MultiPartParser
 
 Parses multipart HTML form content, which supports file uploads. `request.data` and `request.FILES` will be populated with a `QueryDict` and `MultiValueDict` respectively.
 
@@ -90,7 +90,7 @@ You will typically want to use both `FormParser` and `MultiPartParser` together
 
 **.media_type**: `multipart/form-data`
 
-## FileUploadParser
+### FileUploadParser
 
 Parses raw file upload content.  The `request.data` property will be a dictionary with a single key `'file'` containing the uploaded file.
 
@@ -100,13 +100,13 @@ If it is called without a `filename` URL keyword argument, then the client must
 
 **.media_type**: `*/*`
 
-##### Notes:
+!!! note
 
-* The `FileUploadParser` is for usage with native clients that can upload the file as a raw data request.  For web-based uploads, or for native clients with multipart upload support, you should use the `MultiPartParser` instead.
-* Since this parser's `media_type` matches any content type, `FileUploadParser` should generally be the only parser set on an API view.
-* `FileUploadParser` respects Django's standard `FILE_UPLOAD_HANDLERS` setting, and the `request.upload_handlers` attribute.  See the [Django documentation][upload-handlers] for more details.
+    * The `FileUploadParser` is for usage with native clients that can upload the file as a raw data request.  For web-based uploads, or for native clients with multipart upload support, you should use the `MultiPartParser` instead.
+    * Since this parser's `media_type` matches any content type, `FileUploadParser` should generally be the only parser set on an API view.
+    * `FileUploadParser` respects Django's standard `FILE_UPLOAD_HANDLERS` setting, and the `request.upload_handlers` attribute.  See the [Django documentation][upload-handlers] for more details.
 
-##### Basic usage example:
+#### Basic usage example
 
     # views.py
     class FileUploadView(views.APIView):
@@ -127,7 +127,7 @@ If it is called without a `filename` URL keyword argument, then the client must
 
 ---
 
-# Custom parsers
+## Custom parsers
 
 To implement a custom parser, you should override `BaseParser`, set the `.media_type` property, and implement the `.parse(self, stream, media_type, parser_context)` method.
 
@@ -151,7 +151,7 @@ Optional.  If supplied, this argument will be a dictionary containing any additi
 
 By default this will include the following keys: `view`, `request`, `args`, `kwargs`.
 
-## Example
+### Example
 
 The following is an example plaintext parser that will populate the `request.data` property with a string representing the body of the request.
 
@@ -169,11 +169,11 @@ The following is an example plaintext parser that will populate the `request.dat
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## YAML
+### YAML
 
 [REST framework YAML][rest-framework-yaml] provides [YAML][yaml] parsing and rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
@@ -194,7 +194,7 @@ Modify your REST framework settings.
         ],
     }
 
-## XML
+### XML
 
 [REST Framework XML][rest-framework-xml] provides a simple informal XML format. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
@@ -215,11 +215,11 @@ Modify your REST framework settings.
         ],
     }
 
-## MessagePack
+### MessagePack
 
 [MessagePack][messagepack] is a fast, efficient binary serialization format.  [Juan Riaza][juanriaza] maintains the [djangorestframework-msgpack][djangorestframework-msgpack] package which provides MessagePack renderer and parser support for REST framework.
 
-## CamelCase JSON
+### CamelCase JSON
 
 [djangorestframework-camel-case] provides camel case JSON renderers and parsers for REST framework.  This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names.  It is maintained by [Vitaly Babiy][vbabiy].
```


 - `.reference/api-guide/generic-views.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -49,15 +49,15 @@ For very simple cases you might want to pass through any class attributes using
 
 ---
 
-# API Reference
+## API Reference
 
-## GenericAPIView
+### GenericAPIView
 
 This class extends REST framework's `APIView` class, adding commonly required behavior for standard list and detail views.
 
 Each of the concrete generic views provided is built by combining `GenericAPIView`, with one or more mixin classes.
 
-### Attributes
+#### Attributes
 
 **Basic settings**:
 
@@ -78,11 +78,11 @@ The following attributes are used to control pagination when used with list view
 
 * `filter_backends` - A list of filter backend classes that should be used for filtering the queryset.  Defaults to the same value as the `DEFAULT_FILTER_BACKENDS` setting.
 
-### Methods
+#### Methods
 
 **Base methods**:
 
-#### `get_queryset(self)`
+##### `get_queryset(self)`
 
 Returns the queryset that should be used for list views, and that should be used as the base for lookups in detail views.  Defaults to returning the queryset specified by the `queryset` attribute.
 
@@ -99,7 +99,7 @@ For example:
 !!! tip
     If the `serializer_class` used in the generic view spans ORM relations, leading to an N+1 problem, you could optimize your queryset in this method using `select_related` and `prefetch_related`. To get more information about N+1 problem and use cases of the mentioned methods refer to related section in [django documentation][django-docs-select-related].
 
-### Avoiding N+1 Queries
+#### Avoiding N+1 Queries
 
 When listing objects (e.g. using `ListAPIView` or `ModelViewSet`), serializers may trigger an N+1 query pattern if related objects are accessed individually for each item.
 
@@ -132,7 +132,7 @@ These optimizations reduce repeated database access and improve list view perfor
 
 ---
 
-#### `get_object(self)`
+##### `get_object(self)`
 
 Returns an object instance that should be used for detail views.  Defaults to using the `lookup_field` parameter to filter the base queryset.
 
@@ -152,7 +152,7 @@ For example:
 
 Note that if your API doesn't include any object level permissions, you may optionally exclude the `self.check_object_permissions`, and simply return the object from the `get_object_or_404` lookup.
 
-#### `filter_queryset(self, queryset)`
+##### `filter_queryset(self, queryset)`
 
 Given a queryset, filter it with whichever filter backends are in use, returning a new queryset.
 
@@ -171,7 +171,7 @@ For example:
 
         return queryset
 
-#### `get_serializer_class(self)`
+##### `get_serializer_class(self)`
 
 Returns the class that should be used for the serializer.  Defaults to returning the `serializer_class` attribute.
 
@@ -223,19 +223,19 @@ You won't typically need to override the following methods, although you might n
 
 ---
 
-# Mixins
+## Mixins
 
 The mixin classes provide the actions that are used to provide the basic view behavior.  Note that the mixin classes provide action methods rather than defining the handler methods, such as `.get()` and `.post()`, directly.  This allows for more flexible composition of behavior.
 
 The mixin classes can be imported from `rest_framework.mixins`.
 
-## ListModelMixin
+### ListModelMixin
 
 Provides a `.list(request, *args, **kwargs)` method, that implements listing a queryset.
 
 If the queryset is populated, this returns a `200 OK` response, with a serialized representation of the queryset as the body of the response.  The response data may optionally be paginated.
 
-## CreateModelMixin
+### CreateModelMixin
 
 Provides a `.create(request, *args, **kwargs)` method, that implements creating and saving a new model instance.
 
@@ -243,13 +243,13 @@ If an object is created this returns a `201 Created` response, with a serialized
 
 If the request data provided for creating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.
 
-## RetrieveModelMixin
+### RetrieveModelMixin
 
 Provides a `.retrieve(request, *args, **kwargs)` method, that implements returning an existing model instance in a response.
 
 If an object can be retrieved this returns a `200 OK` response, with a serialized representation of the object as the body of the response.  Otherwise, it will return a `404 Not Found`.
 
-## UpdateModelMixin
+### UpdateModelMixin
 
 Provides a `.update(request, *args, **kwargs)` method, that implements updating and saving an existing model instance.
 
@@ -259,7 +259,7 @@ If an object is updated this returns a `200 OK` response, with a serialized repr
 
 If the request data provided for updating the object was invalid, a `400 Bad Request` response will be returned, with the error details as the body of the response.
 
-## DestroyModelMixin
+### DestroyModelMixin
 
 Provides a `.destroy(request, *args, **kwargs)` method, that implements deletion of an existing model instance.
 
@@ -267,13 +267,13 @@ If an object is deleted this returns a `204 No Content` response, otherwise it w
 
 ---
 
-# Concrete View Classes
+## Concrete View Classes
 
 The following classes are the concrete generic views.  If you're using generic views this is normally the level you'll be working at unless you need heavily customized behavior.
 
 The view classes can be imported from `rest_framework.generics`.
 
-## CreateAPIView
+### CreateAPIView
 
 Used for **create-only** endpoints.
 
@@ -281,7 +281,7 @@ Provides a `post` method handler.
 
 Extends: [GenericAPIView], [CreateModelMixin]
 
-## ListAPIView
+### ListAPIView
 
 Used for **read-only** endpoints to represent a **collection of model instances**.
 
@@ -289,7 +289,7 @@ Provides a `get` method handler.
 
 Extends: [GenericAPIView], [ListModelMixin]
 
-## RetrieveAPIView
+### RetrieveAPIView
 
 Used for **read-only** endpoints to represent a **single model instance**.
 
@@ -297,7 +297,7 @@ Provides a `get` method handler.
 
 Extends: [GenericAPIView], [RetrieveModelMixin]
 
-## DestroyAPIView
+### DestroyAPIView
 
 Used for **delete-only** endpoints for a **single model instance**.
 
@@ -305,7 +305,7 @@ Provides a `delete` method handler.
 
 Extends: [GenericAPIView], [DestroyModelMixin]
 
-## UpdateAPIView
+### UpdateAPIView
 
 Used for **update-only** endpoints for a **single model instance**.
 
@@ -313,7 +313,7 @@ Provides `put` and `patch` method handlers.
 
 Extends: [GenericAPIView], [UpdateModelMixin]
 
-## ListCreateAPIView
+### ListCreateAPIView
 
 Used for **read-write** endpoints to represent a **collection of model instances**.
 
@@ -321,7 +321,7 @@ Provides `get` and `post` method handlers.
 
 Extends: [GenericAPIView], [ListModelMixin], [CreateModelMixin]
 
-## RetrieveUpdateAPIView
+### RetrieveUpdateAPIView
 
 Used for **read or update** endpoints to represent a **single model instance**.
 
@@ -329,7 +329,7 @@ Provides `get`, `put` and `patch` method handlers.
 
 Extends: [GenericAPIView], [RetrieveModelMixin], [UpdateModelMixin]
 
-## RetrieveDestroyAPIView
+### RetrieveDestroyAPIView
 
 Used for **read or delete** endpoints to represent a **single model instance**.
 
@@ -337,7 +337,7 @@ Provides `get` and `delete` method handlers.
 
 Extends: [GenericAPIView], [RetrieveModelMixin], [DestroyModelMixin]
 
-## RetrieveUpdateDestroyAPIView
+### RetrieveUpdateDestroyAPIView
 
 Used for **read-write-delete** endpoints to represent a **single model instance**.
 
@@ -347,11 +347,11 @@ Extends: [GenericAPIView], [RetrieveModelMixin], [UpdateModelMixin], [DestroyMod
 
 ---
 
-# Customizing the generic views
+## Customizing the generic views
 
 Often you'll want to use the existing generic views, but use some slightly customized behavior.  If you find yourself reusing some bit of customized behavior in multiple places, you might want to refactor the behavior into a common class that you can then just apply to any view or viewset as needed.
 
-## Creating custom mixins
+### Creating custom mixins
 
 For example, if you need to lookup objects based on multiple fields in the URL conf, you could create a mixin class like the following:
 
@@ -380,7 +380,7 @@ You can then simply apply this mixin to a view or viewset anytime you need to ap
 
 Using custom mixins is a good option if you have custom behavior that needs to be used.
 
-## Creating custom base classes
+### Creating custom base classes
 
 If you are using a mixin across multiple views, you can take this a step further and create your own set of base views that can then be used throughout your project.  For example:
 
@@ -396,7 +396,7 @@ Using custom base classes is a good option if you have custom behavior that cons
 
 ---
 
-# PUT as create
+## PUT as create
 
 Prior to version 3.0 the REST framework mixins treated `PUT` as either an update or a create operation, depending on if the object already existed or not.
 
@@ -406,11 +406,11 @@ Both styles "`PUT` as 404" and "`PUT` as create" can be valid in different circu
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third party packages provide additional generic view implementations.
 
-## Django Rest Multiple Models
+### Django Rest Multiple Models
 
 [Django Rest Multiple Models][django-rest-multiple-models] provides a generic view (and mixin) for sending multiple serialized models and/or querysets via a single API request.
```


 - `.reference/api-guide/testing.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> 7f8ad25e15f911ef2afd54d91dcffb29ca1022f9
@@ -11,11 +11,11 @@ source:
 
 REST framework includes a few helper classes that extend Django's existing test framework, and improve support for making API requests.
 
-# APIRequestFactory
+## APIRequestFactory
 
 Extends [Django's existing `RequestFactory` class][requestfactory].
 
-## Creating test requests
+### Creating test requests
 
 The `APIRequestFactory` class supports an almost identical API to Django's standard `RequestFactory` class.  This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available.
 
@@ -65,7 +65,7 @@ Using Django's `RequestFactory`, you'd need to explicitly encode the data yourse
     content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
     request = factory.put('/notes/547/', content, content_type=content_type)
 
-## Forcing authentication
+### Forcing authentication
 
 When testing views directly using a request factory, it's often convenient to be able to directly authenticate the request, rather than having to construct the correct authentication credentials.
 
@@ -117,7 +117,7 @@ For example, when forcibly authenticating using a token, you might do something
         drf_request = DummyView().initialize_request(request)
         assert drf_request.data.get('example') == 'test'
 
-## Forcing CSRF validation
+### Forcing CSRF validation
 
 By default, requests created with `APIRequestFactory` will not have CSRF validation applied when passed to a REST framework view.  If you need to explicitly turn CSRF validation on, you can do so by setting the `enforce_csrf_checks` flag when instantiating the factory.
 
@@ -126,11 +126,11 @@ By default, requests created with `APIRequestFactory` will not have CSRF validat
 !!! note
     It's worth noting that Django's standard `RequestFactory` doesn't need to include this option, because when using regular Django the CSRF validation takes place in middleware, which is not run when testing views directly.  When using REST framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.
 
-# APIClient
+## APIClient
 
 Extends [Django's existing `Client` class][client].
 
-## Making requests
+### Making requests
 
 The `APIClient` class supports the same request interface as Django's standard `Client` class.  This means that the standard `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` methods are all available.  For example:
 
@@ -141,7 +141,7 @@ The `APIClient` class supports the same request interface as Django's standard `
 
 To support a wider set of request formats, or change the default format, [see the configuration section][configuration].
 
-## Authenticating
+### Authenticating
 
 #### .login(**kwargs)
 
@@ -191,7 +191,7 @@ To unauthenticate subsequent requests, call `force_authenticate` setting the use
 
     client.force_authenticate(user=None)
 
-## CSRF validation
+### CSRF validation
 
 By default CSRF validation is not applied when using `APIClient`.  If you need to explicitly enable CSRF validation, you can do so by setting the `enforce_csrf_checks` flag when instantiating the client.
 
@@ -201,7 +201,7 @@ As usual CSRF validation will only apply to any session authenticated views.  Th
 
 ---
 
-# RequestsClient
+## RequestsClient
 
 REST framework also includes a client for interacting with your application
 using the popular Python library, `requests`. This may be useful if:
@@ -222,13 +222,13 @@ directly.
 
 Note that the requests client requires you to pass fully qualified URLs.
 
-## RequestsClient and working with the database
+### RequestsClient and working with the database
 
 The `RequestsClient` class is useful if you want to write tests that solely interact with the service interface. This is a little stricter than using the standard Django test client, as it means that all interactions should be via the API.
 
 If you're using `RequestsClient` you'll want to ensure that test setup, and results assertions are performed as regular API calls, rather than interacting with the database models directly. For example, rather than checking that `Customer.objects.count() == 3` you would list the customers endpoint, and ensure that it contains three records.
 
-## Headers & Authentication
+### Headers & Authentication
 
 Custom headers and authentication credentials can be provided in the same way
 as [when using a standard `requests.Session` instance][session_objects].
@@ -238,7 +238,7 @@ as [when using a standard `requests.Session` instance][session_objects].
     client.auth = HTTPBasicAuth('user', 'pass')
     client.headers.update({'x-test': 'true'})
 
-## CSRF
+### CSRF
 
 If you're using `SessionAuthentication` then you'll need to include a CSRF token
 for any `POST`, `PUT`, `PATCH` or `DELETE` requests.
@@ -263,12 +263,17 @@ For example...
     }, headers={'X-CSRFToken': csrftoken})
     assert response.status_code == 200
 
-## Live tests
+### Live tests
 
-With careful usage both the `RequestsClient` and the `CoreAPIClient` provide
-the ability to write test cases that can run either in development, or be run
-directly against your staging server or production environment.
+With careful usage the `RequestsClient` provides the ability to write tests
+that exercise your API views in a more end-to-end fashion than `APIClient`,
+while still running entirely in-process against your local Django application.
 
+Note that `RequestsClient` mounts a WSGI adapter and does not perform real
+network I/O. It cannot be used to send HTTP requests to remote services such
+as staging or production servers. For live tests against a deployed service,
+you should instead use a plain `requests.Session` (or similar HTTP client)
+configured with the appropriate base URL and authentication.
 Using this style to create basic tests of a few core pieces of functionality is
 a powerful way to validate your live service. Doing so may require some careful
 attention to setup and teardown to ensure that the tests run in a way that they
@@ -276,38 +281,7 @@ do not directly affect customer data.
 
 ---
 
-# CoreAPIClient
-
-The CoreAPIClient allows you to interact with your API using the Python
-`coreapi` client library.
-
-    # Fetch the API schema
-    client = CoreAPIClient()
-    schema = client.get('http://testserver/schema/')
-
-    # Create a new organization
-    params = {'name': 'MegaCorp', 'status': 'active'}
-    client.action(schema, ['organizations', 'create'], params)
-
-    # Ensure that the organization exists in the listing
-    data = client.action(schema, ['organizations', 'list'])
-    assert(len(data) == 1)
-    assert(data == [{'name': 'MegaCorp', 'status': 'active'}])
-
-## Headers & Authentication
-
-Custom headers and authentication may be used with `CoreAPIClient` in a
-similar way as with `RequestsClient`.
-
-    from requests.auth import HTTPBasicAuth
-
-    client = CoreAPIClient()
-    client.session.auth = HTTPBasicAuth('user', 'pass')
-    client.session.headers.update({'x-test': 'true'})
-
----
-
-# API Test cases
+## API Test cases
 
 REST framework includes the following test case classes, that mirror the existing [Django's test case classes][provided_test_case_classes], but use `APIClient` instead of Django's default `Client`.
 
@@ -316,7 +290,7 @@ REST framework includes the following test case classes, that mirror the existin
 * `APITestCase`
 * `APILiveServerTestCase`
 
-## Example
+### Example
 
 You can use any of REST framework's test case classes as you would for the regular Django test case classes.  The `self.client` attribute will be an `APIClient` instance.
 
@@ -339,11 +313,11 @@ You can use any of REST framework's test case classes as you would for the regul
 
 ---
 
-# URLPatternsTestCase
+## URLPatternsTestCase
 
 REST framework also provides a test case class for isolating `urlpatterns` on a per-class basis. Note that this inherits from Django's `SimpleTestCase`, and will most likely need to be mixed with another test case class.
 
-## Example
+### Example
 
     from django.urls import include, path, reverse
     from rest_framework import status
@@ -366,9 +340,9 @@ REST framework also provides a test case class for isolating `urlpatterns` on a
 
 ---
 
-# Testing responses
+## Testing responses
 
-## Checking the response data
+### Checking the response data
 
 When checking the validity of test responses it's often more convenient to inspect the data that the response was created with, rather than inspecting the fully rendered response.
 
@@ -382,7 +356,7 @@ Instead of inspecting the result of parsing `response.content`:
     response = self.client.get('/users/4/')
     self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})
 
-## Rendering responses
+### Rendering responses
 
 If you're testing views directly using `APIRequestFactory`, the responses that are returned will not yet be rendered, as rendering of template responses is performed by Django's internal request-response cycle.  In order to access `response.content`, you'll first need to render the response.
 
@@ -394,9 +368,9 @@ If you're testing views directly using `APIRequestFactory`, the responses that a
 
 ---
 
-# Configuration
+## Configuration
 
-## Setting the default format
+### Setting the default format
 
 The default format used to make test requests may be set using the `TEST_REQUEST_DEFAULT_FORMAT` setting key.  For example, to always use JSON for test requests by default instead of standard multipart form requests, set the following in your `settings.py` file:
 
@@ -405,7 +379,7 @@ The default format used to make test requests may be set using the `TEST_REQUEST
         'TEST_REQUEST_DEFAULT_FORMAT': 'json'
     }
 
-## Setting the available formats
+### Setting the available formats
 
 If you need to test requests using something other than multipart or json requests, you can do so by setting the `TEST_REQUEST_RENDERER_CLASSES` setting.
```


 - `.reference/api-guide/views.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> 7f8ad25e15f911ef2afd54d91dcffb29ca1022f9
@@ -4,7 +4,7 @@ source:
     - views.py
 ---
 
-# Class-based Views
+## Class-based Views
 
 > Django's class-based views are a welcome departure from the old-style views.
 >
@@ -49,63 +49,63 @@ For example:
     The full methods, attributes on, and relations between Django REST Framework's `APIView`, `GenericAPIView`, various `Mixins`, and `Viewsets` can be initially complex. In addition to the documentation here, the [Classy Django REST Framework][classy-drf] resource provides a browsable reference, with full methods and attributes, for each of Django REST Framework's class-based views.
 
 
-## API policy attributes
+### API policy attributes
 
 The following attributes control the pluggable aspects of API views.
 
-### .renderer_classes
+#### .renderer_classes
 
-### .parser_classes
+#### .parser_classes
 
-### .authentication_classes
+#### .authentication_classes
 
-### .throttle_classes
+#### .throttle_classes
 
-### .permission_classes
+#### .permission_classes
 
-### .content_negotiation_class
+#### .content_negotiation_class
 
-## API policy instantiation methods
+### API policy instantiation methods
 
 The following methods are used by REST framework to instantiate the various pluggable API policies.  You won't typically need to override these methods.
 
-### .get_renderers(self)
+#### .get_renderers(self)
 
-### .get_parsers(self)
+#### .get_parsers(self)
 
-### .get_authenticators(self)
+#### .get_authenticators(self)
 
-### .get_throttles(self)
+#### .get_throttles(self)
 
-### .get_permissions(self)
+#### .get_permissions(self)
 
-### .get_content_negotiator(self)
+#### .get_content_negotiator(self)
 
-### .get_exception_handler(self)
+#### .get_exception_handler(self)
 
-## API policy implementation methods
+### API policy implementation methods
 
 The following methods are called before dispatching to the handler method.
 
-### .check_permissions(self, request)
+#### .check_permissions(self, request)
 
-### .check_throttles(self, request)
+#### .check_throttles(self, request)
 
-### .perform_content_negotiation(self, request, force=False)
+#### .perform_content_negotiation(self, request, force=False)
 
-## Dispatch methods
+### Dispatch methods
 
 The following methods are called directly by the view's `.dispatch()` method.
 These perform any actions that need to occur before or after calling the handler methods such as `.get()`, `.post()`, `put()`, `patch()` and `.delete()`.
 
-### .initial(self, request, \*args, **kwargs)
+#### .initial(self, request, \*args, **kwargs)
 
 Performs any actions that need to occur before the handler method gets called.
 This method is used to enforce permissions and throttling, and perform content negotiation.
 
 You won't typically need to override this method.
 
-### .handle_exception(self, exc)
+#### .handle_exception(self, exc)
 
 Any exception thrown by the handler method will be passed to this method, which either returns a `Response` instance, or re-raises the exception.
 
@@ -113,13 +113,13 @@ The default implementation handles any subclass of `rest_framework.exceptions.AP
 
 If you need to customize the error responses your API returns you should subclass this method.
 
-### .initialize_request(self, request, \*args, **kwargs)
+#### .initialize_request(self, request, \*args, **kwargs)
 
 Ensures that the request object that is passed to the handler method is an instance of `Request`, rather than the usual Django `HttpRequest`.
 
 You won't typically need to override this method.
 
-### .finalize_response(self, request, response, \*args, **kwargs)
+#### .finalize_response(self, request, response, \*args, **kwargs)
 
 Ensures that any `Response` object returned from the handler method will be rendered into the correct content type, as determined by the content negotiation.
 
@@ -127,7 +127,7 @@ You won't typically need to override this method.
 
 ---
 
-# Function Based Views
+## Function Based Views
 
 > Saying [that class-based views] is always the superior solution is a mistake.
 >
@@ -135,7 +135,7 @@ You won't typically need to override this method.
 
 REST framework also allows you to work with regular function based views.  It provides a set of simple decorators that wrap your function based views to ensure they receive an instance of `Request` (rather than the usual Django `HttpRequest`) and allows them to return a `Response` (instead of a Django `HttpResponse`), and allow you to configure how the request is processed.
 
-## @api_view()
+### @api_view()
 
 **Signature:** `@api_view(http_method_names=['GET'])`
 
@@ -159,7 +159,7 @@ By default only `GET` methods will be accepted. Other methods will respond with
         return Response({"message": "Hello, world!"})
 
 
-## API policy decorators
+### API policy decorators
 
 To override the default settings, REST framework provides a set of additional decorators which can be added to your views.  These must come *after* (below) the `@api_view` decorator.  For example, to create a view that uses a [throttle][throttling] to ensure it can only be called once per day by a particular user, use the `@throttle_classes` decorator, passing a list of throttle classes:
 
@@ -192,7 +192,7 @@ Each of these decorators is equivalent to setting their respective [api policy a
 All decorators take a single argument. The ones that end with `_class` expect a single class while the ones ending in `_classes` expect a list or tuple of classes.
 
 
-## View schema decorator
+### View schema decorator
 
 To override the default schema generation for function based views you may use
 the `@schema` decorator. This must come *after* (below) the `@api_view`
@@ -202,7 +202,7 @@ decorator. For example:
     from rest_framework.schemas import AutoSchema
 
     class CustomAutoSchema(AutoSchema):
-        def get_link(self, path, method, base_url):
+        def get_operation(self, path, method):
             # override view introspection here...
 
     @api_view(['GET'])
@@ -210,8 +210,8 @@ decorator. For example:
     def view(request):
         return Response({"message": "Hello for today! See you tomorrow!"})
 
-This decorator takes a single `AutoSchema` instance, an `AutoSchema` subclass
-instance or `ManualSchema` instance as described in the [Schemas documentation][schemas].
+This decorator takes a single `AutoSchema` instance or an `AutoSchema` subclass
+instance as described in the [Schemas documentation][schemas].
 You may pass `None` in order to exclude the view from schema generation.
 
     @api_view(['GET'])
```


 - `.reference/api-guide/settings.md`
```
f9f10e041f9b2a2c936ee54a437d4c255f76e626 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -35,9 +35,9 @@ The `api_settings` object will check for any user-defined settings, and otherwis
 
 ---
 
-# API Reference
+## API Reference
 
-## API policy settings
+### API policy settings
 
 *The following settings control the basic API policies, and are applied to every `APIView` class-based view, or `@api_view` function based view.*
 
@@ -105,7 +105,7 @@ Default: `'rest_framework.schemas.openapi.AutoSchema'`
 
 ---
 
-## Generic view settings
+### Generic view settings
 
 *The following settings control the behavior of the generic class-based views.*
 
@@ -129,7 +129,7 @@ The default page size to use for pagination.  If set to `None`, pagination is di
 
 Default: `None`
 
-### SEARCH_PARAM
+#### SEARCH_PARAM
 
 The name of a query parameter, which can be used to specify the search term used by `SearchFilter`.
 
@@ -143,7 +143,7 @@ Default: `ordering`
 
 ---
 
-## Versioning settings
+### Versioning settings
 
 #### DEFAULT_VERSION
 
@@ -171,7 +171,7 @@ Default: `None`
 
 ---
 
-## Authentication settings
+### Authentication settings
 
 *The following settings control the behavior of unauthenticated requests.*
 
@@ -191,7 +191,7 @@ Default: `None`
 
 ---
 
-## Test settings
+### Test settings
 
 *The following settings control the behavior of APIRequestFactory and APIClient*
 
@@ -218,7 +218,7 @@ Default:
 
 ---
 
-## Schema generation controls
+### Schema generation controls
 
 #### SCHEMA_COERCE_PATH_PK
 
@@ -240,7 +240,7 @@ Default: `{'retrieve': 'read', 'destroy': 'delete'}`
 
 ---
 
-## Content type controls
+### Content type controls
 
 #### URL_FORMAT_OVERRIDE
 
@@ -262,7 +262,7 @@ Default: `'format'`
 
 ---
 
-## Date and time formatting
+### Date and time formatting
 
 *The following settings are used to control how date and time representations may be parsed and rendered.*
 
@@ -325,7 +325,7 @@ Default: `'django'`
 
 ---
 
-## Encodings
+### Encodings
 
 #### UNICODE_JSON
 
@@ -381,7 +381,7 @@ Default: `False`
 
 ---
 
-## View names and descriptions
+### View names and descriptions
 
 **The following settings are used to generate the view names and descriptions, as used in responses to `OPTIONS` requests, and as used in the browsable API.**
 
@@ -422,7 +422,7 @@ If the view instance inherits `ViewSet`, it may have been initialized with sever
 
 Default: `'rest_framework.views.get_view_description'`
 
-## HTML Select Field cutoffs
+### HTML Select Field cutoffs
 
 Global settings for [select field cutoffs for rendering relational fields](relations.md#select-field-cutoffs) in the browsable API.
 
@@ -440,7 +440,7 @@ Default: `"More than {count} items..."`
 
 ---
 
-## Miscellaneous settings
+### Miscellaneous settings
 
 #### EXCEPTION_HANDLER
```


 - `.reference/api-guide/renderers.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -71,9 +71,9 @@ If your API includes views that can serve both regular webpages and API response
 
 ---
 
-# API Reference
+## API Reference
 
-## JSONRenderer
+### JSONRenderer
 
 Renders the request data into `JSON`, using utf-8 encoding.
 
@@ -96,7 +96,7 @@ The default JSON encoding style can be altered using the `UNICODE_JSON` and `COM
 
 **.charset**: `None`
 
-## TemplateHTMLRenderer
+### TemplateHTMLRenderer
 
 Renders data to HTML, using Django's standard template rendering.
 Unlike other renderers, the data passed to the `Response` does not need to be serialized.  Also, unlike other renderers, you may want to include a `template_name` argument when creating the `Response`.
@@ -141,7 +141,7 @@ See the [_HTML & Forms_ Topic Page][html-and-forms] for further examples of `Tem
 
 See also: `StaticHTMLRenderer`
 
-## StaticHTMLRenderer
+### StaticHTMLRenderer
 
 A simple renderer that simply returns pre-rendered HTML.  Unlike other renderers, the data passed to the response object should be a string representing the content to be returned.
 
@@ -163,7 +163,7 @@ You can use `StaticHTMLRenderer` either to return regular HTML pages using REST
 
 See also: `TemplateHTMLRenderer`
 
-## BrowsableAPIRenderer
+### BrowsableAPIRenderer
 
 Renders data into HTML for the Browsable API:
 
@@ -187,7 +187,7 @@ By default the response content will be rendered with the highest priority rende
         def get_default_renderer(self, view):
             return JSONRenderer()
 
-## AdminRenderer
+### AdminRenderer
 
 Renders data into HTML for an admin-like display:
 
@@ -217,7 +217,7 @@ Note that views that have nested or list serializers for their input won't work
 
 **.template**: `'rest_framework/admin.html'`
 
-## HTMLFormRenderer
+### HTMLFormRenderer
 
 Renders data returned by a serializer into an HTML form. The output of this renderer does not include the enclosing `<form>` tags, a hidden CSRF input or any submit buttons.
 
@@ -241,7 +241,7 @@ For more information see the [HTML & Forms][html-and-forms] documentation.
 
 **.template**: `'rest_framework/horizontal/form.html'`
 
-## MultiPartRenderer
+### MultiPartRenderer
 
 This renderer is used for rendering HTML multipart form data.  **It is not suitable as a response renderer**, but is instead used for creating test requests, using REST framework's [test client and test request factory][testing].
 
@@ -253,7 +253,7 @@ This renderer is used for rendering HTML multipart form data.  **It is not suita
 
 ---
 
-# Custom renderers
+## Custom renderers
 
 To implement a custom renderer, you should override `BaseRenderer`, set the `.media_type` and `.format` properties, and implement the `.render(self, data, accepted_media_type=None, renderer_context=None)` method.
 
@@ -261,23 +261,13 @@ The method should return a bytestring, which will be used as the body of the HTT
 
 The arguments passed to the `.render()` method are:
 
-### `data`
+- `data`: the request data, as set by the `Response()` instantiation.
 
-The request data, as set by the `Response()` instantiation.
+- `accepted_media_type=None`: optional.  If provided, this is the accepted media type, as determined by the content negotiation stage. Depending on the client's `Accept:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters.  For example `"application/json; nested=true"`.
 
-### `accepted_media_type=None`
+- `renderer_context=None`: optional.  If provided, this is a dictionary of contextual information provided by the view. By default this will include the following keys: `view`, `request`, `response`, `args`, `kwargs`.
 
-Optional.  If provided, this is the accepted media type, as determined by the content negotiation stage.
-
-Depending on the client's `Accept:` header, this may be more specific than the renderer's `media_type` attribute, and may include media type parameters.  For example `"application/json; nested=true"`.
-
-### `renderer_context=None`
-
-Optional.  If provided, this is a dictionary of contextual information provided by the view.
-
-By default this will include the following keys: `view`, `request`, `response`, `args`, `kwargs`.
-
-## Example
+### Example
 
 The following is an example plaintext renderer that will return a response with the `data` parameter as the content of the response.
 
@@ -292,7 +282,7 @@ The following is an example plaintext renderer that will return a response with
         def render(self, data, accepted_media_type=None, renderer_context=None):
             return smart_str(data, encoding=self.charset)
 
-## Setting the character set
+### Setting the character set
 
 By default renderer classes are assumed to be using the `UTF-8` encoding.  To use a different encoding, set the `charset` attribute on the renderer.
 
@@ -321,7 +311,7 @@ In some cases you may also want to set the `render_style` attribute to `'binary'
 
 ---
 
-# Advanced renderer usage
+## Advanced renderer usage
 
 You can do some pretty flexible things using REST framework's renderers.  Some examples...
 
@@ -330,7 +320,7 @@ You can do some pretty flexible things using REST framework's renderers.  Some e
 * Specify multiple types of HTML representation for API clients to use.
 * Underspecify a renderer's media type, such as using `media_type = 'image/*'`, and use the `Accept` header to vary the encoding of the response.
 
-## Varying behavior by media type
+### Varying behavior by media type
 
 In some cases you might want your view to use different serialization styles depending on the accepted media type.  If you need to do this you can access `request.accepted_renderer` to determine the negotiated renderer that will be used for the response.
 
@@ -357,7 +347,7 @@ For example:
         data = serializer.data
         return Response(data)
 
-## Underspecifying the media type
+### Underspecifying the media type
 
 In some cases you might want a renderer to serve a range of media types.
 In this case you can underspecify the media types it should respond to, by using a `media_type` value such as `image/*`, or `*/*`.
@@ -366,7 +356,7 @@ If you underspecify the renderer's media type, you should make sure to specify t
 
     return Response(data, content_type='image/png')
 
-## Designing your media types
+### Designing your media types
 
 For the purposes of many Web APIs, simple `JSON` responses with hyperlinked relations may be sufficient.  If you want to fully embrace RESTful design and [HATEOAS] you'll need to consider the design and usage of your media types in more detail.
 
@@ -374,7 +364,7 @@ In [the words of Roy Fielding][quote], "A REST API should spend almost all of it
 
 For good examples of custom media types, see GitHub's use of a custom [application/vnd.github+json] media type, and Mike Amundsen's IANA approved [application/vnd.collection+json] JSON-based hypermedia.
 
-## HTML error views
+### HTML error views
 
 Typically a renderer will behave the same regardless of if it's dealing with a regular response, or with a response caused by an exception being raised, such as an `Http404` or `PermissionDenied` exception, or a subclass of `APIException`.
 
@@ -391,11 +381,11 @@ Templates will render with a `RequestContext` which includes the `status_code` a
 !!! note
     If `DEBUG=True`, Django's standard traceback error page will be displayed instead of rendering the HTTP status code and text.
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## YAML
+### YAML
 
 [REST framework YAML][rest-framework-yaml] provides [YAML][yaml] parsing and rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
@@ -416,7 +406,7 @@ Modify your REST framework settings.
         ],
     }
 
-## XML
+### XML
 
 [REST Framework XML][rest-framework-xml] provides a simple informal XML format. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
@@ -437,7 +427,7 @@ Modify your REST framework settings.
         ],
     }
 
-## JSONP
+### JSONP
 
 [REST framework JSONP][rest-framework-jsonp] provides JSONP rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.
 
@@ -460,11 +450,11 @@ Modify your REST framework settings.
         ],
     }
 
-## MessagePack
+### MessagePack
 
 [MessagePack][messagepack] is a fast, efficient binary serialization format.  [Juan Riaza][juanriaza] maintains the [djangorestframework-msgpack][djangorestframework-msgpack] package which provides MessagePack renderer and parser support for REST framework.
 
-## Microsoft Excel: XLSX (Binary Spreadsheet Endpoints)
+### Microsoft Excel: XLSX (Binary Spreadsheet Endpoints)
 
 XLSX is the world's most popular binary spreadsheet format. [Tim Allen][flipperpa] of [The Wharton School][wharton] maintains [drf-excel][drf-excel], which renders an endpoint as an XLSX spreadsheet using OpenPyXL, and allows the client to download it. Spreadsheets can be styled on a per-view basis.
 
@@ -501,23 +491,23 @@ To avoid having a file streamed without a filename (which the browser will often
         renderer_classes = [XLSXRenderer]
         filename = 'my_export.xlsx'
 
-## CSV
+### CSV
 
 Comma-separated values are a plain-text tabular data format, that can be easily imported into spreadsheet applications. [Mjumbe Poe][mjumbewu] maintains the [djangorestframework-csv][djangorestframework-csv] package which provides CSV renderer support for REST framework.
 
-## UltraJSON
+### UltraJSON
 
 [UltraJSON][ultrajson] is an optimized C JSON encoder which can give significantly faster JSON rendering. [Adam Mertz][Amertz08] maintains [drf_ujson2][drf_ujson2], a fork of the now unmaintained [drf-ujson-renderer][drf-ujson-renderer], which implements JSON rendering using the UJSON package.
 
-## CamelCase JSON
+### CamelCase JSON
 
 [djangorestframework-camel-case] provides camel case JSON renderers and parsers for REST framework.  This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names.  It is maintained by [Vitaly Babiy][vbabiy].
 
-## Pandas (CSV, Excel, PNG)
+### Pandas (CSV, Excel, PNG)
 
 [Django REST Pandas] provides a serializer and renderers that support additional data processing and output via the [Pandas] DataFrame API.  Django REST Pandas includes renderers for Pandas-style CSV files, Excel workbooks (both `.xls` and `.xlsx`), and a number of [other formats]. It is maintained by [S. Andrew Sheppard][sheppard] as part of the [wq Project][wq].
 
-## LaTeX
+### LaTeX
 
 [Rest Framework Latex] provides a renderer that outputs PDFs using Lualatex. It is maintained by [Pebble (S/F Software)][mypebble].
```


 - `.reference/api-guide/metadata.md`
```
e045dc465270c18689dba4a970378cd9744e57b6 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -80,13 +80,13 @@ There are a couple of reasons that you might choose to take this approach, inclu
 
 ---
 
-# Custom metadata classes
+## Custom metadata classes
 
 If you want to provide a custom metadata class you should override `BaseMetadata` and implement the `determine_metadata(self, request, view)` method.
 
 Useful things that you might want to do could include returning schema information, using a format such as [JSON schema][json-schema], or returning debug information to admin users.
 
-## Example
+### Example
 
 The following class could be used to limit the information that is returned to `OPTIONS` requests.
 
@@ -107,11 +107,11 @@ Then configure your settings to use this custom class:
         'DEFAULT_METADATA_CLASS': 'myproject.apps.core.MinimalMetadata'
     }
 
-# Third party packages
+## Third party packages
 
 The following third party packages provide additional metadata implementations.
 
-## DRF-schema-adapter
+### DRF-schema-adapter
 
 [drf-schema-adapter][drf-schema-adapter] is a set of tools that makes it easier to provide schema information to frontend frameworks and libraries. It provides a metadata mixin as well as 2 metadata classes and several adapters suitable to generate [json-schema][json-schema] as well as schema information readable by various libraries.
```


 - `.reference/api-guide/versioning.md`
```
0d6589cf45940bb67ace74a06b2c5b053f1c31ef -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -21,7 +21,7 @@ When API versioning is enabled, the `request.version` attribute will contain a s
 
 By default, versioning is not enabled, and `request.version` will always return `None`.
 
-#### Varying behavior based on the version
+### Varying behavior based on the version
 
 How you vary the API behavior is up to you, but one example you might typically want is to switch to a different serialization style in a newer version. For example:
 
@@ -30,7 +30,7 @@ How you vary the API behavior is up to you, but one example you might typically
             return AccountSerializerVersion1
         return AccountSerializer
 
-#### Reversing URLs for versioned APIs
+### Reversing URLs for versioned APIs
 
 The `reverse` function included by REST framework ties in with the versioning scheme. You need to make sure to include the current `request` as a keyword argument, like so.
 
@@ -43,7 +43,7 @@ The above function will apply any URL transformations appropriate to the request
 * If `NamespaceVersioning` was being used, and the API version was 'v1', then the URL lookup used would be `'v1:bookings-list'`, which might resolve to a URL like `http://example.org/v1/bookings/`.
 * If `QueryParameterVersioning` was being used, and the API version was `1.0`, then the returned URL might be something like `http://example.org/bookings/?version=1.0`
 
-#### Versioned APIs and hyperlinked serializers
+### Versioned APIs and hyperlinked serializers
 
 When using hyperlinked serialization styles together with a URL based versioning scheme make sure to include the request as context to the serializer.
 
@@ -69,7 +69,7 @@ You can also set the versioning scheme on an individual view. Typically you won'
     class ProfileList(APIView):
         versioning_class = versioning.QueryParameterVersioning
 
-#### Other versioning settings
+### Other versioning settings
 
 The following settings keys are also used to control versioning:
 
@@ -92,9 +92,9 @@ You can also set your versioning class plus those three values on a per-view or
 
 ---
 
-# API Reference
+## API Reference
 
-## AcceptHeaderVersioning
+### AcceptHeaderVersioning
 
 This scheme requires the client to specify the version as part of the media type in the `Accept` header. The version is included as a media type parameter, that supplements the main media type.
 
@@ -121,7 +121,7 @@ Your client requests would now look like this:
     Host: example.com
     Accept: application/vnd.megacorp.bookings+json; version=1.0
 
-## URLPathVersioning
+### URLPathVersioning
 
 This scheme requires the client to specify the version as part of the URL path.
 
@@ -144,7 +144,7 @@ Your URL conf must include a pattern that matches the version with a `'version'`
         )
     ]
 
-## NamespaceVersioning
+### NamespaceVersioning
 
 To the client, this scheme is the same as `URLPathVersioning`. The only difference is how it is configured in your Django application, as it uses URL namespacing, instead of URL keyword arguments.
 
@@ -170,7 +170,7 @@ In the following example we're giving a set of views two different possible URL
 
 Both `URLPathVersioning` and `NamespaceVersioning` are reasonable if you just need a simple versioning scheme. The `URLPathVersioning` approach might be better suitable for small ad-hoc projects, and the `NamespaceVersioning` is probably easier to manage for larger projects.
 
-## HostNameVersioning
+### HostNameVersioning
 
 The hostname versioning scheme requires the client to specify the requested version as part of the hostname in the URL.
 
@@ -190,7 +190,7 @@ The `HostNameVersioning` scheme can be awkward to use in debug mode as you will
 
 Hostname based versioning can be particularly useful if you have requirements to route incoming requests to different servers based on the version, as you can configure different DNS records for different API versions.
 
-## QueryParameterVersioning
+### QueryParameterVersioning
 
 This scheme is a simple style that includes the version as a query parameter in the URL. For example:
 
@@ -200,11 +200,11 @@ This scheme is a simple style that includes the version as a query parameter in
 
 ---
 
-# Custom versioning schemes
+## Custom versioning schemes
 
 To implement a custom versioning scheme, subclass `BaseVersioning` and override the `.determine_version` method.
 
-## Example
+### Example
 
 The following example uses a custom `X-API-Version` header to determine the requested version.
```


 - `.reference/api-guide/responses.md`
```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -19,9 +19,9 @@ Unless you want to heavily customize REST framework for some reason, you should
 
 ---
 
-# Creating responses
+## Creating responses
 
-## Response()
+### Response()
 
 **Signature:** `Response(data, status=None, template_name=None, headers=None, content_type=None)`
 
@@ -41,37 +41,37 @@ Arguments:
 
 ---
 
-# Attributes
+## Attributes
 
-## .data
+### .data
 
 The unrendered, serialized data of the response.
 
-## .status_code
+### .status_code
 
 The numeric status code of the HTTP response.
 
-## .content
+### .content
 
 The rendered content of the response.  The `.render()` method must have been called before `.content` can be accessed.
 
-## .template_name
+### .template_name
 
 The `template_name`, if supplied.  Only required if `HTMLRenderer` or some other custom template renderer is the accepted renderer for the response.
 
-## .accepted_renderer
+### .accepted_renderer
 
 The renderer instance that will be used to render the response.
 
 Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.
 
-## .accepted_media_type
+### .accepted_media_type
 
 The media type that was selected by the content negotiation stage.
 
 Set automatically by the `APIView` or `@api_view` immediately before the response is returned from the view.
 
-## .renderer_context
+### .renderer_context
 
 A dictionary of additional context information that will be passed to the renderer's `.render()` method.
 
@@ -79,14 +79,14 @@ Set automatically by the `APIView` or `@api_view` immediately before the respons
 
 ---
 
-# Standard HttpResponse attributes
+## Standard HttpResponse attributes
 
 The `Response` class extends `SimpleTemplateResponse`, and all the usual attributes and methods are also available on the response.  For example you can set headers on the response in the standard way:
 
     response = Response()
     response['Cache-Control'] = 'no-cache'
 
-## .render()
+### .render()
 
 **Signature:** `.render()`
```


 - `.reference/api-guide/requests.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -3,8 +3,6 @@ source:
     - request.py
 ---
 
-# Requests
-
 > If you're doing REST-based web service stuff ... you should ignore request.POST.
 >
 > &mdash; Malcom Tredinnick, [Django developers group][cite]
@@ -13,11 +11,11 @@ REST framework's `Request` class extends the standard `HttpRequest`, adding supp
 
 ---
 
-# Request parsing
+## Request parsing
 
 REST framework's Request objects provide flexible request parsing that allows you to treat requests with JSON data or other media types in the same way that you would normally deal with form data.
 
-## .data
+### .data
 
 `request.data` returns the parsed content of the request body.  This is similar to the standard `request.POST` and `request.FILES` attributes except that:
 
@@ -27,13 +25,13 @@ REST framework's Request objects provide flexible request parsing that allows yo
 
 For more details see the [parsers documentation].
 
-## .query_params
+### .query_params
 
 `request.query_params` is a more correctly named synonym for `request.GET`.
 
 For clarity inside your code, we recommend using `request.query_params` instead of the Django's standard `request.GET`. Doing so will help keep your codebase more correct and obvious - any HTTP method type may include query parameters, not just `GET` requests.
 
-## .parsers
+### .parsers
 
 The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Parser` instances, based on the `parser_classes` set on the view or based on the `DEFAULT_PARSER_CLASSES` setting.
 
@@ -44,21 +42,21 @@ You won't typically need to access this property.
 
     If a client sends a request with a content-type that cannot be parsed then a `UnsupportedMediaType` exception will be raised, which by default will be caught and return a `415 Unsupported Media Type` response.
 
-# Content negotiation
+## Content negotiation
 
 The request exposes some properties that allow you to determine the result of the content negotiation stage. This allows you to implement behavior such as selecting a different serialization schemes for different media types.
 
-## .accepted_renderer
+### .accepted_renderer
 
 The renderer instance that was selected by the content negotiation stage.
 
-## .accepted_media_type
+### .accepted_media_type
 
 A string representing the media type that was accepted by the content negotiation stage.
 
 ---
 
-# Authentication
+## Authentication
 
 REST framework provides flexible, per-request authentication, that gives you the ability to:
 
@@ -66,7 +64,7 @@ REST framework provides flexible, per-request authentication, that gives you the
 * Support the use of multiple authentication policies.
 * Provide both user and token information associated with the incoming request.
 
-## .user
+### .user
 
 `request.user` typically returns an instance of `django.contrib.auth.models.User`, although the behavior depends on the authentication policy being used.
 
@@ -74,7 +72,7 @@ If the request is unauthenticated the default value of `request.user` is an inst
 
 For more details see the [authentication documentation].
 
-## .auth
+### .auth
 
 `request.auth` returns any additional authentication context.  The exact behavior of `request.auth` depends on the authentication policy being used, but it may typically be an instance of the token that the request was authenticated against.
 
@@ -82,7 +80,7 @@ If the request is unauthenticated, or if no additional context is present, the d
 
 For more details see the [authentication documentation].
 
-## .authenticators
+### .authenticators
 
 The `APIView` class or `@api_view` decorator will ensure that this property is automatically set to a list of `Authentication` instances, based on the `authentication_classes` set on the view or based on the `DEFAULT_AUTHENTICATORS` setting.
 
@@ -91,11 +89,11 @@ You won't typically need to access this property.
 !!! note
     You may see a `WrappedAttributeError` raised when calling the `.user` or `.auth` properties. These errors originate from an authenticator as a standard `AttributeError`, however it's necessary that they be re-raised as a different exception type in order to prevent them from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from the authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. The authenticator will need to be fixed.
 
-# Browser enhancements
+## Browser enhancements
 
 REST framework supports a few browser enhancements such as browser-based `PUT`, `PATCH` and `DELETE` forms.
 
-## .method
+### .method
 
 `request.method` returns the **uppercased** string representation of the request's HTTP method.
 
@@ -103,7 +101,7 @@ Browser-based `PUT`, `PATCH` and `DELETE` forms are transparently supported.
 
 For more information see the [browser enhancements documentation].
 
-## .content_type
+### .content_type
 
 `request.content_type`, returns a string object representing the media type of the HTTP request's body, or an empty string if no media type was provided.
 
@@ -113,7 +111,7 @@ If you do need to access the content type of the request you should use the `.co
 
 For more information see the [browser enhancements documentation].
 
-## .stream
+### .stream
 
 `request.stream` returns a stream representing the content of the request body.
 
@@ -121,7 +119,7 @@ You won't typically need to directly access the request's content, as you'll nor
 
 ---
 
-# Standard HttpRequest attributes
+## Standard HttpRequest attributes
 
 As REST framework's `Request` extends Django's `HttpRequest`, all the other standard attributes and methods are also available.  For example the `request.META` and `request.session` dictionaries are available as normal.
```


 - `.reference/api-guide/permissions.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -138,35 +138,38 @@ Provided they inherit from `rest_framework.permissions.BasePermission`, permissi
             return Response(content)
 
 !!! note
-    Composition of permissions supports `&` (and), `|` (or) and `~` (not) operators.
+    Composition of permissions supports the `&` (and), `|` (or) and `~` (not) operators, and also allows the use of brackets `(` `)` to group expressions.
 
-# API Reference
+    Operators follow the same precedence and associativity rules as standard logical operators (`~` highest, then `&`, then `|`).
 
-## AllowAny
+
+## API Reference
+
+### AllowAny
 
 The `AllowAny` permission class will allow unrestricted access, **regardless of if the request was authenticated or unauthenticated**.
 
 This permission is not strictly required, since you can achieve the same result by using an empty list or tuple for the permissions setting, but you may find it useful to specify this class because it makes the intention explicit.
 
-## IsAuthenticated
+### IsAuthenticated
 
 The `IsAuthenticated` permission class will deny permission to any unauthenticated user, and allow permission otherwise.
 
 This permission is suitable if you want your API to only be accessible to registered users.
 
-## IsAdminUser
+### IsAdminUser
 
 The `IsAdminUser` permission class will deny permission to any user, unless `user.is_staff` is `True` in which case permission will be allowed.
 
 This permission is suitable if you want your API to only be accessible to a subset of trusted administrators.
 
-## IsAuthenticatedOrReadOnly
+### IsAuthenticatedOrReadOnly
 
 The `IsAuthenticatedOrReadOnly` will allow authenticated users to perform any request.  Requests for unauthenticated users will only be permitted if the request method is one of the "safe" methods; `GET`, `HEAD` or `OPTIONS`.
 
 This permission is suitable if you want to your API to allow read permissions to anonymous users, and only allow write permissions to authenticated users.
 
-## DjangoModelPermissions
+### DjangoModelPermissions
 
 This permission class ties into Django's standard `django.contrib.auth` [model permissions][contribauth].  This permission must only be applied to views that have a `.queryset` property or `get_queryset()` method. Authorization will only be granted if the user *is authenticated* and has the *relevant model permissions* assigned. The appropriate model is determined by checking `get_queryset().model` or `queryset.model`.
 
@@ -178,11 +181,11 @@ The default behavior can also be overridden to support custom model permissions.
 
 To use custom model permissions, override `DjangoModelPermissions` and set the `.perms_map` property.  Refer to the source code for details.
 
-## DjangoModelPermissionsOrAnonReadOnly
+### DjangoModelPermissionsOrAnonReadOnly
 
 Similar to `DjangoModelPermissions`, but also allows unauthenticated users to have read-only access to the API.
 
-## DjangoObjectPermissions
+### DjangoObjectPermissions
 
 This permission class ties into Django's standard [object permissions framework][objectpermissions] that allows per-object permissions on models.  In order to use this permission class, you'll also need to add a permission backend that supports object-level permissions, such as [django-guardian][guardian].
 
@@ -199,7 +202,7 @@ As with `DjangoModelPermissions` you can use custom model permissions by overrid
 !!! note
     If you need object level `view` permissions for `GET`, `HEAD` and `OPTIONS` requests and are using django-guardian for your object-level permissions backend, you'll want to consider using the `DjangoObjectPermissionsFilter` class provided by the [`djangorestframework-guardian` package][django-rest-framework-guardian]. It ensures that list endpoints only return results including objects for which the user has appropriate view permissions.
 
-# Custom permissions
+## Custom permissions
 
 To implement a custom permission, override `BasePermission` and implement either, or both, of the following methods:
 
@@ -228,7 +231,7 @@ Custom permissions will raise a `PermissionDenied` exception if the test fails.
         def has_permission(self, request, view):
              ...
 
-## Examples
+### Examples
 
 The following is an example of a permission class that checks the incoming request's IP address against a blocklist, and denies the request if the IP has been blocked.
 
@@ -265,7 +268,7 @@ Note that the generic views will check the appropriate object level permissions,
 
 Also note that the generic views will only check the object-level permissions for views that retrieve a single model instance.  If you require object-level filtering of list views, you'll need to filter the queryset separately.  See the [filtering documentation][filtering] for more details.
 
-# Overview of access restriction methods
+## Overview of access restriction methods
 
 REST framework offers three different methods to customize access restrictions on a case-by-case basis. These apply in different scenarios and have different effects and limitations.
 
@@ -291,47 +294,47 @@ The following table lists the access restriction methods and the level of contro
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## DRF - Access Policy
+### DRF - Access Policy
 
 The [Django REST - Access Policy][drf-access-policy] package provides a way to define complex access rules in declarative policy classes that are attached to view sets or function-based views. The policies are defined in JSON in a format similar to AWS' Identity & Access Management policies. 
 
-## Composed Permissions
+### Composed Permissions
 
 The [Composed Permissions][composed-permissions] package provides a simple way to define complex and multi-depth (with logic operators) permission objects, using small and reusable components.
 
-## REST Condition
+### REST Condition
 
 The [REST Condition][rest-condition] package is another extension for building complex permissions in a simple and convenient way. The extension allows you to combine permissions with logical operators.
 
-## DRY Rest Permissions
+### DRY Rest Permissions
 
 The [DRY Rest Permissions][dry-rest-permissions] package provides the ability to define different permissions for individual default and custom actions. This package is made for apps with permissions that are derived from relationships defined in the app's data model. It also supports permission checks being returned to a client app through the API's serializer. Additionally it supports adding permissions to the default and custom list actions to restrict the data they retrieve per user.
 
-## Django Rest Framework Roles
+### Django Rest Framework Roles
 
 The [Django Rest Framework Roles][django-rest-framework-roles] package makes it easier to parameterize your API over multiple types of users.
 
-## Rest Framework Roles
+### Rest Framework Roles
 
 The [Rest Framework Roles][rest-framework-roles] makes it super easy to protect views based on roles. Most importantly allows you to decouple accessibility logic from models and views in a clean human-readable way.
 
-## Django REST Framework API Key
+### Django REST Framework API Key
 
 The [Django REST Framework API Key][djangorestframework-api-key] package provides permissions classes, models and helpers to add API key authorization to your API. It can be used to authorize internal or third-party backends and services (i.e. _machines_) which do not have a user account. API keys are stored securely using Django's password hashing infrastructure, and they can be viewed, edited and revoked at anytime in the Django admin.
 
-## Django Rest Framework Role Filters
+### Django Rest Framework Role Filters
 
 The [Django Rest Framework Role Filters][django-rest-framework-role-filters] package provides simple filtering over multiple types of roles.
 
-## Django Rest Framework PSQ
+### Django Rest Framework PSQ
 
 The [Django Rest Framework PSQ][drf-psq] package is an extension that gives support for having action-based **permission_classes**, **serializer_class**, and **queryset** dependent on permission-based rules.
 
-## Axioms DRF PY
+### Axioms DRF PY
 
 The [Axioms DRF PY][axioms-drf-py] package is an extension that provides support for authentication and claim-based fine-grained authorization (**scopes**, **roles**, **groups**, **permissions**, etc. including object-level checks) using JWT tokens issued by an OAuth2/OIDC Authorization Server including AWS Cognito, Auth0, Okta, Microsoft Entra, etc.
```


 - `.reference/api-guide/viewsets.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -48,7 +48,11 @@ If we need to, we can bind this viewset into two separate views, like so:
     user_list = UserViewSet.as_view({'get': 'list'})
     user_detail = UserViewSet.as_view({'get': 'retrieve'})
 
-Typically we wouldn't do this, but would instead register the viewset with a router, and allow the urlconf to be automatically generated.
+!!! warning
+    Do not use `.as_view()` with `@action` methods. It bypasses router setup and may ignore action settings like `permission_classes`. Use `DefaultRouter` for actions.
+
+
+Typically, we wouldn't do this, but would instead register the viewset with a router, and allow the urlconf to be automatically generated.
 
     from myapp.views import UserViewSet
     from rest_framework.routers import DefaultRouter
@@ -58,7 +62,7 @@ Typically we wouldn't do this, but would instead register the viewset with a rou
     urlpatterns = router.urls
 
 !!! warning
-    Do not use `.as_view()` with `@action` methods. It bypasses router setup and may ignore action settings like `permission_classes`. Use `DefaultRouter` for actions.
+    When registering viewsets, do not include a trailing slash in the prefix (e.g., use `r'users'`, not `r'users/'`). Unlike standard Django URL patterns, DRF routers append slashes automatically based on your trailing slash configuration.
 
 Rather than writing your own viewsets, you'll often want to use the existing base classes that provide a default set of behavior.  For example:
 
@@ -243,21 +247,21 @@ The `url_name` argument for `.reverse_action()` should match the same argument t
 
 ---
 
-# API Reference
+## API Reference
 
-## ViewSet
+### ViewSet
 
 The `ViewSet` class inherits from `APIView`.  You can use any of the standard attributes such as `permission_classes`, `authentication_classes` in order to control the API policy on the viewset.
 
 The `ViewSet` class does not provide any implementations of actions.  In order to use a `ViewSet` class you'll override the class and define the action implementations explicitly.
 
-## GenericViewSet
+### GenericViewSet
 
 The `GenericViewSet` class inherits from `GenericAPIView`, and provides the default set of `get_object`, `get_queryset` methods and other generic view base behavior, but does not include any actions by default.
 
 In order to use a `GenericViewSet` class you'll override the class and either mixin the required mixin classes, or define the action implementations explicitly.
 
-## ModelViewSet
+### ModelViewSet
 
 The `ModelViewSet` class inherits from `GenericAPIView` and includes implementations for various actions, by mixing in the behavior of the various mixin classes.
 
@@ -292,7 +296,7 @@ Note however that upon removal of the `queryset` property from your `ViewSet`, a
 
 Also note that although this class provides the complete set of create/list/retrieve/update/destroy actions by default, you can restrict the available operations by using the standard permission classes.
 
-## ReadOnlyModelViewSet
+### ReadOnlyModelViewSet
 
 The `ReadOnlyModelViewSet` class also inherits from `GenericAPIView`.  As with `ModelViewSet` it also includes implementations for various actions, but unlike `ModelViewSet` only provides the 'read-only' actions, `.list()` and `.retrieve()`.
 
@@ -309,11 +313,11 @@ As with `ModelViewSet`, you'll normally need to provide at least the `queryset`
 
 Again, as with `ModelViewSet`, you can use any of the standard attributes and method overrides available to `GenericAPIView`.
 
-# Custom ViewSet base classes
+## Custom ViewSet base classes
 
 You may need to provide custom `ViewSet` classes that do not have the full set of `ModelViewSet` actions, or that customize the behavior in some other way.
 
-## Example
+### Example
 
 To create a base viewset class that provides `create`, `list` and `retrieve` operations, inherit from `GenericViewSet`, and mixin the required actions:
```


 - `.reference/api-guide/authentication.md`
```
d0a5d5e7cad7f1032b4d0a36cab1596076f705ad -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -3,8 +3,6 @@ source:
     - authentication.py
 ---
 
-# Authentication
-
 > Auth needs to be pluggable.
 >
 > &mdash; Jacob Kaplan-Moss, ["REST worst practices"][cite]
@@ -89,7 +87,7 @@ Note that when a request may successfully authenticate, but still be denied perm
 
 ## Django 5.1+ `LoginRequiredMiddleware`
 
-If you're running Django 5.1+ and use the [`LoginRequiredMiddleware`][login-required-middleware], please note that all views from DRF are opted-out of this middleware.  This is because the authentication in DRF is based authentication and permissions classes, which may be determined after the middleware has been applied.  Additionally, when the request is not authenticated, the middleware redirects the user to the login page, which is not suitable for API requests, where it's preferable to return a 401 status code.
+If you're running Django 5.1+ and use the [`LoginRequiredMiddleware`][login-required-middleware], please note that all views from DRF are opted-out of this middleware.  This is because the authentication in DRF is based on authentication and permissions classes, which may be determined after the middleware has been applied.  Additionally, when the request is not authenticated, the middleware redirects the user to the login page, which is not suitable for API requests, where it's preferable to return a 401 status code.
 
 REST framework offers an equivalent mechanism for DRF views via the global settings, `DEFAULT_AUTHENTICATION_CLASSES` and `DEFAULT_PERMISSION_CLASSES`.  They should be changed accordingly if you need to enforce that API requests are logged in.
 
@@ -104,9 +102,9 @@ If you are deploying to Apache, and using any non-session based authentication,
 
 ---
 
-# API Reference
+## API Reference
 
-## BasicAuthentication
+### BasicAuthentication
 
 This authentication scheme uses [HTTP Basic Authentication][basicauth], signed against a user's username and password.  Basic authentication is generally only appropriate for testing.
 
@@ -122,7 +120,7 @@ Unauthenticated responses that are denied permission will result in an `HTTP 401
 !!! note
     If you use `BasicAuthentication` in production you must ensure that your API is only available over `https`.  You should also ensure that your API clients will always re-request the username and password at login, and will never store those details to persistent storage.
 
-## TokenAuthentication
+### TokenAuthentication
 
 !!! note
     The token authentication provided by Django REST framework is a fairly simple implementation.
@@ -171,9 +169,9 @@ The `curl` command line tool may be useful for testing token authenticated APIs.
 !!! note
     If you use `TokenAuthentication` in production you must ensure that your API is only available over `https`.
 
-### Generating Tokens
+#### Generating Tokens
 
-#### By using signals
+##### By using signals
 
 If you want every user to have an automatically generated Token, you can simply catch the User's `post_save` signal.
 
@@ -197,7 +195,7 @@ If you've already created some users, you can generate tokens for all existing u
     for user in User.objects.all():
         Token.objects.get_or_create(user=user)
 
-#### By exposing an api endpoint
+##### By exposing an api endpoint
 
 When using `TokenAuthentication`, you may want to provide a mechanism for clients to obtain a token given the username and password.  REST framework provides a built-in view to provide this behavior.  To use it, add the `obtain_auth_token` view to your URLconf:
 
@@ -246,7 +244,7 @@ And in your `urls.py`:
     ]
 
 
-#### With Django admin
+##### With Django admin
 
 It is also possible to create Tokens manually through the admin interface. In case you are using a large user base, we recommend that you monkey patch the `TokenAdmin` class to customize it to your needs, more specifically by declaring the `user` field as `raw_field`.
 
@@ -257,7 +255,7 @@ It is also possible to create Tokens manually through the admin interface. In ca
     TokenAdmin.raw_id_fields = ['user']
 
 
-#### Using Django manage.py command
+##### Using Django manage.py command
 
 Since version 3.6.4 it's possible to generate a user token using the following command:
 
@@ -272,7 +270,7 @@ In case you want to regenerate the token (for example if it has been compromised
     ./manage.py drf_create_token -r <username>
 
 
-## SessionAuthentication
+### SessionAuthentication
 
 This authentication scheme uses Django's default session backend for authentication.  Session authentication is appropriate for AJAX clients that are running in the same session context as your website.
 
@@ -291,7 +289,7 @@ If you're using an AJAX-style API with SessionAuthentication, you'll need to mak
 CSRF validation in REST framework works slightly differently from standard Django due to the need to support both session and non-session based authentication to the same views. This means that only authenticated requests require CSRF tokens, and anonymous requests may be sent without CSRF tokens. This behavior is not suitable for login views, which should always have CSRF validation applied.
 
 
-## RemoteUserAuthentication
+### RemoteUserAuthentication
 
 This authentication scheme allows you to delegate authentication to your web server, which sets the `REMOTE_USER`
 environment variable.
@@ -312,7 +310,7 @@ Consult your web server's documentation for information about configuring an aut
 * [NGINX (Restricting Access)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)
 
 
-# Custom authentication
+## Custom authentication
 
 To implement a custom authentication scheme, subclass `BaseAuthentication` and override the `.authenticate(self, request)` method.  The method should return a two-tuple of `(user, auth)` if authentication succeeds, or `None` otherwise.
 
@@ -330,7 +328,7 @@ If the `.authenticate_header()` method is not overridden, the authentication sch
 !!! note
     When your custom authenticator is invoked by the request object's `.user` or `.auth` properties, you may see an `AttributeError` re-raised as a `WrappedAttributeError`. This is necessary to prevent the original exception from being suppressed by the outer property access. Python will not recognize that the `AttributeError` originates from your custom authenticator and will instead assume that the request object does not have a `.user` or `.auth` property. These errors should be fixed or otherwise handled by your authenticator.
 
-## Example
+### Example
 
 The following example will authenticate any incoming request as the user given by the username in a custom request header named 'X-USERNAME'.
 
@@ -353,19 +351,19 @@ The following example will authenticate any incoming request as the user given b
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third-party packages are also available.
 
-## django-rest-knox
+### django-rest-knox
 
 [Django-rest-knox][django-rest-knox] library provides models and views to handle token-based authentication in a more secure and extensible way than the built-in TokenAuthentication scheme - with Single Page Applications and Mobile clients in mind. It provides per-client tokens, and views to generate them when provided some other authentication (usually basic authentication), to delete the token (providing a server enforced logout) and to delete all tokens (logs out all clients that a user is logged into).
 
-## Django OAuth Toolkit
+### Django OAuth Toolkit
 
 The [Django OAuth Toolkit][django-oauth-toolkit] package provides OAuth 2.0 support and works with Python 3.4+. The package is maintained by [jazzband][jazzband] and uses the excellent [OAuthLib][oauthlib].  The package is well documented, and well supported and is currently our **recommended package for OAuth 2.0 support**.
 
-### Installation & configuration
+#### Installation & configuration
 
 Install using `pip`.
 
@@ -386,13 +384,13 @@ Add the package to your `INSTALLED_APPS` and modify your REST framework settings
 
 For more details see the [Django REST framework - Getting started][django-oauth-toolkit-getting-started] documentation.
 
-## Django REST framework OAuth
+### Django REST framework OAuth
 
 The [Django REST framework OAuth][django-rest-framework-oauth] package provides both OAuth1 and OAuth2 support for REST framework.
 
 This package was previously included directly in the REST framework but is now supported and maintained as a third-party package.
 
-### Installation & configuration
+#### Installation & configuration
 
 Install the package using `pip`.
 
@@ -400,28 +398,28 @@ Install the package using `pip`.
 
 For details on configuration and usage see the Django REST framework OAuth documentation for [authentication][django-rest-framework-oauth-authentication] and [permissions][django-rest-framework-oauth-permissions].
 
-## JSON Web Token Authentication
+### JSON Web Token Authentication
 
 JSON Web Token is a fairly new standard which can be used for token-based authentication. Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is [djangorestframework-simplejwt][djangorestframework-simplejwt] which provides some features as well as a pluggable token blacklist app.
 
-## Hawk HTTP Authentication
+### Hawk HTTP Authentication
 
 The [HawkREST][hawkrest] library builds on the [Mohawk][mohawk] library to let you work with [Hawk][hawk] signed requests and responses in your API. [Hawk][hawk] lets two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication][mac] (which was based on parts of [OAuth 1.0][oauth-1.0a]).
 
-## HTTP Signature Authentication
+### HTTP Signature Authentication
 
 HTTP Signature (currently a [IETF draft][http-signature-ietf-draft]) provides a way to achieve origin authentication and message integrity for HTTP messages. Similar to [Amazon's HTTP Signature scheme][amazon-http-signature], used by many of its services, it permits stateless, per-request authentication. [Elvio Toccalino][etoccalino] maintains the [djangorestframework-httpsignature][djangorestframework-httpsignature] (outdated) package which provides an easy-to-use HTTP Signature Authentication mechanism. You can use the updated fork version of [djangorestframework-httpsignature][djangorestframework-httpsignature], which is [drf-httpsig][drf-httpsig].
 
-## Djoser
+### Djoser
 
 [Djoser][djoser] library provides a set of views to handle basic actions such as registration, login, logout, password reset and account activation. The package works with a custom user model and uses token-based authentication. This is a ready to use REST implementation of the Django authentication system.
 
-## DRF Auth Kit
+### DRF Auth Kit
 
 [DRF Auth Kit][drf-auth-kit] library provides a modern REST authentication solution with JWT cookies, social login, multi-factor authentication, and comprehensive user management. The package offers full type safety, automatic OpenAPI schema generation with DRF Spectacular. It supports multiple authentication types (JWT, DRF Token, or Custom) and includes built-in internationalization for 50+ languages.
 
 
-## django-rest-auth / dj-rest-auth
+### django-rest-auth / dj-rest-auth
 
 This library provides a set of REST API endpoints for registration, authentication (including social media authentication), password reset, retrieve and update user details, etc. By having these API endpoints, your client apps such as AngularJS, iOS, Android, and others can communicate to your Django backend site independently via REST APIs for user management.
 
@@ -431,25 +429,25 @@ There are currently two forks of this project.
 * [Django-rest-auth][django-rest-auth] is the original project, [but is not currently receiving updates](https://github.com/Tivix/django-rest-auth/issues/568).
 * [Dj-rest-auth][dj-rest-auth] is a newer fork of the project.
 
-## drf-social-oauth2
+### drf-social-oauth2
 
 [Drf-social-oauth2][drf-social-oauth2] is a framework that helps you authenticate with major social oauth2 vendors, such as Facebook, Google, Twitter, Orcid, etc. It generates tokens in a JWTed way with an easy setup.
 
-## drfpasswordless
+### drfpasswordless
 
 [drfpasswordless][drfpasswordless] adds (Medium, Square Cash inspired) passwordless support to Django REST Framework's TokenAuthentication scheme. Users log in and sign up with a token sent to a contact point like an email address or a mobile number.
 
-## django-rest-authemail
+### django-rest-authemail
 
 [django-rest-authemail][django-rest-authemail] provides a RESTful API interface for user signup and authentication. Email addresses are used for authentication, rather than usernames.  API endpoints are available for signup, signup email verification, login, logout, password reset, password reset verification, email change, email change verification, password change, and user detail.  A fully functional example project and detailed instructions are included.
 
-## Django-Rest-Durin
+### Django-Rest-Durin
 
 [Django-Rest-Durin][django-rest-durin] is built with the idea to have one library that does token auth for multiple Web/CLI/Mobile API clients via one interface but allows different token configuration for each API Client that consumes the API. It provides support for multiple tokens per user via custom models, views, permissions that work with Django-Rest-Framework. The token expiration time can be different per API client and is customizable via the Django Admin Interface.
 
 More information can be found in the [Documentation](https://django-rest-durin.readthedocs.io/en/latest/index.html).
 
-## django-pyoidc
+### django-pyoidc
 
 [django_pyoidc][django-pyoidc] adds support for OpenID Connect (OIDC) authentication. This allows you to delegate user management to an Identity Provider, which can be used to implement Single-Sign-On (SSO). It provides support for most uses-cases, such as customizing how token info are mapped to user models, using OIDC audiences for access control, etc.
```


 - `.reference/api-guide/pagination.md`
```
f74a44e850a685ac73c819ae7b96b0d68a8f734f -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -64,9 +64,9 @@ Or apply the style globally, using the `DEFAULT_PAGINATION_CLASS` settings key.
 
 ---
 
-# API Reference
+## API Reference
 
-## PageNumberPagination
+### PageNumberPagination
 
 This pagination style accepts a single number page number in the request query parameters.
 
@@ -97,6 +97,18 @@ To enable the `PageNumberPagination` style globally, use the following configura
 
 On `GenericAPIView` subclasses you may also set the `pagination_class` attribute to select `PageNumberPagination` on a per-view basis.
 
+By default, the query parameter name used for pagination is `page`.
+This can be customized by subclassing `PageNumberPagination` and overriding the `page_query_param` attribute.
+
+For example:
+
+    from rest_framework.pagination import PageNumberPagination
+
+    class CustomPagination(PageNumberPagination):
+        page_query_param = 'p'
+
+With this configuration, clients would request pages using `?p=2` instead of `?page=2`.
+
 #### Configuration
 
 The `PageNumberPagination` class includes a number of attributes that may be overridden to modify the pagination style.
@@ -113,7 +125,7 @@ To set these attributes you should override the `PageNumberPagination` class, an
 
 ---
 
-## LimitOffsetPagination
+### LimitOffsetPagination
 
 This pagination style mirrors the syntax used when looking up multiple database records. The client includes both a "limit" and an
 "offset" query parameter. The limit indicates the maximum number of items to return, and is equivalent to the `page_size` in other styles. The offset indicates the starting position of the query in relation to the complete set of unpaginated items.
@@ -160,7 +172,7 @@ To set these attributes you should override the `LimitOffsetPagination` class, a
 
 ---
 
-## CursorPagination
+### CursorPagination
 
 The cursor-based pagination presents an opaque "cursor" indicator that the client may use to page through the result set. This pagination style only presents forward and reverse controls, and does not allow the client to navigate to arbitrary positions.
 
@@ -216,7 +228,7 @@ To set these attributes you should override the `CursorPagination` class, and th
 
 ---
 
-# Custom pagination styles
+## Custom pagination styles
 
 To create a custom pagination serializer class, you should inherit the subclass `pagination.BasePagination`, override the `paginate_queryset(self, queryset, request, view=None)`, and `get_paginated_response(self, data)` methods:
 
@@ -225,7 +237,7 @@ To create a custom pagination serializer class, you should inherit the subclass
 
 Note that the `paginate_queryset` method may set state on the pagination instance, that may later be used by the `get_paginated_response` method.
 
-## Example
+### Example
 
 Suppose we want to replace the default pagination output style with a modified format that includes the next and previous links under in a nested 'links' key. We could specify a custom pagination class like so:
 
@@ -249,7 +261,7 @@ We'd then need to set up the custom class in our configuration:
 
 Note that if you care about how the ordering of keys is displayed in responses in the browsable API you might choose to use an `OrderedDict` when constructing the body of paginated responses, but this is optional.
 
-## Using your custom pagination class
+### Using your custom pagination class
 
 To have your custom pagination class be used by default, use the `DEFAULT_PAGINATION_CLASS` setting:
 
@@ -266,11 +278,11 @@ API responses for list endpoints will now include a `Link` header, instead of in
 
 ---
 
-# HTML pagination controls
+## HTML pagination controls
 
 By default using the pagination classes will cause HTML pagination controls to be displayed in the browsable API. There are two built-in display styles. The `PageNumberPagination` and `LimitOffsetPagination` classes display a list of page numbers with previous and next controls. The `CursorPagination` class displays a simpler style that only displays a previous and next control.
 
-## Customizing the controls
+### Customizing the controls
 
 You can override the templates that render the HTML pagination controls. The two built-in styles are:
 
@@ -289,19 +301,19 @@ The `.to_html()` and `.get_html_context()` methods may also be overridden in a c
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## DRF-extensions
+### DRF-extensions
 
 The [`DRF-extensions` package][drf-extensions] includes a [`PaginateByMaxMixin` mixin class][paginate-by-max-mixin] that allows your API clients to specify `?page_size=max` to obtain the maximum allowed page size.
 
-## drf-proxy-pagination
+### drf-proxy-pagination
 
 The [`drf-proxy-pagination` package][drf-proxy-pagination] includes a `ProxyPagination` class which allows to choose pagination class with a query parameter.
 
-## link-header-pagination
+### link-header-pagination
 
 The [`django-rest-framework-link-header-pagination` package][drf-link-header-pagination] includes a `LinkHeaderPagination` class which provides pagination via an HTTP `Link` header as described in [GitHub REST API documentation][github-traversing-with-pagination].
```


 - `.reference/api-guide/serializers.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> dff3c8d622096d6f193b382452e056896d4ff885
@@ -3,8 +3,6 @@ source:
     - serializers.py
 ---
 
-# Serializers
-
 > Expanding the usefulness of the serializers is something that we would
 like to address.  However, it's not a trivial problem, and it
 will take some serious design work.
@@ -15,7 +13,9 @@ Serializers allow complex data such as querysets and model instances to be conve
 
 The serializers in REST framework work very similarly to Django's `Form` and `ModelForm` classes. We provide a `Serializer` class which gives you a powerful, generic way to control the output of your responses, as well as a `ModelSerializer` class which provides a useful shortcut for creating serializers that deal with model instances and querysets.
 
-## Declaring Serializers
+## Serializers
+
+### Declaring Serializers
 
 Let's start by creating a simple object we can use for example purposes:
 
@@ -40,7 +40,7 @@ Declaring a serializer looks very similar to declaring a form:
         content = serializers.CharField(max_length=200)
         created = serializers.DateTimeField()
 
-## Serializing objects
+### Serializing objects
 
 We can now use `CommentSerializer` to serialize a comment, or list of comments. Again, using the `Serializer` class looks a lot like using a `Form` class.
 
@@ -56,7 +56,7 @@ At this point we've translated the model instance into Python native datatypes.
     json
     # b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
 
-## Deserializing objects
+### Deserializing objects
 
 Deserialization is similar. First we parse a stream into Python native datatypes...
 
@@ -74,7 +74,7 @@ Deserialization is similar. First we parse a stream into Python native datatypes
     serializer.validated_data
     # {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
 
-## Saving instances
+### Saving instances
 
 If we want to be able to return complete object instances based on the validated data we need to implement one or both of the `.create()` and `.update()` methods. For example:
 
@@ -147,7 +147,7 @@ For example:
 
 Note that in the case above we're now having to access the serializer `.validated_data` property directly.
 
-## Validation
+### Validation
 
 When deserializing data, you always need to call `is_valid()` before attempting to access the validated data, or save an object instance. If any validation errors occur, the `.errors` property will contain a dictionary representing the resulting error messages.  For example:
 
@@ -244,20 +244,20 @@ Serializer classes can also include reusable validators that are applied to the
 
 For more information see the [validators documentation](validators.md).
 
-## Accessing the initial data and instance
+### Accessing the initial data and instance
 
 When passing an initial object or queryset to a serializer instance, the object will be made available as `.instance`. If no initial object is passed then the `.instance` attribute will be `None`.
 
 When passing data to a serializer instance, the unmodified data will be made available as `.initial_data`. If the `data` keyword argument is not passed then the `.initial_data` attribute will not exist.
 
-## Partial updates
+### Partial updates
 
 By default, serializers must be passed values for all required fields or they will raise validation errors. You can use the `partial` argument in order to allow partial updates.
 
     # Update `comment` with partial data
     serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
 
-## Dealing with nested objects
+### Dealing with nested objects
 
 The previous examples are fine for dealing with objects that only have simple datatypes, but sometimes we also need to be able to represent more complex objects, where some of the attributes of an object might not be simple datatypes such as strings, dates or integers.
 
@@ -287,7 +287,7 @@ Similarly if a nested representation should be a list of items, you should pass
         content = serializers.CharField(max_length=200)
         created = serializers.DateTimeField()
 
-## Writable nested representations
+### Writable nested representations
 
 When dealing with nested representations that support deserializing the data, any errors with nested objects will be nested under the field name of the nested object.
 
@@ -388,7 +388,7 @@ This manager class now more nicely encapsulates that user instances and profile
 
 For more details on this approach see the Django documentation on [model managers][model-managers], and [this blogpost on using model and manager classes][encapsulation-blogpost].
 
-## Dealing with multiple objects
+### Dealing with multiple objects
 
 The `Serializer` class can also handle serializing or deserializing lists of objects.
 
@@ -409,7 +409,7 @@ To serialize a queryset or list of objects instead of a single object instance,
 
 The default behavior for deserializing multiple objects is to support multiple object creation, but not support multiple object updates. For more information on how to support or customize either of these cases, see the [ListSerializer](#listserializer) documentation below.
 
-## Including extra context
+### Including extra context
 
 There are some cases where you need to provide extra context to the serializer in addition to the object being serialized.  One common case is if you're using a serializer that includes hyperlinked relations, which requires the serializer to have access to the current request so that it can properly generate fully qualified URLs.
 
@@ -423,7 +423,7 @@ The context dictionary can be used within any serializer field logic, such as a
 
 ---
 
-# ModelSerializer
+## ModelSerializer
 
 Often you'll want serializer classes that map closely to Django model definitions.
 
@@ -446,7 +446,7 @@ By default, all the model fields on the class will be mapped to a corresponding
 
 Any relationships such as foreign keys on the model will be mapped to `PrimaryKeyRelatedField`. Reverse relationships are not included by default unless explicitly included as specified in the [serializer relations][relations] documentation.
 
-#### Inspecting a `ModelSerializer`
+### Inspecting a `ModelSerializer`
 
 Serializer classes generate helpful verbose representation strings, that allow you to fully inspect the state of their fields. This is particularly useful when working with `ModelSerializers` where you want to determine what set of fields and validators are being automatically created for you.
 
@@ -460,7 +460,7 @@ To do so, open the Django shell, using `python manage.py shell`, then import the
         name = CharField(allow_blank=True, max_length=100, required=False)
         owner = PrimaryKeyRelatedField(queryset=User.objects.all())
 
-## Specifying which fields to include
+### Specifying which fields to include
 
 If you only want a subset of the default fields to be used in a model serializer, you can do so using `fields` or `exclude` options, just as you would with a `ModelForm`. It is strongly recommended that you explicitly set all fields that should be serialized using the `fields` attribute. This will make it less likely to result in unintentionally exposing data when your models change.
 
@@ -497,7 +497,7 @@ Alternatively names in the `fields` options can map to properties or methods whi
 
 Since version 3.3.0, it is **mandatory** to provide one of the attributes `fields` or `exclude`.
 
-## Specifying nested serialization
+### Specifying nested serialization
 
 The default `ModelSerializer` uses primary keys for relationships, but you can also easily generate nested representations using the `depth` option:
 
@@ -511,7 +511,7 @@ The `depth` option should be set to an integer value that indicates the depth of
 
 If you want to customize the way the serialization is done you'll need to define the field yourself.
 
-## Specifying fields explicitly
+### Specifying fields explicitly
 
 You can add extra fields to a `ModelSerializer` or override the default fields by declaring fields on the class, just as you would for a `Serializer` class.
 
@@ -525,7 +525,7 @@ You can add extra fields to a `ModelSerializer` or override the default fields b
 
 Extra fields can correspond to any property or callable on the model.
 
-## Specifying read only fields
+### Specifying read only fields
 
 You may wish to specify multiple fields as read-only. Instead of adding each field explicitly with the `read_only=True` attribute, you may use the shortcut Meta option, `read_only_fields`.
 
@@ -550,7 +550,7 @@ Model fields which have `editable=False` set, and `AutoField` fields will be set
 
     Please review the [Validators Documentation](/api-guide/validators/) for details on the [UniqueTogetherValidator](/api-guide/validators/#uniquetogethervalidator) and [CurrentUserDefault](/api-guide/validators/#currentuserdefault) classes.
 
-## Additional keyword arguments
+### Additional keyword arguments
 
 There is also a shortcut allowing you to specify arbitrary additional keyword arguments on fields, using the `extra_kwargs` option. As in the case of `read_only_fields`, this means you do not need to explicitly declare the field on the serializer.
 
@@ -573,7 +573,7 @@ This option is a dictionary, mapping field names to a dictionary of keyword argu
 
 Please keep in mind that, if the field has already been explicitly declared on the serializer class, then the `extra_kwargs` option will be ignored.
 
-## Relational fields
+### Relational fields
 
 When serializing model instances, there are a number of different ways you might choose to represent relationships.  The default representation for `ModelSerializer` is to use the primary keys of the related instances.
 
@@ -581,17 +581,17 @@ Alternative representations include serializing using hyperlinks, serializing co
 
 For full details see the [serializer relations][relations] documentation.
 
-## Customizing field mappings
+### Customizing field mappings
 
 The ModelSerializer class also exposes an API that you can override in order to alter how serializer fields are automatically determined when instantiating the serializer.
 
 Normally if a `ModelSerializer` does not generate the fields you need by default then you should either add them to the class explicitly, or simply use a regular `Serializer` class instead. However in some cases you may want to create a new base class that defines how the serializer fields are created for any given model.
 
-### `serializer_field_mapping`
+#### `serializer_field_mapping`
 
 A mapping of Django model fields to REST framework serializer fields. You can override this mapping to alter the default serializer fields that should be used for each model field.
 
-### `serializer_related_field`
+#### `serializer_related_field`
 
 This property should be the serializer field class, that is used for relational fields by default.
 
@@ -599,29 +599,29 @@ For `ModelSerializer` this defaults to `serializers.PrimaryKeyRelatedField`.
 
 For `HyperlinkedModelSerializer` this defaults to `serializers.HyperlinkedRelatedField`.
 
-### `serializer_url_field`
+#### `serializer_url_field`
 
 The serializer field class that should be used for any `url` field on the serializer.
 
 Defaults to `serializers.HyperlinkedIdentityField`
 
-### `serializer_choice_field`
+#### `serializer_choice_field`
 
 The serializer field class that should be used for any choice fields on the serializer.
 
 Defaults to `serializers.ChoiceField`
 
-### The field_class and field_kwargs API
+#### The field_class and field_kwargs API
 
 The following methods are called to determine the class and keyword arguments for each field that should be automatically included on the serializer. Each of these methods should return a two tuple of `(field_class, field_kwargs)`.
 
-### `build_standard_field(self, field_name, model_field)`
+#### `build_standard_field(self, field_name, model_field)`
 
 Called to generate a serializer field that maps to a standard model field.
 
 The default implementation returns a serializer class based on the `serializer_field_mapping` attribute.
 
-### `build_relational_field(self, field_name, relation_info)`
+#### `build_relational_field(self, field_name, relation_info)`
 
 Called to generate a serializer field that maps to a relational model field.
 
@@ -629,7 +629,7 @@ The default implementation returns a serializer class based on the `serializer_r
 
 The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.
 
-### `build_nested_field(self, field_name, relation_info, nested_depth)`
+#### `build_nested_field(self, field_name, relation_info, nested_depth)`
 
 Called to generate a serializer field that maps to a relational model field, when the `depth` option has been set.
 
@@ -639,24 +639,24 @@ The `nested_depth` will be the value of the `depth` option, minus one.
 
 The `relation_info` argument is a named tuple, that contains `model_field`, `related_model`, `to_many` and `has_through_model` properties.
 
-### `build_property_field(self, field_name, model_class)`
+#### `build_property_field(self, field_name, model_class)`
 
 Called to generate a serializer field that maps to a property or zero-argument method on the model class.
 
 The default implementation returns a `ReadOnlyField` class.
 
-### `build_url_field(self, field_name, model_class)`
+#### `build_url_field(self, field_name, model_class)`
 
 Called to generate a serializer field for the serializer's own `url` field. The default implementation returns a `HyperlinkedIdentityField` class.
 
-### `build_unknown_field(self, field_name, model_class)`
+#### `build_unknown_field(self, field_name, model_class)`
 
 Called when the field name did not map to any model field or model property.
 The default implementation raises an error, although subclasses may customize this behavior.
 
 ---
 
-# HyperlinkedModelSerializer
+## HyperlinkedModelSerializer
 
 The `HyperlinkedModelSerializer` class is similar to the `ModelSerializer` class except that it uses hyperlinks to represent relationships, rather than primary keys.
 
@@ -671,7 +671,7 @@ You can explicitly include the primary key by adding it to the `fields` option,
             model = Account
             fields = ['url', 'id', 'account_name', 'users', 'created']
 
-## Absolute and relative URLs
+### Absolute and relative URLs
 
 When instantiating a `HyperlinkedModelSerializer` you must include the current
 `request` in the serializer context, for example:
@@ -690,7 +690,7 @@ Rather than relative URLs, such as:
 If you *do* want to use relative URLs, you should explicitly pass `{'request': None}`
 in the serializer context.
 
-## How hyperlinked views are determined
+### How hyperlinked views are determined
 
 There needs to be a way of determining which views should be used for hyperlinking to model instances.
 
@@ -731,13 +731,13 @@ Alternatively you can set the fields on the serializer explicitly. For example:
 
 ---
 
-## Changing the URL field name
+### Changing the URL field name
 
 The name of the URL field defaults to 'url'.  You can override this globally, by using the `URL_FIELD_NAME` setting.
 
 ---
 
-# ListSerializer
+## ListSerializer
 
 The `ListSerializer` class provides the behavior for serializing and validating multiple objects at once. You won't *typically* need to use `ListSerializer` directly, but should instead simply pass `many=True` when instantiating a serializer.
 
@@ -745,17 +745,11 @@ When a serializer is instantiated and `many=True` is passed, a `ListSerializer`
 
 The following argument can also be passed to a `ListSerializer` field or a serializer that is passed `many=True`:
 
-### `allow_empty`
-
-This is `True` by default, but can be set to `False` if you want to disallow empty lists as valid input.
-
-### `max_length`
+- `allow_empty`: this is `True` by default, but can be set to `False` if you want to disallow empty lists as valid input.
 
-This is `None` by default, but can be set to a positive integer if you want to validate that the list contains no more than this number of elements.
+- `max_length`: this is `None` by default, but can be set to a positive integer if you want to validate that the list contains no more than this number of elements.
 
-### `min_length`
-
-This is `None` by default, but can be set to a positive integer if you want to validate that the list contains no fewer than this number of elements.
+- `min_length`: this is `None` by default, but can be set to a positive integer if you want to validate that the list contains no fewer than this number of elements.
 
 ### Customizing `ListSerializer` behavior
 
@@ -776,7 +770,7 @@ For example:
         class Meta:
             list_serializer_class = CustomListSerializer
 
-#### Customizing multiple create
+### Customizing multiple create
 
 The default implementation for multiple object creation is to simply call `.create()` for each item in the list. If you want to customize this behavior, you'll need to customize the `.create()` method on `ListSerializer` class that is used when `many=True` is passed.
 
@@ -792,7 +786,7 @@ For example:
         class Meta:
             list_serializer_class = BookListSerializer
 
-#### Customizing multiple update
+### Customizing multiple update
 
 By default the `ListSerializer` class does not support multiple updates. This is because the behavior that should be expected for insertions and deletions is ambiguous.
 
@@ -838,7 +832,7 @@ Here's an example of how you might choose to implement multiple updates:
         class Meta:
             list_serializer_class = BookListSerializer
 
-#### Customizing ListSerializer initialization
+### Customizing ListSerializer initialization
 
 When a serializer with `many=True` is instantiated, we need to determine which arguments and keyword arguments should be passed to the `.__init__()` method for both the child `Serializer` class, and for the parent `ListSerializer` class.
 
@@ -855,7 +849,7 @@ Occasionally you might need to explicitly specify how the child and parent class
 
 ---
 
-# BaseSerializer
+## BaseSerializer
 
 `BaseSerializer` class that can be used to easily support alternative serialization and deserialization styles.
 
@@ -877,7 +871,7 @@ Because this class provides the same interface as the `Serializer` class, you ca
 
 The only difference you'll notice when doing so is the `BaseSerializer` classes will not generate HTML forms in the browsable API. This is because the data they return does not include all the field information that would allow each field to be rendered into a suitable HTML input.
 
-#### Read-only `BaseSerializer` classes
+### Read-only `BaseSerializer` classes
 
 To implement a read-only serializer using the `BaseSerializer` class, we just need to override the `.to_representation()` method. Let's take a look at an example using a simple Django model:
 
@@ -911,7 +905,7 @@ Or use it to serialize multiple instances:
         serializer = HighScoreSerializer(queryset, many=True)
         return Response(serializer.data)
 
-#### Read-write `BaseSerializer` classes
+### Read-write `BaseSerializer` classes
 
 To create a read-write serializer we first need to implement a `.to_internal_value()` method. This method returns the validated values that will be used to construct the object instance, and may raise a `serializers.ValidationError` if the supplied data is in an incorrect format.
 
@@ -956,7 +950,7 @@ Here's a complete example of our previous `HighScoreSerializer`, that's been upd
         def create(self, validated_data):
             return HighScore.objects.create(**validated_data)
 
-#### Creating new base classes
+### Creating new base classes
 
 The `BaseSerializer` class is also useful if you want to implement new generic serializer classes for dealing with particular serialization styles, or for integrating with alternative storage backends.
 
@@ -998,9 +992,9 @@ The following class is an example of a generic serializer that can handle coerci
 
 ---
 
-# Advanced serializer usage
+## Advanced serializer usage
 
-## Overriding serialization and deserialization behavior
+### Overriding serialization and deserialization behavior
 
 If you need to alter the serialization or deserialization behavior of a serializer class, you can do so by overriding the `.to_representation()` or `.to_internal_value()` methods.
 
@@ -1032,7 +1026,7 @@ If any of the validation fails, then the method should raise a `serializers.Vali
 
 The `data` argument passed to this method will normally be the value of `request.data`, so the datatype it provides will depend on the parser classes you have configured for your API.
 
-## Serializer Inheritance
+### Serializer Inheritance
 
 Similar to Django forms, you can extend and reuse serializers through inheritance. This allows you to declare a common set of fields or methods on a parent class that can then be used in a number of serializers. For example,
 
@@ -1066,13 +1060,13 @@ Additionally, the following caveats apply to serializer inheritance:
 
     However, you can only use this technique to opt out from a field defined declaratively by a parent class; it won’t prevent the `ModelSerializer` from generating a default field. To opt-out from default fields, see [Specifying which fields to include](#specifying-which-fields-to-include).
 
-## Dynamically modifying fields
+### Dynamically modifying fields
 
 Once a serializer has been initialized, the dictionary of fields that are set on the serializer may be accessed using the `.fields` attribute.  Accessing and modifying this attribute allows you to dynamically modify the serializer.
 
 Modifying the `fields` argument directly allows you to do interesting things such as changing the arguments on serializer fields at runtime, rather than at the point of declaring the serializer.
 
-### Example
+#### Example
 
 For example, if you wanted to be able to set which fields should be used by a serializer at the point of initializing it, you could create a serializer class like so:
 
@@ -1109,7 +1103,7 @@ This would then allow you to do the following:
     >>> print(UserSerializer(user, fields=('id', 'email')))
     {'id': 2, 'email': 'jon@example.com'}
 
-## Customizing the default fields
+### Customizing the default fields
 
 REST framework 2 provided an API to allow developers to override how a `ModelSerializer` class would automatically generate the default set of fields.
 
@@ -1119,73 +1113,77 @@ Because the serializers have been fundamentally redesigned with 3.0 this API no
 
 ---
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## Django REST marshmallow
+### Django REST marshmallow
 
 The [django-rest-marshmallow][django-rest-marshmallow] package provides an alternative implementation for serializers, using the python [marshmallow][marshmallow] library. It exposes the same API as the REST framework serializers, and can be used as a drop-in replacement in some use-cases.
 
-## Serpy
+### Serpy
 
 The [serpy][serpy] package is an alternative implementation for serializers that is built for speed. [Serpy][serpy] serializes complex datatypes to simple native types. The native types can be easily converted to JSON or any other format needed.
 
-## MongoengineModelSerializer
+### MongoengineModelSerializer
 
 The [django-rest-framework-mongoengine][mongoengine] package provides a `MongoEngineModelSerializer` serializer class that supports using MongoDB as the storage layer for Django REST framework.
 
-## GeoFeatureModelSerializer
+### GeoFeatureModelSerializer
 
 The [django-rest-framework-gis][django-rest-framework-gis] package provides a `GeoFeatureModelSerializer` serializer class that supports GeoJSON both for read and write operations.
 
-## HStoreSerializer
+### HStoreSerializer
 
 The [django-rest-framework-hstore][django-rest-framework-hstore] package provides an `HStoreSerializer` to support [django-hstore][django-hstore] `DictionaryField` model field and its `schema-mode` feature.
 
-## Dynamic REST
+### Dynamic REST
 
 The [dynamic-rest][dynamic-rest] package extends the ModelSerializer and ModelViewSet interfaces, adding API query parameters for filtering, sorting, and including / excluding all fields and relationships defined by your serializers.
 
-## Dynamic Fields Mixin
+### Dynamic Fields Mixin
 
 The [drf-dynamic-fields][drf-dynamic-fields] package provides a mixin to dynamically limit the fields per serializer to a subset specified by an URL parameter.
 
-## DRF FlexFields
+### DRF FlexFields
 
 The [drf-flex-fields][drf-flex-fields] package extends the ModelSerializer and ModelViewSet to provide commonly used functionality for dynamically setting fields and expanding primitive fields to nested models, both from URL parameters and your serializer class definitions.
 
-## Serializer Extensions
+### Serializer Extensions
 
 The [django-rest-framework-serializer-extensions][drf-serializer-extensions]
 package provides a collection of tools to DRY up your serializers, by allowing
 fields to be defined on a per-view/request basis. Fields can be whitelisted,
 blacklisted and child serializers can be optionally expanded.
 
-## HTML JSON Forms
+### HTML JSON Forms
 
 The [html-json-forms][html-json-forms] package provides an algorithm and serializer for processing `<form>` submissions per the (inactive) [HTML JSON Form specification][json-form-spec].  The serializer facilitates processing of arbitrarily nested JSON structures within HTML.  For example, `<input name="items[0][id]" value="5">` will be interpreted as `{"items": [{"id": "5"}]}`.
 
-## DRF-Base64
+### DRF-Base64
 
 [DRF-Base64][drf-base64] provides a set of field and model serializers that handles the upload of base64-encoded files.
 
-## QueryFields
+### QueryFields
 
 [djangorestframework-queryfields][djangorestframework-queryfields] allows API clients to specify which fields will be sent in the response via inclusion/exclusion query parameters.
 
-## DRF Writable Nested
+### DRF Writable Nested
 
 The [drf-writable-nested][drf-writable-nested] package provides writable nested model serializer which allows to create/update models with nested related data.
 
-## DRF Encrypt Content
+### DRF Encrypt Content
 
 The [drf-encrypt-content][drf-encrypt-content] package helps you encrypt your data, serialized through ModelSerializer. It also contains some helper functions. Which helps you to encrypt your data.
 
-## Shapeless Serializers
+### Shapeless Serializers
 
 The [drf-shapeless-serializers][drf-shapeless-serializers] package provides dynamic serializer configuration capabilities, allowing runtime field selection, renaming, attribute modification, and nested relationship configuration without creating multiple serializer classes. It helps eliminate serializer boilerplate while providing flexible API responses.
 
+### DRF Pydantic
+
+The [drf-pydantic][drf-pydantic] package allows you to use Pydantic with Django REST framework for data validation and (de)serialization. If you develop DRF APIs and rely on Pydantic for data validation, this package provides seamless integration between both libraries.
+
 
 [cite]: https://groups.google.com/d/topic/django-users/sVFaOfQi4wY/discussion
 [relations]: relations.md
@@ -1210,3 +1208,4 @@ The [drf-shapeless-serializers][drf-shapeless-serializers] package provides dyna
 [drf-writable-nested]: https://github.com/beda-software/drf-writable-nested
 [drf-encrypt-content]: https://github.com/oguzhancelikarslan/drf-encrypt-content
 [drf-shapeless-serializers]: https://github.com/khaledsukkar2/drf-shapeless-serializers
+[drf-pydantic]: https://github.com/georgebv/drf-pydantic
```


 - `.reference/api-guide/filtering.md`
```
a323cf7c0a33d7ffd395a6805019f613fb79f985 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -82,7 +82,7 @@ We can override `.get_queryset()` to deal with URLs such as `http://example.com/
 
 ---
 
-# Generic Filtering
+## Generic Filtering
 
 As well as being able to override the default queryset, REST framework also includes support for generic filtering backends that allow you to easily construct complex searches and filters.
 
@@ -90,7 +90,7 @@ Generic filters can also present themselves as HTML controls in the browsable AP
 
 ![Filter Example](../img/filter-controls.png)
 
-## Setting filter backends
+### Setting filter backends
 
 The default filter backends may be set globally, using the `DEFAULT_FILTER_BACKENDS` setting. For example.
 
@@ -111,7 +111,7 @@ using the `GenericAPIView` class-based views.
         serializer_class = UserSerializer
         filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
 
-## Filtering and object lookups
+### Filtering and object lookups
 
 Note that if a filter backend is configured for a view, then as well as being used to filter list views, it will also be used to filter the querysets used for returning a single object.
 
@@ -119,7 +119,7 @@ For instance, given the previous example, and a product with an id of `4675`, th
 
     http://example.com/api/products/4675/?category=clothing&max_price=10.00
 
-## Overriding the initial queryset
+### Overriding the initial queryset
 
 Note that you can use both an overridden `.get_queryset()` and generic filtering together, and everything will work as expected.  For example, if `Product` had a many-to-many relationship with `User`, named `purchase`, you might want to write a view like this:
 
@@ -138,9 +138,9 @@ Note that you can use both an overridden `.get_queryset()` and generic filtering
 
 ---
 
-# API Guide
+## API Guide
 
-## DjangoFilterBackend
+### DjangoFilterBackend
 
 The [`django-filter`][django-filter-docs] library includes a `DjangoFilterBackend` class which
 supports highly customizable field filtering for REST framework.
@@ -188,7 +188,7 @@ You can read more about `FilterSet`s in the [django-filter documentation][django
 It's also recommended that you read the section on [DRF integration][django-filter-drf-docs].
 
 
-## SearchFilter
+### SearchFilter
 
 The `SearchFilter` class supports simple single query parameter based searching, and is based on the [Django admin's search functionality][search-django-admin].
 
@@ -251,7 +251,7 @@ For more details, see the [Django documentation][search-django-admin].
 
 ---
 
-## OrderingFilter
+### OrderingFilter
 
 The `OrderingFilter` class supports simple query parameter controlled ordering of results.
 
@@ -271,7 +271,7 @@ Multiple orderings may also be specified:
 
     http://example.com/api/users?ordering=account,username
 
-### Specifying which fields may be ordered against
+#### Specifying which fields may be ordered against
 
 It's recommended that you explicitly specify which fields the API should allow in the ordering filter.  You can do this by setting an `ordering_fields` attribute on the view, like so:
 
@@ -293,7 +293,7 @@ If you are confident that the queryset being used by the view doesn't contain an
         filter_backends = [filters.OrderingFilter]
         ordering_fields = '__all__'
 
-### Specifying a default ordering
+#### Specifying a default ordering
 
 If an `ordering` attribute is set on the view, this will be used as the default ordering.
 
@@ -310,7 +310,7 @@ The `ordering` attribute may be either a string or a list/tuple of strings.
 
 ---
 
-# Custom generic filtering
+## Custom generic filtering
 
 You can also provide your own generic filtering backend, or write an installable app for other developers to use.
 
@@ -318,7 +318,7 @@ To do so override `BaseFilterBackend`, and override the `.filter_queryset(self,
 
 As well as allowing clients to perform searches and filtering, generic filter backends can be useful for restricting which objects should be visible to any given request or user.
 
-## Example
+### Example
 
 For example, you might need to restrict users to only being able to see objects they created.
 
@@ -331,7 +331,7 @@ For example, you might need to restrict users to only being able to see objects
 
 We could achieve the same behavior by overriding `get_queryset()` on the views, but using a filter backend allows you to more easily add this restriction to multiple views, or to apply it across the entire API.
 
-## Customizing the interface
+### Customizing the interface
 
 Generic filters may also present an interface in the browsable API. To do so you should implement a `to_html()` method which returns a rendered HTML representation of the filter. This method should have the following signature:
 
@@ -339,23 +339,23 @@ Generic filters may also present an interface in the browsable API. To do so you
 
 The method should return a rendered HTML string.
 
-# Third party packages
+## Third party packages
 
 The following third party packages provide additional filter implementations.
 
-## Django REST framework filters package
+### Django REST framework filters package
 
 The [django-rest-framework-filters package][django-rest-framework-filters] works together with the `DjangoFilterBackend` class, and allows you to easily create filters across relationships, or create multiple filter lookup types for a given field.
 
-## Django REST framework full word search filter
+### Django REST framework full word search filter
 
 The [djangorestframework-word-filter][django-rest-framework-word-search-filter] developed as alternative to `filters.SearchFilter` which will search full word in text, or exact match.
 
-## Django URL Filter
+### Django URL Filter
 
 [django-url-filter][django-url-filter] provides a safe way to filter data via human-friendly URLs. It works very similar to DRF serializers and fields in a sense that they can be nested except they are called filtersets and filters. That provides easy way to filter related data. Also this library is generic-purpose so it can be used to filter other sources of data and not only Django `QuerySet`s.
 
-## drf-url-filters
+### drf-url-filters
 
 [drf-url-filter][drf-url-filter] is a simple Django app to apply filters on drf `ModelViewSet`'s `Queryset` in a clean, simple and configurable way. It also supports validations on incoming query params and their values. A beautiful python package `Voluptuous` is being used for validations on the incoming query parameters. The best part about voluptuous is you can define your own validations as per your query params requirements.
```


 - `.reference/api-guide/exceptions.md`
```
c0202a0aa5cbaf8573458b932878dfd5044c93ab -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -93,9 +93,9 @@ Note that the exception handler will only be called for responses generated by r
 
 ---
 
-# API Reference
+## API Reference
 
-## APIException
+### APIException
 
 **Signature:** `APIException()`
 
@@ -143,7 +143,7 @@ dictionary of items:
     >>> print(exc.get_full_details())
     {"name":{"message":"This field is required.","code":"required"},"age":{"message":"A valid integer is required.","code":"invalid"}}
 
-## ParseError
+### ParseError
 
 **Signature:** `ParseError(detail=None, code=None)`
 
@@ -151,7 +151,7 @@ Raised if the request contains malformed data when accessing `request.data`.
 
 By default this exception results in a response with the HTTP status code "400 Bad Request".
 
-## AuthenticationFailed
+### AuthenticationFailed
 
 **Signature:** `AuthenticationFailed(detail=None, code=None)`
 
@@ -159,7 +159,7 @@ Raised when an incoming request includes incorrect authentication.
 
 By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use.  See the [authentication documentation][authentication] for more details.
 
-## NotAuthenticated
+### NotAuthenticated
 
 **Signature:** `NotAuthenticated(detail=None, code=None)`
 
@@ -167,7 +167,7 @@ Raised when an unauthenticated request fails the permission checks.
 
 By default this exception results in a response with the HTTP status code "401 Unauthenticated", but it may also result in a "403 Forbidden" response, depending on the authentication scheme in use.  See the [authentication documentation][authentication] for more details.
 
-## PermissionDenied
+### PermissionDenied
 
 **Signature:** `PermissionDenied(detail=None, code=None)`
 
@@ -175,7 +175,7 @@ Raised when an authenticated request fails the permission checks.
 
 By default this exception results in a response with the HTTP status code "403 Forbidden".
 
-## NotFound
+### NotFound
 
 **Signature:** `NotFound(detail=None, code=None)`
 
@@ -183,7 +183,7 @@ Raised when a resource does not exist at the given URL. This exception is equiva
 
 By default this exception results in a response with the HTTP status code "404 Not Found".
 
-## MethodNotAllowed
+### MethodNotAllowed
 
 **Signature:** `MethodNotAllowed(method, detail=None, code=None)`
 
@@ -191,7 +191,7 @@ Raised when an incoming request occurs that does not map to a handler method on
 
 By default this exception results in a response with the HTTP status code "405 Method Not Allowed".
 
-## NotAcceptable
+### NotAcceptable
 
 **Signature:** `NotAcceptable(detail=None, code=None)`
 
@@ -199,7 +199,7 @@ Raised when an incoming request occurs with an `Accept` header that cannot be sa
 
 By default this exception results in a response with the HTTP status code "406 Not Acceptable".
 
-## UnsupportedMediaType
+### UnsupportedMediaType
 
 **Signature:** `UnsupportedMediaType(media_type, detail=None, code=None)`
 
@@ -207,7 +207,7 @@ Raised if there are no parsers that can handle the content type of the request d
 
 By default this exception results in a response with the HTTP status code "415 Unsupported Media Type".
 
-## Throttled
+### Throttled
 
 **Signature:** `Throttled(wait=None, detail=None, code=None)`
 
@@ -215,7 +215,7 @@ Raised when an incoming request fails the throttling checks.
 
 By default this exception results in a response with the HTTP status code "429 Too Many Requests".
 
-## ValidationError
+### ValidationError
 
 **Signature:** `ValidationError(detail=None, code=None)`
 
@@ -235,7 +235,7 @@ By default this exception results in a response with the HTTP status code "400 B
 
 ---
 
-# Generic Error Views
+## Generic Error Views
 
 Django REST Framework provides two error views suitable for providing generic JSON `500` Server Error and
 `400` Bad Request responses. (Django's default error views provide HTML responses, which may not be appropriate for an
@@ -243,7 +243,7 @@ API-only application.)
 
 Use these as per [Django's Customizing error views documentation][django-custom-error-views].
 
-## `rest_framework.exceptions.server_error`
+### `rest_framework.exceptions.server_error`
 
 Returns a response with status code `500` and `application/json` content type.
 
@@ -251,7 +251,7 @@ Set as `handler500`:
 
     handler500 = 'rest_framework.exceptions.server_error'
 
-## `rest_framework.exceptions.bad_request`
+### `rest_framework.exceptions.bad_request`
 
 Returns a response with status code `400` and `application/json` content type.
 
@@ -259,11 +259,11 @@ Set as `handler400`:
 
     handler400 = 'rest_framework.exceptions.bad_request'
 
-# Third party packages
+## Third party packages
 
 The following third-party packages are also available.
 
-## DRF Standardized Errors
+### DRF Standardized Errors
 
 The [drf-standardized-errors][drf-standardized-errors] package provides an exception handler that generates the same format for all 4xx and 5xx responses. It is a drop-in replacement for the default exception handler and allows customizing the error response format without rewriting the whole exception handler. The standardized error response format is easier to document and easier to handle by API consumers.
```


 - `.reference/api-guide/content-negotiation.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -3,8 +3,6 @@ source:
     - negotiation.py
 ---
 
-# Content negotiation
-
 > HTTP has provisions for several mechanisms for "content negotiation" - the process of selecting the best representation for a given response when there are multiple representations available.
 >
 > &mdash; [RFC 2616][cite], Fielding et al.
@@ -40,7 +38,7 @@ For more information on the `HTTP Accept` header, see [RFC 2616][accept-header]
 
     This is a valid approach as the HTTP spec deliberately underspecifies how a server should weight server-based preferences against client-based preferences.
 
-# Custom content negotiation
+## Custom content negotiation
 
 It's unlikely that you'll want to provide a custom content negotiation scheme for REST framework, but you can do so if needed.  To implement a custom content negotiation scheme override `BaseContentNegotiation`.
 
@@ -50,7 +48,7 @@ The `select_parser()` method should return one of the parser instances from the
 
 The `select_renderer()` method should return a two-tuple of (renderer instance, media type), or raise a `NotAcceptable` exception.
 
-## Example
+### Example
 
 The following is a custom content negotiation class which ignores the client
 request when selecting the appropriate parser or renderer.
@@ -70,7 +68,7 @@ request when selecting the appropriate parser or renderer.
             """
             return (renderers[0], renderers[0].media_type)
 
-## Setting the content negotiation
+### Setting the content negotiation
 
 The default content negotiation class may be set globally, using the `DEFAULT_CONTENT_NEGOTIATION_CLASS` setting.  For example, the following settings would use our example `IgnoreClientContentNegotiation` class.
```


 - `.reference/api-guide/fields.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -135,9 +135,9 @@ For more details see the [HTML & Forms][html-and-forms] documentation.
 
 ---
 
-# Boolean fields
+## Boolean fields
 
-## BooleanField
+### BooleanField
 
 A boolean representation.
 
@@ -158,9 +158,9 @@ Corresponds to `django.db.models.fields.BooleanField`.
 
 ---
 
-# String fields
+## String fields
 
-## CharField
+### CharField
 
 A text representation. Optionally validates the text to be shorter than `max_length` and longer than `min_length`.
 
@@ -175,7 +175,7 @@ Corresponds to `django.db.models.fields.CharField` or `django.db.models.fields.T
 
 The `allow_null` option is also available for string fields, although its usage is discouraged in favor of `allow_blank`. It is valid to set both `allow_blank=True` and `allow_null=True`, but doing so means that there will be two differing types of empty value permissible for string representations, which can lead to data inconsistencies and subtle application bugs.
 
-## EmailField
+### EmailField
 
 A text representation, validates the text to be a valid email address.
 
@@ -183,7 +183,7 @@ Corresponds to `django.db.models.fields.EmailField`
 
 **Signature:** `EmailField(max_length=None, min_length=None, allow_blank=False)`
 
-## RegexField
+### RegexField
 
 A text representation, that validates the given value matches against a certain regular expression.
 
@@ -195,7 +195,7 @@ The mandatory `regex` argument may either be a string, or a compiled python regu
 
 Uses Django's `django.core.validators.RegexValidator` for validation.
 
-## SlugField
+### SlugField
 
 A `RegexField` that validates the input against the pattern `[a-zA-Z0-9_-]+`.
 
@@ -203,7 +203,7 @@ Corresponds to `django.db.models.fields.SlugField`.
 
 **Signature:** `SlugField(max_length=50, min_length=None, allow_blank=False)`
 
-## URLField
+### URLField
 
 A `RegexField` that validates the input against a URL matching pattern. Expects fully qualified URLs of the form `http://<host>/<path>`.
 
@@ -211,7 +211,7 @@ Corresponds to `django.db.models.fields.URLField`.  Uses Django's `django.core.v
 
 **Signature:** `URLField(max_length=200, min_length=None, allow_blank=False)`
 
-## UUIDField
+### UUIDField
 
 A field that ensures the input is a valid UUID string. The `to_internal_value` method will return a `uuid.UUID` instance. On output the field will return a string in the canonical hyphenated format, for example:
 
@@ -226,7 +226,7 @@ A field that ensures the input is a valid UUID string. The `to_internal_value` m
     * `'urn'` - RFC 4122 URN representation of the UUID: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`
   Changing the `format` parameters only affects representation values. All formats are accepted by `to_internal_value`
 
-## FilePathField
+### FilePathField
 
 A field whose choices are limited to the filenames in a certain directory on the filesystem
 
@@ -240,7 +240,7 @@ Corresponds to `django.forms.fields.FilePathField`.
 * `allow_files` - Specifies whether files in the specified location should be included. Default is `True`. Either this or `allow_folders` must be `True`.
 * `allow_folders` - Specifies whether folders in the specified location should be included. Default is `False`. Either this or `allow_files` must be `True`.
 
-## IPAddressField
+### IPAddressField
 
 A field that ensures the input is a valid IPv4 or IPv6 string.
 
@@ -253,9 +253,9 @@ Corresponds to `django.forms.fields.IPAddressField` and `django.forms.fields.Gen
 
 ---
 
-# Numeric fields
+## Numeric fields
 
-## IntegerField
+### IntegerField
 
 An integer representation.
 
@@ -266,7 +266,7 @@ Corresponds to `django.db.models.fields.IntegerField`, `django.db.models.fields.
 * `max_value` Validate that the number provided is no greater than this value.
 * `min_value` Validate that the number provided is no less than this value.
 
-## BigIntegerField
+### BigIntegerField
 
 A biginteger representation.
 
@@ -278,7 +278,7 @@ Corresponds to `django.db.models.fields.BigIntegerField`.
 * `min_value` Validate that the number provided is no less than this value.
 * `coerce_to_string` Set to `True` if string values should be returned for the representation, or `False` if `BigInteger` objects should be returned. Defaults to the same value as the `COERCE_BIGINT_TO_STRING` settings key, which will be `False` unless overridden. If `BigInteger` objects are returned by the serializer, then the final output format will be determined by the renderer.
 
-## FloatField
+### FloatField
 
 A floating point representation.
 
@@ -289,7 +289,7 @@ Corresponds to `django.db.models.fields.FloatField`.
 * `max_value` Validate that the number provided is no greater than this value.
 * `min_value` Validate that the number provided is no less than this value.
 
-## DecimalField
+### DecimalField
 
 A decimal representation, represented in Python by a `Decimal` instance.
 
@@ -318,9 +318,9 @@ And to validate numbers up to anything less than one billion with a resolution o
 
 ---
 
-# Date and time fields
+## Date and time fields
 
-## DateTimeField
+### DateTimeField
 
 A date and time representation.
 
@@ -350,7 +350,7 @@ If you want to override this behavior, you'll need to declare the `DateTimeField
         class Meta:
             model = Comment
 
-## DateField
+### DateField
 
 A date representation.
 
@@ -365,7 +365,7 @@ Corresponds to `django.db.models.fields.DateField`
 
 Format strings may either be [Python strftime formats][strftime] which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601][iso8601] style dates should be used. (eg `'2013-01-29'`)
 
-## TimeField
+### TimeField
 
 A time representation.
 
@@ -380,7 +380,7 @@ Corresponds to `django.db.models.fields.TimeField`
 
 Format strings may either be [Python strftime formats][strftime] which explicitly specify the format, or the special string `'iso-8601'`, which indicates that [ISO 8601][iso8601] style times should be used. (eg `'12:34:56.000000'`)
 
-## DurationField
+### DurationField
 
 A Duration representation.
 Corresponds to `django.db.models.fields.DurationField`
@@ -398,9 +398,9 @@ Format may either be the special string `'iso-8601'`, which indicates that [ISO
 
 ---
 
-# Choice selection fields
+## Choice selection fields
 
-## ChoiceField
+### ChoiceField
 
 A field that can accept a value out of a limited set of choices.
 
@@ -415,9 +415,9 @@ Used by `ModelSerializer` to automatically generate fields if the corresponding
 
 Both the `allow_blank` and `allow_null` are valid options on `ChoiceField`, although it is highly recommended that you only use one and not both. `allow_blank` should be preferred for textual choices, and `allow_null` should be preferred for numeric or other non-textual choices.
 
-## MultipleChoiceField
+### MultipleChoiceField
 
-A field that can accept a set of zero, one or many values, chosen from a limited set of choices. Takes a single mandatory argument. `to_internal_value` returns a `set` containing the selected values.
+A field that can accept a list of zero, one or many values, chosen from a limited set of choices. Takes a single mandatory argument. `to_internal_value` returns a `list` containing the selected values, deduplicated.
 
 **Signature:** `MultipleChoiceField(choices)`
 
@@ -430,14 +430,13 @@ As with `ChoiceField`, both the `allow_blank` and `allow_null` options are valid
 
 ---
 
-# File upload fields
+## File upload fields
 
-#### Parsers and file uploads.
-
-The `FileField` and `ImageField` classes are only suitable for use with `MultiPartParser` or `FileUploadParser`. Most parsers, such as e.g. JSON don't support file uploads.
-Django's regular [FILE_UPLOAD_HANDLERS] are used for handling uploaded files.
+!!! note
+    The `FileField` and `ImageField` classes are only suitable for use with `MultiPartParser` or `FileUploadParser`. Most parsers, such as e.g. JSON don't support file uploads.
+    Django's regular [FILE_UPLOAD_HANDLERS] are used for handling uploaded files.
 
-## FileField
+### FileField
 
 A file representation.  Performs Django's standard FileField validation.
 
@@ -449,7 +448,7 @@ Corresponds to `django.forms.fields.FileField`.
 * `allow_empty_file` - Designates if empty files are allowed.
 * `use_url` - If set to `True` then URL string values will be used for the output representation. If set to `False` then filename string values will be used for the output representation. Defaults to the value of the `UPLOADED_FILES_USE_URL` settings key, which is `True` unless set otherwise.
 
-## ImageField
+### ImageField
 
 An image representation. Validates the uploaded file content as matching a known image format.
 
@@ -465,9 +464,9 @@ Requires either the `Pillow` package or `PIL` package.  The `Pillow` package is
 
 ---
 
-# Composite fields
+## Composite fields
 
-## ListField
+### ListField
 
 A field class that validates a list of objects.
 
@@ -491,7 +490,7 @@ The `ListField` class also supports a declarative style that allows you to write
 
 We can now reuse our custom `StringListField` class throughout our application, without having to provide a `child` argument to it.
 
-## DictField
+### DictField
 
 A field class that validates a dictionary of objects. The keys in `DictField` are always assumed to be string values.
 
@@ -509,7 +508,7 @@ You can also use the declarative style, as with `ListField`. For example:
     class DocumentField(DictField):
         child = CharField()
 
-## HStoreField
+### HStoreField
 
 A preconfigured `DictField` that is compatible with Django's postgres `HStoreField`.
 
@@ -520,7 +519,7 @@ A preconfigured `DictField` that is compatible with Django's postgres `HStoreFie
 
 Note that the child field **must** be an instance of `CharField`, as the hstore extension stores values as strings.
 
-## JSONField
+### JSONField
 
 A field class that validates that the incoming data structure consists of valid JSON primitives. In its alternate binary mode, it will represent and validate JSON-encoded binary strings.
 
@@ -531,9 +530,9 @@ A field class that validates that the incoming data structure consists of valid
 
 ---
 
-# Miscellaneous fields
+## Miscellaneous fields
 
-## ReadOnlyField
+### ReadOnlyField
 
 A field class that simply returns the value of the field without modification.
 
@@ -548,7 +547,7 @@ For example, if `has_expired` was a property on the `Account` model, then the fo
             model = Account
             fields = ['id', 'account_name', 'has_expired']
 
-## HiddenField
+### HiddenField
 
 A field class that does not take a value based on user input, but instead takes its value from a default value or callable.
 
@@ -565,7 +564,7 @@ For further examples on `HiddenField` see the [validators](validators.md) docume
 !!! note
     `HiddenField()` does not appear in `partial=True` serializer (when making `PATCH` request).
 
-## ModelField
+### ModelField
 
 A generic field that can be tied to any arbitrary model field. The `ModelField` class delegates the task of serialization/deserialization to its associated model field.  This field can be used to create serializer fields for custom model fields, without having to create a new custom serializer field.
 
@@ -575,7 +574,7 @@ This field is used by `ModelSerializer` to correspond to custom model field clas
 
 The `ModelField` class is generally intended for internal use, but can be used by your API if needed.  In order to properly instantiate a `ModelField`, it must be passed a field that is attached to an instantiated model.  For example: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`
 
-## SerializerMethodField
+### SerializerMethodField
 
 This is a read-only field. It gets its value by calling a method on the serializer class it is attached to. It can be used to add any sort of data to the serialized representation of your object.
 
@@ -601,7 +600,7 @@ The serializer method referred to by the `method_name` argument should accept a
 
 ---
 
-# Custom fields
+## Custom fields
 
 If you want to create a custom field, you'll need to subclass `Field` and then override either one or both of the `.to_representation()` and `.to_internal_value()` methods.  These two methods are used to convert between the initial datatype, and a primitive, serializable datatype. Primitive datatypes will typically be any of a number, string, boolean, `date`/`time`/`datetime` or `None`. They may also be any list or dictionary like object that only contains other primitive objects. Other types might be supported, depending on the renderer that you are using.
 
@@ -609,9 +608,9 @@ The `.to_representation()` method is called to convert the initial datatype into
 
 The `.to_internal_value()` method is called to restore a primitive datatype into its internal python representation. This method should raise a `serializers.ValidationError` if the data is invalid.
 
-## Examples
+### Examples
 
-### A Basic Custom Field
+#### A Basic Custom Field
 
 Let's look at an example of serializing a class that represents an RGB color value:
 
@@ -652,7 +651,7 @@ As an example, let's create a field that can be used to represent the class name
             """
             return value.__class__.__name__
 
-### Raising validation errors
+#### Raising validation errors
 
 Our `ColorField` class above currently does not perform any data validation.
 To indicate invalid data, we should raise a `serializers.ValidationError`, like so:
@@ -698,7 +697,7 @@ The `.fail()` method is a shortcut for raising `ValidationError` that takes a me
 
 This style keeps your error messages cleaner and more separated from your code, and should be preferred.
 
-### Using `source='*'`
+#### Using `source='*'`
 
 Here we'll take an example of a _flat_ `DataPoint` model with `x_coordinate` and `y_coordinate` attributes.
 
@@ -829,30 +828,26 @@ would use the custom field approach when the nested serializer becomes infeasibl
 or overly complex.
 
 
-# Third party packages
+## Third party packages
 
 The following third party packages are also available.
 
-## DRF Compound Fields
+### DRF Compound Fields
 
 The [drf-compound-fields][drf-compound-fields] package provides "compound" serializer fields, such as lists of simple values, which can be described by other fields rather than serializers with the `many=True` option. Also provided are fields for typed dictionaries and values that can be either a specific type or a list of items of that type.
 
-## DRF Extra Fields
+### DRF Extra Fields
 
 The [drf-extra-fields][drf-extra-fields] package provides extra serializer fields for REST framework, including `Base64ImageField` and `PointField` classes.
 
-## djangorestframework-recursive
+### djangorestframework-recursive
 
 the [djangorestframework-recursive][djangorestframework-recursive] package provides a `RecursiveField` for serializing and deserializing recursive structures
 
-## django-rest-framework-gis
+### django-rest-framework-gis
 
 The [django-rest-framework-gis][django-rest-framework-gis] package provides geographic addons for django rest framework like a `GeometryField` field and a GeoJSON serializer.
 
-## django-rest-framework-hstore
-
-The [django-rest-framework-hstore][django-rest-framework-hstore] package provides an `HStoreField` to support [django-hstore][django-hstore] `DictionaryField` model field.
-
 [cite]: https://docs.djangoproject.com/en/stable/ref/forms/api/#django.forms.Form.cleaned_data
 [html-and-forms]: ../topics/html-and-forms.md
 [FILE_UPLOAD_HANDLERS]: https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS
@@ -862,8 +857,6 @@ The [django-rest-framework-hstore][django-rest-framework-hstore] package provide
 [drf-extra-fields]: https://github.com/Hipo/drf-extra-fields
 [djangorestframework-recursive]: https://github.com/heywbj/django-rest-framework-recursive
 [django-rest-framework-gis]: https://github.com/djangonauts/django-rest-framework-gis
-[django-rest-framework-hstore]: https://github.com/djangonauts/django-rest-framework-hstore
-[django-hstore]: https://github.com/djangonauts/django-hstore
 [python-decimal-rounding-modes]: https://docs.python.org/3/library/decimal.html#rounding-modes
 [django-current-timezone]: https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone
 [django-docs-select-related]: https://docs.djangoproject.com/en/stable/ref/models/querysets/#django.db.models.query.QuerySet.select_related
```


 - `.reference/api-guide/relations.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -42,7 +42,7 @@ Relational fields are used to represent model relationships.  They can be applie
     
     would solve the issue.
 
-#### Inspecting relationships.
+## Inspecting relationships.
 
 When using the `ModelSerializer` class, serializer fields and relationships will be automatically generated for you. Inspecting these automatically generated fields can be a useful tool for determining how to customize the relationship style.
 
@@ -56,7 +56,7 @@ To do so, open the Django shell, using `python manage.py shell`, then import the
         name = CharField(allow_blank=True, max_length=100, required=False)
         owner = PrimaryKeyRelatedField(queryset=User.objects.all())
 
-# API Reference
+## API Reference
 
 In order to explain the various types of relational fields, we'll use a couple of simple models for our examples.  Our models will be for music albums, and the tracks listed on each album.
 
@@ -77,7 +77,7 @@ In order to explain the various types of relational fields, we'll use a couple o
         def __str__(self):
             return '%d: %s' % (self.order, self.title)
 
-## StringRelatedField
+### StringRelatedField
 
 `StringRelatedField` may be used to represent the target of the relationship using its `__str__` method.
 
@@ -109,7 +109,7 @@ This field is read only.
 
 * `many` - If applied to a to-many relationship, you should set this argument to `True`.
 
-## PrimaryKeyRelatedField
+### PrimaryKeyRelatedField
 
 `PrimaryKeyRelatedField` may be used to represent the target of the relationship using its primary key.
 
@@ -145,7 +145,7 @@ By default this field is read-write, although you can change this behavior using
 * `pk_field` - Set to a field to control serialization/deserialization of the primary key's value. For example, `pk_field=UUIDField(format='hex')` would serialize a UUID primary key into its compact hex representation.
 
 
-## HyperlinkedRelatedField
+### HyperlinkedRelatedField
 
 `HyperlinkedRelatedField` may be used to represent the target of the relationship using a hyperlink.
 
@@ -194,7 +194,7 @@ By default this field is read-write, although you can change this behavior using
 * `lookup_url_kwarg` - The name of the keyword argument defined in the URL conf that corresponds to the lookup field. Defaults to using the same value as `lookup_field`.
 * `format` - If using format suffixes, hyperlinked fields will use the same format suffix for the target unless overridden by using the `format` argument.
 
-## SlugRelatedField
+### SlugRelatedField
 
 `SlugRelatedField` may be used to represent the target of the relationship using a field on the target.
 
@@ -235,7 +235,7 @@ When using `SlugRelatedField` as a read-write field, you will normally want to e
 * `many` - If applied to a to-many relationship, you should set this argument to `True`.
 * `allow_null` - If set to `True`, the field will accept values of `None` or the empty string for nullable relationships. Defaults to `False`.
 
-## HyperlinkedIdentityField
+### HyperlinkedIdentityField
 
 This field can be applied as an identity relationship, such as the `'url'` field on a HyperlinkedModelSerializer.  It can also be used for an attribute on the object.  For example, the following serializer:
 
@@ -265,7 +265,7 @@ This field is always read-only.
 
 ---
 
-# Nested relationships
+## Nested relationships
 
 As opposed to previously discussed _references_ to another entity, the referred entity can instead also be embedded or _nested_
 in the representation of the object that refers to it.
@@ -273,7 +273,7 @@ Such nested relationships can be expressed by using serializers as fields.
 
 If the field is used to represent a to-many relationship, you should add the `many=True` flag to the serializer field.
 
-## Example
+### Example
 
 For example, the following serializer:
 
@@ -311,7 +311,7 @@ Would serialize to a nested representation like this:
         ],
     }
 
-## Writable nested serializers
+### Writable nested serializers
 
 By default nested serializers are read-only. If you want to support write-operations to a nested serializer field you'll need to create `create()` and/or `update()` methods in order to explicitly specify how the child relationships should be saved:
 
@@ -351,7 +351,7 @@ By default nested serializers are read-only. If you want to support write-operat
 
 ---
 
-# Custom relational fields
+## Custom relational fields
 
 In rare cases where none of the existing relational styles fit the representation you need,
 you can implement a completely custom relational field, that describes exactly how the
@@ -363,7 +363,7 @@ If you want to implement a read-write relational field, you must also implement
 
 To provide a dynamic queryset based on the `context`, you can also override `.get_queryset(self)` instead of specifying `.queryset` on the class or when initializing the field.
 
-## Example
+### Example
 
 For example, we could define a relational field to serialize a track to a custom string representation, using its ordering, title, and duration:
 
@@ -396,7 +396,7 @@ This custom field would then serialize to the following representation:
 
 ---
 
-# Custom hyperlinked fields
+## Custom hyperlinked fields
 
 In some cases you may need to customize the behavior of a hyperlinked field, in order to represent URLs that require more than a single lookup field.
 
@@ -417,7 +417,7 @@ The return value of this method should the object that corresponds to the matche
 
 May raise an `ObjectDoesNotExist` exception.
 
-## Example
+### Example
 
 Say we have a URL for a customer object that takes two keyword arguments, like so:
 
@@ -455,9 +455,9 @@ Generally we recommend a flat style for API representations where possible, but
 
 ---
 
-# Further notes
+## Further notes
 
-## The `queryset` argument
+### The `queryset` argument
 
 The `queryset` argument is only ever required for *writable* relationship field, in which case it is used for performing the model instance lookup, that maps from the primitive user input, into a model instance.
 
@@ -467,7 +467,7 @@ This behavior is now replaced with *always* using an explicit `queryset` argumen
 
 Doing so reduces the amount of hidden 'magic' that `ModelSerializer` provides, makes the behavior of the field more clear, and ensures that it is trivial to move between using the `ModelSerializer` shortcut, or using fully explicit `Serializer` classes.
 
-## Customizing the HTML display
+### Customizing the HTML display
 
 The built-in `__str__` method of the model will be used to generate string representations of the objects used to populate the `choices` property. These choices are used to populate select HTML inputs in the browsable API.
 
@@ -477,7 +477,7 @@ To provide customized representations for such inputs, override `display_value()
         def display_value(self, instance):
             return 'Track: %s' % (instance.title)
 
-## Select field cutoffs
+### Select field cutoffs
 
 When rendered in the browsable API relational fields will default to only displaying a maximum of 1000 selectable items. If more items are present then a disabled option with "More than 1000 items…" will be displayed.
 
@@ -498,7 +498,7 @@ In cases where the cutoff is being enforced you may want to instead use a plain
        style={'base_template': 'input.html'}
     )
 
-## Reverse relations
+### Reverse relations
 
 Note that reverse relationships are not automatically included by the `ModelSerializer` and `HyperlinkedModelSerializer` classes.  To include a reverse relationship, you must explicitly add it to the fields list.  For example:
 
@@ -520,7 +520,7 @@ If you have not set a related name for the reverse relationship, you'll need to
 
 See the Django documentation on [reverse relationships][reverse-relationships] for more details.
 
-## Generic relationships
+### Generic relationships
 
 If you want to serialize a generic foreign key, you need to define a custom field, to determine explicitly how you want to serialize the targets of the relationship.
 
@@ -594,7 +594,7 @@ Note that reverse generic keys, expressed using the `GenericRelation` field, can
 
 For more information see [the Django documentation on generic relations][generic-relations].
 
-## ManyToManyFields with a Through Model
+### ManyToManyFields with a Through Model
 
 By default, relational fields that target a ``ManyToManyField`` with a
 ``through`` model specified are set to read-only.
@@ -607,15 +607,15 @@ If you wish to represent [extra fields on a through model][django-intermediary-m
 
 ---
 
-# Third Party Packages
+## Third Party Packages
 
 The following third party packages are also available.
 
-## DRF Nested Routers
+### DRF Nested Routers
 
 The [drf-nested-routers package][drf-nested-routers] provides routers and relationship fields for working with nested resources.
 
-## Rest Framework Generic Relations
+### Rest Framework Generic Relations
 
 The [rest-framework-generic-relations][drf-nested-relations] library provides read/write serialization for generic foreign keys.
```


 - `.reference/api-guide/routers.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -154,9 +154,9 @@ The router will match lookup values containing any characters except slashes and
 
 Note that path converters will be used on all URLs registered in the router, including viewset actions.
 
-# API Guide
+## API Guide
 
-## SimpleRouter
+### SimpleRouter
 
 This router includes routes for the standard set of `list`, `create`, `retrieve`, `update`, `partial_update` and `destroy` actions.  The viewset can also mark additional methods to be routed, using the `@action` decorator.
 
@@ -179,7 +179,7 @@ This behavior can be modified by setting the `trailing_slash` argument to `False
 
 Trailing slashes are conventional in Django, but are not used by default in some other frameworks such as Rails.  Which style you choose to use is largely a matter of preference, although some javascript frameworks may expect a particular routing style.
 
-## DefaultRouter
+### DefaultRouter
 
 This router is similar to `SimpleRouter` as above, but additionally includes a default API root view, that returns a response containing hyperlinks to all the list views.  It also generates routes for optional `.json` style format suffixes.
 
@@ -200,7 +200,7 @@ As with `SimpleRouter` the trailing slashes on the URL routes can be removed by
 
     router = DefaultRouter(trailing_slash=False)
 
-# Custom Routers
+## Custom Routers
 
 Implementing a custom router isn't something you'd need to do very often, but it can be useful if you have specific requirements about how the URLs for your API are structured.  Doing so allows you to encapsulate the URL structure in a reusable way that ensures you don't have to write your URL patterns explicitly for each new view.
 
@@ -222,7 +222,7 @@ The arguments to the `Route` named tuple are:
 
 **initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view.  Note that the `detail`, `basename`, and `suffix` arguments are reserved for viewset introspection and are also used by the browsable API to generate the view name and breadcrumb links.
 
-## Customizing dynamic routes
+### Customizing dynamic routes
 
 You can also customize how the `@action` decorator is routed. Include the `DynamicRoute` named tuple in the `.routes` list, setting the `detail` argument as appropriate for the list-based and detail-based routes. In addition to `detail`, the arguments to `DynamicRoute` are:
 
@@ -235,7 +235,7 @@ You can also customize how the `@action` decorator is routed. Include the `Dynam
 
 **initkwargs**: A dictionary of any additional arguments that should be passed when instantiating the view.
 
-## Example
+### Example
 
 The following example will only route to the `list` and `retrieve` actions, and does not use the trailing slash convention.
 
@@ -307,21 +307,21 @@ The following mappings would be generated...
 
 For another example of setting the `.routes` attribute, see the source code for the `SimpleRouter` class.
 
-## Advanced custom routers
+### Advanced custom routers
 
 If you want to provide totally custom behavior, you can override `BaseRouter` and override the `get_urls(self)` method.  The method should inspect the registered viewsets and return a list of URL patterns.  The registered prefix, viewset and basename tuples may be inspected by accessing the `self.registry` attribute.
 
 You may also want to override the `get_default_basename(self, viewset)` method, or else always explicitly set the `basename` argument when registering your viewsets with the router.
 
-# Third Party Packages
+## Third Party Packages
 
 The following third party packages are also available.
 
-## DRF Nested Routers
+### DRF Nested Routers
 
 The [drf-nested-routers package][drf-nested-routers] provides routers and relationship fields for working with nested resources.
 
-## ModelRouter (wq.db.rest)
+### ModelRouter (wq.db.rest)
 
 The [wq.db package][wq.db] provides an advanced [ModelRouter][wq.db-router] class (and singleton instance) that extends `DefaultRouter` with a `register_model()` API. Much like Django's `admin.site.register`, the only required argument to `rest.router.register_model` is a model class.  Reasonable defaults for a url prefix, serializer, and viewset will be inferred from the model and global configuration.
 
@@ -330,7 +330,7 @@ The [wq.db package][wq.db] provides an advanced [ModelRouter][wq.db-router] clas
 
     rest.router.register_model(MyModel)
 
-## DRF-extensions
+### DRF-extensions
 
 The [`DRF-extensions` package][drf-extensions] provides [routers][drf-extensions-routers] for creating [nested viewsets][drf-extensions-nested-viewsets], [collection level controllers][drf-extensions-collection-level-controllers] with [customizable endpoint names][drf-extensions-customizable-endpoint-names].
```


 - `.reference/api-guide/throttling.md`
```
d0a5d5e7cad7f1032b4d0a36cab1596076f705ad -> f56ec9546c846acddde7013cfc3aae9ddc40c6f0
@@ -114,9 +114,9 @@ If your project relies on guaranteeing the number of requests during concurrent
 
 ---
 
-# API Reference
+## API Reference
 
-## AnonRateThrottle
+### AnonRateThrottle
 
 The `AnonRateThrottle` will only ever throttle unauthenticated users.  The IP address of the incoming request is used to generate a unique key to throttle against.
 
@@ -127,7 +127,7 @@ The allowed request rate is determined from one of the following (in order of pr
 
 `AnonRateThrottle` is suitable if you want to restrict the rate of requests from unknown sources.
 
-## UserRateThrottle
+### UserRateThrottle
 
 The `UserRateThrottle` will throttle users to a given rate of requests across the API.  The user id is used to generate a unique key to throttle against.  Unauthenticated requests will fall back to using the IP address of the incoming request to generate a unique key to throttle against.
 
@@ -161,7 +161,7 @@ For example, multiple user throttle rates could be implemented by using the foll
 
 `UserRateThrottle` is suitable if you want simple global rate restrictions per-user.
 
-## ScopedRateThrottle
+### ScopedRateThrottle
 
 The `ScopedRateThrottle` class can be used to restrict access to specific parts of the API.  This throttle will only be applied if the view that is being accessed includes a `.throttle_scope` property.  The unique throttle key will then be formed by concatenating the "scope" of the request with the unique user id or IP address.
 
@@ -197,7 +197,7 @@ User requests to either `ContactListView` or `ContactDetailView` would be restri
 
 ---
 
-# Custom throttles
+## Custom throttles
 
 To create a custom throttle, override `BaseThrottle` and implement `.allow_request(self, request, view)`.  The method should return `True` if the request should be allowed, and `False` otherwise.
 
@@ -205,7 +205,7 @@ Optionally you may also override the `.wait()` method.  If implemented, `.wait()
 
 If the `.wait()` method is implemented and the request is throttled, then a `Retry-After` header will be included in the response.
 
-## Example
+### Example
 
 The following is an example of a rate throttle, that will randomly throttle 1 in every 10 requests.
```


 - `.reference/tutorial/1-serialization.md`
```
e221d9a1d6638b936707efc390adff59511a6605 -> 190aae3c2d824b19ff668bf1f06a3dff7aa05ab8
@@ -11,12 +11,23 @@ The tutorial is fairly in-depth, so you should probably get a cookie and a cup o
 
 ## Setting up a new environment
 
-Before we do anything else we'll create a new virtual environment, using [venv]. This will make sure our package configuration is kept nicely isolated from any other projects we're working on.
+Before we do anything else we'll create a new virtual environment called `.venv`, using [venv]. This will make sure our package configuration is kept nicely isolated from any other projects we're working on.
 
-```bash
-python3 -m venv env
-source env/bin/activate
-```
+=== ":fontawesome-brands-linux: Linux, :fontawesome-brands-apple: macOS"
+
+    ```bash
+    python3 -m venv .venv
+    source .venv/bin/activate
+    ```
+
+=== ":fontawesome-brands-windows: Windows"
+
+    If you use Bash for Windows
+
+    ```bash
+    python3 -m venv .venv
+    source .venv\Scripts\activate
+    ```
 
 Now that we're inside a virtual environment, we can install our package requirements.
 
@@ -217,6 +228,10 @@ Let's look at refactoring our serializer using the `ModelSerializer` class.
 Open the file `snippets/serializers.py` again, and replace the `SnippetSerializer` class with the following.
 
 ```python
+from rest_framework import serializers
+from snippets.models import Snippet
+
+
 class SnippetSerializer(serializers.ModelSerializer):
     class Meta:
         model = Snippet
@@ -362,9 +377,9 @@ Quit the server with CONTROL-C.
 
 In another terminal window, we can test the server.
 
-We can test our API using [curl][curl] or [httpie][httpie]. Httpie is a user friendly http client that's written in Python. Let's install that.
+We can test our API using [curl][curl] or [HTTPie][HTTPie]. HTTPie is a user-friendly http client that's written in Python. Let's install that.
 
-You can install httpie using pip:
+You can install HTTPie using pip:
 
 ```bash
 pip install httpie
@@ -436,5 +451,5 @@ We'll see how we can start to improve things in [part 2 of the tutorial][tut-2].
 [repo]: https://github.com/encode/rest-framework-tutorial
 [venv]: https://docs.python.org/3/library/venv.html
 [tut-2]: 2-requests-and-responses.md
-[httpie]: https://github.com/httpie/httpie#installation
+[HTTPie]: https://github.com/httpie/httpie#installation
 [curl]: https://curl.haxx.se/
```


 - `.reference/tutorial/quickstart.md`
```
c0f3649224117609d19e79c77242b525570d25c0 -> 190aae3c2d824b19ff668bf1f06a3dff7aa05ab8
@@ -6,24 +6,49 @@ We're going to create a simple API to allow admin users to view and edit the use
 
 Create a new Django project named `tutorial`, then start a new app called `quickstart`.
 
-```bash
-# Create the project directory
-mkdir tutorial
-cd tutorial
-
-# Create a virtual environment to isolate our package dependencies locally
-python3 -m venv env
-source env/bin/activate  # On Windows use `env\Scripts\activate`
-
-# Install Django and Django REST framework into the virtual environment
-pip install djangorestframework
-
-# Set up a new project with a single application
-django-admin startproject tutorial .  # Note the trailing '.' character
-cd tutorial
-django-admin startapp quickstart
-cd ..
-```
+=== ":fontawesome-brands-linux: Linux, :fontawesome-brands-apple: macOS"
+
+    ```bash
+    # Create the project directory
+    mkdir tutorial
+    cd tutorial
+    
+    # Create a virtual environment to isolate our package dependencies locally
+    python3 -m venv .venv
+    source .venv/bin/activate
+    
+    # Install Django and Django REST framework into the virtual environment
+    pip install djangorestframework
+    
+    # Set up a new project with a single application
+    django-admin startproject tutorial .  # Note the trailing '.' character
+    cd tutorial
+    django-admin startapp quickstart
+    cd ..
+    ```
+
+=== ":fontawesome-brands-windows: Windows"
+
+    If you use Bash for Windows
+
+    ```bash
+    # Create the project directory
+    mkdir tutorial
+    cd tutorial
+    
+    # Create a virtual environment to isolate our package dependencies locally
+    python3 -m venv .venv
+    source .venv\Scripts\activate
+    
+    # Install Django and Django REST framework into the virtual environment
+    pip install djangorestframework
+    
+    # Set up a new project with a single application
+    django-admin startproject tutorial .  # Note the trailing '.' character
+    cd tutorial
+    django-admin startapp quickstart
+    cd ..
+    ```
 
 The project layout should look like:
```


 - `.reference/topics/documenting-your-api.md`
```
e794e5e5e43d6838d9ffb8eb0a505b5f531b261f -> c8af56d2600ef25216175d08c2bea053e00cbcff
@@ -4,10 +4,11 @@
 >
 > &mdash; Roy Fielding, [REST APIs must be hypertext driven][cite]
 
-REST framework provides a range of different choices for documenting your API. The following
-is a non-exhaustive list of the most popular ones.
+REST framework provides a range of different choices for documenting your API. The following is a non-exhaustive list of some of the most popular options.
 
-## Third party packages for OpenAPI support
+## Third-party packages for OpenAPI support
+
+REST framework recommends using third-party packages for generating and presenting OpenAPI schemas, as they provide more features and flexibility than the built-in (deprecated) implementation.
 
 ### drf-spectacular
 
@@ -37,9 +38,9 @@ This also translates into a very useful interactive documentation viewer in the
 
 ## Built-in OpenAPI schema generation (deprecated)
 
-**Deprecation notice: REST framework's built-in support for generating OpenAPI schemas is
-deprecated in favor of 3rd party packages that can provide this functionality instead.
-As replacement, we recommend using the [drf-spectacular](#drf-spectacular) package.**
+!!! warning
+    **Deprecation notice:** REST framework's built-in support for generating OpenAPI schemas is deprecated in favor of third-party packages that provide this functionality instead. As a replacement, we recommend using **drf-spectacular**.
+
 
 There are a number of packages available that allow you to generate HTML
 documentation pages from OpenAPI schemas.
```


 - `.reference/README.md`
```
18c5883be8ad3c5c5c36a5e39855d79ac80de7ca -> 021ab5664b085594876032cf062c1220bc1ca03c
@@ -1,3 +1,8 @@
+---
+hide:
+  - navigation
+---
+
 <style>
 .promo li a {
     float: left;
@@ -17,7 +22,7 @@
 }
 </style>
 
-<p class="badges" height=20px>
+<div class="badges">
     <iframe src="https://ghbtns.com/github-btn.html?user=encode&amp;repo=django-rest-framework&amp;type=watch&amp;count=true" class="github-star-button" allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>
 
     <a href="https://github.com/encode/django-rest-framework/actions/workflows/main.yml">
@@ -27,11 +32,10 @@
     <a href="https://pypi.org/project/djangorestframework/">
         <img src="https://img.shields.io/pypi/v/djangorestframework.svg" class="status-badge">
     </a>
-</p>
+</div>
 
 ---
 
-<p>
 <h1 style="position: absolute;
     width: 1px;
     height: 1px;
@@ -41,8 +45,8 @@
     clip: rect(0,0,0,0);
     border: 0;">Django REST Framework</h1>
 
-<img alt="Django REST Framework" title="Logo by Jake 'Sid' Smith" src="img/logo.png" width="600px" style="display: block; margin: 0 auto 0 auto">
-</p>
+![Django REST Framework](img/logo-light.png#only-light)
+![Django REST Framework](img/logo-dark.png#only-dark)
 
 Django REST framework is a powerful and flexible toolkit for building Web APIs.
 
@@ -61,7 +65,7 @@ Some reasons you might want to use REST framework:
 
 REST framework requires the following:
 
-* Django (4.2, 5.0, 5.1, 5.2)
+* Django (4.2, 5.0, 5.1, 5.2, 6.0)
 * Python (3.10, 3.11, 3.12, 3.13, 3.14)
 
 We **highly recommend** and only officially support the latest patch release of
@@ -69,7 +73,7 @@ each Python and Django series.
 
 The following packages are optional:
 
-* [PyYAML][pyyaml], [uritemplate][uriteemplate] (5.1+, 3.0.0+) - Schema generation support.
+* [PyYAML][pyyaml], [uritemplate][uritemplate] (5.1+, 3.0.0+) - Schema generation support.
 * [Markdown][markdown] (3.3.0+) - Markdown support for the browsable API.
 * [Pygments][pygments] (2.7.0+) - Add syntax highlighting to Markdown processing.
 * [django-filter][django-filter] (1.0.1+) - Filtering support.
@@ -79,27 +83,35 @@ The following packages are optional:
 
 Install using `pip`, including any optional packages you want...
 
-    pip install djangorestframework
-    pip install markdown       # Markdown support for the browsable API.
-    pip install django-filter  # Filtering support
+```bash
+pip install djangorestframework
+pip install markdown       # Markdown support for the browsable API.
+pip install django-filter  # Filtering support
+```
 
 ...or clone the project from github.
 
-    git clone https://github.com/encode/django-rest-framework
+```bash
+git clone https://github.com/encode/django-rest-framework
+```
 
 Add `'rest_framework'` to your `INSTALLED_APPS` setting.
 
-    INSTALLED_APPS = [
-        ...
-        'rest_framework',
-    ]
+```python
+INSTALLED_APPS = [
+    # ...
+    "rest_framework",
+]
+```
 
 If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views.  Add the following to your root `urls.py` file.
 
-    urlpatterns = [
-        ...
-        path('api-auth/', include('rest_framework.urls'))
-    ]
+```python
+urlpatterns = [
+    # ...
+    path("api-auth/", include("rest_framework.urls"))
+]
+```
 
 Note that the URL path can be whatever you want.
 
@@ -111,44 +123,51 @@ We'll create a read-write API for accessing information on the users of our proj
 
 Any global settings for a REST framework API are kept in a single configuration dictionary named `REST_FRAMEWORK`.  Start off by adding the following to your `settings.py` module:
 
-    REST_FRAMEWORK = {
-        # Use Django's standard `django.contrib.auth` permissions,
-        # or allow read-only access for unauthenticated users.
-        'DEFAULT_PERMISSION_CLASSES': [
-            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
-        ]
-    }
+```python
+REST_FRAMEWORK = {
+    # Use Django's standard `django.contrib.auth` permissions,
+    # or allow read-only access for unauthenticated users.
+    "DEFAULT_PERMISSION_CLASSES": [
+        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
+    ]
+}
+```
 
 Don't forget to make sure you've also added `rest_framework` to your `INSTALLED_APPS`.
 
 We're ready to create our API now.
 Here's our project's root `urls.py` module:
 
-    from django.urls import path, include
-    from django.contrib.auth.models import User
-    from rest_framework import routers, serializers, viewsets
-
-    # Serializers define the API representation.
-    class UserSerializer(serializers.HyperlinkedModelSerializer):
-        class Meta:
-            model = User
-            fields = ['url', 'username', 'email', 'is_staff']
-
-    # ViewSets define the view behavior.
-    class UserViewSet(viewsets.ModelViewSet):
-        queryset = User.objects.all()
-        serializer_class = UserSerializer
-
-    # Routers provide an easy way of automatically determining the URL conf.
-    router = routers.DefaultRouter()
-    router.register(r'users', UserViewSet)
-
-    # Wire up our API using automatic URL routing.
-    # Additionally, we include login URLs for the browsable API.
-    urlpatterns = [
-        path('', include(router.urls)),
-        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
-    ]
+```python
+from django.urls import path, include
+from django.contrib.auth.models import User
+from rest_framework import routers, serializers, viewsets
+
+
+# Serializers define the API representation.
+class UserSerializer(serializers.HyperlinkedModelSerializer):
+    class Meta:
+        model = User
+        fields = ["url", "username", "email", "is_staff"]
+
+
+# ViewSets define the view behavior.
+class UserViewSet(viewsets.ModelViewSet):
+    queryset = User.objects.all()
+    serializer_class = UserSerializer
+
+
+# Routers provide an easy way of automatically determining the URL conf.
+router = routers.DefaultRouter()
+router.register(r"users", UserViewSet)
+
+# Wire up our API using automatic URL routing.
+# Additionally, we include login URLs for the browsable API.
+urlpatterns = [
+    path("", include(router.urls)),
+    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
+]
+```
 
 You can now open the API in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/), and view your new 'users' API. If you use the login control in the top right corner you'll also be able to add, create and delete users from the system.
 
@@ -207,7 +226,7 @@ OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 [heroku]: https://www.heroku.com/
 [eventbrite]: https://www.eventbrite.co.uk/about/
 [pyyaml]: https://pypi.org/project/PyYAML/
-[uriteemplate]: https://pypi.org/project/uritemplate/
+[uritemplate]: https://pypi.org/project/uritemplate/
 [markdown]: https://pypi.org/project/Markdown/
 [pygments]: https://pypi.org/project/Pygments/
 [django-filter]: https://pypi.org/project/django-filter/
```


