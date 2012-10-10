# -*- encoding: utf-8 -*-
import hashlib
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_POST
from users.forms import UserAddUserForm


@require_POST
def login(request):
  to_return = {'msg':u'Sin datos del POST' }
  to_return['success'] = False
  if request.method == "POST":
    post = request.POST.copy()
    if post.has_key('username') and post.has_key('password'):
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          auth_login(request, user)
          # Redirect to a success page.
          success = True
          to_return['success'] = True
        else :
          # Return a 'disabled account' error message
          to_return['msg'] = u"Tu cuenta no se ha activado aun."
      else :
        # Return an 'invalid login' error message.
        to_return['msg'] = u"Usuario o contraseña invalida"
    else :
      to_return['msg'] = u"No has ingresado usuario ni contraseña."
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

@require_POST
def register(request):
  to_return = {'msg':u'Sin datos del POST' }
  to_return['success'] = False
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  password_repeat = request.POST['password_repeat']
  first_name = request.POST['first_name']
  last_name = request.POST['last_name']
  if username and email and password and password_repeat and first_name and last_name :
    if password == password_repeat :
      #if not User.objects.filter(email=email, username=username).exists():  
      data = {'username' : username,
              'first_name' : first_name,
              'last_name' : last_name,
              'password1' : password,
              'password2' : password_repeat,
              'email' : email,
              'user' : request.user.id}
      form = UserAddUserForm(data)
      #print form.errors
      if form.is_valid():
        #user = User.objects.create_user(username, email, password)
        #user.first_name = first_name
        print form.cleaned_data
        email_cleaned = form.cleaned_data['email']
        username_cleaned = form.cleaned_data['username']
        #user.last_name = last_name
        form.is_active = False
        form.save()
        #Enviando un correo para que pueda activar su cuenta
        message = "http://%s%s?u=%s&user=%s" % (
          settings.DOMAIN_NAME, 
          reverse('users.views.confirm'),  
          hashlib.md5(settings.KEY_STRING+username_cleaned+email_cleaned).hexdigest(),
          username_cleaned
        ) 
        email = EmailMessage('Hello', message, to=['juanros13@gmail.com'])
        email.send()

        success = True
        to_return['success'] = True
      else:
        to_return['errors'] = form.errors
      #else:
        #to_return['msg'] = u"El usuario ya se encuentra segistrado."
    else:
      to_return['msg'] = u"El password no coincide."
  else:
      to_return['msg'] = u"Faltan datos requeridos."
        #return HttpResponse('OK')
      #return HttpResponse('ERROR: El ususario y correo ya estan dado de alta')
    #return HttpResponse('ERROR: Los password no coinciden ')  
  #return HttpResponse('ERROR: Debes llenar todos los campos obligatorios')
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

def disconnect(request):
  logout(request)
  return HttpResponseRedirect('/')

@login_required
def user_shop(request):
  if request.user.is_active:
    shop = Shop.objects.get(user=request.user)
    print shop
    return render_to_response('aldrovanda/user_add_shop.html', {
      'shop' : shop,
    }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/')

def confirm(request):
  username = request.GET['user']
  key = request.GET['u']
  url = reverse('aldrovanda.views.index')
  try:
    user = User.objects.get(username=username)
    if hashlib.md5(settings.KEY_STRING+user.username+user.email).hexdigest() == key :
      if user.is_active:
        #return HttpResponse('El usuario ya se encuentra activo')
        request.session['_info_message'] = 'El usuario (%s) ya se encuentra activo' % user.username
        return HttpResponseRedirect(url)
        #return render_to_response('aldrovanda/users/info_message.html', {
        #'message' : 'El usuario ya se encuentra dado de alta',
        #}, context_instance=RequestContext(request))
      else:
        if not user.is_staff:
          if not user.is_superuser:
            user.is_active = True
            user.save()
          else:
            return HttpResponse('Really2?') 
        else:
          return HttpResponse('Really?')
      request.session['_info_message'] = 'El usuario (%s) ha sido activado con exito' % user.username
      return HttpResponseRedirect(url)
    else:
      request.session['_info_message'] = 'El key no es valido'
      return HttpResponseRedirect(url)
      #return HttpResponse('El key no es valido')
  except User.DoesNotExist:
    request.session['_info_message'] = 'El usuario (%s) no existe' % username
    return HttpResponseRedirect(url)
  return HttpResponse('NO OK')
  
def test(request):
  usuario = User.objects.get(email='lobo022000@gmail.com', username='juanros13')
  current_site = get_current_site(request)
  print usuario
  return HttpResponse( "%s:>>><<<<%s:8000%s?u=%s&id=%s" % (
      settings.KEY_STRING+usuario.username+usuario.email,  
      current_site.domain, 
      reverse('users.views.confirm'),  
      hashlib.md5(settings.KEY_STRING+usuario.username+usuario.email).hexdigest(),
      usuario.username
    ) 
  )