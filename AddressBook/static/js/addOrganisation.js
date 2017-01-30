  $(function() {
    $('#btnAddOrganisation').click(function() {
        console.log("adding Organisation...")

        $.ajax({
            url: '/addOrganisation',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                window.location.href = "viewBook";                
                console.log("success")
                console.log(response);
            },
            error: function(error) {
                console.log("went bad")
                console.log(error);
            }
        });
    });
  });