$(document).ready(function() {
	// Login and Signin hide/show
	$('#login-button').click(function() {
		$('#signup-box').attr('hidden', '');
		$('#login-box').removeAttr('hidden');
	});

	$('#signup-button').click(function() {
		$('#login-box').attr('hidden', '');
		$('#signup-box').removeAttr('hidden');
	});
});