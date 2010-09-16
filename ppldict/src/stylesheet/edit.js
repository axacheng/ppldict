$(document).ready(function(){
	$(".edit_button").click(function(){
    var element = $(this);
		var edit_key = element.attr("id");
//		$('#' + edit_key).slideToggle(300);
//    $(".edit_div")/
//		$('#' + edit_key).toggleClass("highlight");
  
    //$(".edit_div").toggleClass("edit_div");
		$(".edit_div").show();
    
		return false;
});  
}); 