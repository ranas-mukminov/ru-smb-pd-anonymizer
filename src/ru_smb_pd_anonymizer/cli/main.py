from __future__ import annotations

import typer

from .commands.apply_policy import apply_policy_cmd
from .commands.inspect_schema import inspect_schema_cmd
from .commands.profile_dataset import profile_dataset_cmd
from .commands.suggest_policy import suggest_policy_cmd
from .commands.validate_policy import validate_policy_cmd

app = typer.Typer(help="ru-smb-pd-anonymizer CLI")


app.command("inspect-schema")(inspect_schema_cmd)
app.command("suggest-policy")(suggest_policy_cmd)
app.command("apply-policy")(apply_policy_cmd)
app.command("validate-policy")(validate_policy_cmd)
app.command("profile-dataset")(profile_dataset_cmd)


if __name__ == "__main__":
    app()
