import os
#from django.http import HttpResponse
from django.conf import settings
from django.http import StreamingHttpResponse

#def downloadAFile(request, fileDate, fileTime, downloadFile):
#    return HttpResponse('OK. %s and %s The file %s has been downloaded' % (fileDate, fileTime, downloadFile))
"""
baseDir = settings.MEDIA_ROOT
def downloadAFile(request, downloadFile):
    filename = baseDir + '/' + downloadFile
    f =open(filename)
    data = f.read()
    f.close()
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    return response
    #wrapper = FileWrapper(file(filename))
    #response = HttpResponse(wrapper, content_type='text/plain')
    #response['Content-Length'] = os.path.getsize(filename) 
    #return response
"""

baseDir = settings.MEDIA_ROOT
def download_filename(request, filename):
    filename = baseDir + '/' + filename
    def read_file(filename, chunk_size=512):
        with open(filename, 'r') as file_object:
            while True:
                c = file_object.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(read_file(filename))
    response['Content-Type'] = 'application/octet-stream'
    base_filename = os.path.basename(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            base_filename)
    return response
