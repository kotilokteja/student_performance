from . import dashboard, assessment, performance, insights, about  # noqa: F401

REGISTRY = {
    "Dashboard": dashboard.render,
    "Risk Assessment": assessment.render,
    "Model Performance": performance.render,
    "Dataset Insights": insights.render,
    "About": about.render,
}
