  $(function() {
    $('#btnEditContact').click(function() {
        console.log("editing Contact...")

        $.ajax({
            url: '/runEditContact',
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