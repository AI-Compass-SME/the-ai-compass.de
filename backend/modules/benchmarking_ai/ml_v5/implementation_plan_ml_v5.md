# Implementation Plan - ML v5

## Goal
Evolve `ml_v4` into `ml_v5` by adding **detailed explanations** for each roadmap recommendation. Currently, the roadmap shows only theme names (e.g., "Staff Proficiency"), but users need context on **what each recommendation means** and **how to address it**.

## User Review Required
> [!IMPORTANT]
> **Roadmap Enhancement Strategy**: I will add a new method `generate_recommendation_explanations()` to the `RoadmapGenerator` that provides business-focused explanations for each tactical theme. This can either:
> 1. **Replace** the current simple briefing with a richer, per-item explanation
> 2. **Augment** the current briefing by adding an `explanation` field to each recommendation item

I recommend **Option 2 (Augment)** to maintain backward compatibility while adding value.

## Proposed Changes

### [Copy] ml_v4 → ml_v5
All files from `ml_v4` will be copied to `ml_v5` as the starting point.

---

### [MODIFY] `benchmarking_ai/ml_v5/models.py`

#### RoadmapGenerator Enhancements

**New Method: `_generate_explanation(theme, dimension, source, company_scores, peer_avg_scores)`**
- **Purpose**: Generate a business-focused explanation for why this recommendation matters
- **Logic**:
  - For **Strategic Gap (Critical)** items: Explain the current weakness and its business impact
  - For **Growth Opportunity** items: Explain the peer advantage and potential ROI
  - Use dimension scores to provide specific context (e.g., "Your score of 2.6 vs peer average of 3.8")
  - Reference the tactical theme to make it actionable

**Modified Method: `generate()`**
- Add `explanation` field to each recommendation item in the roadmap
- Call `_generate_explanation()` for each item
- Store peer average scores during `fit()` for comparison

**Example Output Structure**:
```python
{
  "theme": "Staff Proficiency",
  "source": "Strategic Gap (Critical)",
  "impact_score": 11.2,
  "dimension": "People & Culture",
  "explanation": "Your team's AI proficiency (score: 1.8) is significantly below industry standards. Investing in upskilling programs will enable your staff to effectively leverage AI tools, reducing implementation friction and accelerating ROI. Peer companies at your target maturity level average 3.2 in this area."
}
```

---

### [MODIFY] `benchmarking_ai/ml_v5/utils.py`

**New Function: `generate_theme_explanation_template(theme, context)`**
- **Purpose**: Provide explanation templates for common tactical themes
- **Logic**: Map tactical themes to explanation patterns
- **Example**:
  ```python
  THEME_EXPLANATIONS = {
      "Staff Proficiency": "Upskilling your team in AI capabilities...",
      "Leadership Alignment": "Ensuring executive buy-in and strategic clarity...",
      "Data Privacy": "Establishing robust data governance frameworks..."
  }
  ```

---

### [MODIFY] `benchmarking_ai/ml_v5/inference.py`

**No changes required** - The `run_analysis()` method already returns the roadmap structure, which will now include explanations.

---

### [NEW] `benchmarking_ai/ml_v5/sample_frontend_response.json`

Update the sample to show the new `explanation` field in each roadmap recommendation.

---

## Verification Plan

### Automated Verification
- **Unit Test**: `tests/test_roadmap_explanations.py`
  - Verify that every recommendation has an `explanation` field
  - Verify explanations are non-empty and contextual
  - Verify explanations reference actual scores when available

### Manual Verification
- Run `verify_representatives.py` on the 5 cluster representatives
- Generate updated `cluster_representative_test_findings.md`
- **Success Criteria**: Each roadmap item should have a 2-3 sentence explanation that:
  1. States the current gap/opportunity
  2. Explains the business impact
  3. References peer benchmarks where applicable
