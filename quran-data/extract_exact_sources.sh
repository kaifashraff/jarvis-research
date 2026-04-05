#!/bin/bash
# Extract exact sources for Code 7 patterns from JSON dataset

DATAFILE="quran-verified-dataset.json"

echo "🔍 EXTRACTING EXACT SOURCES FOR CODE 7 PATTERNS"
echo "================================================"

# 1. Seven heavens (سَبْعَ سَمَٰوَٰتٍ)
echo -e "\n📖 SEVEN HEAVENS - EXACT SOURCES:"
echo "Searching for phrase 'سَبْعَ سَمَٰوَٰتٍ'..."
grep -n "سَبْعَ سَمَٰوَٰتٍ" "$DATAFILE" | head -10
echo "(Showing first 10 matches if any)"

# 2. Count total occurrences
echo -e "\n📊 COUNT:"
TOTAL_HEAVENS=$(grep -c "سَبْعَ سَمَٰوَٰتٍ" "$DATAFILE")
echo "  Seven heavens occurrences: $TOTAL_HEAVENS"

# 3. Seven Mathani (15:87)
echo -e "\n📖 SEVEN MATHANI (15:87):"
grep -A2 '"87"' "$DATAFILE" | grep "سَبْعًا"
echo "Expected: 'وَلَقَدْ آتَيْنَاكَ سَبْعًا مِّنَ الْمَثَانِي'"

# 4. Phrase "قُلْ" count
echo -e "\n📊 PHRASE 'قُلْ' COUNT:"
# Simple count - note this may overcount in middle of words
QUL_COUNT=$(grep -o "قُلْ" "$DATAFILE" | wc -l)
echo "  Total 'قُلْ' occurrences: $QUL_COUNT"
echo "  (In full Quran: appears 5 times in Meccan surahs 109-114)"

# 5. Word "سَبْعَ" (seven) total
echo -e "\n📊 WORD 'سَبْعَ' (SEVEN) TOTAL:"
SEVEN_COUNT=$(grep -o "سَبْعَ" "$DATAFILE" | wc -l)
echo "  Total 'سَبْعَ' occurrences: $SEVEN_COUNT"

# 6. Check for "seven earths"
echo -e "\n📖 SEVEN EARTHS? (سَبْعَ أَرْضٍ):"
grep -n "سَبْعَ أَرْضٍ\|سَبْعَةِ أَرْضٍ" "$DATAFILE" || echo "  ❌ No mentions found"

# 7. Total surah count in dataset
echo -e "\n📊 DATASET INFO:"
TOTAL_SURAHS=$(grep -oP '"\d{1,3}": {' "$DATAFILE" | wc -l)
echo "  Total surahs in dataset: $TOTAL_SURAHS"
echo "  Expected full Quran: 114"

# 8. Extract specific ayahs for evidence
echo -e "\n📋 EXTRACTING KEY AYAHS FOR EVIDENCE LEDGER:"
echo ""
echo "Surah 41:12 (Seven heavens):"
grep -A1 '"12":' "$DATAFILE" | grep -A1 '"41":' | head -3
echo ""
echo "Surah 65:12 (Seven heavens):"
grep -A1 '"12":' "$DATAFILE" | grep -A1 '"65":' | head -3
echo ""
echo "Surah 67:3 (Seven heavens):"
grep -A1 '"3":' "$DATAFILE" | grep -A1 '"67":' | head -3
echo ""
echo "Surah 71:15 (Seven heavens):"
grep -A1 '"15":' "$DATAFILE" | grep -A1 '"71":' | head -3
echo ""
echo "Surah 15:87 (Seven Mathani):"
grep -A1 '"87":' "$DATAFILE" | grep -A1 '"15":' | head -3

echo -e "\n================================================"
echo "✅ EXTRACTION COMPLETE"
