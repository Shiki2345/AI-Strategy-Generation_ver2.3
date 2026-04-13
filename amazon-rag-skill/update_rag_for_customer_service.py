from scripts.rag_system import AmazonURLRAG
import json

# 初始化RAG系统
try:
    rag = AmazonURLRAG()
    
    # 添加客服限制相关的条目
    rag.add_url_entry(
        user_description='客服专员禁止访问美国亚马逊账户详情页',
        exact_url='https://sellercentral.amazon.com/sw/AccountInfo/',
        page_description='客服人员完全不允许访问此页面，包含敏感财务信息',
        aliases=['客服访问限制', '账户页面禁止', '客服权限控制'],
        keywords=['客服', '禁止', '限制', '账户详情', '完全阻断'],
        marketplace='US',
        category='access_control'
    )
    
    # 导出更新后的数据
    rag.export_to_json('rag_simple_db.json')
    
    # 显示统计信息
    stats = rag.get_statistics()
    print('RAG库已更新:')
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f'更新失败: {e}')
    print('请确保已设置OPENAI_API_KEY环境变量')