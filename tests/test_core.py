"""Integration tests for decompose.core — the full pipeline."""

from decompose.core import decompose_text


class TestDecomposeText:
    def test_empty_input(self):
        r = decompose_text("")
        assert r["units"] == []
        assert r["meta"]["total_units"] == 0

    def test_simple_text(self):
        r = decompose_text("The contractor shall provide all materials per ASTM C150-20.")
        assert r["meta"]["total_units"] == 1
        unit = r["units"][0]
        assert unit["authority"] == "mandatory"
        assert unit["irreducible"] is True
        assert "ASTM" in str(unit.get("entities", []))

    def test_multi_unit_output(self):
        text = "# Requirements\nShall comply with IBC 2021.\n# Background\nGeneral project notes."
        r = decompose_text(text)
        assert r["meta"]["total_units"] >= 2

    def test_meta_includes_profiles(self):
        r = decompose_text("The contractor shall provide materials. The owner may inspect.")
        meta = r["meta"]
        assert "authority_profile" in meta
        assert "risk_profile" in meta
        assert "processing_ms" in meta
        assert meta["_decompose"] == "0.1.0"

    def test_compact_mode(self):
        r = decompose_text("General background information.", compact=True)
        unit = r["units"][0]
        # Compact should omit empty entity lists
        assert "entities" not in unit or unit.get("entities")

    def test_standards_collected_in_meta(self):
        text = "Per ASTM A615 and ACI 318-19, all rebar shall be Grade 60."
        r = decompose_text(text)
        assert len(r["meta"]["standards_found"]) >= 2

    def test_token_reduction_calculated(self):
        text = "The contractor shall do things. " * 100
        r = decompose_text(text)
        assert "token_estimate" in r["meta"]
        assert r["meta"]["token_estimate"]["input"] > 0

    def test_safety_critical_text(self):
        text = (
            "Life safety systems shall be maintained. Seismic design shall comply "
            "with ASCE 7-22. Structural collapse prevention is mandatory."
        )
        r = decompose_text(text)
        unit = r["units"][0]
        assert unit["risk"] == "safety_critical"
        assert unit["attention"] > 5.0

    def test_financial_text(self):
        text = "Contract value: $2,500,000. Retainage: 10%. Liquidated damages of $500 per day."
        r = decompose_text(text)
        unit = r["units"][0]
        assert unit["risk"] == "financial"
        assert len(unit.get("financial", [])) >= 2
