from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name="home"),
    path("showdata", views.showData, name="showData"),
    path("editdata/<int:pk>", views.editData, name="editData"),
    path("updatedata/<int:pk>", views.updateData, name="updateData"),
    path("deletedata/<int:pk>", views.deleteData, name="deleteData"),
    path("register/", views.newreg, name="newreg"),
    path("registered/", views.register, name="registered"),
    path("", views.loginPage, name="loginPage"),
    path("loginuser/", views.loginUser, name="loginUser"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.viewprofile, name="profile"),
    path("createpost/", views.createPost, name="createPost"),
    path("post/", views.post, name="post"),
    path("like/", views.newLike, name="Like"),
    path("gettotallikes", views.getTotalLikes, name="getTotalLikes")
]