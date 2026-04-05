#!/usr/bin/env python3
"""Debug script to understand the normalization differences."""

# Load texts
with open('/home/ubuntu/.openclaw/workspace/quran-data/uthmani/quran-uthmani.txt', 'r', encoding='utf-8') as f:
    uthmani_text = f.read()

with open('/home/ubuntu/.openclaw/workspace/quran-data/simple/quran-simple.txt', 'r', encoding='utf-8') as f:
    simple_text = f.read()

print("Original texts:")
print(f"Uthmani length: {len(uthmani_text)}")
print(f"Simple length: {len(simple_text)}")
print()

# Extract letters only
uthmani_letters = ''.join(c for c in uthmani_text if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')
simple_letters = ''.join(c for c in simple_text if c in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءة')

print(f"Uthmani letters only: {len(uthmani_letters)}")
print(f"Simple letters only: {len(simple_letters)}")
print()

# Show first 100 letters of each
print("First 100 Uthmani letters:")
print(uthmani_letters[:100])
print()

print("First 100 Simple letters:")
print(simple_letters[:100])
print()

# Check if they match
if uthmani_letters == simple_letters:
    print("✓ Letters match perfectly!")
else:
    print("✗ Letters don't match")
    print(f"Difference: {len(simple_letters) - len(uthmani_letters)}")
    
    # Find first mismatch
    for i, (u, s) in enumerate(zip(uthmani_letters, simple_letters)):
        if u != s:
            print(f"First mismatch at position {i}:")
            print(f"  Uthmani: {u} (U+{ord(u):04X})")
            print(f"  Simple:  {s} (U+{ord(s):04X})")
            # Show context
            start = max(0, i-10)
            end = min(len(uthmani_letters), i+10)
            print(f"\nContext around position {i}:")
            print(f"Uthmani: ...{uthmani_letters[start:end]}...")
            print(f"Simple:  ...{simple_letters[start:end]}...")
            break
