from .models import Group, Schedule
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class GroupListView(ListView):

    model = Group

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        return context


class GroupDetailView(DetailView):

    model = Group

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['entries'] = Schedule.objects.filter(group=self.object)
        return context