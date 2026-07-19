from aletheus.runtime import RuntimeContext, runtime_core
from aletheus.runtime.context import RuntimeContext as ContextFromModule
from aletheus.runtime.core import runtime_core as CoreRuntime


def test_runtime_singleton_is_canonical():
    assert runtime_core is CoreRuntime


def test_runtime_context_has_one_canonical_definition():
    assert RuntimeContext is ContextFromModule
