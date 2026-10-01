from app.workflow.workflow_schema import Workflow


sample_workflow = Workflow(
    id="workflow-001",
    name="Employee Data Workflow",
    steps=[
        {
            "id": "step-1",
            "name": "Receive Employee Data",
            "type": "trigger",
            "config": {
                "method": "POST",
                "path": "/employees",
            },
        },
        {
            "id": "step-2",
            "name": "Validate Employee",
            "type": "validation",
            "config": {
                "required_fields": [
                    "name",
                    "email",
                    "department",
                ],
            },
        },
        {
            "id": "step-3",
            "name": "Save Employee",
            "type": "database",
            "config": {
                "operation": "insert",
                "table": "employees",
            },
        },
    ],
)
