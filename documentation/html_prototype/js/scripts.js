window.addEventListener("load", () => {
    let logoel = document.getElementById("logo");

    if (logoel){
        logoel.addEventListener("click", () => { location.href = "./index.html"; })
    }

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
});

function formClick() {
    console.log($("#filter-daterange").val());
}

function delF(element) {
    console.log(element);

    swal({
            text: "Are you sure you want to delete this item?",
            buttons: ["Cancel", "Yes"],
            icon: "warning",
            dangerMode: true
        });
}