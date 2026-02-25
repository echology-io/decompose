"""Tests for decompose.entities."""

from decompose.entities import extract_entities


class TestStandards:
    def test_detects_us_standards(self):
        e = extract_entities("Materials per ASTM C150-20 and ACI 318-19.")
        assert any("ASTM" in s for s in e.standards)
        assert any("ACI" in s for s in e.standards)

    def test_detects_building_codes(self):
        e = extract_entities("Comply with IBC 2021 and NEC 2023.")
        assert any("IBC" in s for s in e.standards)
        assert any("NEC" in s for s in e.standards)

    def test_detects_international_standards(self):
        e = extract_entities("Per ISO 9001:2015 and EN 1992-1.")
        assert any("ISO" in s for s in e.standards)

    def test_detects_osha(self):
        e = extract_entities("OSHA 1926.502 fall protection.")
        assert any("OSHA" in s for s in e.standards)


    # ── v0.2.0: Backported patterns from AECai ──

    def test_detects_military_standards(self):
        e = extract_entities("Design per UFC 3-600-01 and USACE 1110-2-1902.")
        assert any("UFC" in s for s in e.standards)
        assert any("USACE" in s for s in e.standards)

    def test_detects_additional_bodies(self):
        e = extract_entities("Roofing per SMACNA 1006 and NRCA guidelines.")
        assert any("SMACNA" in s for s in e.standards)

    def test_detects_state_dot(self):
        e = extract_entities("Per CA DOT Section 51.1 requirements.")
        assert any("DOT" in s for s in e.standards)

    def test_detects_usc_references(self):
        e = extract_entities("Pursuant to 42 U.S.C. 7401 (Clean Air Act).")
        assert any("U.S.C" in r for r in e.references)


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
