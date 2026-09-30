# Navigation Map - CMS Deficiency Action Planner

## Flow Index

| Flow | Entry | Path | Decision or Recovery |
|---|---|---|---|
| FL-002 Upload through review | SCR-002 | SCR-002 -> SCR-003 -> SCR-004 <-> SCR-005 | Invalid input returns to SCR-002; processing failure retries on SCR-003 |
| FL-003 Generate and edit POC | SCR-004 | SCR-004 -> SCR-006 -> SCR-007 | Incomplete draft remains on SCR-006 |
| FL-004 Approve and export | SCR-007 | SCR-007 -> SCR-008 | Request changes returns to SCR-006 |
| FL-005 End session | SCR-002 or SCR-008 | Confirmation -> SCR-002 empty | Cancel returns focus to trigger |
| FL-006 Recover processing | SCR-003 or SCR-006 | Error -> retry -> review-ready | Replacement required returns to SCR-002 |

## Screen-to-Screen Links

| Source | Trigger | Target | Related UC |
|---|---|---|---|
| SCR-002 | Upload CMS-2567 | SCR-003 | UC-001, UC-002 |
| SCR-003 | Open extraction review | SCR-004 | UC-002 |
| SCR-004 | Resolve uncertain values | SCR-005 | UC-003 |
| SCR-005 | Resolve or leave unresolved | SCR-004 | UC-003, UC-004 |
| SCR-004 | Generate POC | SCR-006 | UC-005 |
| SCR-006 | Send for approval | SCR-007 | UC-006, UC-007 |
| SCR-007 | Request changes | SCR-006 | UC-006, UC-007 |
| SCR-007 | Approve current revision | SCR-008 | UC-007, UC-008 |
| SCR-008 | Return to POC drafts | SCR-006 | UC-006 |
| SCR-008 | End session and remove data | SCR-002 | UC-009 |

## Dead Ends and Exceptions

- No canonical screen is an undocumented dead end.
- SCR-008 is the success endpoint but retains outbound actions to drafts and session cleanup.
- Invalid credentials, validation errors, and retryable failures intentionally remain on the current screen.
- External CMS submission is excluded; export ends with local copy or download.