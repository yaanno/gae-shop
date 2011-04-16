(function ($) {
    
    // add item to cart
    
    var $add_btn = $("#add_btn"),
        $form = $("#add_form");
    
    $add_btn.click(function (event) {
        event.preventDefault();
        //$add_btn.attr({ 'disabled': true });
        addToCart();
    })
    
    function addToCart() {
        var formdata = $form.serialize();
        if (formdata) {
            $.ajax({
                url: "/shop/cart/",
                type: "POST",
                data: formdata,
                success: function (response) {
                    if (response.success) {
                        // feedback
                        location.href = "/shop/cart/";
                    } else {
                        // feedback
                    }
                }
            })
        }
    };
    
    
    
})(jQuery);