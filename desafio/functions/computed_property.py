class computed_property:
    """
    Um decorator semelhante ao @property, mas com um cache baseado em suas dependências.

    O valor da propriedade é calculado uma única vez e armazenado em cache,
    sendo recalculado apenas quando algum dos atributos dependentes for alterado.

    A estrutura de cache é armazenada no atributo interno do objeto chamado "_computed_cache".

    Parâmetros:
    -----------
    *dependencies : str
        Nomes dos atributos dos quais a propriedade depende.
    """

    def __init__(self, *dependencies):
        self.dependencies = dependencies # Lista de atributos dos quais a propriedade depende
        self.fget = None                 # Função getter
        self.fset = None                 # Função setter
        self.fdel = None                 # Função deleter
        self.__doc__ = None              # Docstring preservada

    def __call__(self, func):
        """
        Recebe a função original decorada como getter e armazena sua docstring.
        """
        self.fget = func
        self.__doc__ = func.__doc__
        return self

    def __get__(self, obj, objtype=None):
        """
        Executado ao acessar a propriedade no objeto.

        Verifica se o valor cacheado ainda é válido com base nas dependências;
        se sim, retorna do cache, caso contrário, recalcula e atualiza o cache.
        """
        if obj is None:
            return self

        # Garante que o dicionário de cache está presente
        if not hasattr(obj, "_computed_cache"):
            obj._computed_cache = {}

        key = self.fget.__name__  # Nome da propriedade (ex: "diameter" para uma classe Circle)

        # Valores atuais das dependências
        current_deps = tuple(repr(getattr(obj, dep, object())) for dep in self.dependencies)

        # Recupera o cache (dependências anteriores + valor)
        cache_entry = obj._computed_cache.get(key)

        # Se as dependências não mudaram, retorna o valor cacheado
        if cache_entry:
            old_deps, cached_value = cache_entry
            if old_deps == current_deps:
                return cached_value

        # Caso contrário, recalcula, atualiza o cache e retorna o novo valor
        value = self.fget(obj)
        obj._computed_cache[key] = (current_deps, value)
        return value

    def _invalidate_cache(self, obj):
        """
        Remove a entrada correspondente à propriedade no dicionário de cache do objeto.
        """
        if hasattr(obj, "_computed_cache"):
            obj._computed_cache.pop(self.fget.__name__, None)

    def setter(self, fset):
        """
        Define a função que será usada ao atribuir um valor à propriedade.
        """
        self.fset = fset
        return self

    def deleter(self, fdel):
        """
        Define a função que será usada ao deletar a propriedade.
        """
        self.fdel = fdel
        return self

    def __set__(self, obj, value):
        """
        Executado quando a propriedade recebe um valor.
        Requer que um setter tenha sido definido.
        """
        if self.fset is None:
            raise AttributeError(
                f"Não é possível atribuir à propriedade '{self.fget.__name__}': "
                "nenhum setter foi definido."
            )
        self.fset(obj, value)
        self._invalidate_cache(obj)

    def __delete__(self, obj):
        """
        Executado ao fazer 'del propriedade'. Requer que um deleter tenha sido definido.
        """
        if self.fdel is None:
            raise AttributeError(
                f"Não é possível deletar a propriedade '{self.fget.__name__}': "
                "nenhum deleter foi definido."
            )
        self.fdel(obj)
        self._invalidate_cache(obj)
