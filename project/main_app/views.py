from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from main_app.forms import CaseForm, PhotoForm, CommentForm
from main_app.models import Case, CasePhoto, Comment, Observed


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


def main_page(request):
    return render(request, 'main_page.html')


def cases_list(request, case_filter=None):
    if case_filter == "poszukiwane":
        cases = Case.objects.filter(type=0, status=0).order_by('date')
    elif case_filter == "znalezione":
        cases = Case.objects.filter(type=1, status=0).order_by('date')
    elif case_filter == "zamkniete-ogloszenia":
        cases = Case.objects.filter(status=1).order_by('date')
    elif case_filter is None:
        cases = Case.objects.filter(status=0).order_by('date')
    else:
        return redirect('cases_list')
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
        try:
            observed = Observed.objects.get(case=case, user=request.user)
        except Observed.DoesNotExist:
            observed = None
        comments = Comment.objects.filter(case=case)
        ctx = {
            'case': case,
            'comments': comments,
            'observed': observed
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


class AddEditCommentView(LoginRequiredMixin, View):

    def get(self, request, case_pk, com_pk=None):
        case = get_object_or_404(Case, pk=case_pk)
        if case.status == 1:
            return redirect(f'/case/{case.pk}/')
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


class DeleteCommentView(LoginRequiredMixin, View):

    def get(self, request, case_pk, com_pk):
        case = get_object_or_404(Case, pk=case_pk)
        comment = get_object_or_404(Comment, pk=com_pk)
        user = request.user
        if comment.user == user or user.is_superuser:
            comment.delete()
        return redirect(f'/case/{case.pk}')


class AddToObserved(LoginRequiredMixin, View):

    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        user = request.user
        try:
            Observed.objects.get(case=case, user=user)
        except Observed.DoesNotExist:
            Observed.objects.create(case=case, user=user)
        return redirect(f'/case/{case.pk}/')


class RemoveFromObserved(LoginRequiredMixin, View):

    def get(self, request, case_pk, obs_pk):
        case = get_object_or_404(Case, pk=case_pk)
        observed = get_object_or_404(Observed, pk=obs_pk)
        if observed.user == request.user:
            observed.delete()
        return redirect(f'/case/{case.pk}')
