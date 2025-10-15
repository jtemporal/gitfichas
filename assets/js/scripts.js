// Deals with title width
function updateH1Width() {
  document.querySelectorAll(".title-container").forEach(function (container) {
    const h1 = container.querySelector("h1");
    const h1Width = h1.offsetWidth;
    container.style.setProperty("--h1-width", h1Width + "px");
  });
}

window.addEventListener("resize", updateH1Width);

// search bar logic
function searchCards(inputId, cardsSelector) {
  const searchInput = document.getElementById(inputId);
  const cards = document.querySelectorAll(cardsSelector);

  const noResultsMessage = document.getElementById("no-results-message");

  searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();
    let matchesFound = 0; // Initialize a counter for matches

    cards.forEach((card) => {
      const text = card.getAttribute("data-title") || "";
      const match = text.includes(query);

      // Toggle card visibility
      card.style.display = match ? "block" : "none";

      // Increment the counter if a match is found
      if (match) {
        matchesFound++;
      }
    });

    if (matchesFound === 0 && query.length > 0) {
      // If no matches and the user actually typed something, show the message
      noResultsMessage.style.display = "block";
    } else {
      // Otherwise, hide the message
      noResultsMessage.style.display = "none";
    }
  });
}
