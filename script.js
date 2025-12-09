document.getElementById("genBtn").addEventListener("click", async () => {
    let box = document.getElementById("resultBox");
    box.innerHTML = "Loading...";

    let manual = document.getElementById("manualLtp").value.trim();

    try {
        let url = "https://niftybot-htwt.onrender.com/signal";

        if (manual !== "") {
            url += "?ltp=" + manual;
        }

        let res = await fetch(url);
        let data = await res.json();

        if (data.error) {
            box.innerHTML = "<b>Error:</b> " + data.error;
            return;
        }

        box.innerHTML = `
            <h3>Trade Signal</h3>
            <b>Trend:</b> ${data.trend} <br>
            <b>NIFTY LTP:</b> ${data.ltp} <br>
            <b>Strike:</b> ${data.strike} <br>
            <b>Option Type:</b> ${data.option_type} <br>
            <b>Expiry:</b> ${data.expiry} <br>
            <b>Entry Premium (Est):</b> ${data.entry_premium_est} <br>
            <b>Stoploss:</b> ${data.stoploss} <br>
            <b>Targets:</b> ${data.targets.join(", ")} <br>
            <b>Confidence:</b> ${(data.confidence * 100).toFixed(1)}% <br>
            <b>Notes:</b> ${data.notes}
        `;
        
    } catch (e) {
        box.innerHTML = "Network error: " + e;
    }
});
