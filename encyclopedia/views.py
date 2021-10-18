import random

from logging import PlaceHolder
from re import search
from django.forms.widgets import TextInput, Widget
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

markdowner = Markdown()

# create a form that is used to replace the html code
class typeSearch(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Search'}))

# create a class to input new page data
class newPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Title Here'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Write the text here in .md format'}))

# create a class to edit the content of a page
class edit(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="")


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        search = typeSearch(request.POST)
        if search.is_valid():
            task = search.cleaned_data["item"]
            if task in entries:
                page = util.get_entry(task)
                page_convert = markdowner.convert(page)

                context = {
                    "title" : task,
                    "page" : page_convert,
                    "forms" : typeSearch()
                }
                return render(request, "encyclopedia/entry.html", context)

# code to figure out similar search results
            else:
                for i in entries:
                    if task.lower() in i.lower():
                        searched.append(i)
                        context = {
                            "searched" : searched,
                            "forms" : typeSearch()
                        }
                        return render(request, "encyclopedia/search.html", context)
            return render(request, "encyclopedia/error.html", {
                "forms" : typeSearch(),
                "message" : "Sorry, that page doesn't exist"
            })
                    
        
# the context is so formulated that it contains the items required for index page
    context = {
        "entries" : util.list_entries(),
        "forms" : typeSearch()
    }
    return render(request, "encyclopedia/index.html", context)


def entry(request, name): 
    entries = util.list_entries()
    if name in entries:
        page = util.get_entry(name)
        page_convert = markdowner.convert(page)

        context = {
            "title": name,
            "page" : page_convert,
            "forms" : typeSearch()
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {
            "forms" : typeSearch(),
            "message" : "Sorry, that page doesn't exist"
        })

# code to execcute new page
def newpage(request):
    entries = util.list_entries()
    if request.method == "GET":
        data = newPage(request.GET)
        if data.is_valid():
            title = data.cleaned_data["title"]
            content = data.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "forms" : typeSearch(),
                    "message" : "That page already exists"
                })
            else:
                util.save_entry(title, content)
                context = {
                    "entries" : util.list_entries(),
                    "forms" : typeSearch()
                }
                return render(request, "encyclopedia/index.html", context)
    return render(request, "encyclopedia/newpage.html", {
        "forms" : typeSearch(),
        "newpage" : newPage()
    })

# code to edit page
def change(request, name):
    entries = util.list_entries()
    if request.method == "GET":
        content = util.get_entry(name)
        context = {
            "forms" : typeSearch(),
            "edit" : edit(initial={"textarea" : content}), 
            "title" : name
        }
        return render(request, "encyclopedia/change.html", context)
    else:
        data = edit(request.POST)
        if data.is_valid():
            content = data.cleaned_data["content"]
            if name in entries:
                util.save_entry(name, content)
                context = {
                    "entries" : util.list_entries(),
                    "forms" : typeSearch()
                }
                return render(request, "encyclopedia/index.html", context)
            else:
                return render(request, "encyclopedia/error.html", {
                    "forms" : typeSearch()
                })

# code to load a random page
def randomPage(request):
    if request.method == "GET":
        entries = util.list_entries()
        num = random.randint(0, len(entries)-1)
        randompage = entries[num]
        page = util.get_entry(randompage)
        pageconverted = markdowner.convert(page)

        context = {
            "forms" : typeSearch(),
            "page" : pageconverted,
            "title" : randompage
        }

        return render(request, "encyclopedia/entry.html", context)
