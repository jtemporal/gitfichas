// Deals with title width
function updateH1Width() {
  document.querySelectorAll(".title-container").forEach(function (container) {
    const h1 = container.querySelector("h1");
    const h1Width = h1.offsetWidth;
    container.style.setProperty("--h1-width", h1Width + "px");
  });
}

window.addEventListener("resize", updateH1Width);

// Search bar logic
function searchCards(inputId, cardsSelector) {
  const searchInput = document.getElementById(inputId);
  const cards = document.querySelectorAll(cardsSelector);
  const noResultsMessage = document.getElementById("no-results-message");

  searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();
    let matchesFound = 0;

    cards.forEach((card) => {
      const text = card.getAttribute("data-title").toLowerCase() || "";
      const match = text.includes(query);

      card.style.display = match ? "block" : "none";

      if (match) matchesFound++;
    });

    if (query.length > 0 && matchesFound === 0) {
      noResultsMessage.style.display = "block"; // shows the message
    } else {
      noResultsMessage.style.display = "none"; // hides the message
    }
  });
}
