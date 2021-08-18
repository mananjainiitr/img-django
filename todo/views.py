from django.shortcuts import render , redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader
from .models import TodoList
from .models import TodoItem

# # Create your views here.
# def error_404_view(request,exception):
#     # raise Http404("404 error")
#     return render(request,"todo/404err.html")

def index(request):
    try:
        todolists = TodoList.objects.all()
    except TodoList.DoesNotExist:
        raise Http404("This List Does not Exists")
    context = {
        'todolists': todolists,
            }
    return render(request, 'todo/index.html', context)

def detail(request, list_id):
    try:
        todolist = TodoList.objects.get(id=list_id)
    except TodoList.DoesNotExist:
        raise Http404("This List Does not Exists")
    try:
        items_list = TodoItem.objects.filter(todo_list=todolist)
    except TodoList.DoesNotExist:
        raise Http404("This item Does not Exists")
    context = {
        'todolist': todolist,
        'items_list': items_list,
        'list_id':list_id
    }
    return render(request, 'todo/details.html', context)

def create(request):
    if request.method == "GET":
        cont={"error":"",}
        return render(request, 'todo/createlist.html',cont)
    name = request.POST["name"]
    desc = request.POST["title"]
    due_date = str(request.POST["date"])
    print(due_date)
    # due_tim = request.POST["time"]
    if (TodoList.objects.filter(list_name=name).exists()):
        raise Http404("You cant give same tittle")
    else:
        try:
            TodoList.objects.create(list_name=name)
            TodoItem.objects.create(title=desc,due_date=due_date,todo_list=TodoList.objects.get(list_name=name))
        except:
            cont = {"error":"Error in creating list"}
            return render(request, 'todo/createlist.html',cont)
    
    return redirect('/todo/')

def update(request):

    item = request.POST["item"]
    name = request.POST["name"]
    desc = request.POST["title"]
    check = request.POST["check"]
    
    # due_tim = request.POST["time"]
    try:
        todolist = TodoList.objects.get(id=name)
    except:
        raise Http404("Error occoured due to lack of information")
    if(request.POST["date"]):
        due_date = request.POST["date"]
        TodoItem.objects.filter(todo_list=todolist,id=item).update(title=desc,due_date=due_date,checked=check)
    else:
        TodoItem.objects.filter(todo_list=todolist,id=item).update(title=desc,checked=check)
    return redirect('/todo/'+name+'/')

def delete(request):
    id = request.POST["name"]
    name = TodoList.objects.get(id = id)
    try:
        todolist = TodoList.objects.get(list_name=name)
    except:
        raise Http404("Error occoured due to lack of information")
    TodoList.objects.filter(list_name=name).delete()
    lists = TodoList.objects.all()
    context = {
        'todolists': lists,

    }
    return render(request, 'todo/index.html', context)
def updatetodo(request,list_id,item_id):
    try:
        todoitem = item_id
        TodoList.objects.get(id = list_id)
        itemtitle = TodoItem.objects.get(id = todoitem).title
    except:
        raise Http404("Error occoured due to lack of information")
    try:
        todolist = list_id
    except:
        raise Http404("list item not found")    
    context = {
        'todolist':todolist,
        'todoitem':todoitem,
        'itemtitle':itemtitle,
    }
    return render(request, 'todo/update.html', context)

def deletetodo(request,list_id,item_id):
    try:
        id = item_id
        todoitem = TodoItem.objects.get(id = id).title
        todolist = TodoList.objects.get(id = list_id)
    except:
        raise Http404("list item not found") 
    TodoItem.objects.filter(todo_list=todolist,id = id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def createform(request,list_id):
    id = list_id
    name  = TodoList.objects.get(id = id)
    context={
        'todolist' : name
    }
    return render(request, 'todo/create.html', context)

def item_create(request):
    try:
        id = request.POST["name"]
        name = TodoList.objects.get(id = id)
        desc = request.POST["title"]
        due_date = str(request.POST["date"])
    except:
        raise Http404("cant get sufficient information")
    
    try:
        todolist = TodoList.objects.get(list_name=name)
    except:
        raise  Http404("Error occoured due to lack of information")
    # due_tim = request.POST["time"]
    if (TodoItem.objects.filter(todo_list=todolist,title=desc).exists()):
        raise Http404("You cant give same tittle")

    try:
        TodoItem.objects.create(title=desc,due_date=due_date,todo_list=todolist)
    except:
        raise Http404("Error in creating item in list")
    
    return redirect('/todo/'+id+'/')
