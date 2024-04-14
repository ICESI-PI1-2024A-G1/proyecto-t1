// Create a Signature Pad instance
var canvas = document.createElement('canvas');
canvas.width = 400;
canvas.height = 120;
var signaturePad = new SignaturePad(canvas);

// Sign button
document.getElementById('signButton').addEventListener('click', function(event) {
    event.preventDefault();
    Swal.fire({
        title: "Por favor elige una opción:",
        input: 'select',
        inputOptions: {
            'text': 'Escribir nombre',
            'draw': 'Dibujar firma',
            'upload': 'Subir imagen'
        },
        inputPlaceholder: 'Selecciona una opción',
        showCancelButton: true,
        inputValidator: (value) => {
            return new Promise((resolve) => {
                if (value) {
                    resolve();
                } else {
                    resolve('Debes seleccionar una opción');
                }
            });
        },
    })
    .then((result) => {
        switch (result.value) {
            case "text":
                Swal.fire({
                    title: "Por favor ingresa tu nombre:",
                    input: 'text',
                    showCancelButton: true,
                })
                .then((result) => {
                    if (result.value) {
                        document.getElementById('signature').innerHTML = '<p style="font-family: Cathylise Janetson; font-size: 60px;">' + result.value + '</p>';
                    }
                });
                break;
            case "draw":
                // Show a dialog with a canvas
                Swal.fire({
                    title: 'Por favor dibuja tu firma:',
                    html: canvas,
                    showCancelButton: true,
                    preConfirm: () => {
                        return signaturePad.toDataURL(); // return the drawn signature
                    }
                })
                .then((result) => {
                    if (result.value) {
                        document.getElementById('signature').innerHTML = '<img src="' + result.value + '">';
                    }
                });

                // Clear any previous signature
                signaturePad.clear();
                break;
            case "upload":
                document.getElementById('signatureImage').click();
                break;
        }
    });
});

// Image upload
document.getElementById('signatureImage').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('signature').innerHTML = '<img src="' + e.target.result + '">';
    };
    reader.readAsDataURL(event.target.files[0]);
});

// Save the drawn signature
document.getElementById('saveButton').addEventListener('click', function(event) {
    event.preventDefault();
    if (signaturePad.isEmpty()) {
        alert("Por favor dibuja tu firma.");
    } else {
        var dataUrl = signaturePad.toDataURL();
        document.getElementById('signature').innerHTML = '<img src="' + dataUrl + '">';
        canvas.style.display = 'none';
    }
});