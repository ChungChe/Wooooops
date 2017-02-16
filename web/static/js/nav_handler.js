
function redirect_url(search_str) {
    $.ajax({
        url: search_str,
        success: function(r) {
            window.location.replace(this.url);
            //console.log("Replace to " + this.url + "and r = " + r);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function post_data() {
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "exists" : $('#exists').is(':checked'),
            "search_str" : $('#search_text').val()
            }),
        dataType: 'json',
        url: '/post',
        success: function(data) {
            console.log(data);
            console.log('Success');
            redirect_url('/search/' + data['url']);
        },
        error: function(error) {
            console.log('error');
            console.log(eval(error));
        }
    });
}


$(function() {

    // Click Submit in navbar
    $('#button_submit').click(function() {
        console.log("Click Submit");
        post_data();
    });
    // Press enter in search string
    $('#search_text').keypress(function(e) {
        if (e.which == '13') {
            console.log("Press Enter");
            post_data();
        }
    });



})
