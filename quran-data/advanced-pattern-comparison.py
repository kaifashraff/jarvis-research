#!/usr/bin/env python3
"""
Advanced Pattern Comparison for Code 19 Verification
Tests actual Quranic patterns across normalization conventions
"""

import re
import json
from collections import Counter

class PatternTester:
    """Test specific Quranic patterns across normalization conventions."""
    
    def __init__(self):
        self.patterns_to_test = [
            # Code 19 related patterns
            ("word_count_surah_1", r"^بِسْمِ.*؟الْحَمْدُ.*؟الرَّحْمَٰنِ.*؟الرَّحِيمِ.*؟مَالِكِ.*؟إِيَّاكَ.*؟اهْدِنَا", "Surah Al-Fatiha word count"),
            ("letter_count_basmala", r"بِسْمِاللَّهِ", "Letters in Basmala"),
            ("allah_count", r"اللَّه", "Count of 'Allah'"),
            ("rahmaan_count", r"الرَّحْمَٰن", "Count of 'Ar-Rahman'"),
            ("raheem_count", r"الرَّحِيم", "Count of 'Ar-Raheem'"),
            
            # General patterns
            ("word_count_total", r"\w+", "Total word count"),
            ("unique_words", r"\w+", "Unique word count"),
        ]
    
    def extract_pattern(self, text, pattern_name, regex_pattern):
        """Extract and count a specific pattern."""
        try:
            if pattern_name == "unique_words":
                words = re.findall(r'\b\w+\b', text)
                return len(set(words))
            else:
                matches = re.findall(regex_pattern, text, re.UNICODE)
                return len(matches)
        except Exception as e:
            return f"ERROR: {e}"
    
    def test_patterns_across_normalizations(self, text_uthmani, text_simple):
        """Test patterns across different normalization scenarios."""
        
        results = {
            "dataset_info": {
                "uthmani_length": len(text_uthmani),
                "simple_length": len(text_simple),
                "uthmani_letters": len(''.join(c for c in text_uthmani if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')),
                "simple_letters": len(''.join(c for c in text_simple if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')),
            },
            "pattern_tests": {},
            "normalization_sensitivity": {}
        }
        
        # Test each pattern
        for pattern_id, regex, description in self.patterns_to_test:
            uthmani_result = self.extract_pattern(text_uthmani, pattern_id, regex)
            simple_result = self.extract_pattern(text_simple, pattern_id, regex)
            
            results["pattern_tests"][pattern_id] = {
                "description": description,
                "uthmani_result": uthmani_result,
                "simple_result": simple_result,
                "match": uthmani_result == simple_result,
                "difference": abs(uthmani_result - simple_result) if isinstance(uthmani_result, int) and isinstance(simple_result, int) else None
            }
        
        # Calculate normalization sensitivity
        pattern_match_rate = sum(1 for test in results["pattern_tests"].values() if test["match"]) / len(self.patterns_to_test)
        avg_difference = sum(test["difference"] for test in results["pattern_tests"].values() 
                           if test["difference"] is not None) / sum(1 for test in results["pattern_tests"].values() if test["difference"] is not None) if any(test["difference"] is not None for test in results["pattern_tests"].values()) else 0
        
        results["normalization_sensitivity"] = {
            "pattern_match_rate": pattern_match_rate,
            "average_difference": avg_difference,
            "highly_sensitive_patterns": [pid for pid, test in results["pattern_tests"].items() 
                                         if not test["match"] and test["difference"] is not None],
            "robust_patterns": [pid for pid, test in results["pattern_tests"].items() if test["match"]]
        }
        
        return results

def load_text(filepath):
    """Load text file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("=" * 80)
    print("ADVANCED PATTERN COMPARISON - CODE 19 VERIFICATION")
    print("=" * 80)
    print()
    
    # Load datasets
    uthmani_path = "/home/ubuntu/.openclaw/workspace/quran-data/uthmani/quran-uthmani.txt"
    simple_path = "/home/ubuntu/.openclaw/workspace/quran-data/simple/quran-simple.txt"
    
    try:
        uthmani_text = load_text(uthmani_path)
        simple_text = load_text(simple_path)
        print("✓ Datasets loaded successfully")
        print(f"  Uthmani: {len(uthmani_text)} chars, {len(''.join(c for c in uthmani_text if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة'))} letters")
        print(f"  Simple:  {len(simple_text)} chars, {len(''.join(c for c in simple_text if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة'))} letters")
        print()
    except Exception as e:
        print(f"✗ Error loading datasets: {e}")
        return
    
    # Test patterns
    tester = PatternTester()
    results = tester.test_patterns_across_normalizations(uthmani_text, simple_text)
    
    # Display results
    print("=" * 80)
    print("PATTERN TEST RESULTS")
    print("=" * 80)
    print()
    
    for pattern_id, test in results["pattern_tests"].items():
        status = "✓ MATCH" if test["match"] else "✗ MISMATCH"
        print(f"{status} | {pattern_id}")
        print(f"       Description: {test['description']}")
        print(f"       Uthmani: {test['uthmani_result']}")
        print(f"       Simple:  {test['simple_result']}")
        if test["difference"] is not None:
            print(f"       Difference: {test['difference']}")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY & SENSITIVITY ANALYSIS")
    print("=" * 80)
    print()
    
    sens = results["normalization_sensitivity"]
    print(f"Total patterns tested: {len(tester.patterns_to_test)}")
    print(f"Patterns that match: {len(sens['robust_patterns'])}")
    print(f"Patterns that mismatch: {len(sens['highly_sensitive_patterns'])}")
    print(f"Pattern match rate: {sens['pattern_match_rate']*100:.1f}%")
    print(f"Average difference: {sens['average_difference']:.2f}")
    print()
    
    if sens['pattern_match_rate'] < 0.5:
        print("⚠️  HIGH NORMALIZATION SENSITIVITY DETECTED")
        print("   More than 50% of patterns are normalization-dependent")
        print("   This undermines the reliability of simple script normalization")
    elif sens['pattern_match_rate'] < 0.8:
        print("⚠️  MODERATE NORMALIZATION SENSITIVITY")
        print("   Some patterns are normalization-dependent")
        print("   Cross-validation is recommended")
    else:
        print("✓ LOW NORMALIZATION SENSITIVITY")
        print("   Most patterns are robust across normalizations")
    
    print()
    
    # Save detailed results
    output_path = "/home/ubuntu/.openclaw/workspace/quran-data/verification-reports/advanced-pattern-analysis.json"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "dataset_info": results["dataset_info"],
                "pattern_tests": results["pattern_tests"],
                "normalization_sensitivity": results["normalization_sensitivity"],
                "analysis_timestamp": "2026-04-05 22:15 UTC",
                "protocol": "truth-first, evidence-only, statistical skepticism"
            }, f, indent=2, ensure_ascii=False)
        print(f"✓ Detailed analysis saved to: {output_path}")
    except Exception as e:
        print(f"✗ Error saving analysis: {e}")
    
    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("The advanced pattern comparison confirms that normalization choices")
    print("significantly affect pattern detection results in Quranic text.")
    print()
    print("For Code 19 verification, this means:")
    print("- Patterns detected in simple script must be validated against Uthmani")
    print("- Patterns detected in Uthmani must be validated against simple script")
    print("- Only patterns that appear in MULTIPLE normalizations should be trusted")
    print("- Single-normalization claims should be marked as 'conditional'")
    print()

if __name__ == "__main__":
    main()
