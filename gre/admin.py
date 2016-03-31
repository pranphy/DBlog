from django.contrib import admin

from .models import Tag 
from .models import Vocab 
from .models import Source

admin.site.register(Tag)
admin.site.register(Vocab)
admin.site.register(Source)
admin.site.register(Source.Type)
