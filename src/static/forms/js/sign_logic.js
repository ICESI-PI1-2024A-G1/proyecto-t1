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

    loadStyles(showSelect = false) {
        // Agrega estilos Bootstrap al botón de confirmación
        const confirmButton = Swal.getConfirmButton();
        confirmButton.classList.add('btn', 'btn-primary', 'mx-2');
        confirmButton.classList.remove('swal2-styled');
        
        // Agrega estilos Bootstrap al botón de cancelar
        const cancelButton = Swal.getCancelButton();
        cancelButton.classList.add('btn', 'btn-secondary', 'mx-2');
        cancelButton.classList.remove('swal2-styled');
        
        // Agrega estilos Bootstrap al input
        const selectInput = document.querySelector('#swal2-select');
        
        if(showSelect) {
            selectInput.classList.add('form-select', 'mx-0');
            selectInput.style = `
                --bs-form-select-bg-img: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%2867, 89, 113, 0.6%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
                background-color: #fff;
                background-image: var(--bs-form-select-bg-img),var(--bs-form-select-bg-icon, none);
                background-repeat: no-repeat;
                background-position: right .875rem center;
                background-size: 17px 12px;
                border: var(--bs-border-width) solid #d9dee3;
                border-radius: var(--bs-border-radius);
                transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
            `;
        } else {
            selectInput.style.display = "none"
        }
        const textInput = document.querySelector('.swal2-input');
        textInput.classList.add('form-control', 'mx-0');
        const fileInput = document.querySelector('.swal2-file');
        fileInput.classList.add('form-control', 'mx-auto');
        
        const swalModal = document.querySelector('.swal2-modal');
        swalModal.classList.add('px-4')
        const swalCanvas = document.querySelector('#swal2-html-container');
        swalCanvas.classList.add('border', 'rounded')

    }

    handleSignButtonClick(event) {
        this.serverRoute = window.location.pathname;
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
            didOpen: () => {
                this.loadStyles(true);
            }
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
            didOpen: () => {
                this.loadStyles();
            },
        })
        .then((result) => {
            if (result.value) {
                let signature = '<p style="font-family: Cathylise Janetson; font-size: 60px;">' + result.value + '</p>';
                document.getElementById('signature').innerHTML = signature;
                document.getElementById('signatureStatus').value = "Yes";
                document.getElementById('signatureInput').value = 1 + "---" + result.value;
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
                    Swal.showValidationMessage('Debes dibujar tu firma'); 
                } else {
                    document.getElementById('signature').value = "Yes";
                    document.getElementById('signatureStatus').value = "Yes";
                    return this.signaturePad.toDataURL();
                }
            },
            didOpen: () => {
                this.loadStyles();
            }
        })
        .then((result) => {
            if (result.value) {
                let signature = '<img src="' + result.value + '">';
                document.getElementById('signature').innerHTML = signature;
                document.getElementById('signatureInput').value = 2 + "---" + result.value;
            }
        });

        // Clear any previous signature
        this.signaturePad.clear();
    }

    handleUploadOption() {
        Swal.fire({
            title: 'Subir imagen',
            input: 'file',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            inputAttributes: {
                'accept': 'image/*',
                'aria-label': 'Sube tu firma'
            },
            didOpen: () => {
                this.loadStyles();
            }
            
        }).then((result) => {
            if (result.value) {
                var reader = new FileReader();
                reader.onload = (e) => {
                    let signature = '<img src="' + e.target.result + '" style="max-width: 100%; height: auto;">';
                    document.getElementById('signature').innerHTML = signature;
                    document.getElementById('signatureStatus').value = "Yes";
                    document.getElementById('signatureInput').value = 3 + "---" + e.target.result;
                };
                reader.readAsDataURL(result.value);
            }
        });
    }
}

// Create a new instance of the class
new SignatureLogic();