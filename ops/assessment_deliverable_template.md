# AECai Discovery Assessment — Deliverable Template

**Client:** [Firm Name]
**Prepared by:** Kyle Vines, PE — Echology, Inc.
**Date:** [Date]
**Document Sample:** [N] documents provided by [Firm Name]

---

## Executive Summary

Echology processed [N] documents from [Firm Name]'s project archive through the AECai pipeline. This report summarizes what the system found — every standard referenced, obligations flagged, entities extracted, and risk areas identified. No data left your building during this assessment.

### Key Findings

| Metric | Value |
|--------|-------|
| Documents processed | [N] |
| Formats parsed | [list: PDF, DOCX, etc.] |
| Standards detected | [N] unique references |
| Obligations flagged | [N] "shall" clauses / mandatory requirements |
| Entities extracted | [N] (people, orgs, dates, financial terms) |
| Risk indicators | [N] items across [N] risk categories |
| Processing time | [N] seconds total |

---

## 1. Document Inventory

Every document classified by type, domain, and authority level.

| # | Filename | Type | Domain(s) | Authority Level | Confidence |
|---|----------|------|-----------|-----------------|------------|
| 1 | [filename] | [spec/contract/report/...] | [structural, geotech, ...] | [mandatory/directive/informational] | [high/medium/low] |

---

## 2. Standards Cross-Reference

Every standard referenced in your documents, cross-checked against jurisdiction adoptions.

| Standard | Edition | References | Jurisdiction Status | Notes |
|----------|---------|------------|---------------------|-------|
| ASTM C150 | [year] | [N] docs | [Adopted / Superseded / Not adopted] | [any amendments] |
| ACI 318 | [year] | [N] docs | [status] | |

**Jurisdiction:** [State/AHJ], building code edition [IBC year], amendments [if any].

### Flagged Issues
- [Standard X referenced but superseded by Y in this jurisdiction]
- [Standard Z not adopted by AHJ — verify applicability]

---

## 3. Obligations & Risk Flags

Mandatory requirements, liability traps, and deadline risks extracted from your documents.

### Mandatory Requirements ("shall" clauses)

| # | Source Document | Clause | Risk Level | Context |
|---|----------------|--------|------------|---------|
| 1 | [filename, page N] | "[The contractor shall...]" | [safety_critical/compliance/financial] | [surrounding context] |

### Contractual Obligations

| # | Source Document | Obligation | Type | Due Date |
|---|----------------|------------|------|----------|
| 1 | [filename] | [Submittal required within N days] | [submittal/notice/milestone] | [date if found] |

### Financial Terms

| Term | Value | Source |
|------|-------|--------|
| Contract value | $[amount] | [filename] |
| Retainage | [%] | [filename] |
| Liquidated damages | $[amount]/day | [filename] |

---

## 4. Entity Map

People, organizations, and roles identified across your documents.

| Entity | Role | Source Documents |
|--------|------|-----------------|
| [Name] | Owner / Engineer of Record / Contractor / Sub | [filenames] |

### Sensitive Data Detected

| Type | Count | Action |
|------|-------|--------|
| PE license numbers | [N] | Flagged — excluded from AI processing |
| SSN / EIN | [N] | Flagged — excluded from AI processing |
| Contact details | [N] | Catalogued for entity mapping only |

---

## 5. Timeline & Milestones

Key dates and deadlines extracted from your documents.

| Milestone | Date | Source | Status |
|-----------|------|--------|--------|
| Notice to Proceed | [date] | [filename] | [upcoming/past] |
| Submittal deadline | [date] | [filename] | |
| Substantial completion | [date] | [filename] | |

---

## 6. Decomposition Summary

How the AECai pipeline broke your documents into structured, searchable units.

| Metric | Value |
|--------|-------|
| Total semantic units | [N] |
| Mandatory/directive units | [N] ([%] of total) |
| Informational units | [N] |
| Data/numerical units | [N] |
| Average units per document | [N] |

All units are now indexed and searchable by meaning — not just keywords. Filterable by jurisdiction, discipline, risk level, and authority.

---

## 7. What This Means for [Firm Name]

### Time Recovery
- Manual review of these [N] documents would take approximately [N] hours
- AECai processed them in [N] seconds
- At scale, this translates to [N] hours/year recovered across your project workload

### Risk Reduction
- [N] standards references were found — [N] flagged for jurisdiction verification
- [N] mandatory obligations were buried in boilerplate sections
- [Specific finding relevant to their work]

### Knowledge Capture
- [N] entities and roles mapped across documents — institutional knowledge preserved
- [N] cross-references between documents identified

---

## 8. Next Steps

This assessment credits 100% toward a full AECai engagement.

**Full engagement includes:**
- Processing your complete document archive (all active projects)
- Jurisdiction code registry configured for your AHJs
- Searchable vector index across your entire document library
- Ongoing processing of new documents as they arrive
- On-premise deployment — runs on your hardware, air-gapped

**To proceed:** Reply to this email or contact kyle@echology.io.

---

*This report was generated by AECai — a local-first document intelligence platform by Echology, Inc.*
*No data left [Firm Name]'s premises during this assessment.*
*echology.io | aecai.io*
