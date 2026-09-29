import json

log_file = r'C:\Users\srina\OneDrive\Desktop\food order using AI\scratch\..\..\..\..\..\..\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'TargetFile' in line and 'app.js' in line:
            obj = json.loads(line)
            tcs = obj.get('tool_calls', [])
            for tc in tcs:
                name = tc.get('name')
                args = tc.get('args', {})
                tf = args.get('TargetFile', '')
                if tf.endswith('app.js'):
                    print(f"Line {i}: {name} TargetFile={tf}")
                    if name == 'replace_file_content':
                        print("  TargetContent:", repr(args.get('TargetContent', '')[:100]))
                        print("  ReplacementContent:", repr(args.get('ReplacementContent', '')[:100]))
