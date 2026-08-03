from ..ceie_core.engine import Engine as CEIE
from ..constitutional_isolation.engine import Engine as Isolation
from ..founder_observatory.engine import Engine as Observatory
from ..models import ExperienceView


class Engine:
    def render(self, signal, context):
        return {
            "view": context.view.value,
            "projection": CEIE().project(signal, context),
            "founder_surface_available": context.view is ExperienceView.FOUNDER
            and Isolation()
            .authorize(context.view, "platform_omniscience", True)
            .allowed,
        }

    def founder_snapshot(self, events, context, root_attested):
        return Observatory().summarize(
            events, view=context.view, root_attested=root_attested
        )
