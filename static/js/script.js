/* Author: Rosales Vargas Juan Roberto @lobo022000

*/

$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$('.dropdown-toggle').dropdown()

$(".img-thumbnail").click(function() { 
  var src = $(this).attr("src");
  var src = src.split('.');
  //alert(src[0]);
  $(".img-sorce").attr("src", src[0]+"."+src[1]+".600x600_q85_crop.jpg");
  $(".img-sorce").parent("a").attr("href", src[0]+"."+src[1])
});
//$('#login').modal(options)
// translate validator error msg
$.extend($.validator.messages, {
    required: "Campo obligatorio",
    remote: "Por favor corrige este campo",
    email: "Ingrese una direccion de email valida",
    url: "Ingrese una url valida",
    date: "Ingrese una fecha valida",
    dateISO: "Ingrese una fecha valida (ISO)",
    number: "Ingrese un numero", 
    digits: "Ingrese solo digitos",
    creditcard: "Ingrese un numero de tarjeta valida",
    equalTo: "Los password no coincien",    
    accept: "Ingrese una extension valida",
    maxlength: $.validator.format("No es posible ingresar mas de {0} catacteres"),
    minlength: $.validator.format("Ingrese al menos {0} caracteres"),
    rangelength: $.validator.format("Ingrese un valor con un minimo {0} y maximo {1} caracteres"),
    range: $.validator.format("Ingrese un valor entre {0} y {1}"),
    max: $.validator.format("Ingrese un valor menor o igual a {0}"),
    min: $.validator.format("Ingrese un valor mayor o igual a {0}")
});
//Validacion de la forma para Login
$('#id-login-form').validate({
  rules: {
    username: {
      minlength: 2,
      required: true
    },
    password: {
      required: true,
      minlength: 6
    },
  },
  highlight: function(label) {
    $(label).closest('.control-group').addClass('error');
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
  },
  submitHandler: function() {
    //Get the data from all the fields
    var $form     = $('#id-login-form'),
    data          = $form.serializeArray(),
    $error        = $form.find('div.alert-error:first')
    header_error  = '<h4 class="alert-heading">Error</h4>';

		$.post('/user/login/', data, function(json) {
	    if (json.success) {
        location.reload();
	    } else {
        $error.html(header_error+json.msg).slideDown(400).delay(1500);
      }
      return;
		    // Etc ...
		}) 
		.error(function(e) { alert('error'+e); });
	},
});
//Validacion de la forma para Registrarse
$('#id-register-form').validate({
  rules: {
    /*first_name: {
      minlength: 2,
      required: true,
      
    },
    last_name: {
      required: true,
      minlength: 2,
    },
    email: {
      required: true,
      email: true
    },
    password: {
      required: true,
      minlength: 6,
      noSpace: true,
    },
    password_repeat: {
      required: true,
      minlength: 6,
      noSpace: true,
      equalTo: "#id_password"
    },
    username: {
      required: true,
      minlength: 6,
      regex: "^[a-zA-Z0-9]+$",
    },*/
  },
  messages: {
    username: {
      regex: "El usuario solo puede tener numeros y letras"
    },
    password: {
      noSpace: "El password no puede contener espacios en blanco"
    },
    password_repeat: {
      noSpace: "El password no puede contener espacios en blanco"
    }
  },
  highlight: function(label) {
    $(label).closest('.control-group').addClass('error');
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
  },
  submitHandler: function(form) {
    //Get the data from all the fields

    var $form     = $(form),
    data          = $form.serializeArray(),
    $error        = $form.find('div.alert-error:first')
    header_error  = '<h4 class="alert-heading">Error</h4>';

    $.post('/user/register/', data, function(json) {
      if (json.success) {
        $error.html('').slideUp(400);
        location.reload();
      } else {
        if(json.errors){
          $error.html(header_error);
          $.each(json.errors, function(err, val){
            $error.append(val+"<br>")
          });
          $error.slideDown(400).delay(2500);  
        }else{
          $error.html('').html(header_error+json.msg).slideDown(400).delay(2500);  
        }
      }
      return;
        // Etc ...
    }) 
    .error(function(e) { alert('error'+e); });
  },
});



