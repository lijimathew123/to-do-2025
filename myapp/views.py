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



# core/views.py
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def deploy(request):
    if request.method == "POST":
        try:
            subprocess.run(["git", "pull"], cwd="/home/ubuntu/to-do-2025")
            subprocess.run(["/home/ubuntu/to-do-2025/venv/bin/python3", "manage.py", "migrate"], cwd="/home/ubuntu/to-do-2025")
            subprocess.run(["/home/ubuntu/to-do-2025/venv/bin/python3", "manage.py", "collectstatic", "--noinput"], cwd="/home/ubuntu/to-do-2025")
            subprocess.run(["sudo", "systemctl", "restart", "gunicorn"])  # Optional
            return HttpResponse("Deployment successful.", status=200)
        except Exception as e:
            return HttpResponse(f"Deployment failed: {str(e)}", status=500)
    return HttpResponse("Only POST method is allowed.", status=405)
