document.addEventListener("DOMContentLoaded", () => {
  // Quantity Elements
  const quantityEl = document.getElementById("quantity");
  const customQuantityEl = document.getElementById("custom-quantity");
  const finalQuantityEl = document.getElementById("final-quantity");

  // State
  const selectedToppings = new Set();
  let selectedDrinkId = null;

  // Add hidden inputs for selected options
  const form = document.querySelector("form");
  const sizeInput = document.querySelector("input#size");

  const toppingsInput = document.createElement("input");
  toppingsInput.type = "hidden";
  toppingsInput.name = "extra-toppings";
  toppingsInput.id = "extra-toppings";
  form.appendChild(toppingsInput);

  const drinkInput = document.createElement("input");
  drinkInput.type = "hidden";
  drinkInput.name = "drink-id";
  drinkInput.id = "drink-id";
  form.appendChild(drinkInput);

  // Handle Quantity Display
  function syncFinalQuantity() {
    finalQuantityEl.value = quantityEl.innerText;
  }

  quantityEl.addEventListener("click", () => {
    customQuantityEl.value = quantityEl.innerText;
    quantityEl.classList.add("hidden");
    customQuantityEl.classList.remove("hidden");
    customQuantityEl.focus();
  });

  customQuantityEl.addEventListener("change", () => {
    const newVal = parseInt(customQuantityEl.value);
    if (!isNaN(newVal) && newVal >= 1) {
      quantityEl.innerText = newVal;
    }
    customQuantityEl.classList.add("hidden");
    quantityEl.classList.remove("hidden");
    syncFinalQuantity();
  });

  document.getElementById("sub").addEventListener("click", () => {
    const qty = Math.max(1, parseInt(quantityEl.innerText) - 1);
    quantityEl.innerText = qty;
    syncFinalQuantity();
  });

  document.getElementById("add").addEventListener("click", () => {
    const qty = parseInt(quantityEl.innerText) + 1;
    quantityEl.innerText = qty;
    syncFinalQuantity();
  });

  // Select Size
  document.querySelectorAll("[id^='size-']").forEach((btn) => {
    btn.addEventListener("click", () => {
      sizeInput.value = btn.dataset.id;

      // Highlight selected
      document.querySelectorAll("[id^='size-']").forEach((b) => {
        b.classList.remove("border-[var(--color-pink)]");
        b.classList.add("border-gray-300");
      });
      btn.classList.add("border-[var(--color-pink)]");
      btn.classList.remove("border-gray-300");
    });
  });

  // default size is medium
  const defaultBtn = document.querySelector('[id="size-medium"]');
  if (defaultBtn) {
    defaultBtn.click();
  }

  // Select Toppings
  document.querySelectorAll("[id^='extra-topping-']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const toppingId = btn.dataset.id;

      if (selectedToppings.has(toppingId)) {
        selectedToppings.delete(toppingId);
        btn.classList.remove("border-[var(--color-pink)]");
        btn.classList.add("border-gray-300");
      } else {
        selectedToppings.add(toppingId);
        btn.classList.add("border-[var(--color-pink)]");
        btn.classList.remove("border-gray-300");
      }

      toppingsInput.value = Array.from(selectedToppings).join(",");
    });
  });

  // Select Drink
  document.querySelectorAll(".add-a-drink button").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectedDrinkId = btn.id;
      drinkInput.value = selectedDrinkId;

      // Deselect all others
      document.querySelectorAll(".add-a-drink button").forEach((b) => {
        b.classList.remove("border-[var(--color-pink)]", "ring-2");
      });
      btn.classList.add("border-[var(--color-pink)]", "ring-2");
    });
  });
});
