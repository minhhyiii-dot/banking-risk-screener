# Cleanup Backlog

These are candidate cleanup tasks for the working copy. Do not apply them to the
official copy until reviewed.

## Safe Next Steps

```text
1. Verify the Python baseline still runs after documentation cleanup.
2. Create a small public-demo data package from existing baseline outputs.
3. Decide which raw/intermediate files should be excluded from GitHub.
4. Add docs/notebooklm_outputs/ placeholders later, after NotebookLM flow.
5. Add app/ later, after the baseline/source structure is locked.
```

## Needs Review Before Changing

```text
- Moving data/ folders.
- Renaming code/Models or code/Notebooks.
- Removing RapidMiner .rmp files.
- Removing duplicated model-specific CSV files under code/Models.
- Moving outputs/python_baseline.
```

## Public GitHub Hygiene Later

```text
- Check for personal absolute paths.
- Check for raw/sensitive/unnecessary data.
- Decide whether full raw data belongs in GitHub.
- Keep only small sample data for the Cloudflare demo if needed.
- Add final Cloudflare and GitHub links to README after deployment.
```
