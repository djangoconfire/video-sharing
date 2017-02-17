from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from utils import create_slug,make_display_price
from videos.models import Video
from django.db.models import Prefetch

# My Courses
class MyCourses(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    courses         = models.ManyToManyField('Course',related_name="owned", blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.courses.all().count()

    class Meta:
        verbose_name = 'My courses'
        verbose_name_plural = 'My courses'

def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)


class CourseQuerySet(models.query.QuerySet):

	def active(self):
		return self.filter(active=True)

	def owned(self,user):
		return self.prefetch_related(
				Prefetch('owned',
						  queryset=MyCourses.objects.filter(user=user),
						  to_attr='is_owner'

				)
			)

class CourseManager(models.Manager):
	def get_queryset(self):
		return CourseQuerySet(self.model,using=self._db)

	def all(self):
		return self.get_queryset().all().active()	 				

# Course Model
class Course(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2,max_digits=6)
    updated         = models.DateTimeField(auto_now=True)
    active 			= models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects=CourseManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	return reverse("courses:detail",kwargs={"slug":self.slug})

    def get_purchase_url(self):
    	return reverse("courses:purchase",kwargs={'slug':self.slug})	 

    def display_price(self):
    	return make_display_price(self.price)	   


# Lecture model
class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True) # unique = False
    description     = models.TextField()
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
    	unique_together=(('slug','course'),)    

    def get_absolute_url(self):
		return reverse("courses:lecture-detail", 
						kwargs={"cslug": self.course.slug,
								 "lslug": self.slug})

def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_video_receiver, sender=Course)