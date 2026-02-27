import openai
import asyncio
import json
from typing import Dict, List, Any, Optional
from config import config
from core.logger import logger_manager

class AIEngine:
    def __init__(self):
        self.logger = logger_manager.get_logger('ai_engine')
        self.client = None
        self.conversation_history = []
        self.max_history_length = 50
        self.initialize_openai()
    
    def initialize_openai(self):
        """初始化OpenAI客户端"""
        try:
            if config.OPENAI_API_KEY:
                self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
                self.logger.info("OpenAI客户端初始化成功")
            else:
                self.logger.warning("未配置OpenAI API密钥")
        except Exception as e:
            self.logger.error(f"OpenAI初始化失败: {e}")
    
    async def chat_completion(self, messages: List[Dict], model: str = None) -> Optional[str]:
        """AI对话完成"""
        if not self.client:
            return "AI服务未初始化，请检查API密钥配置"
        
        try:
            model = model or config.DEFAULT_MODEL
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=config.MAX_TOKENS,
                    temperature=0.7
                )
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"AI对话失败: {e}")
            return f"抱歉，处理您的请求时出现错误: {str(e)}"
    
    def add_to_history(self, role: str, content: str):
        """添加对话到历史记录"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        })
        
        # 限制历史记录长度
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_conversation_context(self, limit: int = 10) -> List[Dict]:
        """获取对话上下文"""
        recent_history = self.conversation_history[-limit:] if self.conversation_history else []
        return [{"role": msg["role"], "content": msg["content"]} for msg in recent_history]
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
        self.logger.info("对话历史已清空")
    
    async def process_user_input(self, user_input: str, context: Dict = None) -> str:
        """处理用户输入"""
        try:
            # 添加用户消息到历史
            self.add_to_history("user", user_input)
            
            # 构建系统提示
            system_prompt = self._build_system_prompt(context)
            
            # 构建消息列表
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.get_conversation_context())
            messages.append({"role": "user", "content": user_input})
            
            # 获取AI响应
            response = await self.chat_completion(messages)
            
            # 添加AI响应到历史
            if response:
                self.add_to_history("assistant", response)
            
            return response or "抱歉，我没有理解您的意思。"
            
        except Exception as e:
            self.logger.error(f"处理用户输入失败: {e}")
            return "处理您的请求时出现内部错误。"
    
    def _build_system_prompt(self, context: Dict = None) -> str:
        """构建系统提示词"""
        base_prompt = f"""你是一个高级AI桌面助手，名为{config.APP_NAME} v{config.VERSION}。
你的开发者是{config.DEVELOPER}。

你的能力包括：
1. 系统管理和监控
2. 文件操作和管理
3. 网络诊断和工具
4. 多媒体控制
5. 自动化任务执行
6. 安全扫描和防护

请以专业、友好且高效的方式协助用户。
如果涉及敏感操作，请先确认用户意图。
"""

        if context:
            base_prompt += f"\n当前上下文信息：{json.dumps(context, ensure_ascii=False, indent=2)}"
        
        return base_prompt
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def analyze_system_state(self) -> Dict[str, Any]:
        """分析系统状态"""
        try:
            import psutil
            import platform
            
            system_info = {
                "os": platform.system(),
                "version": platform.version(),
                "architecture": platform.architecture()[0],
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_connections": len(psutil.net_connections()),
                "process_count": len(psutil.pids())
            }
            
            analysis_prompt = f"""
请分析以下系统状态信息，并提供优化建议：

{json.dumps(system_info, indent=2)}

请从性能、安全、资源使用等方面给出专业建议。
"""

            messages = [
                {"role": "system", "content": "你是系统分析师，专门分析计算机系统状态并提供建议。"},
                {"role": "user", "content": analysis_prompt}
            ]
            
            analysis = await self.chat_completion(messages)
            return {
                "system_info": system_info,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"系统状态分析失败: {e}")
            return {"error": str(e)}

# 全局AI引擎实例
ai_engine = AIEngine()