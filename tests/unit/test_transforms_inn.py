import pandas as pd

from ru_smb_pd_anonymizer.transforms.inn import (
    InnHashingTransformer,
    InnMaskingTransformer,
)


def test_inn_masking():
    tf = InnMaskingTransformer(keep=3)
    value = "7701234567"
    masked = tf.transform(pd.Series([value])).iloc[0]
    assert masked.endswith(value[-3:])
    assert masked != value


def test_inn_hashing_is_deterministic():
    tf = InnHashingTransformer(salt="test")
    series = pd.Series(["7701234567"])
    hashed1 = tf.transform(series).iloc[0]
    hashed2 = tf.transform(series).iloc[0]
    assert hashed1 == hashed2
    assert len(hashed1) == 64
