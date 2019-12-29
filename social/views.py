from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, auth
from accounts.models import permittedlist, userpermission, resolvedlist
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'social/index.html')
def register(request):
    if 'register' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'social/register.html',{'error_message':"Username already taken"})
            elif User.objects.filter(email = email).exists():
                return render(request,'social/register.html',{'error_message':"Email already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1, email = email, first_name= first_name, last_name = last_name)
                user.save()
                a= userpermission(user = user,is_student = True, is_counsellor = False, is_faculty = False )
                a.save()
                b = permittedlist(user= user)
                b.save()   
                c = resolvedlist(user= user)
                c.save()                
                return redirect('/social/login/')
        else:
            return render(request,'social/register.html',{'error_message':"Password does not match"})
    return render(request,'social/register.html')
def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request, 'social/login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'social/login.html')
def home(request):
    all_user= User.objects.all()
    #dict = {'all_user':all_user}
    return render(request,'social/home.html',{'all_user':all_user})
def trustable(request, id_user):
    all_user= User.objects.all()
    user = User.objects.get(id =id_user )
    request.user.permittedlist.allowed.add(user.permittedlist)
    return render(request,'social/home.html',{'all_user':all_user})
def resolved(request, id_user):
    all_user= User.objects.all()
    user = User.objects.get(id =id_user )
    request.user.resolvedlist.resolved.add(user.resolvedlist)
    return render(request,'social/home.html',{'all_user':all_user})
def untrustable(request, id_user):
    all_user= User.objects.all()
    user = User.objects.get(id =id_user )
    request.user.permittedlist.allowed.remove(user.resolvedlist)
    return render(request,'social/home.html',{'all_user':all_user})
def create(request):
    if request.user.is_superuser:
        if 'register' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            userType = int(request.POST['userType'])
            is_faculty = False 
            is_counsellor = False
            if userType == 0:
                is_faculty = True
            elif userType == 1:
                is_counsellor = True
            if password1 == password2:
                if User.objects.filter(username = username).exists():
                    return render(request,'social/create.html',{'error_message':"Username already taken"})
                elif User.objects.filter(email = email).exists():
                    return render(request,'social/create.html',{'error_message':"Email already taken"})
                else:
                    user= User.objects.create_user(username = username, password = password1, email = email, first_name= first_name, last_name = last_name)
                    user.save()
                    a= userpermission(user = user,is_student = False, is_counsellor = is_counsellor, is_faculty = is_faculty )
                    a.save()
                    b = resolvedlist(user= user)
                    b.save()       
                    c = permittedlist(user= user)
                    c.save()           
                    return redirect('/')
            else:
                return render(request,'social/create.html',{'error_message':"Password does not match"})
        return render(request,'social/create.html')
    else:
        raise Http404("You are not authorized.")

def unresolved(request,id_user):
    pass
    