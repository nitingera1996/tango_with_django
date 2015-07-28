$('#like').click(function(){
	var cat_id;
	alert("You clicked");
	cat_id = $(this).attr("data-catid");
	alert("You clicked");
	$.get('/rango/like_category/',{category_id: cat_id},function(data){
		$('#like_count').html(data);
		$('#like').hide();
	});
});