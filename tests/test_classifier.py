"""Tests for decompose.classifier."""

from decompose.classifier import classify


class TestAuthority:
    def test_shall_is_mandatory(self):
        c = classify("The contractor shall provide all materials.")
        assert c.authority == "mandatory"
        assert c.authority_score > 0

    def test_must_is_mandatory(self):
        c = classify("All work must comply with specifications.")
        assert c.authority == "mandatory"

    def test_shall_not_is_prohibitive(self):
        c = classify("The contractor shall not modify the existing structure.")
        assert c.authority == "prohibitive"

    def test_should_is_directive(self):
        c = classify("The engineer should review all calculations.")
        assert c.authority == "directive"

    def test_may_is_permissive(self):
        c = classify("The owner may request additional inspections.")
        assert c.authority == "permissive"

    def test_informational_text(self):
        c = classify("For information only: project background notes.")
        assert c.authority == "informational"

    def test_plain_text_defaults_informational(self):
        c = classify("The sky is blue today.")
        assert c.authority == "informational"

    # ── v0.2.0: Backported patterns from AECai ──

    def test_shall_conform_is_mandatory(self):
        c = classify("Materials shall conform to ASTM standards.")
        assert c.authority == "mandatory"

    def test_will_be_required_is_mandatory(self):
        c = classify("A permit will be required before construction begins.")
        assert c.authority == "mandatory"

    def test_forbidden_is_prohibitive(self):
        c = classify("Open flames are forbidden in the storage area.")
        assert c.authority == "prohibitive"

    def test_under_no_circumstances_is_prohibitive(self):
        c = classify("Under no circumstances is welding permitted in the storage area.")
        assert c.authority == "prohibitive"

    def test_is_to_is_directive(self):
        c = classify("The inspector is to verify all welds before covering.")
        assert c.authority == "directive"

    def test_at_discretion_is_permissive(self):
        c = classify("Additional testing at the discretion of the engineer.")
        assert c.authority == "permissive"

    def test_except_where_is_conditional(self):
        c = classify("All joints shall be welded except where bolted connections are specified.")
        assert c.authority in ("mandatory", "conditional")

    def test_in_the_event_is_conditional(self):
        c = classify("In the event of failure, the contractor shall notify the owner.")
        assert c.authority in ("mandatory", "conditional")

    def test_fyi_is_informational(self):
        c = classify("FYI — the schedule has been updated with new milestones.")
        assert c.authority == "informational"


class TestRisk:
    def test_safety_critical_detected(self):
        c = classify("Life safety systems shall be inspected. Seismic load analysis required.")
        assert c.risk == "safety_critical"

    def test_compliance_detected(self):
        c = classify("Shall comply with code requirements. Inspection shall be performed.")
        assert c.risk == "compliance"

    def test_financial_detected(self):
        c = classify("Contract value of $1,500,000 with 10% retainage.")
        assert c.risk == "financial"

    def test_contractual_detected(self):
        c = classify("Indemnification clause. Liability limitations. Warranty period of 2 years.")
        assert c.risk == "contractual"


class TestAttention:
    def test_safety_critical_gets_high_attention(self):
        c = classify("The contractor shall ensure life safety. Seismic design must comply.")
        assert c.attention > 5.0

    def test_informational_gets_low_attention(self):
        c = classify("The sky is blue today.")
        assert c.attention == 0.0

    def test_actionable_for_mandatory(self):
        c = classify("The contractor shall submit shop drawings.")
        assert c.actionable is True

    def test_not_actionable_for_narrative(self):
        c = classify("The project has a long history of community involvement.")
        assert c.actionable is False
