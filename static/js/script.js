// A function to confirm deletion form
function confirmMessage() {
    if (confirm("Are you sure you want to delete all data?")) {
        // Look for the corresponding form in the HTML document
        var form = document.getElementById('delete_all_data');
        // Submit the form
        form.submit();
    }
}

// A JS timer code to refresh the page
var time = new Date().getTime();
    console.log('Timer started.')

    // If there is a mouse movement or a keypress
    $(document.body).bind("mousemove keypress", function (e) {
        // Restart the timer
        time = new Date().getTime();
    });

    function refresh() {
        // If 30 seconds passed without mouse movement or keypress
        if (new Date().getTime() - time >= 30000)
            // refresh the page
            window.location.reload(true);

        else {
            // Run another 10-second timer
            console.log('Another 10 seconds countdown started.')
            setTimeout(refresh, 10000);
        }
    }

    // Run a 10-second timer
    setTimeout(refresh, 10000);