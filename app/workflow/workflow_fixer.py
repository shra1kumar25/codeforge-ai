def fix_workflow(
    workflow_data: dict,
    issue: dict,
):
    fixed_workflow = workflow_data.copy()

    steps = []

    for step in workflow_data.get("steps", []):
        step_copy = step.copy()
        config = step_copy.get("config", {}).copy()

        issue_type = issue.get("type")
        message = issue.get("message")
        issue_step = issue.get("step")

        # Only modify the step where the issue was detected
        if (
            issue_type == "configuration_error"
            and step_copy.get("id") == issue_step
        ):

            # DATABASE: missing table
            if message == "Database table is missing":
                config["table"] = "employees"

            # DATABASE: missing operation
            elif message == "Database operation is missing":
                config["operation"] = "insert"

            # TRIGGER: missing method
            elif message == "Trigger method is missing":
                config["method"] = "POST"

            # TRIGGER: missing path
            elif message == "Trigger path is missing":
                config["path"] = "/employees"

            # VALIDATION: missing required fields
            elif message == "Validation required_fields are missing":
                config["required_fields"] = [
                    "name",
                    "email",
                    "department",
                ]

        step_copy["config"] = config
        steps.append(step_copy)

    fixed_workflow["steps"] = steps

    return {
        "success": True,
        "workflow": fixed_workflow,
        "message": "Workflow fixed successfully",
    }
