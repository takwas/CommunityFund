$(function() {

    // displays list of communities with matching on interest in the input box
    $('#search').keyup(function() {
        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });

    // adds user to the current community
    $('#join_comm').click(function() {
        var cid = $(this).attr('name');

        bootbox.confirm("Are you sure you want to join this community?", 
            function(result) {
                if (result) {
                    $.ajax({
                        type: "POST",
                        url: "join",
                        data: {
                            'cid': cid, 'csrfmiddlewaretoken': '{{csrf_token}}'
                        },
                        success: function(response) {
                            window.location.reload(true);
                        },
                        dataType: 'html'
                    });
                }
            }
        );
    });

    // adds new comment to community
    $('#add_cmnt').click(function() {
        var cid = $(this).attr('name');

        bootbox.prompt("Write a comment", 
            function(result) {
                if (result) {
                    $.ajax({
                        type: "POST",
                        url: "comment",
                        data: {
                            'cid': cid, 'text': result,
                            'csrfmiddlewaretoken': '{{csrf_token}}'
                        },
                        success: function(response) {
                            window.location.reload(true);
                        },
                        dataType: 'html'
                    });
                }
            }
        );
    });

});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search_communities').html(data);
}
