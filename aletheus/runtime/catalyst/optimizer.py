from .models import CatalystRecommendation, CatalystReport


class CatalystOptimizer:
    """
    Catalyst™

    Runtime optimization layer for reducing friction across mesh routing,
    relay delivery, startup paths, and platform execution.

    Catalyst does not own routing. The mesh routes.
    Catalyst recommends and prepares optimizations.
    """

    def analyze_mesh(self, mesh):
        health = mesh.health()
        recommendations = []
        optimized_routes = []

        if health.get("nodes", 0) == 0:
            recommendations.append(
                CatalystRecommendation(
                    target="service_mesh",
                    recommendation="Register runtime nodes before optimization.",
                    impact="high",
                )
            )

        if health.get("handlers", 0) < health.get("nodes", 0):
            recommendations.append(
                CatalystRecommendation(
                    target="service_mesh",
                    recommendation="Some mesh nodes have no handlers. Add handlers or mark nodes as passive.",
                    impact="medium",
                    metadata={
                        "nodes": health.get("nodes", 0),
                        "handlers": health.get("handlers", 0),
                    },
                )
            )

        for route in health.get("node_names", []):
            optimized_routes.append(route)

        status = "optimized" if not recommendations else "review"

        return CatalystReport(
            status=status,
            recommendations=recommendations,
            optimized_routes=optimized_routes,
        )

    def warm_route(self, route_name: str):
        return CatalystRecommendation(
            target=route_name,
            recommendation=f"Route '{route_name}' warmed for faster access.",
            impact="low",
        )

    def health(self):
        return {
            "status": "online",
            "role": "runtime_optimization",
        }
