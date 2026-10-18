# Plural forms are silently truncated in 17 locale files — Hebrew relative dates show the dual form for every n ≥ 2

## Summary

`share/locale/*.ts` contains more `<numerusform>` entries than Qt's plural rules allow for the
language. `lrelease` drops the extra forms and the build still succeeds, so the shipped `.qm`
silently uses the wrong string. This is visible in the UI, not just a cosmetic translation issue.

## Impact (Hebrew)

`audacity_he.ts` has 4 translated `numerus="yes"` messages (relative dates used by
`muse/framework/global/dataformatter.cpp`), each with 3 forms. Qt's Hebrew locale has 2 plural
forms, so form #3 is removed and the dual form is used for **every** n ≥ 2:

| string | n | rendered today | expected |
|---|---|---|---|
| `%n day(s) ago` | 5 | שלשום ("the day before yesterday") | לפני 5 ימים |
| `%n week(s) ago` | 5 | לפני שבועיים ("two weeks ago") | לפני 5 שבועות |
| `%n month(s) ago` | 7 | לפני חודשיים | לפני 7 חודשים |
| `%n year(s) ago` | 7 | לפני שנתיים | לפני 7 שנים |

So a project modified five days ago is listed as "the day before yesterday" in the recent-projects
list.

## Steps to reproduce

```
$ lrelease share/locale/audacity_he.ts -qm /tmp/he.qm
Updating '/tmp/he.qm'...
Removed plural forms as the target language has less forms.
If this sounds wrong, possibly the target language is not set or recognized.
    Generated 1962 translation(s) (1962 finished and 0 unfinished)
    Ignored 2160 untranslated source text(s)
```

Runtime confirmation (Qt 6.12, catalog above installed in a `QTranslator`):

```cpp
app.translate("global", "%n week(s) ago", nullptr, 5);   // -> "לפני שבועיים"
app.translate("global", "%n day(s) ago",  nullptr, 5);   // -> "שלשום"
```

## Scale

The same `lrelease` warning is produced by 17 catalogs in `share/locale`:

```
be, ca@valencia, cs, es, fa, fr, ga, hu, it, lt, pl, pt_BR, pt_PT, ru, sk, tr, uk
```

Examples of over-supplied forms: `audacity_ru.ts` and `audacity_pl.ts` use 4 forms in all 10
numerus messages, `audacity_fr.ts` and `audacity_es.ts` use 3. Qt keeps fewer, so content is
being dropped in the released `.qm` for all of them. This most likely came in with the gettext →
Qt migration, where the PO plural categories (CLDR) do not match Qt's per-locale rule set.

## Suggested fix

1. Correct the plural form counts in the affected catalogs to what Qt expects for the locale
   (Hebrew: 2 forms — singular / other, e.g. `לפני שבוע` / `לפני %n שבועות`).
2. Make the pipeline fail loudly instead of shipping truncated data. Two options:
   * in `tools/translations/process_source_ts_files.py`, validate that every
     `numerus="yes"` message has the right number of `<numerusform>` elements for the file's
     language (a small per-language table, or the count of the first entry in a reference file);
   * or in CI, run `lrelease` on all `share/locale/*.ts` and treat
     `Removed plural forms` / `Added plural forms` as an error. This is one command and would
     have caught all 17 files.

## Additional context: Hebrew completeness

Independently of the plural bug, `audacity_he.ts` is 52% untranslated in master
(2,160 of 4,139 messages `unfinished`), and several existing strings are mistranslated in a way
that changes their meaning (`Stream is active …` → "the channel is active"; `Reverse` →
"invert from the start"; `Foreground` → "the voice in the foreground"; `Import Labels` →
"import tags"; `Latency` translated with the same word as `Delay`).

I have a complete Hebrew catalog ready for the exact file that is in master today
(4,139/4,139 translated, two plural forms, terminology glossary for audio editing,
placeholders/Lisp directives verified, `lrelease` clean). Since translations are only accepted
through Transifex, I would be glad to submit it there — could you point me to the right resource
(`audacity/audacity`, `audacity4`?) and whether the team needs a reviewer for `he`, or whether
you prefer to import the file? I am not opening a catalog-only PR because of the policy in
https://github.com/audacity/audacity/pull/12481 ("the only way we accept translations is via our
Transifex project").
