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
  income_monthly_arbeiter: 0,
  income_monthly_arbeiter_real: 0,
  income_monthly_angestellte: 0,
  income_monthly_angestellte_real: 0,
  wage_industry_vienna: 2,
  wage_industry_vienna_real: 2,
  price_semmel_minutes: 1,
  price_vollmilch_minutes: 1,
  price_kinokarte_minutes: 0,
  price_benzin_minutes: 1,
  rent_avg: 0,
  rent_avg_real: 0,
  price_semmel: 2,
  price_semmel_real: 2,
  price_vollmilch: 2,
  price_vollmilch_real: 2,
  price_kinokarte: 2,
  price_kinokarte_real: 2,
  price_benzin: 2,
  price_benzin_real: 2,
};

const UNIT_SUFFIX = { Jahre: "Jahre", "%": "%", Euro: "€", "Euro pro Monat": "€", "Euro pro Stunde": "€", Minuten: "Min." };

/** Hinweis für einen Wert, der vor einem Methodenbruch liegt (Feld `breaks`), sonst null. */
export function breakNote(indicator, year) {
  const brk = (indicator.breaks ?? []).find((b) => year < b.year);
  // Erster Bruch nach dem Jahr mit Hinweistext; leerer Text = nur im Diagramm markieren
  const labelled = (indicator.breaks ?? []).find((b) => year < b.year && b.before);
  return brk && labelled ? labelled.before : null;
}

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
 *               (auch nach dem Ende einer eingestellten Reihe, Feld `ended`)
 */
export function valueFor(indicator, refYear, currentYear) {
  const years = knownYears(indicator);
  const firstYear = years[0];
  const lastYear = years[years.length - 1];
  const latest = { value: indicator.series[String(lastYear)], year: lastYear };

  // Eingestellte Reihe (`ended`): danach gibt es keinen "aktuellsten Wert", nur eine Lücke.
  if (indicator.ended && refYear > lastYear) return { status: "missing", year: refYear, firstYear, lastYear };
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
      series_ats: undefined,
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

/** Ursprünglicher Schillingwert eines Jahres als Text ("1,07 S"), sonst null. */
export function schillingNote(indicator, year) {
  const value = indicator.series_ats?.[String(year)];
  if (value == null) return null;
  return `${new Intl.NumberFormat(NUMBER_LOCALE, { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value)} S`;
}

/**
 * Ergänzt Preise mit `work_minutes: <Lohn-ID>` um eine Reihe „Arbeitszeit“ in Minuten:
 * Preis / (Stundenlohn / 60), nur für Jahre mit beiden Werten (beide in Euro, nominal).
 * Die neue Reihe steht direkt hinter der Gruppe ihres Preises, als eigene Zeile.
 */
export function withWorkMinutes(indicators) {
  const byId = Object.fromEntries(indicators.map((i) => [i.id, i]));
  const extra = new Map();
  for (const price of indicators) {
    const wage = byId[price.work_minutes];
    if (!wage || price.derived) continue; // nur die nominale Reihe, nicht die Kaufkraftreihe
    const series = {};
    for (const year of Object.keys(price.series)) {
      const p = price.series[year];
      const w = wage.series[year];
      if (p != null && w != null) series[year] = (p / w) * 60;
    }
    const years = Object.keys(series).map(Number);
    const first = Math.min(...years);
    const breaks = [...(price.breaks ?? []), ...(wage.breaks ?? [])]
      .filter((b) => b.year > first) // Brüche vor Reihenbeginn betreffen diese Reihe nicht
      .sort((a, b) => a.year - b.year);
    extra.set(price.group ?? price.id, {
      id: `${price.id}_minutes`,
      label: `${price.label.replace(/ \(Wien\)$/, "")}: Arbeitszeit`,
      unit: "Minuten",
      description: `Wie lange ein Industriearbeiter in Wien brutto arbeiten musste, um sich das leisten zu können (Preis geteilt durch Stundenlohn)`,
      source: `${price.source}; ${wage.source}`,
      source_url: price.source_url,
      sources: [...new Map([...price.sources, ...wage.sources].map((s) => [s.url, s])).values()],
      retrieved: [price.retrieved, wage.retrieved].sort().at(-1),
      notes: [
        "Arbeitsminuten = Preis / (Stundenlohn / 60); beides Wiener Werte desselben Jahres.",
        "Stundenlohn der Industriearbeiter (brutto, September): liegt eher über dem Durchschnitt aller Beschäftigten, die Minuten fallen also eher zu niedrig aus.",
        "Preis im Jahresdurchschnitt, Lohn im September.",
        ...wage.notes.filter((n) => n.startsWith("Ab 2004")),
      ],
      breaks,
      ended: true,
      ended_note: "nur 1987 bis 2005 erfasst",
      derived: true,
      series,
    });
  }
  if (!extra.size) return indicators;
  const result = [];
  indicators.forEach((indicator, i) => {
    result.push(indicator);
    const key = indicator.group ?? indicator.id;
    const next = indicators[i + 1];
    if (extra.has(key) && (next?.group ?? next?.id) !== key) result.push(extra.get(key));
  });
  return result;
}

export const SECTIONS = [
  { title: "Leben und Bevölkerung", match: /^(life_expectancy|share_65plus|median_age|fertility_rate)/ },
  { title: "Einkommen", match: /^(income_|wage_)/ },
  { title: "Preise in Wien", match: /^price_/ },
  { title: "Wohnen", match: /^rent_/ },
  { title: "Politik", match: /^turnout_/ },
];

/** Anzeigezeilen nach Themen (SECTIONS) gegliedert; Reihenfolge innerhalb eines Themas bleibt. */
export function groupIntoSections(rows) {
  const sections = SECTIONS.map((s) => ({ title: s.title, rows: [] }));
  const other = { title: "Weitere", rows: [] };
  for (const row of rows) {
    const index = SECTIONS.findIndex((s) => s.match.test(row.id));
    (index >= 0 ? sections[index] : other).rows.push(row);
  }
  return [...sections, other].filter((s) => s.rows.length);
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
