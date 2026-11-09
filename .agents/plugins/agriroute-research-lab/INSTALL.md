# AgriRoute Research Lab Installation & Verification Guide

This guide explains how to validate, install, and verify the `agriroute-research-lab` plugin using the official Antigravity CLI (`agy`).

---

## Prerequisites
- **Antigravity CLI:** Installed at `~/.gemini/bin/agy` (v1.5.3 or higher).
- **Python Environment:** Conda environment with dependencies located at `/opt/miniconda3/envs/spoilage`.
- **System Requirements:** macOS (Darwin arm64) or Linux x86_64 with read/write access to project directory.

---

## Step 1: Validate Plugin Manifest & Components

Run strict validation to ensure all agents, skills, and rule files conform to Antigravity plugin standards:

```bash
~/.gemini/bin/agy plugin validate .agents/plugins/agriroute-research-lab --strict
```

### Expected Output:
```
Validating agriroute-research-lab (.agents/plugins/agriroute-research-lab/plugin.json)

  skills 17 · agents 7 · rules 1 · hooks 0 · mcpServers 0 · sidecars 0

✔ Validation passed
```

---

## Step 2: Install Local Plugin

Install the plugin into your Antigravity plugin repository:

```bash
~/.gemini/bin/agy plugin install .agents/plugins/agriroute-research-lab
```

---

## Step 3: Verify Installed Plugin

List all active plugins to confirm `agriroute-research-lab` is installed and enabled:

```bash
~/.gemini/bin/agy plugin list
```

### Expected Output:
The list should include `agriroute-research-lab` with its full component manifest (17 skills, 7 agents, 1 rule).

---

## Step 4: Verify Subagent & Skill Discovery

You can test agent and skill discoverability by invoking subagents in chat or via slash commands:
- `@research-director`: Launch research coordination.
- `@data-integrity-auditor`: Audit dataset splits and pHash leakage.
- `@computer-vision-researcher`: Run vision backbone benchmarks.
- `@adversarial-reviewer`: Simulate critical peer review.

---

## Uninstallation

If you need to uninstall the plugin:

```bash
~/.gemini/bin/agy plugin uninstall agriroute-research-lab
```

