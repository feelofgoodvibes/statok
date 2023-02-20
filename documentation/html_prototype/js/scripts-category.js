var operations_data;

window.addEventListener("load", () => {
    operations_data = [];

    $(".operations-list > .operation-item").each((i, operation) => {
        let curop = {
            "id": $(operation).find(".operation-id").text(),
            "value": parseFloat($(operation).find(".operation-value").text().slice(1)),
            "date": $(operation).find(".operation-date").text(),
            "category": $(operation).find(".operation-category").text()
        }
        
        operations_data.push(curop);
    });

    operations_data.reverse();
    renderChart();
});

function renderChart() {
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

    const BARS_AMOUNT = 20;
    const chart_ctx = $("#category-chart")[0];

    values_history = operations_data.map((o) => { return o.value });

    while (values_history.length < BARS_AMOUNT) { values_history.push(0); }
    values_history = values_history.slice(-BARS_AMOUNT);

    new Chart(chart_ctx, {
        type: "bar",
        data: {
            labels: values_history.map((item) => { return "$" + item }),
            datasets: [{
                label: "Values history",
                data: values_history,
                backgroundColor: 'rgba(117, 239, 127, 0.3)',
                borderColor: 'rgba(117, 239, 127, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: scales_options,
            responsive: true,
            maintainAspectRatio: false
        }

    });
}

function edit_category() {
    Swal.fire({
        title: "Edit category",
        input: "text",
        inputPlaceholder: "Category name",
        showCancelButton: true,
        confirmButtonText: "Save",
        confirmButtonColor: "#26923f",
        willOpen: () => {
            Swal.getInput().value = "Food";
        }
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Category saved!",
                icon: "success",
                confirmButtonColor: "#26923f"
            }).then(() => { location.reload(); })
        }
    });
}

function delete_category() {
    Swal.fire({
        title: "Delete category",
        text: "After deleting a category, all operations related to it will be transferred to the \"Other\" category. If you want to delete a category with all its operations, first use the \"Delete all\" option.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Delete category",
        confirmButtonColor: "#C11414",
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Category deleted!",
                icon: "success",
                confirmButtonColor: "#26923f"
            }).then(() => { location = 'index.html'; })
        }
    });
}

function delete_all_operations() {
    Swal.fire({
        title: "Delete all operations",
        text: "Are you sure you want to delete all operations within this category?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Delete all operations",
        confirmButtonColor: "#C11414",
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "All operations were deleted!",
                icon: "success",
                confirmButtonColor: "#26923f"
            }).then(() => { location = 'index.html'; })
        }
    });
}