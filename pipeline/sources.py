"""Register der Rohdateien in data/raw/. Spiegelt data/SOURCES.md."""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
MANUAL = ROOT / "data" / "manual"


@dataclass(frozen=True)
class Source:
    file: str
    url: str
    retrieved: str
    label: str

    @property
    def path(self):
        return RAW / self.file


_STAT = "https://www.statistik.at/fileadmin/pages"
_OGD = "https://data.statistik.gv.at/data"
_BMI = "https://www.bmi.gv.at/412/Nationalratswahlen"

SOURCES = {
    "zeitreihen": Source(
        "statistik_austria_OEsterreich_Zeitreihenindikatoren_1961_2025.ods",
        f"{_STAT}/411/OEsterreich_Zeitreihenindikatoren_1961_2025.ods",
        "2026-10-23",
        "Statistik Austria, Demographische Indikatoren, Zeitreihen 1961 bis 2025 (Österreich)",
    ),
    "lebenserwartung": Source(
        "statistik_austria_Lebenserwartung_fuer_ausgewaehlte_Altersjahre_1868_71_bis_2020_22_sowie_1951_2025.ods",
        f"{_STAT}/413/Lebenserwartung_fuer_ausgewaehlte_Altersjahre_1868_71_bis_2020_22_sowie_1951_2025.ods",
        "2026-10-23",
        "Statistik Austria, Sterbetafeln: Lebenserwartung für ausgewählte Altersjahre 1951 bis 2025",
    ),
    "vpi_lhki38": Source(
        "statistik_austria_OGD_vpilhki38_VPI_LHKI38_1.csv",
        f"{_OGD}/OGD_vpilhki38_VPI_LHKI38_1.csv",
        "2026-10-23",
        "Statistik Austria, Open Data: Lebenshaltungskostenindex 1938 (verkettet), OGD_vpilhki38_VPI_LHKI38_1",
    ),
    "vpi_lhki38_zeitraum": Source(
        "statistik_austria_OGD_vpilhki38_VPI_LHKI38_1_C-VPIZR-0.csv",
        f"{_OGD}/OGD_vpilhki38_VPI_LHKI38_1_C-VPIZR-0.csv",
        "2026-10-23",
        "Metadaten Zeitraum zu OGD_vpilhki38_VPI_LHKI38_1",
    ),
    "vpi_lhki38_indizes": Source(
        "statistik_austria_OGD_vpilhki38_VPI_LHKI38_1_C-VPI1-0.csv",
        f"{_OGD}/OGD_vpilhki38_VPI_LHKI38_1_C-VPI1-0.csv",
        "2026-10-23",
        "Metadaten Indizes zu OGD_vpilhki38_VPI_LHKI38_1",
    ),
    "vpi_lhki38_header": Source(
        "statistik_austria_OGD_vpilhki38_VPI_LHKI38_1_HEADER.csv",
        f"{_OGD}/OGD_vpilhki38_VPI_LHKI38_1_HEADER.csv",
        "2026-10-23",
        "Metadaten Spalten zu OGD_vpilhki38_VPI_LHKI38_1",
    ),
    "vpi_ab_1990": Source(
        "statistik_austria_2_Verbraucherpreisindizes_ab_1990.ods",
        f"{_STAT}/214/2_Verbraucherpreisindizes_ab_1990.ods",
        "2026-10-23",
        "Statistik Austria, Verbraucherpreisindizes ab 1990 (Kontrollreihe)",
    ),
    "einkommen": Source(
        "statistik_austria_1_brutto-_und_nettojahreseinkommen_der_unselbstaendig_erwerbstaetigen_1997_bis_2024_020054.ods",
        f"{_STAT}/333/1_brutto-_und_nettojahreseinkommen_der_unselbstaendig_erwerbstaetigen_1997_bis_2024_020054.ods",
        "2026-10-23",
        "Statistik Austria, Lohnsteuerdaten: Brutto- und Nettojahreseinkommen der unselbständig Erwerbstätigen 1997 bis 2024",
    ),
    "nrw_1919_2008": Source(
        "bmi_nrw_08_wbseit1919.pdf",
        f"{_BMI}/Nationalratswahl_2008/files/history/nrw_08_wbseit1919.pdf",
        "2026-10-23",
        "BMI, Nationalratswahl 2008, Tabelle 6.a. Wahlberechtigte seit 1919",
    ),
    "nrw_2013": Source(
        "bmi_nrw13_endgueltiges_gesamtergebnis.xlsx",
        f"{_BMI}/Nationalratswahl_2013/files/nrw13_endgueltiges_gesamtergebnis.xlsx",
        "2026-10-23",
        "BMI, Nationalratswahl 2013, endgültiges Gesamtergebnis",
    ),
    "nrw_2017": Source(
        "bmi_nrw17_endgueltiges_gesamtergebnis.xlsx",
        f"{_BMI}/Nationalratswahl_2017/files/nrw17_endgueltiges_gesamtergebnis.xlsx",
        "2026-10-23",
        "BMI, Nationalratswahl 2017, endgültiges Gesamtergebnis",
    ),
    "nrw_2019": Source(
        "bmi_nrw19_endgultiges_gesamtergebnis_16102019.xlsx",
        f"{_BMI}/Nationalratswahl_2019/files/endgultiges_gesamtergebnis_nrw19_16102019.xlsx",
        "2026-10-23",
        "BMI, Nationalratswahl 2019, endgültiges Gesamtergebnis",
    ),
    "nrw_2024": Source(
        "bmi_nrw24_endgueltiges_ergebnis_16102024.xlsx",
        f"{_BMI}/Nationalratswahl_2024/files/endgueltiges_ergebnis_beschluss_bundeswahlbehoerde_16102024.xlsx",
        "2026-10-23",
        "BMI, Nationalratswahl 2024, endgültiges Ergebnis",
    ),
}
