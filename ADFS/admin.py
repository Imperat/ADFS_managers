from django.contrib import admin
from django.contrib.auth.models import User

from .models import Attention, ADFSUser


admin.site.register(Attention)

admin.site.unregister(User)
admin.site.register(ADFSUser)
