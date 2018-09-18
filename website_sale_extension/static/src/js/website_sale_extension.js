odoo.define('website_sale_extension.website_sale', function (require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');
    // var base = require("web_editor.base");
    // var utils = require('web.utils');

    if (!$('.oe_website_sale').length) {
        return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
    }

    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (event) {
            var product_id = $('input[name="product_id"]').val();
            if(product_id == localStorage.getItem('bom_id')) {
                $('div.o_wse_bom_selector').html(localStorage.getItem('bom_cart'));
                update_bom_cart();
            } else {
                ajax.jsonRpc("/shop/product/get_product_bom", 'call', {
                    'product_id': parseInt(product_id),
                }).then(function (res) {
                    $('div.o_wse_bom_selector').html(res);
                    update_bom_cart();
                    localStorage.setItem('bom_id', product_id)
                    localStorage.setItem('bom_cart', $('div.o_wse_bom_selector').html());
                });
            }
        });


        $(oe_website_sale).on('click', 'div.o_wse_bom_selector summary', function (event) {
            if ($(this).attr('selectable') == 'True') {
                $(this).toggleClass('o_wse_bom_selected');
                update_bom_cart();
            }
        });


        $(oe_website_sale).on('click', 'span.o_wse_bom_cart_item a', function (event) {
            var id = $(this).data('item_id');
            $('summary.o_wse_bom_selected[data-id="' + id +'"]').trigger('click');
        });


        function update_bom_cart() {
            var $o_wse_bom_selector_cart = $('div.o_wse_bom_selector_cart');
            var product_price = parseFloat($o_wse_bom_selector_cart.data('unit_price'));
            var input_qty = parseInt($('input[name="add_qty"]').val() || 1);
            var item_price = 0.0;
            var bom_line_ids = [];
            $o_wse_bom_selector_cart.html('');
            $('summary.o_wse_bom_selected').each(function() {
                var line_id = parseInt($(this).data('id'));
                var style = "display: " + ($(this).prop('hidden')? "none" : "block");
                var item = '<span class="o_wse_bom_cart_item" style="' + style + '" > ' + $(this).data("name") + ' <a class="far fa fa-times-circle" data-item_id="' + line_id +'"></a></span>';
                $o_wse_bom_selector_cart.append(item);
                item_price += parseFloat($(this).data('price'));
                bom_line_ids.push(line_id);
            });
            $('input.o_wse_bom_line_ids').val(bom_line_ids);
            $('span.oe_currency_value').each(function() {
                $(this).html((product_price + item_price) * input_qty);
            });
            localStorage.setItem('bom_cart', $('div.o_wse_bom_selector').html());
        };

    });

});
