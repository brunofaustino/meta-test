# meta-test

# Pré requisitos

- [Python](https://www.python.org/downloads/) 3.10+

# Configuração do ambiente

- [pip](https://pip.pypa.io/en/stable/cli/pip_install/) 24.3.1+

# Questão 1

![arquitetura.jpg](arquitetura.jpg)

# Questão 2

```sh
python question_2.py data/invoices.csv 2020-01-01
```

Output: 

![output_2.jpg](img/output_2.jpg)

# Questão 3

```sh
python3 question_3.py --files data/hour=13.json data/hour=14.json --customer C2000
```

```sh
python3 question_3.py --files data/hour=13.json data/hour=14.json --customer C1000
```

![output_3.jpg](img/output_3.jpg)