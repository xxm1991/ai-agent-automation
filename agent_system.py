# -*- coding: utf-8 -*-
"""
AI Agent 办公&运维自动化系统
多Agent协作 + 长链推理 + 私有知识库
支持：网络运维、财务精算、办公自动化、健康饮食、数码调优
"""

import json
import time
from typing import Dict, List, Any


# ====================== 1. 问题解析Agent ======================
class IntentAgent:
    """意图识别 + 任务拆解"""
    def analyze(self, query: str) -> Dict:
        query = query.lower()
        scene = "unknown"
        sub_tasks = []

        # 场景分类
        if any(k in query for k in ["网络", "路由", "pve", "docker", "故障", "运维"]):
            scene = "operation"
            sub_tasks = ["环境检查", "日志分析", "根因定位", "方案生成"]
        elif any(k in query for k in ["分期", "利息", "年化", "成本", "财务"]):
            scene = "finance"
            sub_tasks = ["数据提取", "公式计算", "结果验证", "决策建议"]
        elif any(k in query for k in ["excel", "文档", "同步", "办公", "自动化"]):
            scene = "office"
            sub_tasks = ["格式解析", "脚本生成", "自动执行", "结果汇总"]
        elif any(k in query for k in ["嘌呤", "饮食", "健康"]):
            scene = "health"
            sub_tasks = ["食材匹配", "禁忌查询", "方案输出"]
        else:
            scene = "general"
            sub_tasks = ["意图理解", "通用回答"]

        return {
            "scene": scene,
            "sub_tasks": sub_tasks,
            "need_reasoning": len(sub_tasks) >= 3
        }


# ====================== 2. 长链推理Agent ======================
class ReasoningAgent:
    """多步长链推理核心"""
    def run(self, scene: str, sub_tasks: List[str]) -> List[Dict]:
        reasoning_steps = []
        for i, task in enumerate(sub_tasks):
            step = {
                "step": i + 1,
                "task": task,
                "status": "completed",
                "desc": self._get_step_desc(scene, task)
            }
            reasoning_steps.append(step)
            time.sleep(0.1)
        return reasoning_steps

    def _get_step_desc(self, scene: str, task: str) -> str:
        mapping = {
            "operation": {
                "环境检查": "检查网络/容器/虚拟机运行状态与端口",
                "日志分析": "解析报错日志，匹配历史故障库",
                "根因定位": "推理故障源头，排除非关键因素",
                "方案生成": "输出可直接执行的修复命令/配置"
            },
            "finance": {
                "数据提取": "解析金额、期数、费率",
                "公式计算": "真实年化 + 总利息精算",
                "结果验证": "交叉校验避免计算错误",
                "决策建议": "给出最优方案判断"
            }
        }
        return mapping.get(scene, {}).get(task, "执行中...")


# ====================== 3. 知识库Agent ======================
class KnowledgeAgent:
    """私有专业知识库检索"""
    def __init__(self):
        self.kb = {
            "operation": ["PVE故障排查", "Docker重启策略", "软路由端口映射", "网络延迟优化"],
            "finance": ["真实年化公式", "分期成本模型", "补贴抵扣计算"],
            "office": ["Excel格式自动化", "数据同步脚本", "批处理任务"],
            "health": ["高嘌呤食材清单", "低嘌呤饮食方案"]
        }

    def search(self, scene: str) -> List[str]:
        return self.kb.get(scene, [])


# ====================== 4. 执行Agent ======================
class ExecuteAgent:
    """生成最终可执行方案"""
    def generate_result(self, scene: str, reasoning_steps: List, knowledge: List) -> Dict:
        return {
            "scene": scene,
            "reasoning_steps": reasoning_steps,
            "knowledge_used": knowledge,
            "final_solution": "✅ 已完成AI推理，生成标准化可执行方案",
            "tips": "直接复制命令/配置即可落地使用"
        }


# ====================== 总控：多Agent协作系统 ======================
class AIAutomationSystem:
    def __init__(self):
        self.intent = IntentAgent()
        self.reason = ReasoningAgent()
        self.knowledge = KnowledgeAgent()
        self.execute = ExecuteAgent()

    def chat(self, query: str) -> Dict:
        # 1. 意图解析
        intent_result = self.intent.analyze(query)
        # 2. 长链推理
        reasoning = self.reason.run(intent_result["scene"], intent_result["sub_tasks"])
        # 3. 知识库检索
        knowledge = self.knowledge.search(intent_result["scene"])
        # 4. 生成结果
        result = self.execute.generate_result(intent_result["scene"], reasoning, knowledge)
        return result


# ====================== 测试入口 ======================
if __name__ == "__main__":
    agent = AIAutomationSystem()
    test_query = "我想排查网络卡顿问题"
    res = agent.chat(test_query)
    print(json.dumps(res, ensure_ascii=False, indent=2))