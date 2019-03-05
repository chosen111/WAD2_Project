var LANG = {
    E_USERNAME_INVALID: "The username is invalid!",
    E_USERNAME_RANGE: "The username must have between 3 and 18 characters!",
    E_USERNAME_EXISTS: "The username already exists!",
    E_AUTH_MISMATCH: "Username or password mismatch!",
    E_AUTH_DISABALED: "The account is currently disabled",
    E_PASSWORD_MISMATCH: "Password mismatch!",
    E_PASSWORD_RANGE: "The password must have between 6 and 18 characters!",
    E_EMAIL_INVALID: "The e-mail is invalid!",
    I_REGISTER_SUCCESS: "Your account has been successfully created!",

    get(key) {
        return this[key] || key;
    }
}

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

var Validation = {
    register(data) {
        let error = { }
        if (!RegExp("^.{6,18}$").test(data.username)) {
            error.username = "E_USERNAME_RANGE";
        }
        else if (!RegExp("^[a-zA-Z0-9]+([\._\s\-]?[a-zA-Z0-9])*$").test(data.username)) {
            error.username = "E_USERNAME_INVALID";
        }
        if (!RegExp("^.{6,18}$").test(data.password)) {
            error.password = "E_PASSWORD_RANGE";
        }
        else if (data.password !== data.confirmPassword) {
            error.password = "E_PASSWORD_MISMATCH";
            error.confirmPassword = "E_PASSWORD_MISMATCH";
        }
        if (!RegExp("^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$").test(data.email)) {
            error.email = "E_EMAIL_INVALID";
        }
        return error;
    }
}

var Form = {
    serialize($form) {
        let $input = $form.find('input');
        let data = { }

        for (let i = 0; i < $input.length; i++) {
            data[$input[i].id] = $input[i].value
        }
        return data;
    },
    validate($form) {
        let error = Validation[$form.attr("id")].call($form, Form.serialize($form));
        if (!$.isEmptyObject(error)) {
            Form.error.show($form, error);
            return false;
        }
        return true;
    },
    input(type, ico, id, placeholder, cls, value) {
        let $input = $("<div>", { class: "input" }).addClass(id).addClass(cls);
        if (ico) $("<label>", { for: id, class: ico }).appendTo($input);
        $("<input>", { id: id, type: type, name: id, value: value || "", placeholder: placeholder, size: 50 }).appendTo($input);
        return $input;
    },
    error: {
        show($form, error) {
            if (!error) return false;

            for(let key in error) {
                let $input = $form.find(`.input.${key}`).addClass('error');
                if ($input.length == 0) Notification.push("icon-warning", `Cannot find the input: ${key}`, type="warning");

                let $icon = $("<i>", { class: "icon-warning alert" }).appendTo($input);
                Tooltip.add($icon, ico="icon-warning", text=LANG.get(error[key]), type="alert");
            }
        },
        clear($form) {
            $form.find('.input.error').removeClass('error').children('.alert').remove();
        }
    }
}

