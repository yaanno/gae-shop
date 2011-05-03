(function ($) {
    
    // add item to cart
    
    var $add_btn = $("#add_btn"),
        $form = $("#add_form"),
        $items = $("#cart_item_list li span"),
        $modify_cart = $("#modify_cart");
    
    $add_btn.click(function (event) {
        event.preventDefault();
        $add_btn.attr({ 'disabled': true });
        addToCart();
    });
    
    $modify_cart.click(function (event) {
        event.preventDefault();
        if ($(this).hasClass('editing')) {
            $modify_cart.attr({ 'disabled': true });
            updateCart();
        } else {
            editableCart();
        }
    });
    
    function updateCart() {
        
        /*
        format: 
        {
            'products': [
                {'product_id': 61, 'product_quantity': 20},
                {'product_id': 60, 'product_quantity': 20}
            ]
        }
        */
        var formdata = [];
        $items.each(function (index, elem) {
            var input = $(elem).prev(),
                p_id = $(elem).attr('data-product-id'),
                p_quantity = $(input).val();
            formdata.push({ 'product_id': p_id, 'product_quantity': p_quantity })
        })
        var formdata = JSON.stringify({ 'products': formdata })
        $.ajax({
            url: "/shop/cart/",
            type: "PUT",
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
    };
    
    function editableCart() {
        // set editing state
        $modify_cart.toggleClass('editing').text('Update Cart Content');
        
        // replace item quantity spans with inputs
        $items.each(function (index, elem) {
            var input_type ='',
                options = null,
                value = $(elem).text(),
                id = $(elem).attr('data-product-id');
            if ($(elem).attr('data-product-unit') == 'gram') {
                input_type = 'select';
                _options = parseInt(value / 250);
            } else {
                input_type = 'input';
            }
            var input = document.createElement(input_type);
            
            if (input_type === 'select') {
                var modifier = 10;
                if (_options > 10) modifier = 10
                for (var i = 0; i <= _options+modifier; i++) {
                    var o = document.createElement('option');
                        o.value = o.text = i * 250;
                        if (o.value == value) o.selected = true;
                        input.appendChild(o);
                }
            } else {
                input.type = 'text';
                input.value = value;
                input.maxLength = 4;
            }
            input.name = 'product_'+ id;
            var input = document.body.appendChild(input);
            $(elem).before(input);
            $(elem).hide();
        });
        
    }
    
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