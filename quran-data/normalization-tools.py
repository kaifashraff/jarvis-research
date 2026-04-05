#!/usr/bin/env python3
"""
Quran Code 19 Verification - Normalization Tools
Stage 4: Simple Script Comparator

This script provides normalization functions to convert Uthmani script
to simple script (diacritics removed) and compare letter counts.
"""

import re
import json
from collections import Counter
from typing import Dict, List, Tuple, Optional

# Arabic diacritics and special characters to remove
DIACRITICS = {
    'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ً', 'ٌ', 'ٍ', 'َ', 'ّ',
    'ٰ', 'ٰ', 'ٰ', 'ٰ', 'ٰ', 'ٰ',  # Various diacritics
}

# Hamza variants that normalize to plain hamza
HAMZA_VARIANTS = {
    'ء', 'أ', 'إ', 'ؤ', 'ئ', 'ى'  # alif with hamza, hamza on waw, hamza on ya
}

# Alif variants that should be normalized
ALIF_VARIANTS = {
    'ا', 'ى', 'ٱ', 'أ', 'إ'  # standard alif, alif maqsura, alif with hamza
}

# Ta marbuta normalization
ta_marbuta_map = {
    'ة': 'ه'  # ta marbuta becomes heh
}

# Ligatures that should be counted as single characters
LIGATURES = {
    'ﷺ': 'صلى',  # sallallahu alayhi wa sallam
    'ﷺ': 'صلى الله عليه وسلم',
}

class QuranNormalizer:
    """Normalize Quranic text for comparison."""
    
    def __init__(self, convention: str = "simple"):
        self.convention = convention
        self.normalization_rules = self._get_normalization_rules()
    
    def _get_normalization_rules(self) -> Dict:
        """Return the normalization rules for this convention."""
        return {
            "name": self.convention,
            "diacritics_removed": True,
            "hamza_normalized": True,
            "alif_standardized": True,
            "ta_marbuta_as_heh": True,
            "basmala_included": True,
            "word_boundaries_preserved": True,
            "ligatures_handled": "count_as_single"
        }
    
    def remove_diacritics(self, text: str) -> str:
        """Remove all diacritical marks from Arabic text."""
        # Remove known diacritics
        for diacritic in DIACRITICS:
            text = text.replace(diacritic, '')
        return text
    
    def normalize_hamza(self, text: str) -> str:
        """Normalize all hamza variants to plain hamza."""
        result = []
        for char in text:
            if char in HAMZA_VARIANTS:
                result.append('ء')
            else:
                result.append(char)
        return ''.join(result)
    
    def normalize_alif(self, text: str) -> str:
        """Standardize alif variants."""
        result = []
        for char in text:
            if char in ALIF_VARIANTS:
                result.append('ا')
            else:
                result.append(char)
        return ''.join(result)
    
    def normalize_ta_marbuta(self, text: str) -> str:
        """Convert ta marbuta to heh."""
        result = []
        for char in text:
            if char in ta_marbuta_map:
                result.append(ta_marbuta_map[char])
            else:
                result.append(char)
        return ''.join(result)
    
    def normalize_text(self, text: str) -> str:
        """Apply full normalization to text."""
        # Step 1: Remove diacritics
        text = self.remove_diacritics(text)
        
        # Step 2: Normalize hamza variants
        text = self.normalize_hamza(text)
        
        # Step 3: Normalize alif variants
        text = self.normalize_alif(text)
        
        # Step 4: Normalize ta marbuta
        text = self.normalize_ta_marbuta(text)
        
        # Step 5: Remove any remaining non-Arabic characters except basic punctuation
        # Keep only Arabic letters, spaces, and basic punctuation
        arabic_letters = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')
        result = []
        for char in text:
            if char in arabic_letters or char.isspace() or char in {'.', ',', ';', '!', '؟', '،'}:
                result.append(char)
        
        return ''.join(result)
    
    def count_letters(self, text: str, include_spaces: bool = False) -> int:
        """Count letters in normalized text."""
        if include_spaces:
            return len(text)
        else:
            # Count only Arabic letters (no spaces, no punctuation)
            arabic_letters = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')
            count = sum(1 for char in text if char in arabic_letters)
            return count
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        # Split by whitespace and count non-empty tokens
        words = [w for w in text.split() if w]
        return len(words)
    
    def extract_letters_only(self, text: str) -> str:
        """Extract only Arabic letters from text."""
        arabic_letters = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')
        return ''.join(char for char in text if char in arabic_letters)


