$(document).ready(function() {
    var minWidth = 50;
    var minHeight = 50;
    var maxWidth = 600;
    var maxHeight = 450;

    $(".chat-area").resizable({
        minWidth: minWidth,
        minHeight: minHeight,
        maxWidth: maxWidth,
        maxHeight: maxHeight,
        resize: function(event, ui) {
            $(".input-button").width(ui.size.width);
        }
    });
});