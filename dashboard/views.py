from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Task
from .forms import TaskForm, TaskSearchForm, UserRegistrationForm
from .automation import run_email_task, run_scraping_task

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    search_form = TaskSearchForm(request.GET)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        status = search_form.cleaned_data.get('status')
        if query:
            tasks = tasks.filter(name__icontains=query)
        if status:
            tasks = tasks.filter(status=status)

    return render(request, 'dashboard/index.html', {'tasks': tasks, 'search_form': search_form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'dashboard/task_detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'dashboard/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('dashboard')
    return render(request, 'dashboard/task_confirm_delete.html', {'task': task})

@login_required
def run_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        # Simple logic to choose task type based on name for this example
        if 'email' in task.name.lower():
            success = run_email_task(task.pk)
        elif 'scrape' in task.name.lower() or 'scraping' in task.name.lower():
            success = run_scraping_task(task.pk)
        else:
            # Default behavior just to show completion
            task.status = 'completed'
            task.save()
            success = True

        if success:
            messages.success(request, f'Task "{task.name}" ran successfully.')
        else:
            messages.error(request, f'Task "{task.name}" failed to run.')

    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'dashboard/register.html', {'form': form})
