# מה צריך כדי שהתרגום ייכנס לפרויקט — בדיקה מול הריפו

## 1. העובדה שקובעת הכול: תרגומים נכנסים דרך Transifex, לא דרך PR

* `CONTRIBUTING.md` (שורה 26): "See our translators page for more information on how to translate Audacity."
* מדריך המתרגמים הרשמי: "Translation happens on Transifex" ו־"Transifex is still the only place
  the team collects translations from".
* `.tx/config` בריפו מגדיר בדיוק את הקטלוג שלנו:
  `[o:audacity:p:audacity:r:audacity4]`, `file_filter = share/locale/audacity_<lang>.ts`, `type = QT`.
* תקדים מפורש: PR #12481 שתיקן קובץ `.ts` ספרדי נסגר עם ההודעה
  "the only way we accept translations is via our Transifex project".
* ה־CI של הפרויקט (`translate_tx_pull_to_s3.yml`) מושך מ-Transifex ופותח PR אוטומטי על
  `share/locale/*` — כלומר הקובץ שלנו ייכנס דרך הצינור הזה, לא ביד.

**מסקנה:** PR ישיר של `audacity_he.ts` ייסגר. הדרך היחידה למזג את התרגום היא העלאה ל-Transifex
(או בקשה מפורשת מהמתחזקים לייבא את הקובץ).

## 2. מה דרוש בפועל

| # | מה | למה | מי מספק |
|---|---|---|---|
| 1 | חיבור GitHub לחשבון | לפתוח Issue על הבאג (ולהיווכן PR אם יבקשו) | אישור חיבור כאן בצ'אט |
| 2 | חשבון Transifex + הרשאת שפה `he` בפרויקט `audacity/audacity` | העלאת הקובץ — הצינור היחיד שממוזג | אתה (או מתרגם קיים) |
| 3 | החלטה: להעלות את הקובץ במלואו או רק את הפרש | 100% מתורגם = סקירה גדולה; אפשר לפצל | אתה |
| 4 | CLA (רק אם נוגעים בקוד, לא בתרגום) | תיקון ה-CI שמזהה את באג צורות הרבים | חתימה דיגיטלית |
| 5 | תזמון מול string freeze | תרגום שנכנס אחרי הקפאה יגיע בגרסה שאחריה | צוות Audacity |

## 3. מה שכבר מוכן אצלנו (מוכן לשליחה)

* `upstream/audacity_he.ts` — הקובץ המתורגם **כנגד master** (זהה ביט-בביט ל-4.0.1; בדקנו:
  `audacity_he.ts` ב-master זהה לקובץ שב-4.0.1). 4,139/4,139 מתורגמים, 2 צורות רבים,
  `lrelease` נקי.
* `upstream/audacity_he.qm` — מקומפל לבדיקה.
* `upstream/ISSUE.md` — נוסח ה-Issue (אנגלית) עם ראיות הרצה.
* `upstream/PR.md` — נוסח PR + פקודות, למקרה שהמתחזקים יבקשו בכל זאת.

## 4. הבאג שנמצא (זה מה שהמפתח צריך לתקן)

17 קטלוגים (`ru, pl, fr, es, it, cs, sk, uk, be, tr, fa, ga, hu, lt, pt_BR, pt_PT, ca@valencia`)
מכילים יותר צורות רבים ממה ש-Qt תומך בשפה; `lrelease` זורק את העודפות בשקט.
בעברית זה נצפה בפועל: פרויקט מלפני 5 ימים מוצג כ"שלשום", ושבועיים במקום 5 שבועות.
התיקון המוצע: לתקן את מספר הצורות בקטלוגים, ולהוסיף בדיקת CI שמריצה `lrelease` ונכשלת על
"Removed plural forms" — כך זה לא יחזור.

## 5. מה אני יכול לעשות ברגע שיש הרשאות

1. לפתוח את ה-Issue (דורש חיבור GitHub).
2. להכין branch + commit + PR מוכן (fork), אם ירצו בכל זאת.
3. להעלות את הקובץ ל-Transifex — דורש API token של Transifex; אין כזה כרגע.
