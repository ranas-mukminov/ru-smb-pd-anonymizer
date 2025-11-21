import pandas as pd

from ru_smb_pd_anonymizer.transforms.passport import (
    PassportMaskingTransformer,
    PassportTokenizationTransformer,
)


def test_passport_masking_tail():
    tf = PassportMaskingTransformer(keep=2)
    series = pd.Series(["1234 567890"])
    masked = tf.transform(series).iloc[0]
    assert masked.endswith("90")
    assert "*" in masked


def test_passport_tokenization_inverse():
    tf = PassportTokenizationTransformer()
    series = pd.Series(["1234 567890", "4321 098765"])
    tf.fit(series)
    tokens = tf.transform(series)
    assert tokens.iloc[0] != series.iloc[0]
    assert list(tf.inverse(tokens)) == list(series.astype(str))
