(function ($) {
    
    var delivery_method = $("#delivery_method"),
        delivery_method_options = $("#delivery_method_options"),
        select_delivery_area = $("#select_delivery_area"),
        delivery_city = $("#delivery_city"),
        delivery_area = $("#delivery_area"),
        price_total = $(".total"),
        total_price = $("#total_price"),
        delivery_fee = $("#delivery_fee"),
        current_fee = 0.00,
        price_pickup = 0.00,
        price_hu = 1200.00,
        price_bud = 800.00;
    
    var total = $(price_total).attr("data-total-price");
    var method = $("input[name='delivery_method']:checked");
    
    
    if ( $(delivery_area).val() != "" ) {
        $(select_delivery_area).val($(delivery_area).val())
    }
    
    $(delivery_method).delegate("input", "change", function (event) {
        delivery_method_options[0].className = event.target.value;
        calculatePrice()
    });
    
    $(delivery_method_options).delegate("select", "change", function (event) {
        var value = event.target.value;
        $(delivery_area).val(value);
        calculatePrice()
    });
    
    function calculatePrice () {
        var price = 0,
            method_val = $("input[name='delivery_method']:checked").val(),
            delivery_val = $("#select_delivery_area").val();
        if ( method_val == 'pickup' ) {
            price = total - total / 10;
            current_fee = price_pickup;
        } else if ( method_val == 'box' ) {
            
            if ( delivery_val == "Hungary" ) {
                current_fee = price_hu;
                price = parseFloat(total) + parseFloat(price_hu);
            } else if ( delivery_val != "" ) {
                current_fee = price_bud;
                price = parseFloat(total) + parseFloat(price_bud);
            } else {
                price = parseFloat(total);
                current_fee = price_pickup;
            }
            
        } else {
            price = parseFloat(total);
        }

        updatePrice(price);
    };
    
    function updateFee () {
        $(delivery_fee).text(current_fee)
    };
    
    function updatePrice (price) {
        updateFee();
        var price = price.toFixed(2);
        $(total_price).text(price)
    };
    
    function formatPrice () {
        
    }
    
    //console.log($(price_total).attr("data-total-price"))
    
    calculatePrice();
    
})(jQuery);