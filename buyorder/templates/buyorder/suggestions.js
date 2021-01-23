    // once input dectected start autocomplete
    function suggestions() {
        //alert(this.id)
        full_id = this.id;
        str = full_id.toString();
        strarray = str.split("-");
        //alert(strarray[strarray.length - 1]);
        //alert(full_id);
        console.log(full_id)
        if (strarray[strarray.length - 1] === "product") {
            //alert("Searching")
            console.log(strarray[strarray.length - 1]);
            $("#" + full_id).autocomplete({
                source: "{% url 'warehouse:autocomplete_product' %}",
                response: function(event, ui) {
                if (!ui.content.length) {
                    var noResult = { value: "", label: "No data found" };
                    ui.content.push(noResult);
                }
                },
                select: function (e, ui) {
                    if (ui.item.value) {
                    //do stuff after user selected option from autocomplete
                    var url = $("#buyorderform").attr("data-types-url"); // get the url of the `load_types` warehouse view
                    var url_color = $("#buyorderform").attr("data-colors-url"); // get the url of the `load_colors` warehouse view
                    var url_price = $("#buyorderform").attr("data-price-url"); // get the url of the `load_price`                    warehouse view
                    var formid = strarray[strarray.length - 2];
                    var productId = ui.item.value//$(this).val(); // get the selected product ID from the HTML input
                    //console.log(ui.item.value)
                    //console.log(strarray[strarray.length - 2]) //
                    $.ajax({ // initialize an AJAX request
                    url: url, // set the url of the request (= localhost:8000/hr/ajax/load_types/)
                    data: {
                    'product': productId // add the product id to the GET parameters
                    },
                    success: function (data) { // `data` is the return of the `load_types` view function
                    $("#id_form-"+formid+"-type").html(data); // replace the contents of the type input with the data that came from the server
                    }
                    });

                    $.ajax({ // initialize an AJAX request
                    url: url_color, // set the url of the request (= localhost:8000/hr/ajax/load_types/)
                    data: {
                    'product': productId // add the product id to the GET parameters
                    },
                    success: function (data) { // `data` is the return of the `load_types` view function
                    $("#id_form-"+formid+"-color").html(data); // replace the contents of the type input with the data that came from the server
                    }
                    });

                     $.ajax({ // initialize an AJAX request
                     url: url_price, // set the url of the request (= localhost:8000/hr/ajax/load_types/)
                     data: {
                     'product': productId // add the product id to the GET parameters
                     },
                     success: function (data) { // `data` is the return of the `load_types` view function
                     $("#id_form-"+formid+"-price").val(data); // replace the contents of the type input with the data that came from the server
                     }
                     });

                }
                }
                
            });
        }
    }