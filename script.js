document.getElementById("genBtn").addEventListener("click", async () => {
    let box = document.getElementById("resultBox");
    box.innerHTML = "Loading...";

    let manual = document.getElementById("manualLtp").value.trim();

    try {
        let res = await fetch("https://niftybot-htwt.onrender.com/signal?ltp=" + manual);
        let data = await res.json();

        if (data.error) {
            box.innerHTML = data.error;
            return;
        }

        box.innerHTML = `
            <div><b>Trend:</b> ${data.trend}</div>
            <div><b>LTP:</b> ${data.ltp}</div>
            <div><b>Strike:</b> ${data.strike}</div>
            <div><b>Type:</b> ${data.option_type}</div>
            <div><b>Entry Premium:</b> ${data.entry_premium_est}</div>
            <div><b>SL:</b> ${data.stoploss}</div>
            <div><b>Targets:</b> ${data.targets.join(", ")}</div>
        `;
        
    } catch (e) {
        box.innerHTML = "Network error: " + e;
    }
});
