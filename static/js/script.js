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

$(".img-thumbnail")
    .click(function() { 
    	var src = $(this).attr("src");
    	var src = src.split('.');
    	//alert(src[0]);
        $(".img-sorce").attr("src", src[0]+"."+src[1]+".600x600_q85_crop.jpg");
        $(".img-sorce").parent("a").attr("href", src[0]+"."+src[1])
    })
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
    equalTo: "Ingrese el mismo valor",    
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

			$.post('/login/', data, function(json) {
		    if (json.success) {
	        location.reload();
		    } else {
          $error.html(header_error+json.msg).slideDown(400).delay(1500).slideUp(400);
        }
        return;
			    // Etc ...
			}) 
			.error(function(e) { alert('error'+e); });
	},
});
//Validacion de la forma para Registrarse
$('#id-register-form').validate(
{
rules: {
  first_name: {
    minlength: 2,
    required: true
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
  },
  password_repeat: {
    required: true,
    minlength: 6,
  },
  username: {
    required: true,
    minlength: 6,
  },
},
highlight: function(label) {
  $(label).closest('.control-group').addClass('error');
},
success: function(label) {
  label.closest('.control-group').removeClass('error');
},
//submitHandler: function() {
		//alert("submit! use link below to go to the other step");
//},
});

////////////////////////////////
//Add favorite product
////////////////////////////////

$('.btn-favorite').click(function(){
  
  var $form     = $('#id-favorite-form'),
  data          = $form.serializeArray(),
  $icono        = $(this).find('i:first'),
  $img          = $(this).find('img:first'),
  $error        = $('#error-favorite'),
  action        = $form.attr('action'),
  header_error  = '<h4 class="alert-heading">Error</h4>';

  $icono.addClass('hide');
  $img.removeClass('hide');
  //alert($form.attr('action'));
  $.post(action, data, function(json) {
    if (json.success) {
      //alert('OK');
      if(action=='/addFavorite/'){
        $form.get(0).setAttribute('action', '/removeFavorite/');
        $icono.removeClass('hide').addClass('icon-red');
      }else{
        $form.get(0).setAttribute('action', '/addFavorite/');
        $icono.removeClass('hide').removeClass('icon-red');
      }
    } else {
      $('error-product').html(header_error+json.msg).slideDown(400).delay(1500).slideUp(400);
    }
    //$img.hide();
    //$icono.show();
    return;
      // Etc ...
  }) 
  .error(function(e) { alert('Error:'+e); });
  $icono.removeClass('hide').removeClass('icon-red');
  $img.addClass('hide');
});
$("[rel=tooltip]").tooltip({placement:'bottom'});
$('[rel=popover]').popover()


$( "#photos" ).sortable({
  items: "li:not(.state-disabled)",
  update: function(event, ui) {
    var info = $(this).sortable("serialize");
    //$("#sort1output").html(info);
    alert(ui.item.index());
  }
});
$( "#photos" ).disableSelection();
/* Se usa pra mover el input file pero se pudo acomodar con puro css
$(".upload-container").mousemove(function(e) {
    var offL, offR, inpStart
    offL = $(this).offset().left;
    offT = $(this).offset().top;
    aaa= $(this).find("input").width();
    $(this).find("input").css({
        left:e.pageX-aaa-30,
        top:e.pageY-offT-10
    })
}); */
$('#image-upload').live('change', function(){
  var inputFile = $(this);
  var options = { 
    url:        '../uploadImage/', 
    afterSubmit : preloadImageUpload(inputFile),
    success: function(imagen){
        //alert(jqueryWreapper.html());
        //alert(liImage.html)
        var liUploadImage = inputFile.parent().parent();
        liUploadImage.removeClass('state-disabled');
        liUploadImage.html('<div class="add-photos-button"><img height="80" style="margin:auto;" src="'+imagen+'" /></div>');
        var liNewUploadImage = liUploadImage.next();
        liNewUploadImage.html('<div class="upload-container">'+
                                  '<input type="file" name="image-upload" id="image-upload" class="image-upload" multiple/>'+
                              '</div>'+
                              '<div class="add-photos-button">'+
                                '<div class="image-active-icon">'+
                                  '<i class="icon-plus-sign icon-blue"></i>'+
                                '</div>'+
                                '<span>Add Photos</span>'+
                              '</div>');
    },
    target: true
  };
  $("#add-product").ajaxForm(options).submit();
});

$('select.category-select').live("change", function(){
  //alert($(this).val());
  var category    = $(this).val(),
  levelCategory   = ["second-categories","third-categories","fourth-categories"];
  levelCategoryDivName   = ["second-categories","third-categories","fourth-categories"];
  //alert(category);
  $.post('/categoryHierarchy/', {'category':category}, function(json) {
    //alert(json);
    if (json.success) {
      //alert('OK');
      //alert(json.level);
      if(json.categories){
        if(json.level){
          preloadImage(levelCategory[json.level]);
        }
        //alert('#'+levelCategory[json.level]);
        $('#'+levelCategory[json.level]).html("<h5>De que tipo?</h5>"+createSelect(levelCategory[json.level]+"-select", "category-select", json.categories, {"value":"", "name": "--Selecciona un tipo--"}));
      }else{
        $('#'+levelCategory[json.level]).html('');
      }
    }else{
      alert('Tuvimos un problema');
    }
    return;
  }) 
});

function preloadImage(target, image){

}

function preloadImageUpload(inputFile){
  var liUploadImage = inputFile.parent().parent().find(".add-photos-button");
  liUploadImage.html('');
  liUploadImage.html('<img style="margin:auto;padding-top:20px;"src="../static/img/preloded_upload_image.gif" />');
}
function createSelect(id, nameclass, data, dataDefault){
  //alert(nameclass);
  var result = '<select id="'+id+'"  class="'+nameclass+'" >';
  
  if(data){
    if(dataDefault){
      //alert('wtf');
      result += '<option value="'+dataDefault.value+'"" selected>'+dataDefault.name+'</option>';
    }
    $.each(data, function(key, value) {
      result += '<option value="'+key+'"">'+value+'</option>';
    });
  }else{
    result
  }
  result += '</select>';
  //alert(result);
  return result;
}