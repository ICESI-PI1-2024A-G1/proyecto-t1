class SignatureLogic {
    constructor() {
        // Create a Signature Pad instance
        this.canvas = document.createElement('canvas');
        this.canvas.width = 400;
        this.canvas.height = 120;
        this.signaturePad = new SignaturePad(this.canvas);

        // Sign button
        document.getElementById('signButton').addEventListener('click', (event) => {
            this.handleSignButtonClick(event);
        });
    }

    handleSignButtonClick(event) {
        event.preventDefault();
        Swal.fire({
            title: "Por favor, elige una opción:",
            input: 'select',
            inputOptions: {
                'text': 'Escribir nombre',
                'draw': 'Dibujar firma',
                'upload': 'Subir imagen'
            },
            inputPlaceholder: 'Selecciona una opción',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
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
                    this.handleTextOption();
                    break;
                case "draw":
                    this.handleDrawOption();
                    break;
                case "upload":
                    this.handleUploadOption();
                    break;
            }
        });
    }

    handleTextOption() {
        Swal.fire({
            title: "Por favor, ingresa tu nombre:",
            input: 'text',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
        })
        .then((result) => {
            if (result.value) {
                document.getElementById('signature').innerHTML = '<p style="font-family: Cathylise Janetson; font-size: 60px;">' + result.value + '</p>';
                document.getElementById('signatureStatus').value = "Yes";
            }
        });
    }

    handleDrawOption() {
        // Show the signature pad
        Swal.fire({
            title: 'Por favor, dibuja tu firma:',
            html: this.canvas,
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            preConfirm: () => {
                if (this.signaturePad.isEmpty()) {
                    return Promise.reject("Por favor, dibuja tu firma.");
                } else {
                    document.getElementById('signature').value = "Yes";
                    document.getElementById('signatureStatus').value = "Yes";
                    return this.signaturePad.toDataURL();
                }
            }
        })
        .then((result) => {
            if (result.value) {
                document.getElementById('signature').innerHTML = '<img src="' + result.value + '">';
            }
        });

        // Clear any previous signature
        this.signaturePad.clear();
    }

    handleUploadOption() {
        Swal.fire({
            title: 'Subir imagen',
            input: 'file',
            cancelButtonText: 'Cancelar',
            inputAttributes: {
                'accept': 'image/*',
                'aria-label': 'Sube tu firma'
            }
        }).then((result) => {
            if (result.value) {
                var reader = new FileReader();
                reader.onload = (e) => {
                    document.getElementById('signature').innerHTML = '<img src="' + e.target.result + '" style="max-width: 100%; height: auto;">';
                    document.getElementById('signatureStatus').value = "Yes";
                };
                console.log(document.getElementById('signatureStatus').value);
                console.log("Yes")
                reader.readAsDataURL(result.value);
            }
        });
    }
}

// Create a new instance of the class
new SignatureLogic();