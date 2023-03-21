from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util

def convert_md(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = convert_md(title)
    if html == None:
        return render(request, "encyclopedia/error.html", {
            "message": "this message doesn't exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })

def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q']
        html_content = convert_md(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entry_search,
            "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleCheck = util.get_entry(title)
        if titleCheck is not None:
            return render(request, "encyclopedia/error.html", {
            "message": "this Title already exist."
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title'] 
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title'] 
        content = util.get_entry(content)
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md(rand_entry)
    return render(request, "encyclopedia/entry.html", {
      "title": rand_entry,
      "content": html_content  
    })
