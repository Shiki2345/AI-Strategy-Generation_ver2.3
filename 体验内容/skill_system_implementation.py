"""
访问策略配置系统 - Skill 沉淀实现
演示如何将对话结果沉淀为可复用的 Skill
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class Skill:
    """Skill 数据模型"""
    skill_id: str
    skill_name: str
    skill_type: str  # specific_website 或 global_website
    trigger_keywords: List[str]
    conversation_template: Dict
    quick_fill_config: Dict
    learned_rules: List[Dict]
    usage_count: int = 0
    success_rate: float = 1.0
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


class SkillRepository:
    """Skill 仓库 - 负责存储和检索 Skills"""
    
    def __init__(self, storage_path: str = "skills_database.json"):
        self.storage_path = storage_path
        self.skills: Dict[str, Skill] = {}
        self.load_skills()
    
    def load_skills(self):
        """从文件加载 Skills"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for skill_data in data.get('skills', []):
                    skill = Skill(**skill_data)
                    self.skills[skill.skill_id] = skill
            print(f"✓ 已加载 {len(self.skills)} 个 Skills")
        except FileNotFoundError:
            print("✓ 创建新的 Skills 数据库")
            self.skills = {}
    
    def save_skills(self):
        """保存 Skills 到文件"""
        data = {
            'version': '1.0',
            'updated_at': datetime.now().isoformat(),
            'skills': [asdict(skill) for skill in self.skills.values()]
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存 {len(self.skills)} 个 Skills")
    
    def add_skill(self, skill: Skill):
        """添加新 Skill"""
        self.skills[skill.skill_id] = skill
        self.save_skills()
        print(f"✓ 已添加 Skill: {skill.skill_name}")
    
    def search_skills(self, user_input: str, threshold: float = 0.6) -> List[tuple]:
        """
        搜索匹配的 Skills
        返回: [(skill, similarity_score), ...]
        """
        results = []
        user_keywords = set(user_input.lower().split())
        
        for skill in self.skills.values():
            # 计算关键词匹配度
            skill_keywords = set([kw.lower() for kw in skill.trigger_keywords])
            intersection = user_keywords.intersection(skill_keywords)
            
            if skill_keywords:
                similarity = len(intersection) / len(skill_keywords)
                if similarity >= threshold:
                    results.append((skill, similarity))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def update_usage(self, skill_id: str, success: bool = True):
        """更新 Skill 使用统计"""
        if skill_id in self.skills:
            skill = self.skills[skill_id]
            skill.usage_count += 1
            # 更新成功率（简单的滑动平均）
            skill.success_rate = (skill.success_rate * 0.9 + (1.0 if success else 0.0) * 0.1)
            skill.updated_at = datetime.now().isoformat()
            self.save_skills()


class SkillLearner:
    """Skill 学习器 - 从对话中提取和沉淀 Skills"""
    
    def __init__(self, repository: SkillRepository):
        self.repository = repository
    
    def extract_skill_from_conversation(
        self, 
        conversation_history: List[Dict],
        final_config: Dict
    ) -> Skill:
        """
        从对话历史中提取 Skill
        
        Args:
            conversation_history: 对话历史列表
            final_config: 最终生成的配置 JSON
        
        Returns:
            Skill 对象
        """
        # 提取关键词
        keywords = self._extract_keywords(conversation_history)
        
        # 生成 Skill ID
        skill_id = self._generate_skill_id(keywords, final_config['strategy_type'])
        
        # 构建对话模板
        conversation_template = self._build_conversation_template(conversation_history)
        
        # 提取学习到的规则
        learned_rules = self._extract_learned_rules(conversation_history, final_config)
        
        # 生成快速填充配置
        quick_fill_config = self._extract_quick_fill_config(final_config)
        
        # 生成 Skill 名称
        skill_name = self._generate_skill_name(final_config)
        
        skill = Skill(
            skill_id=skill_id,
            skill_name=skill_name,
            skill_type=final_config['strategy_type'],
            trigger_keywords=keywords,
            conversation_template=conversation_template,
            quick_fill_config=quick_fill_config,
            learned_rules=learned_rules,
            usage_count=1
        )
        
        return skill
    
    def _extract_keywords(self, conversation_history: List[Dict]) -> List[str]:
        """从对话中提取关键词"""
        keywords = []
        
        # 定义关键词类别
        category_keywords = {
            'social_media': ['社交媒体', '社交网站', '微博', '抖音', '小红书'],
            'video': ['视频', '视频网站', 'YouTube', 'B站', '哔哩哔哩'],
            'shopping': ['购物', '淘宝', '京东', '拼多多'],
            'time': ['工作时间', '上班时间', '办公时间', '工作日'],
            'action': ['禁止', '限制', '不允许', '阻止']
        }
        
        # 从对话中提取
        full_text = ' '.join([turn.get('content', '') for turn in c