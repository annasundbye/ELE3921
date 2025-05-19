document.addEventListener("DOMContentLoaded", () => {
  // quantity
  const quantity = document.getElementById("quantity");
  const customQuantity = document.getElementById("custom-quantity");
  const finalQuantity = document.getElementById("final-quantity");

  // toppings
  const toppingElements = document.querySelectorAll(".topping-option");
  const extraToppingsInput = document.getElementById("extra-toppings");
  const selectedToppings = new Set();

  toppingElements.forEach((el) => {
    el.addEventListener("click", () => {
      const toppingId = el.dataset.id;

      if (selectedToppings.has(toppingId)) {
        selectedToppings.delete(toppingId);
        el.innerHTML = el.innerHTML.replaceAll("✅", "");
      } else {
        selectedToppings.add(toppingId);

        // TODO: remove toppings
        el.innerHTML += "✅";
      }

      extraToppingsInput.value = Array.from(selectedToppings).join(",");
    });
  });

  function syncFinalQuantity() {
    finalQuantity.value = quantity.innerText;
  }

  quantity.addEventListener("click", () => {
    customQuantity.value = quantity.innerText;

    quantity.classList.add("hidden");
    customQuantity.classList.remove("hidden");
    customQuantity.focus();
  });

  customQuantity.addEventListener("change", () => {
    const newVal = parseInt(customQuantity.value);

    if (!isNaN(newVal) && newVal >= 0) {
      quantity.innerText = newVal;
    }

    customQuantity.classList.add("hidden");
    quantity.classList.remove("hidden");

    syncFinalQuantity();
  });

  document.getElementById("sub").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    if (currentQuantity <= 0) {
      quantity.innerText = 0;
    } else {
      quantity.innerText = currentQuantity - 1;
    }
  });

  document.getElementById("add").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    quantity.innerText = currentQuantity + 1;
    syncFinalQuantity();
  });
});
