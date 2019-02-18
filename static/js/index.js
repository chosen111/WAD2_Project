$(document).ready(function() {
    $(document).on('click', '.button#logout', function() {
        let href = $(this).data('href');
        if (!href) return;

        $.get({
            url: document.location.origin + href,
            success: function(response) {
                window.location.assign(document.location.origin + response['redirect']);
            }
        })
    })

    $(document).on('click', '.button#login', function() {
        $('.overlay').remove();

        let $body = $('body');
        let $overlay = $("<div>", { class: 'overlay' });

        let $loginScreen = $("<section>", { class: 'login-section' }).appendTo($overlay);
        $body.append($overlay);

        let $form = $("<form>", { })
    })
})