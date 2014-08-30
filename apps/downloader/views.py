from django.http import HttpResponse, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from .models import File
from django.conf import settings
from tasks import run_processors

import os
import mimetypes


def download(request, file_id):
    file_obj = File.objects.get(id=file_id)
    file_url = settings.PROJECT_PATH + file_obj.file.url
    wrapper = FileWrapper(file(file_url, 'rb'))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(file_url)[0])
    response['Content-Length'] = os.path.getsize(file_url)
    response['Content-Disposition'] = "attachment; filename=" + file_obj.file_name
    return response


def parse(request, file_id):
    file_obj = File.objects.get(id=file_id)
    if file_obj:
        run_processors(file_obj)
    if file_obj.category.code_name == "teachers_html_from_wimii":   #
        return HttpResponseRedirect('/admin/main/teacher/')
    else:
        return HttpResponseRedirect('/admin/main/schedule/')

