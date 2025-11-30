import pandas as pd

from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields
from ru_smb_pd_anonymizer.dtypes.models import DatasetSchema, FieldInfo, SemanticType
from ru_smb_pd_anonymizer.pipeline.core import apply_policy_to_dataframe
from ru_smb_pd_anonymizer.policies.model import AnonymizationLevel, FieldPolicy, Policy


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


def test_apply_policy_dataframe_report():
    df = pd.DataFrame(
        {
            "inn": ["7701234567"],
            "fio": ["Иванов Иван"],
            "email": ["ivanov@example.com"],
        }
    )
    schema = DatasetSchema(
        fields=[
            FieldInfo(
                name="inn",
                physical_type="string",
                semantic_type=SemanticType.INN,
                is_personal_data=True,
            ),
            FieldInfo(
                name="fio",
                physical_type="string",
                semantic_type=SemanticType.FIO,
                is_personal_data=True,
            ),
            FieldInfo(
                name="email",
                physical_type="string",
                semantic_type=SemanticType.EMAIL,
                is_personal_data=True,
            ),
        ]
    )
    policy = Policy(
        name="demo",
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
    anonymized, report = apply_policy_to_dataframe(df, schema, policy, return_report=True)
    assert anonymized["inn"].iloc[0].endswith("67")
    assert report.policy_name == "demo"
    assert report.rows_processed == len(df)
    assert set(report.columns_anonymized) == {"inn", "fio"}
    assert "email" in report.columns_skipped


def test_resolve_transformer_accepts_fully_qualified_name():
    df = pd.DataFrame({"custom_id": ["123", "456"]})
    schema = DatasetSchema(
        fields=[
            FieldInfo(
                name="custom_id",
                physical_type="string",
                semantic_type=SemanticType.CUSTOM_ID,
                is_personal_data=True,
            )
        ]
    )
    policy = Policy(
        name="fullpath",
        description="",
        use_case="analytics",
        fields=[
            FieldPolicy(
                field_pattern="semantic:CustomID",
                level=AnonymizationLevel.PSEUDONYMIZED_ONE_WAY,
                transformer="ru_smb_pd_anonymizer.transforms.generic_id.GenericIdMaskingTransformer",
                params={"keep": 1},
            )
        ],
    )

    anonymized = apply_policy_to_dataframe(df, schema, policy)
    assert anonymized["custom_id"].iloc[0].endswith("3")
