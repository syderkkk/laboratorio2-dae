from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
def task_list(request):
    tasks = Task.objects.all()

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if status_filter and status_filter != 'all':
        tasks = tasks.filter(status=status_filter)

    if priority_filter and priority_filter != 'all':
        tasks = tasks.filter(priority=priority_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter
    }

    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# Endpoint
def all_tasks(request):
    tasks = Task.objects.all()

    tasks_data = [
        {
            'title': task.title,
            'description': task.description,
            'created_at': task.created_date,
            'due_date': task.due_date,
            'priority': task.priority,
            'status': task.status,
            
        }
        for task in tasks
    ]
    
    return JsonResponse({'tasks': tasks_data})