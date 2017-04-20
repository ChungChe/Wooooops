
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

function submit(ptr) {
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "url_id" : ptr.id 
            }),
        dataType: 'json',
        url: '/submit',
        success: function(data) {
            console.log(data['results']);
            console.log('Success ' + ptr.id);
            //$('#loading-indicator').remove()
            $(ptr).text(data['results']);
            $(ptr).prop('diabled', true);
            //ptr.remove();

        },
        error: function(error) {
            console.log('error');
            console.log(eval(error));
            //ptr.remove('.waiting_logo')
            $(ptr).text(eval(error));
            $(ptr).prop('diabled', true);
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
            redirect_url('/search/' + data['url']);
        },
        error: function(error) {
            console.log('error');
            console.log(eval(error));
        }
    });
}

function post_javlib_search_data() {
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "search_str" : $('#javlib_search_text').val()
            }),
        dataType: 'json',
        url: '/postjavlib',
        success: function(data) {
            redirect_url('/searchjavlib/' + data['url']);
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
    
    $('#javlib_button').click(function() {
        post_javlib_search_data();
    });
    
    // Press enter in search string
    $('#javlib_search_text').keypress(function(e) {
        if (e.which == '13') {
            post_javlib_search_data();
        }
    });

    $('.dl_button').click(function() {
        console.log("Click Download with " + this.id);
        $(this).append('<img src="/static/images/loading.gif" id="loading-indicator" style="display:none" />');
        submit(this)
        $(this).attr('diabled', true);
        //this.remove()
    });

})

$(document).ajaxSend(function(e, r, s) {
    console.log('ajax send');
    $('#loading-indicator').show();
});

$(document).ajaxComplete(function(e, r, s) {
    console.log('ajax complete');
    $('#loading-indicator').hide();
});
