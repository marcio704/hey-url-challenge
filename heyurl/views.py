import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .forms import UrlValidationForm
from .models import Url, Click

log = logging.getLogger(__name__)


def index(request):
    urls = Url.objects.order_by('-created_at')
    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)


def store(request):
    try:
        validation_form = UrlValidationForm(request.POST)
        is_valid = validation_form.is_valid()
        if not is_valid:
            return HttpResponse("Request is not valid, missing proper data", status=400)

        url = validation_form.save(commit=False)
        Url.create(url.original_url)
        return HttpResponse("Storing a new URL object into storage")

    except:
        error_msg = "Something went wrong on creating the Url"
        log.exception(error_msg)
        return HttpResponse(error_msg, status=500)


def short_url(request, short_url):
    try:
        url = Url.objects.get(short_url=short_url)
        Click.create(url, request)
        return HttpResponse("You're looking at url %s" % short_url)

    except Url.DoesNotExist:
        return HttpResponse(f"Short URL {short_url} not found", status=404)

    except:
        error_msg = "Something went wrong on accessing the Url"
        log.exception(error_msg)
        return HttpResponse(error_msg, status=500)


def clicks(request):
    try:
        click_count = Click.objects.for_current_month().count()
        browsers = Click.objects.aggregate_by_browser()
        platforms = Click.objects.aggregate_by_platform()

        context = {
            'click_amount': click_count,
            'browsers': browsers,
            'platforms': platforms,
        }
        return render(request, 'heyurl/clicks.html', context)

    except:
        error_msg = "Something went wrong on accessing the clicks page"
        log.exception(error_msg)
        return HttpResponse(error_msg, status=500)


def json_urls(request):
    try:
        json_list_response = {
            "data": [],
            "included": [],
        }
        urls = Url.objects.order_by('-created_at')[:10]

        for url in urls:
            json_list_response['data'].append(url.to_dict())

        return JsonResponse(json_list_response)

    except:
        error_msg = "Something went wrong on accessing the urls as json API"
        log.exception(error_msg)
        return HttpResponse(error_msg, status=500)
