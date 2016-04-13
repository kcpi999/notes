from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm

def frontpage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/note/')
    else: 
        return render_to_response('frontpage.html')

# ------------register user
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            form.save()
            username = request.POST.get('username', '')
            password = request.POST.get('password1', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/note/')
            else:
                # strange thing
                return HttpResponseRedirect('/accounts/register/')
            
    args = {}
    args.update(csrf(request))    
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)
            
# ------------auth
def login(request):
    c = {}
    c.update(csrf(request))        
    return render_to_response('login.html', c)
    
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
        
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/note/')
    else: 
        return HttpResponseRedirect('/accounts/invalid')
        
def invalid_login(request):
    return render_to_response('invalid_login.html')
    
def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

