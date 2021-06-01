from django.shortcuts import render

from main_app.models import Case


def main_page(request):
    return render(request, 'main_page.html')

def cases_list(request):
    cases = Case.objects.all().order_by('date')
    ctx = {
        'cases': cases
    }
    return render(request, 'cases_list.html', ctx)
