$(".delete_button").click(function() {
    let answer = confirm("Вы действительно хотите удалить?");
    if (answer) {
        $(this).closest("form").submit();
    } else {
        event.preventDefault();
    }
});