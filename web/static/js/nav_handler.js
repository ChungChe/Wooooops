
function redirect_url(search_str) {
    $.ajax({
        url: '/' + search_str,
        success: function(r) {
            redirect_url(this.url);
            window.location.replace(this.url);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$(function() {

    // Click Submit in navbar
    $('#button_submit').click(function() {
        var search_str = $('#search_text').val();
        console.log(search_str);
        redirect_url(search_str);
    });
    // Press enter in search string
    $('#search_text').keypress(function(e) {
        if (e.which == '13') {
            var search_str = $('#search_text').val();
            console.log(search_str);
            redirect_url(search_str);
        }
    });



})
