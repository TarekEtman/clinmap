# Workspace setup — so the AI agent can run commands

## Problem

Grok/Cursor may open a workspace named **`clinical-ai-eval-lab`**, but the canonical repo on disk is:

```text
/Users/nati/Documents/JOB/clinical-ai-eval-lab-v1
```

When those differ, the agent often **cannot spawn a terminal** (`IO Error`, `Command failed to spawn`). You end up running `make` by hand even though the agent can still **edit files** via absolute paths.

## Fix A (recommended): Open the real folder

1. **File → Open Folder** (or Grok Build project root).
2. Choose **`clinical-ai-eval-lab-v1`** only — not the parent `JOB` folder.
3. Start a **new agent chat** in that window.
4. Ask: `run make clinmap-frontier-pack` — the agent should execute locally.

## Fix B: Symlink old name → v1 (one-time)

If your IDE keeps using path `clinical-ai-eval-lab`, create a symlink so both names point at the same tree:

```bash
cd /Users/nati/Documents/JOB
test -e clinical-ai-eval-lab && echo "already exists — skip or remove first" || ln -s clinical-ai-eval-lab-v1 clinical-ai-eval-lab
ls -la clinical-ai-eval-lab
```

Then reopen the workspace as **`clinical-ai-eval-lab`** (the symlink). Terminal tools should resolve to v1 content.

Or run:

```bash
bash /Users/nati/Documents/JOB/clinical-ai-eval-lab-v1/scripts/fix_workspace_symlink.sh
```

## Fix C: Cursor only for “agent runs code”

Keep Grok for planning; use **Cursor Agent** on `clinical-ai-eval-lab-v1` when you need unattended `make audit`, git, etc.

## Verify agent terminal works

In a new chat after Fix A or B:

```text
Run: cd /Users/nati/Documents/JOB/clinical-ai-eval-lab-v1 && make clinmap-frontier-pack
```

You should see tool output in chat — not “paste this in your terminal.”

## Canonical product

All ClinMAP-VOI v0 work lives in **`clinical-ai-eval-lab-v1`**. Do not use a legacy `clinical-ai-eval-lab` copy without the symlink.

## Continue work after fix

- Checklist: `docs/frontier_lab_evidence_checklist.md`
- Command: `make clinmap-frontier-pack`