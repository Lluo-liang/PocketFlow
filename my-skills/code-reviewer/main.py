#!/usr/bin/env python3
"""
代码学习审查器 - 主程序

帮助你理解代码的工作原理、设计思路和改进方向

使用方法：
    python main.py path/to/file.py
    python main.py --stdin  # 从标准输入读取
"""
import sys
import os
from pathlib import Path

# 添加 learning-explainer 的 utils 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "learning-explainer"))
from utils.call_llm import call_llm


def analyze_code(code: str, filename: str = "code") -> str:
    """分析代码并生成学习报告"""

    prompt = f"""
你是一位资深的代码导师，请对以下代码进行详细的学习导向型分析。

文件：{filename}

代码：
```
{code}
```

请以 Markdown 格式输出，包含以下部分：

# 📝 代码学习报告：{filename}

## 🎯 代码功能概述
[用 2-3 句话说明这段代码做什么]

## 🔍 关键概念解析
[列出代码中用到的重要概念，如设计模式、算法、语言特性等，每个概念 1-2 句话解释]

## 📐 代码结构分析
[分析代码的组织结构、模块划分、函数职责等]

## ✨ 亮点与学习价值
[指出代码中值得学习的地方，如优雅的实现、最佳实践等]

## 💡 工作原理详解
[逐步解释代码的核心逻辑是如何工作的]

## 🎓 相关知识点
[列出学习这段代码需要掌握的前置知识]

## 🔧 可能的改进方向
[从学习角度，指出可以尝试改进的地方（不是批评，而是学习机会）]

## 📚 延伸学习建议
[推荐相关的学习资源、类似的代码案例等]

---
要求：
- 语气友好，像老师一样讲解
- 重点帮助理解"为什么这样写"
- 对于复杂部分，提供类比说明
- 指出初学者可能困惑的地方
"""

    return call_llm(prompt)


def main():
    print("="*60)
    print("🔍 代码学习审查器")
    print("="*60)

    # 获取代码
    code = ""
    filename = "unknown"

    if len(sys.argv) > 1:
        if sys.argv[1] == "--stdin":
            # 从标准输入读取
            print("\n请粘贴代码（按 Ctrl+D 结束）：\n")
            code = sys.stdin.read()
            filename = "stdin"
        else:
            # 从文件读取
            filepath = sys.argv[1]
            if not os.path.exists(filepath):
                print(f"❌ 文件不存在：{filepath}")
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            filename = os.path.basename(filepath)
    else:
        # 交互模式
        print("\n请输入代码文件路径：")
        filepath = input("> ").strip()

        if not os.path.exists(filepath):
            print(f"❌ 文件不存在：{filepath}")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        filename = os.path.basename(filepath)

    if not code.strip():
        print("❌ 代码为空，退出。")
        return

    print(f"\n🔍 正在分析：{filename} ({len(code)} 字符)")
    print("-"*60)

    try:
        report = analyze_code(code, filename)

        print("\n" + "="*60)
        print(report)
        print("="*60)

        # 询问是否保存
        save = input("\n\n💾 是否保存报告？(y/n): ").strip().lower()
        if save == 'y':
            report_filename = f"{filename}_学习报告.md"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 已保存到：{report_filename}")

    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
