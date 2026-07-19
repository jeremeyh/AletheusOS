from .metric_registry import MetricRegistry

def markdown(registry: MetricRegistry)->str:
    lines=["# SPAN Metrics",""]
    for m in registry.all():
        lines.append(f"- {m.category}: {m.subject}.{m.name} = {m.value}{m.unit}")
    return "\n".join(lines)
