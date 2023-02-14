window.addEventListener("load", () => {
    let logoel = document.getElementById("logo");

    if (logoel){
        logoel.addEventListener("click", () => { location.href = "/"; })
    }

    $("#btn-filters").accordion({
        active: false,
        collapsible: true
    });

    $('input[name="daterange"]').daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        locale: {
            format: "DD/MM/YYYY hh:mm"
        }
    });
});

function formClick() {
    console.log($("#filter-daterange").val());
}