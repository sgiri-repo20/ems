from django.contrib import admin
from poll.models import Questions, Choice, Answer

# Register your models here.
admin.site.register(Questions)
admin.site.register(Choice)
admin.site.register(Answer)
