import json

log_file = r'C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'js/app.js' in line or 'js\\\\app.js' in line:
            obj = json.loads(line)
            # check type
            t = obj.get('type')
            content = obj.get('content', '')
            if 'Total Lines: 5109' in content:
                print(f"Line {i}: found content with Total Lines: 5109, len={len(content)}")
