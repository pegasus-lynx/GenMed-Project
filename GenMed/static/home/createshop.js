// Geolocation to get the latitude and longitude

var lat = document.getElementById("lat");
var lon = document.getElementById("lon");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(storePosition);
    } else { 
        showErr()
    }
}

function storePosition(position) {
    $('#lat').setAttribute("value", position.coords.latitude);
    $('#lon').setAttribute("value", position.coords.longitude);
}

function showErr() {
    var v=$('#loc_err')
    v.attr('visibility','visible')
}