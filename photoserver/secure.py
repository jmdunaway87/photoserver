from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import utils
from requests_toolbelt.multipart import decoder
import time 
@csrf_exempt
def authenticate(request):
    password = None;
    parts = decoder.MultipartDecoder(request.body, request.headers['content-type']).parts

    authenticated = check_post_parts_for_password(parts)

    if authenticated:
        status_code=200
    else:
        status_code=401
    
    return JsonResponse({"success":authenticated},status=status_code)


def check_password(password):
    correct = utils.get_config().get('admin', 'pw') == password
    if correct == False:
        time.sleep(2)
    return correct


def check_post_parts_for_password(parts):
    password=None
    for part in parts:    
        header = part.headers[b'Content-Disposition'].decode("utf-8") 
        name = header[header.index('name="')+6:]
        name = name[:name.index('"')]
        print(name)
        if(name =='password'):
            password = part.text
    authenticated = check_password(password)
    return authenticated