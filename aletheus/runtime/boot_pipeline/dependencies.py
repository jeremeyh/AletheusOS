BOOT_DEPENDENCIES = {

    "RuntimeStateBootPhase": [],

    "RuntimeCommandBootstrapPhase": [
        "RuntimeStateBootPhase",
    ],

    "RuntimeServiceRegistrationPhase": [
        "RuntimeCommandBootstrapPhase",
    ],

    "RuntimeSchedulerBootPhase": [
        "RuntimeServiceRegistrationPhase",
    ],

    "RuntimeApplicationBootPhase": [
        "RuntimeSchedulerBootPhase",
    ],

    "RuntimeAgentBootPhase": [
        "RuntimeApplicationBootPhase",
    ],

    "RuntimeMemoryInitializationPhase": [
        "RuntimeAgentBootPhase",
    ],
}
