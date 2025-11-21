from pathlib import Path

from ru_smb_pd_anonymizer.policies.model import Policy


def test_load_and_dump_policy(tmp_path: Path):
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(
        """
name: test
use_case: analytics
description: test policy
fields:
  - field_pattern: semantic:FIO
    level: PSEUDONYMIZED_ONE_WAY
    transformer: fio.FioMaskingTransformer
""",
        encoding="utf-8",
    )
    policy = Policy.from_yaml(str(policy_path))
    assert policy.name == "test"
    assert policy.fields[0].transformer == "fio.FioMaskingTransformer"
    out_path = tmp_path / "out.yaml"
    policy.to_yaml(out_path)
    assert out_path.exists()
