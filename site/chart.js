// Liniendiagramm je Indikator als SVG, ohne Bibliothek.
// Lücken bleiben Lücken: Linien enden an fehlenden Jahren, Bereiche ohne Daten sind markiert.

import { emptyRanges, knownYears, nearestYear, segments, xDomain, yScale, yearTicks } from "./chart-logic.js";
import { NUMBER_LOCALE, formatWithUnit, memberLabel, schillingNote } from "./logic.js";

const NS = "http://www.w3.org/2000/svg";
const PLOT_HEIGHT = 190;
const LABEL_ROW = 18;
const MARGIN = { top: 3 * LABEL_ROW + 8, right: 58, bottom: 26, left: 44 };
const TICK_FORMAT = new Intl.NumberFormat(NUMBER_LOCALE, { maximumFractionDigits: 2 });

function svg(tag, attrs = {}, text) {
  const node = document.createElementNS(NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (text != null) node.textContent = text;
  return node;
}

function html(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else node.setAttribute(key, value);
  }
  for (const child of children) if (child != null) node.append(child);
  return node;
}

function memberName(indicator, members) {
  return members.length > 1 ? memberLabel(indicator) : indicator.label;
}

function formatValue(indicator, value) {
  return formatWithUnit(value, indicator);
}

/**
 * Zeichnet ein Diagramm in `plot` (Element mit fester Breite).
 * generations: [{ key, label, refYear, results: { [indicatorId]: valueFor-Ergebnis } }]
 */
