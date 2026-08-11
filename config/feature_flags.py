FEATURE_FLAGS = {
    "enable_alpha_2_3_health_dashboard": True,
    "enable_provider_registry": True,
    "enable_structured_logging": True,
    "enable_result_cache": True,
    "enable_engine_cleanup_checks": True,
    "enable_scheduler": True,
    "enable_commercialization_layer": True,
}


def is_enabled(flag_name: str) -> bool:
    return bool(FEATURE_FLAGS.get(flag_name, False))
