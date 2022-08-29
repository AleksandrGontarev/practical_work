$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#contact .modal-content").html("");
        $("#contact").modal("show");
      },
      success: function (data) {
        $("#contact .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
               // $("#contact").fadeOut("fast", function(){
               //    $(this).before("<strong>Email send :)</strong>");
               //
               // });
          $("#contact .modal-content").html(data.html_contact)
          $("#contact").modal("show");

        }
        else {
          $("#contact .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-contact").click(loadForm);
  $(".ajax-modal").on("submit", ".jx-jx", saveForm);


});
