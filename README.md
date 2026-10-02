# Spring Boot Reviewer Lite

**Free, portable AI instructions for evidence-based Spring Boot code reviews.**

Use the same review workflow in **Codex, AWS Kiro, Claude Code, Cursor, GitHub Copilot, and Gemini CLI**. A self-contained Markdown edition supports other assistants that can read pasted or uploaded instructions and source code.

Get prioritized findings with source locations, concrete impact, minimal fixes, and targeted verification steps. Built for Java developers and small backend teams reviewing one controller/service flow or a pull request.

## Choose your assistant

| Assistant | Installation supplied | Invocation |
| --- | --- | --- |
| Codex CLI / IDE | Native skill in `.agents/skills/` | `$spring-boot-reviewer-lite` followed by your request |
| AWS Kiro | Native skill in `.kiro/skills/` | `/spring-boot-reviewer-lite` or select it in Skills |
| Claude Code | Native skill in `.claude/skills/` | `/spring-boot-reviewer-lite` |
| Cursor | Native skill in shared `.agents/skills/` | Ask to use `spring-boot-reviewer-lite` |
| GitHub Copilot skill-capable agents | Native skill in shared `.agents/skills/` | Ask to use `spring-boot-reviewer-lite` |
| Gemini CLI | Native skill in shared `.agents/skills/` | Ask to use `spring-boot-reviewer-lite` |
| Other AI chats / coding assistants | [Portable Markdown instructions](portable/spring-boot-reviewer-lite.md) | Attach/paste instructions and relevant code |

These native paths are documented by the vendors. They are not a claim that every client version or model was tested. See [compatibility, sources, and test status](docs/COMPATIBILITY.md). AI provider subscriptions and usage limits still apply; this package itself is free.

## Quick start: Codex and Kiro

Clone the repository, or run `git pull --ff-only` in an existing clean clone:

```bash
git clone https://github.com/dakshina-d/spring-boot-reviewer-lite.git
cd spring-boot-reviewer-lite
```

With Python 3.10+ available, install into an existing Spring Boot project. This command works from PowerShell; substitute the real project path:

```powershell
python tools/install.py --client codex kiro --project "C:\path\to\your-spring-project"
```

On macOS/Linux, use `python3` and your project path. Preview changes by adding `--dry-run`. The installer copies all reference files, skips an identical installation, and refuses to overwrite a different existing installation. It does not edit your existing agent configuration or call a network service.

Open the target project in your assistant. Paste this into **Codex chat**, not the shell:

```text
$spring-boot-reviewer-lite Review the order controller, service,
repository, and relevant configuration. Read the skill's references.
Report evidence-backed findings. Do not modify files or run the application.
```

For **Kiro chat**, use:

```text
/spring-boot-reviewer-lite Review the order controller, service,
repository, and relevant configuration. Read the skill's references.
Report evidence-backed findings. Do not modify files or run the application.
```

Use real paths/symbols from your application in place of “order controller”. For custom Kiro agents, read the resource-loading note in [the compatibility guide](docs/COMPATIBILITY.md).

## No Python? Manual installation

Copy the complete `skills/spring-boot-reviewer-lite` folder into the destination from the table above. Keep the folder name and both `references/` files. Back up an existing installation before replacing it. In Windows PowerShell, from this repository's root:

```powershell
$projectPath = 'C:\path\to\your-spring-project'
if (-not (Test-Path -LiteralPath $projectPath -PathType Container)) {
    throw 'Application directory does not exist.'
}
foreach ($relative in @('.agents\skills', '.kiro\skills')) {
    $parent = Join-Path $projectPath $relative
    $destination = Join-Path $parent 'spring-boot-reviewer-lite'
    if (Test-Path -LiteralPath $destination) {
        throw "Already exists: $destination. Back up and review before replacing."
    }
}
foreach ($relative in @('.agents\skills', '.kiro\skills')) {
    $parent = Join-Path $projectPath $relative
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Copy-Item -LiteralPath '.\skills\spring-boot-reviewer-lite' -Destination $parent -Recurse
}
```

## Other clients and portable use

Select the client you actually use:

```bash
python tools/install.py --client claude --project /path/to/application
python tools/install.py --client cursor --project /path/to/application
python tools/install.py --client copilot --project /path/to/application
python tools/install.py --client gemini --project /path/to/application
python tools/install.py --client portable --project /path/to/application
```

Codex, Cursor, Copilot and Gemini share the `.agents/skills/` copy; installing for one makes that copy available to the other compatible clients in that project. `--client all` installs the documented native locations plus `ai-review/spring-boot-reviewer-lite.md`. Use only the locations you need; assistants may discover the same skill in more than one directory.

For an assistant without native skills, attach or paste [the portable file](portable/spring-boot-reviewer-lite.md) together with the relevant code and ask:

```text
Follow the attached Spring Boot Reviewer Lite instructions to review
these source files. State any missing context. Report findings with
source evidence, minimal fixes and verification steps. Do not change code.
```

If it has authorized local-file access, ask it to read `ai-review/spring-boot-reviewer-lite.md` instead. The portable file contains the entire checklist and report format, so the assistant does not need to follow separate file links. It does not give a text-only chat access to your computer. No universal native integration or identical model quality is promised.

## What it reviews

- Request validation and API error behavior
- Object authorization and sensitive-data handling
- Transaction boundaries and consistency failures
- JPA access patterns and database evidence
- Basic timeouts, retries and diagnostic behavior when relevant

Supported defects are separated from questions needing runtime evidence. The skill avoids arbitrary pool sizes, invented query counts, and automatic CSRF warnings without considering credential transport.

## Test before using it on your application

Use [the Codex/Kiro smoke-test guide](docs/TESTING.md). It creates a small separate demo folder without answer keys, so the assistant must find problems from the source. The examples are synthetic source excerpts, not runnable applications or customer code.

A report looks like this:

> **High · High confidence — Transaction advice is bypassed by a self-call**  
> Evidence: `CheckoutService.java:17–24`. The nontransactional entry point calls its own annotated method. Under the fixture's proxy configuration, the two saves do not share one transaction. An inventory failure can leave the order committed.  
> Fix: put the transaction boundary on the externally invoked `checkout` method.  
> Verify: force the inventory write to fail and assert no order is committed using a fresh transaction after the service call.

See [the complete sample report](examples/sample-review.md) and [evaluation rubric](evals/README.md) after your trial.

## Development checks

No Python dependency installation is required:

```bash
python tools/validate.py
python tools/build_portable.py --check
python -m unittest discover -s tests -v
```

GitHub Actions runs these on Linux and Windows. These checks validate the package and installer; they do not establish model accuracy. When changing canonical review instructions, regenerate the portable edition with `python tools/build_portable.py`.

## Updating and removing

Update your repository clone, then rerun the installer. Identical installs are skipped. For a differing installation, back up your edits, remove only the `spring-boot-reviewer-lite` directory at the reported destination, and reinstall. Remove that same directory to uninstall; other skills are unaffected. Portable installs are a single file under `ai-review/`.

## Status and boundaries

**v0.2.0 release candidate — multi-platform distribution.** The core review behavior remains the same as v0.1.0. See [current evidence and remaining tests](docs/COMPATIBILITY.md).

The default is source inspection without application changes or production access. AI findings need engineering judgment. Source review does not certify security or release readiness. The skill has no runtime dependencies, telemetry, or bundled network calls; the host assistant controls tools and permissions.

Contributions should include a sanitized example, framework/client versions, and expected versus observed behavior. See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE); future products do not change this version's license.
