import {
  GENERATIONS,
  displayRows,
  breakNote,
  formatNumber,
  memberLabel,
  referenceYear,
  resolveBirthYears,
  schillingNote,
  unitSuffix,
  valueFor,
  withPriceAdjusted,
  withWorkMinutes,
} from "./logic.js";
import { renderCharts } from "./chart.js";

const CURRENT_YEAR = new Date().getFullYear();
const GROUP_LABELS = { life_expectancy_birth: "Lebenserwartung bei Geburt" };
const FIELDS = ["you", "parents", "grandparents"];
const PARAMS = { you: "jahr", parents: "eltern", grandparents: "grosseltern" };

const $ = (id) => document.getElementById(id);

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else node.setAttribute(key, value);
  }
  for (const child of children) {
    if (child != null) node.append(child);
  }
  return node;
}

function formatDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString("de-AT");
}

function valueNode(indicator, result) {
  const suffix = unitSuffix(indicator);
  return el(
    "span",
    {},
    el("span", { class: "value" }, formatNumber(result.value, indicator.id)),
    suffix ? el("span", { class: "unit" }, ` ${suffix}`) : null,
  );
}

function cell(indicator, refYear) {
  const result = valueFor(indicator, refYear, CURRENT_YEAR);
  const td = el("td", { "data-status": result.status });
  const isEvent = indicator.type === "event";

  if (result.status === "ok") {
    td.append(valueNode(indicator, result));
    if (isEvent) td.append(el("span", { class: "note" }, `Wahl ${result.year}`));
    const ats = schillingNote(indicator, result.year);
    if (ats) td.append(el("span", { class: "note" }, `damals ${ats}`));
    const before = breakNote(indicator, result.year);
    if (before) td.append(el("span", { class: "note" }, before));
  } else if (result.status === "future") {
    td.append(
      el("span", { class: "gap" }, "noch nicht erreicht"),
      valueNode(indicator, result),
      el("span", { class: "note" }, `${isEvent ? "letzte Wahl" : "aktuellster Wert"}: ${result.year}`),
    );
  } else if (result.status === "pending") {
    td.append(
      el("span", { class: "gap" }, `noch keine Daten für ${refYear}`),
      valueNode(indicator, result),
      el("span", { class: "note" }, `aktuellster Wert: ${result.year}`),
    );
  } else if (isEvent) {
    td.append(
      el("span", { class: "gap" }, `keine Daten für ${refYear}`),
      el("span", { class: "note" }, `keine Wahl zwischen ${refYear - 3} und ${refYear + 3}`),
    );
  } else {
    td.append(el("span", { class: "gap" }, `keine Daten für ${refYear}`));
    if (refYear < result.firstYear) td.append(el("span", { class: "note" }, `Reihe beginnt ${result.firstYear}`));
    if (refYear > result.lastYear) {
      td.append(el("span", { class: "note" }, indicator.ended_note ?? `Reihe endet ${result.lastYear}`));
    }
  }
  return td;
}

function sourceDetails(members) {
  const first = members[0];
  const sources = [...new Map(members.flatMap((m) => m.sources).map((s) => [s.url, s])).values()];
  const notes = [...new Set(members.flatMap((m) => m.notes ?? []))];
  return el(
    "details",
    {},
    el("summary", {}, "Quelle und Hinweise"),
    el(
      "div",
      { class: "source" },
      el("p", {}, first.description),
      notes.length ? el("ul", {}, ...notes.map((n) => el("li", {}, n))) : null,
      el("p", {}, "Quellen:"),
      el("ul", {}, ...sources.map((s) => el("li", {}, el("a", { href: s.url, rel: "noopener" }, s.label)))),
      el("p", {}, `Abgerufen am ${formatDate(first.retrieved)}`),
    ),
  );
}

