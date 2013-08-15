$(document).ready(function() {

	$(".comment-reply").hide();

	$(".reply-button").click(function () {
		var button = $(this).attr("id").split("-")[1];
		$("#comment-" + button).show();
	});

	$(".cancel-button").click(function () {
		var button = $(this).attr("id").split("-")[1];
		$("#comment-" + button).hide();
	});

});