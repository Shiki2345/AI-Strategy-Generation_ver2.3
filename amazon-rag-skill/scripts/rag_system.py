"""
Amazon URL RAG 系统核心模块

功能：
1. 初始化向量数据库
2. 添加 URL 条目
3. 检索相似 URL
4. 学习新映射
5. 持久化和备份
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from openai import OpenAI


class AmazonURLRAG:
    """Amazon URL RAG 系统"""
    
    def __init__(self, db_path: str = "./rag_db", api_key: Optional[str] = None):
        """
        初始化 RAG 系统
        
        Args:
            db_path: 数据库路径
            api_key: OpenAI API Key（如果为None，会从环境变量读取）
        """
        self.db_path = db_path
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数")
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=self.api_key)
        
        # 初始化 ChromaDB
        self._init_chromadb()
        
        print(f"✅ RAG 系统初始化成功")
        print(f"📂 数据库路径: {os.path.abspath(db_path)}")
        print(f"📊 当前条目数: {self.collection.count()}")
    
    def _init_chromadb(self):
        """初始化 ChromaDB 客户端和集合"""
        self.chroma_client = chromadb.PersistentClient(path=self.db_path)
        
        # 创建或获取集合
        try:
            self.collection = self.chroma_client.get_collection(name="amazon_urls")
            print("📚 已加载现有 RAG 数据库")
        except:
            self.collection = self.chroma_client.create_collection(
                name="amazon_urls",
                metadata={"description": "Amazon页面URL映射知识库"}
            )
            print("🆕 已创建新的 RAG 数据库")
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        获取文本的向量表示
        
        Args:
            text: 输入文本
            
        Returns:
            向量列表
        """
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    
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
        """
        添加新的 URL 条目
        
        Args:
            user_description: 用户常用描述
            exact_url: 精确的 URL
            page_description: 页面功能描述
            aliases: 别名列表
            keywords: 关键词列表
            marketplace: 站点（US/EU/JP/ALL）
            category: 分类
            
        Returns:
            条目ID
        """
        # 生成向量
        embedding = self._get_embedding(user_description)
        
        # 生成唯一ID
        entry_id = f"rag_{self.collection.count() + 1:03d}"
        
        # 准备元数据
        metadata = {
            "user_description": user_description,
            "exact_url": exact_url,
            "page_description": page_description,
            "aliases": json.dumps(aliases or [], ensure_ascii=False),
            "keywords": json.dumps(keywords or [], ensure_ascii=False),
            "marketplace": marketplace,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        # 添加到向量库
        self.collection.add(
            embeddings=[embedding],
            documents=[user_description],
            metadatas=[metadata],
            ids=[entry_id]
        )
        
        print(f"✅ 已添加: {user_description} -> {exact_url}")
        return entry_id
    
    def search_url(
        self,
        query: str,
        top_k: int = 3,
        marketplace: Optional[str] = None
    ) -> Dict:
        """
        检索相似的 URL
        
        Args:
            query: 查询文本
            top_k: 返回前K个结果
            marketplace: 可选的站点过滤
            
        Returns:
            检索结果字典
        """
        # 生成查询向量
        query_embedding = self._get_embedding(query)
        
        # 准备过滤条件
        where_filter = None
        if marketplace and marketplace != "ALL":
            where_filter = {"marketplace": marketplace}
        
        # 检索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            similarity = 1 - distance  # 距离越小，相似度越高
            
            formatted_results.append({
                "id": results['ids'][0][i],
                "user_description": metadata['user_description'],
                "exact_url": metadata['exact_url'],
                "page_description": metadata['page_description'],
                "aliases": json.loads(metadata.get('aliases', '[]')),
                "marketplace": metadata.get('marketplace', 'ALL'),
                "category": metadata.get('category', 'general'),
                "similarity": round(similarity, 4),
                "distance": round(distance, 4)
            })
        
        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    
    def learn_alias(self, entry_id: str, new_alias: str):
        """
        为已有条目添加新别名
        
        Args:
            entry_id: 条目ID
            new_alias: 新别名
        """
        # 获取现有条目
        entry = self.collection.get(ids=[entry_id])
        if not entry['ids']:
            print(f"❌ 未找到条目: {entry_id}")
            return
        
        # 解析现有别名
        metadata = entry['metadatas'][0]
        aliases = json.loads(metadata.get('aliases', '[]'))
        
        # 添加新别名（去重）
        if new_alias not in aliases:
            aliases.append(new_alias)
            metadata['aliases'] = json.dumps(aliases, ensure_ascii=False)
            
            # 更新条目
            self.collection.update(
                ids=[entry_id],
                metadatas=[metadata]
            )
            
            print(f"✅ 已为 {entry_id} 添加别名: {new_alias}")
    
    def increment_usage(self, entry_id: str):
        """
        增加条目的使用次数
        
        Args:
            entry_id: 条目ID
        """
        entry = self.collection.get(ids=[entry_id])
        if entry['ids']:
            metadata = entry['metadatas'][0]
            metadata['usage_count'] = int(metadata.get('usage_count', 0)) + 1
            metadata['last_used'] = datetime.now().isoformat()
            
            self.collection.update(
                ids=[entry_id],
                metadatas=[metadata]
            )
    
    def get_statistics(self) -> Dict:
        """
        获取 RAG 库统计信息
        
        Returns:
            统计信息字典
        """
        all_entries = self.collection.get()
        
        total_count = len(all_entries['ids'])
        
        # 统计分类
        categories = {}
        marketplaces = {}
        total_usage = 0
        
        for metadata in all_entries['metadatas']:
            category = metadata.get('category', 'general')
            marketplace = metadata.get('marketplace', 'ALL')
            usage = int(metadata.get('usage_count', 0))
            
            categories[category] = categories.get(category, 0) + 1
            marketplaces[marketplace] = marketplaces.get(marketplace, 0) + 1
            total_usage += usage
        
        return {
            "total_entries": total_count,
            "categories": categories,
            "marketplaces": marketplaces,
            "total_usage": total_usage,
            "avg_usage": round(total_usage / total_count, 2) if total_count > 0 else 0
        }
    
    def export_to_json(self, output_path: str = "./rag_backup.json"):
        """
        导出 RAG 库为 JSON 格式
        
        Args:
            output_path: 输出文件路径
        """
        all_entries = self.collection.get()
        
        backup_data = []
        for i, entry_id in enumerate(all_entries['ids']):
            metadata = all_entries['metadatas'][i]
            
            backup_data.append({
                "id": entry_id,
                "user_description": metadata['user_description'],
                "exact_url": metadata['exact_url'],
                "page_description": metadata['page_description'],
                "aliases": json.loads(metadata.get('aliases', '[]')),
                "keywords": json.loads(metadata.get('keywords', '[]')),
                "marketplace": metadata.get('marketplace', 'ALL'),
                "category": metadata.get('category', 'general'),
                "usage_count": metadata.get('usage_count', 0),
                "created_at": metadata.get('created_at'),
                "last_used": metadata.get('last_used')
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已导出到: {os.path.abspath(output_path)}")
        return output_path


if __name__ == "__main__":
    # 简单测试
    print("=" * 60)
    print("Amazon URL RAG 系统")
    print("=" * 60)
    
    # 测试初始化
    try:
        rag = AmazonURLRAG()
        stats = rag.get_statistics()
        print(f"\n📊 统计信息: {json.dumps(stats, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n💡 提示：请确保已设置 OPENAI_API_KEY 环境变量")
