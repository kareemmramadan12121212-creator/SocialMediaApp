from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views.generic import ListView
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.

class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super(SignUp, self).get(*args, **kwargs)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('HomePage')
    else:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return redirect('login')


def logout_page(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountSettingsView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'profile_image', 'bio']
    success_url = '/profile/'
    template_name = 'account_settings.html'

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required(login_url='login'), name='dispatch')
class Profile(ListView):
    model = Post
    template_name = 'profile.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-date_posted')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddPost(CreateView):
    model = Post
    fields = ['text']
    template_name = 'new_post.html'
    success_url = '/profile/'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserProfile(ListView):
    model = Post
    template_name = 'userProfile.html'
    paginate_by = 5

    def get(self, *args, **kwargs):
        UserName = self.kwargs['username']
        user_username = self.request.user.username
        if user_username == UserName:
            return redirect('profile')
        else:
            return super(UserProfile, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        UserName = self.kwargs['username']
        USER = User.objects.get(username=UserName)
        context["USER"] = USER
        is_following = self.request.user.is_following(USER)
        context["is_following"] = is_following
        context["get_num_followers"] = USER.get_num_followers()
        return context

    def get_queryset(self):
        UserName = self.kwargs['username']
        USER = User.objects.get(username=UserName)
        return Post.objects.filter(user=USER).order_by('-date_posted')


@method_decorator(login_required(login_url='login'), name='dispatch')
class SearchUsers(ListView):
    model = User
    template_name = 'search-users.html'
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET['search']
        qs = User.objects.filter(username__contains = search_term)
        return qs

@login_required(login_url='login')
def follow_user (request,id):
    follower = request.user
    followed = User.objects.get(id=id)
    new_follow = follow(follower=follower,followed=followed)
    new_follow.save()
    return redirect('/user/'+followed.username)

@login_required(login_url='login')
def unfollow_user (request,id):
    follower = request.user
    followed = User.objects.get(id=id)
    follow.objects.filter(follower=follower, followed=followed).delete()
    return redirect('/user/'+followed.username)

@method_decorator(login_required(login_url='login'), name='dispatch')
class HomePage(ListView):
    model = Post
    template_name = 'homePage.html'
    paginate_by = 5

    def get_queryset(self):
        followings = self.request.user.get_followings()
        return Post.objects.filter(user_id__in = followings).order_by('-date_posted')

