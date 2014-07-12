$(document).ready(function() {
	$('.app-icon').click(function() {
		if ($(this).hasClass('grayscale'))
			$(this).removeClass('grayscale');
		else
			$(this).addClass('grayscale');
		alert('activated');
	});
});