$(document).ready(function(){
	
	$("#about-btn").addClass('btn btn-primary');
	$("#about-btn").click( function(event){
		msgtr = $("#msg").html()
		msgtr = msgtr + "o"
		$("#msg").html(msgtr)
	});
	$('#like').click(function(){
			var cat_id;
			cat_id = $(this).attr("data-catid");
			$.get('/rango/like_category/',{category_id: cat_id},function(data){
				$('#like_count').html(data);
				$('#like').hide();
			});
    });
	
	$('#suggestion_id').keyup(function(){
		var startswith;
		startswith = $(this).val();
		$.get('/rango/suggest_category/',{query_string: startswith},function(data){
		    $('#cats').html(data);
		});
	});
});