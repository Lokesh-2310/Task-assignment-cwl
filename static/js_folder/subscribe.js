// -----------------------------
// APPLY PROMO CODE
// -----------------------------
function applyPromo() {
    const promoInput = document.getElementById("promoInput");
    const promoMessage = document.getElementById("promoMessage");
    const subscribeBtn = document.getElementById("subscribeBtn");
    const priceDisplay = document.getElementById("priceDisplay");
    const promoCodeHidden = document.getElementById("promoCodeHidden");

    const enteredCode = promoInput.value.trim().toUpperCase();

    // The valid promo code
    const validPromo = "BFSALE25";

    // Reset message first
    promoMessage.innerHTML = "";
    promoMessage.style.display = "none";

    // -----------------------------
    // CHECK PROMO CODE
    // -----------------------------
    if (enteredCode === "") {
        promoMessage.style.display = "block";
        promoMessage.style.color = "#ff3d3d";
        promoMessage.innerHTML = "<i class='fas fa-times-circle'></i> Please enter a promo code.";
        return;
    }

    if (enteredCode !== validPromo) {
        promoMessage.style.display = "block";
        promoMessage.style.color = "#ff3d3d";
        promoMessage.innerHTML = "<i class='fas fa-times-circle'></i> Invalid promo code!";
        return;
    }

    // -----------------------------
    // VALID PROMO APPLIED
    // -----------------------------
    promoMessage.style.display = "block";
    promoMessage.style.color = "#4cff4c";
    promoMessage.innerHTML = "<i class='fas fa-check-circle'></i> Promo code applied successfully!";

    // Store promo to send with form
    promoCodeHidden.value = enteredCode;

    // Extract original price (shown in HTML)
    let originalPrice = parseInt(
        priceDisplay.querySelector(".full-price")?.innerText.replace("$", "") ||
        priceDisplay.querySelector(".discounted")?.innerText.replace("$", "")
    );

    // Calculate 50% OFF
    let discountedPrice = Math.floor(originalPrice * 0.5);

    // Update price display UI
    priceDisplay.innerHTML = `
        <span class="original">${originalPrice}</span>
        <span class="discounted">${discountedPrice}</span>
        <span class="discount-badge">50% OFF</span>
    `;

    // Enable Subscribe Button & Update text
    subscribeBtn.disabled = false;
    subscribeBtn.innerHTML = `<i class="fas fa-credit-card"></i> Subscribe for ${discountedPrice}`;

    // Optional: Disable further promo edits
    promoInput.disabled = true;
}


// -----------------------------
// PREVENT FORM SUBMISSION WITHOUT PROMO IF DISABLED
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
    const subscribeBtn = document.getElementById("subscribeBtn");

    if (subscribeBtn) {
        subscribeBtn.addEventListener("click", (event) => {
            if (subscribeBtn.disabled) {
                event.preventDefault();
            }
        });
    }
});
