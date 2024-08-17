(function($) {
    $(function() {
        var companySelect = $('#id_company');
        var orderSelect = $('#id_order');

        function updateOrders() {
            var companyId = companySelect.val();
            if (companyId) {
                $.ajax({
                    type: 'POST',
                    url: '/get_orders_for_company/',
                    data: {
                        'company_id': companyId,
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function(data) {
                        console.log("Orders updated");
                        orderSelect.html(data);
                    }
                });
            } else {
                orderSelect.html('');
            }
        }

        companySelect.change(updateOrders);
        updateOrders();
    });
})(jQuery); // Changed from django.jQuery to jQuery
