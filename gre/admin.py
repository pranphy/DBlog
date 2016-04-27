from django.contrib import admin

from .models import Tag 
from .models import Vocab 
from .models import Source
from .models import VcVocab 
from .models import VcSentence 

admin.site.register(Tag)
admin.site.register(Vocab)
admin.site.register(Source)
admin.site.register(VcVocab)
admin.site.register(VcSentence)
admin.site.register(Source.Type)
