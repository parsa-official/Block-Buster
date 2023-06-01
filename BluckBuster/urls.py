from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('user/', include('account.urls', namespace='account')),
    path('movies/', include('cinema.urls', namespace='cinema')),
    path('series/', include('television.urls', namespace='television')),
    path('celebs/', include('people.urls', namespace='people')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'blog.views.custom_404_view'