"""
测试 RAG 检索功能

测试各种查询场景，验证 RAG 系统的检索准确性
"""

import os
import sys
from pathlib import Path
from typing import List

# 添加父目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import AmazonURLRAG


def print_search_result(result: dict, show_details: bool = True):
    """
    格式化打印搜索结果
    
    Args:
        result: 搜索结果
        show_details: 是否显示详细信息
    """
    print(f"\n🔍 查询: \"{result['query']}\"")
    print(f"📊 找到 {result['count']} 个匹配项")
    print("-" * 70)
    
    for i, item in enumerate(result['results'], 1):
        similarity_percent = item['similarity'] * 100
        
        # 根据相似度显示不同的图标
        if similarity_percent >= 85:
            icon = "🎯"
            status = "高度匹配"
        elif similarity_percent >= 70:
            icon = "✅"
            status = "较好匹配"
        elif similarity_percent >= 50:
            icon = "🟡"
            status = "部分匹配"
        else:
            icon = "🔴"
            status = "弱匹配"
        
        print(f"\n{icon} 结果 {i}: {item['user_description']} ({status})")
        print(f"   相似度: {similarity_percent:.1f}%")
        print(f"   URL: {item['exact_url']}")
        
        if show_details:
            print(f"   描述: {item['page_description']}")
            if item['aliases']:
                print(f"   别名: {', '.join(item['aliases'][:3])}")
            print(f"   站点: {item['marketplace']} | 分类: {item['category']}")


def test_exact_match(rag: AmazonURLRAG):
    """测试精确匹配"""
    print("\n" + "=" * 70)
    print("📝 测试场景 1: 精确匹配")
    print("=" * 70)
    
    test_queries = [
        "美国亚马逊账户详情页",
        "订单管理页面",
        "库存管理页面"
    ]
    
    for query in test_queries:
        result = rag.search_url(query, top_k=1)
        print_search_result(result, show_details=False)


def test_fuzzy_match(rag: AmazonURLRAG):
    """测试模糊匹配"""
    print("\n" + "=" * 70)
    print("📝 测试场景 2: 模糊匹配")
    print("=" * 70)
    
    test_queries = [
        "我想看账户信息",  # 应该匹配账户详情页
        "在哪里查看订单",  # 应该匹配订单管理
        "怎么修改价格",    # 应该匹配定价管理
    ]
    
    for query in test_queries:
        result = rag.search_url(query, top_k=3)
        print_search_result(result, show_details=True)


def test_alias_match(rag: AmazonURLRAG):
    """测试别名匹配"""
    print("\n" + "=" * 70)
    print("📝 测试场景 3: 别名匹配")
    print("=" * 70)
    
    test_queries = [
        "Seller Central账户详情",  # 别名
        "Manage Orders",           # 英文别名
        "Campaign Manager"         # 广告活动管理的别名
    ]
    
    for query in test_queries:
        result = rag.search_url(query, top_k=2)
        print_search_result(result, show_details=False)


def test_semantic_search(rag: AmazonURLRAG):
    """测试语义搜索"""
    print("\n" + "=" * 70)
    print("📝 测试场景 4: 语义搜索")
    print("=" * 70)
    
    test_queries = [
        "我想看我赚了多少钱",      # 应该匹配支付报告
        "买家给我发了消息",        # 应该匹配买家消息中心
        "产品被退货了怎么处理",    # 应该匹配退货管理
        "我要投放广告",            # 应该匹配广告活动管理
    ]
    
    for query in test_queries:
        result = rag.search_url(query, top_k=3)
        print_search_result(result, show_details=True)


def test_marketplace_filter(rag: AmazonURLRAG):
    """测试站点过滤"""
    print("\n" + "=" * 70)
    print("📝 测试场景 5: 站点过滤")
    print("=" * 70)
    
    query = "账户详情页"
    
    print(f"\n查询: \"{query}\"")
    
    marketplaces = ["ALL", "US", "JP", "EU"]
    for marketplace in marketplaces:
        result = rag.search_url(query, top_k=2, marketplace=marketplace)
        print(f"\n🌍 站点: {marketplace}")
        print(f"   找到 {result['count']} 个结果")
        for item in result['results']:
            print(f"   - {item['user_description']} ({item['marketplace']})")


def test_no_match(rag: AmazonURLRAG):
    """测试无匹配情况"""
    print("\n" + "=" * 70)
    print("📝 测试场景 6: 低匹配度查询")
    print("=" * 70)
    
    test_queries = [
        "我想吃火锅",              # 完全无关
        "天气怎么样",              # 完全无关
        "亚马逊物流追踪详情",      # 可能部分相关但库中无此页面
    ]
    
    for query in test_queries:
        result = rag.search_url(query, top_k=3)
        print_search_result(result, show_details=False)
        
        # 判断是否需要用户补充信息
        if result['results'] and result['results'][0]['similarity'] < 0.5:
            print(f"   ⚠️  最佳匹配相似度 < 50%，建议引导用户补充信息")


def interactive_test(rag: AmazonURLRAG):
    """交互式测试"""
    print("\n" + "=" * 70)
    print("🎮 交互式测试模式")
    print("=" * 70)
    print("输入查询内容，系统将返回匹配的 URL")
    print("输入 'quit' 退出")
    print("-" * 70)
    
    while True:
        query = input("\n🔍 请输入查询: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 退出测试")
            break
        
        if not query:
            continue
        
        try:
            result = rag.search_url(query, top_k=3)
            print_search_result(result, show_details=True)
            
            # 询问是否为正确结果
            if result['results']:
                correct = input("\n❓ 第一个结果是否正确？(y/n): ").strip().lower()
                if correct == 'y':
                    print("✅ 太好了！")
                    # 可以增加使用计数
                    rag.increment_usage(result['results'][0]['id'])
                else:
                    print("💡 可以考虑添加新的别名或创建新条目")
        
        except Exception as e:
            print(f"❌ 查询出错: {e}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("🧪 Amazon URL RAG 系统测试")
    print("=" * 70)
    
    try:
        # 初始化 RAG 系统
        print("\n📝 正在加载 RAG 系统...")
        rag = AmazonURLRAG(db_path="../rag_db")
        
        # 显示统计信息
        stats = rag.get_statistics()
        print(f"✅ 已加载 {stats['total_entries']} 条数据")
        
        # 运行测试套件
        test_exact_match(rag)
        test_fuzzy_match(rag)
        test_alias_match(rag)
        test_semantic_search(rag)
        test_marketplace_filter(rag)
        test_no_match(rag)
        
        # 显示最终统计
        print("\n" + "=" * 70)
        print("📊 测试完成统计")
        print("=" * 70)
        stats = rag.get_statistics()
        print(f"总条目数: {stats['total_entries']}")
        print(f"总使用次数: {stats['total_usage']}")
        print(f"平均使用次数: {stats['avg_usage']}")
        
        # 询问是否进入交互模式
        print("\n" + "=" * 70)
        interactive = input("是否进入交互式测试？(y/N): ").strip().lower()
        if interactive == 'y':
            interactive_test(rag)
        
        print("\n✅ 所有测试完成！")
        
    except ValueError as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 解决方案:")
        print("  1. 设置环境变量: set OPENAI_API_KEY=your_key")
        print("  2. 或创建 .env 文件")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
