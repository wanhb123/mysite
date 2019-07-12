from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'choice_text', 'question_id', 'votes')
    search_fields = ('question_text',)
    list_filter = ['question_text']
    list_per_page = 1


admin.site.register([Question, Choice])