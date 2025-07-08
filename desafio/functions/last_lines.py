import io
import os

def last_lines(filename, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Retorna um iterador sobre as linhas de um arquivo em ordem reversa,
    semelhante ao comando Unix `tac`, mantendo os caracteres de nova linha.
    Aplica fix para arquivos Windows, removendo '\r'.

    Parâmetros:
        filename (str): Caminho para o arquivo de texto.
        buffer_size (int): Tamanho dos blocos lidos em bytes.

    Retorno:
        iterator: Iterador sobre as linhas do arquivo em ordem reversa.
    """
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        buffer = b""
        position = file_size

        while position > 0:
            # Tamanho do bloco a ser lido.
            read_size = min(buffer_size, position)
            position -= read_size # Move o ponteiro para o início do próximo bloco
            f.seek(position)
            chunk = f.read(read_size) 
            buffer = chunk + buffer # Novo chunk vem "antes" do que o que já está no buffer
            # a variável buffer vai ultrapassar o tamanho de buffer_size, pois precisa armazenar o que foi lido
            # até que chegue o final da linha, do contrário, teriamos que retornar linhas quebradas.

            # Divide o buffer em uma lista de linhas usando o caractere de nova linha.
            # Ex: b'\nlinhaB\n'.split(b'\n') -> [b'', b'linhaB', b'']
            lines = buffer.split(b'\n')

            # Guarda o começo da linha para levar para a próxima iteração
            buffer = lines.pop(0)

            for line in reversed(lines):
                if line:
                    """Decodifica de bytes para string (UTF-8), substitui caracteres problemáticos,
                       remove '\r' (de quebras de linha do Windows) e adiciona um '\n' ao final."""
                    yield line.decode('utf-8', errors='ignore').replace('\r', '') + '\n'

                elif position > 0 or (file_size == len(chunk) and len(lines) > 0):
                    """Verifica se a linha vazia (b'') deve ser ignorada.
                       Ela tenta filtrar o b'' gerado por split() quando o arquivo termina com '\n'.
                       Se 'position > 0': Ainda há mais arquivo para ler (não chegou no início).
                       Se 'file_size == len(chunk) and len(lines) > 0': o arquivo é pequeno
                       e foi lido em um único chunk (position == 0)."""
                    pass

                else:
                    """Se não for uma linha vazia que deve ser ignorada (ou seja, é uma linha vazia real),
                   então a renderiza uma quebra de linha."""
                    yield '\n'

        if buffer:
            yield buffer.decode('utf-8', errors='ignore').replace('\r', '') + '\n'
