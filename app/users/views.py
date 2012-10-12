# -*- encoding: utf-8 -*-
import hashlib
import datetime
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
        #print form.cleaned_data
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
        email = EmailMessage('Hello', message, to=[email_cleaned], bcc=['juanros13@gmail.com'])
        email.send()
        request.session['_info_message'] = 'Se ha enviado un correo de confirmacion a (%s) para validar el registro' % email_cleaned
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

def forgot_password(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  return render_to_response('aldrovanda/users/request_change_password.html', {
    'message':message,
  }, context_instance=RequestContext(request))

@require_POST
def forgot_password_send_mail(request):
  email = request.POST['email']
  url_warning = reverse('users.views.forgot_password')
  url_success = reverse('aldrovanda.views.index')
  if email:
    try:
      user = User.objects.get(email=email)
      now = datetime.datetime.now().strftime("%Y-%m-%d")
      print now
      message = "http://%s%s?u=%s&email=%s" % (
        settings.DOMAIN_NAME, 
        reverse('users.views.pass_recovery'),  
        hashlib.md5(settings.KEY_STRING+now+email).hexdigest(),
        email
      ) 
      mail = EmailMessage('Hello', message, to=[email], bcc=['juanros13@gmail.com'])
      mail.send()
      request.session['_info_message'] = 'El correo de recuperacion fue enviado a %s' % email
      return HttpResponseRedirect(url_success)
    except User.DoesNotExist:
      request.session['_info_message'] = 'El correo (%s) no esta dado de alta en nuestra base de datos' % email
      return HttpResponseRedirect(url_warning)
  else:
    return HttpResponse('NO OK')

def pass_recovery_save(request):
  email = request.POST['email']
  key = request.POST['key']
  password = request.POST['password1']
  password2 = request.POST['password2']
  url = reverse('aldrovanda.views.index')
  now = datetime.datetime.now().strftime("%Y-%m-%d")
  if password == password2:
    try:
      user = User.objects.get(email=email)
      if hashlib.md5(settings.KEY_STRING+now+email).hexdigest() == key :
        if user.is_active:
          if not user.is_staff and not user.is_superuser:
            user.set_password(password)
            user.save()
            request.session['_info_message'] = 'El password fue cambiado correctamente (%s)' % email
            return HttpResponseRedirect(url)
          else:
            request.session['_info_message'] = 'Los miembros del staff no puede cambiar su password de esta forma'
            return HttpResponseRedirect(url)
        else:
          request.session['_info_message'] = 'Mientras tu usuario no este activo no puedes cambiar el password'
          return HttpResponseRedirect(url)
      else:
        request.session['_info_message'] = 'El key no es valido'
        return HttpResponseRedirect(url)
        #return HttpResponse('El key no es valido')
    except User.DoesNotExist:
      request.session['_info_message'] = 'El usuario (%s) no existe' % email
      return HttpResponseRedirect(url)
  else:
    request.session['_info_message'] = 'Los passwords no coniciden'
    return HttpResponseRedirect(url)
  return HttpResponse('NO OK')

def pass_recovery(request):
  email = request.GET['email']
  key = request.GET['u']
  url = reverse('aldrovanda.views.index')
  now = datetime.datetime.now().strftime("%Y-%m-%d")
  try:
    user = User.objects.get(email=email)
    if hashlib.md5(settings.KEY_STRING+now+email).hexdigest() == key :
      if user.is_active:
        if not user.is_staff and not user.is_superuser:
          return render_to_response('aldrovanda/users/change_password.html', {
            'key':key,
            'email':email,
          }, context_instance=RequestContext(request))
        else:
          request.session['_info_message'] = 'Los miembros del staff no puede cambiar su password de esta forma'
          return HttpResponseRedirect(url)
      else:
        request.session['_info_message'] = 'Mientras tu usuario no este activo no puedes cambiar el password'
        return HttpResponseRedirect(url)
    else:
      request.session['_info_message'] = 'El key no es valido'
      return HttpResponseRedirect(url)
      #return HttpResponse('El key no es valido')
  except User.DoesNotExist:
    request.session['_info_message'] = 'El usuario (%s) no existe' % email
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