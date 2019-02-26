// Overlay functions
var Overlay = {
    // Show overlay
    show(forced=false) {
        let $overlay = $('.overlay');
        if (!$overlay) return // Overlay doesn't exist so we cancel the execution
        if ($overlay.hasClass('visible')) return;

        // If forced parameter is true, don't show any animations
        if (forced) {
            $overlay.addClass('forced');
        }
        // Else show the overlay in a fashioned manner
        else {
            $overlay.removeClass('forced');
        }
        $overlay.removeClass('hidden').addClass('visible')
    },
    // Remove overlay
    remove(forced=false) {
        let $overlay = $('.overlay');
        if (!$overlay) return; // Overlay doesn't exist so we cancel the execution
        if ($overlay.hasClass('hidden')) return;

        // If forced parameter is true, don't show any animations
        if (forced) {
            $overlay.addClass('forced');
            $overlay.empty();
        }
        // Else hide the overlay in a fashioned manner
        else {
            $overlay.removeClass('forced');
            $overlay.one('webkitTransitionEnd otransitionend msTransitionEnd transitionend', function(evt) {
                $overlay.empty();
            })
        }
        $overlay.removeClass('visible').addClass('hidden')
    }
}

var Button = {
    create(ico, text, cls) {
        let $button = $("<button>", { class: `button` }).addClass(cls);
        if (ico) $("<i>", { class: ico }).appendTo($button);
        $("<span>", { class: "text", text: text }).appendTo($button);
        return $button;
    }
}

var Input = {
    create(ico, id, placeholder, cls, value) {
        let $input = $("<div>", { class: "input" }).addClass(id).addClass(cls);
        if (ico) $("<label>", { for: id, class: ico }).appendTo($input);
        $("<input>", { id: id, type: "text", name: id, value: value, placeholder: placeholder, size: 50 }).appendTo($input);
        return $input;
    }
}

var Notification = {
    push(ico, text, type, timeout=5) {
        let $section = $("section.notification");
        let $notification = $("<div>", { class: "notification" }).addClass(type);
        if (ico) $("<i>", { class: ico }).appendTo($notification);
        $("<span>", { class: "message", text: text }).appendTo($notification);

        $section.append($notification);
        $notification.animate({ height: 32, opacity: 1 });
        setTimeout(this.hide, timeout*1000, $notification);
    },
    hide($notification) {
        $notification.animate({ height: 0, opacity: 0 }, {
            complete() {
                $notification.remove();
            }
        })
    }
}

// Redirect functions
var Redirect = {
    open(href, target) {
        if (!href) return; // There is no href data on the element (console tampered maybe?)
        if (target != undefined) {
            window.open(href, target);
        }
        else {
            window.location.assign(href);
        }
    }
}

