from django.urls import path, include
from .views import *

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("update-task/<int:pk>/", UpdateTaskView.as_view(), name="update_task"),
    path("delete-task/<int:pk>/", DeleteTaskView.as_view(), name="delete_task"),
    path("add-task/", AddTaskView.as_view(), name="add_task"),
    path("complete-task/<int:pk>/", CompleteTaskView.as_view(), name="complete_task"),
    path("undone-task/<int:pk>/", UndoneTaskView.as_view(), name="undone_task"),
    path("api/v1/", include("todo.api.v1.urls")),
]
