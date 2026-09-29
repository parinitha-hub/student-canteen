import json

log_file = r'C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'view_file' in line and 'app.js' in line:
            obj = json.loads(line)
            tcs = obj.get('tool_calls', [])
            for tc in tcs:
                args = tc.get('args', {})
                if 'app.js' in args.get('AbsolutePath', ''):
                    print(f"Step {i}: view_file start={args.get('StartLine')}, end={args.get('EndLine')}")
            # also check if this is a tool output
            if obj.get('type') == 'PLANNER_RESPONSE':
                pass
            content = obj.get('content', '')
            if 'Showing lines' in content and 'app.js' in content:
                print(f"Step {i}: output has content len={len(content)}")
