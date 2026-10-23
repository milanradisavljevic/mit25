import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import {
  GENERATIONS,
  displayRows,
  formatNumber,
  referenceYear,
  resolveBirthYears,
  valueFor,
} from "../site/logic.js";

const NOW = 2026;
const data = JSON.parse(readFileSync(new URL("../site/data.json", import.meta.url), "utf-8"));
const byId = Object.fromEntries(data.indicators.map((i) => [i.id, i]));

const yearly = { id: "x", series: { 1961: 1.5, 1962: null, 1963: 2.5 } };
const events = { id: "e", type: "event", series: { 1966: 90, 1970: 91, 1971: 92, 2024: 77 } };

test("Standardannahme: Eltern minus 30, Großeltern minus 60", () => {
  const { errors, years } = resolveBirthYears({ you: "1985", parents: "", grandparents: "" }, NOW);
  assert.deepEqual(errors, {});
  assert.deepEqual(years.parents, { birthYear: 1955, assumed: true });
  assert.deepEqual(years.grandparents, { birthYear: 1925, assumed: true });
  assert.equal(referenceYear(years.you.birthYear), 2010);
});

test("eigene Angaben ersetzen die Annahme", () => {
  const { years } = resolveBirthYears({ you: "1985", parents: "1958", grandparents: "1932" }, NOW);
  assert.deepEqual(years.parents, { birthYear: 1958, assumed: false });
  assert.deepEqual(years.grandparents, { birthYear: 1932, assumed: false });
});

test("ungültige Eingaben werden gemeldet", () => {
  assert.ok(resolveBirthYears({ you: "" }, NOW).errors.you);
  assert.ok(resolveBirthYears({ you: "abc" }, NOW).errors.you);
  assert.ok(resolveBirthYears({ you: "2030" }, NOW).errors.you);
  assert.ok(resolveBirthYears({ you: "1985", parents: "1990" }, NOW).errors.parents);
  assert.ok(resolveBirthYears({ you: "1985", parents: "1950", grandparents: "1960" }, NOW).errors.grandparents);
});

test("Jahreswert vorhanden", () => {
  assert.deepEqual(valueFor(yearly, 1961, NOW), { status: "ok", value: 1.5, year: 1961 });
});

test("Lücke (null) und Jahre vor Reihenbeginn sind missing, nie interpoliert", () => {
  assert.equal(valueFor(yearly, 1962, NOW).status, "missing");
  const before = valueFor(yearly, 1950, NOW);
  assert.equal(before.status, "missing");
  assert.equal(before.firstYear, 1961);
});

test("Stichjahr erreicht, aber noch keine Daten: aktuellster Wert", () => {
  assert.deepEqual(valueFor(yearly, 2026, NOW), { status: "pending", value: 2.5, year: 1963 });
});

test("Stichjahr in der Zukunft: aktuellster Wert", () => {
  assert.deepEqual(valueFor(yearly, 2030, NOW), { status: "future", value: 2.5, year: 1963 });
  assert.deepEqual(valueFor(events, 2030, NOW), { status: "future", value: 77, year: 2024 });
});

test("Wahl: nächste innerhalb ±3 Jahre, bei Gleichstand die frühere", () => {
  assert.equal(valueFor(events, 1970, NOW).year, 1970);
  assert.equal(valueFor(events, 1968, NOW).year, 1966);
  assert.equal(valueFor(events, 1973, NOW).year, 1971);
  assert.equal(valueFor(events, 1990, NOW).status, "missing");
});

test("Zahlenformat österreichisch", () => {
  assert.equal(formatNumber(78.4321, "life_expectancy_birth_male"), "78,4");
  assert.equal(formatNumber(1.2964, "fertility_rate"), "1,30");
});

test("Anzeigezeilen: VPI ausgeblendet, Lebenserwartung gebündelt", () => {
  const rows = displayRows(data.indicators, { life_expectancy_birth: "Lebenserwartung bei Geburt" });
  assert.ok(!rows.some((r) => r.id === "cpi"));
  const le = rows.find((r) => r.id === "life_expectancy_birth");
  assert.equal(le.label, "Lebenserwartung bei Geburt");
  assert.equal(le.members.length, 2);
});

test("Geburtsjahre 1960 bis 2005: jede Zelle hat einen gültigen Zustand", () => {
  for (let born = 1960; born <= 2005; born++) {
    const { years } = resolveBirthYears({ you: String(born) }, NOW);
    for (const g of GENERATIONS) {
      const ref = referenceYear(years[g.key].birthYear);
      for (const indicator of data.indicators) {
        const r = valueFor(indicator, ref, NOW);
        assert.ok(["ok", "future", "pending", "missing"].includes(r.status));
        if (r.status !== "missing") assert.equal(typeof r.value, "number", `${indicator.id} ${ref}`);
        if (r.status === "ok" && indicator.type !== "event") assert.equal(r.year, ref);
      }
    }
  }
});

test("Stichproben gegen data.json", () => {
  // Geburtsjahr 1985: Du 2010, Eltern 1980, Großeltern 1950
  assert.equal(valueFor(byId.share_65plus, 2010, NOW).status, "ok");
  assert.equal(valueFor(byId.share_65plus, 1950, NOW).status, "missing");
  assert.equal(valueFor(byId.life_expectancy_birth_male, 1950, NOW).status, "missing");
  assert.equal(valueFor(byId.life_expectancy_birth_male, 1951, NOW).value, 62.38);
  assert.equal(valueFor(byId.turnout_nrw, 1950, NOW).year, 1949);
  assert.equal(valueFor(byId.turnout_nrw, 2010, NOW).year, 2008);
  // Geburtsjahr 2001: Du 2026, Daten bis 2025
  assert.deepEqual(valueFor(byId.median_age, 2026, NOW).status, "pending");
});
