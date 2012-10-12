/* Author: Rosales Vargas Juan Roberto @lobo022000

*/
//Validacion de la forma para recuperar pass
$('#id-recovery-form').validate({
  rules: {
     email: {
      required: true,
      email: true
    },
  },
  highlight: function(label) {
    $(label).closest('.control-group').addClass('error');
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
  }
});
$('#id-recovery-form-save').validate({
  rules: {
    password1: {
      required: true,
      minlength: 6,
      noSpace: true,
    },
    password2: {
      required: true,
      minlength: 6,
      noSpace: true,
      equalTo: "#id-password"
    },
  },
  highlight: function(label) {
    $(label).closest('.control-group').addClass('error');
  },
  success: function(label) {
    label.closest('.control-group').removeClass('error');
  }
});

