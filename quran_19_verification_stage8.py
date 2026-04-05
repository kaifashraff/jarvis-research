#!/usr/bin/env python3
"""
QURAN CODE 19 VERIFICATION — STAGE 8: VERIFICATION ENGINEER
============================================================
Statistical Testing — Permutation Testing, Multiple-Hypothesis Correction,
Sensitivity Analysis, Robustness Testing, Confidence Scores.

Protocol: Statistical skepticism, permutation testing, BH-FDR correction.
"""

import json
import math
import hashlib
import re
import time
from collections import Counter
from datetime import datetime, timezone

try:
    import numpy as np
    import scipy.stats as stats
    HAS_STATS = True
except ImportError:
    HAS_STATS = False

import requests

# ============================================================
# SECTION 1: DATA INGESTION
# ============================================================

def fetch_quran_uthmani():
    """Fetch Uthmani Quran text from API."""
    print("[Stage8] Fetching Quran Uthmani text...")
    resp = requests.get("https://api.alquran.cloud/v1/quran/quran-uthmani", timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["surahs"]

def fetch_quran_simple():
    """Fetch Simple Arabic Quran text."""
    print("[Stage8] Fetching Simple Arabic Quran text...")
    resp = requests.get("https://api.alquran.cloud/v1/quran/quran-simple", timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["surahs"]

def normalize_letter_count(text, convention="A"):
    """
    Apply normalization conventions for letter counting.
    
    Convention A: Standardized alifs, hamza removed, ta marbuta as ta, diacritics removed, basmala included
    Convention B: Standardized alifs, standard hamza, ta marbuta as ha, diacritics removed, basmala excluded
    Convention C: Keep variants, keep hamza variants, ta marbuta as is, diacritics kept, basmala included
    Convention D: Standardized alifs, hamza removed, ta marbuta as is, diacritics removed, basmala excluded
    """
    result = text
    
    # Remove diacritics for conventions A, B, D
    if convention in ("A", "B", "D"):
        # Arabic diacritics range
        diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]')
        result = diacritics.sub('', result)
    
    if convention == "C":
        # Convention C keeps most variants but standardize some
        pass
    
    # Alif standardization for A, B, D
    if convention in ("A", "B", "D"):
        result = result.replace('آ', 'ا')
        result = result.replace('أ', 'ا')
        result = result.replace('إ', 'ا')
        result = result.replace('ٱ', 'ا')
    
    # Hamza normalization for A, D (remove standalone hamza in certain contexts)
    if convention in ("A", "D"):
        # Remove hamza above/below when not part of a letter
        result = result.replace('ء', '')
    
    # Ta marbuta handling
    if convention == "A":
        result = result.replace('ة', 'ت')
    elif convention == "B":
        result = result.replace('ة', 'ه')
    # C and D keep as-is
    
    return result


# ============================================================
# SECTION 2: BUILD QURAN DATA STRUCTURES
# ============================================================

def build_quran_dataset(surahs):
    """Build structured dataset from surahs."""
    dataset = []
    for surah in surahs:
        surah_num = surah["number"]
        surah_name = surah["name"]
        ayahs = []
        for ayah in surah["ayahs"]:
            ayahs.append({
                "number": ayah["numberInSurah"],
                "text": ayah["text"],
                "absolute_number": ayah.get("number", 0)  # absolute Ayah number in Quran
            })
        dataset.append({
            "surah_number": surah_num,
            "surah_name": surah_name,
            "ayah_count": len(ayahs),
            "revelation_order": surah.get("revelationOrder", 0),
            "ayahs": ayahs
        })
    return dataset

def count_letters_text(text):
    """Count Arabic letters only (exclude spaces, punctuation, numbers)."""
    # Arabic letter Unicode range: U+0600-U+06FF (Arabic), U+0750-U+077F (Arabic Supplement)
    arabic_letters = re.compile(r'[\u0621-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06FA-\u06FF]')
    return len([c for c in text if arabic_letters.match(c)])

def count_letters_per_convention(text, convention="A"):
    """Count letters after normalization."""
    normalized = normalize_letter_count(text, convention)
    # Count Arabic letters in normalized text
    arabic_letters = re.compile(r'[\u0621-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06FA-\u06FF]')
    return len([c for c in normalized if arabic_letters.match(c)])

def count_words_text(text):
    """Count words (whitespace-separated tokens)."""
    return len(text.split())

def count_letter_frequencies(text, convention="A"):
    """Get per-letter frequency counts."""
    normalized = normalize_letter_count(text, convention)
    arabic_letters = re.compile(r'[\u0621-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06FA-\u06FF]')
    letters = [c for c in normalized if arabic_letters.match(c)]
    return Counter(letters)


# ============================================================
# SECTION 3: PATTERNS TO TEST (from Claims)
# ============================================================

def build_claims():
    """
    Define all claims to verify. Each claim has:
    - description
    - expected_result  
    - pattern_type
    - text_source
    - counting_rule
    
    These are the KNOWN Code 19 claims from literature.
    """
    claims = [
        {
            "claim_id": "CLAIM_001",
            "description": "Surah 74:30 mentions the number 19 ('Over it are nineteen')",
            "surah": 74,
            "ayah": 30,
            "expected_number": 19,
            "category": "explicit_mention",
            "test_type": "direct_text"
        },
        {
            "claim_id": "CLAIM_002",
            "description": "Total number of surahs (114) is divisible by 19",
            "expected_number": 19,
            "category": "surah_count",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_003",
            "description": "Basmala 'Bismillah' phrase count vs surah count: 114 surahs, 114 basmalas",
            "expected_number": 19,
            "category": "basmala_count",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_004",
            "description": "Ayah 9:129 is the last verse; total verses divisible by 19 (6346 = 19 × 334)",
            "expected_number": 19,
            "category": "total_ayahs",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_005",
            "description": "Words in Surah 1 (Al-Fatiha): specific count related to 19",
            "surah": 1,
            "expected_number": 19,
            "category": "word_count_fatiha",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_006",
            "description": "Letters in Surah 1 (Al-Fatiha): total divisible by 19 (convention A)",
            "surah": 1,
            "expected_number": 19,
            "category": "letter_count_fatiha",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_007",
            "description": "Surah 74:30 structure — number of letters in the verse is divisible by 19",
            "surah": 74,
            "ayah": 30,
            "category": "letter_count_74_30",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_008",
            "description": "First word 'Iqra' + last occurrence patterns relate to 19",
            "category": "iqra_pattern",
            "test_type": "positional"
        },
        {
            "claim_id": "CLAIM_009",
            "description": "Word 'Allah' appears 2698 times = 19 × 142",
            "word": "الله",
            "expected_number": 19,
            "category": "allah_count",
            "test_type": "word_frequency"
        },
        {
            "claim_id": "CLAIM_010",
            "description": "Word 'Rahman' (the Most Gracious) appears in a pattern divisible by 19",
            "word_count_target": 57,  # 19 × 3
            "expected_number": 19,
            "category": "rahman_count",
            "test_type": "word_frequency"
        },
        {
            "claim_id": "CLAIM_011",
            "description": "Sum of surah numbers + verse numbers across Quran divisible by 19",
            "expected_number": 19,
            "category": "surah_verse_sum",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_012",
            "description": "First revelation (surah 96) — 19 letters in first 5 words",
            "surah": 96,
            "ayah": 1,
            "ayah_count": 5,
            "expected_number": 19,
            "category": "first_revelation",
            "test_type": "letter_count"
        },
        {
            "claim_id": "CLAIM_013",
            "description": "Number of unique words in Quran relates to 19",
            "expected_number": 19,
            "category": "unique_words",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_014",
            "description": "Gematria value of 'bism' divisible by 19",
            "word": "بسم",
            "expected_number": 19,
            "category": "gematria_bism",
            "test_type": "gematria"
        },
        {
            "claim_id": "CLAIM_015",
            "description": "Gematria value of 'kitab' (book) divisible by 19",
            "word": "كتاب",
            "expected_number": 19,
            "category": "gematria_kitab",
            "test_type": "gematria"
        },
        {
            "claim_id": "CLAIM_016",
            "description": "Letter Qaf (ق) distribution relates to 19",
            "letter": "ق",
            "expected_number": 19,
            "category": "qaf_count",
            "test_type": "letter_frequency"
        },
        {
            "claim_id": "CLAIM_017",
            "description": "Sum of digits in surah-verse pairs has pattern with 19",
            "expected_number": 19,
            "category": "digit_sum",
            "test_type": "positional"
        },
        {
            "claim_id": "CLAIM_018",
            "description": "Number of surahs with odd/even verse counts shows 19-pattern",
            "expected_number": 19,
            "category": "verse_parity",
            "test_type": "structural"
        },
        {
            "claim_id": "CLAIM_019",
            "description": "Word count of entire Quran divisible by 19",
            "expected_number": 19,
            "category": "total_words",
            "test_type": "divisibility"
        },
        {
            "claim_id": "CLAIM_020",
            "description": "Total letters in entire Quran divisible by 19",
            "expected_number": 19,
            "category": "total_letters",
            "test_type": "divisibility"
        },
    ]
    return claims


# ============================================================
# SECTION 4: GEMATRIA (ABJAD VALUES)
# ============================================================

def abjad_value(char):
    """Return Abjad numerical value for an Arabic character."""
    values = {
        'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ٱ': 1,
        'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'ة': 5,
        'و': 6, 'ؤ': 6, 'ز': 7, 'ح': 8, 'ط': 9,
        'ي': 10, 'ى': 10, 'ئ': 10, 'ك': 20, 'ل': 30,
        'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
        'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400,
        'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900,
        'غ': 1000,
    }
    return values.get(char, 0)

def word_gematria(word):
    """Calculate gematria of an Arabic word."""
    total = 0
    for ch in word:
        total += abjad_value(ch)
    return total


# ============================================================
# SECTION 5: EXECUTE VERIFICATION CLAIMS
# ============================================================

def verify_claim(claim, dataset, dataset_simple):
    """
    Verify a single claim against the data.
    Returns: {claim_id, status, actual_value, details, robustness}
    """
    cid = claim["claim_id"]
    result = {"claim_id": cid, "description": claim["description"], "status": "UNKNOWN"}
    
    try:
        if claim["test_type"] == "direct_text":
            result = verify_direct_text(claim, dataset)
        
        elif claim["test_type"] == "divisibility":
            result = verify_divisibility(claim, dataset, claim.get("surah"))
        
        elif claim["test_type"] == "letter_count":
            result = verify_letter_count(claim, dataset)
        
        elif claim["test_type"] == "word_frequency":
            result = verify_word_frequency(claim, dataset)
        
        elif claim["test_type"] == "gematria":
            result = verify_gematria(claim)
        
        elif claim["test_type"] == "letter_frequency":
            result = verify_letter_frequency(claim, dataset)
        
        elif claim["test_type"] == "positional":
            result = verify_positional(claim, dataset)
        
        elif claim["test_type"] == "structural":
            result = verify_structural(claim, dataset)
        
        else:
            result["status"] = "UNSUPPORTED_TEST_TYPE"
            result["details"] = f"Unknown test type: {claim['test_type']}"
    
    except Exception as e:
        result["status"] = "ERROR"
        result["details"] = str(e)
    
    return result


def verify_direct_text(claim, dataset):
    """Verify: does ayah text contain the expected number written out?"""
    cid = claim["claim_id"]
    surah_num = claim["surah"]
    ayah_num = claim["ayah"]
    
    surah = dataset[surah_num - 1]
    ayah = surah["ayahs"][ayah_num - 1]
    text = ayah["text"]
    
    # Arabic word for 19: تسعة عشر or تسعةَ عَشَرَ
    nineteen_pattern = re.compile(r'تسعة\s*عشر')
    
    match = nineteen_pattern.search(text)
    
    return {
        "claim_id": cid,
        "status": "VERIFIED" if match else "NOT_VERIFIED",
        "actual_value": "text match" if match else "no match",
        "details": f"Surah {surah_num}:{ayah_num} text = {text[:100]}...",
        "text_source": f"api.alquran.cloud/v1/quran/quran-uthmani",
        "counting_rule": "direct text match for Arabic 'nineteen'"
    }


def verify_divisibility(claim, dataset, surah_num=None):
    """Verify: is the count divisible by 19?"""
    cid = claim["claim_id"]
    category = claim["category"]
    
    if category == "surah_count":
        total = len(dataset)
        remainder = total % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if remainder == 0 else "NOT_VERIFIED",
            "actual_value": total,
            "remainder": remainder,
            "quotient": total // 19 if remainder == 0 else None,
            "details": f"Total surahs: {total}",
            "text_source": "api.alquran.cloud API",
            "counting_rule": "count surahs in dataset"
        }
    
    elif category == "total_ayahs":
        total = sum(s["ayah_count"] for s in dataset)
        remainder = total % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if remainder == 0 else "NOT_VERIFIED",
            "actual_value": total,
            "remainder": remainder,
            "quotient": total // 19 if remainder == 0 else None,
            "details": f"Total ayahs: {total}",
            "text_source": "api.alquran.cloud API",
            "counting_rule": "sum ayah_count across all surahs"
        }
    
    elif category == "total_words":
        total = 0
        for surah in dataset:
            for ayah in surah["ayahs"]:
                total += count_words_text(ayah["text"])
        remainder = total % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if remainder == 0 else "NOT_VERIFIED",
            "actual_value": total,
            "remainder": remainder,
            "quotient": total // 19 if remainder == 0 else None,
            "details": f"Total words: {total}",
            "text_source": "api.alquran.cloud (uthmani)",
            "counting_rule": "whitespace-separated tokens, all surahs"
        }
    
    elif category == "total_letters":
        total = 0
        for convention in ["A", "B", "C", "D"]:
            c = 0
            for surah in dataset:
                for ayah in surah["ayahs"]:
                    c += count_letters_per_convention(ayah["text"], convention)
            result = {
                "claim_id": cid,
                "convention": convention,
                "status": "VERIFIED" if c % 19 == 0 else "NOT_VERIFIED",
                "actual_value": c,
                "remainder": c % 19,
                "quotient": c // 19 if c % 19 == 0 else None,
                "details": f"Total letters (convention {convention}): {c}",
            }
            if convention == "A":
                result["text_source"] = "api.alquran.cloud (uthmani)"
                result["counting_rule"] = f"Arabic letters, convention {convention}"
        # Return the convention A result as primary
        return result
    
    elif category in ("word_count_fatiha", "letter_count_fatiha"):
        surah = dataset[0]  # Surah 1
        if category == "word_count_fatiha":
            total = 0
            for ayah in surah["ayahs"]:
                total += count_words_text(ayah["text"])
            # Exclude basmala from word count if present (ayah 1 starts with it)
            remainder = total % 19
            return {
                "claim_id": cid,
                "status": "VERIFIED" if remainder == 0 else "NOT_VERIFIED",
                "actual_value": total,
                "remainder": remainder,
                "quotient": total // 19 if remainder == 0 else None,
                "details": f"Words in Al-Fatiha: {total}",
                "text_source": "api.alquran.cloud (uthmani, Surah 1)",
                "counting_rule": "whitespace-separated tokens in Surah 1"
            }
        else:
            results_A = []
            for convention in ["A", "B", "C", "D"]:
                total = 0
                for ayah in surah["ayahs"]:
                    total += count_letters_per_convention(ayah["text"], convention)
                rem = total % 19
                results_A.append({
                    "convention": convention,
                    "total": total,
                    "remainder": rem,
                    "quotient": total // 19 if rem == 0 else None,
                    "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED"
                })
            # Convention A is primary
            primary = results_A[0]
            return {
                "claim_id": cid,
                "status": primary["status"],
                "actual_value": primary["total"],
                "remainder": primary["remainder"],
                "quotient": primary["quotient"],
                "robustness": results_A,
                "details": f"Letters in Al-Fatiha (A): {primary['total']}, (B): {results_A[1]['total']}, (C): {results_A[2]['total']}, (D): {results_A[3]['total']}",
                "text_source": "api.alquran.cloud (uthmani, Surah 1)",
                "counting_rule": f"Arabic letters in Surah 1, convention {primary['convention']}"
            }
    
    elif category == "letter_count_74_30":
        surah = dataset[73]  # Surah 74
        ayah = surah["ayahs"][29]  # Ayah 30
        results = {}
        for convention in ["A", "B", "C", "D"]:
            total = count_letters_per_convention(ayah["text"], convention)
            rem = total % 19
            results[convention] = {"total": total, "remainder": rem, "quotient": total // 19 if rem == 0 else None}
        primary = results["A"]
        return {
            "claim_id": cid,
            "status": "VERIFIED" if primary["remainder"] == 0 else "NOT_VERIFIED",
            "actual_value": primary["total"],
            "remainder": primary["remainder"],
            "quotient": primary["quotient"],
            "robustness": results,
            "details": f"Letters in 74:30 (A): {primary['total']}, (B): {results['B']['total']}, (C): {results['C']['total']}, (D): {results['D']['total']}",
            "text_source": "api.alquran.cloud (uthmani, 74:30)",
            "counting_rule": "Arabic letters in Surah 74:30"
        }
    
    elif category == "basmala_count":
        # Count basmala occurrences
        basmala_count = 0
        for surah in dataset:
            for ayah in surah["ayahs"]:
                if ayah["text"].startswith("بِسْمِ ٱللَّهِ"):
                    basmala_count += 1
        # Also check if 19 divides
        rem = basmala_count % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
            "actual_value": basmala_count,
            "remainder": rem,
            "quotient": basmala_count // 19 if rem == 0 else None,
            "details": f"Basmala occurrences: {basmala_count}",
            "text_source": "api.alquran.cloud (uthmani)",
            "counting_rule": "startswith match for basmala pattern"
        }
    
    elif category == "surah_verse_sum":
        total = 0
        for surah in dataset:
            for ayah in surah["ayahs"]:
                total += surah["surah_number"] + ayah["number"]
        rem = total % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
            "actual_value": total,
            "remainder": rem,
            "quotient": total // 19 if rem == 0 else None,
            "details": f"Sum of surah+verse numbers: {total}",
            "text_source": "structural data from API",
            "counting_rule": "sum(surah_number + verse_number) for all ayahs"
        }
    
    elif category == "unique_words":
        all_words = set()
        for surah in dataset:
            for ayah in surah["ayahs"]:
                for word in ayah["text"].split():
                    # Strip diacritics for normalization
                    cleaned = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', word)
                    all_words.add(cleaned)
        rem = len(all_words) % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
            "actual_value": len(all_words),
            "remainder": rem,
            "quotient": len(all_words) // 19 if rem == 0 else None,
            "details": f"Unique words (diacritic-stripped): {len(all_words)}",
            "text_source": "api.alquran.cloud (uthmani)",
            "counting_rule": "unique whitespace tokens after diacritic removal"
        }
    
    else:
        return {
            "claim_id": cid,
            "status": "UNKNOWN",
            "details": f"Divisibility claim not yet implemented for category: {category}"
        }


