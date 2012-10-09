function preloadImage(target, nameImage, style){
  //alert(target);
  contentHtml=$('#'+target);
  //styles=style.join(';') 
  var styleInline = '';
  $.each(style, function(key, value) {
    styleInline +=key+":"+value+";";
  });
  //alert(styleInline);
  contentHtml.html('<img style="'+styleInline+'" src="/static/img/'+nameImage+'.gif" />');
}
function preloadImage(target, nameImage, style){
  //alert(target);
  contentHtml=$('#'+target);
  //styles=style.join(';') 
  var styleInline = '';
  $.each(style, function(key, value) {
    styleInline +=key+":"+value+";";
  });
  //alert(styleInline);
  contentHtml.html('<img style="'+styleInline+'" src="/static/img/'+nameImage+'.gif" />');
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
$.validator.addMethod("noSpace", function(value, element) { 
  return value.indexOf(" ") < 0 && value != ""; 
}, "No pueden existir espacios en blanco para el nombre de la tienda");

var nameShopValid, nameShop;
$.validator.addMethod("uniqueShopName", function(value, element) {
    preloadImage('preloader-shop', 'preloded_30X30_blue','');
    $.ajaxSetup({async: false});
    if(nameShop!=value){
      $.post('/usuario/tienda/validate/', {shop:value}, function(json) {
        if (json.success) {
          nameShopValid = true;

        } else {
          nameShopValid = false;
        }
      });
    nameShop=value;
    }
    $.ajaxSetup({async: true});
    return nameShopValid;
}, "El nombre de la tienda ya esta tomado.");
$.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your input."
);