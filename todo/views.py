from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, View
from .models import Task
from .mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CreateOrUpdateTaskForm

# Create your views here.


class TaskListView(LoginRequiredMixin, ListView):
    """
    this is a ckass for showing list of Tasks
    """

    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.profile)


class AddTaskView(LoginRequiredMixin, CreateView):
    """
    this is a class for create Tasks
    """

    model = Task
    form_class = CreateOrUpdateTaskForm
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):

        form.instance.user = self.request.user.profile
        return super(AddTaskView, self).form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """
    this is a class for delete Tasks
    """

    model = Task
    success_url = reverse_lazy("task_list")
    template_name = "delete.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.profile)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    this is a class for update Tasks
    """

    model = Task
    form_class = CreateOrUpdateTaskForm
    template_name = "update_task.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.profile)


class CompleteTaskView(LoginRequiredMixin, View):
    """
    this is a class for make  Tasks complete
    """

    model = Task
    success_url = reverse_lazy("task_list")

    def get(self, request, pk, *args, **kwargs):

        task = get_object_or_404(Task, id=pk, user=request.user.profile)
        task.is_complete = True
        task.save()
        return redirect(self.success_url)


class UndoneTaskView(LoginRequiredMixin, View):
    """
    this is a class for undone task
    """

    model = Task
    success_url = reverse_lazy("task_list")

    def get(self, request, pk, *args, **kwargs):

        task = get_object_or_404(Task, id=pk, user=request.user.profile)
        task.is_complete = False
        task.save()
        return redirect(self.success_url)
