import json
import re

log_file = r'C:\Users\srina\OneDrive\Desktop\food order using AI\scratch\..\..\..\..\..\..\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'

lines_dict = {}

with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Showing lines' in line and 'app.js' in line:
            obj = json.loads(line)
            content = obj.get('content', '')
            # Example format:
            # Showing lines 2940 to 3050
            # <line_number>: <original_line>
            m = re.search(r'Showing lines (\d+) to (\d+)', content)
            if m:
                start_l = int(m.group(1))
                end_l = int(m.group(2))
                # extract lines
                for cl in content.splitlines():
                    lm = re.match(r'^(\d+):\s(.*)$', cl)
                    if lm:
                        lnum = int(lm.group(1))
                        ltext = lm.group(2)
                        lines_dict[lnum] = ltext

print(f"Total lines captured from view_file: {len(lines_dict)}")
if lines_dict:
    print(f"Min line: {min(lines_dict.keys())}, Max line: {max(lines_dict.keys())}")
    # find missing ranges
    all_keys = sorted(lines_dict.keys())
    missing = []
    for num in range(1, max(all_keys) + 1):
        if num not in lines_dict:
            missing.append(num)
    print(f"Missing count: {len(missing)} out of {max(all_keys)}")
