from django.shortcuts import render,get_object_or_404
from django.views.generic import (
	CreateView,
	DetailView,
	UpdateView,
	ListView,
	DeleteView
	)
from django.http import Http404
from models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from forms import CourseForm


# Create
class CourseCreateView(StaffMemberRequiredMixin,CreateView):
	model=Course
	form_class=CourseForm
	success_url='/success/'

	def form_valid(self,form):
		obj=form.save(commit=False)
		obj.user=self.request.user
		obj.save()

		return super(CourseCreateView,self).form_valid(form)


# Lecture Detail
class LectureDetailView(MemberRequiredMixin,DetailView):
	def get_object(self):
		course_slug=self.kwargs.get("cslug")
		lecture_slug=self.kwargs.get("lslug")
		obj=get_object_or_404(Lecture,course__slug=course_slug,slug=lecture_slug)
		return obj


# Detail
class CourseDetailView(MemberRequiredMixin,DetailView):
	queryset=Course.objects.all()

	def get_object(self):
		slug=self.kwargs.get("slug")
		obj=Course.objects.filter(slug=slug)
		if obj.exists():
			return obj.first()
		raise Http404	


# List
class CourseListView(ListView):
	def get_queryset(self):
		request=self.request
		qs=Course.objects.all()
		query=request.GET.get('q')
		if query:
			qs=qs.fiter(title__icontains=query)
		return qs	

# Update
class CourseUpdateView(StaffMemberRequiredMixin,UpdateView):
	queryset=Course.objects.all()
	form_class=CourseForm

	def form_valid(self,form):
		obj=form.save(commit=False)
		if not self.request.user.is_staff:
			obj.user=self.request.user
		obj.save()
		
		return super(CourseUpdateView,self).form_valid(form)	


	def get_object(self):
		slug=self.kwargs.get("slug")
		obj=Course.objects.filter(slug=slug)
		if obj.exists():
			return obj.first()
		raise Http404


# Delete
class CourseDeleteView(StaffMemberRequiredMixin,DeleteView):
	queryset=Course.objects.all()
	success_url='/videos/'

	def get_object(self):
		slug=self.kwargs.get("slug")
		obj=Course.objects.filter(slug=slug)
		if obj.exists():
			return obj.first()
		raise Http404