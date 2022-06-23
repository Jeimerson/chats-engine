from django.db import models
from django.utils.translation import gettext_lazy as _

from chats.core.models import BaseModel


class Sector(BaseModel):
    name = models.CharField(_("name"), max_length=120)
    project = models.ForeignKey(
        "projects.Project", verbose_name=_("sectors"), on_delete=models.CASCADE
    )
    # manager = models.ForeignKey("projects.ProjectPermission", verbose_name=_("sectors"), on_delete=models.CASCADE)
    rooms_limit = models.IntegerField(_("Rooms limit per employee"))
    work_start = models.IntegerField(_("work start"))
    work_end = models.IntegerField(_("work end"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    @property
    def employee_pks(self):
        return list(self.permissions.all().values_list("user__pk", flat="True"))

    @property
    def active_rooms(self):
        return self.rooms.filter(is_active=True)

    @property
    def deativated_rooms(self):
        return self.rooms.filter(is_active=True)

    @property
    def open_active_rooms(self):
        return self.rooms.filter(user__isnull=True, is_active=True)

    @property
    def closed_active_rooms(self):
        return self.rooms.filter(user__isnull=False, is_active=True)

    @property
    def open_deactivated_rooms(self):
        return self.rooms.filter(user__isnull=True, is_active=False)

    @property
    def vacant_deactivated_rooms(self):
        return self.rooms.filter(user__isnull=False, is_active=False)


class SectorPermission(BaseModel):
    ROLE_NOT_SETTED = 0
    ROLE_AGENT = 1
    ROLE_MANAGER = 2

    ROLE_CHOICES = [
        (ROLE_NOT_SETTED, _("not set")),
        (ROLE_AGENT, _("admin")),
        (ROLE_MANAGER, _("manager")),
    ]

    user = models.ForeignKey(
        "accounts.User",
        related_name="sector_permissions",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
    )

    sector = models.ForeignKey(
        Sector,
        related_name="permissions",
        verbose_name=_("Sector"),
        on_delete=models.CASCADE,
    )
    role = models.PositiveIntegerField(
        _("role"), choices=ROLE_CHOICES, default=ROLE_NOT_SETTED
    )

    class Meta:
        verbose_name = _("Project Permission")
        verbose_name_plural = _("Project Permissions")

    def __str__(self):
        return self.name
