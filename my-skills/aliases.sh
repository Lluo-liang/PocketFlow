#!/bin/bash
# PocketFlow 技能快捷别名
#
# 使用方法：
#   source my-skills/aliases.sh
#
# 或添加到 ~/.bashrc 或 ~/.zshrc：
#   echo "source /Users/80892291/WorkSpace/IDEA/pocketflow/PocketFlow/my-skills/aliases.sh" >> ~/.zshrc

SKILLS_BASE="/Users/80892291/WorkSpace/IDEA/pocketflow/PocketFlow/my-skills"

# 概念讲解器
alias explain="cd $SKILLS_BASE/learning-explainer && python main.py"
alias 讲解="cd $SKILLS_BASE/learning-explainer && python main.py"

# 代码审查器
alias review="cd $SKILLS_BASE/code-reviewer && python main.py"
alias 审查="cd $SKILLS_BASE/code-reviewer && python main.py"

# 练习生成器
alias practice="cd $SKILLS_BASE/practice-generator && python main.py"
alias 练习="cd $SKILLS_BASE/practice-generator && python main.py"

# 快捷跳转
alias cdskills="cd $SKILLS_BASE"

echo "✅ PocketFlow 技能别名已加载！"
echo ""
echo "可用命令："
echo "  explain <概念>      - 讲解概念"
echo "  review <文件>       - 审查代码"
echo "  practice <主题>     - 生成练习"
echo "  cdskills           - 跳转到技能目录"
echo ""
echo "示例："
echo "  explain 'Python装饰器'"
echo "  review mycode.py"
echo "  practice '二叉树遍历' -d hard"
echo ""
