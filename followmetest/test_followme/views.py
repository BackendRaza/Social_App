from io import RawIOBase
from django.core.checks import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password
from .models import *
from datetime import datetime
from django.db.models import Count

def index(request):
    userposts = Posts.objects.all().order_by('pdate').reverse()
    getlikes = Like.objects.filter(postid=userposts)
    return render(request, "index.html", {'post': userposts, 'tlikes':getlikes})

def showData(request):
    all_data = Userr.objects.all()
    return render(request, "show.html", {'key': all_data})

def editData(request, pk):
    get_data = Userr.objects.get(id=pk)
    return render(request, "update.html", {"key1": get_data})

def updateData(request, pk):
    udata = Userr.objects.get(id=pk)
    udata.FirstName = request.POST['fname']
    udata.LastName = request.POST['lname']
    udata.Email = request.POST['umail']
    udata.Contact = request.POST['cont']
    udata.ProfilePic = request.FILES['dp']
    udata.save()
    return redirect(viewprofile)

def deleteData(request, pk):
    deldata = Userr.objects.get(id=pk)
    deldata.delete()
    return redirect(showData)

# Registeration Form with email and password validation

def newreg(request):
    return render(request, "register.html")

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        umail = request.POST['umail']
        contact = request.POST['cont']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        profilepic = request.FILES['dp']

        #validate email id if it already exist
        user = Userr.objects.filter(Email=umail)

        if user:
            message = "Email address you entered already exist"
            return render(request, "register.html", {"msg":message})
        else:
            if password == cpassword:
                newuser = Userr.objects.create(FirstName=fname, LastName=lname, Email=umail, Contact=contact, Password=password, ProfilePic=profilepic)
                message = "Registeration successfull"
                return render(request,"index.html", {"msg":message})
            else:
                message = "Both Password Fields doesn't match"
                return render(request, "register.html", {"msg":message})

def loginPage(request):
    return render(request, "login.html")

def loginUser(request):
    if request.method == "POST":
        uemail = request.POST["uemail"]
        upass = request.POST["upass"]

        user = Userr.objects.get(Email=uemail)

        if user:
            if user.Password == upass:
                request.session['Id'] = user.id
                request.session['FirstName'] = user.FirstName
                request.session['LastName'] = user.LastName
                request.session['Email'] = user.Email
                request.session['ProfilePic'] = user.ProfilePic.url
                message = "Login Successful!!!"
                # return render(request, "index.html", {'msg': message})
                return redirect(index)
            else:
                message = "Password is incorrect"
                return render(request, "login.html", {'msg': message})
        else:
            message = "This email does not exist!! Please Register"
            return render(request, "login.html", {'msg': message})

def logout(request):
    request.session.clear()
    message = "User Logged out!!!!!!"
    return redirect(loginPage)

# PROFILE

def viewprofile(request):
    id = request.session["Id"]
    udetails = Userr.objects.all().filter(id=id)
    profile = Posts.objects.all().filter(userid=id).order_by('pdate').reverse()
    return render(request, 'profile.html', {"pdetails": profile, "udetails": udetails})

# POSTS

def createPost(request):
    return render(request, 'createpost.html')

def post(request):
    if request.method == "POST":
        phead = request.POST['phead']
        pimage = request.FILES['pimg']
        ptext = request.POST['ptext']
        user = request.POST['uid']
        uid = Userr.objects.get(id=user)
        pdate = datetime.now()

        newpost = Posts.objects.create(pheading=phead,pimg=pimage, ptext=ptext, userid=uid, pdate=pdate)
        return redirect(index)

def newLike(request):
    if request.method == "GET":
        pid = request.GET['post_id']
        likedpost = Posts.objects.get(id=pid)
        userid = request.session["Id"]
        udetails = Userr.objects.get(id=userid)
        l = Like(userid=udetails, postid=likedpost)
        l.save()
        # newlike = Like.objects.create(userid=udetails, postid=pid)
    return redirect(index)
        # return render(request, "index.html")
    return HttpResponse("Bad request")

def getTotalLikes(request):
    # count = Like.objects.all()
    # loguser = request.session['Id']
    # userlikes = Posts.objects.all()
    # count = Like.objects.filter(postid=userlikes)
    # print(len(userlikes))
    # return render(request, 'test.html', {'obj': userlikes})
    userposts = Posts.objects.all()
    post = Like.objects.all().count()
    # getlikes = Like.objects.get(id=userposts)
    # print(userposts)
    return render(request, "test.html", {'post': userposts, 'obj':post})






