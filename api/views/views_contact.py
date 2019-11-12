from log import log
import sys
import os
import datetime

from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

from api.models import User
from api.auth import auth_user_id

@auth_user_id
def contact_us(request):
    user_id = int(request.POST.get('user_id'))
    title = request.POST.get('title')
    content = request.POST.get('content')
    user = User.objects.get(id=user_id)

    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d-%H-%M-%S.txt')
    path = os.path.join(settings.BASE_DIR, 'contacts/' + filename)

    with open(path, 'w', encoding='utf8') as fp:
        f = File(fp)
        f.write('from: ' + user.name + ' ' + user.email + '\tid=' + str(user_id) + '\n')
        f.write('date: ' + str(now) + '\n')
        f.write('title: ' + title + '\n\n')
        f.write(content)

    return HttpResponse(status=200)

@log
def api_contact(request):
    try:
        if request.method == 'POST':
            return contact_us(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)