var Notification = {
    push(ico, text, type, timeout=5) {
        if (!text) return;
        
        let $section = $("section.notification");
        let $notification = $("<div>", { class: "notification" }).addClass(type);
        if (ico) $("<i>", { class: ico }).appendTo($notification);
        $("<span>", { class: "message", text: LANG.get(text) }).appendTo($notification);

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

// Tooltip functions
var Tooltip = {
    add(el, ico, text, type="default") {
        el.addClass('has-tooltip').data({ tooltip: text, tooltipType: type, tooltipIco: ico });
        return el;
    },
    show(el) {
        let $tooltip = $("<div>", { class: `is-tooltip ${el.data('tooltip-type')}` }).appendTo($('body'));
        if (el.data('tooltip-ico')) $("<i>", { class: el.data('tooltip-ico') }).appendTo($tooltip);
        $("<span>", { class: "text", text: el.data('tooltip') }).appendTo($tooltip);

        el.data('tooltip-ref', $tooltip);

        // Huge calculations to determine where the tooltip should be positioned, don't even ask
        let { left, top } = el.offset();
        let preset = {
          top: document.documentElement.clientHeight-top+5,
          middle: top+el[0].offsetHeight/2-$tooltip[0].offsetHeight/2,
          bottom: top+el[0].offsetHeight+5,
          left: document.documentElement.clientWidth-left+5,
          center: left+el[0].offsetWidth/2-$tooltip[0].offsetWidth/2,
          right: left+el[0].offsetWidth+5
        }
        let position = { 
          x: { css: "left", px: preset.center },
          y: { css: "bottom", px: preset.top }
        }
        let arrow = "bottom";

        if (position.x.px - $tooltip[0].offsetWidth <= 0 || position.x.px + $tooltip[0].offsetWidth >= document.documentElement.clientWidth) {
          position.y = { css: "top", px: preset.middle }
          if (position.x.px - $tooltip[0].offsetWidth <= 0) {
            position.x = { css: "left", px: preset.right }
            arrow = "left";
          }
          if (position.x.px + $tooltip[0].offsetWidth >= document.documentElement.clientWidth) {
            position.x = { css: "right", px: preset.left }
            arrow = "right"
          }
        }
        else {
          if (top - $tooltip[0].offsetHeight - 10 <= 0) {
            position.y = { css: "top", px: preset.bottom }
            arrow = "top";
          }      
        }
        $tooltip.css(position.x.css, position.x.px).css(position.y.css, position.y.px);
        $tooltip.addClass(arrow);
    },
    hide(el) {
        $tooltip = el.data('tooltip-ref');
        if (!$tooltip) return;

        $tooltip.remove();
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
        //Notification.push("icon-warning", "Test notification", type="alert");
        if (!href) return; // There is no href data on the element (console tampered maybe?)

        // Select the overlay element and append the main elements
        let $overlay = $('.overlay').empty();
        let $loginSection = $("<section>", { class: 'login-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($loginSection);
        // When the close button is clicked hide the overlay
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

        // Prepare the form elements
        let $form = $("<form>", { id: "login" });
        $("<div>", { class: "title", text: "Log In" }).appendTo($form);
        let $alternative = $("<div>", { class: "alternative" }).appendTo($form);
        Button.create("icon-sq-facebook", "Facebook", "facebook").appendTo($alternative);
        Button.create("icon-sq-twitter", "Twitter", "twitter").appendTo($alternative);
        $("<div>", { class: "separator", text: "OR" }).appendTo($form);
        Form.input(type="text", ico="icon-user", id="username", placeholder="USERNAME").appendTo($form);
        Form.input(type="password", ico="icon-locked", id="password", placeholder="PASSWORD").appendTo($form);
        // Extra account options
        let $extra = $("<div>", { class: "extra" }).appendTo($form);
        $("<div>", { text: "Don't have an account? " }).append($("<a>", { class: "register", text: "Sign Up!" })).appendTo($extra);
        $("<div>").append($("<a>", { class: "recover", text: "Forgot password?" })).appendTo($extra);
        Button.create("icon-rarrow", "Log In", "submit").appendTo($form);
        // When the submit button is clicked post the data to our login url
        $form.on('submit', function(evt) {
            Form.error.clear($form);
            $.post({
                headers: { "X-CSRFToken": csrf_token },
                url: document.location.origin + href,
                data: $form.serialize(),
                // If the login is successful, redirect to index page
                success(response) {
                    if (response['error']) {
                        Form.error.show($form, response['error']['form']);
                        Notification.push("icon-warning", response['error']['notification'], "warning");
                        return;
                    }
                    Overlay.remove(forced=false);
                    $form.trigger("reset");
                    Redirect.open(document.location.origin + response['redirect'])
                },
                fail() {                    
                    console.error(arguments);
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

        // Select the overlay element and append the main elements
        let $overlay = $('.overlay').empty();
        let $registerSection = $("<section>", { class: 'register-section' }).appendTo($overlay);
        let $close = $("<div>", { class: "icon-close" }).appendTo($registerSection);
        // When the close button is clicked hide the overlay
        $close.on('click', function() {
            Overlay.remove(forced=false);
        })

        // Prepare the form elements
        let $form = $("<form>", { id: "register" });
        $("<div>", { class: "title", text: "Sign Up" }).appendTo($form);
        let $alternative = $("<div>", { class: "alternative" }).appendTo($form);
        Button.create("icon-sq-facebook", "Facebook", "facebook").appendTo($alternative);
        Button.create("icon-sq-twitter", "Twitter", "twitter").appendTo($alternative);
        $("<div>", { class: "separator", text: "OR" }).appendTo($form);
        Form.input(type="text", ico="icon-user", id="username", placeholder="USERNAME").appendTo($form);
        Form.input(type="text", ico="icon-mail", id="email", placeholder="E-MAIL ADDRESS").appendTo($form);
        Form.input(type="password", ico="icon-locked", id="password", placeholder="PASSWORD").appendTo($form);
        Form.input(type="password", ico="icon-locked", id="confirmPassword", placeholder="PASSWORD").appendTo($form);
        // Extra account options
        let $extra = $("<div>", { class: "extra" }).appendTo($form);
        $("<div>", { text: "Already have an account? " }).append($("<a>", { class: "login", text: "Log In!" })).appendTo($extra);
        $("<div>").append($("<a>", { class: "recover", text: "Forgot password?" })).appendTo($extra);
        Button.create("icon-check", "Register", "submit").appendTo($form);
        // When the submit button is clicked post the data to our register url
        $form.on('submit', function(evt) {
            Form.error.clear($form);
            if(Form.validate($form)) {
                $.post({
                    headers: { "X-CSRFToken": csrf_token },
                    url: document.location.origin + href,
                    data: $form.serialize(),
                    // If the register is successful, close the overlay
                    success(response) {
                        if (response['error']) {
                            Form.error.show($form, response['error']['form']);
                            Notification.push("icon-warning", response['error']['notification'], "warning");
                            return;
                        }
                        Overlay.remove(forced=false);
                        $form.trigger("reset");
                        Notification.push("icon-check", "I_REGISTER_SUCCESS");
                    },
                    fail() {                    
                        console.log(arguments);
                    }
                })
            }
            evt.preventDefault();
        })
        // Insert the form elements in our login section and the overlay in our body page
        $form.appendTo($registerSection);

        // Animate the overlay and the login window
        let height = $form.height();
        $form.height(0);

        Overlay.show(forced=false); 
        $form.delay(400).animate({ height: height }, {
            complete() {
                $form.css({ height: 'auto' }).trigger("reset");
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
    $(document.body).on('keyup', function(evt) {
        // If the Escape key is released
        if (evt.key === 'Escape') {
            // Remove the overlay
           Overlay.remove(forced=true);
        }
    })

    $(document.body).on('click', '.register', function(evt) {
        let href = $(this).data('href') || "/codenamez/register/";
        Authentication.register(href);
    })

    $(document.body).on('click', '.login', function(evt) {
        let href = $(this).data('href') || "/codenamez/login/";
        Authentication.login(href);
    })

    $(document.body).on('click', '.logout', function(evt) {
        let href = $(this).data('href');
        Authentication.logout(href);
    })

    $(document.body).on('mouseenter', '[class*="has-tooltip"]', function(evt) {
        Tooltip.show($(this));
	})

	$(document.body).on('mouseleave', '[class*="has-tooltip"]', function(evt) { 
		Tooltip.hide($(this));
	})
})
