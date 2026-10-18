# PR מוכן (למקרה שהמתחזקים יבקשו) — Audacity 4 Hebrew catalog

> אזהרה: לפי `CONTRIBUTING.md`, `.tx/config` והתקדים ב-PR #12481, הפרויקט **לא מקבל**
> PR שמשנה קטלוג תרגום. הקובץ כאן מוכן לשליחה ב-Transifex, או ל-PR רק אם מתחזק יבקש במפורש.

## ענף ופקודות

```bash
gh repo fork audacity/audacity --clone=false
git clone https://github.com/<user>/audacity.git
cd audacity
git remote add upstream https://github.com/audacity/audacity.git
git fetch upstream master
git switch -c translation/hebrew-audacity4 upstream/master
cp /path/to/upstream/audacity_he.ts share/locale/audacity_he.ts
git add share/locale/audacity_he.ts
git commit -s -F commit-msg.txt
git push -u origin translation/hebrew-audacity4
gh pr create --repo audacity/audacity --base master --head <user>:translation/hebrew-audacity4 \
  --title "Hebrew: complete translation of the Audacity 4 UI, correct plural forms" \
  --body-file pr-body.txt
```

## הודעת commit

```
Hebrew: complete translation of the Audacity 4 UI, fix plural forms

Translates all 4,139 messages of share/locale/audacity_he.ts (2,160 were
unfinished) and replaces the existing strings with a terminology-consistent
translation based on an audio-editing glossary (track=רצועה, clip=קטע,
playhead=ראש השמעה, gain=הגבר, level=מפלס, envelope=מעטפת...).

Also fixes the numerus entries: Hebrew has two plural forms in Qt, the file
carried three, so lrelease dropped the third form and the dual form was
displayed for every n >= 2 ("שלשום" for a project modified five days ago).

Verified:
- lrelease: 4139 finished, 0 unfinished, no plural warnings
- QTranslator: action/Exit -> יציאה, preferences/Sample rate -> קצב דגימה
- placeholders (%1..%n, %s, %d, %Ln) and Lisp directives (~a, ~%) identical
  to the sources in all 4,139 messages
- rich-text tags preserved
```

## גוף ה-PR

```markdown
## What

Complete Hebrew translation of the Audacity 4 UI and a fix for the plural forms.

* `share/locale/audacity_he.ts`: 4,139 / 4,139 messages translated (2,160 were
  `unfinished`). Existing strings were reviewed and replaced where they were
  inconsistent or wrong (`Stream is active` → "the channel is active",
  `Reverse` → "invert from the start", `Foreground` → "the voice in the
  foreground", `Import Labels` → "import tags", `Latency` and `Delay` shared
  one word).
* Plural fix: Hebrew has two forms in Qt, the file had three, so `lrelease`
  removed the third and used the dual for every n ≥ 2. Now singular/plural.

## Why

The Hebrew UI was 52% English; relative dates were visibly wrong
(a project modified 5 days ago showed "שלשום" = the day before yesterday).

## Verification

```
$ lrelease share/locale/audacity_he.ts -qm /tmp/he.qm
    Generated 4139 translation(s) (4139 finished and 0 unfinished)
```

No "Removed plural forms" warning. Placeholder and rich-text integrity checked
programmatically for all messages; a Qt `QTranslator` loads the `.qm` and
returns Hebrew for the UI contexts.

## Notes

Per CONTRIBUTING.md translations are collected in Transifex. I am opening this
because the catalog is fully done and ready; happy to close it and upload
there instead if that is still preferred.
```
