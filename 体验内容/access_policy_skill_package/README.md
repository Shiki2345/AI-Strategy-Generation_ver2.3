# 访问策略配置 Skill 包 - 使用指南

## 📦 包含内容

1. **skill_definition.json** - Skill 核心定义
   - 对话流程模板
   - 参数收集逻辑
   - 常见问题处理

2. **config_template.json** - 配置模板
   - 标准 JSON 结构
   - 占位符说明
   - 可直接填充使用

3. **presets.json** - 预设资源库
   - 常见网站分类
   - 时间段预设
   - 用户范围模板

4. **example_output.json** - 示例配置
   - 完整可用的配置
   - 基于真实对话生成

## 🚀 如何使用

### 场景 1: AI 助手集成
将 `skill_definition.json` 导入到支持 Skill 的 AI 系统中，助手将自动：
- 识别用户意图
- 引导对话流程
- 生成标准配置

### 场景 2: 手动配置
1. 复制 `config_template.json`
2. 从 `presets.json` 选择预设值
3. 替换 `{{占位符}}`
4. 导出最终配置

### 场景 3: 二次开发
基于此 Skill 扩展新功能：
- 添加新的网站分类到 `presets.json`
- 扩展 `dialogue_flow` 支持更多策略类型
- 自定义参数验证规则

## 🎯 快速开始示例

**需求**: 限制学生上课时间玩游戏

**步骤**:
1. 打开 `skill_definition.json` 找到对话流程
2. 从 `presets.json` 选择 `gaming` 分类
3. 使用 `school_hours` 时间预设
4. 填充到 `config_template.json`
5. 生成最终配置

**预期输出**:
```json
{
  "policy_name": "上课时间游戏网站限制",
  "time_restrictions": {
    "schedule": {
      "days_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "time_range": {"start": "08:00", "end": "17:00"}
    }
  },
  "blacklist": {
    "domains": ["*.4399.com", "*.7k7k.com", "*.steam.com", "..."]
  }
}
```

## 🔧 自定义扩展

### 添加新网站分类
编辑 `presets.json`:
```json
"streaming_music": {
  "name": "音乐流媒体",
  "domains": ["*.spotify.com", "*.music.163.com"],
  "tags": ["音乐", "娱乐"]
}
```

### 支持新策略类型
修改 `skill_definition.json` 的 `policy_type`:
- `time_based_whitelist` (时间白名单)
- `bandwidth_limit` (带宽限制)
- `content_filter` (内容过滤)

## 📊 配置模板占位符说明

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{{POLICY_NAME}}` | 策略名称 | "工作时间视频网站限制" |
| `{{DESCRIPTION}}` | 策略描述 | "工作时间禁止员工访问视频网站" |
| `{{DAYS_OF_WEEK}}` | 星期数组 | ["Monday", "Tuesday", ...] |
| `{{START_TIME}}` | 开始时间 | "09:00" |
| `{{END_TIME}}` | 结束时间 | "18:00" |
| `{{TIMEZONE}}` | 时区 | "Asia/Shanghai" |
| `{{BLOCKED_DOMAINS}}` | 域名数组 | ["*.bilibili.com", ...] |
| `{{MATCH_TYPE}}` | 匹配类型 | "wildcard" / "exact" / "regex" |
| `{{BLOCK_MESSAGE}}` | 拦截提示 | "工作时间禁止访问视频网站" |
| `{{APPLY_TO}}` | 适用范围 | "all_users" / "specific_groups" |
| `{{EXCEPTION_ROLES}}` | 例外角色 | ["BOSS", "Manager"] |
| `{{TIMESTAMP}}` | 时间戳 | "2024-01-01T00:00:00Z" |
| `{{TAGS}}` | 标签数组 | ["工作时间", "视频限制"] |

## 🎨 对话流程说明

### Phase 1: 识别意图
- 匹配用户输入关键词
- 判断策略类型
- 确认用户需求

### Phase 2: 收集基本信息
- 时间范围（必需）
- 屏蔽网站列表（必需）
- 用户范围（必需）

### Phase 3: 确认细节
- 域名精准度检查
- 子域名匹配策略
- 策略命名

### Phase 4: 生成配置
- 填充配置模板
- 添加增强功能
- 验证配置完整性

### Phase 5: 交付
- 输出 JSON 配置
- 提供使用说明
- 给出后续建议

## 📞 技术支持

遇到问题？
1. 查看 `example_output.json` 参考完整配置
2. 检查 `skill_definition.json` 中的 `best_practices`
3. 参考 `common_patterns` 处理特殊情况

## 💡 最佳实践

### 1. 域名配置
- ✅ 使用通配符 `*.domain.com` 匹配所有子域名
- ✅ 避免使用过于宽泛的顶级域名（如 qq.com）
- ✅ 优先使用精准的服务域名（如 v.qq.com）

### 2. 时间设置
- ✅ 明确指定时区，避免歧义
- ✅ 使用 24 小时制 (HH:MM)
- ✅ 考虑跨时区场景

### 3. 用户范围
- ✅ 优先使用角色/组而非个人
- ✅ 合理设置例外情况
- ✅ 记录例外原因

### 4. 日志与监控
- ✅ 开启违规日志记录
- ✅ 定期审查访问日志
- ✅ 根据数据优化策略

## 📝 版本历史

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- ✨ 支持时间限制黑名单策略
- ✨ 包含 6 大预设网站分类
- ✨ 提供完整对话流程模板
- ✨ 支持用户例外配置

## 📄 许可证

本 Skill 包采用 MIT 许可证，可自由使用、修改和分发。

---

**Made with ❤️ by Access Policy Assistant**
