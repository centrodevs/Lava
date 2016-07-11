$(document).ready(function() {

    var listView = true;

    var results_json = JSON.parse(COMPANY_RESULTS.replace(/&#39;/g, "\""));
    var success = results_json.length > 0;
    var banner;

    if (success) {
        banner = $("#result-banner");
        $("#result-banner").show();
    } else {
        banner = $("#result-banner-fail");
        $("#result-banner-fail").show();
    }

    /* Set a timeout for the result banner's display */
    setTimeout(function() {
        banner.slideUp();
        $("#helpBtn").fadeIn();
    }, 700);

    var mapDisplayStatus = {};

    function initMap() {
        var map;
        var bounds = new google.maps.LatLngBounds();
        var mapOptions = {
            mapTypeId: 'roadmap'
        };
        var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
        // var uluru = {lat: 36.398, lng: -122.03};
        var map = new google.maps.Map(document.getElementById('map'), mapOptions);

        var markers = results_json;
        var user_answers = JSON.parse(USER_ANSWERS.replace(/&#39;/g, "\""));
        var labelClasses = ["success", "warning", "info", "danger"];

        for (var j = 0; j < user_answers.length; j++) {
            var label = user_answers[j];
            var labelStyle = labelClasses[j % labelClasses.length];
            var newLabel = "<span class='label label-" + labelStyle + "'>" + label + "</span> &nbsp;";
            $("#labelCollection").append($(newLabel));
        }

        var infoWindow = new google.maps.InfoWindow(), marker, i;

        var infoWindowContent = [];

        for( i = 0; i < markers.length; i++ ) {
            var companyInfo = markers[i];
            infoWindowContent.push(formatContent(companyInfo, ""));
            var position = new google.maps.LatLng(companyInfo['Latitude'], companyInfo['Longitude']);
            bounds.extend(position);
            marker = new google.maps.Marker({
                position: position,
                map: map,
                title: companyInfo['Organization Name'],
                animation: google.maps.Animation.DROP,
                icon: image
            });

            // Allow each marker to have an info window
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infoWindow.setContent(infoWindowContent[i]);
                    infoWindow.open(map, marker);
                }
            })(marker, i));

            // Automatically center the map fitting all markers on the screen
            map.fitBounds(bounds);
        }

        // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
        var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
            this.setZoom(5);
            google.maps.event.removeListener(boundsListener);
        });
      }

    initMap();

    var offset = 220;
    var duration = 500;
    $(window).scroll(function() {
        if ($(this).scrollTop() > offset) {
            $('.back-to-top').fadeIn(duration);
        } else {
            $('.back-to-top').fadeOut(duration);
        }
    });

    $('.back-to-top').click(function(event) {
        event.preventDefault();

        // Scroll to the top
        $('html, body').animate({scrollTop: 0}, duration);
        return false;
    });
});


function formatContent(companyInfo, content) {
    content = content || '<b>' + companyInfo["Organization Name"] + '</b> is one of the largest corporation in the United States that serves in the ' +
        'technology industry.';

    var contentString = '<div id="content">' +
            '<h4><b>Website: </b>' + companyInfo["Website"] + '</h4>' +
            '<h4><b>Phone: </b>' + companyInfo["Phone"] + '</h4>' +
            '<h4><b>Address: </b>' + companyInfo["Full Address"] + '</h4>' + content

    return contentString;
}