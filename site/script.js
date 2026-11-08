"use strict";

// Preferences are optional: the page remains readable without storage or JavaScript.
const root = document.documentElement;
const themeButton = document.querySelector(".theme-toggle");
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
let selectedTheme = null;
try {
  const storedTheme = localStorage.getItem("toss-theme");
  if (storedTheme === "light" || storedTheme === "dark") selectedTheme = storedTheme;
} catch (_) { /* Restricted storage leaves the system preference in control. */ }

function updateThemeButton() {
  const isDark = (selectedTheme || (systemTheme.matches ? "dark" : "light")) === "dark";
  if (selectedTheme) root.dataset.theme = selectedTheme;
  themeButton.setAttribute("aria-pressed", String(isDark));
  themeButton.setAttribute("aria-label", isDark ? "切换至浅色主题" : "切换至深色主题");
}

themeButton.hidden = false;
updateThemeButton();
themeButton.addEventListener("click", () => {
  const isDark = (selectedTheme || (systemTheme.matches ? "dark" : "light")) === "dark";
  selectedTheme = isDark ? "light" : "dark";
  try { localStorage.setItem("toss-theme", selectedTheme); } catch (_) { /* Optional. */ }
  updateThemeButton();
});
systemTheme.addEventListener("change", updateThemeButton);

const filterTools = document.querySelector(".filter-tools");
const filters = [...document.querySelectorAll(".filter")];
const rows = [...document.querySelectorAll(".standard-row")];
const search = document.querySelector("#standard-search");
const emptyState = document.querySelector(".empty-state");
const result = document.querySelector(".filter-result");
let category = "all";
filterTools.hidden = false;

function filterStandards() {
  const query = search.value.trim().toLocaleLowerCase();
  let visibleCount = 0;
  for (const row of rows) {
    const matchesCategory = category === "all" || row.dataset.category === category;
    const matchesQuery = row.textContent.toLocaleLowerCase().includes(query);
    row.hidden = !(matchesCategory && matchesQuery);
    if (!row.hidden) visibleCount++;
  }
  emptyState.hidden = visibleCount > 0;
  result.textContent = `显示 ${visibleCount} 项标准，共 ${rows.length} 项。`;
}

for (const button of filters) {
  button.addEventListener("click", () => {
    category = button.dataset.filter;
    for (const filter of filters) {
      const active = filter === button;
      filter.classList.toggle("active", active);
      filter.setAttribute("aria-pressed", String(active));
    }
    filterStandards();
  });
}
search.addEventListener("input", filterStandards);
