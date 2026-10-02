# Spring Boot Reviewer Lite

**A free AI skill for evidence-based Spring Boot code reviews.**

Turn a review request into prioritized findings with source locations, concrete impact, a minimal fix, and a targeted verification step.

Built for Java developers and small backend teams. Start with one controller/service flow or one pull request.

## What it covers

- Request validation and API error behavior
- Object authorization and sensitive-data handling
- Transaction boundaries and consistency failures
- JPA access patterns and database evidence
- Basic timeouts, retries and diagnostic behavior when relevant

It separates supported defects from questions requiring more evidence. It does not prescribe arbitrary pool sizes, infer missing indexes from annotations, or flag CSRF configuration without considering credential transport.

## Quick start: Claude Code

Prerequisite: Claude Code with local project access and custom skills support. The skill is free; your AI provider's usage charges or subscription still apply.

Clone this repository:

```bash
git clone https://github.com/dakshina-d/spring-boot-reviewer-lite.git
cd spring-boot-reviewer-lite
```

Then copy the complete `skills/spring-boot-reviewer-lite` folder into your application's `.claude/skills/` directory. The result must be:

```text
my-application/
  .claude/skills/spring-boot-reviewer-lite/
    SKILL.md
    agents/openai.yaml
    references/review-checklist.md
    references/report-format.md
```

From this downloaded repository's root, PowerShell users can run the following after replacing the application path. It refuses to overwrite an existing installation:

```powershell
$projectPath = 'C:\path\to\my-application'
if (-not (Test-Path -LiteralPath $projectPath -PathType Container)) {
    throw 'Application directory does not exist.'
}
$skillsDir = Join-Path $projectPath '.claude\skills'
$destination = Join-Path $skillsDir 'spring-boot-reviewer-lite'
if (Test-Path -LiteralPath $destination) {
    throw 'Skill already exists. Back it up and review changes before updating.'
}
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -LiteralPath '.\skills\spring-boot-reviewer-lite' -Destination $destination -Recurse
```

Open Claude Code in your application and request:

```text
/spring-boot-reviewer-lite Review the order controller, service, repository,
and relevant security configuration. Report evidence-backed findings.
Do not modify files or run the application.
```

Natural-language activation can also work, but use the explicit command for the first trial. If it is missing, check the folder nesting and your client's skill discovery settings. Remove the copied skill directory to uninstall.

Installation follows the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills). Native Claude Code execution has not yet been tested for this release candidate.

## Other coding assistants

The core uses the [Agent Skills format](https://agentskills.io/specification). This release has been exercised through a Codex review agent with an explicit skill path. For a client that can read local files, explicitly ask it to read `SKILL.md` and the linked references before reviewing. This is a manual workflow, not a claim of native integration with every assistant. Cursor/Kiro integration is outside v0.1.0.

## Example output

> **High · High confidence — Transaction advice is bypassed by a self-call**  
> Evidence: `examples/checkout/CheckoutService.java:17–24`. The nontransactional entry point calls its own annotated method. Under the fixture's proxy configuration, the two repository saves do not share one transaction. An inventory failure can leave the order committed.  
> Fix: put the transaction boundary on the externally invoked `checkout` method.  
> Verify: force the inventory write to fail and assert no order is committed using a fresh transaction after the service call.

See [the complete sample report](examples/sample-review.md). The examples are synthetic source excerpts, not runnable applications or customer code.

## Try the examples

Ask your assistant to use the skill to review `examples/checkout`, including its `CONTEXT.md`. Then review `examples/orders` separately. The second example checks whether the reviewer avoids unsupported warnings.

For repeatable evaluation, see [evals/README.md](evals/README.md). Keep expected results out of the reviewing agent's context.

## Validate the package

Python 3.10+ is required only for the repository validator, not for using the skill:

```bash
python3 tools/validate.py
```

This checks package structure and local Markdown links. It is not a Java compiler, vulnerability scanner, or behavioral benchmark. GitHub Actions runs the same check on pushes and pull requests after publication.

## Boundaries

The default workflow is a source review without code changes or production access. Follow your organization's rules before giving any AI assistant access to private code. AI findings require engineering judgment; source inspection cannot certify security or release readiness.

There are no bundled network calls, telemetry, installation executables, or runtime dependencies in the skill. The host AI client controls tools and permissions.

## Project status

**v0.1.0 release candidate.** Format checks and two synthetic review cases have been exercised. See [evaluation status](evals/README.md) for results and limits. Native-client testing and feedback from real Spring Boot projects are the next release gates.

Contributions: include a minimal synthetic reproduction, expected versus actual review behavior, framework versions, and evidence. Do not post customer code, credentials, or personal data. See [CONTRIBUTING.md](CONTRIBUTING.md).

Licensed under MIT. You may use, modify and redistribute this free version under that license. Future paid products, if any, are separate; this version has no license-key or upgrade dependency.
