from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


import os 

from payments.models import Customer
from core.forms import UploadFileForm

import io
from PIL import Image


def index(request):
    return render(request,"core/index.html",{"title":"Home Page"})


@login_required
def convert(request):
    form = UploadFileForm()
    return render(request,"core/user_convert.html",{"form":form})


@csrf_exempt
def api_convert(request):
    if request.method == 'POST':
        token = request.POST.get("token")
        if token:
            if 1:             
                c = Customer.objects.get(token = token)
                if c.balance >= 1:
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        image = form.cleaned_data['file']
                        image = Image.open(image).convert('RGB')
                        with io.BytesIO() as f:
                            image.save(f, format='JPEG',optimize=True,quality=70)
                            imi = f.getvalue()
                        response  =  HttpResponse(imi,content_type="image/jpeg")
                        response['Content-Disposition'] = f'attachment; filename=image.jpg'
                        c.balance -= 1
                        c.save()
                        return response
                    else:
                        error  = ''
                        for i in form.errors.as_data()['file']:
                            for j in i:
                                error += j
                        return HttpResponseNotFound(error)
                else:
                    return HttpResponseNotFound("Low Balance Kindly Recharge")
            else:
                return HttpResponseNotFound("No Key Found")
        else:
            return HttpResponseNotFound("Wrong Key")
    else:
        return HttpResponseNotFound("Method Not allowed")