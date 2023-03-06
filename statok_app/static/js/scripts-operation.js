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

function oppage_save() {
    Swal.fire({
        title: "Save operation",
        text: "Operation information successfully updated!",
        icon: "success",
    }).then((result) => {
        if (result.isConfirmed) {
            location.href='index.html'
        }
    });
}