export function drawChart(plot, row, generations, width) {
  const members = row.members;
  const isEvent = members[0].type === "event";
  const dataYears = [...new Set(members.flatMap((m) => knownYears(m.series)))].sort((a, b) => a - b);
  const refYears = generations.map((g) => g.refYear);
  const [x0, x1] = xDomain(dataYears, refYears);
  const values = members.flatMap((m) => Object.values(m.series).filter((v) => v !== null));
  const { domain: [y0, y1], ticks } = yScale(Math.min(...values), Math.max(...values));

  const plotWidth = Math.max(width - MARGIN.left - MARGIN.right, 80);
  const height = MARGIN.top + PLOT_HEIGHT + MARGIN.bottom;
  const x = (year) => MARGIN.left + ((year - x0) / Math.max(x1 - x0, 1)) * plotWidth;
  const y = (value) => MARGIN.top + (1 - (value - y0) / (y1 - y0)) * PLOT_HEIGHT;
  const plotTop = MARGIN.top;
  const plotBottom = MARGIN.top + PLOT_HEIGHT;
  const halfYear = plotWidth / Math.max(x1 - x0, 1) / 2;

  const root = svg("svg", {
    width,
    height,
    viewBox: `0 0 ${width} ${height}`,
    class: "chart-svg",
    role: "img",
    tabindex: "0",
    "aria-label": `${row.label}, ${dataYears[0]} bis ${dataYears.at(-1)}. Markiert: ${generations
      .map((g) => `${g.label} ${g.refYear}`)
      .join(", ")}. Pfeiltasten zeigen einzelne Jahre.`,
  });

  // Gitter und Y-Achse
  for (const tick of ticks) {
    root.append(svg("line", { class: "grid", x1: MARGIN.left, x2: MARGIN.left + plotWidth, y1: y(tick), y2: y(tick) }));
    root.append(svg("text", { class: "tick", x: MARGIN.left - 6, y: y(tick), "text-anchor": "end", "dominant-baseline": "middle" }, TICK_FORMAT.format(tick)));
  }

  // Bereiche ohne Daten
  const currentYear = new Date().getFullYear();
  for (const [from, to] of emptyRanges([x0, x1], dataYears)) {
    const left = Math.max(x(from) - halfYear, MARGIN.left);
    const right = Math.min(x(to) + halfYear, MARGIN.left + plotWidth);
    root.append(svg("rect", { class: "empty", x: left, y: plotTop, width: right - left, height: PLOT_HEIGHT }));
    const after = from > dataYears.at(-1);
    const ended = members.every((m) => m.ended);
    const endedText = members.some((m) => m.ended_note) ? "nicht erfasst" : "Reihe endet";
    const text = after && ended ? endedText : from > currentYear ? "Zukunft" : after ? "noch keine Daten" : "keine Daten";
    if (right - left >= text.length * 6.5 + 8) {
      root.append(svg("text", { class: "empty-label", x: (left + right) / 2, y: plotTop + 16, "text-anchor": "middle" }, text));
    }
  }

  // X-Achse
  root.append(svg("line", { class: "axis", x1: MARGIN.left, x2: MARGIN.left + plotWidth, y1: plotBottom, y2: plotBottom }));
  for (const tick of yearTicks([x0, x1], Math.max(2, Math.floor(plotWidth / 70)))) {
    root.append(svg("text", { class: "tick", x: x(tick), y: plotBottom + 18, "text-anchor": "middle" }, String(tick)));
  }

  // Methodenbrüche: feine Linie zwischen den Jahren, Beschriftung unten im Diagramm
  for (const year of [...new Set(members.flatMap((m) => (m.breaks ?? []).map((b) => b.year)))]) {
    const bx = x(year) - halfYear;
    root.append(svg("line", { class: "break", x1: bx, x2: bx, y1: plotTop, y2: plotBottom }));
    root.append(svg("text", { class: "break-label", x: bx + 4, y: plotBottom - 6 }, `Methodenwechsel ${year}`));
  }

  // Stichjahre: Beschriftung oben, Linie durch das Diagramm
  generations.forEach((g, i) => {
    const gx = x(g.refYear);
    const labelY = 12 + i * LABEL_ROW;
    root.append(svg("line", { class: `ref ref-${g.key}`, x1: gx, x2: gx, y1: labelY + 5, y2: plotBottom }));
    root.append(svg("circle", { class: `ref-dot ref-${g.key}`, cx: gx, cy: labelY, r: 4 }));
    const text = `${g.label} ${g.refYear}`;
    const flip = gx + 8 + text.length * 6.5 > width;
    root.append(
      svg("text", { class: "ref-label", x: flip ? gx - 8 : gx + 8, y: labelY, "text-anchor": flip ? "end" : "start", "dominant-baseline": "middle" }, text),
    );
  });

  // Datenreihen
  members.forEach((m, i) => {
    const cls = `series series-${i}`;
    if (isEvent) {
      for (const year of knownYears(m.series)) {
        root.append(svg("circle", { class: `${cls} point`, cx: x(year), cy: y(m.series[year]), r: 4 }));
      }
      return;
    }
    for (const part of segments(m.series, (m.breaks ?? []).map((b) => b.year))) {
      if (part.length === 1) {
        root.append(svg("circle", { class: `${cls} point`, cx: x(part[0][0]), cy: y(part[0][1]), r: 2 }));
      } else {
        const d = part.map(([yr, v], j) => `${j ? "L" : "M"}${x(yr).toFixed(1)},${y(v).toFixed(1)}`).join("");
        root.append(svg("path", { class: `${cls} line`, d }));
      }
    }
  });

  // Beschriftung am Linienende nur, wenn alle Labels passen und sich nicht berühren;
  // sonst trägt die Legende die Zuordnung (Labels werden nie gestapelt oder abgeschnitten).
  if (members.length > 1 && !isEvent) {
    const labels = members.map((m) => {
      const last = knownYears(m.series).at(-1);
      return { text: memberName(m, members), x: x(last) + 6, y: y(m.series[last]) };
    });
    const fits = labels.every((l) => l.x + l.text.length * 6.5 <= width);
    const apart = labels.every((a, i) => labels.every((b, j) => i === j || Math.abs(a.y - b.y) >= 14));
    if (fits && apart) {
      for (const l of labels) {
        root.append(svg("text", { class: "end-label", x: l.x, y: l.y, "dominant-baseline": "middle" }, l.text));
      }
    }
  }

  // Werte der Stichjahre (bei Wahlen: die gewählte Wahl) in Generationsfarbe
  for (const g of generations) {
    for (const m of members) {
      const result = g.results[m.id];
      if (result.status !== "ok") continue;
      root.append(svg("circle", { class: `hit ref-${g.key}`, cx: x(result.year), cy: y(result.value), r: 5 }));
    }
  }

  // Hover- und Tastaturebene
  const crosshair = svg("line", { class: "crosshair", y1: plotTop, y2: plotBottom, visibility: "hidden" });
  root.append(crosshair);
  const overlay = svg("rect", { class: "overlay", x: MARGIN.left - halfYear, y: plotTop, width: plotWidth + 2 * halfYear, height: PLOT_HEIGHT });
  root.append(overlay);

  const tooltip = html("div", { class: "tooltip", hidden: "" });
  const eventYears = dataYears;
  let activeYear = null;

  function show(year) {
    activeYear = year;
    const px = x(year);
    crosshair.setAttribute("x1", px);
    crosshair.setAttribute("x2", px);
    crosshair.setAttribute("visibility", "visible");
    const rows = members.map((m) => {
      const v = m.series[year];
      const text = v === undefined || v === null ? "keine Daten" : formatValue(m, v);
      return html(
        "div",
        { class: "tooltip-row" },
        html("span", { class: `key key-${members.indexOf(m)}` }),
        html("strong", {}, text),
        members.length > 1 ? html("span", {}, ` ${memberName(m, members)}`) : null,
      );
    });
    tooltip.replaceChildren(html("div", { class: "tooltip-year" }, isEvent ? `Wahl ${year}` : String(year)), ...rows);
    tooltip.hidden = false;
    const tipWidth = tooltip.offsetWidth;
    tooltip.style.left = `${Math.min(Math.max(px + 12, 0), width - tipWidth - 4)}px`;
    if (px + 12 + tipWidth > width) tooltip.style.left = `${Math.max(px - tipWidth - 12, 0)}px`;
    tooltip.style.top = `${plotTop}px`;
  }

  function hide() {
    activeYear = null;
    crosshair.setAttribute("visibility", "hidden");
    tooltip.hidden = true;
  }

  function yearAt(clientX) {
    const box = root.getBoundingClientRect();
    const raw = x0 + ((clientX - box.left - MARGIN.left) / plotWidth) * (x1 - x0);
    const year = Math.min(Math.max(Math.round(raw), x0), x1);
    return isEvent ? nearestYear(eventYears, year) : year;
  }

  overlay.addEventListener("pointermove", (e) => show(yearAt(e.clientX)));
  overlay.addEventListener("pointerleave", hide);
  root.addEventListener("blur", hide);
  root.addEventListener("keydown", (e) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) return;
    e.preventDefault();
    const steps = isEvent ? eventYears : Array.from({ length: x1 - x0 + 1 }, (_, i) => x0 + i);
    let index = activeYear === null ? steps.length - 1 : steps.indexOf(activeYear);
    if (e.key === "ArrowLeft") index = Math.max(index - 1, 0);
    if (e.key === "ArrowRight") index = Math.min(index + 1, steps.length - 1);
    if (e.key === "Home") index = 0;
    if (e.key === "End") index = steps.length - 1;
    show(steps[index]);
  });

  plot.replaceChildren(root, tooltip);
}

