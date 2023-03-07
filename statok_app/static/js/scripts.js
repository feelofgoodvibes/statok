window.addEventListener("load", () => {
    if (document.getElementById("logo")) { document.getElementById("logo").addEventListener("click", () => { location.href = "/"; }) }

    $("#btn-filters").accordion({
        active: false,
        collapsible: true
    });


    // Setting up filters
    // Datetime
    let url_params = new URLSearchParams(window.location.search);
    let fStartDate; let fEndDate;

    try {
        fStartDate = url_params.get("date_from") == null ? operations_data[operations_data.length-1].date : url_params.get("date_from");
        fEndDate = url_params.get("date_to") == null ? operations_data[0].date : url_params.get("date_to");
    }
    catch {
        fStartDate = false;
        fEndDate = false;
    }

    $('input[name="daterange"]').daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        timePickerSeconds: true,
        startDate: fStartDate,
        endDate: fEndDate,
        locale: {
            format: "YYYY-MM-DD HH:mm:ss"
        }
    });

    // Type
    if ($("input[name='operationtype'][value=" + url_params.get("type") + "]")[0]){
        $("input[name='operationtype'][value=" + url_params.get("type") + "]")[0].checked = true;
    }

    if ($("#total-money-value")[0]){
        // Render total money
        let total = 0;
        operations_data.forEach(operation => {
            total += operation.value
        });
    
        if (total >= 0){
            total_text = "$" + parseFloat(Number(total).toFixed(2));
            $("#total-money-value").addClass("money-pos");
        }
        else {
            total_text = "-$" + Math.abs(parseFloat(Number(total).toFixed(2)));
            $("#total-money-value").addClass("money-neg");
        }
    
        $("#total-money-value").text(total_text);
    
        // Charts
        renderCharts();
    }
});

function applyFilters() {
    operation_type = parseInt($("input[name='operationtype']:checked")[0].value);
    date_from = $("#filter-daterange").data('daterangepicker').startDate.format("YYYY-MM-DD HH:mm:ss");
    date_to = $("#filter-daterange").data('daterangepicker').endDate.format("YYYY-MM-DD HH:mm:ss");

    url_with_filters = location.origin + location.pathname + "?";

    if (operation_type != 0) {
        url_with_filters += "type=" + operation_type + "&";
    }

    url_with_filters += "date_from=" + date_from + "&date_to=" + date_to;

    location.href = url_with_filters;
}

function clearFilters() {
    location.href = location.origin + location.pathname;
}

function operationDelete(element) {
    let operation_id = parseInt(element.getAttribute("data-opid"));

    Swal.fire({
        title: "Delete operation №" + operation_id,
        text: "Are you sure you want to delete this operation?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DC3545",
        confirmButtonText: "Yes, delete",
        cancelButtonColor: "#414141"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: "/api/v1/operation/" + operation_id,
                method: "DELETE",
                success: (response) => {
                    Swal.fire({
                        title: `Operation №${response.id} was successfully deleted!`,
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.reload(); })
                },
                error: (response) => {
                    Swal.fire({
                        title: "Error occured!",
                        icon: "error",
                        confirmButtonColor: "#26923f"
                    });
                }
            });
        }
    });
}

