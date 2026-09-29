import json

log_file = r'C:\Users\srina\.gemini\antigravity-ide\brain\20e971cb-0d00-4045-8d1c-25a9a4f41ad9\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'app.js' in line:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                args = tc.get('args', {})
                tf = args.get('TargetFile', '')
                if tf.endswith('js\\app.js') or tf.endswith('js/app.js'):
                    print(f"Step {i}: tool={tc.get('name')}, desc={args.get('Description', '')}")
