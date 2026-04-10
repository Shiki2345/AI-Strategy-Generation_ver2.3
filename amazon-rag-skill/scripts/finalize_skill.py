"""
Skill 炼制完成脚本

功能：
1. 更新 RAG 使用统计
2. 验证 Skill 可用性
3. 生成 Skill 总结报告
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from rag_system_simple import SimpleAmazonURLRAG
import json
from datetime import datetime


def update_rag_usage(rag_db_path: str, entry_id: str):
    """更新 RAG 条目的使用统计"""
    print(f"\n{'='*60}")
    print("[STEP 1] Update RAG Usage Statistics")
    print(f"{'='*60}")
    
    rag = SimpleAmazonURLRAG(rag_db_path)
    rag.increment_usage(entry_id)
    
    print(f"[OK] Updated usage count for entry {entry_id}")
    return True


def validate_skill(skill_path: str):
    """验证 Skill 文件的完整性"""
    print(f"\n{'='*60}")
    print("[STEP 2] Validate Skill File")
    print(f"{'='*60}")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill = json.load(f)
    
    required_fields = [
        "skill_metadata",
        "applicable_scenarios",
        "dialogue_flow",
        "best_practices"
    ]
    
    missing_fields = [field for field in required_fields if field not in skill]
    
    if missing_fields:
        print(f"[ERROR] Skill missing required fields: {missing_fields}")
        return False
    
    print(f"[OK] Skill structure is valid")
    print(f"   - Skill ID: {skill['skill_metadata']['skill_id']}")
    print(f"   - Skill 名称: {skill['skill_metadata']['skill_name']}")
    print(f"   - 版本: {skill['skill_metadata']['version']}")
    print(f"   - 适用场景数: {len(skill['applicable_scenarios'])}")
    print(f"   - 对话阶段数: {len(skill['dialogue_flow'])}")
    print(f"   - 最佳实践数: {len(skill['best_practices'])}")
    
    return True


def validate_policy(policy_path: str):
    """验证策略配置文件"""
    print(f"\n{'='*60}")
    print("[STEP 3] Validate Policy Config")
    print(f"{'='*60}")
    
    with open(policy_path, 'r', encoding='utf-8') as f:
        policy = json.load(f)
    
    print(f"[OK] Policy config is valid")
    print(f"   - 策略 ID: {policy['policy_id']}")
    print(f"   - 策略名称: {policy['policy_name']}")
    print(f"   - 策略类型: {policy['policy_type']}")
    print(f"   - 目标页面: {policy['target_resources']['page_name']}")
    print(f"   - 目标 URL: {policy['target_resources']['exact_url']}")
    print(f"   - 敏感度: {policy['target_resources']['sensitivity_level']}")
    print(f"   - 审批人: {policy['access_control']['approval_workflow']['approval_chain'][0]['approver_role']}")
    
    return True


def generate_skill_summary(
    skill_path: str,
    policy_path: str,
    output_path: str
):
    """生成 Skill 总结报告"""
    print(f"\n{'='*60}")
    print("[STEP 4] Generate Skill Summary Report")
    print(f"{'='*60}")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill = json.load(f)
    
    with open(policy_path, 'r', encoding='utf-8') as f:
        policy = json.load(f)
    
    summary = {
        "skill_finalization": {
            "completed_at": datetime.now().isoformat(),
            "status": "success",
            "skill_id": skill['skill_metadata']['skill_id'],
            "skill_name": skill['skill_metadata']['skill_name'],
            "version": skill['skill_metadata']['version']
        },
        "dialogue_session": {
            "user_request": "不允许运营专员访问美国亚马逊的账户详情页",
            "rag_query": "美国亚马逊账户详情页",
            "rag_result": {
                "entry_id": "rag_001",
                "similarity": 1.0,
                "exact_url": "https://sellercentral.amazon.com/sw/AccountInfo/"
            },
            "dialogue_rounds": 6,
            "key_decisions": [
                {
                    "question": "访问控制类型",
                    "answer": "实时审批制"
                },
                {
                    "question": "审批人",
                    "answer": "BOSS"
                },
                {
                    "question": "临时权限有效期",
                    "answer": "由 BOSS 定义"
                },
                {
                    "question": "申请理由",
                    "answer": "可选填写"
                },
                {
                    "question": "生效时间",
                    "answer": "全天生效（7x24）"
                }
            ]
        },
        "generated_artifacts": {
            "policy_config": {
                "file": policy_path,
                "policy_id": policy['policy_id'],
                "policy_type": policy['policy_type'],
                "target_page": policy['target_resources']['page_name'],
                "target_url": policy['target_resources']['exact_url']
            },
            "skill_definition": {
                "file": skill_path,
                "skill_id": skill['skill_metadata']['skill_id'],
                "applicable_scenarios": len(skill['applicable_scenarios']),
                "dialogue_phases": len(skill['dialogue_flow']),
                "best_practices": len(skill['best_practices']),
                "example_use_cases": len(skill['example_use_cases'])
            }
        },
        "skill_features": {
            "rag_integration": "✅ 已集成 RAG 检索",
            "multi_round_dialogue": "✅ 支持多轮对话",
            "decision_tree": "✅ 包含决策树逻辑",
            "auto_generation": "✅ 自动生成配置",
            "best_practices": "✅ 包含最佳实践",
            "reusable_patterns": "✅ 可复用模式"
        },
        "reusability": {
            "similar_scenarios": [
                "非财务人员访问支付报告需审批",
                "普通员工访问用户权限管理需审批",
                "实习生访问定价管理需审批",
                "运营助理访问品牌注册需审批"
            ],
            "adaptation_required": "修改目标页面、限制对象、审批人等参数",
            "complexity": "低 - 只需修改参数，无需修改流程"
        },
        "next_steps": [
            "将策略配置导入访问控制系统",
            "测试运营专员访问触发拦截",
            "测试审批流程是否正常",
            "验证临时权限自动过期",
            "收集用户反馈并优化",
            "使用 Skill 配置其他敏感页面"
        ],
        "knowledge_extraction": {
            "new_user_patterns": [
                "不允许...访问...",
                "需要审批",
                "特殊情况可申请临时权限"
            ],
            "decision_rules": [
                "当用户说'需要审批'时 → 判断为审批制访问控制",
                "当用户说'全天生效'时 → 设置 7x24 时间范围",
                "当用户说'由 BOSS 定义'时 → 设置 duration_controlled_by: approver"
            ],
            "best_practice_learned": [
                "审批超时设置 30 分钟平衡及时性和用户体验",
                "申请理由可选降低门槛同时保留信息",
                "多渠道通知确保审批人及时响应",
                "访问期间显示倒计时提醒用户"
            ]
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Summary report generated: {os.path.abspath(output_path)}")
    
    # 打印总结
    print(f"\n{'='*60}")
    print("SKILL FINALIZATION SUMMARY")
    print(f"{'='*60}")
    print(f"\n📌 Skill 信息:")
    print(f"   - ID: {summary['skill_finalization']['skill_id']}")
    print(f"   - 名称: {summary['skill_finalization']['skill_name']}")
    print(f"   - 版本: {summary['skill_finalization']['version']}")
    print(f"   - 完成时间: {summary['skill_finalization']['completed_at']}")
    
    print(f"\n📌 对话会话:")
    print(f"   - 用户请求: {summary['dialogue_session']['user_request']}")
    print(f"   - RAG 检索: {summary['dialogue_session']['rag_query']}")
    print(f"   - 匹配相似度: {summary['dialogue_session']['rag_result']['similarity'] * 100}%")
    print(f"   - 对话轮次: {summary['dialogue_session']['dialogue_rounds']}")
    
    print(f"\n📌 生成的产物:")
    print(f"   - 策略配置: {summary['generated_artifacts']['policy_config']['file']}")
    print(f"   - Skill 定义: {summary['generated_artifacts']['skill_definition']['file']}")
    print(f"   - 总结报告: {output_path}")
    
    print(f"\n📌 Skill 可复用于:")
    for scenario in summary['reusability']['similar_scenarios'][:3]:
        print(f"   - {scenario}")
    
    print(f"\n[SUCCESS] Skill finalized successfully!")
    
    return summary


def main():
    """主函数"""
    print("="*60)
    print("Skill Finalization Process")
    print("="*60)
    
    # 配置路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rag_db_path = os.path.join(base_dir, "rag_simple_db.json")
    skill_path = os.path.join(base_dir, "skills", "approval_based_access_control_skill.json")
    policy_path = os.path.join(base_dir, "generated_policies", "运营专员账户详情页审批策略.json")
    summary_path = os.path.join(base_dir, "skill_finalization_report.json")
    
    try:
        # 1. 更新 RAG 使用统计
        update_rag_usage(rag_db_path, "rag_001")
        
        # 2. 验证 Skill
        if not validate_skill(skill_path):
            print("❌ Skill 验证失败")
            return
        
        # 3. 验证策略配置
        if not validate_policy(policy_path):
            print("❌ 策略配置验证失败")
            return
        
        # 4. 生成总结报告
        summary = generate_skill_summary(skill_path, policy_path, summary_path)
        
        print(f"\n{'='*60}")
        print("[SUCCESS] All skill finalization steps completed!")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
