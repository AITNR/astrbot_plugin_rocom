"""
用户绑定本地持久化存储

使用 StarTools.get_data_dir() 确保数据存储在 AstrBot data 目录下，
插件更新/重装不会丢失用户数据。
"""

import os
import json
import copy
import asyncio
from typing import List, Dict, Optional, Any
from astrbot.api import logger


class AsyncDataManager:
    """通用异步 JSON 数据管理器"""

    def __init__(self, data_dir: str, filename: str, default_data: Any):
        self.data_dir = data_dir
        self.path = os.path.join(data_dir, filename)
        self.default_data = default_data
        self.lock = asyncio.Lock()
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Any:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"[Rocom] 加载 {self.path} 失败: {e}")
        return copy.deepcopy(self.default_data)

    async def _save(self):
        try:
            temp_path = self.path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.path)
        except Exception as e:
            logger.error(f"[Rocom] 保存 {self.path} 失败: {e}")


class UserManager(AsyncDataManager):
    """用户绑定管理"""

    def __init__(self, data_dir: str):
        super().__init__(data_dir, "rocom_bindings.json", {})

    async def get_user_bindings(self, user_id: Any) -> List[Dict]:
        user_id = str(user_id)
        async with self.lock:
            return copy.deepcopy(self.data.get(user_id, []))

    async def get_primary_binding(self, user_id: Any) -> Optional[Dict]:
        bindings = await self.get_user_bindings(user_id)
        for b in bindings:
            if b.get("is_primary"):
                return b
        return bindings[0] if bindings else None

    async def save_user_bindings(self, user_id: Any, bindings: List[Dict]):
        user_id = str(user_id)
        async with self.lock:
            # 去重（按 binding_id）
            cleaned = []
            seen = set()
            for b in bindings:
                bid = b.get("binding_id") or b.get("framework_token", "")
                if bid not in seen:
                    cleaned.append(b)
                    seen.add(bid)

            # 确保有且只有一个 is_primary
            if cleaned:
                has_primary = False
                for b in cleaned:
                    if b.get("is_primary"):
                        if has_primary:
                            b["is_primary"] = False
                        else:
                            has_primary = True
                if not has_primary:
                    cleaned[0]["is_primary"] = True

            self.data[user_id] = cleaned
            await self._save()

    async def add_binding(self, user_id: Any, binding: Dict):
        """添加一个绑定，自动设为主账号"""
        user_id = str(user_id)
        existing = await self.get_user_bindings(user_id)
        # 先取消其他的 primary
        for b in existing:
            b["is_primary"] = False
        binding["is_primary"] = True
        existing.append(binding)
        await self.save_user_bindings(user_id, existing)

    async def delete_user_binding(self, user_id: Any, index: int) -> Optional[Dict]:
        """按序号(1-based)删除绑定，返回被删除的绑定"""
        user_id = str(user_id)
        bindings = await self.get_user_bindings(user_id)
        if not (1 <= index <= len(bindings)):
            return None
        removed = bindings.pop(index - 1)
        await self.save_user_bindings(user_id, bindings)
        return removed

    async def switch_primary(self, user_id: Any, index: int) -> bool:
        """按序号 (1-based) 切换主账号"""
        user_id = str(user_id)
        bindings = await self.get_user_bindings(user_id)
        if not (1 <= index <= len(bindings)):
            return False
        for i, b in enumerate(bindings):
            b["is_primary"] = (i + 1 == index)
        await self.save_user_bindings(user_id, bindings)
        return True

    async def remove_binding_by_id(self, user_id: Any, binding_id: str) -> bool:
        """按 binding_id 删除指定绑定，返回是否删除成功"""
        user_id = str(user_id)
        async with self.lock:
            bindings = self.data.get(user_id, [])
            original_len = len(bindings)
            bindings = [b for b in bindings if b.get("binding_id") != binding_id]
            if len(bindings) < original_len:
                self.data[user_id] = bindings
                await self._save()
                return True
            return False

    async def get_all_users_bindings(self) -> Dict[str, List[Dict]]:
        """获取所有用户的绑定数据（深拷贝）"""
        async with self.lock:
            result = {}
            for user_id, bindings in self.data.items():
                result[user_id] = copy.deepcopy(bindings)
            return result
