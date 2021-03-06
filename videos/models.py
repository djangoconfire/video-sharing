from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from courses.utils import create_slug
# Create your models here.

class Video(models.Model):
	title				=models.CharField(max_length=100,null=True)
	slug				=models.SlugField(blank=True)
	embed_code			=models.TextField()
	free				=models.BooleanField(default=True)
	member_required		=models.BooleanField(default=False)
	updated				=models.DateTimeField(auto_now=True,null=True)
	timestamp			=models.DateTimeField(auto_now_add=True,null=True)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("videos:detail",kwargs={"slug":self.slug})	

def pre_save_video_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)
pre_save.connect(pre_save_video_receiver,sender=Video)			