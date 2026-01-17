from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from . forms import RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Task

# Create your views here.

#@login_required
#def home(request):
   # return render(request,"index.html")
   
#@login_required
#def home(request):
   # if request.method == "POST":
    #    title = request.POST.get("title")
      #  if title:
    #        Task.objects.create(user=request.user, title=title)

   # tasks = Task.objects.filter(user=request.user) 
   # return render(request, "index.html", {"tasks": tasks})


@login_required
def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(
                user=request.user,
                title=title
            )

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "index.html", {"tasks": tasks})



def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request,"register.html",{'form':form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html")

   
    return render(request, "login.html")



@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def delete_task(request,id):
    task = get_object_or_404(Task,id=id)
    if request.method == "POST":
        task.delete()
        return redirect("home")
    return render(request,'delete.html',{'task':task})
        #return HttpResponse("Delete")

def complete_task(required,id):
    task = get_object_or_404(Task, id=id)
    task.completed= True
    task.save()
    return redirect('home')

