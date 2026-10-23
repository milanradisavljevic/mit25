// Reine Logik ohne DOM, damit sie mit `node --test` prüfbar ist.

export const AGE = 25;
export const PARENT_GAP = 30;
export const GRANDPARENT_GAP = 60;
export const ELECTION_WINDOW = 3;
export const MIN_YEAR = 1850;

export const GENERATIONS = [
  { key: "grandparents", label: "Großeltern", gap: GRANDPARENT_GAP },
  { key: "parents", label: "Eltern", gap: PARENT_GAP },
  { key: "you", label: "Du", gap: 0 },
];

const DECIMALS = {
  life_expectancy_birth_male: 1,
  life_expectancy_birth_female: 1,
  share_65plus: 1,
  median_age: 1,
  fertility_rate: 2,
  turnout_nrw: 1,
  income_median_gross: 0,
  income_median_gross_real: 0,
};

const UNIT_SUFFIX = { Jahre: "Jahre", "%": "%", Euro: "€" };

/**
 * Prüft die Eingaben. Liefert { errors: {feld: Text}, years: {grandparents, parents, you} }.
 * Leere optionale Felder werden durch die Standardannahme ersetzt (assumed = true).
 */
export function resolveBirthYears(input, currentYear) {
  const errors = {};
  const parse = (text) => (text === "" || text == null ? null : Number(text));
  const you = parse(input.you);
  const parents = parse(input.parents);
  const grandparents = parse(input.grandparents);

  const checkYear = (field, value) => {
    if (value === null) return;
    if (!Number.isInteger(value) || value < MIN_YEAR || value > currentYear) {
      errors[field] = `Bitte ein Jahr zwischen ${MIN_YEAR} und ${currentYear} eingeben.`;
    }
  };
  if (you === null) errors.you = "Bitte dein Geburtsjahr eingeben.";
  checkYear("you", you);
  checkYear("parents", parents);
  checkYear("grandparents", grandparents);
  if (Object.keys(errors).length) return { errors, years: null };

  const p = parents ?? you - PARENT_GAP;
  const g = grandparents ?? you - GRANDPARENT_GAP;
  if (p >= you) errors.parents = "Das Geburtsjahr der Eltern muss vor deinem liegen.";
  if (g >= p) errors.grandparents = "Das Geburtsjahr der Großeltern muss vor dem der Eltern liegen.";
  if (Object.keys(errors).length) return { errors, years: null };

  return {
    errors,
    years: {
      grandparents: { birthYear: g, assumed: grandparents === null },
      parents: { birthYear: p, assumed: parents === null },
      you: { birthYear: you, assumed: false },
    },
  };
}

export function referenceYear(birthYear) {
  return birthYear + AGE;
}

function knownYears(indicator) {
  return Object.entries(indicator.series)
    .filter(([, value]) => value !== null)
    .map(([year]) => Number(year))
    .sort((a, b) => a - b);
}

/**
 * Wert eines Indikators für ein Stichjahr.
 *
 * status:
 *  - "ok":      Wert für das Stichjahr (bei Wahlen: nächste Wahl innerhalb ±3 Jahre, bei Gleichstand die frühere)
 *  - "future":  Stichjahr liegt in der Zukunft; value/year = aktuellster Wert
 *  - "pending": Stichjahr erreicht, aber noch nicht veröffentlicht; value/year = aktuellster Wert
 *  - "missing": keine Daten für das Stichjahr; firstYear/lastYear zur Einordnung
 */
