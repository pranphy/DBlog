from django.contrib import admin
from .models import News
from .models import NavigationItems
from .models import BlogPost


admin.site.register(News)
admin.site.register(NavigationItems)
admin.site.register(BlogPost)
