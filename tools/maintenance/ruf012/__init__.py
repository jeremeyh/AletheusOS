"""Genesis 11 RUF012 transformation framework."""

from .models import RewriteFailure, RewritePreview, RewriteStatistics
from .registry import TransformationRegistry
from .rewriter import CandidateRewriter, RewriteError
from .transactions import DryRunTransaction, TransactionResult
from .validator import SourceValidator, ValidationResult

__all__ = [
    "CandidateRewriter",
    "DryRunTransaction",
    "RewriteError",
    "RewriteFailure",
    "RewritePreview",
    "RewriteStatistics",
    "SourceValidator",
    "TransactionResult",
    "TransformationRegistry",
    "ValidationResult",
]
