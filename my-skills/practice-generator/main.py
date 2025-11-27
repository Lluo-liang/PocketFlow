#!/usr/bin/env python3
"""
编程练习生成器

根据你想学习的知识点，生成渐进式练习题

使用方法：
    python main.py "Python列表推导式"
    python main.py "二叉树遍历" --difficulty hard
    python main.py "SQL查询" --count 5
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "learning-explainer"))
from utils.call_llm import call_llm


def generate_practice(topic: str, difficulty: str = "medium", count: int = 3) -> str:
    """生成练习题"""

    difficulty_desc = {
        "easy": "初级（适合刚接触的学习者）",
        "medium": "中级（适合有基础的学习者）",
        "hard": "高级（适合深入掌握的学习者）"
    }

    prompt = f"""
你是一位经验丰富的编程导师，请为学习"{topic}"生成 {count} 道{difficulty_desc[difficulty]}练习题。

要求：
1. 题目难度递增，从简单到复杂
2. 每道题包含：
   - 题目描述（清晰具体）
   - 输入输出示例
   - 提示（帮助思考的方向）
   - 参考答案（带详细注释）
   - 知识点总结（这道题考察什么）

请以 Markdown 格式输出：

# 📝 {topic} - 练习题集

难度：{difficulty_desc[difficulty]}
生成时间：[当前时间]

---

## 练习 1：[题目名称]

### 📋 题目描述
[清晰描述要解决的问题]

### 📥 输入输出示例
```
输入：...
输出：...
```

### 💡 提示
1. 提示1
2. 提示2
3. 提示3

### ✅ 参考答案
```python
# 详细的代码，带注释
```

### 🎓 知识点总结
[这道题考察了什么知识点，为什么这样写]

---

## 练习 2：...
[重复上述结构]

---

## 练习 3：...
[重复上述结构]

---

## 🎯 学习建议

1. **循序渐进**：按顺序完成练习
2. **独立思考**：先尝试自己解决，再看答案
3. **举一反三**：思考如何改变题目条件
4. **总结归纳**：完成后总结学到的东西

## 📚 延伸练习

[建议3-5个可以自己尝试的变体题目]

---
*祝你学习愉快！* 🎓
"""

    return call_llm(prompt)


def main():
    parser = argparse.ArgumentParser(description='编程练习生成器')
    parser.add_argument('topic', help='想练习的主题，如：Python装饰器、二叉树遍历')
    parser.add_argument('--difficulty', '-d',
                       choices=['easy', 'medium', 'hard'],
                       default='medium',
                       help='难度级别：easy/medium/hard')
    parser.add_argument('--count', '-c',
                       type=int,
                       default=3,
                       help='生成题目数量（默认3道）')

    args = parser.parse_args()

    print("="*60)
    print("📝 编程练习生成器")
    print("="*60)

    print(f"\n🎯 主题：{args.topic}")
    print(f"📊 难度：{args.difficulty}")
    print(f"🔢 数量：{args.count} 道题")
    print("-"*60)

    try:
        print("\n⏳ 正在生成练习题，请稍候...")
        exercises = generate_practice(args.topic, args.difficulty, args.count)

        print("\n" + "="*60)
        print(exercises)
        print("="*60)

        # 询问是否保存
        save = input("\n\n💾 是否保存练习题？(y/n): ").strip().lower()
        if save == 'y':
            filename = f"{args.topic.replace(' ', '_')}_{args.difficulty}_练习.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exercises)
            print(f"✅ 已保存到：{filename}")
            print(f"\n💡 建议：找个编辑器打开文件，边看边练！")

    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
