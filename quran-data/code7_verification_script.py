#!/usr/bin/env python3
"""
Quran Code 7 Verification Script
Performs systematic analysis of Quranic text for Code 7 patterns
"""

import json
import re
from typing import Dict, List, Tuple, Counter
from collections import defaultdict

# Load the Quran dataset
with open('quran-data/quran-verified-dataset.json', 'r', encoding='utf-8') as f:
    quran_data = json.load(f)

# Arabic letter definitions (Uthmani script)
ARABIC_LETTERS = set([
    'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي',
    'ء', 'آ', 'أ', 'ؤ', 'إ', 'ئ', 'ى', 'ٱ'  # Including variants
])

def normalize_uthmani(text: str) -> str:
    """Normalize Uthmani script for consistent counting."""
    # Keep all letters including diacritics for accurate counting
    # Remove ayah markers, surah numbers, etc.
    text = re.sub(r'�bers+|ۜ|۝|۞|۟|۠|ۡ|ۢ|ۣ|ۤ|ۥ|ۦ|ۧ|ۨ|۩|۪|۫|۬|ۭ', '', text)  # Remove Arabic diacritics/ornaments
    text = text.strip()
    return text

def count_arabic_letters(text: str, normalize_variants: bool = False) -> int:
    """Count Arabic letters in text."""
    if normalize_variants:
        # Normalize alif variants to ا
        text = text.replace('آ', 'ا').replace('أ', 'ا').replace('إ', 'ا').replace('ئ', 'ء').replace('ى', 'ي')
    return len([c for c in text if c in ARABIC_LETTERS])

def count_specific_phrase(texts: List[str], phrase: str) -> int:
    """Count occurrences of exact phrase across all texts."""
    count = 0
    for text in texts:
        count += text.count(phrase)
    return count

def find_ayahs_with_phrase(quran_data: Dict, phrase: str) -> List[Tuple[int, int]]:
    """Find all ayahs containing the exact phrase."""
    results = []
    for surah_num, surah in quran_data['surahs'].items():
        for ayah_num, ayah_text in surah['ayahs'].items():
            if phrase in ayah_text:
                results.append((int(surah_num), int(ayah_num)))
    return results

def get_all_ayah_texts(quran_data: Dict) -> List[str]:
    """Extract all ayah texts as list."""
    all_texts = []
    for surah in quran_data['surahs'].values():
        all_texts.extend(surah['ayahs'].values())
    return all_texts

def analyze_seven_heavens(quran_data: Dict) -> Dict:
    """Analyze mentions of seven heavens."""
    phrase = "سَبْعَ سَمَٰوَٰتٍ"
    occurrences = find_ayahs_with_phrase(quran_data, phrase)
    return {
        "claim": "Seven heavens mentioned",
        "phrase": phrase,
        "occurrences": occurrences,
        "count": len(occurrences),
        "sources": [f"{s}:{a}" for s, a in occurrences],
        "status": "verified" if len(occurrences) > 0 else "rejected"
    }

def analyze_seven_days(quran_data: Dict) -> Dict:
    """Analyze mentions of seven days in creation."""
    # Look for various patterns of "seven days"
    phrases = ["سَبْعَةَ أَيَّامٍ", "سَبْعَ أَيَّامٍ", "سَبْعَةِ أَيَّامٍ"]
    total_count = 0
    all_occurrences = []
    for phrase in phrases:
        occ = find_ayahs_with_phrase(quran_data, phrase)
        all_occurrences.extend(occ)
    # Remove duplicates
    unique_occurrences = list(set(all_occurrences))
    return {
        "claim": "Seven days of creation",
        "phrases": phrases,
        "occurrences": unique_occurrences,
        "count": len(unique_occurrences),
        "sources": [f"{s}:{a}" for s, a in unique_occurrences],
        "status": "verified" if len(unique_occurrences) > 0 else "rejected"
    }

def analyze_seven_mathani(quran_data: Dict) -> Dict:
    """Analyze Surah 15:87 - Seven Mathani."""
    surah = quran_data['surahs'].get('15')
    if surah and '87' in surah['ayahs']:
        ayah_text = surah['ayahs']['87']
        has_seven = "سَبْعًا" in ayah_text
        has_mathani = "الْمَثَانِي" in ayah_text
        return {
            "claim": "Seven Mathani (oft-repeated)",
            "surah_ayah": "15:87",
            "text": ayah_text,
            "contains_seven": has_seven,
            "contains_mathani": has_mathani,
            "status": "verified" if has_seven and has_mathani else "rejected"
        }
    return {"claim": "Seven Mathani", "status": "error", "note": "Surah 15 not found or ayah 87 missing"}

def analyze_seven_letters_words(quran_data: Dict) -> Dict:
    """Find Arabic words with exactly 7 letters."""
    all_texts = get_all_ayah_texts(quran_data)
    all_words = []
    for text in all_texts:
        # Simple word split by spaces and punctuation
        words = re.split(r'[\s\u0640]+', text)  # Split by spaces and tatweel
        words = [w for w in words if w and count_arabic_letters(w) > 0]
        all_words.extend(words)

    word_counts = defaultdict(list)
    for word in set(all_words):  # Unique words only
        letter_count = count_arabic_letters(word)
        if letter_count == 7:
            word_counts[7].append(word)

    return {
        "claim": "Words with exactly 7 letters",
        "total_unique_words": len(set(all_words)),
        "seven_letter_words": word_counts[7],
        "count": len(word_counts[7]),
        "status": "verified" if len(word_counts[7]) > 0 else "rejected"
    }

