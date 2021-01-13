from django.shortcuts import render 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.urls import reverse
from django import forms
from . import util
import random
from django.contrib import messages
import markdown2


my_entries = []
mode = "create"

class NewTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput , label="entry") 
    content= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":1}))

    
    
def index(request):
     global my_entries
     entries = util.list_entries()
     my_entries = []
     for entry in entries:
        my_entries.append(entry)
     return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries()
    })

def show(request, name):
     global my_entries
     if name not in my_entries :
        return render(request, "encyclopedia/error.html") 
    
     text =markdown2.markdown(util.get_entry(name))
     filename = f"encyclopedia/templates/encyclopedia/display.html"
     f= open(filename, "w+")
     text2 =" {% extends " + '''"encyclopedia/layout.html"''' + " %}"
     f.write(text2+"\r\n")
     f.write("{% block title %}"+name+"{% endblock %}"+"\r\n")
     f.write("{% block body %}"+"\r\n")
     f.write(text+"\r\n")
     f.write("{% endblock %}"+"\r\n")
     f.close()   
     return render(request, "encyclopedia/display.html")     
   

def search(request):
    global my_entries
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        filter_data = []
        filter_data = [x for x in my_entries if ( q in x)]
        print(filter_data)
        print(my_entries)
        if len(filter_data) > 1:
              return render(request, 'encyclopedia/search.html',{
                 "name":filter_data
              })
        else :
              show(request,filter_data[0])
              return render(request, "encyclopedia/display.html")        
        
    else:
        return HttpResponse('Please submit a search term.')
  

def create(request):
    global my_entries
    global mode
    if request.method =="POST":
        form = NewTaskForm(request.POST)
        
        if form.is_valid():
           title = form.cleaned_data["title"]
          
           if title in my_entries and mode=="create":
                
                messages.error(request, 'The title name already Exists, please try another title')
                return render(request,"encyclopedia/create.html", {
                "form":form })
           else:
                
                content1=form.cleaned_data["content"]
                text = request.POST.get("content", None)
                filename0 = f"entries/{title}.md"
                if text is not None :
                    if mode == "create":
                         my_entries.append(title)
                    util.save_entry(title, text)
                    show(request,title)
                    mode = "create" 
                    return render(request, "encyclopedia/display.html")    
        else:
            return render(request,"encyclopedia/create.html", {
                "form":form
            })   
    return render(request, "encyclopedia/create.html",{
        "form":NewTaskForm
    } )
    return render(request, "encyclopedia/create.html")    

def edit(request,name):
    global mode 
    file_data = util.get_entry(name)
    if request.method =="GET":
        form2 = NewTaskForm(None, initial={"title":name ,"content":file_data})
        mode = "edit"
        return render(request, "encyclopedia/create.html",{"form":form2})
    return render(request, "encyclopedia/create.html",{"form":form2})    
  
def random1(request):
    global my_entries
    entries = util.list_entries()
    my_entries = []
    for entry in entries:
        my_entries.append(entry)
    indx = random.randint(1, len(my_entries))
    entry = my_entries[indx]
    if entry is not None:
        show(request, entry)
        return render(request, "encyclopedia/display.html")           
    return render(request, "encyclopedia/display.html") 
