$(document).ready(function() {
    let minWidth = 50;
    let minHeight = 50;
    let maxWidth = 600;
    let maxHeight = 450;

    $(".chat-area").resizable({
        minWidth: minWidth,
        minHeight: minHeight,
        maxWidth: maxWidth,
        maxHeight: maxHeight,
        resize: function(event, ui) {
            $(".input-button").width(ui.size.width + 20);
        }
    });
});