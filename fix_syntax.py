import re

for path in [r'C:\Users\pc\Desktop\gemini-mobile-ai\index.html', r'C:\Users\pc\Desktop\Gemini-Interface.html']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the broken multiline string
    broken_str = "const sysInstruction = (state.activeGem ? state.activeGem.instructions + '\n' : '')"
    fixed_str = 'const sysInstruction = (state.activeGem ? state.activeGem.instructions + "\\n" : "")'
    if broken_str in content:
        content = content.replace(broken_str, fixed_str)
        print('Fixed broken_str in', path)

    # Also make sure there are no other unescaped multiline single-quote strings
    content = content.replace("state.activeGem.instructions + '\n'", 'state.activeGem.instructions + "\\n"')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Syntax fix applied.')
