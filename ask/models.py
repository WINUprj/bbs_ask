from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Question(models.Model):
	user = models.CharField(max_length=50)
	title = models.CharField(max_length=200)

	question = models.TextField()
	update_date = models.DateTimeField(default=timezone.now)
	posted_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('ask:question_detail', kwargs={'pk':self.pk})

class Comment(models.Model):
	user = models.CharField(max_length=50)
	text = models.TextField()
	post = models.ForeignKey(Question, verbose_name='target_post', on_delete=models.CASCADE)
	parent = models.ForeignKey('self', verbose_name='parent_comment', null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.text
	
class Reply(models.Model):
	name = models.CharField(max_length=50)
	text = models.TextField()
	target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='target_comment')
	created_at = models.DateTimeField('created_date', default=timezone.now)

	def __str__(self):
		return self.text[:30]
