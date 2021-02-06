from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Setup, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from blogapp.forms import CreatePostForm, UserCreateForm, EditPostForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    dict = {'data' : None}
    try:
        limit = Setup.objects.get(SetupKey='blog')
        Posts = Post.objects.all().order_by('-date_creation')[:limit.NumberPostsHome]
        dict = {'data' : Posts}
    except:
        print("No result for thhis query")
    return render(request, 'blogapp/index.html', dict)

#####################################################################################################################################

def Signup(request):
    if request.method=='POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('blog:management'))
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'blogapp/signup.html', context)

#####################################################################################################################################

@login_required
def Management(request):
    categories = Category.get_all_categories()
    posts = Post.get_all_posts()
    categoryID = request.GET.get('category')
    if categoryID:
        posts = Post.get_all_posts_by_categoryid(categoryID)
    else:
        posts = Post.get_all_posts();
    data = {}
    data['categories'] = categories
    data['posts'] = posts
    return render(request, 'blogapp/management.html', data)

#####################################################################################################################################

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "blogapp/create_post.html"
    success_url = reverse_lazy( "blog:management" )

#####################################################################################################################################

def EditPost(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    form = EditPostForm(request.POST or None, instance = posts)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('blog:management'))
    context = {'form': form}
    return render(request, 'blogapp/edit_post.html', context)

#####################################################################################################################################

# def Filter(request):
#     categories = Category.objects.all()
#     for unit in categories:
#         email = self.request.GET.get(unit.title)
#         print(email)
#     dict = {'data' : categories}
#     return render(request, 'blogapp/management.html', dict)


# class Management(ListView):
#     template_name = "blogapp/management.html"
#     model = Post
#     context_object_name = "posts"
