
// Search Communities
$(function() {
    $('#searchquery').keyup(function() {
        $.ajax({
               
            type: "POST",
            data: {
               'searchquery': $('#searchquery').val(),
               'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken").val()
            },
            url: "/search/",
            success: searchSuccess,
            dataType: 'html'
               
        });
        
    });
    
});

function searchSuccess(data, textStatus, jqXHR)
{
    
    console.log(data)
    $('#search-results').html(data);
    
}



