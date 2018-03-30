// main var
var map;
var markers = [];
var qtWidget;

new QWebChannel(qt.webChannelTransport, function (channel) {
    qtWidget = channel.objects.qtWidget;
});

// main init function
function initialize() {
    var myOptions = {
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var div = document.getElementById("map_canvas");
    map = new google.maps.Map(div, myOptions);

    google.maps.event.addListener(map, 'dragend', function () {
        center = gmap_getCenter();
        qtWidget.mapMoved(center.lat(), center.lng());
    });
    google.maps.event.addListener(map, 'click', function (ev) {
        qtWidget.mapClicked(ev.latLng.lat(), ev.latLng.lng());
    });
    google.maps.event.addListener(map, 'rightclick', function (ev) {
        qtWidget.mapRightClicked(ev.latLng.lat(), ev.latLng.lng());
    });
    google.maps.event.addListener(map, 'dblclick', function (ev) {
        qtWidget.mapDoubleClicked(ev.latLng.lat(), ev.latLng.lng());
    });
}

// custom functions
function gmap_setCenter(lat, lng) {
    map.setCenter(new google.maps.LatLng(lat, lng));
}

function gmap_getCenter() {
    return map.getCenter();
}

function gmap_setZoom(zoom) {
    map.setZoom(zoom);
}

function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function change_color_based_on_cluster(number_cluster) {
    var r = 255;
    var g = 255;
    var b = 255;
    if(number_cluster % 3 == 0) {
        r = 0;
        g = 255/50 * number_cluster;
    } else if(number_cluster % 3 == 1) {
        g = 0;
        b = 255/50 * number_cluster;
    } else if(number_cluster % 3 == 2) {
        b = 0;
        r = 255/50 * number_cluster;
    }
    return rgbToHex(r, g, b);
}

function get_center_coords(listCoords) {
    var total_X = 0;
    var total_Y = 0;
    var result = [];
    for(var i = 0; i < listCoords.length; i++) {
        total_X += listCoords[i][0];
        total_Y += listCoords[i][1];
    }
    alert(total_X);
    result['latitude'] = total_X / listCoords.length;
    result['longitude'] = total_Y / listCoords.length;
    alert("latitude: " + result['latitude'] +"|longitude: "+result['longitude']);
    return result;
}

function draw_circle(center, max_r){
    alert("max R:" + max_r);
    var centerPoint = new google.maps.LatLng(center['latitude'], center['longitude']);
    var cityCircle = new google.maps.Circle({
            //strokeColor: '#FF0000',
            strokeOpacity: 0.2,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: centerPoint,
            radius: Math.pow(2,max_r) * 3141.592654
    });
}

function get_max_r(center, listCoords) {
    var max_r = 0;
    for(var i = 0; i < listCoords.length; i++) {
        var curr_r = Math.sqrt(Math.pow(2, center['latitude']-listCoords[i][0]) + Math.pow(2, center['longitude']-listCoords[i][1]));
        if(curr_r > max_r) {
            max_r = curr_r;
        }
    }
    return max_r;
}

function gmap_addMarker(key, latitude, longitude, parameters) {
    if (key in markers) {
        gmap_deleteMarker(key);
    }

    var coords = new google.maps.LatLng(latitude, longitude);
    var icon  = marker_sympol(2);
    var label = [];
    label['text'] = key;
    label['color'] = 'white';
    parameters['map'] = map;
    parameters['position'] = coords;
    parameters['label'] = label;
    parameters['icon'] = icon;
    //parameters['icon'] = 'yellowMarker.png';
    var marker = new google.maps.Marker(parameters);
    google.maps.event.addListener(marker, 'dragend', function () {
        qtWidget.markerMoved(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'click', function () {
        qtWidget.markerClicked(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'dblclick', function () {
        qtWidget.markerDoubleClicked(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'rightclick', function () {
        qtWidget.markerRightClicked(key, marker.position.lat(), marker.position.lng())
    });

    markers[key] = marker;
    return key;
}

function marker_sympol(number_cluster) {
    var color = change_color_based_on_cluster(number_cluster);
    return {
        path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z',
        fillColor: color,
        primaryColor: 'white',
        fillOpacity: 1,
        strokeColor: '#000',
        strokeWeight: 2,
        scale: 1,
        labelOrigin: new google.maps.Point(0,-25)
    };
}

function calculateAndDisplayRoute(oLat, oLong, dLat, dLong) {
    var orgi = new google.maps.LatLng(oLat, oLong);
    var di = new google.maps.LatLng(dLat, dLong);
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    directionsDisplay.setMap(map);
    directionsDisplay.setOptions({suppressMarkers: true});
    directionsService.route({
        origin: orgi,
        destination: di,
        travelMode: 'DRIVING'
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function displayAllRout(listCoords, bestTour) {
    var directionsService = new google.maps.DirectionsService;
    for(var i = 0; i < listCoords.length-1; i++) {
        var currentCoord = new google.maps.LatLng(listCoords[bestTour[i]][0], listCoords[bestTour[i]][1]);
        var nextCoord = new google.maps.LatLng(listCoords[bestTour[i+1]][0], listCoords[bestTour[i+1]][1]);
        directionsService.route({
            origin: currentCoord,
            destination: nextCoord,
            travelMode: 'DRIVING'
        }, function (response, status) {
            if (status === 'OK') {
                var directionsDisplay = new google.maps.DirectionsRenderer;
                var color = change_color_based_on_cluster(i);
                directionsDisplay.setMap(map);
                directionsDisplay.setOptions({  suppressMarkers: true,
                                                polylineOptions: {
                                                        strokeColor: color,
                                                        strokeOpacity: 0.5,
                                                        strokeWeight: 10
                                                }});
                directionsDisplay.setDirections(response);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
        await sleep(1000);
    }
    //var center = get_center_coords(listCoords);
    //var max_r = get_max_r(center, listCoords);
    //draw_circle(center, max_r);
}

function displayAllRouteVer2(listCoords, bestTour) {
    var directionsService = new google.maps.DirectionsService;
    var waypts = [];
    for(var i = 1; i < listCoords.length; i++) {
        if(i%10==9) {
            var start = new google.maps.LatLng(listCoords[bestTour[i-9]][0], listCoords[bestTour[i-9]][1]);
            var end = new google.maps.LatLng(listCoords[bestTour[i]][0], listCoords[bestTour[i]][1]);
            directionsService.route({
                origin: start,
                destination: end,
                waypoints: waypts,
                optimizeWaypoints: true,
                travelMode: 'DRIVING'
            }, function(response, status) {
                if (status === 'OK') {
                    var directionsDisplay = new google.maps.DirectionsRenderer;
                    directionsDisplay.setMap(map);
                    directionsDisplay.setOptions({suppressMarkers: true});
                    directionsDisplay.setDirections(response);
                } else {
                    window.alert('Directions request failed due to ' + status);
                }
            });
            waypts = [];
        } else if(i==listCoords.length-1) {
            var sub = i%10;
            var start = new google.maps.LatLng(listCoords[bestTour[i-sub]][0], listCoords[i-sub][1]);
            var end = new google.maps.LatLng(listCoords[bestTour[i]][0], listCoords[i][1]);
            directionsService.route({
                origin: start,
                destination: end,
                waypoints: waypts,
                optimizeWaypoints: false,
                travelMode: 'DRIVING'
            }, function(response, status) {
                if (status === 'OK') {
                    var directionsDisplay = new google.maps.DirectionsRenderer;
                    directionsDisplay.setMap(map);
                    directionsDisplay.setOptions({suppressMarkers: true});
                    directionsDisplay.setDirections(response);
                } else {
                    window.alert('Directions request failed due to ' + status);
                }
            });
        } else if(i%10!=0) {
            var cur = new google.maps.LatLng(listCoords[bestTour[i]][0], listCoords[bestTour[i]][1]);
            waypts.push({
              location: cur,
              stopover: true
            });
            alert(listCoords[bestTour[i]][0]);
        }
    }
}

function gmap_moveMarker(key, latitude, longitude) {
    var coords = new google.maps.LatLng(latitude, longitude);
    markers[key].setPosition(coords);
}

function gmap_deleteMarker(key) {
    markers[key].setMap(null);
    delete markers[key]
}

function gmap_changeMarker(key, extras) {
    if (!(key in markers)) {
        return
    }
    markers[key].setOptions(extras);
}

