from pathlib import Path

from typer.testing import CliRunner

from ru_smb_pd_anonymizer.cli.main import app

runner = CliRunner()


def test_inspect_and_apply(tmp_path: Path):
    data_path = Path("examples/data/synthetic_crm.csv")
    schema_path = tmp_path / "schema.json"
    result = runner.invoke(
        app,
        ["inspect-schema", "--input", str(data_path), "--format", "csv", "--out", str(schema_path)],
    )
    assert result.exit_code == 0
    policy_path = Path("examples/configs/policy_analytics.yaml")
    output_path = tmp_path / "out.csv"
    result = runner.invoke(
        app,
        [
          "apply-policy",
          "--input",
          str(data_path),
          "--format",
          "csv",
          "--schema",
          str(schema_path),
          "--policy",
          str(policy_path),
          "--output",
          str(output_path),
        ],
    )
    assert result.exit_code == 0
    assert output_path.exists()
