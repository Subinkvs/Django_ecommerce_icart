jQuery(function(){
    $('.button-increament').on('click', function(e) { 
        e.preventDefault();

       var inc_value = $(this).closest('.product_data').find('.qty-input').val();
       var value = parseInt(inc_value,10);
       value = isNaN(value) ? 0 : value;
       if(value < 10)
       {
        value++;
        $(this).closest('.product_data').find('.qty-input').val(value);
       }
    });
    $('.button-decreament').on('click', function(e) { 
        e.preventDefault();

       var dec_value = $(this).closest('.product_data').find('.qty-input').val();
       var value = parseInt(dec_value,10);
       value = isNaN(value) ? 0 : value;
       if(value > 1)
       {
        value--;
        $(this).closest('.product_data').find('.qty-input').val(value);
       }
    });
    $('.addToCartBtn').on('click', function(e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

      
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // window.location.reload(true)
                
                console.log(response)
                alertify.success(response.status)
               
            }
            
        });
    });
    $('.addToWishlistBtn').on('click', function(e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

      
        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // window.location.reload(true)
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });
    $('.ChangeQuantity').on('click', function(e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

      
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken: token
            },
            success: function () {
                
               window.location.reload(true)
            }
        });
    });
    $('.delete-cart-item').on('click', function(e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

      
        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");
                location.reload(true);
            }
        });
    });

    $('.delete-wishlist-item').on('click', function(e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

      
        $.ajax({
            method: "POST",
            url: "delete-wishlist-item",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");
                location.reload(true);
            }
        });
    });
});


