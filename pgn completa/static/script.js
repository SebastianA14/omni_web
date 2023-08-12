// Function to handle button clicks
function buttonClicked(direction) {
    // Send the direction to the server
    fetch("/control", {
        method: "POST",
        body: JSON.stringify({ direction }),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Verificar la respuesta del servidor en la consola
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Add click event listeners to the buttons
const buttons = document.getElementsByClassName("button");
Array.from(buttons).forEach((button) => {
    button.addEventListener("click", function() {
        const direction = button.getAttribute("data-direction");
        buttonClicked(direction);
    });
});
