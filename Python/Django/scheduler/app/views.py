from django.shortcuts import render
import datetime
from pytz import timezone

# Create your views here.
def home(request):
    tz = timezone('Asia/Kolkata')
    dt = tz.localize( datetime.datetime.now().time() )
    print(dt)
    context = {
    'time' : dt
    }
    return render(request, 'base.html', context)
