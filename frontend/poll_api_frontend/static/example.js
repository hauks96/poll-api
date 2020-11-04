// Examples by Ægir M. Hauksson

$.ajax({
    url: "{% url 'doing-something' %}",
    headers: {'X-CSRFToken': csrftoken},
    data: {'some_attribute': some_value},
    type: "GET",
    dataType: 'json',
    success: function (data) {
        if (data) {
            console.log(data);
            // call function to do something with data
            process_data_function(data);
        }
    }
});

$.ajax({
    url: "{% url 'get-html' %}",
    headers: {'X-CSRFToken': csrftoken},
    data: {'search_input': search_input},
    type: "GET",
    dataType: 'html',
    success: function (data) {
    if (data) {
        /* You could also use json here to get multiple html to
        render in different places */
        console.log(data);
        // Add the http response to element
        target_element.html(data);
    }
}
});