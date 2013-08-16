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

	$("#community-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-community").slideDown(350);
		} else {
			$(".feed-community").slideUp(350);
		}
	});

	$("#governance-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-governance").slideDown(350);
		} else {
			$(".feed-governance").slideUp(350);
		}
	});

	$("#politics-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-politics").slideDown(350);
		} else {
			$(".feed-politics").slideUp(350);
		}
	});

});