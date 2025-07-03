import pandas as pd

# Path to your original CSV
csv_file = 'mappings/Makemodern.csv'
df = pd.read_csv(csv_file)

# Helper to clean up names
def clean_name(name):
    return ''.join(c for c in name.upper() if c.isalnum())

# Helper to get 2-3 letter substrings
def get_substrings(clean):
    substrings = set()
    n = len(clean)
    for i in range(n - 1):
        substrings.add(clean[i:i+2])
    for i in range(n - 2):
        substrings.add(clean[i:i+3])
    return sorted(substrings, key=lambda x: (len(x), x))

# Generate all possible abbreviation candidates
def generate_candidates(name):
    clean = clean_name(name)
    candidates = []
    if len(clean) >= 2:
        candidates.append(clean[0] + clean[-1])
        candidates.append(clean[:2])
    if len(clean) >= 3:
        candidates.append(clean[:3])
    # Add all internal 2-3 letter substrings
    candidates.extend(get_substrings(clean))
    # Deduplicate
    seen = set()
    result = []
    for c in candidates:
        if 2 <= len(c) <= 3 and c not in seen:
            seen.add(c)
            result.append(c)
    return result

# Assign unique codes
used_codes = set()
final_codes = []
collision_counts = {}

for name, existing_code in zip(df['name'], df['code']):
    candidates = generate_candidates(name)
    assigned = None
    for cand in candidates:
        if cand not in used_codes:
            assigned = cand
            break
    if not assigned:
        # All candidates taken, fallback to numbered version
        base = candidates[0] if candidates else 'XX'
        counter = collision_counts.get(base, 1)
        assigned = (base + str(counter))[:3]
        while assigned in used_codes:
            counter += 1
            assigned = (base + str(counter))[:3]
        collision_counts[base] = counter + 1
    used_codes.add(assigned)
    final_codes.append(assigned)

# Save new CSV
df['code'] = final_codes
df.to_csv('mappings/Makemodern_deduped.csv', index=False)
print(" Done! Saved unique codes to mappings/Makemodern_deduped.csv")
