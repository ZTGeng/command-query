# Command Query

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI驱动的跨平台命令行生成工具，支持：
- Windows (CMD/PowerShell)
- Linux
- macOS

## 安装依赖
- Linux / macOS
```bash
pip install openai
```
- Windows
```bash
pip install openai psutil
```

## 使用
**方式一：直接通过命令调用**
```bash
python /path_to_repo/command-query.py key=OPENAI_API_KEY [query]
```
其中 OPENAI_API_KEY 替换为你的 API 密钥，[query] 为你希望生成命令的描述。例如：
```bash
python /path_to_repo/command-query.py key=sk-xxx 列出当前目录下所有以.py结尾的文件
```
脚本会调用 OpenAI 接口生成一个符合要求的命令，并将该命令复制到剪贴板，终端会显示提示信息。

**方式二：设置别名（Alias）**

为脚本设置别名，只需要输入别名和查询内容即可调用脚本。
- Linux / macOS

编辑 shell 配置文件（例如 ~/.bashrc 或 ~/.zshrc），添加如下行：
```bash
alias q='python /path_to_repo/command-query.py key=OPENAI_API_KEY'
```
- Windows

**CMD**：可以使用 doskey 命令设置临时别名，只在当前 CMD 会话中有效。
```cmd
doskey q=python C:\path_to_repo\command-query.py key=OPENAI_API_KEY $*
```
**PowerShell**：可以定义一个函数来作为别名。在 PowerShell 配置文件（通常是 `profile.ps1`，路径可通过运行 `$PROFILE` 命令查看，若文件不存在请手动创建对应目录和文件）中添加：
```powershell
function q {
    python C:\path_to_repo\command-query.py key=OPENAI_API_KEY @args
}
```
设置别名后即可使用：
```bash
q 显示当前磁盘使用情况
```
## 示例
假设你在 Linux 下想生成一个显示当前用户所有进程的命令，你可以这样调用：
```bash
python /path_to_repo/command-query.py key=OPENAI_API_KEY 列出当前用户的所有进程
```
或如果你已设置别名：
```bash
q 列出当前用户的所有进程
```
按照终端提示信息，将生成的命令粘贴到命令行内执行。