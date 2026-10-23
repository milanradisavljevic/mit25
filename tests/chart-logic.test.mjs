import assert from "node:assert/strict";
import { test } from "node:test";

import {
  emptyRanges,
  knownYears,
  nearestYear,
  niceStep,
  segments,
  xDomain,
  yScale,
  yearTicks,
} from "../site/chart-logic.js";

test("runde Schrittweiten", () => {
  assert.equal(niceStep(10, 4), 2.5);
  assert.equal(niceStep(30, 4), 10);
  assert.equal(niceStep(1.5, 4), 0.5);
});

test("Y-Bereich umfasst die Daten und endet auf Teilstrichen", () => {
  const { domain, ticks } = yScale(62.38, 84.58);
  assert.ok(domain[0] <= 62.38 && domain[1] >= 84.58);
  assert.equal(ticks[0], domain[0]);
  assert.equal(ticks.at(-1), domain[1]);
  assert.deepEqual(yScale(1.3, 2.8).ticks, [1, 1.5, 2, 2.5, 3]);
});

test("X-Bereich schließt Stichjahre außerhalb der Daten ein", () => {
  assert.deepEqual(xDomain([1961, 2025], [1925, 1955, 1985]), [1925, 2025]);
  assert.deepEqual(xDomain([1961, 2025], [1970, 2000, 2030]), [1961, 2030]);
});

test("Jahres-Teilstriche bleiben unter der Höchstzahl", () => {
  assert.deepEqual(yearTicks([1925, 2025], 6), [1940, 1960, 1980, 2000, 2020]);
  assert.ok(yearTicks([1919, 2030], 4).length <= 4);
});

test("Linien werden an null und an fehlenden Jahren getrennt, nie verbunden", () => {
  const series = { 2000: 1, 2001: 2, 2002: null, 2003: 4, 2005: 6 };
  assert.deepEqual(segments(series), [[[2000, 1], [2001, 2]], [[2003, 4]], [[2005, 6]]]);
  assert.deepEqual(knownYears(series), [2000, 2001, 2003, 2005]);
});

test("Bereiche ohne Daten vor und nach der Reihe", () => {
  assert.deepEqual(emptyRanges([1925, 2030], [1961, 2025]), [[1925, 1960], [2026, 2030]]);
  assert.deepEqual(emptyRanges([1961, 2025], [1961, 2025]), []);
});

test("nächstes Jahr, bei Gleichstand das frühere", () => {
  assert.equal(nearestYear([1995, 1999], 1997), 1995);
  assert.equal(nearestYear([1995, 1999], 1998), 1999);
});
