"""
简化版 Amazon URL RAG 系统（不需要 ChromaDB）

使用 JSON 文件存储数据，使用简单的文本相似度匹配
适合快速测试和演示
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import difflib


class SimpleAmazonURLRAG:
    """简化版 Amazon URL RAG 系统（无需向量数据库）"""
    
    def __init__(self, db_path: str = "./rag_simple_db.json"):
        """
        初始化简化 RAG 系统
        
        Args:
            db_path: JSON 数据库文件路径
        """
        self.db_path = db_path
        self.data = []
        
        # 尝试加载现有数据
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"[OK] 已加载 {len(self.data)} 条数据")
        else:
            print("[NEW] 创建新的数据库")
        
        print(f"[DB] 数据库路径: {os.path.abspath(db_path)}")
    
    def add_url_entry(
        self,
        user_description: str,
        exact_url: str,
        page_description: str,
        aliases: List[str] = None,
        keywords: List[str] = None,
        marketplace: str = "ALL",
        category: str = "general"
    ) -> str:
        """添加新的 URL 条目"""
        entry_id = f"rag_{len(self.data) + 1:03d}"
        
        entry = {
            "id": entry_id,
            "user_description": user_description,
            "exact_url": exact_url,
            "page_description": page_description,
            "aliases": aliases or [],
            "keywords": keywords or [],
            "marketplace": marketplace,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        self.data.append(entry)
        self._save()
        
        print(f"[OK] 已添加: {user_description} -> {exact_url}")
        return entry_id
    
    def search_url(
        self,
        query: str,
        top_k: int = 3,
        marketplace: Optional[str] = None
    ) -> Dict:
        """检索相似的 URL（使用简单文本匹配）"""
        results = []
        
        for entry in self.data:
            # 过滤站点
            if marketplace and marketplace != "ALL" and entry['marketplace'] != marketplace:
                continue
            
            # 计算相似度（检查多个字段）
            similarity_scores = []
            
            # 1. 与用户描述的相似度
            desc_sim = difflib.SequenceMatcher(None, query.lower(), 
                                               entry['user_description'].lower()).ratio()
            similarity_scores.append(desc_sim)
            
            # 2. 与别名的相似度
            for alias in entry['aliases']:
                alias_sim = difflib.SequenceMatcher(None, query.lower(), 
                                                   alias.lower()).ratio()
                similarity_scores.append(alias_sim)
            
            # 3. 关键词匹配
            query_words = set(query.lower().split())
            keyword_matches = sum(1 for kw in entry['keywords'] 
                                if kw.lower() in query_words)
            if entry['keywords']:
                keyword_sim = keyword_matches / len(entry['keywords'])
                similarity_scores.append(keyword_sim)
            
            # 取最高相似度
            max_similarity = max(similarity_scores)
            
            results.append({
                "id": entry['id'],
                "user_description": entry['user_description'],
                "exact_url": entry['exact_url'],
                "page_description": entry['page_description'],
                "aliases": entry['aliases'],
                "marketplace": entry['marketplace'],
                "category": entry['category'],
                "similarity": round(max_similarity, 4),
                "distance": round(1 - max_similarity, 4)
            })
        
        # 排序并取 top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        results = results[:top_k]
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    def increment_usage(self, entry_id: str):
        """增加条目的使用次数"""
        for entry in self.data:
            if entry['id'] == entry_id:
                entry['usage_count'] = entry.get('usage_count', 0) + 1
                entry['last_used'] = datetime.now().isoformat()
                self._save()
                break
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        categories = {}
        marketplaces = {}
        total_usage = 0
        
        for entry in self.data:
            category = entry.get('category', 'general')
            marketplace = entry.get('marketplace', 'ALL')
            usage = int(entry.get('usage_count', 0))
            
            categories[category] = categories.get(category, 0) + 1
            marketplaces[marketplace] = marketplaces.get(marketplace, 0) + 1
            total_usage += usage
        
        return {
            "total_entries": len(self.data),
            "categories": categories,
            "marketplaces": marketplaces,
            "total_usage": total_usage,
            "avg_usage": round(total_usage / len(self.data), 2) if self.data else 0
        }
    
    def export_to_json(self, output_path: str = "./rag_backup.json"):
        """导出为 JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"[OK] 已导出到: {os.path.abspath(output_path)}")
        return output_path
    
    def _save(self):
        """保存到文件"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 简单测试
    print("=" * 60)
    print("简化版 Amazon URL RAG 系统")
    print("=" * 60)
    
    try:
        rag = SimpleAmazonURLRAG()
        stats = rag.get_statistics()
        print(f"\n[STATS] 统计信息: {json.dumps(stats, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
