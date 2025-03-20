import sys, re, subprocess, os
from openai import OpenAI

def detect_windows_shell():
    """检测当前所在的Windows Shell类型"""
    try:
        import psutil
        # 通过遍历父进程判断shell类型
        current_process = psutil.Process()
        for parent in current_process.parents():
            name = parent.name().lower()
            if 'powershell' in name:
                return 'PowerShell'
            elif 'cmd' in name:
                return 'cmd'
            elif 'bash' in name:  # 兼容WSL
                return 'WSL'
        return 'unknown'
    except (psutil.NoSuchProcess, ImportError):
        # 回退方案：通过环境变量判断
        if 'PROMPT' in os.environ:  # CMD特有变量
            return 'cmd'
        elif 'PSModulePath' in os.environ:
            return 'PowerShell'
        return 'unknown'

def get_os_type():
    """检测操作系统类型并返回标准化标识"""
    os_name = sys.platform
    if os_name.startswith('win'):
        return 'windows'
    elif os_name == 'darwin':
        return 'macos'
    elif os_name.startswith('linux'):
        return 'linux'
    return 'unknown'

def extract_command(response_text):
    """尝试提取bash代码块中的命令"""
    match = re.search(r'```bash\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 如果没有代码块，尝试直接提取整个内容
    return response_text.strip()

def copy_to_clipboard(command):
    """跨平台剪贴板操作"""
    os_type = get_os_type()
    
    try:
        if os_type == 'windows':
            subprocess.run(
                'clip',
                shell=True,
                input=command.encode('utf-8'),
                check=True
            )
        elif os_type == 'macos':
            subprocess.run(
                ['pbcopy'],
                input=command.encode('utf-8'),
                check=True
            )
        elif os_type == 'linux':
            subprocess.run(
                ['xclip', '-selection', 'clipboard'],
                input=command.encode('utf-8'),
                check=True
            )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {os.path.basename(sys.executable)} {sys.argv[0]} key=API_KEY [query]")
        sys.exit(1)

    os_type = get_os_type()
    if os_type == 'unknown':
        print("无法识别的操作系统")
        sys.exit(1)

    # 解析参数
    api_key = sys.argv[1].split('=')[1]
    query = ' '.join(sys.argv[2:])

    # 配置OpenAI
    client = OpenAI(api_key = api_key)

    if os_type == 'windows':
        shell_type = detect_windows_shell()
        if shell_type == 'unknown':
            os_name = 'Windows'
        else:
            os_name = f"Windows ({shell_type})"
    elif os_type == 'macos':
        os_name = 'macOS'
    else:
        os_name = 'Linux'

    # 构造prompt
    prompt = f"""Generate a {os_name} command to fulfill the following requirement:
{query}

Requirements:
1. Output only the command itself
2. Wrap it in a ```bash code block
3. No explanations or additional comments"""

    try:
        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print(f"API请求失败: {str(e)}")
        sys.exit(1)

    # 提取命令
    response_text = response.choices[0].message.content
    command = extract_command(response_text)

    if not command:
        print("无法从响应中提取有效命令")
        print("原始响应内容：")
        print(response_text)
        sys.exit(1)

    # 尝试复制到剪贴板
    if copy_to_clipboard(command):
        if os_type == 'windows':
            print(f"命令已复制到剪贴板，按 Ctrl+V 执行：\n{command}")
        else:
            print(f"命令已复制到剪贴板，按 Ctrl+Shift+V 执行：\n{command}")
    else:
        print("剪贴板工具未找到，请手动复制以下命令：")
        print(command)

        if os_type == 'windows':
            print("提示：Windows原生支持clip命令，请检查系统是否正常")
        else:
            print("提示：可能需要安装xclip（Linux）或使用pbcopy（macOS）")

if __name__ == "__main__":
    main()