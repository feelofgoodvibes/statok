var operations_data;

window.addEventListener("load", () => {
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
    const category_type = category_data.type;

    values_history = category_data.operations.map((o) => { return category_type == "EXPENSE" ? Math.abs(o.value) : o.value; });
    while (values_history.length < BARS_AMOUNT) { values_history.push(0); }
    values_history = values_history.slice(-BARS_AMOUNT);

    new Chart(chart_ctx, {
        type: "bar",
        data: {
            labels: values_history.map((item) => { return "$" + item }),
            datasets: [{
                label: "Values history",
                data: values_history,
                backgroundColor: category_type == "EXPENSE" ? 'rgba(241, 116, 143, 0.3)' : 'rgba(117, 239, 127, 0.3)',
                borderColor: category_type == "EXPENSE" ? 'rgba(241, 116, 143, 1)' : 'rgba(117, 239, 127, 1)',
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
            Swal.getInput().value = $("#category-name").text().slice(10);
        },

        preConfirm: (result) => {
            return $.ajax({
                url: "/api/v1/category/" + location.pathname.split("/")[2],
                method: "PUT",
                data: {"name": result},
                success: (response) => {
                    Swal.fire({
                        title: "Category edited!",
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.reload(); })
                }
            }).catch(response => {
                let erorr_msg = typeof response.responseJSON["error"] == "string" ?
                                response.responseJSON["error"] :
                                "Location: " + response.responseJSON["error"][0]["loc"] + ". Error: " + response.responseJSON["error"][0]["msg"];
                Swal.showValidationMessage(erorr_msg);
            });
        }
    });
}

function delete_category() {
    Swal.fire({
        title: "Delete category",
        text: "After deleting a category, all operations related to it will be transferred to the \"Other\" category. If you want to delete a category with all its operations, first use the \"Delete all operations\" option.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Delete category",
        confirmButtonColor: "#C11414",

        preConfirm: () => {
            $.ajax({
                url: "/api/v1/category/" + category_data.id,
                method: "DELETE",
                success: (response) => {
                    console.log(response);
                    Swal.fire({
                        title: `\"${response.name}\" category was successfully deleted!`,
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.href = "/category"; })
                }
            }).catch(response => {
                let erorr_msg = typeof response.responseJSON["error"] == "string" ?
                                response.responseJSON["error"] :
                                "Location: " + response.responseJSON["error"][0]["loc"] + ". Error: " + response.responseJSON["error"][0]["msg"];
                Swal.fire({
                    title: "Error occured!",
                    text: erorr_msg,
                    icon: "error",
                    confirmButtonColor: "#26923f"
                })
            });
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
            $.ajax({
                url: "/api/v1/category/" + category_data.id + "/operation",
                method: "DELETE",
                success: () => {
                    Swal.fire({
                        title: "Operations successfully deleted!",
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.reload(); });
                }
            })
        }
    });
}