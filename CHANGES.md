Sync with [original](https://github.com/encode/django-rest-framework/tree/main/docs)

 - `.reference/api-guide/testing.md`

```
ade172e1d5db87dc86bc616cbb4df7ccd2eb2fd3 -> 365d409adb43ebad7d8a42cab2407ec841d8038e
@@ -353,6 +353,7 @@ REST framework also provides a test case class for isolating `urlpatterns` on a
 ## Example
 
     from django.urls import include, path, reverse
+    from rest_framework import status
     from rest_framework.test import APITestCase, URLPatternsTestCase
```


