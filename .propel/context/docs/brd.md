# CMS Deficiency Action Planner

## Description

**CMS Deficiency Action Planner** is a localhost MVP for nursing-home compliance and quality staff. It processes uploaded CMS-2567 documents to extract provider details, CMS F-tags, and Statements of Deficiency, then uses AI to generate grounded, editable **Plans of Correction (POCs)** for each identified deficiency. The generated POCs are reviewed, edited, and approved by authorized human users before any use or submission.

The system assists compliance staff in preparing corrective-action responses; it does not automatically submit responses to CMS or replace human compliance judgment.

## Problems & Solutions

### Problem 1: Error-Prone Manual Extraction

**Who is affected:** Nursing-home compliance and quality staff

**Impact:** Manual review can introduce transcription errors, miss deficiencies, and make source verification slow.

**How this product solves it:** Extracts provider details, F-tags, and SODs with page-level evidence and visible uncertainty.

### Problem 2: Labor-Intensive Correction-Plan Drafting

**Who is affected:** Compliance staff and authorized compliance leaders

**Impact:** Drafting separate, grounded POCs is time-consuming and may produce inconsistent responses.

**How this product solves it:** Generates structured drafts from reviewed deficiency data, identifies missing facts, and requires human editing and approval.

## Key Features

- Upload and validate CMS-2567 PDF and image-based documents.
- Extract provider details, F-tags, and multiple Statements of Deficiency.
- Use OCR when native document text is incomplete or unavailable.
- Show source pages, supporting snippets, confidence, and uncertain candidates.
- Let reviewers correct extracted fields while preserving original evidence.
- Generate a grounded, structured POC independently for each reviewed deficiency.
- Identify missing facility information instead of inventing facts.
- Distinguish extracted, AI-generated, user-edited, and approved content.
- Require authorized human approval.
- Copy or download approved content as a clearly labeled draft.

## Success Criteria

- Achieve at least 95% field-level accuracy for provider name, F-tag, and complete SOD text on a representative document set.
- Detect every deficiency in the evaluation set or surface it as an uncertain candidate for human review.
- Let reviewers verify each extracted value, source page, supporting snippet, and uncertainty without manually searching the document.
- Produce no unsupported facility-specific factual claims in evaluated POC drafts; missing information is explicitly identified.
- Preserve human review and approval for every POC.
- Deliver a usable localhost MVP within 6-8 weeks.

## Scope

**In:** Localhost MVP for nursing-home CMS-2567 documents; native, scanned, and mixed PDFs; multiple deficiencies; traceable extraction and uncertainty review; reviewer corrections; grounded POC drafting; human editing and approval; transient session state; copy/download of approved drafts; external OCR and AI processing under approved PHI-handling terms.

**Out:** Databases and persistent document management; cloud hosting; CMS submission or communication; automated compliance decisions or approval; autonomous corrective actions; multi-tenancy; enterprise authentication/SSO; advanced analytics; infrastructure automation and deployment pipelines. These are excluded to keep the MVP focused on validated extraction and review.

## Assumptions & Open Questions

| # | Item | Risk / Impact | Owner |
|---|---|---|---|
| 1 | Define the size and composition of the representative extraction test set. | The 95% accuracy target cannot be evaluated consistently without agreed ground truth. | Product owner and compliance lead |
| 2 | Confirm state-specific POC expectations in addition to federal CMS requirements. | A structurally sound draft may still omit state-required content. | Compliance or legal lead |
| 3 | Validate the five-part POC structure with practicing nursing-home compliance reviewers. | Drafts may not match the reviewers' operational process. | Compliance lead |
| 4 | Select external OCR and AI services that support PHI processing, HIPAA-compliant BAAs, risk analysis, and acceptable retention terms. | External processing could create privacy or contractual exposure. | Privacy/security owner |
| 5 | Confirm access to varied, legally usable CMS-2567 samples with verified extraction labels. | Extraction quality cannot be trained or tested credibly without representative documents. | Product owner |
| 6 | Validate differentiation from products such as EasyPOC and SkyComply, emphasizing evidence-backed extraction and uncertainty review. | The MVP may duplicate existing offerings without a compelling advantage. | Product owner |
| 7 | Confirm whether the MVP supports English-language documents only. | Unexpected languages could reduce OCR and extraction accuracy. | Product owner |
| 8 | Set the upload size and page-count limits for realistic survey documents. | Undefined limits may cause poor performance or failed processing. | Product owner and engineering lead |