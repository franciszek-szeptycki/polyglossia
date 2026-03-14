from dataclasses import dataclass

from tenants.consts import Language

@dataclass(frozen=True)
class TenantDTO:
    id: int
    user_id: int
    language: Language
