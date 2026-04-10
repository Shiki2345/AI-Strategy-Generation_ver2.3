"""
测试简化版 RAG 检索功能
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag_system_simple import SimpleAmazonURLRAG


def print_search_result(result: dict):
    """格式化打印搜索结果"""
    print(f"\n[QUERY] {result['query']}")
    print(f"[FOUND] {result['count']} 个匹配项")
    print("-" * 70)
    
    for i, item in enumerate(result['results'], 1):
        similarity_percent = item['similarity'] * 100
        
        # 根据相似度显示不同的标记
        if similarity_percent >= 85:
            status = "[高度匹配]"
        elif similarity_percent >= 70:
            status = "[较好匹配]"
        elif similarity_percent >= 50:
            status = "[部分匹配]"
        else:
            status = "[弱匹配]"
        
        print(f"\n{status} 结果 {i}: {item['user_description']}")
        print(f"   相似度: {similarity_percent:.1f}%")
        print(f"   URL: {item['exact_url']}")
        print(f"   描述: {item['page_description']}")
        if item['aliases']:
            print(f"   别名: {', '.join(item['aliases'][:3])}")
        print(f"   站点: {item['marketplace']} | 分类: {item['category']}")


def run_tests():
    """运行测试"""
    print("=" * 70)
    print("简化版 Amazon URL RAG 系统测试")
    print("=" * 70)
    
    try:
        # 初始化
        print("\n[INIT] 加载 RAG 系统...")
        rag = SimpleAmazonURLRAG(db_path="../rag_simple_db.json")
        
        stats = rag.get_statistics()
        print(f"[OK] 已加载 {stats['total_entries']} 条数据")
        
        # 测试用例
        test_cases = [
            {"name": "精确匹配", "queries": [
                "美国亚马逊账户详情页",
                "订单管理页面"
            ]},
            {"name": "模糊匹配", "queries": [
                "我想看账户信息",
                "在哪里查看订单",
                "怎么修改价格"
            ]},
            {"name": "语义搜索", "queries": [
                "我想看我赚了多少钱",
                "买家给我发了消息",
                "产品被退货了"
            ]}
        ]
        
        for test_group in test_cases:
            print(f"\n\n{'=' * 70}")
            print(f"[TEST] {test_group['name']}")
            print("=" * 70)
            
            for query in test_group['queries']:
                result = rag.search_url(query, top_k=3)
                print_search_result(result)
        
        # 统计信息
        print(f"\n\n{'=' * 70}")
        print("[STATS] 测试完成统计")
        print("=" * 70)
        print(f"总条目数: {stats['total_entries']}")
        print(f"总使用次数: {stats['total_usage']}")
        print(f"平均使用次数: {stats['avg_usage']}")
        
        # 交互测试
        print(f"\n\n{'=' * 70}")
        interactive = input("是否进入交互式测试？(y/N): ").strip().lower()
        
        if interactive == 'y':
            print("\n[INTERACTIVE] 交互式测试模式")
            print("输入查询内容，系统将返回匹配的 URL")
            print("输入 'quit' 退出")
            print("-" * 70)
            
            while True:
                query = input("\n[INPUT] 请输入查询: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("[EXIT] 退出测试")
                    break
                
                if not query:
                    continue
                
                try:
                    result = rag.search_url(query, top_k=3)
                    print_search_result(result)
                except Exception as e:
                    print(f"[ERROR] 查询出错: {e}")
        
        print("\n[SUCCESS] 所有测试完成！")
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_tests()
