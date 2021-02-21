from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Setup, Category, Temp, Newsletter
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from blogapp.forms import CreatePostForm, UserCreateForm, EditPostForm, NewsletterForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

# Create your views here.
def index(request):
    if request.method=='POST':
        form = NewsletterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return HttpResponseRedirect(reverse_lazy('blog:index'))
    else:
        form = NewsletterForm()
    # context = {'form': form}
    dict = {'data' : None}
    try:
        limit = Setup.objects.get(SetupKey='blog')
        Posts = Post.objects.all().order_by('-date_creation')[:limit.NumberPostsHome]
        dict = {'data' : Posts}
    except:
        print("No result for thhis query")
    return render(request, 'blogapp/index.html', {'form': form, 'data' : Posts})

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

# def Newsletter(request):
#     print('got hereeeee')
#     if 'q' in request.GET:
#         print('INSIDE')
#     # print(request)
#     # print(request.GET())
#     cat = request.GET.get('q')
#     print('here')
#     print(cat)
#     # if cat:
#     #     print(cat)
#     #     p = Newsletter(email=cat, status='ACTIVE')
#     #     p.save(force_insert=True)
#     return HttpResponseRedirect(reverse_lazy('blog:index'))

#####################################################################################################################################

# class CreatePost(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = CreatePostForm
#     template_name = "blogapp/create_post.html"
#     success_url = reverse_lazy( "blog:management" )

#####################################################################################################################################

