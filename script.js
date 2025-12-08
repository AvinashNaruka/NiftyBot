// ---------------------------
//  FIXED SCRIPT.JS
// ---------------------------

const btn = document.getElementById("generateBtn");
const loader = document.getElementById("loader");

const trendEl = document.getElementById("trend");
const ltpEl = document.getElementById("nifty_ltp");
const strikeEl = document.getElementById("strike");
const typeEl = document.getElementById("option_type");
const entryEl = document.getElementById("entry");
const slEl = document.getElementById("sl");
const tgtEl = document.getElementById("tgt");

// Render backend URL
const API_URL = "https://niftybot-htwt.onrender.com/signal";

btn.addEventListener("click", () => {
    generateSignal();
});

async function generateSignal() {

    loader.style.display = "block";
    btn.disabled = true;

    // timeout controller (Render wake-up takes 30–60 sec)
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 90000); // 90 sec

    try {
        const res = await fetch(API_URL, {
            method: "GET",
            signal: controller.signal,
        });

        clearTimeout(timeout);

        if (!res.ok) {
            throw new Error("Server response not OK");
        }

        const data = await res.json();

        // ❗ If backend sends error
        if (data.error) {
            alert("Server Error: " + data.error);
            return;
        }

        // ------------------------
        // UPDATE UI FIELDS
        // ------------------------
        trendEl.textContent = data.trend || "—";
        ltpEl.textContent = data.ltp || "—";
        strikeEl.textContent = data.strike || "—";
        typeEl.textContent = data.option_type || "—";

        entryEl.textContent = data.entry || "—";
        slEl.textContent = data.sl || "—";
        tgtEl.textContent = data.tgt || "—";

    } ca
