from django.shortcuts import render,redirect

# Create your views here.

from .models import Todo

def index(request):
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'myapp/index.html', {'todos': todos})

def add_todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('index')
    return render(request, 'myapp/add_todo.html')

def toggle_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')

def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect('index')
