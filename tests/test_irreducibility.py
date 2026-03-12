"""Tests for decompose.irreducibility."""

from decompose.irreducibility import detect_irreducibility


class TestIrreducibility:
    def test_legal_mandate_is_irreducible(self):
        text = (
            "The vendor shall provide all materials per specification no. 12345. "
            "Maximum weight shall not exceed 500 lb. "
            "Warranty obligations per ARTICLE 5.2 apply."
        )
        r = detect_irreducibility(text)
        assert r.irreducible is True
        assert r.recommendation == "PRESERVE_VERBATIM"
        assert r.match_count >= 3

    def test_measured_values_are_irreducible(self):
        text = "Weight limit: 4000 lb. Distance: 50 km. Height: 100 ft."
        r = detect_irreducibility(text)
        assert r.irreducible is True
        assert "measured_value" in r.categories

    def test_financial_values_are_irreducible(self):
        text = "Contract amount: $1,250,000.00 due upon completion."
        r = detect_irreducibility(text)
        assert r.irreducible is True
        assert "financial_value" in r.categories

    def test_simple_text_is_summarizable(self):
        text = "This is general background information about the project."
        r = detect_irreducibility(text)
        assert r.irreducible is False
        assert r.recommendation == "SUMMARIZABLE"

    def test_confidence_scales_with_matches(self):
        low = detect_irreducibility("The maximum value is 10 ft.")
        high = detect_irreducibility(
            "Shall provide materials per spec no. 123. Maximum 500 lb. "
            "ARTICLE 5.2 warranty. Liability clause. NOT TO EXCEED 1000 kg."
        )
        assert high.confidence > low.confidence
