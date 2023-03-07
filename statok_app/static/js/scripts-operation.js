window.addEventListener("load", () => {
    $('input[name="datesingle"]').daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        singleDatePicker: true,
        timePickerSeconds: true,
        locale: {
            format: "YYYY-MM-DD HH:mm:ss"
        },
        startDate: operation_data.date
    });

    let value = parseInt($('input[name="value"]')[0].value);
    $('input[name="value"]').addClass(value >= 0 ? "money-pos" : "money-neg");
    $('input[name="value"]').on("input", (event) => {
        if (event.target.value === "-") return;
        if (event.target.value.length != 1 && event.target.value.slice(-1) == ".") return;


        if (isNaN(parseFloat(event.target.value))) {
            event.target.value = "";
        }

        event.target.value = isNaN(parseFloat(event.target.value)) ? "" : parseFloat(event.target.value);

        if (parseFloat(event.target.value) <= 0) {
            event.target.classList.remove("money-pos");
            event.target.classList.add("money-neg");
        }
        else {
            event.target.classList.remove("money-neg");
            event.target.classList.add("money-pos");
        }
    });

    // Load categories list
    let category_select = $("#category-select");

    load_categories_list(operation_data.category.type).then((response) => {
        for (let key in response){
            category_select.append($("<option>", {
                value: response[key].id,
                text: response[key].name
            }));
        }
        category_select[0].value = operation_data.category.id;
    });
});

function oppage_delete() {
    Swal.fire({
        title: `Delete operation №${operation_data.id}`,
        text: "Are you sure you want to delete this operation?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DC3545",
        confirmButtonText: "Yes, delete",
        cancelButtonColor: "#414141",

        preConfirm: (result) => {
            $.ajax({
                url: "/api/v1/operation/" + operation_data.id,
                method: "DELETE",
                success: (response) => {
                    Swal.fire({
                        title: `Operation №${operation_data.id} was successfully deleted!`,
                        icon: "success",
                        confirmButtonColor: "#26923f"
                    }).then(() => { location.href = "/"; })
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
                });
            });
        }
    });
}

function oppage_save() {
    let new_value = $("input[name='value']").val();
    let new_date = $("input[name='datesingle']").data('daterangepicker').startDate.format("YYYY-MM-DD HH:mm:ss");
    let new_category = $("#category-select").val();

    $.ajax({
        url: "/api/v1/operation/" + operation_data.id,
        method: "PUT",
        data: {"value": new_value, "date": new_date, "category_id": new_category},
        success: (response) => {
            Swal.fire({
                title: `Operation №${operation_data.id} was successfully updated!`,
                icon: "success",
                confirmButtonColor: "#26923f"
            }).then(() => { location.reload(); })
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
        });
    });
}