from django.shortcuts import render, redirect
from django.views import View

from main_app.forms import CaseForm, PhotoForm
from main_app.models import Case, CasePhoto


def main_page(request):
    return render(request, 'main_page.html')

def cases_list(request):
    cases = Case.objects.all().order_by('date')
    ctx = {
        'cases': cases
    }
    return render(request, 'cases_list.html', ctx)


class AddCaseView(View):

    def get(self, request):
        case_form = CaseForm()
        photo_form = PhotoForm()
        ctx = {
            'caseForm': case_form,
            'photoForm': photo_form
        }
        return render(request, 'add_case.html', ctx)

    def post(self, request):
        case_form = CaseForm(request.POST)
        if case_form.is_valid():
            user = request.user
            if user.is_authenticated:
                case = Case(user=user, **case_form.cleaned_data)
                case.save()
            else:
                case = Case(**case_form.cleaned_data)
                case.save()
            photos = request.FILES.getlist('photos')
            if len(photos) != 0:
                for photo in photos:
                    CasePhoto.objects.create(photo=photo, case=case)
            return redirect('cases_list')

        photo_form = PhotoForm()
        ctx = {
            'caseForm': case_form,
            'photoForm': photo_form
        }
        return render(request, 'add_case.html', ctx)
