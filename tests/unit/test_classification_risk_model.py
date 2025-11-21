import pandas as pd

from ru_smb_pd_anonymizer.classification.risk_model import score_dataset
from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields


def test_risk_model_scores():
    df = pd.DataFrame(
        {
            "inn": ["7701234567", "7701234567"],
            "city": ["Москва", "Москва"],
        }
    )
    schema = detect_fields(df.columns, df.head().to_dict(orient="records"))
    scores = score_dataset(df, schema)
    assert scores["inn"] == "high"
    assert scores["city"] in {"low", "medium", "high"}
