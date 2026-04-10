import sys
import os
sys.path.append(os.path.dirname(__file__))

from rag_system_simple import SimpleAmazonURLRAG
import json

rag = SimpleAmazonURLRAG('../rag_simple_db.json')
result = rag.search_url('定价管理', top_k=3)

print(json.dumps(result, ensure_ascii=False, indent=2))
