$(document).ready(function() {

	$("#menu-bar").hide();

	$("#menu-icon").click(function () {
		$("#menu-bar").toggle();
	});

	$(".comment-reply").hide();

	$(".reply-button").click(function () {
		var button = $(this).attr("id").split("-")[1];
		$("#comment-" + button).show();
	});

	$(".cancel-button").click(function () {
		var button = $(this).attr("id").split("-")[1];
		$("#comment-" + button).hide();
	});

	$("#varieties").hide();

	$("#filter-postings-link").click(function () {
		$("#varieties").toggle();
	});

	$("#community-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-co").slideDown(350);
		} else {
			$(".feed-co").slideUp(350);
		}
	});

	$("#events-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-ev").slideDown(350);
		} else {
			$(".feed-ev").slideUp(350);
		}
	});

	$("#government-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-go").slideDown(350);
		} else {
			$(".feed-go").slideUp(350);
		}
	});

	$("#politics-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-po").slideDown(350);
		} else {
			$(".feed-po").slideUp(350);
		}
	});

	$("#volunteering-box").click(function() {
		if($(this).is(":checked")) { 
			$(".feed-vo").slideDown(350);
		} else {
			$(".feed-vo").slideUp(350);
		}
	});

});