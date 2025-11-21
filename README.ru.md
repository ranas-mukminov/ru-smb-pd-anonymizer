# ru-smb-pd-anonymizer (русская версия)

Фреймворк анонимизации/псевдонимизации российских наборов ПДн перед передачей во внешние LLM/AI-сервисы, аутсорс и аналитику. Делает акцент на российские форматы (ФИО, паспорт РФ, ИНН, СНИЛС, телефоны, адреса по ФИАС), политики под типовые задачи и пайплайны для pandas/SQLAlchemy/Airflow/dbt.

## Возможности
- детекторы ПДн/СПДн по названиям и значениям полей;
- трансформеры: маскирование, токенизация, hashing+salt, форматосохраняющее шифрование (интерфейс), generalization, noise, suppression;
- политики под use-case: аналитика, ML/LLM, техподдержка, логи;
- интеграции: CLI, pandas, SQLAlchemy, Airflow-оператор, dbt-макросы;
- AI-слой со stub-провайдером — не отправляет реальные ПДн вовне без явного разрешения.

## Быстрый старт
```bash
pip install ru-smb-pd-anonymizer
ru-pd-anon inspect-schema --input examples/data/synthetic_crm.csv --format csv --out schema.json
ru-pd-anon suggest-policy --schema schema.json --use-case ml_training --out policy.yaml
ru-pd-anon apply-policy --input examples/data/synthetic_crm.csv --format csv --schema schema.json --policy policy.yaml --output examples/data/synthetic_crm_anon.csv
```

## Ограничения и ответственность
Проект технический и не является юридическим инструментом. Анонимизация/псевдонимизация требуют отдельной правовой оценки по 152-ФЗ/233-ФЗ и анализу риска реидентификации. Пользователь обязан соблюдать локализацию, законность обработки и трансграничной передачи ПДн.

## Поддержка и услуги
Разработка и консультации — [run-as-daemon.ru](https://run-as-daemon.ru). Возможны услуги по построению безопасных пайплайнов ПДн, подготовке к использованию внешних LLM/AI и внедрению анонимизации как кода.
