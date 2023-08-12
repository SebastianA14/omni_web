$(document).ready(function() {
    var joystickContainer = $("#joystick-container");
    var joystickHandle = $("#joystick-handle");
    var joystickRadius = joystickContainer.width() / 2;
    var handleRadius = joystickHandle.width() / 2;
    var isJoystickActive = false;

    joystickContainer.on("mousedown touchstart", function(e) {
        e.preventDefault();
        isJoystickActive = true;
        updateJoystickPosition(e);
    });

    $(document).on("mousemove touchmove", function(e) {
        if (isJoystickActive) {
            updateJoystickPosition(e);
        }
    });

    $(document).on("mouseup touchend", function(e) {
        if (isJoystickActive) {
            resetJoystick();
        }
    });

    function updateJoystickPosition(e) {
        var touch = e.type.startsWith("touch");
        var clientX = touch ? e.originalEvent.touches[0].clientX : e.clientX;
        var clientY = touch ? e.originalEvent.touches[0].clientY : e.clientY;
        var containerOffset = joystickContainer.offset();
        var centerX = containerOffset.left + joystickRadius;
        var centerY = containerOffset.top + joystickRadius;
        var deltaX = clientX - centerX;
        var deltaY = clientY - centerY;
        var distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        var angle = Math.atan2(deltaY, deltaX);

        if (distance > joystickRadius - handleRadius) {
            deltaX = Math.cos(angle) * (joystickRadius - handleRadius);
            deltaY = Math.sin(angle) * (joystickRadius - handleRadius);
        }

        joystickHandle.css({
            left: centerX + deltaX,
            top: centerY + deltaY
        });

        var normalizedDeltaX = deltaX / (joystickRadius - handleRadius);
        var normalizedDeltaY = deltaY / (joystickRadius - handleRadius);

        // Enviar los valores normalizados a través de AJAX o WebSocket
        sendJoystickData(normalizedDeltaX, normalizedDeltaY);
    }

    function resetJoystick() {
        joystickHandle.css({ left: "50%", top: "50%" });
        isJoystickActive = false;

        // Enviar valores de joystick a cero cuando se suelta
        sendJoystickData(0, 0);
    }

    function sendJoystickData(deltaX, deltaY) {
        // Realizar la llamada AJAX o WebSocket para enviar los datos del joystick al servidor
        // Aquí puedes agregar tu lógica para enviar los datos al servidor
    }
});
