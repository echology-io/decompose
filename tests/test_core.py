"""Integration tests for decompose.core — the full pipeline."""

from decompose.core import decompose_text, filter_for_llm


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
        assert meta["_decompose"] == "0.2.0"

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


# ── filter_for_llm ──────────────────────────────────────────────


class TestFilterForLlm:

    def _make_result(self, units):
        return {"units": units, "meta": {"total_units": len(units)}}

    def test_empty_input(self):
        r = filter_for_llm({"units": [], "meta": {}})
        assert r["text"] == ""
        assert r["units"] == []
        assert r["meta"]["input_units"] == 0

    def test_missing_units_key(self):
        r = filter_for_llm({})
        assert r["text"] == ""

    def test_filters_by_authority(self):
        units = [
            {"text": "Shall provide materials.", "authority": "mandatory", "risk": "informational", "type": "requirement"},
            {"text": "Background context.", "authority": "informational", "risk": "informational", "type": "narrative"},
            {"text": "Should follow practices.", "authority": "directive", "risk": "informational", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["output_units"] == 2
        assert "Shall provide" in r["text"]
        assert "Background context" not in r["text"]

    def test_filters_by_risk(self):
        units = [
            {"text": "Safety critical.", "authority": "informational", "risk": "safety_critical", "type": "narrative"},
            {"text": "General info.", "authority": "informational", "risk": "informational", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["output_units"] == 1
        assert "Safety critical" in r["text"]

    def test_filters_by_type(self):
        units = [
            {"text": "Max load 500 lbs.", "authority": "informational", "risk": "informational", "type": "constraint"},
            {"text": "Narrative text.", "authority": "informational", "risk": "informational", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["output_units"] == 1

    def test_min_attention(self):
        units = [
            {"text": "High.", "authority": "informational", "risk": "informational", "type": "narrative", "attention": 8.0},
            {"text": "Low.", "authority": "informational", "risk": "informational", "type": "narrative", "attention": 2.0},
        ]
        r = filter_for_llm(self._make_result(units), min_attention=7.0)
        assert r["meta"]["output_units"] == 1
        assert "High" in r["text"]

    def test_include_headings_true(self):
        units = [
            {"text": "Steel per AISC.", "authority": "mandatory", "risk": "informational", "type": "requirement",
             "heading": "Structural", "heading_path": ["Division 05", "Structural"]},
        ]
        r = filter_for_llm(self._make_result(units), include_headings=True)
        assert "[Division 05 > Structural]" in r["text"]

    def test_include_headings_false(self):
        units = [
            {"text": "Steel per AISC.", "authority": "mandatory", "risk": "informational", "type": "requirement",
             "heading": "Structural", "heading_path": ["Structural"]},
        ]
        r = filter_for_llm(self._make_result(units), include_headings=False)
        assert "[" not in r["text"]

    def test_max_tokens_truncation(self):
        units = [{"text": "A" * 1000, "authority": "mandatory", "risk": "informational", "type": "requirement"}]
        r = filter_for_llm(self._make_result(units), max_tokens=50)
        assert len(r["text"]) <= 200  # 50 * 4

    def test_max_tokens_zero_no_truncation(self):
        units = [{"text": "A" * 1000, "authority": "mandatory", "risk": "informational", "type": "requirement"}]
        r = filter_for_llm(self._make_result(units), max_tokens=0)
        assert len(r["text"]) == 1000

    def test_reduction_pct(self):
        units = [
            {"text": "Keep.", "authority": "mandatory", "risk": "informational", "type": "requirement"},
            {"text": "Drop.", "authority": "informational", "risk": "informational", "type": "narrative"},
            {"text": "Drop.", "authority": "informational", "risk": "informational", "type": "narrative"},
            {"text": "Drop.", "authority": "informational", "risk": "informational", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["reduction_pct"] == 75

    def test_token_estimate(self):
        units = [{"text": "A" * 400, "authority": "mandatory", "risk": "informational", "type": "requirement"}]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["token_estimate"] == 100

    def test_custom_authorities(self):
        units = [
            {"text": "Mandatory.", "authority": "mandatory", "risk": "informational", "type": "narrative"},
            {"text": "Permissive.", "authority": "permissive", "risk": "informational", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units), authorities=("permissive",), risks=(), types=())
        assert r["meta"]["output_units"] == 1
        assert "Permissive" in r["text"]

    def test_or_logic(self):
        """Units matching ANY criterion are included."""
        units = [
            {"text": "Financial risk.", "authority": "informational", "risk": "financial", "type": "narrative"},
        ]
        r = filter_for_llm(self._make_result(units))
        assert r["meta"]["output_units"] == 1

    def test_end_to_end(self):
        text = (
            "The contractor shall provide all steel per ASTM A992. "
            "This is general background information about the project. "
            "Maximum concrete strength shall not exceed 6000 psi."
        )
        dr = decompose_text(text)
        r = filter_for_llm(dr)
        assert r["meta"]["input_units"] >= 1
        assert r["meta"]["output_units"] >= 1
        assert len(r["text"]) > 0
