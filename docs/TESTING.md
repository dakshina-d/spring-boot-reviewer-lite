# Test with Codex and Kiro

Use the same fixture and comparable settings to compare assistants. Record the client version, selected model, date, discovery method, and raw response. Keep this guide and the answer rubric outside the reviewer context.

## 1. Prepare a separate demo

From the downloaded repository root in Windows PowerShell, create a new directory next to the repository. If the directory exists, choose a different name:

```powershell
$demo = Join-Path (Split-Path -Parent (Get-Location).Path) 'spring-reviewer-demo'
if (Test-Path -LiteralPath $demo) { throw 'Demo already exists. Choose another name.' }
New-Item -ItemType Directory -Path $demo | Out-Null
Copy-Item -Recurse -LiteralPath '.\examples\checkout' -Destination $demo
Copy-Item -Recurse -LiteralPath '.\examples\orders' -Destination $demo
python tools/install.py --client codex kiro --project "$demo"
```

Open that demo directory as the workspace in your Codex IDE integration or Kiro. If using Codex CLI, enter the demo folder and launch your configured Codex client. It should not need to build or execute the Java snippets. Python is only needed for installation; alternatively copy the skill manually as described in the README.

## 2. Run a fresh checkout review

In Codex chat:

```text
$spring-boot-reviewer-lite Review checkout. Read checkout/CONTEXT.md
and its Java files. Load the skill's checklist and report format.
Review only the stated scope. Do not modify files or run the application.
```

In a separate fresh Kiro chat:

```text
/spring-boot-reviewer-lite Review checkout. Read checkout/CONTEXT.md
and its Java files. Load the skill's checklist and report format.
Review only the stated scope. Do not modify files or run the application.
```

Confirm the client actually loaded the skill and references in its activity/tool trace when available. If the slash command is absent, check the installation and Kiro custom-agent resources note before switching to a manual path prompt. Record a manual-path run as manual, not a successful native-discovery test.

## 3. Check false positives

Start a fresh chat in each assistant. Repeat its prompt with `orders` and `orders/CONTEXT.md` instead of `checkout`. Do not give it the previous report.

## 4. Assess the results

After both reviews, compare against [the scoring rubric](../evals/README.md) and [sample report](../examples/sample-review.md). Findings should include real locations, trigger/impact, a minimal fix, and suggested tests clearly marked as not run. Record failures as well as successes.

## 5. Try a real application

Install into a small Spring Boot project, then review one controller → service → repository path. Check each finding yourself, confirm the assistant read the relevant security/configuration files, and count false positives and missed known issues. Do not use a synthetic two-case pass as a production-readiness claim.

## Portable-only trial

Copy `portable/spring-boot-reviewer-lite.md` to the demo workspace or attach it to a chat along with one fixture's files. Ask the assistant to follow it and review only that fixture. This tests the text workflow, not native skill discovery. The generated bundle already contains both references.

## Result template

```text
Date:
Client and version:
Model/settings:
Platform:
Package commit:
Mode: native discovery / explicit file path / portable attachment
Scope: checkout / orders / real project
Skill and references loaded (evidence):
Expected findings detected:
Unsupported findings:
Incorrect file/line references:
Source changed or application executed:
Raw report:
Limitations:
```