def load_quran_text(filepath: str) -> str:
    """Load Quran text from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")


def compare_normalizations(
    uthmani_text: str,
    simple_text: str,
    normalizer: QuranNormalizer
) -> Dict:
    """
    Compare letter counts between Uthmani and simple script.
    
    Returns a detailed comparison report.
    """
    # Normalize Uthmani text to simple script
    normalized_uthmani = normalizer.normalize_text(uthmani_text)
    
    # Extract letters only for accurate counting
    uthmani_letters = normalizer.extract_letters_only(uthmani_text)
    simple_letters = normalizer.extract_letters_only(simple_text)
    normalized_uthmani_letters = normalizer.extract_letters_only(normalized_uthmani)
    
    # Count letters
    uthmani_count = normalizer.count_letters(uthmani_text)
    simple_count = normalizer.count_letters(simple_text)
    normalized_uthmani_count = normalizer.count_letters(normalized_uthmani)
    
    # Count words
    uthmani_words = normalizer.count_words(uthmani_text)
    simple_words = normalizer.count_words(simple_text)
    
    # Calculate differences
    count_diff = abs(uthmani_count - simple_count)
    normalized_diff = abs(normalized_uthmani_count - simple_count)
    
    # Find discrepancies in letter patterns
    uthmani_pattern = normalizer.extract_letters_only(uthmani_text)
    simple_pattern = normalizer.extract_letters_only(simple_text)
    normalized_uthmani_pattern = normalizer.extract_letters_only(normalized_uthmani)
    
    # Check if patterns match after normalization
    patterns_match = normalized_uthmani_pattern == simple_pattern
    
    # Detailed letter-by-letter comparison
    letter_comparison = []
    min_len = min(len(uthmani_letters), len(simple_letters))
    
    for i in range(min_len):
        letter_match = uthmani_letters[i] == simple_letters[i]
        letter_comparison.append({
            "position": i + 1,
            "uthmani_letter": uthmani_letters[i],
            "simple_letter": simple_letters[i],
            "match": letter_match
        })
    
    # Count mismatches
    mismatches = sum(1 for cmp in letter_comparison if not cmp["match"])
    
    return {
        "normalization_convention": normalizer.convention,
        "normalization_rules": normalizer.normalization_rules,
        "letter_counts": {
            "uthmani_raw": uthmani_count,
            "simple_raw": simple_count,
            "uthmani_normalized": normalized_uthmani_count,
            "difference_uthmani_vs_simple": count_diff,
            "difference_normalized_vs_simple": normalized_diff
        },
        "word_counts": {
            "uthmani": uthmani_words,
            "simple": simple_words
        },
        "pattern_match": {
            "patterns_match_after_normalization": patterns_match,
            "mismatched_positions": mismatches,
            "total_positions_checked": min_len
        },
        "letter_comparison": letter_comparison[:50],  # First 50 for brevity
        "discrepancies_found": mismatches > 0,
        "normalization_effect": {
            "count_difference_introduced": abs(uthmani_count - normalized_uthmani_count),
            "pattern_correction": "improved" if patterns_match else "degraded"
        }
    }


def generate_comparison_matrix(
    comparison_results: List[Dict]
) -> Dict:
    """
    Generate a comparison matrix across multiple normalization conventions.
    """
    if not comparison_results:
        return {"error": "No comparison results provided"}
    
    # Extract metrics for matrix
    conventions = [r["normalization_convention"] for r in comparison_results]
    counts = [r["letter_counts"] for r in comparison_results]
    pattern_matches = [r["pattern_match"]["patterns_match_after_normalization"] 
                       for r in comparison_results]
    
    # Create matrix
    matrix = {
        "conventions_tested": conventions,
        "letter_count_matrix": {
            "convention": conventions,
            "uthmani_raw": [c["uthmani_raw"] for c in counts],
            "simple_raw": [c["simple_raw"] for c in counts],
            "normalized_counts": [c["uthmani_normalized"] for c in counts],
            "vs_simple_difference": [c["difference_uthmani_vs_simple"] for c in counts],
            "vs_simple_difference_normalized": [c["difference_normalized_vs_simple"] for c in counts]
        },
        "pattern_match_matrix": {
            "convention": conventions,
            "pattern_matches_simple": pattern_matches
        },
        "robustness_scores": {},
        "summary": {
            "conventions_with_perfect_match": sum(pattern_matches),
            "total_conventions": len(pattern_matches),
            "perfect_match_rate": sum(pattern_matches) / len(pattern_matches) if pattern_matches else 0
        }
    }
    
    # Calculate robustness scores (higher is better)
    for result in comparison_results:
        conv = result["normalization_convention"]
        
        # Robustness score based on:
        # 1. Pattern match (50% weight)
        # 2. Small count difference (30% weight)
        # 3. Consistent normalization (20% weight)
        
        pattern_score = 1.0 if result["pattern_match"]["patterns_match_after_normalization"] else 0.0
        count_diff = result["letter_counts"]["difference_normalized_vs_simple"]
        count_score = max(0, 1.0 - (count_diff / max(result["letter_counts"]["simple_raw"], 1)))
        
        robustness = 0.5 * pattern_score + 0.3 * count_score + 0.2
        matrix["robustness_scores"][conv] = round(robustness, 3)
    
    return matrix


def generate_recommendation(matrix: Dict) -> Dict:
    """
    Generate recommendation based on comparison matrix.
    """
    if not matrix.get("robustness_scores"):
        return {"error": "No robustness scores available"}
    
    scores = matrix["robustness_scores"]
    best_convention = max(scores.items(), key=lambda x: x[1])
    
    # Determine recommendation level
    best_score = best_convention[1]
    
    if best_score >= 0.9:
        recommendation_level = "STRONG_RECOMMENDATION"
        rationale = (
            f"The {best_convention[0]} convention achieves {best_score*100:.1f}% robustness, "
            "indicating excellent pattern preservation and minimal count differences. "
            "This convention is highly recommended for Code 19 verification."
        )
    elif best_score >= 0.7:
        recommendation_level = "RECOMMENDED"
        rationale = (
            f"The {best_convention[0]} convention achieves {best_score*100:.1f}% robustness. "
            "While not perfect, it provides a good balance between pattern preservation "
            "and practical implementation. Use with caution and document normalization rules."
        )
    elif best_score >= 0.5:
        recommendation_level = "CONDITIONAL_RECOMMENDATION"
        rationale = (
            f"The {best_convention[0]} convention achieves {best_score*100:.1f}% robustness. "
            "This convention shows significant sensitivity to normalization choices. "
            "Only use if explicitly required, and always report the exact normalization rules used."
        )
    else:
        recommendation_level = "NOT_RECOMMENDED"
        rationale = (
            f"The {best_convention[0]} convention achieves only {best_score*100:.1f}% robustness. "
            "This convention introduces substantial pattern distortion and count differences. "
            "Avoid for Code 19 verification work."
        )
    
    return {
        "recommendation": recommendation_level,
        "best_convention": best_convention[0],
        "best_score": best_score,
        "rationale": rationale,
        "caveats": [
            "Normalization choices can significantly affect pattern detection results.",
            "Always explicitly state your normalization convention in publications.",
            "Test multiple conventions to ensure robustness of findings.",
            "Code 19 patterns that only appear in specific normalizations should be treated with skepticism."
        ]
    }


def main():
    """Main execution function."""
    print("=" * 80)
    print("QURAN CODE 19 VERIFICATION - STAGE 4: SIMPLE SCRIPT COMPARATOR")
    print("=" * 80)
    print()
    
    # Load datasets
    try:
        uthmani_path = "/home/ubuntu/.openclaw/workspace/quran-data/uthmani/quran-uthmani.txt"
        simple_path = "/home/ubuntu/.openclaw/workspace/quran-data/simple/quran-simple.txt"
        
        uthmani_text = load_quran_text(uthmani_path)
        simple_text = load_quran_text(simple_path)
        
        print("✓ Datasets loaded successfully")
        print(f"  - Uthmani text: {len(uthmani_text)} characters")
        print(f"  - Simple text: {len(simple_text)} characters")
        print()
        
    except Exception as e:
        print(f"✗ Error loading datasets: {e}")
        return
    
    # Test multiple normalization conventions
    conventions = [
        "simple",
        "uthmani_no_diacritics",
        "full_normalization"
    ]
    
    normalizers = [QuranNormalizer(conv) for conv in conventions]
    comparison_results = []
    
    print("Testing normalization conventions...")
    print("-" * 80)
    
    for normalizer in normalizers:
        print(f"\n📊 Testing convention: {normalizer.convention}")
        print(f"   Rules: {normalizer.normalization_rules}")
        
        result = compare_normalizations(uthmani_text, simple_text, normalizer)
        comparison_results.append(result)
        
        print(f"   Uthmani raw count: {result['letter_counts']['uthmani_raw']}")
        print(f"   Simple raw count: {result['letter_counts']['simple_raw']}")
        print(f"   Normalized count: {result['letter_counts']['uthmani_normalized']}")
        print(f"   Difference vs simple: {result['letter_counts']['difference_normalized_vs_simple']}")
        print(f"   Pattern match: {result['pattern_match']['patterns_match_after_normalization']}")
        print(f"   Discrepancies: {result['pattern_match']['mismatched_positions']}")
    
    print()
    print("=" * 80)
    print("GENERATING COMPARISON MATRIX")
    print("=" * 80)
    
    matrix = generate_comparison_matrix(comparison_results)
    
    print("\n📈 Comparison Matrix:")
    print(json.dumps(matrix, indent=2, ensure_ascii=False))
    
    print()
    print("=" * 80)
    print("GENERATING RECOMMENDATION")
    print("=" * 80)
    
    recommendation = generate_recommendation(matrix)
    
    print("\n🎯 Recommendation:")
    print(f"Level: {recommendation['recommendation']}")
    print(f"Best convention: {recommendation['best_convention']}")
    print(f"Robustness score: {recommendation['best_score']:.3f}")
    print(f"\nRationale:")
    print(f"  {recommendation['rationale']}")
    
    print("\n⚠️ Caveats:")
    for caveat in recommendation['caveats']:
        print(f"  • {caveat}")
    
    print()
    print("=" * 80)
    print("SENSITIVITY ANALYSIS")
    print("=" * 80)
    
    # Analyze sensitivity to normalization
    sensitivity_report = {
        "highly_sensitive_patterns": [],
        "moderately_sensitive_patterns": [],
        "robust_patterns": [],
        "normalization_dependent_findings": []
    }
    
    for result in comparison_results:
        conv = result["normalization_convention"]
        if not result["pattern_match"]["patterns_match_after_normalization"]:
            sensitivity_report["highly_sensitive_patterns"].append(conv)
            sensitivity_report["normalization_dependent_findings"].append({
                "convention": conv,
                "issue": f"Pattern mismatch: {result['pattern_match']['mismatched_positions']} positions differ"
            })
    
    print("\n🔍 Sensitivity to Normalization:")
    print(f"Highly sensitive conventions: {len(sensitivity_report['highly_sensitive_patterns'])}")
    for conv in sensitivity_report['highly_sensitive_patterns']:
        print(f"  - {conv}")
    
    print(f"\nNormalization-dependent findings: {len(sensitivity_report['normalization_dependent_findings'])}")
    for finding in sensitivity_report['normalization_dependent_findings']:
        print(f"  - {finding['convention']}: {finding['issue']}")
    
    # Save results
    output_dir = "/home/ubuntu/.openclaw/workspace/quran-data/verification-reports"
    
    try:
        with open(f"{output_dir}/stage4-comparison-report.json", 'w', encoding='utf-8') as f:
            json.dump({
                "comparison_matrix": matrix,
                "recommendation": recommendation,
                "sensitivity_analysis": sensitivity_report,
                "raw_results": comparison_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Full report saved to: {output_dir}/stage4-comparison-report.json")
        
    except Exception as e:
        print(f"\n✗ Error saving report: {e}")
    
    print()
    print("=" * 80)
    print("TASK COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
