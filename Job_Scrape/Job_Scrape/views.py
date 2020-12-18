from django.shortcuts import render
import requests
from .scraper2 import get_all_jobs

def home(request):

    a,b,c,d = get_all_jobs('chemical+engineer','philadelphia')

    data = zip(a,b,c,d)

    context = {'data':data}

    return render(request,'scrape/home.html',context)
