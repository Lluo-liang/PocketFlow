"""
学习讲解器的流程定义
"""
from pocketflow import Flow
from nodes import (
    AnalyzeConceptNode,
    GenerateExplanationNode,
    GenerateExamplesNode,
    GeneratePracticeNode,
    FormatOutputNode
)


def create_explainer_flow():
    """创建概念讲解流程"""

    # 创建所有节点
    analyze = AnalyzeConceptNode()
    explain = GenerateExplanationNode()
    examples = GenerateExamplesNode()
    practice = GeneratePracticeNode()
    format_output = FormatOutputNode()

    # 连接节点（线性工作流）
    analyze >> explain >> examples >> practice >> format_output

    # 创建并返回流程
    return Flow(start=analyze)
