
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
/*$.fn.sort_select_box = function(){
    var my_options = $("#" + this.attr('id') + ' option');
    my_options.sort(function(a,b) {
        if (a.text > b.text) return 1;
        else if (a.text < b.text) return -1;
        else return 0
    })
   return my_options;
}*/
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

$('#add-shop').validate({
  rules: {
    shop: {
      minlength: 4,
      required: true,
      regex: "^[a-zA-Z0-9]+$",
      uniqueShopName: true
    },

  },
  messages: {
    shop: {
      required: "El nombre de al tienda no puede estar en blanco.",
      minlength: "El nombre de la tienda debe tener mimino 4 caracteres",
      regex: "El nombre de la tienda solo puede tener numeros y letras"
    }
  },
  errorLabelContainer: ".help-block",
  highlight: function(label) {
    //$(".help-block").html('');
    $(label).closest('.control-group').addClass('error');
    $(".legend-shop").html('');
    $("#preloader-shop").html('');
    $('#btn-add-shop').attr("disabled", "disabled");
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
    $(".legend-shop").html('Puedes cambiar el nombre de la tienda despues.');
    //$('#preloader-shop').html('<i class="icon-ok icon-green"></i>');
    $("#preloader-shop").html('');
    $('#btn-add-shop').removeAttr("disabled");        
  },
  submitHandler: function(form) {
    //alert($('#name-shop').val());
    var nameShop = $('#name-shop').val();
    $.post('/usuario/tienda/add/', {shop:nameShop}, function(json) {
      if (json.success) {
        //$('#preloader-shop').html('<i class="icon-ok icon-green"></i>');
        //$(".legend-shop").html('Puedes cambiar el nombre de la tienda despues.');
        //alert('ok');
        window.location.href = json.url;
      } else {
        if(json.msg.user){
          alert(json.msg.user);
        }else{
          alert(json.msg.name);
        }
        //$('#preloader-shop').html('<i class="icon-ok icon-green"></i>');
        //$(".legend-shop").html('');
        //$(form).find('div.control-group').addClass('error');
        //alert('NoOk');
      }
      return;
          // Etc ...
      }) 
      .error(function(e) { alert('Error:'+e); });
  },
});