function renderCharts() {
    const BARS_AMOUNT = 10;

    // Total budget pie -------------------------------
    const ctx_pie = $("#total-budget-pie")[0];

    let total_incomes = 0;
    let total_expenses = 0;

    operations_data.forEach(operation => {
        if (operation.value >= 0){
            total_incomes += operation.value
        }
        else {
            total_expenses += operation.value
        }
    });

    new Chart(ctx_pie, {
        type: "doughnut",
        data: {
            labels: ["Incomes", "Expenses"],
            datasets: [{
                data: [total_incomes, total_expenses],
                backgroundColor: [
                    'hsl(125, 79%, 70%)',
                    'hsl(347, 82%, 70%)'
                ],
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true
        }
    });

    // Balance history -------------------------------
    scales_options = {
        x: {
            ticks: { display: false },
            grid: { display: false },
            border: { display: false }},
        y: {
            ticks: { display: false },
            grid: { display: false },
            border: { display: false }
        }
    }

    const ctx_balance = $("#balance-history-chart")[0];

    let balance_history = [];
    let curbal = 0;

    operations_data.reverse().forEach(operation => {
        curbal += operation.value;
        balance_history.push(parseFloat(Number(curbal).toFixed(2)));
    });

    while (balance_history.length < BARS_AMOUNT) { balance_history.push(0); }
    balance_history = balance_history.slice(-BARS_AMOUNT);

    new Chart(ctx_balance, {
        type: "bar",
        data: {
            labels: balance_history.map((item) => {return "$" + item}),
            datasets: [{
                label: 'Balance history',
                data: balance_history,
                backgroundColor: 'rgba(116, 190, 237, 0.3)',
                borderColor: 'rgba(116, 190, 237, 1)',
                borderWidth: 1
              }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: scales_options,
            responsive: true
        }
    });

    // Latest incomes --------------------
    const ctx_incomes = $("#latest-incomes-chart")[0];

    let latest_incomes = [];
    let latest_expenses = [];

    operations_data.forEach(operation => {
        if (operation.value >= 0){
            latest_incomes.push(operation.value);
        }
        else {
            latest_expenses.push(Math.abs(operation.value));
        }
    });

    while (latest_incomes.length < BARS_AMOUNT) { latest_incomes.push(0); }
    while (latest_expenses.length < BARS_AMOUNT) { latest_expenses.push(0); }
    latest_incomes = latest_incomes.slice(-BARS_AMOUNT);
    latest_expenses = latest_expenses.slice(-BARS_AMOUNT);

    new Chart(ctx_incomes, {
        type: "bar",
        data: {
            labels: latest_incomes.map((item) => {return "$" + item}),
            datasets: [{
                label: 'Latest incomes',
                data: latest_incomes,
                backgroundColor: 'rgba(117, 239, 127, 0.3)',
                borderColor: 'rgba(117, 239, 127, 1)',
                borderWidth: 1
              }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: scales_options,
            responsive: true
        }
    });

    // Latest expenses --------------------
    const ctx_expenses = $("#latest-expenses-chart")[0];

    new Chart(ctx_expenses, {
        type: "bar",
        data: {
            labels: latest_expenses.map((item) => {return "-$" + item}),
            datasets: [{
                label: 'Latest expenses',
                data: latest_expenses,
                backgroundColor: 'rgba(241, 116, 143, 0.3)',
                borderColor: 'rgba(241, 116, 143, 1)',
                borderWidth: 1
              }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: scales_options,
            responsive: true
        }
    });
}

function operationEdit(el) {
    location.href = "/operation/"+el.getAttribute("data-opid");
}

function add_operation(type) {
    Swal.fire({
        title: "Add " + type + " operation",
        text: "Enter operation value",
        html:
            '<div class="c-swal2-container">' +
                '<span class="c-swal2-inputlabel">Value</span>' +
                '<input id="swal-input-value" class="c-swal2-input">' +
                '<span class="c-swal2-inputlabel">Category</span>' +
                '<select id="swal-select-category" class="c-swal2-input"></select>' +
            '</div>',
        showCancelButton: true,
        confirmButtonText: "Add",
        confirmButtonColor: "#26923f",
        willOpen: () => {
            load_categories_list(type).then((response) => {
                $("#swal-input-value")[0].addEventListener("input", (event) => {value_validator(event, "pos")})

                for (let index in response){
                    $("#swal-select-category")[0].appendChild($("<option>", {"text": response[index].name, "value": response[index].id})[0]);
                }
            });
        },

        preConfirm: () => {
            let operation_value = $("#swal-input-value")[0].value;
            let operation_category = $("#swal-select-category")[0].value;

            if (operation_value == "" || isNaN(Number(operation_value))){
                Swal.showValidationMessage("Incorrect value!");
            }

            else {
                $.post({
                    url: "/api/v1/operation",
                    data: {"value": operation_value, "category_id": operation_category}
    
                })
                .done((response) => {
                    Swal.fire({
                        title: "Operation added successfully!",
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.reload(); });
                })
                .fail ((response) => {
                    let erorr_msg;

                    if (typeof response.responseJSON["error"] == "string"){
                        erorr_msg = response.responseJSON["error"];
                    }

                    else {    
                        erorr_msg = "Location: " + response.responseJSON["error"][0]["loc"] + ". Error: " + response.responseJSON["error"][0]["msg"];
                    }

                    Swal.fire({
                        title: "Error occured!",
                        text: erorr_msg,
                        icon: "error",
                        confirmButtonColor: "#26923f"
                    });
                });
            }
        }
    });
}

function add_category(type) {
    Swal.fire({
        title: "Add " + type + " category",
        input: "text",
        inputPlaceholder: "Name of the category",
        showCancelButton: true,
        confirmButtonText: "Add",
        confirmButtonColor: "#26923f",

        preConfirm: (result) => {
            if (result.value == ""){
                Swal.showValidationMessage("Incorrect value!");
            }
        }

    }).then((result) => {
        if (!result.isConfirmed) return;
        
        let category_name = result.value;
        let type_as_int = type.toLowerCase() == "income" ? 1 : 2;

        $.post({
            url: "/api/v1/category",
            data: {"name": category_name, "type": type_as_int}
        })
        .done((response) => {
            Swal.fire({
                title: "Category added successfully!",
                icon: "success",
                confirmButtonColor: "#26923f"
            }).then(() => { location.reload(); });
        })
        .fail ((response) => {
            let erorr_msg;

            if (typeof response.responseJSON["error"] == "string"){
                erorr_msg = response.responseJSON["error"];
            }

            else {    
                erorr_msg = "Location: " + response.responseJSON["error"][0]["loc"] + ". Error: " + response.responseJSON["error"][0]["msg"];
            }

            Swal.fire({
                title: "Error occured!",
                text: erorr_msg,
                icon: "error",
                confirmButtonColor: "#26923f"
            });
        });
    });
}

function load_categories_list(type) {
    let type_as_int = type.toLowerCase() == "income" ? 1 : 2;
    return $.get({
        url: "/api/v1/category?type="+type_as_int,

    });
}

function value_validator(value, type=null){
}