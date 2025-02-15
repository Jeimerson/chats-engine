from chats.apps.api.v1.internal.eda_clients.flows_eda_client import FlowsEDAClient
from chats.apps.projects.models import Project, ProjectPermission, TemplateType
from chats.apps.queues.models import QueueAuthorization
from chats.apps.sectors.models import SectorAuthorization


class SectorSetupHandlerUseCase:
    def __init__(self):
        self._flows_client = FlowsEDAClient()

    def setup_sectors_in_project(
        self,
        project: Project,
        template_type: TemplateType,
        creator_permission: ProjectPermission,
    ):
        setup = template_type.setup

        for setup_sector in setup.get("sectors", {}):
            setup_queues = setup_sector.pop("queues", None)

            if not setup_queues:
                continue

            sector, created = project.sectors.get_or_create(
                name=setup_sector.pop("name"), defaults=setup_sector
            )
            if not created:
                continue

            SectorAuthorization.objects.create(
                role=1, permission=creator_permission, sector=sector
            )
            content = {
                "project_uuid": str(project.uuid),
                "name": sector.name,
                "project_auth": str(creator_permission.pk),
                "user_email": str(creator_permission.user.email),
                "uuid": str(sector.uuid),
                "queues": [],
            }

            for setup_queue in setup_queues:
                queue = sector.queues.get_or_create(
                    name=setup_queue.pop("name"), defaults=setup_queue
                )[0]
                QueueAuthorization.objects.create(
                    role=1, permission=creator_permission, queue=queue
                )
                content["queues"].append({"uuid": str(queue.uuid), "name": queue.name})

            self._flows_client.request_ticketer(content=content)
