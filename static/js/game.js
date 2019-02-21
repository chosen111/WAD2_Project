$(document).ready(function() {
    $(document).on('contextmenu', '.card', function(e) {
        let $flipCard = $(this).children();
        let toggle = $flipCard.hasClass('reversed') ? true : false;
        if (toggle) {
            $flipCard.removeClass('reversed').addClass('normal');
        }
        else {
            $flipCard.removeClass('normal').addClass('reversed');
        }

        e.preventDefault();
    })
})