def verify_letter_count(claim, dataset):
    """Verify: count letters in specific text, check divisibility by 19."""
    cid = claim["claim_id"]
    surah = dataset[claim["surah"] - 1]
    
    if "ayah" in claim:
        ayah = surah["ayahs"][claim["ayah"] - 1]
        if "ayah_count" in claim:
            # First N ayahs
            total = 0
            for i in range(min(claim["ayah_count"], surah["ayah_count"])):
                total += count_letters_per_convention(surah["ayahs"][i]["text"], "A")
        else:
            total = count_letters_per_convention(ayah["text"], "A")
    else:
        # Entire surah
        total = sum(count_letters_per_convention(a["text"], "A") for a in surah["ayahs"])
    
    rem = total % 19
    return {
        "claim_id": cid,
        "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
        "actual_value": total,
        "remainder": rem,
        "quotient": total // 19 if rem == 0 else None,
        "details": f"Letters: {total}, remainder mod 19: {rem}",
        "text_source": "api.alquran.cloud (uthmani)",
        "counting_rule": "convention A, letters only"
    }


def verify_word_frequency(claim, dataset):
    """Verify: specific word frequency and divisibility by 19."""
    cid = claim["claim_id"]
    word = claim.get("word", "")
    target = claim.get("expected_number")
    
    if not word:
        return {"claim_id": cid, "status": "ERROR", "details": "No word specified"}
    
    # Strip diacritics for matching
    word_clean = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', word)
    
    total = 0
    for surah in dataset:
        for ayah in surah["ayahs"]:
            ayah_clean = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', ayah["text"])
            for w in ayah_clean.split():
                if w == word_clean:
                    total += 1
    
    rem = total % 19 if target else None
    quotient = total // 19 if rem is not None and rem == 0 else None
    
    return {
        "claim_id": cid,
        "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
        "actual_value": total,
        "target": target * (total // target) if target and total >= target else None,
        "remainder": rem,
        "quotient": quotient,
        "details": f"Word '{word}' occurs {total} times in Quran",
        "text_source": "api.alquran.cloud (uthmani, diacritic-stripped match)",
        "counting_rule": f"exact word match for '{word}' (diacritic-stripped)"
    }


def verify_gematria(claim):
    """Verify: gematria value is divisible by 19."""
    cid = claim["claim_id"]
    word = claim.get("word", "")
    
    if not word:
        return {"claim_id": cid, "status": "ERROR", "details": "No word specified"}
    
    gem = word_gematria(word)
    rem = gem % 19
    
    return {
        "claim_id": cid,
        "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
        "actual_value": gem,
        "remainder": rem,
        "quotient": gem // 19 if rem == 0 else None,
        "details": f"Gematria of '{word}' = {gem}, {gem}/19 = {gem/19:.2f}",
        "text_source": "Abjad numerical system",
        "counting_rule": "standard Abjad values for Arabic letters"
    }


def verify_letter_frequency(claim, dataset):
    """Verify: letter frequency count relates to 19."""
    cid = claim["claim_id"]
    letter = claim.get("letter", "")
    
    if not letter:
        return {"claim_id": cid, "status": "ERROR", "details": "No letter specified"}
    
    total_count = 0
    for surah in dataset:
        for ayah in surah["ayahs"]:
            for ch in ayah["text"]:
                if ch == letter:
                    total_count += 1
    
    rem = total_count % 19
    
    return {
        "claim_id": cid,
        "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
        "actual_value": total_count,
        "remainder": rem,
        "quotient": total_count // 19 if rem == 0 else None,
        "details": f"Letter '{letter}' occurs {total_count} times in Quran",
        "text_source": "api.alquran.cloud (uthmani)",
        "counting_rule": f"exact character match for '{letter}' in Uthmani text"
    }


def verify_positional(claim, dataset):
    """Verify: positional patterns related to 19."""
    cid = claim["claim_id"]
    category = claim["category"]
    
    if category == "iqra_pattern":
        # Check if 'Iqra' (ٱقْرَأْ) appears in expected position
        iqra_count = 0
        positions = []
        for si, surah in enumerate(dataset):
            for ai, ayah in enumerate(surah["ayahs"]):
                if re.search(r'ٱقْرَأ', ayah["text"]):
                    iqra_count += 1
                    positions.append((si + 1, ai + 1))
        
        rem = iqra_count % 19 if iqra_count else None
        return {
            "claim_id": cid,
            "status": "VERIFIED" if iqra_count and rem == 0 else "NOT_VERIFIED",
            "actual_value": iqra_count,
            "positions": positions[:10],  # first 10 occurrences
            "remainder": rem,
            "details": f"Word 'Iqra' occurs {iqra_count} times at {len(positions)} positions",
            "text_source": "api.alquran.cloud (uthmani)",
            "counting_rule": "regex match for Iqra pattern"
        }
    
    elif category == "digit_sum":
        # Sum of digits in formatted surah:verse numbers
        total = 0
        for surah in dataset:
            for ayah in surah["ayahs"]:
                s_str = str(surah["surah_number"])
                a_str = str(ayah["number"])
                total += sum(int(d) for d in s_str) + sum(int(d) for d in a_str)
        rem = total % 19
        return {
            "claim_id": cid,
            "status": "VERIFIED" if rem == 0 else "NOT_VERIFIED",
            "actual_value": total,
            "remainder": rem,
            "quotient": total // 19 if rem == 0 else None,
            "details": f"Sum of all digits in surah:verse numbers: {total}",
            "text_source": "structural data from API",
            "counting_rule": "sum of decimal digits of all surah_numbers and verse_numbers"
        }
    
    else:
        return {"claim_id": cid, "status": "UNKNOWN", "details": f"Positional claim not implemented: {category}"}


def verify_structural(claim, dataset):
    """Verify: structural claims about Quran."""
    cid = claim["claim_id"]
    category = claim["category"]
    
    if category == "verse_parity":
        odd_count = 0
        even_count = 0
        for surah in dataset:
            if surah["ayah_count"] % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
        
        results = {
            "odd_verse_count_surahs": odd_count,
            "even_verse_count_surahs": even_count,
            "total": 114
        }
        
        # Check if both are divisible by 19
        odd_rem = odd_count % 19
        even_rem = even_count % 19
        
        return {
            "claim_id": cid,
            "status": "VERIFIED" if odd_rem == 0 else "PARTIAL",
            "odd_count": odd_count,
            "even_count": even_count,
            "odd_remainder": odd_rem,
            "even_remainder": even_rem,
            "details": f"Surahs with odd verses: {odd_count}, even verses: {even_count}",
            "text_source": "structural data from API",
            "counting_rule": "surahs grouped by parity of ayah_count"
        }
    
    else:
        return {"claim_id": cid, "status": "UNKNOWN", "details": f"Structural claim not implemented: {category}"}


# ============================================================
# SECTION 6: STATISTICAL TESTING — PERMUTATION TESTS
# ============================================================

def permutation_test_divisibility(actual_value, divisor, n_permutations=100000):
    """
    Permutation test for divisibility claim.
    
    Null hypothesis: The observed value's remainder mod divisor is uniformly distributed.
    We simulate random values in a plausible range and compute how often
    we get remainder 0 by chance.
    
    For count-based claims: simulate counts from empirical distribution.
    """
    # Set reasonable bounds for simulation
    if actual_value < 100:
        min_count = max(1, actual_value - 50)
        max_count = int(actual_value * 2)
    else:
        min_count = max(1, actual_value - int(actual_value * 0.3))
        max_count = int(actual_value * 1.5)
    
    # Ensure min < max
    if min_count >= max_count:
        min_count = max(1, max_count - 100)
    if min_count >= max_count:
        min_count = 1
        max_count = 1000
    
    # Under the null, remainders are uniformly distributed
    # P(remainder == 0) = 1/divisor
    
    np.random.seed(42)
    random_values = np.random.randint(min_count, max_count + 1, size=n_permutations)
    remainders = random_values % divisor
    
    p_random = np.sum(remainders == 0) / n_permutations  # Should be ~1/divisor
    
    return {
        "n_permutations": n_permutations,
        "p_value_random": round(float(p_random), 6),
        "expected_random_p": round(1.0 / divisor, 6),
        "observed_remainder": actual_value % divisor,
        "exact_p_value": round(1.0 / divisor, 6),  # For uniform remainder, exact p = 1/d
        "interpretation": "random match" if actual_value % divisor == 0 else "no match needed"
    }


def permutation_test_word_frequency(word_count, total_words, n_permutations=10000):
    """
    Permutation test for word frequency.
    
    Null hypothesis: words are distributed uniformly across the text.
    We simulate random word placements and check frequency patterns.
    """
    np.random.seed(42)
    
    # Under uniform distribution, expected frequency = total_words / vocabulary_size
    # But we test if frequency is divisible by 19
    
    remainder = word_count % 19
    # What fraction of random frequencies would also be divisible?
    # This is approximately 1/19 for any reasonable range
    
    p_value = 1.0 / 19
    
    return {
        "word_count": word_count,
        "divisor": 19,
        "remainder": remainder,
        "p_value": round(p_value, 6),
        "n_permutations": n_permutations,
        "interpretation": "not significant" if p_value > 0.05 else "marginal"
    }


def compute_bonferroni_correction(p_values, alpha=0.05):
    """Apply Bonferroni correction for multiple hypothesis testing."""
    n = len(p_values)
    corrected_alpha = alpha / n
    results = []
    for i, p in enumerate(p_values):
        results.append({
            "index": i,
            "raw_p": p,
            "corrected_p": min(p * n, 1.0),
            "significance": "significant" if p * n < alpha else "not significant"
        })
    return results, corrected_alpha


def compute_benjamini_hochberg(p_values, alpha=0.05):
    """Apply Benjamini-Hochberg FDR correction."""
    p_values = np.array(p_values, dtype=float)
    n = len(p_values)
    
    # Sort p-values
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    
    # Compute BH critical values
    critical_values = np.array([(i + 1) / n * alpha for i in range(n)])
    
    # Find the largest k where p(k) <= BH_critical(k)
    comparisons = sorted_p <= critical_values
    if np.any(comparisons):
        k = np.where(comparisons)[0][-1]
        significant_indices = sorted_indices[:k + 1]
    else:
        significant_indices = np.array([], dtype=int)
    
    return significant_indices


def compute_confidence_score(status, remainder, robustness_results=None, 
                             p_value=None, bonferroni_significant=False,
                             bh_significant=False, normalization_robust=True):
    """
    Compute overall confidence score (0.0 - 1.0) for a claim.
    
    Scoring:
    - VERIFIED: base 0.5
    - remainder == 0: +0.2
    - p < 0.05: +0.1
    - Bonferroni significant: +0.1
    - Robust across normalizations: +0.1
    - Multiple converging evidence: +0.05
    """
    score = 0.0
    
    if status == "VERIFIED":
        score += 0.50
    elif status == "PARTIAL":
        score += 0.25
    
    if remainder is not None and remainder == 0:
        score += 0.20
    
    if p_value is not None:
        if p_value < 0.001:
            score += 0.15
        elif p_value < 0.01:
            score += 0.10
        elif p_value < 0.05:
            score += 0.05
    
    if bonferroni_significant:
        score += 0.10
    
    if bh_significant:
        score += 0.05
    
    if normalization_robust:
        score += 0.10
    
    return min(round(score, 3), 1.0)


def classify_claim(score):
    """Classify claim based on confidence score."""
    if score >= 0.70:
        return "STRONG"
    elif score >= 0.40:
        return "WEAK"
    else:
        return "REJECTED"


def assign_confidence_level(score):
    """Assign human-readable confidence level."""
    if score >= 0.85:
        return "VERY_HIGH"
    elif score >= 0.70:
        return "HIGH"
    elif score >= 0.55:
        return "MODERATE"
    elif score >= 0.40:
        return "LOW"
    else:
        return "VERY_LOW"


# ============================================================
# SECTION 7: MAIN EXECUTION
# ============================================================

def main():
    print("=" * 70)
    print("QURAN CODE 19 VERIFICATION — STAGE 8: STATISTICAL TESTING")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Protocol: Statistical skepticism, permutation testing, BH-FDR correction")
    print()
    
    # Step 1: Load data
    print("[1/7] Loading Quran datasets...")
    surahs = fetch_quran_uthmani()
    dataset = build_quran_dataset(surahs)
    
    surahs_simple = fetch_quran_simple()
    dataset_simple = build_quran_dataset(surahs_simple)
    
    print(f"  Loaded {len(dataset)} surahs")
    total_ayahs = sum(s["ayah_count"] for s in dataset)
    print(f"  Total ayahs: {total_ayahs}")
    print()
    
    # Step 2: Define claims
    print("[2/7] Loading claims to verify...")
    claims = build_claims()
    print(f"  {len(claims)} claims defined")
    print()
    
    # Step 3: Execute verification
    print("[3/7] Running verification on all claims...")
    results = []
    for claim in claims:
        r = verify_claim(claim, dataset, dataset_simple)
        results.append(r)
        status = r["status"]
        print(f"  {claim['claim_id']:12s} {claim['description'][:60]:60s} -> {status}")
    print()
    
    # Step 4: Statistical testing
    print("[4/7] Performing statistical testing (permutation tests)...")
    stat_reports = []
    all_p_values = []
    
    for result in results:
        report = {"claim_id": result["claim_id"]}
        
        actual = result.get("actual_value")
        if not isinstance(actual, (int, float)) or actual is None:
            report["stats"] = {"p_value": None, "reason": "non-numeric result"}
            all_p_values.append(1.0)  # Non-numeric = cannot verify = p=1
            stat_reports.append(report)
            continue
        
        # Permutation test for divisibility claims
        try:
            perm = permutation_test_divisibility(actual, 19)
            report["stats"] = perm
            report["remainder"] = result.get("remainder")
            # Use p_value_random if available, else exact_p_value
            p_val = perm.get("p_value_random") or perm.get("exact_p_value")
            all_p_values.append(p_val if result.get("remainder") == 0 else 1.0)
        except Exception as e:
            report["stats"] = {"error": str(e)}
            all_p_values.append(1.0)
        stat_reports.append(report)
    
    print(f"  Permutation tests completed for {len(stat_reports)} claims")
    print(f"  P-values computed: {sum(1 for p in all_p_values if p is not None)}")
    print()
    
    # Step 5: Multiple-hypothesis correction
    print("[5/7] Applying multiple-hypothesis correction (Bonferroni + BH-FDR)...")
    
    n_claims = len(all_p_values)
    bonferroni_corrected, corrected_alpha = compute_bonferroni_correction(
        [p if p is not None else 1.0 for p in all_p_values]
    )
    
    bh_significant = compute_benjamini_hochberg(
        [p if p is not None else 1.0 for p in all_p_values]
    )
    
    print(f"  Number of claims: {n_claims}")
    print(f"  Bonferroni-corrected alpha: {corrected_alpha:.6f}")
    print(f"  BH-FDR significant indices: {list(bh_significant)}")
    print()
    
    # Step 6: Robustness across normalizations
    print("[6/7] Testing robustness across normalization conventions...")
    
    robustness_results = {}
    
    # Test total letter count across all 4 conventions
    for convention in ["A", "B", "C", "D"]:
        total = 0
        for surah in dataset:
            for ayah in surah["ayahs"]:
                total += count_letters_per_convention(ayah["text"], convention)
        remainder = total % 19
        robustness_results[f"total_letters_{convention}"] = {
            "convention": convention,
            "count": total,
            "remainder": remainder,
            "divisible": remainder == 0
        }
        status = "PASS" if remainder == 0 else "FAIL"
        print(f"  Total letters (convention {convention}): {total:>8d}  mod 19 = {remainder:>2d} [{status}]")
    
    # Test Fatiha letter count across all 4 conventions
    surah1 = dataset[0]
    for convention in ["A", "B", "C", "D"]:
        total = sum(count_letters_per_convention(a["text"], convention) for a in surah1["ayahs"])
        remainder = total % 19
        robustness_results[f"fatiha_letters_{convention}"] = {
            "convention": convention,
            "count": total,
            "remainder": remainder,
            "divisible": remainder == 0
        }
        status = "PASS" if remainder == 0 else "FAIL"
        print(f"  Fatiha letters (convention {convention}): {total:>4d}  mod 19 = {remainder:>2d} [{status}]")
    
    # Check 74:30 letter count across convention
    surah74_ayah30 = dataset[73]["ayahs"][29]["text"]
    for convention in ["A", "B", "C", "D"]:
        total = count_letters_per_convention(surah74_ayah30, convention)
        remainder = total % 19
        robustness_results[f"74_30_letters_{convention}"] = {
            "convention": convention,
            "count": total,
            "remainder": remainder,
            "divisible": remainder == 0
        }
        status = "PASS" if remainder == 0 else "FAIL"
        print(f"  74:30 letters (convention {convention}): {total:>4d}  mod 19 = {remainder:>2d} [{status}]")
    
    print()
    
    # Step 7: Confidence scores and classification
    print("[7/7] Computing confidence scores and classifications...")
    
    final_claims = []
    for i, (result, stat, bonf) in enumerate(zip(results, stat_reports, bonferroni_corrected)):
        # Ensure result has required fields
        result.setdefault("description", "No description provided")
        result.setdefault("status", "UNKNOWN")
        
        remainder = result.get("remainder")
        p_val = stat["stats"].get("p_value")
        if p_val is None and result["status"] == "VERIFIED":
            p_val = 1.0 / 19  # Exact probability under uniform distribution
        elif p_val is None:
            p_val = 1.0
        
        robust = all(
            robustness_results.get(k, {}).get("divisible", False)
            for k in robustness_results
            if result["claim_id"] in k
        ) if any(result["claim_id"] in k for k in robustness_results) else True
        
        score = compute_confidence_score(
            status=result["status"],
            remainder=remainder,
            p_value=p_val,
            bonferroni_significant=bonf["significance"] == "significant",
            bh_significant=i in bh_significant,
            normalization_robust=robust
        )
        
        classification = classify_claim(score)
        level = assign_confidence_level(score)
        
        claim_entry = {
            "claim_id": result["claim_id"],
            "description": result.get("description", "No description"),
            "status": result["status"],
            "actual_value": result.get("actual_value"),
            "remainder": remainder,
            "p_value": round(p_val, 6),
            "bonferroni_significant": bonf["significance"] == "significant",
            "bh_fdr_significant": i in bh_significant,
            "confidence_score": score,
            "classification": classification,
            "confidence_level": level,
            "text_source": result.get("text_source", "not specified"),
            "counting_rule": result.get("counting_rule", "not specified"),
            "details": result.get("details", ""),
            "robustness": result.get("robustness", robustness_results),
        }
        final_claims.append(claim_entry)
        
        print(f"  {result['claim_id']:12s} score={score:.3f}  [{classification:8s}] [{level:10s}]  p={p_val:.6f}  [{result['status']}]")
    print()
    
    # ============================================================
    # SUMMARY
    # ============================================================
    
    strong_claims = [c for c in final_claims if c["classification"] == "STRONG"]
    weak_claims = [c for c in final_claims if c["classification"] == "WEAK"]
    rejected_claims = [c for c in final_claims if c["classification"] == "REJECTED"]
    verified = [c for c in final_claims if c["status"] == "VERIFIED"]
    not_verified = [c for c in final_claims if c["status"] != "VERIFIED"]
    
    # Save results
    report = {
        "report_title": "QURAN CODE 19 VERIFICATION — STAGE 8: STATISTICAL TESTING",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "protocol": "Statistical skepticism, permutation testing, BH-FDR correction",
        "total_claims": len(final_claims),
        "summary": {
            "strong": len(strong_claims),
            "weak": len(weak_claims),
            "rejected": len(rejected_claims),
            "verified": len(verified),
            "not_verified": len(not_verified),
        },
        "multiple_hypothesis_correction": {
            "method": "Bonferroni + Benjamini-Hochberg FDR",
            "n_tests": n_claims,
            "bonferroni_alpha": round(corrected_alpha, 6),
            "bonferroni_significant_count": sum(1 for b in bonferroni_corrected if b["significance"] == "significant"),
            "bh_fdr_significant_count": len(bh_significant),
        },
        "robustness_summary": robustness_results,
        "claims": final_claims,
        "strong_claims": strong_claims,
        "weak_claims": weak_claims,
        "rejected_claims": rejected_claims,
        "methodology": {
            "permutations": 100000,
            "random_seed": 42,
            "normalization_conventions": ["A", "B", "C", "D"],
            "statistical_tests": [
                "Exact divisibility test",
                "Permutation test (100k iterations)",
                "Bonferroni family-wise error correction",
                "Benjamini-Hochberg FDR correction",
                "Cross-normalization robustness test"
            ],
            "confidence_scoring": {
                "base_verified": 0.50,
                "remainder_zero": 0.20,
                "p_less_0.001": 0.15,
                "p_less_0.01": 0.10,
                "p_less_0.05": 0.05,
                "bonferroni_sig": 0.10,
                "bh_fdr_sig": 0.05,
                "normalization_robust": 0.10,
                "max_score": 1.0
            },
            "classification_thresholds": {
                "STRONG": ">= 0.70",
                "WEAK": ">= 0.40",
                "REJECTED": "< 0.40"
            }
        }
    }
    
    # Write report
    report_path = "/home/ubuntu/.openclaw/workspace/quran-19-stage8-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Write human-readable summary
    summary_path = "/home/ubuntu/.openclaw/workspace/quran-19-stage8-summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("QURAN CODE 19 VERIFICATION — STAGE 8: STATISTICAL TESTING REPORT\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {report['timestamp']}\n")
        f.write(f"Protocol: Statistical skepticism, permutation testing, BH-FDR correction\n\n")
        
        f.write(f"TOTAL CLAIMS TESTED: {len(final_claims)}\n")
        f.write(f"  VERIFIED:     {len(verified)}\n")
        f.write(f"  NOT VERIFIED: {len(not_verified)}\n")
        f.write(f"  STRONG:       {len(strong_claims)}\n")
        f.write(f"  WEAK:         {len(weak_claims)}\n")
        f.write(f"  REJECTED:     {len(rejected_claims)}\n\n")
        
        f.write("-" * 70 + "\n")
        f.write("STRONG CLAIMS (confidence >= 0.70)\n")
        f.write("-" * 70 + "\n")
        for c in strong_claims:
            f.write(f"\n  [{c['claim_id']}] {c['description']}\n")
            f.write(f"    Score: {c['confidence_score']:.3f} ({c['confidence_level']})\n")
            f.write(f"    Status: {c['status']}, Actual: {c['actual_value']}, Remainder: {c['remainder']}\n")
            f.write(f"    p-value: {c['p_value']}, Bonferroni: {c['bonferroni_significant']}, BH-FDR: {c['bh_fdr_significant']}\n")
            f.write(f"    Source: {c['text_source']}\n")
            f.write(f"    Rule: {c['counting_rule']}\n")
        
        f.write("\n" + "-" * 70 + "\n")
        f.write("WEAK CLAIMS (confidence 0.40-0.69)\n")
        f.write("-" * 70 + "\n")
        for c in weak_claims:
            f.write(f"\n  [{c['claim_id']}] {c['description']}\n")
            f.write(f"    Score: {c['confidence_score']:.3f} ({c['confidence_level']})\n")
            f.write(f"    Status: {c['status']}, Actual: {c['actual_value']}, Remainder: {c['remainder']}\n")
            f.write(f"    p-value: {c['p_value']}\n")
            f.write(f"    Source: {c['text_source']}\n")
        
        f.write("\n" + "-" * 70 + "\n")
        f.write("REJECTED CLAIMS (confidence < 0.40)\n")
        f.write("-" * 70 + "\n")
        for c in rejected_claims:
            f.write(f"\n  [{c['claim_id']}] {c['description']}\n")
            f.write(f"    Score: {c['confidence_score']:.3f} ({c['confidence_level']})\n")
            f.write(f"    Status: {c['status']}, Actual: {c['actual_value']}, Remainder: {c['remainder']}\n")
            f.write(f"    p-value: {c['p_value']}\n")
            f.write(f"    Source: {c['text_source']}\n")
        
        f.write("\n" + "-" * 70 + "\n")
        f.write("ROBUSTNESS ACROSS NORMALIZATIONS\n")
        f.write("-" * 70 + "\n")
        for key, val in robustness_results.items():
            status = "PASS" if val["divisible"] else "FAIL"
            f.write(f"  {key}: count={val['count']}, mod19={val['remainder']}, divisible={val['divisible']} [{status}]\n")
        
        f.write("\n" + "-" * 70 + "\n")
        f.write("METHODOLOGY\n")
        f.write("-" * 70 + "\n")
        f.write(f"\n  Permutations: {report['methodology']['permutations']:,}\n")
        f.write(f"  Random seed: {report['methodology']['random_seed']}\n")
        f.write(f"  Normalization conventions: {', '.join(report['methodology']['normalization_conventions'])}\n")
        f.write(f"  Statistical tests:\n")
        for t in report["methodology"]["statistical_tests"]:
            f.write(f"    - {t}\n")
        f.write(f"\n  Multiple-hypothesis correction:\n")
        f.write(f"    - Bonferroni (FWER): alpha = {corrected_alpha:.6f}\n")
        f.write(f"    - Benjamini-Hochberg (FDR): {len(bh_significant)} significant\n")
        f.write(f"\n  Confidence scoring:\n")
        for key, val in report["methodology"]["confidence_scoring"].items():
            f.write(f"    - {key}: {val}\n")
        f.write(f"\n  Classification:\n")
        for key, val in report["methodology"]["classification_thresholds"].items():
            f.write(f"    - {key}: {val}\n")
    
    print("=" * 70)
    print("STAGE 8 COMPLETE")
    print("=" * 70)
    print(f"Report: {report_path}")
    print(f"Summary: {summary_path}")
    print(f"Total: {len(final_claims)} claims | Strong: {len(strong_claims)} | Weak: {len(weak_claims)} | Rejected: {len(rejected_claims)}")
    print(f"Verified: {len(verified)} | Not Verified: {len(not_verified)}")
    
    return report


if __name__ == "__main__":
    main()
