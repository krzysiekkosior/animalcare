from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from main_app.forms import CaseForm, PhotoForm, CommentForm
from main_app.models import Case, CasePhoto, Comment


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


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


class CaseView(View):

    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        comments = Comment.objects.filter(case=case)
        ctx = {
            'case': case,
            'comments': comments
        }
        return render(request, 'case_details.html', ctx)


class EditCaseView(View):

    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)

        if case.user != request.user:
            return redirect('cases_list')
        case_form = CaseForm(instance=case)
        photo_form = PhotoForm()
        ctx = {
            'caseForm': case_form,
            'photoForm': photo_form,
            'case': case
        }
        return render(request, 'edit_case.html', ctx)

    def post(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        case_form = CaseForm(request.POST, instance=case)
        if case_form.is_valid():
            case_form.save()
            photos = request.FILES.getlist('photos')
            if len(photos) != 0:
                for photo in photos:
                    CasePhoto.objects.create(photo=photo, case=case)
            return redirect(f'/case/{case.pk}')

        photo_form = PhotoForm()
        ctx = {
            'caseForm': case_form,
            'photoForm': photo_form,
            'case': case
        }
        return render(request, 'edit_case.html', ctx)


class CloseCaseView(SuperUserCheck, View):

    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        case.status = 1
        case.save()
        return redirect(f'/case/{case.pk}')


class DeleteCaseView(SuperUserCheck, View):

    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        case.delete()
        return redirect('/cases/')


class AddEditCommentView(View):

    def get(self, request, case_pk, com_pk=None):
        if com_pk is None:
            form = CommentForm()
            title = "Dodaj komentarz"
        else:
            comment = Comment.objects.get(pk=com_pk)
            form = CommentForm(instance=comment)
            title = "Edytuj komentarz"
        ctx = {
            'form': form,
            'title': title
        }
        return render(request, 'add_or_edit_comment.html', ctx)

    def post(self, request, case_pk, com_pk=None):
        if com_pk is None:
            title = "Dodaj komentarz"
            form = CommentForm(request.POST)
            user = request.user
            case = Case.objects.get(pk=case_pk)
            if form.is_valid():
                content = form.cleaned_data['content']
                Comment.objects.create(user=user, case=case, content=content)
                return redirect(f'/case/{case_pk}')
        else:
            comment = Comment.objects.get(pk=com_pk)
            form = CommentForm(request.POST, instance=comment)
            title = "Edytuj komentarz"
            if form.is_valid():
                form.save()
                return redirect(f'/case/{case_pk}')
        ctx = {
            'form': form,
            'title': title
        }
        return render(request, 'add_or_edit_comment.html', ctx)
