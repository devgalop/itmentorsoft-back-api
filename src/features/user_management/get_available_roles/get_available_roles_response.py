from pydantic import BaseModel


class RoleDetail(BaseModel):
    id: str
    name: str
    homologate_name: str


class GetAvailableRolesResponse(BaseModel):
    is_success: bool
    roles: list[RoleDetail]
