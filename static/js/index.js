$(document).ready(function() {
    $(document).on('click', '.button#login', function() {
        $('.overlay').remove();
        
        let $body = $('body');
        let $overlay = $("<div>", { class: 'overlay' });

        let $loginScreen = $("<section>", { class: 'login-section' }).appendTo($overlay);
        $body.append($overlay);
    })
})