from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django.core.mail import EmailMessage

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from accounts.tokens import account_activation_token


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password2']
            user = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(raw_password=password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user=user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            context = {'activate_acc': 'Na podany adres email został wysłany link aktywacyjny.'}
            return render(request, 'email_verification.html', context)
        return render(request, 'registration/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {'activate_pass': 'Konto zostało aktywowane. Możesz się teraz zalogować.'}
        return render(request, 'email_verification.html', context)
    else:
        context = {'activate_fail': 'Link aktywacyjny jest niepoprawny.'}
        return render(request, 'email_verification.html', context)
