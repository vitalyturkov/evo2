from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from .forms import FileForm
from .models import FileEntity
# from FileSharingService.settings import BASE_DIR
# from FileSharingService.settings import WEBSITE
from django.http import HttpResponse
import datetime
import hashlib # for sha256
MAX_FILE_SIZE = 10240


def main(request):

    if request.method == 'POST':

        c = {}
        c.update(csrf(request))
        c['form'] = FileForm

        f = request.FILES['file']

        if f.size > MAX_FILE_SIZE:
            c['message'] = "Mate, the file you've provided is too big. Pls make sure it's <10KB."
            return render_to_response("upload.html", c)


        c['hash'], c['amount'] = sha256(request.FILES['file'])

        
        

        return render_to_response("upload.html", c)

    if request.method == 'GET':
        # if it's GET (not POST) - we just serve the form

        c = {}
        c.update(csrf(request))
        c['form'] = FileForm

        return render_to_response("upload.html", c)


def download(request, file_id):

    file_object = FileEntity.objects.filter(id=file_id)[0]
    f_name = file_object.filename

    with open(BASE_DIR + "\\media\\" + file_id, 'rb') as f:
        data = f.read()

    response = HttpResponse(data, content_type='none')
    response['Content-Disposition'] = 'attachment; filename=' + f_name
    # such a stub ...
    response['Content-Length'] = data.__sizeof__()
    return response


def sha256(file):

    sha = hashlib.sha256()
    file = file.read() # encode not needed - says the type is bytes
    sha.update(file)
    hash_sum = sha.hexdigest()

    # write to DB
    # doesnotexist exception
    try:
        file_object = FileEntity.objects.get(hash = hash_sum)
        file_object.amount = file_object.amount + 1
        amount = file_object.amount
        print('An existing hash was found. Incrementing.')
    except:
        print('An object does not exist. Creating one.')
        amount = 1
        file_object =  FileEntity(hash =  hash_sum, amount = amount)
        file_object.amount = amount
    file_object.save()

    return hash_sum, amount