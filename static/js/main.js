$(document).ready(function () {
    $('.navbar-nav a').on('click', function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Login Modal
    $('#loginButton').click(function () {
        $('#loginModal').modal('show');
    })

    // Location Modal
    $('#locationButton').click(function () {
        $('#locationModal').modal('show');
    })

    // Location Modal
    $('#signinButton').click(function () {
        $('#signinModal').modal('show');
    });
});

//google map
//set map options
var myLatLng = { lat: 19.09761241932646, lng: 72.88250110269311 };
var mapOptions = {
    center: myLatLng,
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

//create map
var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);


//create a DirectionsRenderer object which we will use to display the route
var directionsDisplay = new google.maps.DirectionsRenderer();

//bind the DirectionsRenderer to the map
directionsDisplay.setMap(map);



//define calcRoute function
function calcRoute() {
    //create request
    var request = {
        origin: document.getElementById("address1").value,
        destination: document.getElementById("address2").value,
        travelMode: google.maps.TravelMode.DRIVING, //WALKING, BYCYCLING, TRANSIT
        unitSystem: google.maps.UnitSystem.IMPERIAL
    };

    //create a DirectionsService object to use the route method and get a result for our request
    var directionsService = new google.maps.DirectionsService();

    //pass the request to the route method
    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {

            //Get distance and time
            const output = document.querySelector('#output');
            output.innerHTML = "<div class='alert-info'>From: " + document.getElementById("from").value + ".<br />To: " + document.getElementById("to").value + ".<br /> Driving distance <i class='fas fa-road'></i> : " + result.routes[0].legs[0].distance.text + ".<br />Duration <i class='fas fa-hourglass-start'></i> : " + result.routes[0].legs[0].duration.text + ".</div>";

            //display route
            directionsDisplay.setDirections(result);
        } else {
            //delete route from map
            directionsDisplay.setDirections({ routes: [] });
            //center map in London
            map.setCenter(myLatLng);

            //show error message
            output.innerHTML = "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve driving distance.</div>";
        }
    });

}

//create autocomplete objects for all inputs
var options = {
    types: ['(cities)']
}

var input1 = document.getElementById("address1");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("address2");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

//Price calculation and map form info
function price_map_info() {
    var kg = $('#kg_value').val();
    var price_per_kg = 5;
    var distance = 10;
    var total_price = Math.round(kg * price_per_kg * distance);
    var price = 'Amt : ' + total_price + ' ₹';
    document.getElementById('price').innerHTML = price;
    var info = {
        'name1' : $('#name1').val(),
        'address1' : $('#address1').val(),
        'number1' : $('#number1').val(),
        'name2' : $('#name2').val(),
        'address2' : $('#address2').val(),
        'number2' : $('#number2').val(),
        'kg' : kg,
        'amount': total_price,
    };
    $.ajax({
        url: "map",
        type: "GET",
        data: info,
    });
}

// Razorpay
function razorpay() {
    var payment = JSON.parse(document.getElementById('payment').textContent);
    var razorpay_api_key = JSON.parse(document.getElementById('razorpay_api_key').textContent);
    var amount = payment.amount;
    var currency = payment.currency;
    var order_id = payment.id;
    var options = {
        "key": razorpay_api_key,
        "amount": amount,
        "currency": currency,
        "name": "WeDeliver",
        "description": "Fast and Secure",
        "image": "https://images.crowdspring.com/blog/wp-content/uploads/2017/07/27131755/9b475a68-ee0f-4895-8082-2a4706cfeb4b.png",
        "order_id": order_id,
        "callback_url":"success",
        // "handler": function (response) {
        //     var payment_id = response.razorpay_payment_id;
        //     sessionStorage.setItem("paymentid", payment_id);
        //     var date = new Date();
        //     var n = date.toDateString();
        //     var time = date.toLocaleTimeString();
        //     paid_on = n + ' ' + time;
        //     sessionStorage.setItem("paidon", paid_on);
        //     window.location.href = "success";
        // },
        "prefill": {
            "name": "'Gaurav Kuma'r",
            "email": "gaurav.kumar@example.com",
            "contact": "9999999999"
        },
        "notes": {
            "address": "WeDeliver"
        },
        "theme": {
            "color": "#F37254"
        }
    };

    var rzp1 = new Razorpay(options);
    rzp1.on('payment.failed', function (response) {
        alert(response.error.code);
        alert(response.error.description);
        alert(response.error.source);
        alert(response.error.step);
        alert(response.error.reason);
        alert(response.error.metadata.order_id);
        alert(response.error.metadata.payment_id);
    });
    document.getElementById('rzp-button').onclick = function (e) {
        rzp1.open();
        e.preventDefault();
    }
}

function backpage() {
    history.back()
}