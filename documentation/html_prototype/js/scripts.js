window.addEventListener("load", () => {
    if (document.getElementById("logo")) { document.getElementById("logo").addEventListener("click", () => { location.href = "./index.html"; }) }

    $("#btn-filters").accordion({
        active: false,
        collapsible: true
    });

    $("#jquery-del-dialog").dialog({
        autoOpen: false,
        buttons: [
            {
                text: "Yes, delete"
            }
        ]
    });

    $('input[name="daterange"]').daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        locale: {
            format: "DD/MM/YYYY hh:mm"
        }
    });

    // Render total money
    let total = 0;
    operations_data.forEach(operation => {
        total += operation.value
    });

    if (total >= 0){
        total_text = "$" + total;
        $("#total-money-value").addClass("money-pos");
    }
    else {
        total_text = "-$" + Math.abs(total);
        $("#total-money-value").addClass("money-neg");
    }

    $("#total-money-value").text(total_text);

    // Charts
    renderCharts();
});

function formClick() {
    console.log($("#filter-daterange").val());
}

function delete_operation(element) {
    Swal.fire({
        title: "Delete operation",
        text: "Are you sure you want to delete this operation?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DC3545",
        confirmButtonText: "Yes, delete",
        cancelButtonColor: "#414141"
    }).then((result) => {
        if (result.isConfirmed) {
            location.href='index.html'
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

    operations_data.forEach(operation => {
        curbal += operation.value;
        balance_history.push(curbal);
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
    location.href = "operation.html";
}

function add_operation(type) {
    Swal.fire({
        title: "Add " + type + " operation",
        text: "Enter operation value",
        html: 
            '<input id="swal-input-value" class="swal2-input" placeholder="Value">' +
            '<select id="swal-select-category" class="swal2-input"></select>',
        showCancelButton: true,
        confirmButtonText: "Add",
        confirmButtonColor: "#26923f",
        willOpen: () => {
            $("#swal-select-category")[0].appendChild($("<option>", {"text": "Food", "value": "Food"})[0]);
            $("#swal-select-category")[0].appendChild($("<option>", {"text": "Restaurant", "value": "Restaurant"})[0]);
            $("#swal-select-category")[0].appendChild($("<option>", {"text": "Transaction", "value": "Transaction"})[0]);
            $("#swal-select-category")[0].appendChild($("<option>", {"text": "Store", "value": "Store"})[0]);
            $("#swal-select-category")[0].appendChild($("<option>", {"text": "Taxi", "value": "Taxi"})[0]);
        }
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Operation added successfully!",
                icon: "success",
                confirmButtonColor: "#26923f",
            })
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
        confirmButtonColor: "#26923f"
    }).then((result) => {
        if (result.isConfirmed){
            Swal.fire({
                title: "Category added!",
                icon: "success",
                confirmButtonColor: "#26923f"

            }).then(() => { location = "categories.html"; });
        }
    });
}