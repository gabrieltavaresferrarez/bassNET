import platform
import os
import re

# TODO - COPY FILES

class Path:
    def __init__(self, path=None):
        self.__system = platform.system()
        self.__string_pathSeparator = '\\' if self.__system == 'Windows' else '/'

        #creation of path ---------------------------------------------
        if path:
            path = path.replace('/', self.__string_pathSeparator) # std separators
            path = path.replace('\\', self.__string_pathSeparator) # std separators
            path = path[:-1] if path[-1] == self.__string_pathSeparator else path # remove last separator if exists
            if path[0] == '.': #relative path with dot
                self.global_path=False
                path = path[1:]
                path = path[1:] if path[0] == self.__string_pathSeparator else path

                self.path = os.getcwd() + self.__string_pathSeparator + path
            #caminho global 
            elif (self.__system=='Windows' and path[1] ==  ':') or (self.__system !='Windows' and path[0] ==  '/') : 
                self.global_path=True
                self.path = path
            #relative path
            else:
                self.global_path=False
                self.path = os.getcwd() + self.__string_pathSeparator + path

        else:
            self.global_path=True
            self.path = os.getcwd()
        self.__listPath = self.path.split(self.__string_pathSeparator)
        self.__listPath = self.__listPath[1:] if self.__listPath[0] == '' else self.__listPath

        
    """Return if the file or folder exists

    Returns:
        bool :  True if exists
    """
    def exists(self) -> bool:
        return os.path.exists(self.path)

    """Return if item is a directory

    Returns:
        bool :  True if is directory
    """
    def is_dir(self):
        if self.exists():
            return os.path.isdir(self.path)
        else:
            raise ValueError('Caminho não existe')

    """Return if item is a file

    Returns:
        bool :  True if is file
    """
    def is_file(self):
        if self.exists():
            return os.path.isfile(self.path)
        else:
            raise ValueError('Caminho não existe')




    # atributos ====================================================================
    @property
    def str(self):
        return self.path
    def __str__(self):
        return self.path
    def __repr__(self):
        return f'<My custom path> : {self.path}'
    def __call__(self):
        return self.path




    # list(obj) ====================================================================================
    def __iter__(self):
        self.__index = 0
        return self
    
    def __next__(self):
        if self.__index < len(self.__listPath):
            resultado = self.__listPath[self.__index]
            self.__index += 1
            return resultado
        else:
            raise StopIteration
    
    def __getitem__(self, index):
        if index < len(self.__listPath):
            return self.__listPath[index]
        else:
            raise IndexError(f'Index {index} maior que o desejado. Máximo é {len(self.__listPath)-1}')
    @property
    def list(self):
        return list(self)


    # Operações -----------------------------------------------------------------
    def __sub__(self, valor):
        if type(valor) != int:
            raise ValueError('Pode subtrair apenas valores inteiros')
        if valor > len(self.__listPath) - 1:
            raise ValueError(f'Caminho {self.path} pode subtrair no máximo {len(self.__listPath) - 1} valores')
        return Path(self.__string_pathSeparator.join(list(self)[:-valor]))
    
    def __add__(self, valor):
        if type(valor) ==  str: 
            valor = valor[1:] if valor[0] in ['\\', '/'] else valor # remove primeiro separador se tiver
            valor = valor.replace('/', self.__string_pathSeparator) # std separators
            valor = valor.replace('\\', self.__string_pathSeparator) # std separators
            return Path(self.path + self.__string_pathSeparator + valor)


    """Create a directory if item doesn't exists

    Returns:
        bool :  True if create directory | False if path already exists
    """
    def make_dir(self):
        if self.exists():
            return False #arquivo já existe
        os.makedirs(self.path)
        return True

    """List all itens in Path

    Arguments:
        filter : str -> is unix filter like to define wich itens should be listed

    Returns:
        list :  Return a list of all ites in that directory

    Example:
        path.list_dir(filter='*.png')
        path.list_dir(filter='teste.*')
        path.list_dir(filter='teste.png')
    """
    def list_dir(self, filter:str = None) -> list:
        if self.is_dir():
            listStr_paths =  os.listdir(self.path)
        else:
            raise ValueError(f'Path {self.path} is not a directory or doesn\'t exists')

        if filter:
            if filter[0] == '*':
                padrao = filter[1:]
            else:
                padrao = '^'+filter

            if filter[-1] == '*':
                padrao = padrao[:-1]
            else:
                padrao = padrao +'$'
            listStr_paths = [path for path in listStr_paths if re.search(padrao, path)]
        return listStr_paths

    """Create a empty file in the path

    Returns:
        bool :  True if create file | False if file already exists
    """
    def make_file(self):
        if self.exists():
            return False #arquivo já existe
        elif not((self-1).exists()):
            (self-1).make_dir()
        
        open(self.path, 'w').close()
        return True
    
    """Delete path

    Returns:
        bool :  True if deleted
    """
    def delete(self):
        if self.is_file():
            os.remove(self.path)
            return True
        elif self.is_dir():
            os.rmdir(self.path)
            return True
        else:
            raise ValueError('Caminho não existe')
    
if __name__ == '__main__':
    path = Path('bola/bola2/') 

    print(path.path)

    print(path.str) # retorna o caminho em string
    print(str(path)) # retorna o caminho em string
    print(path()) # retorna o caminho em string


    print(list(path))
    print(path.list) # retorna o caminho em lista de caminhos
    print(list(path)) # retorna o caminho em lista de caminhos

    print(path[1]) # retorna a parte do caminho 
    
    print(path - 1)

    print(path.exists()) # bool

    print(path.make_dir()) # create dir if dont exists
# #     print(path.make_file()) # create file if dont exists


    print(path.is_dir()) # bool
    print(path.is_file()) # bool

    
    print(path + 'teste')
    print(path + '/teste/teste')
    print(path + 'teste/teste')
    print(path + '\\teste\\teste')
    print(path + 'teste\\teste')
    
    print(path.list_dir())
    
    print(path.delete())
