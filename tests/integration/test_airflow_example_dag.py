import importlib


def test_import_airflow_example():
    module = importlib.import_module("examples.airflow.dag_anonymize_crm")
    assert hasattr(module, "anonymize")
