import os

# 노트 파일이 저장된 폴더 경로를 지정합니다.
folder_path = '/path/to/your/obsidian/vault'

# 수정할 문자열
def fix_image_paths(content):
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        if line.startswith('![](/'):
            fixed_lines.append(line)
        elif line.startswith('![](assets/images/posts_img/'):
            fixed_lines.append(line.replace('![](assets/images/posts_img/', '![](/assets/images/posts_img/'))
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)

for root, _, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 경로 수정
            new_content = fix_image_paths(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

print("모든 파일에서 경로 수정이 완료되었습니다.")
