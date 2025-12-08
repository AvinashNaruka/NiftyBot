document.getElementById("fetchBtn").addEventListener("click", fetchSignal);

async function fetchSignal() {
    const loader = document.getElementById("loader");
    const box = document.getElementById("signalBox");

    loader.classList.remove("hidden");
    box.classList.add("hidden");

    try {
        const res = await fetch("https://niftybot-htwt.onrender.com/signal");
        const data = await res.json();

        loader.classList.add("hidden");

        if (data.error) {
            alert("API Error: " + data.message);
            return;
        }

        // Fill Data
        document.getElementById("trend").textContent = data.trend;
        document.getElementById("ltp").textContent = data.nifty_ltp;
        document.getElementById("strike").textContent = data.strike;
        document.getElementById("otype").textContent = data.option_type;

        document.getElementById("premium").textContent = data.entry_premium;
        document.getElementById("sl").textContent = data.stoploss;
        document.getElementById("targets").textContent = data.targets.join(" / ");

        // Trend Color
        let t = data.trend;
        let tspan = document.getElementById("trend");

        if (t === "UP") tspan.className = "up";
        else if (t === "DOWN") tspan.className = "down";
        else tspan.className = "side";

        box.classList.remove("hidden");

    } catch (error) {
        loader.classList.add("hidden");
        alert("Network Error!");
    }
}
