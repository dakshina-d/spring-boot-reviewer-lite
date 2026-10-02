# Compatibility and verification

The canonical skill is `skills/spring-boot-reviewer-lite/`. All native installs copy it unchanged. `portable/spring-boot-reviewer-lite.md` is generated from its instruction body and both references. Python is needed only for helper scripts, not for using the review instructions.

## Supported installation routes

Paths below are relative to the project you want to review. Start the assistant in that project. Vendor documentation was checked on 2026-10-02.

| Client | Installer option | Destination | How to request a review | Primary documentation |
| --- | --- | --- | --- | --- |
| Codex CLI / IDE | `codex` | `.agents/skills/spring-boot-reviewer-lite/` | `$spring-boot-reviewer-lite Review ...` | [OpenAI](https://learn.chatgpt.com/docs/build-skills) |
| Kiro IDE / CLI with skills support | `kiro` | `.kiro/skills/spring-boot-reviewer-lite/` | `/spring-boot-reviewer-lite Review ...` or select the skill | [Kiro](https://kiro.dev/docs/skills/) |
| Claude Code | `claude` | `.claude/skills/spring-boot-reviewer-lite/` | `/spring-boot-reviewer-lite Review ...` | [Anthropic](https://code.claude.com/docs/en/skills) |
| Cursor | `cursor` | `.agents/skills/spring-boot-reviewer-lite/` | Ask to use the named skill; confirm it appears in Skills | [Cursor](https://cursor.com/docs/skills) |
| Copilot skill-capable agents | `copilot` | `.agents/skills/spring-boot-reviewer-lite/` | Ask to use the named skill | [GitHub](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| Gemini CLI | `gemini` | `.agents/skills/spring-boot-reviewer-lite/` | Ask to use the named skill; inspect `/skills list` | [Gemini CLI](https://geminicli.com/docs/cli/skills/) |
| Other assistants | `portable` | `ai-review/spring-boot-reviewer-lite.md` | Read/attach/paste the complete file and supply source | Generic text workflow; no native loader assumed |

The shared `.agents/skills/` destination is intentional. The installer deduplicates that path when multiple clients are selected. Kiro and Claude receive separate copies. A client that scans several of these paths can show duplicates; choose only required targets and keep installed copies on the same version.

## Kiro details

Open the target project and look in Agent Steering & Skills. In supported versions, you may instead import this skill-folder URL:

https://github.com/dakshina-d/spring-boot-reviewer-lite/tree/main/skills/spring-boot-reviewer-lite

Use the folder URL, not the repository root. If a custom agent does not see the skill, merge this entry into its existing `resources` array:

```json
"skill://.kiro/skills/*/SKILL.md"
```

Do not replace the full agent configuration or remove its other resources. Our installer does not modify agent configuration. For older clients without native skills, use the portable instructions and explicitly attach relevant source.

## Codex details

The project-folder route targets local Codex CLI/IDE environments. The hosted ChatGPT Work skill directory is a separate installation surface; copying files onto your Windows computer does not install them into a remote chat. In Work, select an installed skill through the skill picker, or use the portable file with attached/accessible source. For Codex Cloud, the installed project skill must exist in the repository/environment the task checks out.

If local discovery does not show the skill, confirm the project root and that `SKILL.md` and references are present. Check the skill selector and use an explicit file-path prompt while troubleshooting. Model settings and host permissions still apply.

## What has actually been verified

| Layer | Evidence | Limits |
| --- | --- | --- |
| Canonical review skill | Two synthetic scopes reviewed by a Codex subagent on 2026-10-02; expected checkout defects found and orders false positives avoided | Explicit skill path; not a local CLI/IDE discovery test |
| Portable generation | Bundle deterministically includes canonical instructions and both reference files; drift check in CI | Text packaging alone does not prove every model follows the rules |
| Portable review behavior | A fresh Codex subagent followed only the generated bundle on both fixture scopes; found both checkout defects and no actionable orders findings | Explicit file input; not a Claude/Kiro/other-model test |
| Project installer | Automated copy, rerun, no-overwrite, dry-run, invalid-path and symlink checks | Does not launch an AI client; symlink test can skip where the OS disallows symlinks |
| Native client discovery | Locations and invocation guidance checked against the primary documentation above | Codex CLI/IDE, Kiro, Claude Code, Cursor, Copilot and Gemini were not launched in this build environment |
| Real projects | No real-project result recorded yet | Use the smoke guide, then a small project you are authorized to review |

The release provides native-format packages and a text fallback. It does not claim verified support for every AI product, client version, or model. Assistants need sufficient context and instruction-following ability; text-only chats need supplied source. Authentication, subscription and tool access are controlled by each provider.
