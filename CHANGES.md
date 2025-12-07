Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)

 - `.reference/api-guide/serializers.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> 40172399afcc60510a78bdae39818ee6686b72e4
@@ -430,7 +430,7 @@ The context dictionary can be used within any serializer field logic, such as a
 
 Often you'll want serializer classes that map closely to Django model definitions.
 
-The `ModelSerializer` class provides a shortcut that let's you automatically create a `Serializer` class with fields that correspond to the Model fields.
+The `ModelSerializer` class provides a shortcut that lets you automatically create a `Serializer` class with fields that correspond to the Model fields.
 
 **The `ModelSerializer` class is the same as a regular `Serializer` class, except that**:
 
@@ -708,7 +708,7 @@ You can override a URL field view name and lookup field by using either, or both
     class AccountSerializer(serializers.HyperlinkedModelSerializer):
         class Meta:
             model = Account
-            fields = ['account_url', 'account_name', 'users', 'created']
+            fields = ['url', 'account_name', 'users', 'created']
             extra_kwargs = {
                 'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
                 'users': {'lookup_field': 'username'}
```



 - `.reference/api-guide/authentication.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> 442444f0bedc55af7ea1fcdc5755a343de1b1c57
@@ -416,7 +416,7 @@ JSON Web Token is a fairly new standard which can be used for token-based authen
 
 ## Hawk HTTP Authentication
 
-The [HawkREST][hawkrest] library builds on the [Mohawk][mohawk] library to let you work with [Hawk][hawk] signed requests and responses in your API. [Hawk][hawk] let's two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication][mac] (which was based on parts of [OAuth 1.0][oauth-1.0a]).
+The [HawkREST][hawkrest] library builds on the [Mohawk][mohawk] library to let you work with [Hawk][hawk] signed requests and responses in your API. [Hawk][hawk] lets two parties securely communicate with each other using messages signed by a shared key. It is based on [HTTP MAC access authentication][mac] (which was based on parts of [OAuth 1.0][oauth-1.0a]).
 
 ## HTTP Signature Authentication
```



 - `.reference/api-guide/settings.md`

```
c8b6d3dcdf0a9fe04eb914e29e18efa42fe59a6c -> f9f10e041f9b2a2c936ee54a437d4c255f76e626
@@ -371,6 +371,14 @@ When set to `True`, the serializer `DecimalField` class will return strings inst
 
 Default: `True`
 
+#### COERCE_BIGINT_TO_STRING
+
+When returning biginteger objects in API representations that do not support numbers up to 2^64, it is best to return the value as a string. This avoids the loss of precision that occurs with biginteger implementations.
+
+When set to `True`, the serializer `BigIntegerField` class (by default) will return strings instead of `BigInteger` objects. When set to `False`, serializers will return `BigInteger` objects, which the default JSON encoder will return as numbers.
+
+Default: `False`
+
 ---
 
 ## View names and descriptions
```



 - `.reference/api-guide/permissions.md`

```
70e54f45add6a96f92bbadbcff30fc211f2ce0c3 -> 363dbba4137fe488f33ed24e0a9025228e66301f
@@ -340,6 +340,10 @@ The [Django Rest Framework Role Filters][django-rest-framework-role-filters] pac
 
 The [Django Rest Framework PSQ][drf-psq] package is an extension that gives support for having action-based **permission_classes**, **serializer_class**, and **queryset** dependent on permission-based rules.
 
+## Axioms DRF PY
+
+The [Axioms DRF PY][axioms-drf-py] package is an extension that provides support for authentication and claim-based fine-grained authorization (**scopes**, **roles**, **groups**, **permissions**, etc. including object-level checks) using JWT tokens issued by an OAuth2/OIDC Authorization Server including AWS Cognito, Auth0, Okta, Microsoft Entra, etc.
+
 
 [cite]: https://developer.apple.com/library/mac/#documentation/security/Conceptual/AuthenticationAndAuthorizationGuide/Authorization/Authorization.html
 [authentication]: authentication.md
@@ -359,3 +363,4 @@ The [Django Rest Framework PSQ][drf-psq] package is an extension that gives supp
 [django-rest-framework-guardian]: https://github.com/rpkilby/django-rest-framework-guardian
 [drf-access-policy]: https://github.com/rsinger86/drf-access-policy
 [drf-psq]: https://github.com/drf-psq/drf-psq
+[axioms-drf-py]: https://github.com/abhishektiwari/axioms-drf-py
```



 - `.reference/api-guide/fields.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> f9f10e041f9b2a2c936ee54a437d4c255f76e626
@@ -269,6 +269,18 @@ Corresponds to `django.db.models.fields.IntegerField`, `django.db.models.fields.
 * `max_value` Validate that the number provided is no greater than this value.
 * `min_value` Validate that the number provided is no less than this value.
 
