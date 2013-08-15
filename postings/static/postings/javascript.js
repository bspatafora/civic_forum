$(document).ready(function() {

	$(".comment-reply").hide();

	$(".reply-button").click(function () {
		var button = $(this).attr("id");
		$("#comment-" + button).show();
	});

});