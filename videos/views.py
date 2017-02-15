from django.shortcuts import render
from django.views.generic import (
	CreateView,
	DetailView,
	UpdateView,
	ListView,
	DeleteView
	)
from models import Video
from forms import VideoForm
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from mixins import MemberRequiredMixin, StaffMemberRequiredMixin

# Create
class VideoCreateView(StaffMemberRequiredMixin,CreateView):
	model=Video
	form_class=VideoForm

# Detail
class VideoDetailView(MemberRequiredMixin,DetailView):
	queryset=Video.objects.all()

	def get_context_data(self,*args,**kwargs):
		context=super(VideoDetailView,self).get_context_data(*args,**kwargs)
		print context
		return context

# List
class VideoListView(ListView):
	def get_queryset(self):
		request=self.request
		qs=Video.objects.all()
		query=request.GET.get('q')
		if query:
			qs=qs.fiter(title__icontains=query)
		return qs	

# Update
class VideoUpdateView(StaffMemberRequiredMixin,UpdateView):
	queryset=Video.objects.all()	
	form_class=VideoForm	

# Delete
class VideoDeleteView(StaffMemberRequiredMixin,DeleteView):
	queryset=Video.objects.all()
	success_url='/videos/'