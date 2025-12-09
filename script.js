const API_URL = "/signal";

async function generateSignal() {
    document.getElementById("result").innerHTML = "Loading...";

    // Read manual LTP from input box
    const manualLtp = document.getElementById("manualLtp").value;

    // Send manual LTP to backend
    const res = await fetch(API_URL + "?ltp=" + manualLtp);
    const data = await res.json();

    document.getElementById("result").innerHTML =
        "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
}
