$(document).ready(function () {
    $('.navbar-nav a').on('click', function () {
        $('.navbar-collapse').collapse('show');
    });

    //Login Modal
    $('#loginButton').click(function () {
        $('#loginModal').modal('show');
    })

    //Reset Login Modal Modal
    $('#loginModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })

    //Location Modal
    $('#locationButton').click(function () {
        $('#locationModal').modal('show');
    })

    //Sign In Modal
    $('#signinButton').click(function () {
        $('#signinModal').modal('show');
    });

    //Reset  Sign In Modal
    $('#signinModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })

    //Cancel Order Modal
    $('cancel_order').click(function() {
        $('#cancelorderModal').modal('show');
    });

    //Mobile Number Verification Modal
    $('#MobileNumberVerificationButton').click(function () {
        $('#MobileNumberVerificationModal').modal('show');
    })

    //Reset Mobile Number Verification Modal
    $('#MobileNumberVerificationModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })

    //E-Mail Id Verification Modal
    $('#EMailidVerificationButton').click(function () {
        $('#EMailidVerificationModal').modal('show');
    })

    //Reset E-Mail Id Verification Modal
    $('#EMailidVerificationModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })

    //Popover
    $('[data-bs-toggle="popover"]').popover();

    //Popover dismis
    $('.popover-dismiss').popover({
        trigger: 'focus'
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

var map = new google.maps.Map(document.getElementById("googleMap1"), mapOptions);

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

var input3 = document.getElementById("address");
var autocomplete3 = new google.maps.places.Autocomplete(input3, options);

// var input4 = document.getElementById("setaddress");
// var autocomplete3 = new google.maps.places.Autocomplete(input4, options);

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
    var firstname = JSON.parse(document.getElementById('firstname').textContent);
    var lastname = JSON.parse(document.getElementById('lastname').textContent);
    var email = JSON.parse(document.getElementById('email').textContent);
    var user_id = JSON.parse(document.getElementById('user_id').textContent)
    var username = firstname + ' ' + lastname
    var amount = payment.amount;
    var currency = payment.currency;
    var order_id = payment.id;
    var options = {
        "key": razorpay_api_key,
        "amount": amount,
        "currency": currency,
        "name": "WeDeliver",
        "description": "Fast and Secure",
        "image": "/static/media/razorpaylogo.png",
        "order_id": order_id,
        "callback_url":"success/"+user_id,
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
            "name": username,
            "email": email,
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

function full_name() {
    var firstname = JSON.parse(document.getElementById('firstname').textContent);
    var lastname = JSON.parse(document.getElementById('lastname').textContent);
    var fullname = firstname + ' ' + lastname
    var info = {'fullname' : fullname}
    $.ajax({
        url: "map",
        type: "GET",
        data: info,
    });
}

function phoneotp() {
    $.ajax({
        url: "otp",
        type: "GET",
    });
}

function emailotp(user_id) {
    $.ajax({
        url: "emailotp/" + user_id,
        type: "GET",
    });
}

//Phone No. OTP Box
function getMobileOtpBoxElement(index) {
    return document.getElementById('MobileOtpBox' + index);
  }
  function onMobileKeyUpEvent(index, event) {
    const eventCode = event.which || event.keyCode;
    if (getMobileOtpBoxElement(index).value.length === 1) {
      if (index !== 4) {
        getMobileOtpBoxElement(index+ 1).focus();
      } else {
        getMobileOtpBoxElement(index).blur();
      }
    }
    if (eventCode === 8 && index !== 1) {
      getMobileOtpBoxElement(index - 1).focus();
    }
  }
  function onMobileFocusEvent(index) {
    for (item = 1; item < index; item++) {
      const currentElement = getMobileOtpBoxElement(item);
      if (!currentElement.value) {
          currentElement.focus();
          break;
      }
    }
  }

//Email OTP Box
function getEmailOtpBoxElement(index) {
    return document.getElementById('EmailOtpBox' + index);
  }
  function onEmailKeyUpEvent(index, event) {
    const eventCode = event.which || event.keyCode;
    if (getEmailOtpBoxElement(index).value.length === 1) {
      if (index !== 4) {
        getEmailOtpBoxElement(index+ 1).focus();
      } else {
        getEmailOtpBoxElement(index).blur();
      }
    }
    if (eventCode === 8 && index !== 1) {
      getEmailOtpBoxElement(index - 1).focus();
    }
  }
  function onEmailFocusEvent(index) {
    for (item = 1; item < index; item++) {
      const currentElement = getEmailOtpBoxElement(item);
      if (!currentElement.value) {
          currentElement.focus();
          break;
      }
    }
  }

//User Phone No. OTP
function user_phone_no_otp() {
    var box1 = $('#MobileOtpBox1').val();
    var box2 = $('#MobileOtpBox2').val();
    var box3 = $('#MobileOtpBox3').val();
    var box4 = $('#MobileOtpBox4').val();
    user_otp = box1 + box2 + box3 + box4
    info = {'user_otp' : user_otp}
    $.ajax({
        url: "phone_no_otp_verification",
        type: "GET",
        data: info,
    });
}

//User Email OTP
function user_email_otp(user_id) {
    var box1 = $('#EmailOtpBox1').val();
    var box2 = $('#EmailOtpBox2').val();
    var box3 = $('#EmailOtpBox3').val();
    var box4 = $('#EmailOtpBox4').val();
    user_otp = box1 + box2 + box3 + box4
    info = {'user_otp' : user_otp}
    $.ajax({
        url: "email_otp_verification/" + user_id,
        type: "GET",
        data: info,
    });
}

async function otp_timer(otp_id) {
    var seconds = 5;
    await new Promise(r => setTimeout(() => r(), 1000));
    function tick() {
        var timer1 = document.getElementById("timer1");
        var timer2 = document.getElementById("timer2");
        var resend_otp = document.getElementsByClassName("resend_otp");
        var end_otp = document.getElementsByClassName("end_otp");
        seconds--;
        if(otp_id == 0) {
            timer1.innerHTML =  (seconds < 10 ? "0" : "") + String(seconds);
        }
        if(otp_id == 1) {
            timer2.innerHTML =  (seconds < 10 ? "0" : "") + String(seconds); 
            console.log(timer2.textContent)
        }
        if( seconds > 0 ) {
            setTimeout(tick, 1000);
         } else {
            resend_otp[otp_id].innerHTML = "<button type='button' class='btn btn-primary'>Resend OTP</button>";
            end_otp[otp_id].innerHTML =  "";
        }
    }
    tick();
}

async function end_otp(otp_id) {
    var seconds =10;
    await new Promise(r => setTimeout(() => r(), 1000));
    function tick() {
        var counter = document.getElementsByClassName("end_otp");
        var expire = document.getElementsByClassName("expire_otp");
        var box = document.getElementsByClassName("form-control-otp");
        seconds--;
        if( seconds > 0 ) {
            setTimeout(tick, 1000);
        } else {
                counter[otp_id].innerHTML = "Your otp has been expire.<br>Please click <b>Resend OTP</b> to get new otp.";
                counter[otp_id].style.color = "red";
                expire[otp_id].innerHTML = "";
                if(otp_id == 0){
                    for (var i=0; i < 4; i++){
                        var boxes = box[i];
                        boxes.style.borderColor = "red";
                    }
                }
                if(otp_id ==1){
                    for (var i=4; i < 8; i++){
                        var boxes = box[i];
                        boxes.style.borderColor = "red";
                    }
                }
        }
    }
    tick();
}