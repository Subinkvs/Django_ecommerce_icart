$(function(){
    $('#cancelOrderBtn').on('click', function() {
        var orderId = $(this).data('order-id');
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/orders/" + orderId + "/cancel/",
            data: {
                'orderId':orderId,
                csrfmiddlewaretoken: token
            },
            success: function(response) {
                console.log(response);
                alertify.success(response.status);

                setTimeout(function() {
                    location.reload(true);
                }, 1000);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
