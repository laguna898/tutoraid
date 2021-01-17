from django.http import HttpResponse
from django.http import Http404

from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Course

def index(request):
    latest_5_course_list = Course.objects.order_by('id')[:5]

    #template = loader.get_template('courses/index.html')
    context = {
        'latest_5_course_list': latest_5_course_list
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'courses/index.html', context)

def detail(request, course_id):
    # try:
    #     course = Course.objects.get(pk=course_id)
    # except Course.DoesNotExist:
    #     raise Http404("course does not exist")
    # return render(request, 'courses/detail.html', {'course': course})
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/detail.html', {'course': course})

def results(request, course_id):
    response = "You're looking at the results of course %s."
    return HttpResponse(response % course_id)

def vote(request, course_id):
    return HttpResponse("You're voting on course %s." % course_id)