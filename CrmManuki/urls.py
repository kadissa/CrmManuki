from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings


handler404 = "core.views.page_not_found"
handler403 = "core.views.permission_denied"
handler500 = "core.views.server_error"

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("easyweek/", include("webhooks.urls")),
    path("crm/", include("bnovo.urls")),
    path("order/", include("bath.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
