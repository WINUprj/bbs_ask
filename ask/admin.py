from django.contrib import admin
from .models import Question, Comment, Reply

# Register your models here.

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('title', 'question')
    list_display = ['title', 'update_date', 'posted_date']
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)