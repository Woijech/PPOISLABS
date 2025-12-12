from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set

@dataclass(frozen=True)
class Permission:
    code: str
    description: str = ""
    priority: int = 0
    
    def is_higher_priority_than(self, other: "Permission") -> bool:
        """Check if this permission has higher priority than another"""
        return self.priority > other.priority

@dataclass
class Role:
    name: str
    permissions: Set[Permission] = field(default_factory=set)
    is_active: bool = True
    
    def allows(self, code: str) -> bool:
        return self.is_active and any(p.code == code for p in self.permissions)
    
    def add_permission(self, permission: Permission) -> None:
        """Add a permission to this role"""
        self.permissions.add(permission)
    
    def remove_permission(self, permission: Permission) -> None:
        """Remove a permission from this role"""
        self.permissions.discard(permission)
    
    def deactivate(self) -> None:
        """Deactivate this role"""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate this role"""
        self.is_active = True

@dataclass
class Department:
    name: str
    cost_center: str
    budget: int = 0
    head_id: str = ""
    
    def allocate_budget(self, amount: int) -> None:
        """Allocate budget to department"""
        self.budget += amount
    
    def spend_budget(self, amount: int) -> bool:
        """Spend budget from department. Returns True if successful"""
        if amount <= self.budget:
            self.budget -= amount
            return True
        return False
    
    def get_remaining_budget(self) -> int:
        """Get remaining budget"""
        return self.budget

@dataclass
class AccessPolicy:
    allowed_roles: Set[str] = field(default_factory=set)
    denied_roles: Set[str] = field(default_factory=set)
    
    def can_access(self, roles: List[Role]) -> bool:
        has_denied = any(r.name in self.denied_roles for r in roles)
        if has_denied:
            return False
        return any(r.name in self.allowed_roles for r in roles)
    
    def allow_role(self, role_name: str) -> None:
        """Allow a role in this policy"""
        self.allowed_roles.add(role_name)
    
    def deny_role(self, role_name: str) -> None:
        """Deny a role in this policy"""
        self.denied_roles.add(role_name)

@dataclass
class Organization:
    name: str
    inn: str
    address: str = ""
    phone: str = ""
    email: str = ""
    
    def update_contact_info(self, phone: str = "", email: str = "") -> None:
        """Update organization contact information"""
        if phone:
            self.phone = phone
        if email:
            self.email = email
    
    def validate_inn(self) -> bool:
        """Validate INN (Tax Identification Number)"""
        return len(self.inn) in (10, 12) and self.inn.isdigit()

@dataclass
class User:
    id: str
    login: str
    display_name: str
    is_blocked: bool = False
    roles: List[Role] = field(default_factory=list)
    department: Department | None = None
    org: Organization | None = None
    email: str = ""
    phone: str = ""
    
    def has_permission(self, code: str) -> bool:
        return not self.is_blocked and any(r.allows(code) for r in self.roles)
    
    def assign_role(self, role: Role) -> None:
        if role not in self.roles:
            self.roles.append(role)
    
    def remove_role(self, role: Role) -> None:
        """Remove a role from user"""
        if role in self.roles:
            self.roles.remove(role)
    
    def block(self) -> None:
        """Block user access"""
        self.is_blocked = True
    
    def unblock(self) -> None:
        """Unblock user access"""
        self.is_blocked = False
    
    def change_department(self, department: Department) -> None:
        """Change user's department"""
        self.department = department
    
    def get_active_roles(self) -> List[Role]:
        """Get list of active roles"""
        return [r for r in self.roles if r.is_active]


# Role-based user classes for clarity
@dataclass
class Admin(User):
    """Administrator with full system access"""
    
    def __post_init__(self):
        # Call parent initialization if exists
        if hasattr(super(), '__post_init__'):
            super().__post_init__()
        # Ensure admin has all permissions
        admin_role = Role(
            name="ADMIN",
            permissions={
                Permission("CREATE_DOCUMENT", "Create documents"),
                Permission("EDIT_DOCUMENT", "Edit documents"),
                Permission("DELETE_DOCUMENT", "Delete documents"),
                Permission("APPROVE_DOCUMENT", "Approve documents"),
                Permission("MANAGE_USERS", "Manage users"),
                Permission("MANAGE_ROLES", "Manage roles"),
                Permission("VIEW_AUDIT_LOG", "View audit logs"),
                Permission("MANAGE_SYSTEM", "Manage system settings"),
            }
        )
        if admin_role not in self.roles:
            self.roles.append(admin_role)
    
    def manage_user(self, user: User, action: str) -> bool:
        """Manage user (block, unblock, change roles)"""
        if action == "block":
            user.block()
            return True
        elif action == "unblock":
            user.unblock()
            return True
        return False