function valueTable(row) {
  const members = row.members;
  const years = [...new Set(members.flatMap((m) => Object.keys(m.series)))].sort();
  return html(
    "details",
    { class: "chart-table" },
    html("summary", {}, "Alle Werte als Tabelle"),
    html(
      "table",
      {},
      html("thead", {}, html("tr", {}, html("th", { scope: "col" }, members[0].type === "event" ? "Wahl" : "Jahr"), ...members.map((m) => html("th", { scope: "col" }, memberName(m, members))))),
      html(
        "tbody",
        {},
        ...years.map((year) =>
          html(
            "tr",
            {},
            html("th", { scope: "row" }, year),
            ...members.map((m) => {
              if (m.series[year] == null) return html("td", {}, "keine Daten");
              const ats = schillingNote(m, year);
              return html("td", {}, formatValue(m, m.series[year]), ats ? ` (${ats})` : null);
            }),
          ),
        ),
      ),
    ),
  );
}

function legend(row) {
  if (row.members.length < 2) return null;
  return html(
    "p",
    { class: "chart-legend" },
    ...row.members.map((m, i) => html("span", {}, html("span", { class: `key key-${i}` }), memberName(m, row.members))),
  );
}

const observers = new WeakMap();

/** Baut für jede Anzeigezeile ein Diagramm in `container` und zeichnet bei Größenänderung neu. */
export function renderCharts(container, rows, generations) {
  container.querySelectorAll(".chart-plot").forEach((plot) => observers.get(plot)?.disconnect());
  const articles = rows.map((row) => {
    const plot = html("div", { class: "chart-plot" });
    const unit = row.members[0].unit;
    const article = html(
      "article",
      { class: "chart", id: `chart-${row.id}` },
      html("h3", {}, row.label),
      html("p", { class: "chart-unit" }, unit),
      legend(row),
      plot,
      valueTable(row),
    );
    const observer = new ResizeObserver(([entry]) => {
      const width = Math.floor(entry.contentRect.width);
      if (width > 0 && String(width) !== plot.dataset.width) {
        plot.dataset.width = width;
        drawChart(plot, row, generations, width);
      }
    });
    observer.observe(plot);
    observers.set(plot, observer);
    return article;
  });
  container.replaceChildren(...articles);
}
