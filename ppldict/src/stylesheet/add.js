$(document).ready(function(){
  $(document).ready

	
	//First hide form on add_form, when user clicking 'Add' it will show up
	$(".toggle").click(function(){
    $("#add_main").slideToggle("fast");
    }) 
    $("#add_main").hide()
    
  // Animation, for submitting form
  $('#add_form').submit(function(){
			var form = $(this),
			formData = form.serialize(),
			formMethod = form.attr('method'),
			responseText = $('#submit_result') 
			responseText.hide()
			            .addClass('waiting')
									.text('Please wait...')
									.fadeIn(200);
    $.ajax({
				url: "/add",
				type: formMethod,
				data: formData,
				success: function(data){
					var responsData = $.parseJSON(data),
					    responseData_class = '';
					switch(responsData.status){
						case 'error':
						  responseData_class = 'response_error';
						break;
						case 'success':
						  responseData_class = 'response_success';
						break;				
					}
					
					responseText.fadeOut(200, function(){
						$(this).removeClass('waiting')
						       .addClass(responseData_class)
									 .text(responsData.message)
									 .fadeIn(200,function(){
									     setTimeout(function(){
									     responseText.fadeOut(200,function(){
									         $(this).removeClass(responseData_class);
										 });
										 }, 3000);
					$("#add_main").slideToggle("slow");
									 });
					
					});					
//					alert(responsData.message);
				}
			});

			return false;
    })

})
