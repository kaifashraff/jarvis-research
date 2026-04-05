#!/usr/bin/env python3
import json

# Load dataset
with open('quran-verified-dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("🔍 EXTRACTING EXACT SOURCES FOR CODE 7 PATTERNS\n")
print("=" * 60)

# 1. Seven heavens (سَبْعَ سَمَٰوَٰتٍ)
print("\n📖 SEVEN HEAVENS - EXACT SOURCES:")
target_phrase = "سَبْعَ سَمَٰوَٰتٍ"
found = []
for surah_num, surah in data['surahs'].items():
    for ayah_num, text in surah['ayahs'].items():
        if target_phrase in text:
            found.append((surah_num, ayah_num))
            print(f"  ✅ Surah {surah_num}:{ayah_num} - {surah['name']}")
            print(f"     Text: {text}")
print(f"\n  TOTAL COUNT: {len(found)}")

# 2. Word "سبع" (seven) in all forms
print("\n📖 WORD 'سَبْع' (SEVEN) - ALL OCCURRENCES:")
seven_variants = ["سَبْعَ", "سَبْعَة", "سَبْعًا", "سَبْعِ", "سَبْعُ"]
all_seven = []
for surah_num, surah in data['surahs'].items():
    for ayah_num, text in surah['ayahs'].items():
        for variant in seven_variants:
            if variant in text:
                all_seven.append((surah_num, ayah_num, variant, text))
                print(f"  ✅ Surah {surah_num}:{ayah_num} - '{variant}' in: {text[:50]}...")
print(f"\n  TOTAL COUNT: {len(all_seven)}")

# 3. Seven Mathani - Surah 15:87
print("\n📖 SEVEN MATHANI (15:87):")
if '15' in data['surahs'] and '87' in data['surahs']['15']['ayahs']:
    text = data['surahs']['15']['ayahs']['87']
    print(f"  ✅ Surah 15:87 - {text}")
    has_seven = any(v in text for v in seven_variants)
    has_mathani = "الْمَثَانِي" in text
    print(f"     Contains 'seven': {has_seven}")
    print(f"     Contains 'mathani': {has_mathani}")
else:
    print("  ❌ Surah 15:87 not found in dataset")

# 4. Phrase "قُلْ" occurrences
print("\n📖 PHRASE 'قُلْ' (SAY) - OCCURRENCES:")
qul_count = 0
for surah_num, surah in data['surahs'].items():
    for ayah_num, text in surah['ayahs'].items():
        count = text.count("قُلْ")
        if count > 0:
            qul_count += count
            print(f"  ✅ Surah {surah_num}:{ayah_num} - {count} occurrence(s)")
print(f"\n  TOTAL COUNT: {qul_count}")

# 5. Seven heavens by surah
print("\n📊 SEVEN HEAVENS BY SURAH:")
heavens_by_surah = {}
for surah_num, ayah_num in found:
    heavens_by_surah[surah_num] = heavens_by_surah.get(surah_num, 0) + 1
for surah, count in sorted(heavens_by_surah.items()):
    print(f"  Surah {surah}: {count} occurrence(s)")

# 6. Check for "seven earths" (سَبْعَ أَرْضِينَ)
print("\n📖 SEVEN EARTHS? (Searching for 'seven earths')")
found_earths = []
for surah_num, surah in data['surahs'].items():
    for ayah_num, text in surah['ayahs'].items():
        if "سَبْعَ أَرْضٍ" in text or "سَبْعَةِ أَرْضٍ" in text:
            found_earths.append((surah_num, ayah_num, text))
if found_earths:
    for s, a, t in found_earths:
        print(f"  ✅ Surah {s}:{a} - {t}")
else:
    print("  ❌ No mentions of 'seven earths' found")

# 7. Count of letter "س" (seen) - 7th letter of Arabic alphabet
print("\n📊 LETTER 'س' (SEEN) COUNT:")
seen_total = 0
for surah_num, surah in data['surahs'].items():
    for ayah_num, text in surah['ayahs'].items():
        seen_total += text.count('س')
print(f"  Total occurrences of letter 'س': {seen_total}")
print(f"  Divisible by 7? {seen_total % 7 == 0} (remainder: {seen_total % 7})")

# 8. Surah names with 7 Arabic letters
print("\n📖 SURAH NAMES WITH EXACTLY 7 ARABIC LETTERS:")
def count_arabic_letters(text):
    arabic = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئى')
    return len([c for c in text if c in arabic])

seven_letter_surahs = []
for num, surah in data['surahs'].items():
    letter_count = count_arabic_letters(surah['name'])
    if letter_count == 7:
        seven_letter_surahs.append((num, surah['name'], letter_count))
        print(f"  ✅ Surah {num}: {surah['name']} ({letter_count} letters)")
print(f"\n  TOTAL: {len(seven_letter_surahs)} surah names with 7 letters")

# 9. Check Basmala letter count (Surah 1:1-7)
print("\n📊 BASMALA (SURAH 1:1-7) ANALYSIS:")
if '1' in data['surahs']:
    basmala_text = data['surahs']['1']['ayahs']['1']
    letter_count = count_arabic_letters(basmala_text)
    word_count = len(basmala_text.split())
    print(f"  Text: {basmala_text}")
    print(f"  Arabic letters: {letter_count}")
    print(f"  Words: {word_count}")
    print(f"  Divisible by 7? Letters: {letter_count % 7 == 0}, Words: {word_count % 7 == 0}")

print("\n" + "=" * 60)
print("✅ EXTRACTION COMPLETE")
