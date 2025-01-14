import re

def extract_rarities_from_text(text):
    # Dictionary to store the type and rarity values
    rarities = {}

    # Regular expression pattern to find 'type == id' and 'this.rare = number'
    type_pattern = re.compile(r'if \(type == (\d+)\)\s*\{')
    rare_pattern = re.compile(r'\s*this\.rare\s*=\s*(-?\d+)')

    # Find all occurrences of 'if (type == ...) {' and 'this.rare = ...'
    matches = type_pattern.finditer(text)
    
    # Iterate over all matches for 'if (type == ...)' blocks
    for match in matches:
        item_type = int(match.group(1))
        
        # Find the rarity in the corresponding block
        block_start = match.start()
        block_end = text.find('return;', block_start)
        block = text[block_start:block_end]

        # Look for the rarity value in the block
        rare_match = rare_pattern.search(block)
        if rare_match:
            rarity = int(rare_match.group(1))
        else:
            rarity = 1  # Default to 1 if rarity is not found

        # Store the type and rarity in the dictionary
        rarities[str(item_type)] = rarity

    return rarities


# Example usage:
with open("input.txt","r") as f:
    large_text = f.read()

rarities = extract_rarities_from_text(large_text)

import json
# Print the extracted rarities
with open("output.json","w") as f:
    f.write(json.dumps(rarities))
