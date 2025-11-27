"""
LLM 调用工具
根据你的 LLM 提供商修改这个文件
"""
import os

def call_llm(prompt: str, system_prompt: str = None) -> str:
    """
    调用 LLM 生成响应

    参数：
        prompt: 用户提示
        system_prompt: 系统提示（可选）

    返回：
        LLM 的响应文本
    """
    # TODO: 根据你使用的 LLM 修改这部分代码

    # 示例 1: OpenAI
    # from openai import OpenAI
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # messages = []
    # if system_prompt:
    #     messages.append({"role": "system", "content": system_prompt})
    # messages.append({"role": "user", "content": prompt})
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=messages
    # )
    # return response.choices[0].message.content

    # 示例 2: Anthropic Claude
    # from anthropic import Anthropic
    # client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # response = client.messages.create(
    #     model="claude-sonnet-4-0",
    #     max_tokens=2000,
    #     system=system_prompt or "",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.content[0].text

    # 示例 3: Google Gemini
    # from google import genai
    # client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    # full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
    # response = client.models.generate_content(
    #     model='gemini-2.0-flash-exp',
    #     contents=full_prompt
    # )
    # return response.text

    # 占位符实现（用于测试）
    print(f"⚠️  请配置 LLM 调用！")
    print(f"System: {system_prompt}")
    print(f"Prompt: {prompt}")
    return f"[占位符响应] 你需要在 utils/call_llm.py 中配置你的 LLM"


if __name__ == "__main__":
    # 测试 LLM 调用
    test_prompt = "解释什么是递归"
    print("测试 LLM 调用...")
    response = call_llm(test_prompt)
    print(f"\n响应:\n{response}")
