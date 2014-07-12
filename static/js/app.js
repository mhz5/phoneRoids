$(document).ready(function() {
	$('.card').click(function() {
		if ($(this).hasClass('grayscale'))
			$(this).removeClass('grayscale');
		else
			$(this).addClass('grayscale');

	});

	$('[data-toggle=offcanvas]').click(function() {
		$('.row-offcanvas').toggleClass('active');

		

	});
});

