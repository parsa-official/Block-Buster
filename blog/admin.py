from django.contrib import admin
from .models import Trailer,BlogArticle,BlogCategory

admin.site.register(Trailer)
admin.site.register(BlogCategory)
admin.site.register(BlogArticle)