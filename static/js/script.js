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
    //alert(ui.item.index());
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
  //alert(category);
  $.post('/categoryHierarchy/', {'category':category}, function(json) {
    //alert(json);
    if (json.success) {
      //alert('OK');
      //alert(json.level);
      if(json.categories){

        preloadImage(levelCategory[json.level], 'preloded_30X30_blue', {'margin':'auto', 'padding-top':'40px'});
        //alert('#'+levelCategory[json.level]);
        $('#'+levelCategory[json.level]).html("<label>¿De que tipo?</label>"+createSelect(levelCategory[json.level]+"-select", "category-select", json.categories, {"value":"", "name": "--Selecciona un tipo--"}));
      }else{
        $('#'+levelCategory[json.level]).html('');
      }
    }else{
      alert('Tuvimos un problema');
    }
    return;
  }) 
});

function preloadImage(target, nameImage, style){
  //alert(target);
  contentHtml=$('#'+target);
  //styles=style.join(';') 
  var styleInline = '';
  $.each(style, function(key, value) {
    styleInline +=key+":"+value+";";
  });
  //alert(styleInline);
  contentHtml.html('<img style="'+styleInline+'" src="../static/img/'+nameImage+'.gif" />');
}

function preloadImageUpload(inputFile){
  var liUploadImage = inputFile.parent().parent().find(".add-photos-button");
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

$('#tags-product').typeahead({
  source:function (query, process) {
    if(query.length>=3 && query.length<=5){
      $.post('/getTags/', { query: query }, function (data) {
        //alert(data);
        return process(data);
      });
    }
  },
  minLength:3,
  items:15
});
$('#materials-product').typeahead({
  source:function (query, process) {
    if(query.length>=3 && query.length<=5){
      $.post('/getMaterials/', { query: query }, function (data) {
        //alert(data);
        return process(data);
      });
    }
  },
  minLength:3,
  items:15
});


$('#tags-product, #materials-product').keyup(function(){
    this.value = this.value.toLowerCase();
});
$.fn.sort_select_box = function(){
    var my_options = $("#" + this.attr('id') + ' option');
    my_options.sort(function(a,b) {
        if (a.text > b.text) return 1;
        else if (a.text < b.text) return -1;
        else return 0
    })
   return my_options;
}
$('.tag').live('close', function () {
  var button = $(this).find('button'),
  inputHidden = $(this).find('input'),
  arrayInput = button.attr('id').split('--'),
  inputVal = arrayInput[1],
  inputText = arrayInput[2],
  inputTarget = $('#'+arrayInput[0]);

  if(inputTarget.is('select')){
    //inputTarget[options.length] = new Option(inputHidden.val(), inputHidden.val(), true, true);
    inputTarget.append(new Option(inputText,inputVal, true, true));

    //ordenando las opciones orden alfabetico
    var my_options = $("#"+arrayInput[0]+" option");

    my_options.sort(function(a,b) {
        if (a.text > b.text) return 1;
        else if (a.text < b.text) return -1;
        else return 0
    })

    inputTarget.empty().append( my_options );
    inputTarget.val('');
  }
  

  //alert(inputTarget.attr('id'));
  if(inputTarget.is(':disabled')){
    inputTarget.removeAttr('disabled');
  }
})

$('#style-product').change(function(){
  addTag('styles', 'style-product', 2);
});

$('#add-tag').click(function(){
  addTag('tags', 'tags-product', 5);
});
$('#add-material').click(function(){
  //Si tiene algo el input de tag agregarlo de lo contrario no hacer nada
  addTag('materials', 'materials-product', 5);
});
function addTag(target, inputName, maximNumberOfItems){
  var target = $('#'+target),
  numberOfItems = target.children().length,
  input = $('#'+inputName);
  //alert(numberOfItems);
  if(input.val()!=''){
    
    target.append('<span class="tag">'+
      '<button type="button" class="close" data-dismiss="alert" id="'+inputName+'--'+input.val()+'--'+input.find("option:selected").text()+'" >&times;</button>'+
      input.val()+
      '<input type="hidden" name="'+inputName+'['+target.length+']"  value="'+input.val()+'" />'+
    '</span>');
    if(input.is('select')){
      //alert("es un maldito select");
      input.find('[value="'+input.val()+'"]').remove();
    }else{
      input.val('');  
    }
    if(numberOfItems>=maximNumberOfItems-1){
      input.attr("disabled", "disabled");
    }
  } 
}
$('#add-shop').validate({
  ignoreTitle: true,
  debug: true,
  rules: {
    shop: {
      minlength: 4,
      required: true,
    },

  },
  messages: {
    shop: {
      required: "El nombre de al tienda no puede estar en blanco.",
      minlength: "El nombre de la tienda debe tener mimino 4 caracteres",  
    }
    
  },
  errorLabelContainer: ".help-block",
  highlight: function(label) {
    $(".help-block").html('');
    $(label).closest('.control-group').addClass('error');
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
    $(".help-block").remove();
    $("#error-content").html('<span class="help-block">Puedes cambiar el nombre de la tienda despues.</span>');
    //alert("success");
  },
  submitHandler: function() {
    alert("enviando");
  },
});