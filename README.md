# ru-smb-pd-anonymizer

[![CI](https://github.com/run-as-daemon/ru-smb-pd-anonymizer/actions/workflows/ci.yml/badge.svg)](https://github.com/run-as-daemon/ru-smb-pd-anonymizer/actions/workflows/ci.yml)
[![Security](https://github.com/run-as-daemon/ru-smb-pd-anonymizer/actions/workflows/security.yml/badge.svg)](https://github.com/run-as-daemon/ru-smb-pd-anonymizer/actions/workflows/security.yml)

## English
Framework for anonymization / pseudonymization of Russian personal data before sending datasets to AI/LLM services, outsourcing teams, analytics, or tech support. Provides detectors for Russian-specific identifiers (FIO, passport, INN, SNILS, phone, address, email), reusable transformers (masking, hashing, tokenization, FPE hooks, generalization), policies for common use-cases, and pipeline adapters for pandas, SQLAlchemy, Airflow, dbt, plus an AI stub layer for schema and policy suggestions. License: Apache-2.0. This is a technical toolkit; legal assessment remains with your counsel/compliance.

---

## Русский
Фреймворк для анонимизации/псевдонимизации персональных данных по российским реалиям (ФИО, паспорт, ИНН, СНИЛС, адрес, телефон, e-mail, внутренние идентификаторы) перед передачей:
- в аутсорс-разработку;
- во внешние AI/LLM-сервисы;
- в аналитические и продуктовые команды;
- в техподдержку и подрядчикам.

Для кого: малый и средний бизнес в РФ, in-house data- и ML-команды, интеграторы, компании, которым нужно использовать внешние AI/LLM-сервисы с соблюдением 152-ФЗ/233-ФЗ и требований к обезличиванию.

### Как использовать
```bash
pip install ru-smb-pd-anonymizer

ru-pd-anon inspect-schema --input examples/data/synthetic_crm.csv --format csv --out schema.json
ru-pd-anon suggest-policy --schema schema.json --use-case analytics --out policy.yaml
ru-pd-anon apply-policy \
  --input examples/data/synthetic_crm.csv \
  --format csv \
  --schema schema.json \
  --policy policy.yaml \
  --output examples/data/synthetic_crm_anon.csv
```

### Что внутри
- детекторы российских форматов и эвристики по названиям/значениям;
- политики для аналитики, ML, техподдержки, логов;
- трансформеры: маскирование, токенизация, hashing+salt, generalization, noise, FPE-интерфейс;
- пайплайны для pandas/SQLAlchemy, Airflow-оператор, dbt-макросы;
- AI-стаб: подсказка типов полей и уровней анонимизации без отправки реальных ПДн по умолчанию.

### Профессиональные услуги — run-as-daemon.ru
Проект развивается инженером DevOps/DevSecOps с сайта [run-as-daemon.ru](https://run-as-daemon.ru).
Если вам нужно:
- построить безопасные пайплайны аналитики и ML на основе ПДн;
- подготовиться к использованию внешних LLM/AI-сервисов с учётом 152-ФЗ и работы с обезличенными данными;
- выстроить анонимизацию/псевдонимизацию как код,

можно заказать консалтинг, внедрение и поддержку под вашу инфраструктуру.

### Оговорки
- фреймворк не гарантирует юридически достаточную анонимизацию;
- ответственность за законность обработки, передачу, локализацию ПДн несёт оператор/клиент;
- примеры датасетов — синтетические, без реальных ПДн;
- «анонимизация» требует отдельной правовой оценки, особенно для обратимых стратегий.
