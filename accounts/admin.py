from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Moderator)
admin.site.register(Visitor)
admin.site.register(Token)
