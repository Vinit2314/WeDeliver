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
// var myLatLng = { lat: 19.09761241932646, lng: 72.88250110269311 };
// var mapOptions = {
//     center: myLatLng,
//     zoom: 7,
//     mapTypeId: google.maps.MapTypeId.ROADMAP
// };

// //create map
// var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);


// //create a DirectionsRenderer object which we will use to display the route
// var directionsDisplay = new google.maps.DirectionsRenderer();

// //bind the DirectionsRenderer to the map
// directionsDisplay.setMap(map);



// //define calcRoute function
// function calcRoute() {
//     //create request
//     var request = {
//         origin: document.getElementById("from").value,
//         destination: document.getElementById("to").value,
//         travelMode: google.maps.TravelMode.DRIVING, //WALKING, BYCYCLING, TRANSIT
//         unitSystem: google.maps.UnitSystem.IMPERIAL
//     };

//     //create a DirectionsService object to use the route method and get a result for our request
//     var directionsService = new google.maps.DirectionsService();

//     //pass the request to the route method
//     directionsService.route(request, function (result, status) {
//         if (status == google.maps.DirectionsStatus.OK) {

//             //Get distance and time
//             const output = document.querySelector('#output');
//             output.innerHTML = "<div class='alert-info'>From: " + document.getElementById("from").value + ".<br />To: " + document.getElementById("to").value + ".<br /> Driving distance <i class='fas fa-road'></i> : " + result.routes[0].legs[0].distance.text + ".<br />Duration <i class='fas fa-hourglass-start'></i> : " + result.routes[0].legs[0].duration.text + ".</div>";

//             //display route
//             directionsDisplay.setDirections(result);
//         } else {
//             //delete route from map
//             directionsDisplay.setDirections({ routes: [] });
//             //center map in London
//             map.setCenter(myLatLng);

//             //show error message
//             output.innerHTML = "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve driving distance.</div>";
//         }
//     });

// }

// //create autocomplete objects for all inputs
// var options = {
//     types: ['(cities)']
// }

// var input1 = document.getElementById("from");
// var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

// var input2 = document.getElementById("to");
// var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

//  tomtom map
tomtomApiKey = JSON.parse(document.getElementById('tomtom_map_key').textContent);
tt.setProductInfo('WeDeliver', '1.0');

var map = tt.map({
    key: tomtomApiKey,
    container: 'map',
    center: [72.9992, 19.1254],
    zoom: 20,
});

var Searchoptions = {
    idleTimePress: 100,

    minNumberOfCharacters: 1,

    searchOptions: {
        key: tomtomApiKey,
        language: 'en-US'
    },

    autocompleteOptions: {
        key: tomtomApiKey,
        language: 'en-US',
        limit: 10,
    },

    labels: {
        placeholder: 'e.g. Mumbai...'
    },
};

var ttSearchBox = new tt.plugins.SearchBox(tt.services, Searchoptions)

var updateSearchOptions = function () {
    let options = ttSearchBox.getOptions()
    options.searchOptions.boundingBox = map.getBounds()
    ttSearchBox.updateOptions(options)
    console.log(options)
}

map.on('dragend', function () {
    updateSearchOptions()
});

map.on('load', function () {
    document.querySelector('.searchBox').appendChild(ttSearchBox.getSearchBoxHTML());
    updateSearchOptions()
});

ttSearchBox.on('tomtom.searchbox.resultsfound', function (data) {
    console.log(data);
});

ttSearchBox.query();

//var marker = new tt.Marker().setLngLat([-122.492544, 37.768454]).addTo(map);
ttSearchBox.on('tomtom.searchbox.resultsfound', handleResultsFound);
ttSearchBox.on('tomtom.searchbox.resultselected', handleResultSelection);
ttSearchBox.on('tomtom.searchbox.resultfocused', handleResultSelection);
ttSearchBox.on('tomtom.searchbox.resultscleared', handleResultClearing);

function handleResultsFound(event) {
    var results = event.data.results.fuzzySearch.results;

    if (results.length === 0) {
        searchMarkersManager.clear();
    }
    searchMarkersManager.draw(results);
    fitToViewport(results);
}

function handleResultSelection(event) {
    var result = event.data.result;
    if (result.type === 'category' || result.type === 'brand') {
        return;
    }
    searchMarkersManager.draw([result]);
    fitToViewport(result);
}

function fitToViewport(markerData) {
    if (!markerData || markerData instanceof Array && !markerData.length) {
        return;
    }
    var bounds = new tt.LngLatBounds();
    if (markerData instanceof Array) {
        markerData.forEach(function (marker) {
            bounds.extend(getBounds(marker));
        });
    } else {
        bounds.extend(getBounds(markerData));
    }
    map.fitBounds(bounds, { padding: 100, linear: true });
}

