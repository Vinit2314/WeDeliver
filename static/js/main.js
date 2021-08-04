$(document).ready(function(){
    $('.navbar-nav a').on('click', function(){
        $('.navbar-collapse').collapse('hide');
    });
});

// Login Modal
$('#loginModal').click(function () {
    $('#loginButton').modal('show');
})


// Location Modal
$('#locationModal').click(function () {
    $('#locationButton').modal('show');
})

// Location Modal
$('#sighinModal').click(function () {
    $('#signinButton').modal('show');
});