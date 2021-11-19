from django.http import HttpResponse
from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from requests_toolbelt.multipart import decoder
from . import secure
from . import utils
import os
def get_image(self,user,type,id):
    path= f"images/{user}/{type}/{id}.jpg"
    content = None
    print(path)
    with open(path, 'rb') as f:
        print(f)
        content = f.read()
    return HttpResponse(content, content_type='image/jpg')
@csrf_exempt 
def save_image(request,user,type,id):
    parts = decoder.MultipartDecoder(request.body, request.headers['content-type']).parts
    if secure.check_post_parts_for_password(parts) == False:
        return JsonResponse( {"authorized":False}, status=401)
    for part in parts:
        header = part.headers[b'Content-Disposition'].decode("utf-8") 
        name = header[header.index('name="')+6:]
        name = name[:name.index('"')]

        if '.jpg' in name:  
             configs = utils.get_config()
             path= f"images/{user}/{type}/{id}.jpg"
             os.makedirs(os.path.dirname(path), exist_ok=True)

             with open(path, 'wb') as f:
                 f.write(part.content)
                 f.close()
    return JsonResponse( {"success":True}, status=200)
