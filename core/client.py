"""
WeGame + Rocom HTTP API 客户端

基于单一 API Key 模型：
- 每个开发者仅维护 1 个 WeGame API Key
- 该 Key 统一用于 WeGame 登录层与具体游戏接口 (如 game:rocom)
- session 管理接口依据 X-API-Key + X-User-Identifier 进行身份校验
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

    def _wegame_headers(
        self, fw_token: str = "", user_identifier: str = ""
    ) -> Dict[str, str]:
        """登录/账号管理接口的请求头 (scope=wegame)"""
        headers = {}
        if self.wegame_api_key:
            headers["X-API-Key"] = self.wegame_api_key
        
        if fw_token:
            headers["X-Framework-Token"] = fw_token
        if user_identifier:
            headers["X-User-Identifier"] = self._sanitize_uid(user_identifier)
        return headers

    def _sanitize_uid(self, uid: str) -> str:
        """参考 Go 端的 SanitizeStrictInput 逻辑"""
        import re
        if not uid: return ""
        uid = str(uid).strip()
        # 注意：服务器端 Go 逻辑允许字母、数字以及中日韩字符。
        cleaned = re.sub(r'[^a-zA-Z0-9_\- \u4e00-\u9fa5]', '', uid)
        return cleaned.strip()

    def _rocom_headers(self, fw_token: str) -> Dict[str, str]:
        """游戏数据查询接口的请求头 (scope=game:rocom)"""
        headers = {
            "X-Framework-Token": fw_token
        }
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

    async def qq_qr_login(
        self, user_identifier: str = ""
    ) -> Optional[Dict]:
        """发起 QQ 扫码登录，返回 frameworkToken + qr_image (base64)"""
        params = {"client_type": "bot", "client_id": "astrbot"}
        if user_identifier:
            params["user_identifier"] = self._sanitize_uid(user_identifier)
        return await self._get(
            "/api/v1/login/wegame/qr",
            self._wegame_headers(user_identifier=user_identifier),
            params=params,
        )

    async def qq_qr_status(
        self, fw_token: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """轮询 QQ 扫码状态"""
        params = {}
        if user_identifier:
            params["user_identifier"] = self._sanitize_uid(user_identifier)
        return await self._get(
            "/api/v1/login/wegame/status",
            self._wegame_headers(
                fw_token, user_identifier=user_identifier
            ),
            params=params,
        )

    async def wechat_qr_login(
        self, user_identifier: str = ""
    ) -> Optional[Dict]:
        """发起微信扫码登录，返回 frameworkToken + qr_image (URL)"""
        params = {"client_type": "bot", "client_id": "astrbot"}
        if user_identifier:
            params["user_identifier"] = self._sanitize_uid(user_identifier)
        return await self._get(
            "/api/v1/login/wegame/wechat/qr",
            self._wegame_headers(user_identifier=user_identifier),
            params=params,
        )

    async def wechat_qr_status(
        self, fw_token: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """轮询微信扫码状态"""
        params = {}
        if user_identifier:
            params["user_identifier"] = self._sanitize_uid(user_identifier)
        return await self._get(
            "/api/v1/login/wegame/wechat/status",
            self._wegame_headers(
                fw_token, user_identifier=user_identifier
            ),
            params=params,
        )

    async def get_qq_token(
        self, fw_token: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """查询 QQ 扫码凭证"""
        user_identifier = self._sanitize_uid(user_identifier)
        params = {}
        if user_identifier:
            params["user_identifier"] = user_identifier
        return await self._get(
            "/api/v1/login/wegame/token",
            self._wegame_headers(fw_token, user_identifier),
            params=params,
        )

    async def get_wechat_token(
        self, fw_token: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """查询微信扫码凭证"""
        user_identifier = self._sanitize_uid(user_identifier)
        params = {}
        if user_identifier:
            params["user_identifier"] = user_identifier
        return await self._get(
            "/api/v1/login/wegame/wechat/token",
            self._wegame_headers(fw_token, user_identifier),
            params=params,
        )

    async def import_token(
        self, tgp_id: str, tgp_ticket: str, user_identifier: str = ""
    ) -> Optional[Dict]:
        """导入 tgp_id + tgp_ticket 凭证"""
        user_identifier = self._sanitize_uid(user_identifier)
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
            self._wegame_headers(user_identifier=user_identifier),
            json_data=body,
        )

    async def create_binding(
        self, fw_token: str, user_identifier: str
    ) -> Optional[Dict]:
        """将匿名创建的 frameworkToken 通过 API Key 绑定给用户，从而获得持久授权"""
        user_identifier = self._sanitize_uid(user_identifier)
        payload = {
            "framework_token": fw_token,
            "user_identifier": user_identifier,
            "client_type": "bot",
            "client_id": "astrbot",
        }
        return await self._post(
            "/api/v1/user/bindings",
            # 这里必须带 API Key
            self._wegame_headers(user_identifier=user_identifier),
            json_data=payload,
        )

    async def delete_binding(
        self, binding_id: str, user_identifier: str
    ) -> bool:
        """删除绑定记录"""
        headers = self._wegame_headers(user_identifier=user_identifier)
        res = await self._delete(
            f"/api/v1/user/bindings/{binding_id}",
            headers
        )
        return res is not None

    # ─── 洛克王国游戏数据 ───

    async def get_role(
        self, fw_token: str, account_type: int = None
    ) -> Optional[Dict]:
        """角色资料"""
        params = {}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/profile/role",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_evaluation(
        self, fw_token: str, account_type: int = None
    ) -> Optional[Dict]:
        """AI 维度评价"""
        params = {}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/profile/evaluation",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_pet_summary(
        self, fw_token: str, account_type: int = None
    ) -> Optional[Dict]:
        """精灵摘要"""
        params = {}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/profile/pet-summary",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_collection(
        self, fw_token: str, account_type: int = None
    ) -> Optional[Dict]:
        """收藏数据"""
        params = {}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/profile/collection",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_battle_overview(
        self, fw_token: str, account_type: int = None
    ) -> Optional[Dict]:
        """对战总览"""
        params = {}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/profile/battle-overview",
            self._rocom_headers(fw_token),
            params=params,
        )

    async def get_battle_list(
        self,
        fw_token: str,
        page_size: int = 4,
        after_time: str = "",
        zone: int = None,
    ) -> Optional[Dict]:
        """对战记录列表"""
        params: Dict[str, Any] = {"page_size": page_size}
        if after_time:
            params["after_time"] = after_time
        if zone is not None:
            params["zone"] = zone
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
        zone: int = None,
    ) -> Optional[Dict]:
        """精灵列表"""
        params = {
            "pet_subset": pet_subset,
            "page_no": page_no,
            "page_size": page_size,
        }
        if zone is not None:
            params["zone"] = zone
        return await self._get(
            "/api/v1/games/rocom/battle/pets",
            self._rocom_headers(fw_token),
            params,
        )

    async def get_lineup_list(
        self,
        fw_token: str,
        page_no: int = 1,
        category: str = "",
        account_type: int = None,
    ) -> Optional[Dict]:
        """查询阵容助手列表"""
        params = {"page_no": page_no}
        if category:
            params["category"] = category
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/lineup/list",
            self._rocom_headers(fw_token),
            params,
        )

    async def get_exchange_posters(
        self,
        fw_token: str,
        page_no: int = 1,
        refresh: bool = False,
        account_type: int = None,
    ) -> Optional[Dict]:
        """查询交换大厅海报列表"""
        params = {"page_no": page_no, "refresh": "true" if refresh else "false"}
        if account_type:
            params["account_type"] = account_type
        return await self._get(
            "/api/v1/games/rocom/exchange/posters",
            self._rocom_headers(fw_token),
            params,
        )

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
