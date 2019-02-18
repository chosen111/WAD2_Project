$(document).ready(function() {
    let csrf_token = $('main .menu').data('csrf');

    // Overlay functions
    let Overlay = {
        show(forced=false) {
            let $overlay = $('.overlay');
            if (!$overlay) return;

            // If forced parameter is true, don't show any animations
            if (forced) {
                return $overlay.css({ opacity: 1 });
            }
            // Else show the overlay in a fashioned manner
            else {
                $overlay.stop().animate({ opacity: 1 });
            }
        },
        // Remove overlay
        remove(forced=false) {
            let $overlay = $('.overlay');
            if (!$overlay) return;

            // If forced parameter is true, don't show any animations
            if (forced) {
                return $overlay.remove();
            }
            // Else hide the overlay in a fashioned manner
            else {
                $overlay.stop().animate({ opacity: 0 }, {
                    complete() {
                        $overlay.remove();
                    }
                });
            }
        }
    }

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

        Overlay.remove(forced=true);

        let $body = $('body');
        let $overlay = $("<div>", { class: 'overlay' });
        let $loginSection = $("<section>", { class: 'login-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($loginSection);
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

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
        
        $form.appendTo($loginSection);
        $overlay.appendTo($body);

        let height = $form.height();
        $form.height(0);

        Overlay.show(forced=false);        
        $form.delay(400).animate({ height: height }, {
            duration: 400,
            complete: function() {
                $form.children().animate({ opacity: 1 }, 400);
            }
        });
    })
})