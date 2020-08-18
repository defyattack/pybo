from django.contrib import admin

# Register your models here.
from .models import Category,Question,Answer,Comment

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['cname']

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)

