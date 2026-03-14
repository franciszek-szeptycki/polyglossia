from tenants.domain.entities import TenantDTO
from tenants.infrastructure.models import Tenant


class TenantRepository:
    def get_by_user_id(self, user_id) -> TenantDTO:
        tenant = Tenant.objects.get(pk=user_id)  # pyright: ignore[reportAttributeAccessIssue]
        return self._to_dto(tenant)

    def _to_dto(self, tenant: Tenant) -> TenantDTO:
        return TenantDTO(
            id=tenant.id,  # pyright: ignore[reportAttributeAccessIssue]
            user_id=tenant.user_id,  # pyright: ignore[reportAttributeAccessIssue]
            language=tenant.language,  # pyright: ignore[reportArgumentType]
        )

tenant_repository = TenantRepository()