function getBounds(data) {
    var btmRight;
    var topLeft;
    if (data.viewport) {
        btmRight = [data.viewport.btmRightPoint.lng, data.viewport.btmRightPoint.lat];
        topLeft = [data.viewport.topLeftPoint.lng, data.viewport.topLeftPoint.lat];
    }
    return [btmRight, topLeft];
}

function handleResultClearing() {
    searchMarkersManager.clear();
}

function handleResultsFound(event) {
    var results = event.data.results.fuzzySearch.results;

    if (results.length === 0) {
        searchMarkersManager.clear();
    }
    searchMarkersManager.draw(results);
    fitToViewport(results);
}

function handleResultSelection(event) {
    var result = event.data.result;
    if (result.type === 'category' || result.type === 'brand') {
        return;
    }
    searchMarkersManager.draw([result]);
    fitToViewport(result);
}

function fitToViewport(markerData) {
    if (!markerData || markerData instanceof Array && !markerData.length) {
        return;
    }
    var bounds = new tt.LngLatBounds();
    if (markerData instanceof Array) {
        markerData.forEach(function (marker) {
            bounds.extend(getBounds(marker));
        });
    } else {
        bounds.extend(getBounds(markerData));
    }
    map.fitBounds(bounds, { padding: 100, linear: true });
}

function getBounds(data) {
    var btmRight;
    var topLeft;
    if (data.viewport) {
        btmRight = [data.viewport.btmRightPoint.lng, data.viewport.btmRightPoint.lat];
        topLeft = [data.viewport.topLeftPoint.lng, data.viewport.topLeftPoint.lat];
    }
    return [btmRight, topLeft];
}

function handleResultClearing() {
    searchMarkersManager.clear();
}


function SearchMarkersManager(map, options) {
    this.map = map;
    this._options = options || {};
    this._poiList = undefined;
    this.markers = {};
}

SearchMarkersManager.prototype.draw = function (poiList) {
    this._poiList = poiList;
    this.clear();
    this._poiList.forEach(function (poi) {
        var markerId = poi.id;
        var poiOpts = {
            name: poi.poi ? poi.poi.name : undefined,
            address: poi.address ? poi.address.freeformAddress : '',
            distance: poi.dist,
            classification: poi.poi ? poi.poi.classifications[0].code : undefined,
            position: poi.position,
            entryPoints: poi.entryPoints
        };
        var marker = new SearchMarker(poiOpts, this._options);
        marker.addTo(this.map);
        this.markers[markerId] = marker;
    }, this);
};

SearchMarkersManager.prototype.clear = function () {
    for (var markerId in this.markers) {
        var marker = this.markers[markerId];
        marker.remove();
    }
    this.markers = {};
    this._lastClickedMarker = null;
};

function SearchMarker(poiData, options) {
    this.poiData = poiData;
    this.options = options || {};
    this.marker = new tt.Marker({
        element: this.createMarker(),
        anchor: 'bottom'
    });
    var lon = this.poiData.position.lng || this.poiData.position.lon;
    this.marker.setLngLat([
        lon,
        this.poiData.position.lat
    ]);
}

SearchMarker.prototype.addTo = function (map) {
    this.marker.addTo(map);
    this._map = map;
    return this;
};

SearchMarker.prototype.createMarker = function () {
    var elem = document.createElement('div');
    elem.className = 'tt-icon-marker-black tt-search-marker';
    if (this.options.markerClassName) {
        elem.className += ' ' + this.options.markerClassName;
    }
    var innerElem = document.createElement('div');
    innerElem.setAttribute('style', 'background: white; width: 10px; height: 10px; border-radius: 50%; border: 3px solid black;');

    elem.appendChild(innerElem);
    return elem;
};

SearchMarker.prototype.remove = function () {
    this.marker.remove();
    this._map = null;
};

map.addControl(new tt.FullscreenControl());
map.addControl(new tt.NavigationControl());

//Price calculation and map form info
function price_map_info() {
    var kg = $('#kg_value').val();
    var price_per_kg = 5;
    var distance = 10;
    var total_price = Math.round(kg * price_per_kg * distance);
    var price = 'Amt : ' + total_price + ' ₹';
    document.getElementById('price').innerHTML = price;
    info = {
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
        success: function (data) {
        },
        failure: function (data) {
            alert('Got an error!!');
        }
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

function backpage(){
    history.back()
}
