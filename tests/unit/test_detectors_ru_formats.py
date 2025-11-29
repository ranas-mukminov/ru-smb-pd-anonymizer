
from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields
from ru_smb_pd_anonymizer.dtypes.models import SemanticType


def test_detects_russian_identifiers():
    columns = ["inn", "snils", "passport", "phone", "email", "fio"]
    sample_rows = [
        {
            "inn": "7701234567",
            "snils": "123-456-789 12",
            "passport": "1234 567890",
            "phone": "+7 999 123-45-67",
            "email": "ivanov@example.com",
            "fio": "Иванов Иван",
        }
    ]
    schema = detect_fields(columns, sample_rows)
    mapping = {f.name: f.semantic_type for f in schema.fields}
    assert mapping["inn"] == SemanticType.INN
    assert mapping["snils"] == SemanticType.SNILS
    assert mapping["passport"] == SemanticType.PASSPORT
    assert mapping["phone"] == SemanticType.PHONE
    assert mapping["email"] == SemanticType.EMAIL
    assert mapping["fio"] == SemanticType.FIO


def test_negative_formats():
    columns = ["inn"]
    sample_rows = [{"inn": "12345"}]
    schema = detect_fields(columns, sample_rows)
    assert schema.fields[0].semantic_type != SemanticType.INN