+## BigIntegerField
+
+A biginteger representation.
+
+Corresponds to `django.db.models.fields.BigIntegerField`.
+
+**Signature**: `BigIntegerField(max_value=None, min_value=None, coerce_to_string=None)`
+
+* `max_value` Validate that the number provided is no greater than this value.
+* `min_value` Validate that the number provided is no less than this value.
+* `coerce_to_string` Set to `True` if string values should be returned for the representation, or `False` if `BigInteger` objects should be returned. Defaults to the same value as the `COERCE_BIGINT_TO_STRING` settings key, which will be `False` unless overridden. If `BigInteger` objects are returned by the serializer, then the final output format will be determined by the renderer.
+
 ## FloatField
 
 A floating point representation.
```



 - `.reference/README.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> 18c5883be8ad3c5c5c36a5e39855d79ac80de7ca
@@ -57,32 +57,6 @@ Some reasons you might want to use REST framework:
 
 ---
 
-## Funding
-
-REST framework is a *collaboratively funded project*. If you use
-REST framework commercially we strongly encourage you to invest in its
-continued development by **[signing up for a paid plan][funding]**.
-
-*Every single sign-up helps us make REST framework long-term financially sustainable.*
-
-<ul class="premium-promo promo">
-    <li><a href="https://getsentry.com/welcome/" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/sentry130.png)">Sentry</a></li>
-    <li><a href="https://getstream.io/?utm_source=DjangoRESTFramework&utm_medium=Webpage_Logo_Ad&utm_content=Developer&utm_campaign=DjangoRESTFramework_Jan2022_HomePage" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/stream-130.png)">Stream</a></li>
-    <li><a href="https://www.spacinov.com/" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/spacinov.png)">Spacinov</a></li>
-    <li><a href="https://retool.com/?utm_source=djangorest&utm_medium=sponsorship" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/retool-sidebar.png)">Retool</a></li>
-    <li><a href="https://bit.io/jobs?utm_source=DRF&utm_medium=sponsor&utm_campaign=DRF_sponsorship" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/bitio_logo_gold_background.png)">bit.io</a></li>
-    <li><a href="https://posthog.com?utm_source=DRF&utm_medium=sponsor&utm_campaign=DRF_sponsorship" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/135996800-d49fe024-32d9-441a-98d9-4c7596287a67.png)">PostHog</a></li>
-    <li><a href="https://cryptapi.io" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/cryptapi.png)">CryptAPI</a></li>
-    <li><a href="https://www.fezto.xyz/?utm_source=DjangoRESTFramework" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/fezto.png)">FEZTO</a></li>
-    <li><a href="https://www.svix.com/?utm_source=django-REST&utm_medium=sponsorship" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/svix.png)">Svix</a></li>
-    <li><a href="https://zuplo.link/django-web" style="background-image: url(https://fund-rest-framework.s3.amazonaws.com/zuplo.png)">Zuplo</a></li>
-</ul>
-<div style="clear: both; padding-bottom: 20px;"></div>
-
-*Many thanks to all our [wonderful sponsors][sponsors], and in particular to our premium backers, [Sentry](https://getsentry.com/welcome/), [Stream](https://getstream.io/?utm_source=DjangoRESTFramework&utm_medium=Webpage_Logo_Ad&utm_content=Developer&utm_campaign=DjangoRESTFramework_Jan2022_HomePage), [Spacinov](https://www.spacinov.com/), [Retool](https://retool.com/?utm_source=djangorest&utm_medium=sponsorship), [bit.io](https://bit.io/jobs?utm_source=DRF&utm_medium=sponsor&utm_campaign=DRF_sponsorship), [PostHog](https://posthog.com?utm_source=DRF&utm_medium=sponsor&utm_campaign=DRF_sponsorship), [CryptAPI](https://cryptapi.io), [FEZTO](https://www.fezto.xyz/?utm_source=DjangoRESTFramework), [Svix](https://www.svix.com/?utm_source=django-REST&utm_medium=sponsorship), , and [Zuplo](https://zuplo.link/django-web).*
-
----
-
 ## Requirements
 
 REST framework requires the following:
@@ -192,8 +166,6 @@ Framework.
 
 For support please see the [REST framework discussion group][group], try the `#restframework` channel on `irc.libera.chat`, or raise a question on [Stack Overflow][stack-overflow], making sure to include the ['django-rest-framework'][django-rest-framework-tag] tag.
 
-For priority support please sign up for a [professional or premium sponsorship plan](https://fund.django-rest-framework.org/topics/funding/).
-
 ## Security
 
 **Please report security issues by emailing security@encode.io**.
@@ -246,7 +218,6 @@ OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 [serializer-section]: api-guide/serializers#serializers
 [modelserializer-section]: api-guide/serializers#modelserializer
 [functionview-section]: api-guide/views#function-based-views
-[sponsors]: https://fund.django-rest-framework.org/topics/funding/#our-sponsors
 
 [quickstart]: tutorial/quickstart.md
 
@@ -257,10 +228,8 @@ OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 [authentication]: api-guide/authentication.md
 
 [contributing]: community/contributing.md
-[funding]: community/funding.md
 
 [group]: https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework
 [stack-overflow]: https://stackoverflow.com/
 [django-rest-framework-tag]: https://stackoverflow.com/questions/tagged/django-rest-framework
 [security-mail]: mailto:rest-framework-security@googlegroups.com
-[twitter]: https://twitter.com/_tomchristie
```


