import pandas as pd

from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields
from ru_smb_pd_anonymizer.policies.model import AnonymizationLevel, FieldPolicy, Policy
from ru_smb_pd_anonymizer.pipeline.core import apply_policy_to_dataframe


def test_apply_policy_dataframe():
    df = pd.DataFrame(
        {
            "inn": ["7701234567", "540234567890"],
            "fio": ["Иванов Иван", "Петров Петр"],
        }
    )
    schema = detect_fields(df.columns, df.head(5).to_dict(orient="records"))
    policy = Policy(
        name="test",
        description="",
        use_case="analytics",
        fields=[
            FieldPolicy(
                field_pattern="semantic:INN",
                level=AnonymizationLevel.PSEUDONYMIZED_ONE_WAY,
                transformer="inn.InnMaskingTransformer",
                params={"keep": 2},
            ),
            FieldPolicy(
                field_pattern="semantic:FIO",
                level=AnonymizationLevel.ANONYMIZED_IRREVERSIBLE,
                transformer="fio.FioMaskingTransformer",
                params={},
            ),
        ],
    )
    anonymized = apply_policy_to_dataframe(df, schema, policy)
    assert anonymized["inn"].iloc[0].endswith("67")
    assert anonymized["fio"].iloc[0].startswith("Иванов")
