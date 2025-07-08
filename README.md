# Desafios BWGI

#### Os desafios de dados encontram-se no arquivo "Desafio de Dados.pdf" com as respostas destacadas na cor verde.

#### Os desafios de programação estão no diretório `desafio`, as funções estão na pasta `functions` e o testes na pasta `tests`.

##### Para rodar os testes utilize a linha de comando a partir do diretório `desafio`:
```commandline
python -m unittest discover
```

#### Abaixo alguns exemplo de como utilizar as funções:

##### reconcile_accounts
```python
from functions.reconcile_accounts import reconcile_accounts

transactions1 = [['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'], ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'], ['2020-12-05', 'Tecnologia', '50.00', 'AWS']]
transactions2 = [['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'], ['2020-12-05', 'Tecnologia', '49.99', 'AWS'], ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares']]

reconciled1, reconciled2 = reconcile_accounts(transactions1, transactions2)
print(reconciled1)
print(reconciled2)
```

##### last_lines
```python
from functions.last_lines import last_lines

filepath = self._create_file("single_line.txt", "Single line file.\n")
for line in last_lines('single_line.txt'):
    print(line, end='')
```

##### computed_property
```python
from functions.computed_property import computed_property
from math import sqrt

class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property('x', 'y', 'z')
    def magnitude(self):
        print('computing magnitude')
        return sqrt(self.x**2 + self.y**2 + self.z**2)
```
