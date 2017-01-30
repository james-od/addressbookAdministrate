  $(function() {
    $('#btnEditOrg').click(function() {
        console.log("editing organisation...")

        $.ajax({
            url: '/runEditOrg',
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