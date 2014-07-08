from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.core.files.base import ContentFile
from django.core.servers.basehttp import FileWrapper
from .models import File
from django.conf import settings

import os
import mimetypes


def download(request, file_name, extension, file_id):
    file_obj = File.objects.get(id=file_id)
    file_url = settings.PROJECT_PATH + file_obj.file.url
    wrapper = FileWrapper(file(file_url, 'rb'))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(file_url)[0])
    response['Content-Length'] = os.path.getsize(file_url)
    response['Content-Disposition'] = "attachment; filename=" + file_obj.file_name
    return response