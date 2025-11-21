import pandas as pd

from ru_smb_pd_anonymizer.transforms.snils import SnilsHashingTransformer, SnilsMaskingTransformer


def test_snils_masking():
    tf = SnilsMaskingTransformer(keep=2)
    value = "123-456-789 12"
    masked = tf.transform(pd.Series([value])).iloc[0]
    assert masked.endswith("12")
    assert masked != value


def test_snils_hashing():
    tf = SnilsHashingTransformer(salt="demo")
    value = "123-456-789 12"
    hashed = tf.transform(pd.Series([value])).iloc[0]
    assert len(hashed) == 64
    assert hashed != value
