from aletheus.runtime import runtime_core


def test_workspace_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Founder Workspace" in diagnostics["services"]


def test_workspace_overview():
    result = runtime_core.commands.dispatch("workspace.overview")
    assert not result.errors
    assert "workspace" in result.results


def test_objective_create_and_list():
    created = runtime_core.commands.dispatch(
        "objective.create",
        {
            "title": "Test Objective",
            "description": "Validate Founder Workspace objective creation.",
            "priority": "high",
            "application": "tests",
        },
    )

    assert not created.errors
    assert "objective" in created.results

    listed = runtime_core.commands.dispatch("objective.list", {})
    assert len(listed.results["objectives"]) >= 1


def test_founder_journal():
    created = runtime_core.commands.dispatch(
        "founder.journal.create",
        {
            "title": "Test Journal",
            "body": "Founder Workspace journal test.",
            "category": "test",
            "tags": ["test", "workspace"],
        },
    )

    assert not created.errors
    assert "journal_entry" in created.results

    listed = runtime_core.commands.dispatch("founder.journal.list", {})
    assert len(listed.results["journal"]) >= 1


def test_notification_create_and_list():
    created = runtime_core.commands.dispatch(
        "notification.create",
        {
            "title": "Test Notification",
            "message": "Workspace notification test.",
            "severity": "info",
        },
    )

    assert not created.errors
    assert "notification" in created.results

    listed = runtime_core.commands.dispatch("notification.list", {})
    assert len(listed.results["notifications"]) >= 1


if __name__ == "__main__":
    test_workspace_service_registered()
    test_workspace_overview()
    test_objective_create_and_list()
    test_founder_journal()
    test_notification_create_and_list()
    print("Aletheus Genesis 0.8 Founder Workspace tests passed.")
