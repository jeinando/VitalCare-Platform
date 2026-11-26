# Release 1 backlog

`backlog.json` holds the 51 items of the Release 1 backlog (45 user stories and 6 technical tasks). It is the seed used to create the GitHub issues once; after that, **GitHub Issues and the GitHub Project are the source of truth**, and this file is kept only as a historical record.

## Create the issues

1. Install the GitHub CLI and sign in:

   ```bash
   gh auth login
   ```

2. Preview what will be created (changes nothing):

   ```bash
   python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform
   ```

3. Create the labels and issues:

   ```bash
   python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform --apply
   ```

4. Optional: create a GitHub Project (board) first, then add every issue to it. The project number is in its URL (`github.com/users/jeinando/projects/1`). The CLI needs the `project` scope: `gh auth refresh -s project`.

   ```bash
   python scripts/create_backlog_issues.py --repo jeinando/VitalCare-Platform --apply \
       --project 1 --project-owner jeinando
   ```

The script skips issues that already exist (same `[ID]` title prefix), so it is safe to run again.

## Labels created

| Label | Meaning |
| --- | --- |
| `epic: E0 ...` to `epic: E10 ...` | Epic the item belongs to |
| `priority: must`, `should`, `could`, `won't` | MoSCoW priority |
| `type: user story`, `type: technical` | Kind of item |

## Suggested GitHub Project setup

| Field | Type | Values |
| --- | --- | --- |
| Status | Single select | Todo, Ready, In progress, In review, Done |
| Points | Number | Initial estimate from the issue body |
| Sprint | Iteration | 2-week iterations |
