from app.workflow.workflow_schema import Workflow


def inspect_workflow(workflow: Workflow):
    return {
        "workflow_id": workflow.id,
        "workflow_name": workflow.name,
        "step_count": len(workflow.steps),
        "steps": [
            {
                "id": step.id,
                "name": step.name,
                "type": step.type,
                "config": step.config,
            }
            for step in workflow.steps
        ],
    }
