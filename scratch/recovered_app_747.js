import json

log_file = r'C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'TargetFile' in line and 'app.js' in line:
            obj = json.loads(line)
            tcs = obj.get('tool_calls', [])
            for tc in tcs:
                name = tc.get('name')
                args = tc.get('args', {})
                tf = args.get('TargetFile', '')
                print(f"Line {i}: tool={name}, target={tf}")
                if 'write_to_file' in str(name):
                    code = args.get('CodeContent', '')
                    print(f"   write_to_file CodeContent len = {len(code)}")
                    with open(f"scratch/recovered_app_{i}.js", "w", encoding="utf-8") as out:
                        out.write(code)
                    print(f"   Saved to scratch/recovered_app_{i}.js")
