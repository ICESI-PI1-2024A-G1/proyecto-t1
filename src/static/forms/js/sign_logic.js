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
                        if (signaturePad.isEmpty()) {
                            return Promise.reject("Por favor dibuja tu firma.");
                        } else {
                            return signaturePad.toDataURL(); // return the drawn signature
                        }
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
                Swal.fire({
                    title: 'Subir imagen',
                    input: 'file',
                    inputAttributes: {
                        'accept': 'image/*',
                        'aria-label': 'Sube tu firma'
                    }
                }).then((result) => {
                    if (result.value) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            document.getElementById('signature').innerHTML = '<img src="' + e.target.result + '" style="max-width: 100%; height: auto;">';
                        };
                        reader.readAsDataURL(result.value);
                    }
                });
                break;
        }
    });
});