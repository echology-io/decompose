"""Tests for decompose.entities."""

from decompose.entities import extract_entities


class TestStandards:
    def test_detects_international_standards(self):
        e = extract_entities("Per ISO 9001:2015 and EN 1992-1.")
        assert any("ISO" in s for s in e.standards)

    def test_detects_ieee(self):
        e = extract_entities("Comply with IEEE 802.11 and ANSI C12.1.")
        assert any("IEEE" in s for s in e.standards)
        assert any("ANSI" in s for s in e.standards)

    def test_detects_ul(self):
        e = extract_entities("Listed per UL 489 and ASME B31.1.")
        assert any("UL" in s for s in e.standards)
        assert any("ASME" in s for s in e.standards)

    def test_detects_usc_references(self):
        e = extract_entities("Pursuant to 42 U.S.C. 7401 (Clean Air Act).")
        assert any("U.S.C" in r for r in e.references)

    def test_detects_cfr_references(self):
        e = extract_entities("Per 40 C.F.R. Part 122 requirements.")
        assert any("C.F.R" in r for r in e.references)


class TestDates:
    def test_detects_mdy_dates(self):
        e = extract_entities("Submitted on 01/15/2026.")
        assert "01/15/2026" in e.dates

    def test_detects_written_dates(self):
        e = extract_entities("Due by January 15, 2026.")
        assert any("January" in d for d in e.dates)


class TestFinancial:
    def test_detects_dollar_amounts(self):
        e = extract_entities("Contract value: $1,500,000.00")
        assert any("1,500,000" in f for f in e.financial)

    def test_detects_percentages(self):
        e = extract_entities("Retainage of 10% applies.")
        assert "10%" in e.financial

    def test_deduplicates(self):
        e = extract_entities("$500 here and $500 there.")
        assert e.financial.count("$500") == 1
