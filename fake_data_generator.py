#!/usr/bin/env python3
"""
fake_data_generator.py
---------------------------------
Gerador de massa de dados fake para QA, com suporte a:
- Locale (ex.: pt_BR, en_US)
- Campos comuns (nome, email, cpf, cnpj, telefone, endereço, etc.)
- Saída em CSV ou JSON
- Schema customizado via lista de campos
- Semente (seed) para reprodutibilidade

Uso:
python fake_data_generator.py --rows 100 --locale pt_BR --format csv --schema nome,email,cpf,telefone,empresa --output dados.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

try:
    from faker import Faker
except ImportError:
    print("Erro: biblioteca 'Faker' não encontrada. Instale com: pip install Faker", file=sys.stderr)
    sys.exit(1)

# Mapeamento de campos "amigáveis" -> funções do Faker
def get_field_generators(fake: "Faker") -> Dict[str, Any]:
    return {
        # Pessoas
        "nome": fake.name,
        "primeiro_nome": fake.first_name,
        "sobrenome": fake.last_name,
        "email": fake.email,
        "usuario": fake.user_name,
        "senha": fake.password,
        "data_nascimento": lambda: fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "cpf": lambda: getattr(fake, "cpf")(),
        "cnpj": lambda: getattr(fake, "cnpj")(),
        "rg": lambda: getattr(fake, "rg")(),
        "telefone": lambda: fake.phone_number(),
        "celular": lambda: fake.cellphone_number() if hasattr(fake, "cellphone_number") else fake.phone_number(),
        "uuid": fake.uuid4,

        # Endereços
        "endereco": fake.street_address,
        "bairro": getattr(fake, "bairro", lambda: fake.secondary_address()),
        "cidade": fake.city,
        "estado": fake.state,
        "cep": fake.postcode,
        "pais": fake.country,

        # Empresa
        "empresa": fake.company,
        "cargo": fake.job,
        "cnpj_empresa": lambda: getattr(fake, "cnpj")(),

        # Internet e web
        "url": fake.url,
        "dominio": fake.domain_name,
        "ip": fake.ipv4,

        # Financeiro
        "preco": lambda: float(f"{fake.pyfloat(left_digits=3, right_digits=2, positive=True):.2f}"),
        "moeda": fake.currency_code,
        "cartao_credito": fake.credit_card_number,

        # Datas e tempo
        "data": lambda: fake.date().isoformat(),
        "hora": lambda: fake.time(),
        "timestamp": lambda: fake.date_time_between(start_date="-2y", end_date="now").isoformat(),

        # Texto
        "frase": fake.sentence,
        "texto": lambda: fake.text(max_nb_chars=140),
    }

DEFAULT_SCHEMA = ["nome","email","cpf","telefone","endereco","cidade","estado","cep","empresa","cargo","data"]

def build_row(fake: "Faker", schema: List[str]) -> Dict[str, Any]:
    generators = get_field_generators(fake)
    row = {}
    for field in schema:
        f = field.strip()
        gen = generators.get(f)
        if gen is None:
            # Se não houver gerador específico, tenta atributo do faker diretamente
            if hasattr(fake, f):
                val = getattr(fake, f)()
            else:
                val = None
        else:
            val = gen()
        row[f] = val
    return row

def main():
    parser = argparse.ArgumentParser(description="Gerador de massa de dados fake para QA.")
    parser.add_argument("--rows", type=int, default=100, help="Quantidade de linhas (default: 100)")
    parser.add_argument("--locale", type=str, default="pt_BR", help="Locale do Faker (ex.: pt_BR, en_US)")
    parser.add_argument("--format", type=str, choices=["csv","json"], default="csv", help="Formato de saída (csv/json)")
    parser.add_argument("--schema", type=str, default=",".join(DEFAULT_SCHEMA), help="Lista de campos separados por vírgula")
    parser.add_argument("--output", type=str, default=None, help="Caminho do arquivo de saída (default: auto)")
    parser.add_argument("--seed", type=int, default=None, help="Semente para dados reprodutíveis")
    args = parser.parse_args()

    fake = Faker(args.locale)
    if args.seed is not None:
        Faker.seed(args.seed)

    schema = [s.strip() for s in args.schema.split(",") if s.strip()]

    rows = [build_row(fake, schema) for _ in range(args.rows)]

    # Nome de saída padrão
    if args.output is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"fake_data_{args.locale}_{ts}.{args.format}"

    if args.format == "csv":
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=schema)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Arquivo gerado: {args.output}")
    print(f"Campos: {', '.join(schema)}")
    print(f"Linhas: {len(rows)}")

if __name__ == "__main__":
    main()