def analyze_phrase_repetitions(quran_data: Dict, target_count: int = 7) -> Dict:
    """Find phrases repeated exactly target_count times."""
    all_texts = get_all_ayah_texts(quran_data)
    all_text = ' '.join(all_texts)

    # Common short phrases to check
    test_phrases = [
        "قُلْ",
        "إِنَّا",
        "وَاللَّهُ",
        "لَا إِلَٰهَ",
        "رَبِّ",
        "يَا أَيُّهَا"
    ]

    results = []
    for phrase in test_phrases:
        count = all_text.count(phrase)
        if count == target_count:
            results.append({
                "phrase": phrase,
                "count": count,
                "match": True
            })

    return {
        "claim": f"Phrases repeated exactly {target_count} times",
        "target_count": target_count,
        "found_phrases": results,
        "count": len(results),
        "status": "verified" if len(results) > 0 else "rejected"
    }

def analyze_surah_groupings(quran_data: Dict) -> Dict:
    """Analyze surah groupings of 7."""
    surahs = list(quran_data['surahs'].keys())
    surahs_int = sorted([int(s) for s in surahs])

    groupings = []

    # Check contiguous groups of 7
    for i in range(len(surahs_int) - 6):
        group = surahs_int[i:i+7]
        groupings.append({
            "group": group,
            "start_surah": group[0],
            "end_surah": group[6],
            "size": 7
        })

    return {
        "claim": "Contiguous groups of 7 surahs",
        "total_surahs": len(surahs_int),
        "possible_groups": len(groupings),
        "groups": groupings[:5],  # Show first 5
        "status": "verified" if len(groupings) > 0 else "rejected"
    }

def analyze_other_seven_patterns(quran_data: Dict) -> List[Dict]:
    """Search for other patterns involving number 7."""
    patterns = []

    # 1. Count of letter 'س' (seen) which numerically relates to 7?
    all_texts = get_all_ayah_texts(quran_data)
    all_text = ' '.join(all_texts)
    seen_count = all_text.count('س')
    if seen_count % 7 == 0:
        patterns.append({
            "pattern": "Letter س (Seen) count divisible by 7",
            "count": seen_count,
            "divisible_by_7": True,
            "status": "verified"
        })

    # 2. Count of word "سبع" (sab'a - seven) itself
    sabaa_count = all_text.count('سَبْعَ') + all_text.count('سَبْعَة')
    patterns.append({
        "pattern": "Word 'seven' (سَبْعَ/سَبْعَة) occurrences",
        "count": sabaa_count,
        "status": "verified" if sabaa_count > 0 else "rejected"
    })

    # 3. Surahs with 7 letters in their names (Arabic)
    seven_letter_names = []
    for num, surah in quran_data['surahs'].items():
        name = surah['name']
        letter_count = count_arabic_letters(name)
        if letter_count == 7:
            seven_letter_names.append({"surah": num, "name": name, "letters": letter_count})
    patterns.append({
        "pattern": "Surah names with exactly 7 Arabic letters",
        "count": len(seven_letter_names),
        "surahs": seven_letter_names,
        "status": "verified" if len(seven_letter_names) > 0 else "rejected"
    })

    return patterns

# Run all analyses
print("🔍 QURAN CODE 7 VERIFICATION - SYSTEMATIC ANALYSIS\n")
print("=" * 60)

results = {}

print("\n1. Analyzing Seven Heavens...")
results['seven_heavens'] = analyze_seven_heavens(quran_data)

print("\n2. Analyzing Seven Days of Creation...")
results['seven_days'] = analyze_seven_days(quran_data)

print("\n3. Analyzing Seven Mathani (15:87)...")
results['seven_mathani'] = analyze_seven_mathani(quran_data)

print("\n4. Analyzing 7-letter Words...")
results['seven_letter_words'] = analyze_seven_letters_words(quran_data)

print("\n5. Analyzing Phrase Repetitions (7x)...")
results['phrase_repetitions'] = analyze_phrase_repetitions(quran_data, 7)

print("\n6. Analyzing Surah Groupings...")
results['surah_groupings'] = analyze_surah_groupings(quran_data)

print("\n7. Analyzing Other Seven Patterns...")
results['other_patterns'] = analyze_other_seven_patterns(quran_data)

# Print summary
print("\n" + "=" * 60)
print("📊 VERIFICATION SUMMARY")
print("=" * 60)

for key, result in results.items():
    print(f"\n{key.upper().replace('_', ' ')}:")
    print(f"  Status: {result['status'].upper()}")
    if 'count' in result:
        print(f"  Count: {result['count']}")
    if 'sources' in result:
        print(f"  Sources: {', '.join(result['sources'])}")

# Save results to JSON
output = {
    "metadata": {
        "analysis_date": "2026-04-05",
        "dataset": "quran-verified-dataset_v1",
        "normalization": "uthmani_with_diacritics",
        "protocol": "truth-first_verification"
    },
    "results": results
}

with open('quran-data/code7-systematic-results.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n✅ Results saved to quran-data/code7-systematic-results.json")
print("\n🔍 ANALYSIS COMPLETE")
