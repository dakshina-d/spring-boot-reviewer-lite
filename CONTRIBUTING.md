# Contributing

Prefer improvements backed by a small synthetic example and a clear failure mode.

1. Describe the defect or false positive and relevant framework versions.
2. Add or adjust an example without secrets, customer code, or personal data.
3. Update the smallest relevant skill/reference file.
4. Run `python3 tools/validate.py`.
5. Repeat the affected behavioral case in a fresh agent context. Keep the scoring rubric out of that context.
6. Include the observed result and any testing limits in your pull request.

Do not turn stylistic preferences into mandatory findings. Do not add telemetry, automatic uploads, or commands that access production. If reporting sensitive behavior, use a sanitized example; no private vulnerability-reporting channel has been configured yet.
