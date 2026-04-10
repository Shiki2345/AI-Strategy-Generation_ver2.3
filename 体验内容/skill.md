{
  "skill_name": "web_access_policy_builder",
  "skill_type": "conversational_configurator",
  "version": "1.0",
  "description": "通过对话生成网页访问策略配置",
  
  "workflow": {
    "step1": "识别策略类型 (specific_website/global_website)",
    "step2": "多轮确认 (对象/时间/内容/审批)",
    "step3": "生成JSON配置",
    "step4": "沉淀对话模式"
  },
  
  "templates": {
    "greeting": "您好！我是访问策略配置助手，可以帮助您配置网页访问策略。首先，请您描述一下您想要配置的策略类型：\n1. 限制特定网站访问\n2. 控制所有网站的操作权限",
    
    "questions": [
      {
        "id": "target_users",
        "question": "生效对象是谁？",
        "follow_up": ["是否排除特定人群？", "是否包括实习生/外包/远程员工？"]
      },
      {
        "id": "schedule", 
        "question": "什么时间生效？",
        "follow_up": ["具体时间段？", "工作日/周末？", "是否包括午休？"]
      },
      {
        "id": "restrictions",
        "question": "具体限制内容是什么？",
        "follow_up": ["具体网站列表？", "完全禁止还是功能限制？"]
      },
      {
        "id": "approval",
        "question": "是否需要审批流程？",
        "follow_up": ["谁审批？", "线上还是线下？", "最长有效期？"]
      }
    ],
    
    "json_schema": {
      "file": "web_access_policy_schema.json",
      "default_values": {
        "policy_type": "specific_website",
        "status": "active",
        "enforcement.action": "block_with_notification",
        "monitoring.report_frequency": "weekly"
      }
    },
    
    "pattern_extraction": {
      "keywords_to_watch": ["禁止", "限制", "允许", "上班时间", "下班后", "社交媒体", "视频网站", "游戏网站"],
      "common_patterns": [
        {
          "name": "工作时间社交媒体限制",
          "triggers": ["上班时间", "社交媒体", "禁止访问"],
          "template": "工作时间{网站类型}访问限制策略"
        }
      ]
    }
  },
  
  "examples": {
    "example1": {
      "user_query": "我想在上班时间禁止员工访问社交媒体网站",
      "config": "web_access_policy_social_media_work_hours.json"
    }
  }
}