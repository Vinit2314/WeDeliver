$(document).ready(function () {
    //loader
    $('body').append('<div id="loadingDiv"><div class="TruckLoader d-none d-sm-block"><i class="mt-2" style="display:flex; justify-content:center;">WeDeliver</i><div class="TruckLoader-cab"><div class="tube"><div class="TruckLoader-smoke"></div></div></div><hr /></div><div class="loader d-block d-sm-none"></div>');
    $(window).on('load', function(){
    setTimeout(removeLoader, 2000); //wait for page load PLUS two seconds.
    });
    function removeLoader(){
    $( "#loadingDiv" ).fadeOut(500, function() {
    // fadeOut complete. Remove the loading div
    $( "#loadingDiv" ).remove(); //makes page more lightweight
    });  
    }

    if(sessionStorage.getItem('type') == 'document') {
        $("#kg").remove();
        $("#kg1").remove();
        $("#kg2").remove();
    }
    else if(sessionStorage.getItem('type') == 'food' || sessionStorage.getItem('type') == 'package') {
        $("#pages_no").remove();
        $("#pages_no1").remove();
        $("#pages_no2").remove();
    }
    
    //Login Modal
    $('#loginButton').click(function () {
        $('#loginModal').modal('show');
    })

    //Location Modal
    $('#locationButton').click(function () {
        $('#locationModal').modal('show');
    })

    //Sign In Modal
    $('#signinButton').click(function () {
        $('#signinModal').modal('show');
    });

    //Cancel Order Modal
    $('#cancelorderButton').click(function() {
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

    //Login Required Modal
    $('#loginrequiredButton').click(function () {
        $('#loginrequiredModal').modal('show');
    })

    //OTP Verification Required Modal
    $('#otprequiredButton').click(function () {
        $('#otprequiredModal').modal('show');
    })
});

window.onload = () => {
    globalThis.resend = 0;

    const myInput = document.querySelectorAll("#password, #sign_password, #sign_confirm_password, #id_new_password1,#id_new_password2");
    myInput.forEach(element => {
        element.onpaste = e => e.preventDefault();
    });

    var login_flag = JSON.parse(document.getElementById('login_flag').textContent);
    if(login_flag == "F") {
        alert('Invalid Credentials!!');
    }

    var signup_flag = JSON.parse(document.getElementById('signup_flag').textContent);
    if(signup_flag == "PF") {
        alert('Password does not match!!');
    }else if(signup_flag == "EF") {
        alert('Email already registered!!');
    }else if(signup_flag == "UF") {
        alert('Username already Taken!!');
    }else if(signup_flag == "EFUF") {
        alert('Email already registered and Username already Taken!!');
    }

    emailid_and_phoneno()

    phone_emai_verify_button()
}

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

var input4 = document.getElementById("set_location");
var autocomplete3 = new google.maps.places.Autocomplete(input4, options);

//Price calculation and map form info
function price_map_info() {
    if(sessionStorage.getItem('type') == 'document') {
        var quantity = $('#pages_value').val();
    }
    else if(sessionStorage.getItem('type') == 'food' || sessionStorage.getItem('type') == 'package') {
        var quantity = $('#kg_value').val();
    }
    var price = sessionStorage.getItem('price');
    var distance = 10;
    var total_price = Math.round(quantity * price * distance);
    var price = 'Amt : ' + total_price + ' &#x20B9;';
    document.getElementById('price').innerHTML = price;
    var info = {
        'name1' : $('#name1').val(),
        'address1' : $('#address1').val(),
        'number1' : $('#number1').val(),
        'name2' : $('#name2').val(),
        'address2' : $('#address2').val(),
        'number2' : $('#number2').val(),
        'quantity' : quantity,
        'amount': total_price,
        'type' : sessionStorage.getItem('type'),
        'csrfmiddlewaretoken' : $('input[name = csrfmiddlewaretoken]').val(),
    };
    if($('#name1').val() != '' && $('#address1').val() != '' && $('#number1').val() != '' && $('#name2').val() != '' && $('#address2').val() != '' && $('#number2').val() != '' && quantity != '') {
        sessionStorage.setItem('name', $('#name1').val());
        sessionStorage.setItem('number', $('#number1').val());
        $.ajax({
            url: "map",
            type: "GET",
            data: info,
        });
    }
}

// Razorpay
function razorpay() {
    var payment = JSON.parse(document.getElementById('payment').textContent);
    var razorpay_api_key = JSON.parse(document.getElementById('razorpay_api_key').textContent);
    var email = JSON.parse(document.getElementById('email').textContent);
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
            "name": sessionStorage.getItem('name'),
            "email": email,
            "contact": sessionStorage.getItem('number'),
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

function emailid_and_phoneno() {
    //Phone No
    globalThis.phone_no = $("#phone_no").val();

    //Email-Id
    globalThis.email_id = $("#email").val();
}
function phone_emai_verify_button() {
    if( $("#phone_no").val() == "" ) {
        $("#phone_number_otp").hide();
    } else {
        $("#phone_number_otp").show();
    }
    if( $("#email").val() == "" ) {
        $("#email_id_otp").hide();
    } else {
        $("#email_id_otp").show();
    }
}

async function phoneotp() {
    info = {
        'phone_no' : phone_no,
        }
    $.ajax({
        url: "phoneotp",
        type: "GET",
        data: info,
    });
    await new Promise(r => setTimeout(() => r(), 1000));
    $( "#phone_no_otp_div" ).load(window.location.href + " #phone_no_otp_div" )
    await new Promise(r => setTimeout(() => r(), 1000));
}

async function emailotp() {
    info = {
            'email_id' : email_id,
            }
    $.ajax({
        url: "emailotp",
        type: "GET",
        data: info,
    });
    await new Promise(r => setTimeout(() => r(), 1000));
    $( "#email_otp_div" ).load(window.location.href + " #email_otp_div" )
    await new Promise(r => setTimeout(() => r(), 1000));
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
async function user_phone_no_otp() {
    var box1 = $('#MobileOtpBox1').val();
    var box2 = $('#MobileOtpBox2').val();
    var box3 = $('#MobileOtpBox3').val();
    var box4 = $('#MobileOtpBox4').val();
    user_otp = box1 + box2 + box3 + box4
    var phone_no_otp = parseInt(document.getElementById('phone_no_otp_div').textContent);
    if (user_otp == phone_no_otp) {
        info = {
            'user_otp' : user_otp,
            'csrfmiddlewaretoken' : $('input[name = csrfmiddlewaretoken]').val(),
            'phone_no_verify_flag' : 'V',
            'phone_no' : phone_no,
                }
        $.ajax({
            url: "phone_no_otp_verification",
            type: "GET",
            data: info,
        });
        await new Promise(r => setTimeout(() => r(), 1000));
        document.location.reload(true);
    }else {
        resend = 0;
        var box = document.getElementsByClassName("form-control-otp");
        var error = document.getElementsByClassName("otp_error");
        error[0].innerHTML = "OTP does not Match. Plese try again.<br>";
        var email_error = error[0];
        email_error.style.color = "red";
        for (var i=0; i < 4; i++){
            var boxes = box[i];
            boxes.style.borderColor = "red";
        }
    }
}

//User Email OTP
async function user_email_otp() {
    var box1 = $('#EmailOtpBox1').val();
    var box2 = $('#EmailOtpBox2').val();
    var box3 = $('#EmailOtpBox3').val();
    var box4 = $('#EmailOtpBox4').val();
    user_otp = box1 + box2 + box3 + box4
    var email_otp = parseInt(document.getElementById('email_otp_div').textContent);
    if (user_otp == email_otp) {
        info = {
            'user_otp' : user_otp,
            'csrfmiddlewaretoken' : $('input[name = csrfmiddlewaretoken]').val(),
            'email_verify_flag' : 'V',
            'email_id' : email_id,
                }
        $.ajax({
            url: "email_otp_verification",
            type: "GET",
            data: info,
        });
        await new Promise(r => setTimeout(() => r(), 1000));    
        document.location.reload(true);
    }else {
        resend = 0;
        var box = document.getElementsByClassName("form-control-otp");
        var error = document.getElementsByClassName("otp_error");
        error[1].innerHTML = "OTP does not Match. Plese try again.<br>";
        var email_error = error[1];
        email_error.style.color = "red";
        for (var i=4; i < 8; i++){
            var boxes = box[i];
            boxes.style.borderColor = "red";
        }
    }
}

async function resendotp(otp_id) {
    resend = 1;
    var seconds = 31;
    var endseconds = 61;
    function tick() {
    var resesndchangehead = document.getElementsByClassName("resendchangehead");
    var retimer1 = document.getElementById("retimer1");
    var retimer2 = document.getElementById("retimer2");
    var resend_otp = document.getElementsByClassName("resend_otp");
    var expire = document.getElementsByClassName("expire_otp");
    var error = document.getElementsByClassName("otp_error");
    resend_otp[otp_id].innerHTML = "";
    seconds--;
    if(otp_id == 0) {
        resesndchangehead[0].innerHTML = "OTP has been <b>Resend</b> to your Mobile Number";
        if(resend == 1){
            error[0].innerHTML = "";
        }
    }
    if(otp_id == 1) {
        resesndchangehead[1].innerHTML = "OTP has been <b>Resend</b> to your E-Mail ID";
        if(resend == 1){
            error[1].innerHTML = "";
        }
    }
    if(otp_id == 0) {
        retimer1.innerHTML =  "Resend OTP in " + (seconds < 10 ? "0" : "") + String(seconds);
        retimer1.style.color = "black";
    }
    if(otp_id == 1) {
        retimer2.innerHTML =  "Resend OTP in " + (seconds < 10 ? "0" : "") + String(seconds);
        retimer2.style.color = "black";
    }
    if(otp_id == 0) {
        expire[otp_id].innerHTML = "<a onclick='user_phone_no_otp()' class='btn btn-success'>Submit</a>"
    }
    if(otp_id ==1) {
        expire[otp_id].innerHTML = "<a onclick='user_email_otp()' class='btn btn-success'>Submit</a>"
    }
    if( seconds > 0) {
        setTimeout(tick, 1000);
    } else {
        resend_otp[otp_id].innerHTML = "<button type='button' onclick='resendotp(otp_id)' class='btn btn-primary'>Resend OTP</button>";
        if(otp_id == 0) {
        retimer1.innerHTML =  "";
            }
        if(otp_id == 1) {
            retimer2.innerHTML =  "";
            }
        }
    }
    var box = document.getElementsByClassName("form-control-otp");
    if(otp_id == 0){
        for (var i=0; i < 4; i++){
            var boxes = box[i];
            boxes.style.borderColor = "#F3F6F9";
        }
    }
    if(otp_id == 1){
        for (var i=4; i < 8; i++){
            var boxes = box[i];
            boxes.style.borderColor = "#F3F6F9";
        }
    }
    function end_otp() {
        endseconds--;
        if(endseconds > 0) {
            setTimeout(end_otp, 1000);
        }else{
            var counter = document.getElementsByClassName("end_otp");
            var expire = document.getElementsByClassName("expire_otp");
            counter[otp_id].innerHTML = "Your otp has been expire.<br>Please click <b>Resend OTP</b> to get new otp.";
            counter[otp_id].style.color = "red";
            expire[otp_id].innerHTML = "";
            if(otp_id == 0){
                for (var i=0; i < 4; i++){
                    var boxes = box[i];
                    boxes.style.borderColor = "red";
                }
            }
            if(otp_id == 1){
                for (var i=4; i < 8; i++){
                    var boxes = box[i];
                    boxes.style.borderColor = "red";
                }
            }
        }
    }
    tick();
    end_otp();
    if(otp_id == 0) {
        info = {
            'phone_no' : phone_no,
            }
        $.ajax({
            url: "resendphonenootp",
            type: "GET",
            data: info,
        });
    }
    if(otp_id == 1) {
        info = {
            'email_id' : email_id,
            }
        $.ajax({
            url: "resendemailotp",
            type: "GET",
            data: info,
        });
    }
    await new Promise(r => setTimeout(() => r(), 1000));
    if(otp_id == 0) {
        $( "#phone_no_otp_div" ).load(window.location.href + " #phone_no_otp_div" );
    }
    if(otp_id == 1) {
        $( "#email_otp_div" ).load(window.location.href + " #email_otp_div" );
    }
    await new Promise(r => setTimeout(() => r(), 1000));
}

function otp_timer(otp_id) {
    globalThis.otp_id= otp_id;
    var seconds = 31;
    var endseconds = 61;
    function tick() {
        var timer1 = document.getElementById("timer1");
        var timer2 = document.getElementById("timer2");
        var resend_otp = document.getElementsByClassName("resend_otp");
        seconds--;
        if(otp_id == 0) {
            timer1.innerHTML =  "Resend OTP in " + (seconds < 10 ? "0" : "") + String(seconds);
        }
        if(otp_id == 1) {
            timer2.innerHTML =  "Resend OTP in " + (seconds < 10 ? "0" : "") + String(seconds);
        }
        if( seconds > 0 ) {
            setTimeout(tick, 1000);
        } 
        else {
            resend_otp[otp_id].innerHTML = "<button type='button' onclick='resendotp(otp_id)' class='btn btn-primary'>Resend OTP</button>";
            if(otp_id == 0) {
                timer1.innerHTML =  "";
            }
            if(otp_id == 1) {
                timer2.innerHTML =  "";
            }        
        }
    }
    function end_otp() {
        var counter = document.getElementsByClassName("end_otp");
        var expire = document.getElementsByClassName("expire_otp");
        var box = document.getElementsByClassName("form-control-otp");
        endseconds--;
        if( endseconds > 0 ) {
            if(resend == 0){
                setTimeout(end_otp, 1000);
            }
            else{
                return resend;
            }
        } 
        else 
        {
            counter[otp_id].innerHTML = "Your otp has been expire.<br>Please click <b>Resend OTP</b> to get new otp.";
            counter[otp_id].style.color = "red";
            expire[otp_id].innerHTML = "";
            if(otp_id == 0){
                for (var i=0; i < 4; i++){
                    var boxes = box[i];
                    boxes.style.borderColor = "red";
                }
            }
            if(otp_id == 1){
                for (var i=4; i < 8; i++){
                    var boxes = box[i];
                    boxes.style.borderColor = "red";
                }
            }
        }
    }
    tick();
    end_otp();
}

function cancel_order() {
    $('.cancelmodal').modal('hide');
    $('body').append('<div class="cont"><div class="paper"></div><cancelbutton><div class="cancelloader"><div></div><div></div><div></div><div></div><div></div><div></div></div>Canceling</cancelbutton><div class="g-cont"><div class="garbage"></div><div class="garbage"></div><div class="garbage"></div><div class="garbage"></div><div class="garbage"></div><div class="garbage"></div><div class="garbage"></div></div></div>');
    setTimeout(removeLoader, 2000);
    function removeLoader(){
    $( ".cont" ).fadeOut(500, function() {
    // fadeOut complete. Remove the loading div
    $( ".cont" ).remove(); //makes page more lightweight
    });  
    }
}

function card(id) {
    if(id == "document") {
        var price = document.getElementById("document_price").textContent;
        sessionStorage.setItem("type", "document");
    }
    else if(id == "food") {
        var price = document.getElementById("food_price").textContent;
        sessionStorage.setItem("type", "food");
    }
    else if(id == "package") {
        var price = document.getElementById("package_price").textContent;
        sessionStorage.setItem("type", "package");
    }
    sessionStorage.setItem("price", price);
}

function logout() {
    sessionStorage.clear()
}

function check() {
    if(document.getElementById("rememberme").checked == false){
      document.getElementById("rememberme").checked = true;
      }else if(document.getElementById("rememberme").checked == true){
      document.getElementById("rememberme").checked = false;
      }
}

function view_password(view_password_id) {
    if(view_password_id == 1) {
        var ViewPassword = document.querySelector('#view_password1');
        var password = document.querySelector('#password');
        view();
    }else if(view_password_id == 2) {
        var ViewPassword = document.querySelector('#view_password2')
        var password = document.querySelector('#sign_password');
        view();
    }else if(view_password_id == 3) {
        var ViewPassword = document.querySelector('#view_password3')
        var password = document.querySelector('#sign_confirm_password');
        view();
    }
    else if(view_password_id == 4) {
        var ViewPassword = document.querySelector('#view_password4')
        var password = document.querySelector('#id_new_password1');
        view();
    }
    else if(view_password_id == 5) {
        var ViewPassword = document.querySelector('#view_password5')
        var password = document.querySelector('#id_new_password2');
        view();
    }

    function view() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            if(ViewPassword.classList[1] == 'fad') {
                ViewPassword.classList.remove('fad', 'fa-eye-slash');
                ViewPassword.classList.add('fas', 'fa-eye')
            }else if(ViewPassword.classList[1] == 'fas') {
                ViewPassword.classList.remove('fas', 'fa-eye');
                ViewPassword.classList.add('fad', 'fa-eye-slash')
            }
        };
}