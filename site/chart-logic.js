// Reine Rechenhilfen für die Diagramme, ohne DOM (getestet mit node --test).

/** Runde Schrittweite (1, 2, 2,5, 5, 10 × Zehnerpotenz) für etwa `count` Intervalle. */
export function niceStep(span, count) {
  const raw = span / count;
  const magnitude = 10 ** Math.floor(Math.log10(raw));
  const norm = raw / magnitude;
  const factor = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10;
  return factor * magnitude;
}

/** Y-Bereich auf runde Werte erweitert, mit Teilstrichen. */
export function yScale(min, max, count = 4) {
  if (min === max) {
    min -= 1;
    max += 1;
  }
  const step = niceStep(max - min, count);
  const lo = Math.floor(min / step) * step;
  const hi = Math.ceil(max / step) * step;
  const ticks = [];
  for (let i = 0; lo + i * step <= hi + step / 1e6; i++) {
    ticks.push(Number((lo + i * step).toPrecision(12)));
  }
  return { domain: [lo, hi], ticks };
}

/** Jahre mit Wert (nicht null), aufsteigend. */
export function knownYears(series) {
  return Object.keys(series)
    .filter((y) => series[y] !== null)
    .map(Number)
    .sort((a, b) => a - b);
}

/** X-Bereich: alle Jahre mit Daten und alle Stichjahre, damit Lücken sichtbar werden. */
export function xDomain(dataYears, refYears) {
  const all = [...dataYears, ...refYears];
  return [Math.min(...all), Math.max(...all)];
}

/** Jahres-Teilstriche auf Vielfachen einer runden Schrittweite, höchstens `maxTicks`. */
export function yearTicks([start, end], maxTicks) {
  const step = [1, 2, 5, 10, 20, 25, 50, 100].find((s) => Math.floor(end / s) - Math.ceil(start / s) + 1 <= maxTicks) ?? 100;
  const ticks = [];
  for (let y = Math.ceil(start / step) * step; y <= end; y += step) ticks.push(y);
  return ticks;
}

/**
 * Linienabschnitte: [[[Jahr, Wert], ...], ...]. Ein null-Wert oder ein fehlendes Jahr
 * beendet den Abschnitt; über Lücken wird nie hinweg verbunden.
 */
export function segments(series) {
  const result = [];
  let current = [];
  let previous = null;
  for (const year of Object.keys(series).map(Number).sort((a, b) => a - b)) {
    const value = series[year];
    const contiguous = previous !== null && year === previous + 1;
    if (value === null || (!contiguous && current.length)) {
      if (current.length) result.push(current);
      current = [];
    }
    if (value !== null) current.push([year, value]);
    previous = year;
  }
  if (current.length) result.push(current);
  return result;
}

/** Bereiche im X-Bereich ohne Daten vor dem ersten bzw. nach dem letzten Jahr. */
export function emptyRanges([start, end], dataYears) {
  const ranges = [];
  const first = dataYears[0];
  const last = dataYears[dataYears.length - 1];
  if (start < first) ranges.push([start, first - 1]);
  if (end > last) ranges.push([last + 1, end]);
  return ranges;
}

/** Nächstes Jahr aus `years`; bei Gleichstand das frühere. */
export function nearestYear(years, target) {
  let best = null;
  for (const year of years) {
    if (best === null || Math.abs(year - target) < Math.abs(best - target)) best = year;
  }
  return best;
}
