from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


import os 
import pdfkit

from payments.models import Customer
from core.forms import UploadFileForm


PATH = os.path.join(os.getcwd(),"core","driver","software.deb")
config = pdfkit.configuration(wkhtmltopdf=PATH)


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
            try:             
                c = Customer.objects.get(token = token)
                if c.balance >= 1:
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        html = b''
                        name = request.FILES['file'].name[0:-5] + ".pdf"
                        for i in request.FILES['file'].chunks():
                            html += i
                        html = html.decode()
                        pdf = pdfkit.from_string(html, False,configuration = config) 
                        response  =  HttpResponse(pdf,content_type='application/force-download')
                        response['Content-Disposition'] = f'attachment; filename={name}'
                        c.balance -= 1
                        c.save()
                        return response
                    else:
                        error = ''
                        for i in form.errors.as_data()['file']:
                            for j in i:
                                error += j
                        return HttpResponseNotFound(error)
                else:
                    return HttpResponseNotFound("Low Balance Kindly Recharge")
            except:
                return HttpResponseNotFound("No Key Found")
        else:
            return HttpResponseNotFound("Wrong Key")
    else:
        return HttpResponseNotFound("Method Not allowed")