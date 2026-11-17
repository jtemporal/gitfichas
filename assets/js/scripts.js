// Deals with title width
function updateH1Width() {
  document.querySelectorAll(".title-container").forEach(function (container) {
    const h1 = container.querySelector("h1");
    const h1Width = h1.offsetWidth;
    container.style.setProperty("--h1-width", h1Width + "px");
  });
}

window.addEventListener("resize", updateH1Width);

// Home page: search box and family chips filter the card grid together
function initCardFilters() {
  var input = document.getElementById("search-input");
  var tiles = Array.prototype.slice.call(document.querySelectorAll(".gf-grid .gf-tile"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".gf-chip"));
  var empty = document.getElementById("no-results-message");
  if (!input || tiles.length === 0) return;
  var family = "all";

  function apply() {
    var query = input.value.trim().toLowerCase();
    var shown = 0;
    tiles.forEach(function (tile) {
      var text = (tile.getAttribute("data-title") || "").toLowerCase();
      var match =
        (family === "all" || tile.getAttribute("data-family") === family) &&
        (query === "" || text.indexOf(query) !== -1);
      tile.hidden = !match;
      if (match) shown += 1;
    });
    if (empty) empty.hidden = shown !== 0;
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      family = chip.getAttribute("data-family");
      chips.forEach(function (other) {
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });
      apply();
    });
  });
  input.addEventListener("input", apply);
  apply();
}

// Copy buttons: [data-copy="text"] copies that text, [data-copy-url] copies this page's address
function copyText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text);
  }
  return new Promise(function (resolve, reject) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (error) {
      ok = false;
    }
    document.body.removeChild(area);
    if (ok) resolve();
    else reject(new Error("copy failed"));
  });
}

document.addEventListener("click", function (event) {
  var button = event.target.closest ? event.target.closest("[data-copy], [data-copy-url]") : null;
  if (!button) return;
  var text = button.hasAttribute("data-copy-url")
    ? window.location.origin + window.location.pathname
    : button.getAttribute("data-copy");
  copyText(text).then(function () {
    var label = button.querySelector("[data-copy-label]");
    var original = label ? label.textContent : null;
    button.classList.add("is-copied");
    if (label) label.textContent = button.getAttribute("data-copied") || original;
    setTimeout(function () {
      button.classList.remove("is-copied");
      if (label) label.textContent = original;
    }, 1600);
  }, function () {});
});

// Card page: study mode hides the notes so each part can be revealed one at a time
function initStudyMode() {
  var study = document.getElementById("study");
  var page = document.querySelector(".gf-post");
  if (!study || !page) return;

  var rows = Array.prototype.slice.call(study.querySelectorAll("[data-study-row]"));
  var bars = Array.prototype.slice.call(study.querySelectorAll("[data-study-progress] span"));
  var progress = study.querySelector("[data-study-progress]");
  var progressText = study.querySelector("[data-study-progress-text]");
  var info = study.querySelector("[data-study-info]");
  var nextButton = study.querySelector("[data-study-next]");
  var pill = page.querySelector("[data-study-pill]");
  var template = study.getAttribute("data-progress-template") || "%n / %t";
  var hideWhileStudying = Array.prototype.slice.call(page.querySelectorAll("[data-study-hide]"));

  function isRevealed(row) {
    return row.classList.contains("is-revealed");
  }

  function update() {
    var revealed = rows.filter(isRevealed).length;
    bars.forEach(function (bar, index) {
      bar.classList.toggle("is-on", index < revealed);
    });
    if (progress) progress.setAttribute("aria-valuenow", String(revealed));
    if (progressText) {
      progressText.textContent = template.replace("%n", revealed).replace("%t", rows.length);
    }
    if (info) info.hidden = revealed !== rows.length;
    if (nextButton) nextButton.disabled = revealed === rows.length;
  }

  function setRevealed(row, on) {
    row.classList.toggle("is-revealed", on);
    row.querySelector("[data-study-note]").hidden = !on;
    row.querySelector("[data-study-reveal]").hidden = on;
  }

  function setOpen(on) {
    study.hidden = !on;
    page.classList.toggle("gf-is-studying", on);
    if (pill) pill.hidden = !on;
    hideWhileStudying.forEach(function (element) {
      element.hidden = on;
    });
    if (window.history && window.history.replaceState) {
      var base = window.location.pathname + window.location.search;
      window.history.replaceState(null, "", on ? base + "#study" : base);
    }
    if (on) window.scrollTo(0, 0);
  }

  rows.forEach(function (row) {
    row.querySelector("[data-study-reveal]").addEventListener("click", function () {
      setRevealed(row, true);
      update();
    });
  });

  if (nextButton) {
    nextButton.addEventListener("click", function () {
      var next = rows.filter(function (row) { return !isRevealed(row); })[0];
      if (next) setRevealed(next, true);
      update();
    });
  }

  var allButton = study.querySelector("[data-study-all]");
  if (allButton) {
    allButton.addEventListener("click", function () {
      rows.forEach(function (row) { setRevealed(row, true); });
      update();
    });
  }

  var resetButton = study.querySelector("[data-study-reset]");
  if (resetButton) {
    resetButton.addEventListener("click", function () {
      rows.forEach(function (row) { setRevealed(row, false); });
      update();
    });
  }

  Array.prototype.slice.call(page.querySelectorAll("[data-study-open]")).forEach(function (button) {
    button.addEventListener("click", function () { setOpen(true); });
  });
  Array.prototype.slice.call(page.querySelectorAll("[data-study-close]")).forEach(function (button) {
    button.addEventListener("click", function () { setOpen(false); });
  });

  update();
  if (window.location.hash === "#study") setOpen(true);
}
