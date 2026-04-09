"""
WeGame + Rocom HTTP API 客户端

认证分两层：
- 登录 / 账号管理接口使用 wegame_api_key (scope=wegame)
- 游戏数据查询接口使用 rocom_api_key (scope=game:rocom)
- 所有游戏查询接口额外携带 X-Framework-Token
"""

import httpx
from typing import Optional, Dict, Any, List
from astrbot.api import logger


class RocomClient:
    """洛克王国 API 客户端"""

    def __init__(
        self,
        base_url: str = "https://wegame.shallow.ink",
        wegame_api_key: str = "",
        timeout: float = 15.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.wegame_api_key = wegame_api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    def _wegame_headers(self, fw_token: str = "") -> Dict[str, str]:
        """登录/账号管理接口的请求头"""
        headers = {}
        if self.wegame_api_key:
            headers["X-API-Key"] = self.wegame_api_key
        if fw_token:
            headers["X-Framework-Token"] = fw_token
        return headers

    def _rocom_headers(self, fw_token: str) -> Dict[str, str]:
        """游戏数据查询接口的请求头"""
        headers = {"X-Framework-Token": fw_token}
        if self.wegame_api_key:
            headers["X-API-Key"] = self.wegame_api_key
        return headers

    async def _get(
        self, path: str, headers: Dict[str, str], params: Optional[Dict] = None
    ) -> Optional[Dict]:
        try:
            client = await self._get_client()
            resp = await client.get(
                f"{self.base_url}{path}", headers=headers, params=params
            )
            data = resp.json()
            if data.get("code") != 0:
                logger.warning(f"[Rocom API] {path} 错误: {data.get('message', '未知')}")
                return None
            return data.get("data", {})
        except Exception as e:
            logger.error(f"[Rocom API] GET {path} 异常: {e}")
            return None

    async def _post(
        self,
        path: str,
        headers: Dict[str, str],
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Optional[Dict]:
        try:
            client = await self._get_client()
            resp = await client.post(
                f"{self.base_url}{path}",
                headers=headers,
                json=json_data,
                params=params,
            )
            data = resp.json()
            if data.get("code") != 0:
                logger.warning(f"[Rocom API] {path} 错误: {data.get('message', '未知')}")
                return None
            return data.get("data", {})
        except Exception as e:
            logger.error(f"[Rocom API] POST {path} 异常: {e}")
            return None

    async def _delete(
        self, path: str, headers: Dict[str, str]
    ) -> Optional[Dict]:
        try:
            client = await self._get_client()
            resp = await client.delete(f"{self.base_url}{path}", headers=headers)
            data = resp.json()
            if data.get("code") != 0:
                logger.warning(f"[Rocom API] {path} 错误: {data.get('message', '未知')}")
                return None
            return data.get("data", {})
        except Exception as e:
            logger.error(f"[Rocom API] DELETE {path} 异常: {e}")
            return None

    # ─── 登录相关 ───

    async def qq_qr_login(self, user_identifier: str = "") -> Optional[Dict]:
        """发起 QQ 扫码登录，返回 frameworkToken + qr_image (base64)"""
        params = {"client_type": "bot", "client_id": "astrbot"}
        if user_identifier:
            params["user_identifier"] = user_identifier
        return await self._get(
            "/api/v1/login/wegame/qr",
            self._wegame_headers(),
            params=params,
        )

    async def qq_qr_status(self, fw_token: str) -> Optional[Dict]:
        """轮询 QQ 扫码状态"""
        return await self._get(
            "/api/v1/login/wegame/status",
            self._wegame_headers(fw_token),
        )

    async def wechat_qr_login(self, user_identifier: str = "") -> Optional[Dict]:
        """发起微信扫码登录，返回 frameworkToken + qr_image (URL)"""
        params = {"client_type": "bot", "client_id": "astrbot"}
        if user_identifier:
            params["user_identifier"] = user_identifier
        return await self._get(
            "/api/v1/login/wegame/wechat/qr",
            self._wegame_headers(),
            params=params,
        )

    async def wechat_qr_status(self, fw_token: str) -> Optional[Dict]:
        """轮询微信扫码状态"""
        return await self._get(
            "/api/v1/login/wegame/wechat/status",
            self._wegame_headers(fw_token),
        )

    async def get_qq_token(self, fw_token: str) -> Optional[Dict]:
        """查询 QQ 扫码凭证"""
        return await self._get(
            "/api/v1/login/wegame/token",
            self._wegame_headers(fw_token),
        )

    async def get_wechat_token(self, fw_token: str) -> Optional[Dict]:
        """查询微信扫码凭证"""
        return await self._get(
            "/api/v1/login/wegame/wechat/token",
            self._wegame_headers(fw_token),
        )

    async def import_token(
        self, tgp_id: str, tgp_ticket: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """导入 tgp_id + tgp_ticket 凭证"""
        body: Dict[str, Any] = {
            "tgp_id": tgp_id,
            "tgp_ticket": tgp_ticket,
            "client_type": "bot",
            "client_id": "astrbot",
        }
        if user_identifier:
            body["user_identifier"] = user_identifier
        return await self._post(
            "/api/v1/login/wegame/token",
            self._wegame_headers(),
            json_data=body,
        )

    async def refresh_token(self, fw_token: str) -> Optional[Dict]:
        """刷新 QQ 凭证（仅 QQ 扫码登录的凭证支持）"""
        return await self._get(
            "/api/v1/login/wegame/refresh",
            self._wegame_headers(fw_token),
        )

    async def delete_token(self, fw_token: str) -> Optional[Dict]:
        """删除凭证"""
        return await self._delete(
            "/api/v1/login/wegame/token",
            self._wegame_headers(fw_token),
        )

    # ─── 账号绑定管理 ───

    async def get_bindings(self, user_identifier: str) -> Optional[Dict]:
        """获取用户绑定列表"""
        headers = self._wegame_headers()
        headers["X-User-Identifier"] = user_identifier
        return await self._get("/api/v1/user/bindings", headers)

    async def create_binding(
        self, fw_token: str, user_identifier: str
    ) -> Optional[Dict]:
        """手动创建绑定"""
        headers = self._wegame_headers()
        return await self._post(
            "/api/v1/user/bindings",
            headers,
            json_data={
                "framework_token": fw_token,
                "user_identifier": user_identifier,
                "client_type": "bot",
                "client_id": "astrbot",
            },
        )

    async def switch_primary(
        self, binding_id: str, user_identifier: str
    ) -> Optional[Dict]:
        """切换主账号"""
        headers = self._wegame_headers()
        headers["X-User-Identifier"] = user_identifier
        return await self._post(
            f"/api/v1/user/bindings/{binding_id}/primary", headers
        )

    async def refresh_binding(
        self, binding_id: str, user_identifier: str
    ) -> Optional[Dict]:
        """刷新绑定凭证"""
        headers = self._wegame_headers()
        headers["X-User-Identifier"] = user_identifier
        return await self._post(
            f"/api/v1/user/bindings/{binding_id}/refresh", headers
        )

    async def delete_binding(
        self, binding_id: str, user_identifier: str
    ) -> Optional[Dict]:
        """删除绑定"""
        headers = self._wegame_headers()
        headers["X-User-Identifier"] = user_identifier
        return await self._delete(
            f"/api/v1/user/bindings/{binding_id}", headers
        )

    # ─── 洛克王国游戏数据 ───

    async def get_role(self, fw_token: str) -> Optional[Dict]:
        """角色资料"""
        return await self._get(
            "/api/v1/games/rocom/profile/role",
            self._rocom_headers(fw_token),
        )

    async def get_evaluation(self, fw_token: str) -> Optional[Dict]:
        """AI 维度评价"""
        return await self._get(
            "/api/v1/games/rocom/profile/evaluation",
            self._rocom_headers(fw_token),
        )

    async def get_pet_summary(self, fw_token: str) -> Optional[Dict]:
        """精灵摘要"""
        return await self._get(
            "/api/v1/games/rocom/profile/pet-summary",
            self._rocom_headers(fw_token),
        )

    async def get_collection(self, fw_token: str) -> Optional[Dict]:
        """收藏数据"""
        return await self._get(
            "/api/v1/games/rocom/profile/collection",
            self._rocom_headers(fw_token),
        )

    async def get_battle_overview(self, fw_token: str) -> Optional[Dict]:
        """对战总览"""
        return await self._get(
            "/api/v1/games/rocom/profile/battle-overview",
            self._rocom_headers(fw_token),
        )

    async def get_battle_list(
        self,
        fw_token: str,
        page_size: int = 4,
        after_time: str = "",
    ) -> Optional[Dict]:
        """对战记录列表"""
        params: Dict[str, Any] = {"page_size": page_size}
        if after_time:
            params["after_time"] = after_time
        return await self._get(
            "/api/v1/games/rocom/battle/list",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_pets(
        self,
        fw_token: str,
        pet_subset: int = 0,
        page_no: int = 1,
        page_size: int = 10,
    ) -> Optional[Dict]:
        """精灵列表"""
        params = {
            "pet_subset": pet_subset,
            "page_no": page_no,
            "page_size": page_size,
        }
        return await self._get(
            "/api/v1/games/rocom/battle/pets",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
