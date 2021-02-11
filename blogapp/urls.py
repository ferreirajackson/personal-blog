from django.conf.urls import url
from blogapp import views
from django.contrib.auth import views as auth_views

# Down below are all the routes for the project
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"create/", views.CreatePost, name="create_post"),
    url(r"login/", auth_views.LoginView.as_view(template_name="blogapp/login.html"),name='login'),
    url(r"logout/", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/", views.Signup, name="signup"),
    url(r"edit/(?P<pk>\d+)", views.EditPost, name="edit_post"),
    url(r"delete/(?P<pk>\d+)", views.DeletePost, name="delete_post"),
    url(r"management/", views.Management, name="management"),
    # url(r"addcategory/", views.AddCategory, name="add_category"), 
    url(r"deleteCategory/(?P<value>.*)/$", views.DeleteCategory, name="delete_category"),
    url(r"delete_all/", views.DeleteAllCategories, name="delete_all_categories"),

]
