(function($) {
    $(function() {
        var companySelect = $('#id_company');
        var productSelect = $('#id_product');

        function updateProducts() {
            var companyId = companySelect.val();
            if (companyId) {
                $.ajax({
                    type: 'POST',
                    url: '/get_products_for_company/',
                    data: {
                        'company_id': companyId,
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function(data) {
                        console.log("Products updated");
                        productSelect.html(data);
                    }
                });
            } else {
                productSelect.html('');
            }
        }

        companySelect.change(updateProducts);
        updateProducts();
    });
})(jQuery); // Changed from django.jQuery to jQuery
