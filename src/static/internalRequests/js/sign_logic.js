// Load signature on page load
document.addEventListener('DOMContentLoaded', (event) => {
    console.log("Hola")
    var signatureInput = document.getElementById('signatureInput').value;
    var signatureValue = signatureInput.substring(4);
    var signatureType = signatureInput.charAt(1);
    var signatureElement = document.getElementById('signature');

    if (signatureType === '1') {
        signatureElement.innerHTML = '<p style="font-family: Cathylise Janetson; font-size: 60px;">' + signatureValue + '</p>';
    } else if (signatureType === '2') {
        signatureElement.innerHTML = '<img src="' + signatureValue + '">';
    } else if (signatureType === '3') {
        signatureElement.innerHTML = '<img src="' + signatureValue + '" style="max-width: 100%; height: auto;">';
    }
});