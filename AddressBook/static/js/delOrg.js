  $(function() {
    $('#btnDelContact').click(function() {
        console.log("deleting Contact...")

        $.ajax({
            url: '/delContact',
            data: $('form').serialize(),
            type: 'PUT',
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