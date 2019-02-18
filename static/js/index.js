$(document).ready(function() {
    let csrf_token = $('main .menu').data('csrf');

    // Overlay functions
    let Overlay = {
        // Show overlay
        show(forced=false) {
            let $overlay = $('.overlay');
            if (!$overlay) return; // Overlay doesn't exist so we cancel the execution

            // If forced parameter is true, don't show any animations
            if (forced) {
                return $overlay.css({ opacity: 1 });
            }
            // Else show the overlay in a fashioned manner
            else {
                $overlay.stop().animate({ opacity: 1 });
                $overlay.children().delay(400).animate({ opacity: 1 });
            }
        },
        // Remove overlay
        remove(forced=false) {
            let $overlay = $('.overlay');
            if (!$overlay) return; // Overlay doesn't exist so we cancel the execution

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
                })
            }
        }
    }

    $(document).on('keyup', function(e) {
        // If the Escape key is released
        if (e.key === 'Escape') {
            // Remove the overlay
           Overlay.remove(forced=true);
        }
    })

    $(document).on('click', '.button#admin', function() {
        let href = $(this).data('href');
        if (!href) return; // There is no href data on the element (console tampered maybe?)
        
        window.location.assign(document.location.origin + '/' + href);
    })

    $(document).on('click', '.button#logout', function() {
        let href = $(this).data('href');
        if (!href) return; // There is no href data on the element (console tampered maybe?)

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
        if (!href) return; // There is no href data on the element (console tampered maybe?)

        // Make sure there is no existent overlay
        Overlay.remove(forced=true);

        // Select the body element and append the main elements
        let $body = $('body');
        let $overlay = $("<div>", { class: 'overlay' });
        let $loginSection = $("<section>", { class: 'login-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($loginSection);
        // When the close button is clicked hide the overlay
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

        // Prepare the form elements
        let $form = $("<form>", { id: "login-form" });
        $("<div>", { class: "title", text: "Log In" }).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "username", class: "icon-user" })).append(
            $("<input>", { class: "input", id: "username", type: "text", name: "username", value: "", size: 50 })).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "password", class: "icon-encryption" })).append(
            $("<input>", { class: "input", id: "password", type: "password", name: "password", value: "", size: 50 })).appendTo($form);
        let $submit = $("<div>", { class: "button", id: "submit", text: "Log In" }).appendTo($form);
        // When the submit button is clicked post the data to our login url
        $submit.on('click', function() {
            $.post({
                headers: { "X-CSRFToken": csrf_token },
                url: document.location.origin + href,
                data: $form.serialize(),
                // If the login is successful, redirect to index page
                success(response) {
                    window.location.assign(document.location.origin + response['redirect']);
                }
            })
        })
        
        // Insert the form elements in our login section and the overlay in our body page
        $form.appendTo($loginSection);
        $overlay.appendTo($body);

        // Animate the overlay, login window and the login form
        let height = $form.height();
        $form.height(0);

        Overlay.show(forced=false);        
        $form.delay(800).animate({ height: height }, {
            complete: function() {
                $form.children().animate({ opacity: 1 }, 400);
            }
        })
    })
})