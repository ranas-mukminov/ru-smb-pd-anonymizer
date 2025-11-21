import pandas as pd

from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields
from ru_smb_pd_anonymizer.pipeline.core import apply_policy_to_dataframe
from ru_smb_pd_anonymizer.policies.model import Policy


def test_full_flow_csv_to_csv(tmp_path):
    input_path = "examples/data/synthetic_crm.csv"
    df = pd.read_csv(input_path)
    schema = detect_fields(df.columns, df.head(10).to_dict(orient="records"))
    policy = Policy.from_yaml("src/ru_smb_pd_anonymizer/policies/builtin/analytics.yaml")
    anonymized = apply_policy_to_dataframe(df, schema, policy)
    output_path = tmp_path / "crm_anon.csv"
    anonymized.to_csv(output_path, index=False)
    assert output_path.exists()
    assert anonymized["fio"].iloc[0] != df["fio"].iloc[0]
