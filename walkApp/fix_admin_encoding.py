with open('users/api_views_admin.py', 'rb') as f:
    raw = f.read()
content = raw.decode('utf-8')
if 'Ã' in content:
    fixed = content.encode('latin-1').decode('utf-8')
    with open('users/api_views_admin.py', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print('Fix aplicado')
else:
    print('Ya está limpio')
