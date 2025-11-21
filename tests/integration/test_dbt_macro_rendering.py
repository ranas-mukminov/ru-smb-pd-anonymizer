from pathlib import Path


def test_dbt_macros_exist():
    macros_path = Path("src/ru_smb_pd_anonymizer/pipeline/dbt_macros.sql")
    content = macros_path.read_text(encoding="utf-8")
    assert "pd_hash" in content
    assert "pd_mask_tail" in content