def Redirects(request, pk):
    print('building it')
    # posts = get_object_or_404(Post, pk=pk)
    # form = EditPostForm(request.POST or None, instance = posts)
    # # Deleting everything in the table
    # all = Temp.objects.all().first()
    # if all:
    #     all.delete()
    # # filling temp table
    # first = Post.objects.get(pk=pk)
    # p = Temp(categories=first.categories)
    # p.save(force_insert=True)
    # categor = ''
    # print('ve se chega aqui pelo menos')
    # first = Temp.objects.all().first()
    # print(pk)
    # print(first)
    # if first.categories:
    #     categor = first.categories.split(',')
    #     print(categor, 'chunks')
    # if form.is_valid():
    #     form.save()
    #     return HttpResponseRedirect(reverse_lazy('blog:management'))
    # # context = {'form': form}
    # # return render(request, 'blogapp/edit_post.html', context)
    return render(request, 'blogapp/edit_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def DeleteAllCategories(request):
    print('got hereeeeeee delete all')
    temp_categories = Temp.objects.all().first()
    temp_categories.delete()
    return HttpResponseRedirect(reverse_lazy('blog:management'))

#####################################################################################################################################

def ChangeTag(request, pk):
    request.session['pk'] = pk
    cat = False
    if request.method=='GET':
        cat = request.GET.get('change')
    if cat:
        find = Post.objects.get(pk=pk)
        print(find, 'THIS IS THE ONE')
        if find:
            if find.categories == '':
                new = cat
                find.categories = new
                find.save()
                print(cat, 'cat')
                print(new, 'new')
                print('none')
            else:
                new = cat + ',' + str(find.categories)
                print(new, 'inseriu')
                find.categories = new
                find.save()
                print('first')
        else:
            find = Post(categories=cat)
            find.save(force_insert=True)
            print('second')
    # second session
    posts = get_object_or_404(Post, pk=pk)
    if posts.categories:
        chunks = posts.categories.split(',')
        print(chunks, 'chunks')
        categor = chunks
    else:
        categor= ''
    return render(request, 'blogapp/change_tag.html', {'data':categor})

#####################################################################################################################################

def CreatePost(request):
    print("return this")
    cat = False
    if request.method=='GET':
        cat = request.GET.get('add')
    if cat:
        find = Temp.objects.all().exists()
        print(find, 'THIS IS THE ONE')
        if find:
            first = Temp.objects.all().first()
            new = cat + ',' + first.categories
            print(str, 'inseriu')
            p = Temp.objects.get(categories=first.categories)
            p.categories = new
            p.save()
        else:
            p = Temp(categories=cat)
            p.save(force_insert=True)
    first = Temp.objects.all().first()
    if first:
        chunks = first.categories.split(',')
        print(chunks, 'chunks')
        categor = chunks
    else:
        categor= ''
    # data = categor
    if request.method=='POST':
        print('got here')
        form = CreatePostForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            temp_categories = Temp.objects.all().first()
            if temp_categories:
                print('=-=-=-=-=-=-=-=-=-=-=------------------------------==============================================')
                print(temp_categories.categories)
                post.categories = temp_categories.categories
                temp_categories.delete()
            post.save()
            # Send email
            all_users = Newsletter.objects.filter(status='ok')
            print(all_users)
            if all_users.exists():
                for user in all_users:
                    print(user, 'each of')
                    email_user = str(user.email)
                    message = 'NOVO POST GALERA'
                    send_mail('Teste', message, 'ccfitgym@gmail.com', [email_user], fail_silently=False)
            return HttpResponseRedirect(reverse_lazy('blog:management'))
    else:
        form = CreatePostForm()
    # context = {'data': data}
    return render(request, 'blogapp/create_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def EditPost(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    form = EditPostForm(request.POST or None, instance = posts)
    # Deleting everything in the table
    all = Temp.objects.all().first()
    if all:
        all.delete()
    # filling temp table
    first = Post.objects.get(pk=pk)
    p = Temp(categories=first.categories)
    p.save(force_insert=True)
    categor = ''
    print('ve se chega aqui pelo menos')
    first = Temp.objects.all().first()
    print(pk)
    print(first)
    if first.categories:
        categor = first.categories.split(',')
        print(categor, 'chunks')
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('blog:management'))
    # context = {'form': form}
    # return render(request, 'blogapp/edit_post.html', context)
    return render(request, 'blogapp/edit_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def DeletePost(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    print(posts)
    print(request.method)
    if request.method == 'GET':
        posts.delete()
    return HttpResponseRedirect(reverse_lazy('blog:management'))

#####################################################################################################################################


def DeleteCategory(request, value):
    print('test here')
    first = Temp.objects.all().first()
    string_set = first.categories.split(',')
    new_set = []
    for a_string in string_set:
        if value != a_string:
            new_set.append(a_string)
    print(new_set, 'new set')
    novo = ''
    print(new_set)
    for n in new_set:
        if new_set.index(n) == len(new_set)-1:
            novo = novo + n
        else:
            novo = n + ',' + novo
        print(novo, 'lets seeee the result')
    f = Temp.objects.all().first()
    p = Temp.objects.get(categories=f.categories)
    p.categories = novo
    p.save()
    blank = Temp.objects.all().first()
    if blank.categories == '':
        blank.delete()
    return HttpResponseRedirect(reverse_lazy('blog:create_post'))

#####################################################################################################################################

def DeleteCategoryEdit(request, value):
    print('check ifs gotten here')
    print('and did something')
    pk_number = int(request.session['pk'])
    posts = Post.objects.get(pk=pk_number)
    string_set = posts.categories.split(',')
    new_set = []
    for a_string in string_set:
        if value != a_string:
            new_set.append(a_string)
    print(new_set, 'new set')
    novo = ''
    print(new_set)
    for n in new_set:
        if new_set.index(n) == len(new_set)-1:
            novo = novo + n
        else:
            novo = n + ',' + novo
        print(novo, 'lets seeee the result')
    # updating post
    posts.categories = novo
    posts.save()
    response = HttpResponseRedirect(reverse_lazy('blogapp:change_tag', kwargs={'pk': pk_number}))
    return response



#####################################################################################################################################

# def AddCategory(request):
#     show = request.GET.get('add')
#     print(show)
#     return HttpResponseRedirect(reverse_lazy('blog:management'))

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
