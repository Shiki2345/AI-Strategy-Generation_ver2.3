#!/usr/bin/env python3
"""
快速RAG检索脚本
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from rag_system_simple import SimpleAmazonURLRAG

def search_pages(queries):
    rag = SimpleAmazonURLRAG("amazon-rag-skill/rag_simple_db.json")
    
    all_results = []
    for query in queries:
        print(f"\n[SEARCH] 检索: {query}")
        results = rag.search_url(query, top_k=3)
        
        for i, result in enumerate(results['results']):
            print(f"  {i+1}. {result['user_description']} (相似度: {result['similarity']:.2f})")
            print(f"     URL: {result['exact_url']}")
            print(f"     站点: {result['marketplace']}")
            print()
            
        all_results.extend(results['results'])
    
    return all_results

if __name__ == "__main__":
    # 检索目标页面
    queries = [
        "买家消息中心",
        "商品评论管理"
    ]
    
    results = search_pages(queries)