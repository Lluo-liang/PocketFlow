#!/bin/bash
# PocketFlow 技能快速设置脚本

echo "🚀 PocketFlow 个人技能设置"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python"
    exit 1
fi

echo "✓ 找到 Python: $(python3 --version)"

# 返回项目根目录
cd "$(dirname "$0")/.."

# 安装 PocketFlow
echo ""
echo "📦 安装 PocketFlow 框架..."
pip install -e . || { echo "❌ 安装失败"; exit 1; }
echo "✓ PocketFlow 安装完成"

# 安装技能依赖
echo ""
echo "📦 安装技能依赖..."
cd my-skills/learning-explainer
pip install -r requirements.txt || { echo "❌ 依赖安装失败"; exit 1; }
echo "✓ 依赖安装完成"

# 检查 LLM 配置
echo ""
echo "🔑 检查 LLM API Key..."

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "✓ 找到 OPENAI_API_KEY"
    LLM_FOUND=true
elif [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo "✓ 找到 ANTHROPIC_API_KEY"
    LLM_FOUND=true
elif [ ! -z "$GEMINI_API_KEY" ]; then
    echo "✓ 找到 GEMINI_API_KEY"
    LLM_FOUND=true
else
    echo "⚠️  未找到 LLM API Key"
    echo ""
    echo "请设置以下环境变量之一："
    echo "  export OPENAI_API_KEY='your-key'       # OpenAI"
    echo "  export ANTHROPIC_API_KEY='your-key'    # Claude"
    echo "  export GEMINI_API_KEY='your-key'       # Gemini"
    echo ""
    echo "然后编辑 my-skills/learning-explainer/utils/call_llm.py"
    echo "取消注释对应的 LLM 代码"
    LLM_FOUND=false
fi

# 测试安装
echo ""
echo "🧪 测试技能..."
cd ../../

if [ "$LLM_FOUND" = true ]; then
    echo "运行测试: learning-explainer"
    cd my-skills/learning-explainer
    echo "测试" | python main.py 2>&1 | head -5
    echo "✓ 技能可以运行（请配置 LLM 以获得实际结果）"
else
    echo "⚠️  跳过测试（需要先配置 LLM）"
fi

# 完成
echo ""
echo "================================"
echo "✅ 设置完成！"
echo ""
echo "下一步："
echo "1. 配置 LLM API Key（如果还没有）"
echo "2. 编辑 my-skills/learning-explainer/utils/call_llm.py"
echo "3. 运行: cd my-skills/learning-explainer && python main.py '你的概念'"
echo ""
echo "查看快速开始指南："
echo "  cat my-skills/快速开始指南.md"
echo ""
