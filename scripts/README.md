## GitHub CLI (issues + PR workflow)

### 0) Logga in
```bash
gh auth login
```

(Valfritt) sätt default repo:
```bash
gh repo set-default Sandstrom96/travel_buddy
```

### Exempel: ta en issue korrekt (från terminalen)

1) Lista issues:
```bash
gh issue list
```

2) Läs issue:
```bash
gh issue view 14
```

3) Assigna dig själv:
```bash
gh issue edit 14 --add-assignee @me
```

4) Skapa branch kopplad till issue:
```bash
gh issue develop 14 --checkout
```

5) När du gjort en ändring:
```bash
git status
git add -A
git commit -m "Issue #14: add /health endpoint"
git push -u origin HEAD
```

6) Skapa PR:
```bash
gh pr create --fill
```

7) Be om review (valfritt):
```bash
gh pr edit --add-reviewer <github-username>
```

## Scripts (GitHub automation)

Skapa lokal env för scripts:
```bash
cp scripts/.env.example scripts/.env
```

Kör scripts (exempel):
```bash
bash scripts/github/update_issues_part1.sh
bash scripts/github/update_issues_part2.sh
bash scripts/github/update_issues_part3.sh
bash scripts/github/set_roadmap_dates_safe.sh
```