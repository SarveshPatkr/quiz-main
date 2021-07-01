from django.contrib import admin
from .models import *

class AnswerModelAdmin(admin.StackedInline):
    model = AnswerModel

class QuestionModelAdmin(admin.ModelAdmin):
    inlines = [ AnswerModelAdmin ]

admin.site.register(QuestionModel, QuestionModelAdmin)
admin.site.register(CategoryModel)
admin.site.register(UserModel)
admin.site.register(CreateQuizModel)
admin.site.register(SetQuizModel)
admin.site.register(ShareQuizModel)