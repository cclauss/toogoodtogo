from django.db import connection
from django.http import HttpResponse


def healthcheck(request):
    with connection.cursor() as c:
        c.execute('SELECT 1')
    return HttpResponse('OK')
