window.addEventListener("load", () => {
    if (document.getElementById("logo")) { document.getElementById("logo").addEventListener("click", () => { location.href = "./index.html"; }) }

    $('input[name="datesingle"]').daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        singleDatePicker: true,
        locale: {
            format: "DD/MM/YYYY hh:mm"
        }
    });

    let value = parseInt($('input[name="value"]')[0].value.slice(1));
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
});
