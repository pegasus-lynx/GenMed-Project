// Geolocation to get the latitude and longitude

var lat = document.getElementById("lat");
var lon = document.getElementById("lon");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(storePosition, showError);
    } else { 
        $('#loc_err').attr('visibility','visible')
    }
}

function storePosition(position) {
    $('#lat').attr("value", position.coords.latitude);
    $('#lon').attr("value", position.coords.longitude);
}

function showError(err) {
    console.log(err) 
}