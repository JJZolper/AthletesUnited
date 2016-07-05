
// Post Posts
$(document).ready(function() {
    $('#CommunityPostForm').submit(function(event) { // catch the form's submit event
        event.preventDefault();
        $.ajax({ // create an AJAX call...
            type: $(this).attr('method'), // GET or POST
            data: $(this).serialize(), // get the form data
            url: $(this).attr('action'), // the file to call
            // success: function(data){alert(data)}
            success: function(data)
            {
               
                console.log(data.html)
                $(".new-community-posts").html(data.html);
    
            }
            
        });
        
        return false;
        
    });

});

// Delete a post or comment with AJAX triggered via a hyperlink
window.onload = function() {
    
    var aShowMorePosts = document.getElementById("showMorePosts");
    
    var aAllComments = document.getElementById("showAllComments");
    
    var aVerifiedUserComments = document.getElementById("showVerifiedUserComments");

    var aPost = document.getElementById("deletePost");
    
    var aComment = document.getElementById("deleteComment");
    
    if(!!aShowMorePosts)
    {
        
        aShowMorePosts.onclick = function() {
            
            console.log("Show More Posts Request ")
            showMorePosts();
            return false;
            
        }
        
    }
    
    if(!!aAllComments)
    {
        
        aAllComments.onclick = function() {
            
            var postid = $( this ).attr( 'postid' );
            console.log("All Comments Request: " + postid)
            showAllComments(postid);
            return false;
            
        }
        
    }
    
    if(!!aVerifiedUserComments)
    {
        
        aVerifiedUserComments.onclick = function() {
            
            var postid = $( this ).attr( 'postid' );
            var verifiedathleteslug = $( this ).attr( 'verifiedathleteslug' );
            console.log("Verified User Comments Request: " + postid + " " + verifiedathleteslug)
            showVerifiedUserComments(postid, verifiedathleteslug);
            return false;
            
        }
        
    }
    
    if(!!aPost)
    {
        
        aPost.onclick = function() {
            
            var postidreq = $( this ).attr( 'postidreq' );
            console.log("Post ID: " + postidreq)
            deletePost(postidreq);
            return false;
            
        }
        
    }
 
    if(!!aComment)
    {
        
        aComment.onclick = function() {
            
            var commentidreq = $( this ).attr( 'commentidreq' );
            console.log("Comment ID: " + commentidreq)
            deleteComment(commentidreq);
            return false;
            
        }
        
    }

}

function showMorePosts() {
    
    $.ajax({
           
        type: $(this).attr('method'), // GET or POST
        data: {},                 // Pass the Community Post Request to perform retrieval
        url: $(this).attr('action'),
        success: function(data) {

            $('.communityEXT').append(data.morepostshtml)

        },

            failure: function(data) {
            alert('Error retrieving more posts');

        }
           
    });
    
    return false;
    
}

function showAllComments(postid) {
    
    $('#comments-' + postid).html("");
    
    $.ajax({
           
        type: $(this).attr('method'), // GET or POST
        data: {'postid': postid},                 // Pass the Community Post Request to perform retrieval
        url: $(this).attr('action'),
        success: function(data) {

            $('#comments-' + postid).html(data.commentshtml);

        },

        failure: function(data) {
            alert('Error retrieving the community comments');

        }

    });
    
    return false;
    
}

function showVerifiedUserComments(postid, verifiedathleteslug) {
    
    $('#comments-' + postid).html("");
    
    $.ajax({

        type: $(this).attr('method'), // GET or POST
        data: {'postid': postid, 'verifiedathleteslug': verifiedathleteslug},                 // Pass the Community Post Request to perform retrieval
        url: $(this).attr('action'),
        success: function(data) {

            $('#comments-' + postid).html(data.commentshtml);

        },

        failure: function(data) {
            alert('Error retrieving the community comments');

        }

    });

    return false;
    
}


function deletePost(postidreq) {

    $.ajax({

        type: $(this).attr('method'), // GET or POST
        data: {'postidreq': postidreq},                 // Pass the PostID to perform deletion
        url: $(this).attr('action'),
        success: function(data) {
           
            element = document.getElementById('p' + data.postID);
            element.parentNode.removeChild(element);
           
            console.log("The post with id: " + data.postID + " is now deleted.")
           
        },
           
        failure: function(data) {
            alert('Error deleting the post with ID: ' + data.postID);
           
        }

    });
    
    return false;

}

function deleteComment(commentidreq) {
    
    $.ajax({
       
       type: $(this).attr('method'), // GET or POST
       data: {'commentidreq': commentidreq},                 // Pass the CommentID to perform deletion
       url: $(this).attr('action'),
       success: function(data) {
           
           element = document.getElementById('c' + data.commentID);
           element.parentNode.removeChild(element);
           
           console.log("The comment with id: " + data.commentID + " is now deleted.")
       
       },
           
       failure: function(data) {
           alert('Error deleting the comment with ID: ' + data.commentID);
       
       }
           
    });
    
    return false;
    
}






