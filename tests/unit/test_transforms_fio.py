import pandas as pd

from ru_smb_pd_anonymizer.transforms.fio import (
    FioMaskingTransformer,
    FioTokenizationTransformer,
)


def test_fio_masking():
    tf = FioMaskingTransformer()
    series = pd.Series(["Иванов Иван Иванович"])
    result = tf.transform(series)
    assert "Иванов I.I." in result.iloc[0]


def test_fio_tokenization_inverse():
    tf = FioTokenizationTransformer()
    series = pd.Series(["Иванов Иван", "Петров Петр"])
    tf.fit(series)
    tokens = tf.transform(series)
    assert tokens.iloc[0] != series.iloc[0]
    restored = tf.inverse(tokens)
    assert list(restored) == list(series.astype(str))
