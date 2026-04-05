#!/bin/bash
# Quran Code 7 Analysis - Shell-based approach

cd /home/ubuntu/.openclaw/workspace/quran-data

echo "🔍 QURAN CODE 7 VERIFICATION - SHELL ANALYSIS"
echo "=============================================="

# 1. Find seven heavens (سَبْعَ سَمَٰوَٰتٍ)
echo -e "\n1. SEVEN HEAVENS:"
echo "Searching for phrase 'سَبْعَ سَمَٰوَٰتٍ'..."
grep -r "سَبْعَ سَمَٰوَٰتٍ" quran-verified-dataset.json | wc -l
echo "Expected: occurrences in Surahs 41, 65, 67, 71"

# 2. Find seven days creation
echo -e "\n2. SEVEN DAYS OF CREATION:"
echo "Searching for patterns..."
grep -r "سَبْعَةَ أَيَّامٍ\|سَبْعَ أَيَّامٍ\|سَبْعَةِ أَيَّامٍ" quran-verified-dataset.json | wc -l
echo "Expected: 0 (Quran says six days)"

# 3. Find Seven Mathani
echo -e "\n3. SEVEN MATHANI (15:87):"
grep -A2 -B2 '"87":' quran-verified-dataset.json | grep "سَبْعًا"
echo "Expected: Found in Surah 15, Ayah 87"

# 4. Count "قُلْ" occurrences for phrase repetition test
echo -e "\n4. PHRASE 'قُلْ' REPETITIONS:"
grep -o "قُلْ" quran-verified-dataset.json | wc -l
echo "Expected: 5 (Surahs 109, 110, 112, 113, 114)"

# 5. Count word "سَبْعَ" (seven)
echo -e "\n5. WORD 'سَبْعَ' (seven) TOTAL COUNT:"
grep -o "سَبْعَ" quran-verified-dataset.json | wc -l
echo "Expected: At least 1 (from 15:87) + others"

# 6. Extract all surah numbers to verify 114 total
echo -e "\n6. TOTAL SURAH COUNT:"
grep -oP '"\d{1,3}": {' quran-verified-dataset.json | wc -l
echo "Expected: 114 surahs"

# 7. Check for 7-letter words (simple check for common words)
echo -e "\n7. 7-LETTER WORDS (Sample check):"
echo "Checking Basmala:"
echo "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ" | wc -c
echo "Characters in Basmala (with spaces)"

echo -e "\n=============================================="
echo "✅ SHELL ANALYSIS COMPLETE"
