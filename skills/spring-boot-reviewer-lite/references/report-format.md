# Review report contract

## Scope and limits

List inspected files/change scope, detected versions, known configuration, and missing context. Say whether this is static inspection, executed tests, or both.

## Findings

Order by severity, then confidence. Merge duplicate symptoms of one root cause.

For each finding provide:

- **ID / severity / confidence / title**
- **Evidence:** exact relative path and line(s), plus the relevant behavior. Redact sensitive values.
- **Trigger and impact:** how a caller reaches the problem and what fails.
- **Minimal fix:** a concrete, scoped change; include alternatives only when needed.
- **Verification:** a reproducible check or targeted test that would fail before and pass after the fix.

| Severity | Use when evidence supports |
| --- | --- |
| Critical | Reachable, broad compromise or catastrophic data loss; exceptional, requires strong evidence. |
| High | Unauthorized access or mutation, material consistency failure, or a major reachable availability defect. |
| Medium | Incorrect behavior on a realistic path or a bounded reliability defect. |
| Low | Small but concrete functional or diagnostic impact; exclude purely stylistic advice. |

Confidence: **High** for a traced path with relevant configuration available; **Medium** when the defect follows from inspected code but some impact details remain uncertain. If the existence of the defect itself depends on unseen controls or runtime behavior, put it below instead.

If none are supported, say: **No actionable findings in the inspected scope.** This does not certify the full system.

## Needs verification

List unanswered questions separately with the exact missing evidence and why it matters. Omit if empty. Do not restate generic checklist items as questions.

## Validation performed

List commands/tests actually executed and their outcomes. Clearly label suggested tests as **not run**. State remaining coverage limits. Do not fabricate a score, passed test, vulnerability scan, benchmark, or release approval.
