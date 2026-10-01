def diagnose_workflow(workflow_data: dict):
    issues = []

    steps = workflow_data.get("steps", [])

    # Workflow must contain steps
    if not steps:
        issues.append({
            "type": "workflow_error",
            "message": "Workflow has no steps",
            "severity": "high",
        })

        return {
            "healthy": False,
            "issue_count": len(issues),
            "issues": issues,
        }

    for step in steps:
        step_type = step.get("type")
        config = step.get("config", {})

        # -------------------------
        # TRIGGER VALIDATION
        # -------------------------

        if step_type == "trigger":

            if not config.get("method"):
                issues.append({
                    "step": step.get("id"),
                    "type": "configuration_error",
                    "message": "Trigger method is missing",
                    "severity": "high",
                })

            if not config.get("path"):
                issues.append({
                    "step": step.get("id"),
                    "type": "configuration_error",
                    "message": "Trigger path is missing",
                    "severity": "high",
                })

        # -------------------------
        # VALIDATION STEP
        # -------------------------

        if step_type == "validation":

            if not config.get("required_fields"):
                issues.append({
                    "step": step.get("id"),
                    "type": "configuration_error",
                    "message": "Validation required_fields are missing",
                    "severity": "medium",
                })

        # -------------------------
        # DATABASE STEP
        # -------------------------

        if step_type == "database":

            if not config.get("operation"):
                issues.append({
                    "step": step.get("id"),
                    "type": "configuration_error",
                    "message": "Database operation is missing",
                    "severity": "high",
                })

            if not config.get("table"):
                issues.append({
                    "step": step.get("id"),
                    "type": "configuration_error",
                    "message": "Database table is missing",
                    "severity": "high",
                })

    return {
        "healthy": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
    }
