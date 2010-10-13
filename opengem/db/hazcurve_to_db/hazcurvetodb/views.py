from django.http import HttpResponse

def index(request)
    return HttpResponse("You are looking at intensitymeasuretype index")

def detail(request, intensitymeasuretype_id)
    return HttpResponse("You are looking at imt: %s."% intensityemeasuretype_id)
