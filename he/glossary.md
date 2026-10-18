# מילון מונחים לתרגום Audacity 4.0.1 לעברית
## Hebrew terminology glossary for Audacity 4.0.1

המילון הוא הבסיס לתרגום: כל מונח נבחר לפי המשמעות שלו *בתוך התוכנה* (מה הכפתור עושה),
ולא לפי תרגום מילולי. המונחים כאן מחייבים — כל הקטלוגים (`.ts` ו־`.po`) מתורגמים לפיהם.

### 1. ישויות בפרויקט

| English | עברית | הערה |
|---|---|---|
| Project | פרויקט | לא "מיזם" |
| Track | רצועה | לא "ערוץ" (ערוץ = channel) ולא "טראק" |
| Clip | קטע | קטע שמע ברצועה; "קליפ" שמור לווידאו |
| Track header | כותרת רצועה | |
| Track name | שם הרצועה | |
| Selection | בחירה | "בחירת שמע" = audio selection |
| Region | אזור | |
| Label | תווית | Labels track = רצועת תוויות (לא "תויות") |
| Envelope | מעטפת | מעטפת עוצמה/מעטפת מהירות |
| Group | קבוצה | קבוצת רצועות |
| Workspace | סביבת עבודה | |
| Timeline | ציר זמן | |
| Playhead | ראש השמעה | הסמן האנכי שמראה היכן מתנגן |
| Cursor | סמן | |

### 2. שמע, עוצמה ומדידה

| English | עברית | הערה |
|---|---|---|
| Audio | שמע | "אודיו" רק בשמות מוצרים/פורמטים (audio.com, Audio Unit) |
| Sample | דגימה | |
| Sample rate | קצב דגימה | |
| Bit depth / Sample format | עומק סיביות | |
| Channel | ערוץ | |
| Mono / Stereo | מונו / סטריאו | |
| Amplitude | משרעת | לא "אמפליטודה" בגוף הממשק |
| Level | מפלס | מפלס שמע; "רמה" רק בהקשרי הגדרות |
| Meter | מד | מד מפלסים = level meter |
| Peak | שיא | Peak dB = שיא בדציבלים |
| Gain | הגבר | מונח סטנדרטי; לא "רווח" |
| Volume | עוצמת קול | |
| Loudness | עוצמת שמע | Loudness Normalization = נירמול עוצמת שמע |
| Clipping | קליפינג | תופעת גזירת הגל; הפועל: "להיחתך" |
| Distortion | עיוות | |
| Noise | רעש | |
| Hiss | לחש | רעש בתדרים גבוהים |
| Hum | זמזום | רעש רשת חשמל 50/60Hz |
| Silence | שקט | |
| Fade in / Fade out | עלייה הדרגתית / דעיכה הדרגתית | "דעיכה"/"עלייה" בלבד בפריסטים קצרים |
| Crossfade | מיזוג צולב | |
| Pan | פאן | איזון בין ערוצים |
| Balance | איזון | |
| Phase | פאזה | |
| Polarity | קוטביות | Invert = היפוך קוטביות |
| Frequency | תדר | |
| Band | פס | פס תדרים |
| Filter | מסנן | |
| Low-pass / High-pass | מעביר נמוכים / מעביר גבוהים | |
| Notch | חוסם צר | |
| Equalization / EQ | אקולייזר | |
| Spectrogram | ספקטרוגרמה | |
| Spectrum | ספקטרום | |
| Waveform | צורת גל | |
| Pitch | גובה צליל | |
| Tempo | קצב | |
| Speed | מהירות | |
| Latency | השהיית קלט/פלט | לא סתם "השהיה" (delay) |
| Buffer | מאגר | |
| Device | התקן | |
| Host | מארח | Audio host = מארח שמע |
| Monitoring | ניטור | |

### 3. אפקטים (שמות ופעולות)

| English | עברית | הערה |
|---|---|---|
| Effect | אפקט | |
| Effect rack | מתלה אפקטים | |
| Realtime effect | אפקט בזמן אמת | |
| Amplify | הגברה | |
| Normalize | נירמול | לא "נרמול" ולא "נירמול עוצמה" כשיש הבחנה מ-Loudness |
| Noise Reduction | הפחתת רעש | |
| Noise Gate | שער רעש | |
| Compressor | מדחס | |
| Limiter | מגביל | |
| Expander | מרחיב | |
| Threshold | סף | |
| Ratio | יחס | |
| Attack / Release | התקפה / שחרור | |
| Makeup gain | הגבר משלים | |
| Reverb | הדהוד | Echo = הד, כדי לא להתבלבל |
| Echo | הד | |
| Delay | השהיה | אפקט ההשהיה |
| Chorus | כורוס | |
| Flanger | פלנג'ר | |
| Phaser | פייזר | |
| Wahwah | וואה־וואה | |
| Tremolo / Vibrato | טרמולו / ויברטו | |
| Invert | היפוך קוטביות | |
| Reverse | היפוך | השמעה מהסוף להתחלה |
| Truncate Silence | קיצור קטעי שקט | |
| Click removal | הסרת נקישות | |
| De-esser | מפחית שורקים | |
| Auto Duck | הנמכה אוטומטית | |
| Hard limiter | מגביל קשיח | |

