$(document).ready(function () {
    $("#branch_div").hide();
    $(".pay_fee_button").hide();

    // If any checkbox is not selected then set Total Amount to zero
    $("#id_amount").val(0);

    // Set value of Total Amount on load
    var checkboxes = $('div.checkbox-group.required :checkbox:checked')
    if (checkboxes.length > 0){
        var total = 0
        for (i = 0; i < checkboxes.length; i++) { 
            total = total + parseInt(checkboxes[i].value.split('_')[1]);
        }
        $("#id_amount").val(total);
        $(".pay_fee_button").show();
    }
    else{
        $("#id_amount").val(0);
        $(".pay_fee_button").hide();
    }

    // Style default razorpay button
    $(".razorpay-payment-button").addClass('btn btn-primary text-center');
    $(".razorpay-payment-button").val('Confirm Pay');

    // Dynamically loads branch based on institute
    $("#id_inst").change(function () {
        $("#branch_div").show();
        $.ajax({
            type: "POST",
            url: '/branch_list/',
            data: {
                'branch_id': $("#" +this.id+ " option:selected").attr('value')
            },
            dataType: 'json',
            success: function(response){
                $('#id_branch').find('option').remove();
                $.each( response, function( key, value ) {
                    $("#id_branch").append(new Option(value, key));
                });
            },
            error: function(response){
                // debugger
            }
        });
    });

    // Update value of Total Amount based on checked checkboxes 
    $(".check_input").click(function () {
        var checkboxes = $('div.checkbox-group.required :checkbox:checked')
        if (checkboxes.length > 0){
            var total = 0
            for (i = 0; i < checkboxes.length; i++) { 
                total = total + parseInt(checkboxes[i].value.split('_')[1]);
            }
            $("#id_amount").val(total);
            $(".pay_fee_button").show();
        }
        else{
            $("#id_amount").val(0);
            $(".pay_fee_button").hide();
        }
    });

    $('#payment_form').submit(function(){
        var checkboxes = $('div.checkbox-group.required :checkbox:checked')
        if (checkboxes.length > 0){
            var c_ids = [];
            for (i = 0; i < checkboxes.length; i++) { 
                c_ids.push(checkboxes[i].value.split('_')[0]);
            }
        return true;
        } else {
        return false;
        }
    });

});