export function valueFor(indicator, refYear, currentYear) {
  const years = knownYears(indicator);
  const firstYear = years[0];
  const lastYear = years[years.length - 1];
  const latest = { value: indicator.series[String(lastYear)], year: lastYear };

  if (refYear > currentYear) return { status: "future", ...latest };

  if (indicator.type === "event") {
    let best = null;
    for (const year of years) {
      const distance = Math.abs(year - refYear);
      if (distance <= ELECTION_WINDOW && (best === null || distance < Math.abs(best - refYear))) {
        best = year;
      }
    }
    if (best !== null) return { status: "ok", value: indicator.series[String(best)], year: best };
    return { status: "missing", year: refYear, firstYear, lastYear };
  }

  const value = indicator.series[String(refYear)];
  if (value !== undefined && value !== null) return { status: "ok", value, year: refYear };
  if (refYear > lastYear) return { status: "pending", ...latest };
  return { status: "missing", year: refYear, firstYear, lastYear };
}

// "de-DE" statt "de-AT": CLDR trennt Tausender in de-AT mit Leerzeichen, in Österreich
// (und in den Quelltabellen) ist der Punkt üblich. Dezimalkomma ist in beiden gleich.
export const NUMBER_LOCALE = "de-DE";

export function formatNumber(value, indicatorId) {
  const digits = DECIMALS[indicatorId] ?? 1;
  return new Intl.NumberFormat(NUMBER_LOCALE, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value);
}

/** Einheit, die direkt hinter dem Zahlenwert steht ("Jahre", "%", "€"), sonst null. */
export function unitSuffix(indicator) {
  return UNIT_SUFFIX[indicator.unit] ?? null;
}

export function formatWithUnit(value, indicator) {
  const suffix = unitSuffix(indicator);
  return formatNumber(value, indicator.id) + (suffix ? ` ${suffix}` : "");
}

/** Beschriftung einer Reihe innerhalb ihrer Gruppe ("Männer", "nominal", ...). */
export function memberLabel(indicator) {
  return indicator.sublabel ?? indicator.label.split(", ").at(-1);
}

/**
 * Ergänzt Indikatoren mit `deflate: "cpi"` um eine Reihe in Preisen des letzten VPI-Jahres:
 * Wert × VPI(Bezugsjahr) / VPI(Jahr). Fehlt einer der Werte, bleibt das Jahr null.
 * Original und umgerechnete Reihe werden als Gruppe angezeigt.
 */
export function withPriceAdjusted(indicators) {
  const cpi = indicators.find((i) => i.id === "cpi");
  if (!cpi) return indicators;
  const base = Math.max(...Object.keys(cpi.series).filter((y) => cpi.series[y] !== null).map(Number));
  const baseValue = cpi.series[String(base)];
  const result = [];
  for (const indicator of indicators) {
    if (indicator.deflate !== "cpi") {
      result.push(indicator);
      continue;
    }
    const series = Object.fromEntries(
      Object.entries(indicator.series).map(([year, value]) => {
        const index = cpi.series[year];
        return [year, value === null || index == null ? null : (value * baseValue) / index];
      }),
    );
    result.push({ ...indicator, group: indicator.id, sublabel: "nominal" });
    result.push({
      ...indicator,
      id: `${indicator.id}_real`,
      group: indicator.id,
      sublabel: `in Preisen von ${base}`,
      series,
      sources: [...indicator.sources, ...cpi.sources],
      notes: [
        ...indicator.notes,
        `Umrechnung in Preise von ${base}: Wert × VPI ${base} / VPI des jeweiligen Jahres (Jahresdurchschnitte, ${cpi.label}).`,
      ],
      deflate: undefined,
      derived: true,
    });
  }
  return result;
}

/**
 * Sichtbare Indikatoren in Anzeige-Reihenfolge, zusammengehörige Reihen (group) gebündelt.
 * Liefert [{ id, label, members: [indicator, ...] }].
 */
export function displayRows(indicators, groupLabels = {}) {
  const rows = [];
  const byGroup = new Map();
  for (const indicator of indicators) {
    if (indicator.display === false) continue;
    const key = indicator.group ?? indicator.id;
    if (!byGroup.has(key)) {
      const row = { id: key, label: groupLabels[key] ?? indicator.label, members: [] };
      byGroup.set(key, row);
      rows.push(row);
    }
    byGroup.get(key).members.push(indicator);
  }
  return rows;
}
