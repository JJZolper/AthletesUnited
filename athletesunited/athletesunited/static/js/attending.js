
// Toggle whether an Athlete is attending or not attending an Event
window.onload = function() {
    var aCollegeEventAttending = document.getElementById("toggleCollegeEventAttending");

    if(!!aCollegeEventAttending)
    {
        aCollegeEventAttending.onclick = function() {
            var eventidreq = $( this ).attr( 'eventidreq' );
            console.log("Event ID: " + eventidreq)
            toggleCollegeEventAttending(eventidreq);
            return false;
        }
    }
}

function toggleCollegeEventAttending(eventidreq) {
    
    $.ajax({
        type: $(this).attr('method'), // GET or POST
        data: {'eventidreq': eventidreq},                 // Pass the PostID to perform deletion
        url: $(this).attr('action'),
        success: function(data) {
            console.log("Athlete is now: " + data.AttendingStatus)
            element = document.getElementById("AttendingStatus");
            element.innerHTML = "" + data.AttendingStatus + "";
        },
        failure: function(data) {
            alert('Error updating the attending status of the college event with ID: ' + data.collegeEventID);
        }
    });
    return false;
}