### 4. פעולות עריכה ופקודות

| English | עברית | הערה |
|---|---|---|
| Cut / Copy / Paste | גזירה / העתקה / הדבקה | |
| Paste Special | הדבקה מיוחדת | |
| Trim | קיצוץ | Trim audio to selection |
| Split | פיצול | Split clip = פיצול קטע |
| Join | חיבור | |
| Merge | מיזוג | |
| Duplicate | שכפול | |
| Delete | מחיקה | |
| Remove | הסרה | |
| Insert | הוספה | |
| Undo / Redo | ביטול / ביצוע מחדש | |
| Snap | הצמדה | Snapping = הצמדה |
| Zoom in / out | התקרבות / התרחקות | |
| Scroll | גלילה | |
| Drag | גרירה | |
| Drop | שחרור | Drag and drop = גרירה ושחרור |
| Render | רינדור | |
| Mix and Render | ערבוב ורינדור | |
| Import / Export | ייבוא / ייצוא | |
| Save / Save as | שמירה / שמירה בשם | |
| Recording | הקלטה | Record = הקלט (פועל), הקלטה (שם עצם) |
| Playback | השמעה | Play = נגן/השמעה לפי הקשר |
| Stop / Pause | עצירה / השהיה | |
| Loop | חזרה | Loop playback = השמעה חוזרת |

### 5. ממשק, קבצים והגדרות

| English | עברית | הערה |
|---|---|---|
| Preferences | העדפות | |
| Settings | הגדרות | |
| Preset | פריסט | "הגדרה קבועה מראש" ארוך מדי ללחצנים |
| Plugin | תוסף | |
| Extension | הרחבה | |
| Macro | מאקרו | |
| Batch processing | עיבוד אצווה | |
| Metadata / Tags | מטא־נתונים / תגים | |
| Format | פורמט | |
| Bit rate | קצב סיביות | |
| Encoding | קידוד | |
| Dither | דית'ר | |
| Resample | דגימה מחדש | |
| Toolbar | סרגל כלים | |
| Panel | חלונית | |
| Tab | לשונית | |
| Dialog | תיבת דו־שיח | |
| Dropdown | רשימה נפתחת | |
| Checkbox | תיבת סימון | |
| Slider | מחוון | |
| Field | שדה | |
| Default | ברירת מחדל | |
| Custom | מותאם אישית | |
| Reset | איפוס | |
| Apply | החלה | |
| Cancel | ביטול | |
| OK | אישור | |
| Close | סגירה | |
| Browse | עיון | |
| Preview | תצוגה מקדימה | |
| Path | נתיב | |
| Folder | תיקייה | |
| Error / Warning | שגיאה / אזהרה | |
| Shortcut | קיצור דרך | |
| Accessibility | נגישות | |
| Theme | ערכת נושא | |

### 6. כללים מחייבים

1. **אין לתעתק כשיש מונח עברי מקובל.** "track" → רצועה, לא טראק; "effect" → אפקט (מקובל).
2. **עקביות מלאה בין שני הקטלוגים** (`.ts` של ממשק Qt ו־`.po` הוותיק): אותו מונח אנגלי = אותו מונח עברי.
3. **שומרים על כל מציין מקום** (`%1`, `%2`, `%n`, `%s`, `%d`, `\n`, `&`, תגי HTML/rich-text) ללא שינוי.
4. **סימני פיסוק:** משתמשים ב־`…` ולא ב־`...`; מירכאות עבריות „…” או "…" ולא `"` ישר; מקף עברי ־ במילים מחוברות.
5. **קיצורים:** "סה״כ", "למשל", "וכו'" — בגרש עברי (׳) או גרשיים (״).
6. **פנייה למשתמש** בלשון רבים/ניטרלי ("בחר", "לחץ") — כמו במקור, בלי "אתה/את".
7. **מחרוזות קצרות** (כפתורים, כותרות): עד שתי מילים, בלי מילות קישור מיותרות.
8. **שמות טכניים** (VST, LV2, LADSPA, Nyquist, FLAC, MP3, BPM, dB, Hz, MIDI, Audio Unit, audio.com,
   שמות חברות ומוצרים) נשארים באנגלית.
9. **RTL:** לא מוסיפים תווי כיוון בתוך מחרוזת עם מציין מקום; Qt מטפל בכיווניות.
10. **תרגום לפי תפקוד:** בממשק "Action title" הכיתוב הוא תווית תפריט — קצר ופועלי; "Action description"
    הוא תיאור/tooltip — משפט מלא שמסביר מה הפעולה עושה.
