"""Adaptador de Camunda 8 REST v2. Requiere tareas de usuario Camunda (no job-based legacy)."""
import os, time
import httpx

class CamundaError(Exception):
    pass

class CamundaClient:
    def __init__(self):
        self.base = os.getenv("CAMUNDA_BASE_URL", "http://localhost:8080").rstrip("/")
        self.auth_mode = os.getenv("CAMUNDA_AUTH_MODE", "none").lower()
        self.token = ""
        self.expires = 0.0

    def _token(self):
        if self.auth_mode == "none":
            return None
        if self.auth_mode == "static":
            token = os.getenv("CAMUNDA_TOKEN", "")
            if not token: raise CamundaError("Falta CAMUNDA_TOKEN")
            return token
        if self.auth_mode != "oauth": raise CamundaError("CAMUNDA_AUTH_MODE inválido")
        if time.time() < self.expires and self.token:
            return self.token
        auth_url = os.getenv("CAMUNDA_OAUTH_URL", "")
        if not auth_url: raise CamundaError("Falta CAMUNDA_OAUTH_URL")
        payload = {"grant_type": "client_credentials", "client_id": os.getenv("CAMUNDA_CLIENT_ID", ""),
                   "client_secret": os.getenv("CAMUNDA_CLIENT_SECRET", "")}
        audience = os.getenv("CAMUNDA_OAUTH_AUDIENCE", "")
        if audience: payload["audience"] = audience
        with httpx.Client(timeout=15) as c:
            resp = c.post(auth_url, data=payload); resp.raise_for_status()
        data = resp.json()
        self.token = data["access_token"]
        self.expires = time.time() + max(5, int(data.get("expires_in", 60)) - 20)
        return self.token

    def _request(self, method, path, json=None):
        token = self._token()
        headers = {"Accept": "application/json"}
        if token: headers["Authorization"] = f"Bearer {token}"
        try:
            with httpx.Client(timeout=25) as c:
                r = c.request(method, f"{self.base}/v2/{path.lstrip('/')}", json=json, headers=headers)
                r.raise_for_status()
                return r.json() if r.content else {}
        except httpx.HTTPError as exc:
            raise CamundaError(f"Error de Camunda al llamar {path}: {exc}") from exc

    def health(self): return self._request("GET", "topology")

    def start(self, process_id, variables):
        return self._request("POST", "process-instances", {"processDefinitionId": process_id, "variables": variables})

    def tasks(self, instance_key):
        result = self._request("POST", "user-tasks/search", {"filter": {"processInstanceKey": str(instance_key)}, "page": {"limit": 100}})
        return [x for x in result.get("items", []) if x.get("state") in ("CREATED", "ASSIGNED", "UPDATING")]

    def complete(self, key, variables):
        return self._request("POST", f"user-tasks/{key}/completion", {"variables": variables})

    def status(self, instance_key):
        """Consulta estado de proceso, disponible en REST v2 (eventual consistency)."""
        return self._request("GET", f"process-instances/{instance_key}")
