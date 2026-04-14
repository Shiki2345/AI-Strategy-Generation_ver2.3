"""
将 Amazon_real_URL.txt 中的 219 条 URL 导入 rag_simple_db.json
处理编码问题（UTF-8 被当 Latin-1 读取导致的乱码）并转换为 RAG 格式
"""
import json
import re
from datetime import datetime

# ---- 1. 读取源数据并修复编码 ----
input_path = r"c:\Users\Administrator\Desktop\Algernon\AI辅助策略生成模块\Amazon_real_URL.txt"

with open(input_path, "rb") as f:
    raw = f.read()

# 尝试直接 UTF-8 解码
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError:
    # 如果失败，尝试 Latin-1 -> UTF-8 修复
    text = raw.decode("latin-1")

# 如果 name 字段仍然是乱码（Latin-1 编码的 UTF-8），修复它
def fix_mojibake(s):
    """修复 UTF-8 被当 Latin-1 读取的乱码"""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return s

source = json.loads(text)
entries = source["payload"]["data"]

# ---- 2. 分类规则 ----
def classify_url(name, url):
    """根据名称和 URL 自动分类"""
    name_lower = name.lower()
    url_lower = url.lower()

    # 站点首页
    if url_lower.endswith("/") and "sellercentral" in url_lower and "/home" not in url_lower and len(url_lower.split("/")) <= 4:
        return "marketplace_homepage", "ALL"

    # 广告
    if "advertising" in url_lower or "campaign" in url_lower or "sspa" in url_lower or "cm/" in url_lower:
        return "advertising", "ALL"
    if any(k in name_lower for k in ["广告", "ad", "campaign"]):
        return "advertising", "ALL"

    # 订单
    if "orders" in url_lower or "order" in url_lower:
        return "order_management", "ALL"
    if any(k in name_lower for k in ["订单", "order"]):
        return "order_management", "ALL"

    # 库存/FBA
    if "inventory" in url_lower or "fba" in url_lower or "sendtoamazon" in url_lower:
        return "inventory_fba", "ALL"
    if any(k in name_lower for k in ["库存", "fba", "亚马逊物流", "补货", "移除"]):
        return "inventory_fba", "ALL"

    # 商品/Listing
    if "listing" in url_lower or "product" in url_lower or "abis" in url_lower:
        return "product_management", "ALL"
    if any(k in name_lower for k in ["商品", "listing", "上传", "编辑", "变体"]):
        return "product_management", "ALL"

    # 定价
    if "pricing" in url_lower or "automatepricing" in url_lower or "discounts" in url_lower:
        return "pricing", "ALL"
    if any(k in name_lower for k in ["定价", "价格", "佣金"]):
        return "pricing", "ALL"

    # 促销/优惠
    if "promotions" in url_lower or "coupons" in url_lower or "merchandising" in url_lower or "vine" in url_lower:
        return "promotions", "ALL"
    if any(k in name_lower for k in ["促销", "优惠", "coupon", "秒杀"]):
        return "promotions", "ALL"

    # 财务/付款
    if "payments" in url_lower or "billing" in url_lower or "wallet" in url_lower or "deposit" in url_lower or "charge" in url_lower or "settlements" in url_lower:
        return "finance", "ALL"
    if any(k in name_lower for k in ["付款", "账单", "钱包", "存款", "付费", "结算", "报表", "发票"]):
        return "finance", "ALL"

    # 账户/设置
    if "accountinfo" in url_lower or "account" in url_lower or "global-dashboard" in url_lower or "seller-verification" in url_lower:
        return "account_settings", "ALL"
    if any(k in name_lower for k in ["账户", "账号", "设置", "登录", "验证", "信息", "权限"]):
        return "account_settings", "ALL"

    # 绩效/健康
    if "performance" in url_lower or "voice-of-the-customer" in url_lower or "feedback" in url_lower or "guarantee" in url_lower or "chargebacks" in url_lower:
        return "account_health", "ALL"
    if any(k in name_lower for k in ["绩效", "账户状况", "反馈", "索赔", "买家之声"]):
        return "account_health", "ALL"

    # 报告/分析
    if "report" in url_lower or "analytics" in url_lower or "business-reports" in url_lower or "custom-analytics" in url_lower:
        return "reports", "ALL"
    if any(k in name_lower for k in ["报告", "报表", "分析"]):
        return "reports", "ALL"

    # 品牌
    if "brandregistry" in url_lower or "brand" in url_lower or "enhanced-content" in url_lower:
        return "brand", "ALL"
    if any(k in name_lower for k in ["品牌", "brand"]):
        return "brand", "ALL"

    # B2B
    if "b2b" in url_lower or "business" in url_lower and "manage-quotes" in url_lower:
        return "b2b", "ALL"

    # 帮助/支持
    if "help" in url_lower or "case" in url_lower or "support" in url_lower or "forums" in url_lower or "learn" in url_lower:
        return "help_support", "ALL"
    if any(k in name_lower for k in ["帮助", "cases", "论坛", "大学", "新闻"]):
        return "help_support", "ALL"

    # 应用/开发
    if "appstore" in url_lower or "apps" in url_lower or "developer" in url_lower or "tsba" in url_lower or "solutionprovider" in url_lower:
        return "apps_services", "ALL"

    # 税务
    if "tax" in url_lower:
        return "tax", "ALL"

    # 退货
    if "return" in url_lower:
        return "returns", "ALL"

    # 登录/认证
    if "signin" in url_lower or "register" in url_lower or "mfa" in url_lower or "sso" in url_lower or "cnep" in url_lower:
        return "authentication", "ALL"

    # 增长/计划
    if "grow" in url_lower or "programs" in url_lower or "selection" in url_lower or "opportunity" in url_lower:
        return "growth_tools", "ALL"

    # 配送设置
    if "shipping" in url_lower or "sbr" in url_lower:
        return "shipping_settings", "ALL"

    return "other", "ALL"


