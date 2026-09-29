import json

log_file = r'C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'TargetFile' in line and 'app.js' in line:
            obj = json.loads(line)
            print(f"Line {i}: type={obj.get('type')}, status={obj.get('status')}")
            for tc in obj.get('tool_calls', []):
                print("  tool_call:", tc)