@dataclass
class Manager(User):
    """Manager with document approval and team management permissions"""
    
    def __post_init__(self):
        if hasattr(super(), '__post_init__'):
            super().__post_init__()
        manager_role = Role(
            name="MANAGER",
            permissions={
                Permission("CREATE_DOCUMENT", "Create documents"),
                Permission("EDIT_DOCUMENT", "Edit documents"),
                Permission("APPROVE_DOCUMENT", "Approve documents"),
                Permission("VIEW_TEAM_DOCS", "View team documents"),
                Permission("MANAGE_TEAM_BUDGET", "Manage team budget"),
            }
        )
        if manager_role not in self.roles:
            self.roles.append(manager_role)
    
    def approve_document(self, doc) -> bool:
        """Approve a document if manager has permission"""
        if self.has_permission("APPROVE_DOCUMENT"):
            doc.approve()
            return True
        return False
    
    def allocate_team_budget(self, amount: int) -> bool:
        """Allocate budget to the manager's department"""
        if self.department and self.has_permission("MANAGE_TEAM_BUDGET"):
            self.department.allocate_budget(amount)
            return True
        return False


@dataclass
class Accountant(User):
    """Accountant with financial document and payment permissions"""
    
    def __post_init__(self):
        if hasattr(super(), '__post_init__'):
            super().__post_init__()
        accountant_role = Role(
            name="ACCOUNTANT",
            permissions={
                Permission("CREATE_INVOICE", "Create invoices"),
                Permission("VIEW_PAYMENTS", "View payments"),
                Permission("PROCESS_PAYMENT", "Process payments"),
                Permission("VIEW_FINANCIAL_DOCS", "View financial documents"),
                Permission("AUDIT_TRANSACTIONS", "Audit transactions"),
            }
        )
        if accountant_role not in self.roles:
            self.roles.append(accountant_role)
    
    def process_invoice(self, invoice) -> bool:
        """Process an invoice if accountant has permission"""
        if self.has_permission("PROCESS_PAYMENT") and hasattr(invoice, 'mark_paid'):
            invoice.mark_paid()
            return True
        return False
    
    def audit_account(self, account) -> dict:
        """Audit an account and return audit report"""
        if self.has_permission("AUDIT_TRANSACTIONS"):
            return {
                "account": account.number if hasattr(account, 'number') else str(account),
                "auditor": self.display_name,
                "status": "audited"
            }
        return {}


@dataclass
class RegularUser(User):
    """Regular user with basic document operations"""
    
    def __post_init__(self):
        if hasattr(super(), '__post_init__'):
            super().__post_init__()
        user_role = Role(
            name="USER",
            permissions={
                Permission("CREATE_DOCUMENT", "Create documents"),
                Permission("EDIT_OWN_DOCUMENT", "Edit own documents"),
                Permission("VIEW_DOCUMENT", "View documents"),
            }
        )
        if user_role not in self.roles:
            self.roles.append(user_role)
    
    def can_edit_document(self, doc) -> bool:
        """Check if user can edit a document (only own documents)"""
        if hasattr(doc, 'author'):
            return self.has_permission("EDIT_OWN_DOCUMENT") and doc.author.id == self.id
        return False


@dataclass
class Guest(User):
    """Guest user with read-only access"""
    
    def __post_init__(self):
        if hasattr(super(), '__post_init__'):
            super().__post_init__()
        guest_role = Role(
            name="GUEST",
            permissions={
                Permission("VIEW_DOCUMENT", "View documents"),
            }
        )
        if guest_role not in self.roles:
            self.roles.append(guest_role)
    
    def can_only_view(self) -> bool:
        """Guest can only view documents"""
        return True