function renderHead(years) {
  const row = $("generations");
  row.replaceChildren(el("td"));
  for (const g of GENERATIONS) {
    const { birthYear, assumed } = years[g.key];
    const refYear = referenceYear(birthYear);
    row.append(
      el(
        "th",
        { scope: "col", class: `gen gen-${g.key}` },
        el("span", { class: "gen-name" }, g.label),
        el("span", { class: "gen-year" }, String(refYear)),
        el("span", { class: "gen-born" }, `geboren ${birthYear}${assumed ? ", angenommen" : ""}`),
      ),
    );
  }
}

function renderBody(rows, years) {
  const table = document.querySelector(".compare");
  table.querySelectorAll("tbody").forEach((tb) => tb.remove());
  const refYears = GENERATIONS.map((g) => referenceYear(years[g.key].birthYear));

  for (const row of rows) {
    const body = el("tbody", { class: "indicator", id: `row-${row.id}` });
    const heading = el("span", {}, row.label);
    if (row.members.length === 1) {
      const indicator = row.members[0];
      body.append(
        el("tr", {}, el("th", { scope: "row" }, heading, sourceDetails(row.members)), ...refYears.map((y) => cell(indicator, y))),
      );
    } else {
      body.append(el("tr", { class: "group-head" }, el("th", { scope: "rowgroup", colspan: "4" }, heading, sourceDetails(row.members))));
      for (const indicator of row.members) {
        const sublabel = memberLabel(indicator);
        body.append(el("tr", { class: "member" }, el("th", { scope: "row" }, sublabel), ...refYears.map((y) => cell(indicator, y))));
      }
    }
    table.append(body);
  }
}

function readInput() {
  return Object.fromEntries(FIELDS.map((f) => [f, $(f).value.trim()]));
}

function showErrors(errors) {
  for (const f of FIELDS) {
    $(`${f}-error`).textContent = errors[f] ?? "";
    $(f).setAttribute("aria-invalid", errors[f] ? "true" : "false");
  }
}

function updateUrl(input) {
  const params = new URLSearchParams();
  for (const f of FIELDS) if (input[f]) params.set(PARAMS[f], input[f]);
  history.replaceState(null, "", params.size ? `?${params}` : location.pathname);
}

function updateHints(input) {
  const you = Number(input.you);
  const valid = Number.isInteger(you) && input.you.length === 4;
  $("parents").placeholder = valid ? String(you - 30) : "";
  $("grandparents").placeholder = valid ? String(you - 60) : "";
}

function render(data, { quiet = false } = {}) {
  const input = readInput();
  updateHints(input);
  const { errors, years } = resolveBirthYears(input, CURRENT_YEAR);
  // Während der Eingabe keine Fehlermeldung für ein unvollständiges Geburtsjahr
  if (quiet && input.you.length < 4) return;
  showErrors(errors);
  if (!years) return;
  const rows = displayRows(data.indicators, GROUP_LABELS);
  renderHead(years);
  renderBody(rows, years);
  $("result").hidden = false;
  const generations = GENERATIONS.map((g) => {
    const refYear = referenceYear(years[g.key].birthYear);
    const results = Object.fromEntries(data.indicators.map((i) => [i.id, valueFor(i, refYear, CURRENT_YEAR)]));
    return { key: g.key, label: g.label, refYear, results };
  });
  renderCharts($("charts"), rows, generations);
  updateUrl(input);
}

async function main() {
  const params = new URLSearchParams(location.search);
  for (const f of FIELDS) $(f).value = params.get(PARAMS[f]) ?? "";

  let data;
  try {
    // no-cache: Browser fragt nach, ob data.json neuer ist, statt eine veraltete Kopie zu nehmen
    const response = await fetch("data.json", { cache: "no-cache" });
    if (!response.ok) throw new Error(response.statusText);
    data = await response.json();
    data.indicators = withWorkMinutes(withPriceAdjusted(data.indicators));
  } catch {
    $("load-error").hidden = false;
    return;
  }
  $("data-date").textContent = `Datenstand: ${formatDate(data.generated_at)}`;

  const form = $("form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    render(data);
  });
  form.addEventListener("input", () => render(data, { quiet: true }));
  if ($("you").value) render(data);
}

main();
