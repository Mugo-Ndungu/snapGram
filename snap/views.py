from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, CreatePostForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


# Create your views here.
def home(request):
    post = Post.objects.all()
    return render(request, 'index.html', {'post': post})


def about(request):
    return render(request, 'about.html', {'title': 'About'})


@login_required
def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Confirm your Snapgram Account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('<h3 style ="text-align:center;"> We have sent a link to your email, please follow the link to complete the registration. </h3>')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('<h4> Thank you for your email confirmation. To login to your account, <a href="/accounts/login">Click here .</a> </h4>')
    else:
        return HttpResponse('<h1 style = "color:red;"> Activation link is invalid! </h1>')


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


def create(request):


    current_user = request.user

    form = CreatePostForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = CreatePostForm()
    return render(request, 'post.html', {'form': form})
