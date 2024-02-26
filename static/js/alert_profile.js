$(".delete_user").click(function() {
    let answer = confirm("Вы действительно хотите удалить пользователя?");
    if (answer) {
        $(this).closest("form").submit();
    } else {
        event.preventDefault();
    }
});


$(".exit").click(function() {
    let answer = confirm("Вы действительно хотите выйти?");
    if (answer) {
        $(this).closest("form").submit();
    } else {
        event.preventDefault();
    }
});