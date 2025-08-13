# Fake Data Generator for QA

A Python-based CLI tool to generate **fake test data** in CSV or JSON format, tailored for **QA** and **automation** scenarios.

Supports multiple locales (e.g., `pt_BR`, `en_US`), customizable field schemas, and reproducible data generation using seeds.  
Perfect for manual and automated test environments without exposing real data.

---

## ✨ Features
- Generate **fake data** in CSV or JSON format.
- Multiple locales supported (`pt_BR`, `en_US`, etc.).
- Customizable schema: choose exactly which fields you need.
- Seed option for reproducible datasets.
- Ready for manual testing, automation, or performance testing.

---

## 📦 Installation
```bash
pip install Faker

## 🚀 Usage
Generate 20 rows in CSV (Brazil locale):
```bash
python fake_data_generator.py --rows 20 --locale pt_BR --format csv --output data.csv

Generate 10 rows in JSON (US locale, custom fields):
python fake_data_generator.py --rows 10 --locale en_US --format json --schema name,email,address --output data.json

Example Output (CSV):
nome,email,cpf,telefone,empresa
João Silva,joao@example.com,123.456.789-10,(11) 99999-9999,ACME LTDA

Author
👩‍💻 Renata Sousa
