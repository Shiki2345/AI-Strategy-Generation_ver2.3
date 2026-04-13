// ==UserScript==
// @name         Amazon客服专员账户详情页访问限制
// @namespace    http://company.internal/
// @version      1.0
// @description  禁止客服专员访问美国亚马逊账户详情页
// @author       IT Security Team
// @match        *://sellercentral.amazon.com/*
// @match        *://sellercentral.amazon.co.uk/*
// @match        *://sellercentral.amazon.co.jp/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    
    // 配置参数
    const CONFIG = {
        // 被限制的URL模式
        blockedUrls: [
            'sellercentral.amazon.com/sw/AccountInfo',
            'sellercentral.amazon.co.uk/sw/AccountInfo',
            'sellercentral.amazon.co.jp/sw/AccountInfo'
        ],
        
        // 客服角色列表
        customerServiceRoles: [
            '客服专员', '客服助理', '初级客服', 
            '售后专员', '客户支持', '在线客服', '电话客服',
            'Customer Service', 'CS Representative'
        ],
        
        // 当前用户角色（这里需要根据实际系统获取）
        currentUserRole: getUserRole() // 需要实现这个函数
    };
    
    // 获取当前用户角色
    function getUserRole() {
        // 方法1: 从页面元素获取
        const userRoleElement = document.querySelector('[data-user-role]');
        if (userRoleElement) {
            return userRoleElement.getAttribute('data-user-role');
        }
        
        // 方法2: 从本地存储获取
        const storedRole = localStorage.getItem('user-role');
        if (storedRole) {
            return storedRole;
        }
        
        // 方法3: 从cookie获取
        const roleCookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('user-role='));
        if (roleCookie) {
            return roleCookie.split('=')[1];
        }
        
        // 方法4: 从URL参数获取（临时测试用）
        const urlParams = new URLSearchParams(window.location.search);
        const roleParam = urlParams.get('user-role');
        if (roleParam) {
            return decodeURIComponent(roleParam);
        }
        
        // 默认返回（实际使用时应该从认证系统获取）
        return 'unknown';
    }
    
    // 检查是否是客服角色
    function isCustomerServiceRole() {
        return CONFIG.customerServiceRoles.includes(CONFIG.currentUserRole);
    }
    
    // 检查当前URL是否被禁止
    function isBlockedUrl(url = window.location.href) {
        return CONFIG.blockedUrls.some(blocked => 
            url.toLowerCase().includes(blocked.toLowerCase())
        );
    }
    
    // 显示阻断页面
    function showBlockScreen() {
        // 记录访问尝试
        logAccessAttempt();
        
        // 替换页面内容
        document.documentElement.innerHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>访问被禁止 - Amazon Seller Central</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-width: 700px;
                    text-align: center;
                    animation: slideIn 0.5s ease-out;
                }
                
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(-50px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .error-icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                    display: block;
                }
                
                .error-title {
                    color: #e74c3c;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    font-weight: 600;
                }
                
                .warning-box {
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 25px;
                    border-radius: 12px;
                    margin: 25px 0;
                    border-left: 5px solid #f39c12;
                }
                
                .warning-box h2 {
                    color: #856404;
                    margin-top: 0;
                    font-size: 1.4em;
                }
                
                .warning-box p {
                    color: #856404;
                    line-height: 1.6;
                    margin-bottom: 0;
                }
                
                .info-box {
                    background: #d1ecf1;
                    border: 1px solid #bee5eb;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 25px 0;
                    text-align: left;
                }
                
                .info-box h3 {
                    color: #0c5460;
                    margin-top: 0;
                    margin-bottom: 15px;
                }
                
                .info-box p {
                    color: #0c5460;
                    margin: 8px 0;
                }
                
                .alternatives-box {
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 25px;
                    border-radius: 12px;
                    margin: 25px 0;
                    text-align: left;
                }
                
                .alternatives-box h3 {
                    color: #155724;
                    margin-top: 0;
                    margin-bottom: 15px;
                    text-align: center;
                }
                
                .alternatives-list {
                    list-style: none;
                    padding: 0;
                }
                
                .alternatives-list li {
                    padding: 10px 0;
                    border-bottom: 1px solid #c3e6cb;
                    color: #155724;
                }
                
                .alternatives-list li:last-child {
                    border-bottom: none;
                }
                
                .alternatives-list a {
                    color: #155724;
                    text-decoration: none;
                    font-weight: 500;
                }
                
                .alternatives-list a:hover {
                    text-decoration: underline;
                }
                
                .help-section {
                    margin: 30px 0;
                    padding: 25px;
                    background: #f8f9fa;
                    border-radius: 12px;
                }
                
                .help-section h3 {
                    color: #495057;
                    margin-bottom: 15px;
                }
                
                .help-section ol {
                    text-align: left;
                    max-width: 500px;
                    margin: 0 auto;
                    color: #495057;
                    line-height: 1.6;
                }
                
                .btn-group {
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    flex-wrap: wrap;
                    margin: 30px 0;
                }
                
                .btn {
                    padding: 15px 25px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    transition: all 0.3s ease;
                    font-weight: 500;
                }
                
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }
                
                .btn-primary { background: #3498db; color: white; }
                .btn-success { background: #27ae60; color: white; }
                .btn-warning { background: #f39c12; color: white; }
                .btn-secondary { background: #95a5a6; color: white; }
                .btn-info { background: #17a2b8; color: white; }
                
                .footer-notice {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #eee;
                    font-size: 14px;
                    color: #666;
                    line-height: 1.5;
                }
                
                .footer-notice p {
                    margin: 8px 0;
                }
                
                .user-info {
                    background: #e3f2fd;
                    border: 1px solid #bbdefb;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #1565c0;
                }
                
                @media (max-width: 600px) {
                    .container {
                        margin: 10px;
                        padding: 20px;
                    }
                    
                    .btn-group {
                        flex-direction: column;
                        align-items: stretch;
                    }
                    
                    .btn {
                        justify-content: center;
                    }
                    
                    .error-title {
                        font-size: 2em;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error-icon">🚫</div>
                <h1 class="error-title">禁止访问</h1>
                
                <div class="user-info">
                    <strong>当前用户角色：</strong>${CONFIG.currentUserRole} | 
                    <strong>访问时间：</strong>${new Date().toLocaleString('zh-CN')}
                </div>
                
                <div class="warning-box">
                    <h2>客服人员不允许访问【美国站账户详情页】</h2>
                    <p>
                        此页面包含公司核心财务和账户信息，根据权限分离原则和数据安全规定，
                        客服人员无权查看此类信息。这是为了保护公司和客户的数据安全。
                    </p>
                </div>

                <div class="info-box">
                    <h3>📋 页面信息</h3>
                    <p><strong>页面名称：</strong>美国亚马逊账户详情页</p>
                    <p><strong>URL：</strong>https://sellercentral.amazon.com/sw/AccountInfo/</p>
                    <p><strong>敏感级别：</strong>关键敏感 - 包含银行、税务、公司核心信息</p>
                    <p><strong>限制等级：</strong>完全禁止访问</p>
                    <p><strong>适用角色：</strong>所有客服相关职位</p>
                </div>

                <div class="alternatives-box">
                    <h3>🔄 客服专用页面（推荐访问）</h3>
                    <ul class="alternatives-list">
                        <li>📦 <a href="/orders-v3" onclick="navigateToPage(this.href)">订单管理页面</a> - 查看和管理客户订单信息</li>
                        <li>💬 <a href="/messaging/inbox" onclick="navigateToPage(this.href)">买家消息中心</a> - 处理客户咨询和消息</li>
                        <li>🔄 <a href="/returns/list" onclick="navigateToPage(this.href)">退货管理页面</a> - 处理客户退货和退款申请</li>
                        <li>⭐ <a href="/product-reviews" onclick="navigateToPage(this.href)">产品评论管理</a> - 查看和分析产品评论</li>
                        <li>🎫 <a href="/cu/case-lobby" onclick="navigateToPage(this.href)">案件管理页面</a> - 管理客服工单和案件</li>
                        <li>🏠 <a href="/customer-service-dashboard" onclick="navigateToPage(this.href)">客服工作台</a> - 客服专用首页</li>
                    </ul>
                </div>

                <div class="help-section">
                    <h3>💡 如需协助客户解决账户相关问题，请按以下流程处理：</h3>
                    <ol>
                        <li><strong>联系运营人员：</strong>将有权限的运营同事拉入对话</li>
                        <li><strong>转接处理：</strong>将客户转接给有相应权限的同事</li>
                        <li><strong>提交工单：</strong>创建内部协助工单，由相关部门处理</li>
                        <li><strong>记录问题：</strong>详细记录客户问题，便于后续跟进</li>
                    </ol>
                </div>

                <div class="btn-group">
                    <a href="#" onclick="contactOperations()" class="btn btn-primary">
                        📞 联系运营人员
                    </a>
                    <a href="#" onclick="createSupportTicket()" class="btn btn-success">
                        📝 提交协助工单
                    </a>
                    <a href="#" onclick="goToDashboard()" class="btn btn-info">
                        🏠 客服工作台
                    </a>
                    <a href="#" onclick="viewAlternatives()" class="btn btn-warning">
                        🔄 查看更多可用页面
                    </a>
                    <a href="#" onclick="goBack()" class="btn btn-secondary">
                        ⬅️ 返回上一页
                    </a>
                </div>

                <div class="footer-notice">
                    <p><strong>⚠️ 重要提醒：</strong></p>
                    <p>• 此访问尝试已被系统记录并通知相关管理人员</p>
                    <p>• 如对此限制有疑问，请联系 IT 管理员或人事部门</p>
                    <p>• 重复尝试访问被禁页面可能影响个人绩效考核</p>
                    <p>• 此限制是为了保护公司数据安全和客户隐私</p>
                </div>
            </div>

            <script>
                // 全局函数
                function navigateToPage(url) {
                    // 构建完整URL
                    const baseUrl = window.location.origin;
                    const fullUrl = url.startsWith('http') ? url : baseUrl + url;
                    
                    console.log('导航到：', fullUrl);
                    window.location.href = fullUrl;
                }
                
                function contactOperations() {
                    // 实际实现时可以集成内部通讯系统
                    alert('正在为您联系运营人员...\\n\\n请稍候，运营同事将通过内部系统与您联系。');
                    
                    // 可以在这里添加实际的联系逻辑
                    // 例如：发送内部消息、创建会话等
                }
                
                function createSupportTicket() {
                    const reason = prompt('请简单描述需要协助的问题：', '客户咨询账户相关信息，需要有权限同事协助处理');
                    if (reason) {
                        alert('工单已提交！\\n\\n工单内容：' + reason + '\\n\\n相关部门将尽快处理您的请求。');
                        
                        // 实际实现时在这里提交工单
                        console.log('工单内容：', reason);
                    }
                }
                
                function goToDashboard() {
                    navigateToPage('/customer-service-dashboard');
                }
                
                function viewAlternatives() {
                    const alternatives = \`
客服人员可以访问的页面：

📦 订单管理 - /orders-v3
💬 买家消息 - /messaging/inbox  
🔄 退货管理 - /returns/list
⭐ 产品评论 - /product-reviews
🎫 案件管理 - /cu/case-lobby
📊 业务报告 - /business-reports（部分）
🏠 客服工作台 - /customer-service-dashboard

如需访问其他页面，请咨询IT管理员。
                    \`;
                    alert(alternatives);
                }
                
                function goBack() {
                    if (document.referrer) {
                        window.location.href = document.referrer;
                    } else {
                        navigateToPage('/');
                    }
                }
                
                // 防止通过开发者工具绕过
                document.addEventListener('keydown', function(e) {
                    // 禁用F12、Ctrl+Shift+I等快捷键
                    if (e.key === 'F12' || 
                        (e.ctrlKey && e.shiftKey && e.key === 'I') ||
                        (e.ctrlKey && e.shiftKey && e.key === 'J') ||
                        (e.ctrlKey && e.key === 'U')) {
                        e.preventDefault();
                        alert('开发者工具已被禁用，如有技术问题请联系IT支持。');
                    }
                });
                
                // 禁用右键菜单
                document.addEventListener('contextmenu', function(e) {
                    e.preventDefault();
                });
                
                // 防止页面后退
                history.pushState(null, null, window.location.href);
                window.addEventListener('popstate', function(event) {
                    history.pushState(null, null, window.location.href);
                });
                
                console.log('客服访问限制页面已加载 - 用户角色：${CONFIG.currentUserRole}');
            </script>
        </body>
        </html>
        `;
        
        // 防止页面被重新加载
        window.addEventListener('beforeunload', function(e) {
            e.preventDefault();
            return '页面访问已被限制';
        });
    }
    
    // 记录访问尝试
    function logAccessAttempt() {
        const logData = {
            timestamp: new Date().toISOString(),
            user_role: CONFIG.currentUserRole,
            attempted_url: window.location.href,
            user_agent: navigator.userAgent,
            referrer: document.referrer,
            action: 'blocked_customer_service_access',
            page_title: document.title
        };
        
        console.warn('🚫 客服访问限制 - 访问被阻断:', logData);
        
        // 存储到本地（实际使用时应发送到服务器）
        try {
            const logs = JSON.parse(localStorage.getItem('access_violation_logs') || '[]');
            logs.push(logData);
            
            // 只保留最近50条记录
            if (logs.length > 50) {
                logs.splice(0, logs.length - 50);
            }
            
            localStorage.setItem('access_violation_logs', JSON.stringify(logs));
        } catch (e) {
            console.error('日志存储失败:', e);
        }
        
        // 实际使用时，这里应该发送到服务器
        // fetch('/api/security-log', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(logData)
        // }).catch(err => console.error('日志上传失败:', err));
    }
    
    // 拦截所有导航到被禁页面的尝试
    function interceptNavigation() {
        // 拦截链接点击
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (link && link.href && isBlockedUrl(link.href)) {
                e.preventDefault();
                e.stopPropagation();
                showBlockScreen();
                return false;
            }
        }, true);
        
        // 拦截表单提交
        document.addEventListener('submit', function(e) {
            const form = e.target;
            if (form && form.action && isBlockedUrl(form.action)) {
                e.preventDefault();
                e.stopPropagation();
                showBlockScreen();
                return false;
            }
        }, true);
        
        // 监控URL变化
        let lastUrl = location.href;
        new MutationObserver(() => {
            const url = location.href;
            if (url !== lastUrl) {
                lastUrl = url;
                if (isBlockedUrl(url)) {
                    showBlockScreen();
                }
            }
        }).observe(document, { subtree: true, childList: true });
        
        // 拦截 window.open
        const originalOpen = window.open;
        window.open = function(url, name, specs) {
            if (url && isBlockedUrl(url)) {
                showBlockScreen();
                return null;
            }
            return originalOpen.call(window, url, name, specs);
        };
        
        // 拦截 location 赋值
        const originalLocationHref = Object.getOwnPropertyDescriptor(Location.prototype, 'href');
        Object.defineProperty(Location.prototype, 'href', {
            set: function(url) {
                if (isBlockedUrl(url)) {
                    showBlockScreen();
                    return;
                }
                originalLocationHref.set.call(this, url);
            },
            get: originalLocationHref.get
        });
    }
    
    // 主初始化函数
    function initialize() {
        console.log('Amazon客服访问限制脚本启动');
        console.log('当前用户角色:', CONFIG.currentUserRole);
        console.log('当前页面URL:', window.location.href);
        
        // 检查是否是客服角色
        if (!isCustomerServiceRole()) {
            console.log('非客服角色，跳过访问限制');
            return;
        }
        
        console.log('检测到客服角色，启用访问限制');
        
        // 检查当前页面是否被禁止
        if (isBlockedUrl()) {
            console.warn('当前页面被禁止访问，显示阻断页面');
            showBlockScreen();
            return;
        }
        
        // 设置导航拦截
        interceptNavigation();
        
        console.log('访问限制初始化完成');
    }
    
    // 等待页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
    
    // 调试信息
    console.log('Amazon客服访问限制脚本已加载');
    
    // 暴露一些调试接口（生产环境应移除）
    window._debugAccessControl = {
        config: CONFIG,
        isCustomerService: isCustomerServiceRole(),
        isBlocked: isBlockedUrl(),
        showBlock: showBlockScreen,
        checkUrl: isBlockedUrl
    };
    
})();