$(document).ready(function() {
    let csrf_token = $('main .menu').data('csrf');

    $(document).on('click', '.button#logout', function() {
        let href = $(this).data('href');
        if (!href) return;

        $.post({
            headers: { "X-CSRFToken": csrf_token },
            url: document.location.origin + href,
            success: function(response) {
                window.location.assign(document.location.origin + response['redirect']);
            }
        })
    })

    $(document).on('click', '.button#login', function() {
        let href = $(this).data('href');
        if (!href) return;

        $('.overlay').remove();

        let $body = $('body');
        let $overlay = $("<div>", { class: 'overlay' });
        let $loginScreen = $("<section>", { class: 'login-section' }).appendTo($overlay);

        let $form = $("<form>", { id: "login-form" });
        $("<div>", { class: "title", text: "Log In" }).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "username", class: "icon-user" })).append(
            $("<input>", { class: "input", id: "username", type: "text", name: "username", value: "", size: 50 })).appendTo($form);

        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "password", class: "icon-encryption" })).append(
            $("<input>", { class: "input", id: "password", type: "password", name: "password", value: "", size: 50 })).appendTo($form);

        let $submit = $("<div>", { class: "button", id: "submit", text: "Log In" }).appendTo($form);
        $submit.on('click', function() {
            $.post({
                headers: { "X-CSRFToken": csrf_token },
                url: document.location.origin + href,
                data: $form.serialize(),
                success(response) {
                    window.location.assign(document.location.origin + response['redirect']);
                }
            });
        })
        
        $form.appendTo($loginScreen);
        $overlay.appendTo($body);

        let height = $form.height();
        $form.height(0);
        
        $form.delay(400).animate({ height: height }, {
            duration: 400,
            complete: function() {
                $(this).children().animate({ opacity: 1 }, 400);
            }
        });
    })
})