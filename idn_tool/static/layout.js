$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();
});

$('.nav div.main_list ul li a').click(function () {
    $('.navTrigger').toggleClass('active');
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();
});

// Make the main menu item active (based on page title)
$(document).ready(function() {
 var className = document.getElementsByClassName('dropdown-item');
   for(var index=0;index < className.length;index++){
      if (className[index].innerHTML===document.title) {
        $(className[index]).addClass('active_menu_item');
      }
      else {$(className[index]).removeClass('active_menu_item');}
   }

});


