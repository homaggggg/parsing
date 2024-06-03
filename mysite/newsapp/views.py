from django.shortcuts import redirect, render
from django.urls import reverse
from pymongo import MongoClient
from bson import ObjectId
from django import forms

class NewsForm(forms.Form):
    title = forms.CharField(max_length=200)
    link = forms.CharField(max_length=200)
    date = forms.CharField(max_length=200)

client = MongoClient('mongodb://localhost:27017')
db = client['Sites']
collection = db['News']

def readDB(request):
    news = collection.find()
    news_ls = []
    for new in news:
        new['id'] = str(new['_id'])
        news_ls.append(new)

    return render(request, 'index.html', {'news': news_ls})

def readDbOne(request, pk):
    new = collection.find_one({'_id': ObjectId(pk)})
    new['id'] = str(new['_id'])
    return render(request, 'new.html', {'new': new})

def CreateDocDB(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if(form.is_valid()):
            collection.insert_one(form.cleaned_data)

    else:
        form = NewsForm()
    return render(request, 'form_create.html', {'form': form})

def UpdateDB(request, pk):
    new = collection.find_one({'_id': ObjectId(pk)})
    if new:
        new['id'] = str(new['_id'])

    if request.method == 'POST':
        form = NewsForm(request.POST)
        if(form.is_valid()):
            collection.update_one({'_id': ObjectId(pk)}, {'$set': form.cleaned_data})

    else:
        form = NewsForm(initial=new)
    return render(request, 'form_update.html', {'form': form})

def DeleteDocDB(request, pk):
    new = collection.find_one({'_id': ObjectId(pk)})
    if new:
        new['id'] = str(new['_id'])

    if request.method == 'POST':
        collection.delete_one({'_id': ObjectId(pk)})
        return redirect(reverse('news'))

    return render(request, 'delete.html', {'new': new})

def DeleteAllDocsDB(request):
    if request.method == 'POST':
        collection.drop()
        return redirect(reverse('news'))