def detect_marketplace(url):
    """从站点特定 URL 检测 marketplace"""
    marketplace_map = {
        "sellercentral.amazon.com/": "US",
        "sellercentral.amazon.co.uk/": "UK",
        "sellercentral.amazon.de/": "DE",
        "sellercentral.amazon.fr/": "FR",
        "sellercentral.amazon.it/": "IT",
        "sellercentral.amazon.es/": "ES",
        "sellercentral.amazon.nl/": "NL",
        "sellercentral.amazon.se/": "SE",
        "sellercentral.amazon.pl/": "PL",
        "sellercentral.amazon.com.be/": "BE",
        "sellercentral.amazon.co.jp/": "JP",
        "sellercentral-japan.amazon.com/": "JP",
        "sellercentral.amazon.com.au/": "AU",
        "sellercentral.amazon.sg/": "SG",
        "sellercentral.amazon.com.mx/": "MX",
        "sellercentral.amazon.ca/": "CA",
        "sellercentral.amazon.sa/": "SA",
        "sellercentral.amazon.ae/": "AE",
        "sellercentral.amazon.eg/": "EG",
        "sellercentral-europe.amazon.com/": "EU",
        "advertising.amazon.com/": "US",
        "advertising.amazon.co.uk/": "UK",
        "advertising.amazon.de/": "DE",
        "advertising.amazon.fr/": "FR",
        "advertising.amazon.it/": "IT",
        "advertising.amazon.es/": "ES",
        "advertising.amazon.nl/": "NL",
        "advertising.amazon.se/": "SE",
        "advertising.amazon.pl/": "PL",
        "advertising.amazon.co.jp/": "JP",
        "advertising-japan.amazon.com/": "JP",
        "advertising.amazon.com.au/": "AU",
        "advertising.amazon.com.mx/": "MX",
        "advertising.amazon.ca/": "CA",
    }
    for pattern, market in marketplace_map.items():
        if pattern in url:
            return market
    if "*" in url:
        return "ALL"
    return "ALL"


# ---- 3. 转换为 RAG 格式 ----
now = datetime.now().isoformat()
rag_entries = []

for i, entry in enumerate(entries):
    name = fix_mojibake(entry["name"])
    url = entry["url_pattern"]

    category, _ = classify_url(name, url)
    marketplace = detect_marketplace(url)

    rag_entry = {
        "id": f"rag_{i+1:03d}",
        "user_description": name,
        "exact_url": url,
        "page_description": "",
        "aliases": [],
        "keywords": [kw for kw in re.split(r'[-/\s]', name) if len(kw) > 0],
        "marketplace": marketplace,
        "category": category,
        "created_at": now,
        "usage_count": 0,
        "last_used": None
    }
    rag_entries.append(rag_entry)

# ---- 4. 写入 ----
output_path = r"c:\Users\Administrator\Desktop\Algernon\AI辅助策略生成模块\amazon-rag-skill\rag_simple_db.json"
backup_path = r"c:\Users\Administrator\Desktop\Algernon\AI辅助策略生成模块\amazon-rag-skill\rag_backup.json"

# 备份旧数据
import shutil
shutil.copy2(output_path, backup_path)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(rag_entries, f, ensure_ascii=False, indent=2)

# 同步到根目录
root_output = r"c:\Users\Administrator\Desktop\Algernon\AI辅助策略生成模块\rag_simple_db.json"
root_backup = r"c:\Users\Administrator\Desktop\Algernon\AI辅助策略生成模块\rag_backup.json"
shutil.copy2(output_path, root_output)
shutil.copy2(backup_path, root_backup)

# ---- 5. 统计 ----
categories = {}
marketplaces = {}
for e in rag_entries:
    cat = e["category"]
    mkt = e["marketplace"]
    categories[cat] = categories.get(cat, 0) + 1
    marketplaces[mkt] = marketplaces.get(mkt, 0) + 1

print(f"导入完成！共 {len(rag_entries)} 条记录")
print(f"\n按分类统计：")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
print(f"\n按站点统计：")
for mkt, count in sorted(marketplaces.items(), key=lambda x: -x[1]):
    print(f"  {mkt}: {count}")

# 输出前 5 条检查编码
print(f"\n前5条数据（检查编码）：")
for e in rag_entries[:5]:
    print(f"  {e['id']}: {e['user_description']} -> {e['exact_url']}")
