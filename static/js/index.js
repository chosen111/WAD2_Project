function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name+'=; Max-Age=-99999999;';  
}

$(document).ready(function() {
    $(document).on('click', '.button#logout', function() {
        let href = $(this).data('href');
        if (!href) return;

        $.post({
            headers: { "X-CSRFToken": token },
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
        $body.append($overlay);

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
                headers: { "X-CSRFToken": token },
                url: document.location.origin + href,
                data: $form.serialize(),
                success(response) {
                    window.location.assign(document.location.origin + response['redirect']);
                }
            });
        })
        
        $form.appendTo($loginScreen);

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