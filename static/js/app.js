$(document).ready(function() {
	$('.card').click(function() {
		if ($(this).hasClass('grayscale'))
			$(this).removeClass('grayscale');
		else
			$(this).addClass('grayscale');

	});
});