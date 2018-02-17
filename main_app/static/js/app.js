$('button').on('click', function(event){
	event.preventDefault();
	var element = $(this);
	$.ajax({
		url: '/like_treasure/',
		method: 'GET',
		data: {treasure_id: element.attr('data-id')},
		success: function(response){
		  element.html('Likes: ' + response);
		}
	})
})