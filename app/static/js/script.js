// static/js/script.js

// Signature Pad Integration
var canvas = document.getElementById('signature-pad');

if (canvas) {
    var signaturePad = new SignaturePad(canvas);

    document.getElementById('clear').addEventListener('click', function (e) {
        e.preventDefault();
        signaturePad.clear();
    });

    var form = document.querySelector('form');
    form.addEventListener('submit', function (e) {
        if (signaturePad.isEmpty()) {
            alert('Please provide a signature.');
            e.preventDefault();
        } else {
            var dataUrl = signaturePad.toDataURL();
            document.getElementById('signature').value = dataUrl;
        }
    });
}

// Autocomplete for Locations (Example with a predefined list)
var locations = ["Warehouse A", "Dock B", "Depot C", "Factory D", "Terminal E"];

function autocomplete(inp, arr) {
    // Autocomplete function implementation
    // Due to space constraints, the implementation is not included
}

var routeFromInput = document.getElementById('routeFrom');
var routeToInput = document.getElementById('routeTo');

if (routeFromInput && routeToInput) {
    autocomplete(routeFromInput, locations);
    autocomplete(routeToInput, locations);
}
