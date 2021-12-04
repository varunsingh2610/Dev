from django.shortcuts import render
from django.http import HttpResponse
from .forms import ConnectionForm
from .models import ConnectionsDB
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect

import pandas as pd
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, create_engine, select)

# Create your views here.
def home(request):

    engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                           format("root", "Passw0rd@123",
                                  "localhost", "DataProcessor"), pool_pre_ping=True, pool_recycle=3600)
    metadata = MetaData()
    myTable = Table("table", metadata, autoload=True, autoload_with=engine)
    print(metadata.tables.keys())
    print(myTable.columns.keys())
    name = "\r\n-- @ Author:"
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            # database = form.cleaned_data['database']
            form.save()

    data = ConnectionsDB.objects.all()
    form = ConnectionForm()
    return render(request, 'base.html', {'form': form, 'data':data, 'c': html})


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        print(uploaded_file.name)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
    # return HttpResponse("OK")
    return render(request, 'base.html', {'url' : url})
