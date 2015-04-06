$(function() {

    // displays list of communities with matching on interest in the input box
    $('#search').keyup(function() {
        if ($('#search').val().trim()) {
            $('#search_communities').show();
            $.ajax({
                type: "POST",
                url: "/search/",
                data: {
                    'search_text': $('#search').val().trim(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: searchSuccess,
                dataType: 'html'
            });
        } else {
            $('#search_communities').hide();
        }
    });

    // disable enter button
    $('#search').keydown(function(event){
        if (event.keyCode==13) {
            event.preventDefault();
            return false;
        }
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
                            window.location.reload(true)                                                       
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

        bootbox.prompt("Write a comment (maximum 100 characters):", 
            function(result) {
                if (result) {
                    $.ajax({
                        type: "POST",
                        url: "comment",
                        data: {
                            'cid': cid, 'text': result.trim().substring(0,100),
                            'csrfmiddlewaretoken': '{{csrf_token}}'
                        },
                        success: function(response) {
                            // reload page to display new comment
                            window.location.reload(true);
                        },
                        dataType: 'html'
                    });
                }
            }
        );
    });

    $('#project_start').click(function() {
        bootbox.alert("You must enter your credit card information before you can start a project.",
            function() {});
    });

    $('#project_fund').click(function() {
        bootbox.alert("You must enter your credit card information before you can fund this project.",
            function() {});
    });

    // Javascript to enable link to a nav tab
    var url = document.location.toString();
    if (url.match('#')) {
        $('.nav-pills a[href=#'+url.split('#')[1]+']').tab('show') ;
    } 

    // Change hash for page-reload to open proper tab
    $('.nav-pills a').on('shown.bs.tab', function (e) {
        window.location.hash = e.target.hash;
    });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search_communities').html(data);
}
