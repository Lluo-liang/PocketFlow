#!/usr/bin/env python3
"""
概念深度讲解器 - 主程序

使用方法：
    python main.py                    # 交互模式
    python main.py "Python装饰器"    # 命令行模式
"""
import sys
from flow import create_explainer_flow


def main():
    print("="*60)
    print("🎓 概念深度讲解器")
    print("="*60)

    # 获取要讲解的概念
    if len(sys.argv) > 1:
        # 命令行参数模式
        concept = " ".join(sys.argv[1:])
    else:
        # 交互模式
        print("\n请输入你想深入理解的概念：")
        print("示例：Python装饰器、二叉树、闭包、REST API、依赖注入等")
        concept = input("\n> ").strip()

    if not concept:
        print("❌ 未输入概念，退出。")
        return

    print(f"\n🔍 正在深入讲解：{concept}")
    print("-"*60)

    # 初始化共享存储
    shared = {
        "concept": concept,
        "analysis": {},
        "explanation": {},
        "examples": {},
        "practice": {},
        "final_output": ""
    }

    # 创建并运行流程
    try:
        flow = create_explainer_flow()
        flow.run(shared)

        # 询问是否保存
        save = input("\n\n💾 是否保存到文件？(y/n): ").strip().lower()
        if save == 'y':
            filename = f"{concept.replace(' ', '_')}_讲解.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(shared["final_output"])
            print(f"✅ 已保存到：{filename}")

    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
