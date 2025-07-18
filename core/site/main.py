from django.shortcuts import render,redirect

from core.models import Category


def index(request):
    ctgs = Category.objects.all()

    print("\n\n",ctgs,'\n\n')
    ctx = {}
    return render(request,'site/index.html',ctx)