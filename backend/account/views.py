from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, ProfileImageForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class Register(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'you register successfully', 'success')
            return redirect('core:home')
        else:
            messages.warning(request, 'you full input allright', 'warning')
            return render(request, self.template_name, {'form': form})


class Login(View):
    form_calss = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_calss
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_calss(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your Login success', 'success')
                return redirect('core:home')
            else:
                messages.warning(request, 'your pass or username is not corect')
                return render(request, self.template_name, {'form': form})
        else:
            messages.warning(request, 'your pass or username is not corect')
            return render(request, self.template_name, {'form': form})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your logout success', 'success')
        return redirect('core:home')


class Dashboard(LoginRequiredMixin, View):
    form_class = ProfileImageForm
    template_name = 'account/dashboard.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, self.template_name, {'user': user, 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'your image uploaded', 'info')
            return redirect('account:dashboard', request.user.username)
        else:
            messages.warning(request, 'dont image uploaded', 'warning')
            return redirect('account:dashboard', request.user.username)
