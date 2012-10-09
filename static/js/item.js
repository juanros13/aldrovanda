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
      if(action=='/favorite/add/item/'){
        $form.get(0).setAttribute('action', '/favorite/remove/item/');
        $icono.removeClass('hide').addClass('icon-red');
      }else{
        $form.get(0).setAttribute('action', '/favorite/add/item/');
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