// Authentication functions
var Authentication = {
    login(href) {
        Notification.push("icon-warning", "Test notification", type="alert", timeout=100);
        if (!href) return; // There is no href data on the element (console tampered maybe?)

        // Select the body element and append the main elements
        let $overlay = $('.overlay');
        let $loginSection = $("<section>", { class: 'login-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($loginSection);
        // When the close button is clicked hide the overlay
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

        // Prepare the form elements
        let $form = $("<form>", { id: "login-form" });
        $("<div>", { class: "title", text: "Log In" }).appendTo($form);
        let $alternative = $("<div>", { class: "alternative" }).appendTo($form);
        Button.create("icon-sq-facebook", "Facebook", "facebook").appendTo($alternative);
        Button.create("icon-sq-twitter", "Twitter", "twitter").appendTo($alternative);
        $("<div>", { class: "separator", text: "OR" }).appendTo($form);
        Input.create(ico="icon-user", id="username").appendTo($form);
        Input.create(ico="icon-locked", id="password").appendTo($form);
        // Extra account options
        let $extra = $("<div>", { class: "extra" }).appendTo($form);
        $("<div>", { text: "Don't have an account? " }).append($("<a>", { class: "register", text: "Sign Up!" })).appendTo($extra);
        $("<div>").append($("<a>", { class: "recover", text: "Forgot password?" })).appendTo($extra);
        Button.create("icon-rarrow", "Log In", "submit").appendTo($form);
        // When the submit button is clicked post the data to our login url
        $form.on('submit', function(evt) {
            $.post({
                headers: { "X-CSRFToken": csrf_token },
                url: document.location.origin + href,
                data: $form.serialize(),
                // If the login is successful, redirect to index page
                success(response) {
                    if (response['error']) return console.error(response['error']);
                    Redirect.open(document.location.origin + response['redirect'])
                },
                fail() {
                    console.log(arguments);
                }
            })
            evt.preventDefault();
        })
        // Insert the form elements in our login section and the overlay in our body page
        $form.appendTo($loginSection);
            
        // Animate the overlay, login window and the login form
        let height = $form.height();
        $form.height(0);

        Overlay.show(forced=false); 
        $form.delay(400).animate({ height: height }, {
            complete() {
                $form.css({ height: 'auto' });
            }
        })
    },
    register(href) {
        if (!href) return; // There is no href data on the element (console tampered maybe?)

        // Select the body element and append the main elements
        let $overlay = $('.overlay');

        $overlay.empty();

        let $loginSection = $("<section>", { class: 'register-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($loginSection);
        // When the close button is clicked hide the overlay
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

        // Prepare the form elements
        let $form = $("<form>", { id: "register-form" });
        $("<div>", { class: "title", text: "Sign Up" }).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "username", class: "icon-user" })).append(
            $("<input>", { class: "input", id: "username", type: "text", name: "username", value: "", size: 50 })).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "email", class: "icon-user" })).append(
            $("<input>", { class: "input", id: "email", type: "text", name: "email", value: "", size: 50 })).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "password", class: "icon-encryption" })).append(
            $("<input>", { class: "input", id: "password", type: "password", name: "password", value: "", size: 50 })).appendTo($form);
        $("<div>", { class: "input-wrapper" }).append(
            $("<label>", { for: "confirm-password", class: "icon-encryption" })).append(
            $("<input>", { class: "input", id: "confirm-password", type: "password", name: "confirm-password", value: "", size: 50 })).appendTo($form);
        let $submit = $("<div>", { class: "button submit", text: "Log In" }).appendTo($form);
        // When the submit button is clicked post the data to our login url
        $submit.on('click', function() {
            $.post({
                headers: { "X-CSRFToken": csrf_token },
                url: '/codenamez/register',
                data: $form.serialize(),
                // If the login is successful, redirect to index page
                success(response) {
                    if (response['error']) return console.error(response['error']);
                    Redirect.open(document.location.origin + response['redirect'])
                },
                fail() {
                    console.log(arguments);
                }
            })
        })
        // Insert the form elements in our login section and the overlay in our body page
        $form.appendTo($loginSection);

        // Animate the overlay and the login window
        let height = $form.height();
        $form.height(0);

        Overlay.show(forced=false); 
        $form.delay(400).animate({ height: height }, {
            complete() {
                $form.css({ height: 'auto' });
                console.log($form.css("height"));
            }
        })
    },
    logout(href) {
        if (!href) return; // There is no href data on the element (console tampered maybe?)

        $.post({
            headers: { "X-CSRFToken": csrf_token },
            url: document.location.origin + href,
            success: function(response) {
                Redirect.open(document.location.origin + response['redirect'])
            }
        })
    }
}

// When document is ready
$(document).ready(function() {
    $(document).on('keyup', function(evt) {
        // If the Escape key is released
        if (evt.key === 'Escape') {
            // Remove the overlay
           Overlay.remove(forced=true);
        }
    })

    $(document).on('click', '.register', function(evt) {
        let href = $(this).data('href') || "/codenamez/register/";
        Authentication.register(href);
    })

    $(document).on('click', '.login', function(evt) {
        let href = $(this).data('href');
        Authentication.login(href);
    })

    $(document).on('click', '.logout', function(evt) {
        let href = $(this).data('href');
        Authentication.logout(href);
    })
})