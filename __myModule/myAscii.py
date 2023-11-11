list_ascii = ['NUL','SOH',
'STX',
'ETX',
'EOT',
'ENQ',
'ACK',
'BEL',
'BS',
'HT',
'LF',
'VT',
'FF',
'CR',
'SO',
'SI',
'DLE',
'DC1',
'DC2',
'DC3',
'DC4',
'NAK',
'SYN',
'ETB',
'CAN',
'EM',
'SUB',
'ESC',
'FS',
'GS',
'RS',
'US',
' ',
'!',
'"',
'#',
'$',
'%',
'&',
"'",
'(',
')',
'*',
'+',
',',
'-',
'.',
'/',
'0',
'1',
'2',
'3',
'4',
'5',
'6',
'7',
'8',
'9',
':',
';',
'<',
'=',
'>',
'?',
'@',
'A',
'B',
'C',
'D',
'E',
'F',
'G',
'H',
'I',
'J',
'K',
'L',
'M',
'N',
'O',
'P',
'Q',
'R',
'S',
'T',
'U',
'V',
'W',
'X',
'Y',
'Z',
'[',
'\\',
']',
'^',
'_',
'`',
'a',
'b',
'c',
'd',
'e',
'f',
'g',
'h',
'i',
'j',
'k',
'l',
'm',
'n',
'o',
'p',
'q',
'r',
's',
't',
'u',
'v',
'w',
'x',
'y',
'z',
'{',
'|',
'}',
'~',
'DEL',
'€',
'',
'‚',
'ƒ',
'„',
'…',
'†',
'‡',
'ˆ',
'‰',
'Š',
'‹',
'Œ',
'',
'Ž',
'',
'',
'‘',
'’',
'“',
'”',
'•',
'–',
'—',
'˜',
'™',
'š',
'›',
'œ',
'',
'ž',
'Ÿ',
'P',
'¡',
'¢',
'£',
'¤',
'¥',
'¦',
'§',
'¨',
'©',
'ª',
'«',
'¬',
'Y',
'®',
'¯',
'°',
'±',
'²',
'³',
'´',
'µ',
'¶',
'·',
'¸',
'¹',
'º',
'»',
'¼',
'½',
'¾',
'¿',
'À',
'Á',
'Â',
'Ã',
'Ä',
'Å',
'Æ',
'Ç',
'È',
'É',
'Ê',
'Ë',
'Ì',
'Í',
'Î',
'Ï',
'Ð',
'Ñ',
'Ò',
'Ó',
'Ô',
'Õ',
'Ö',
'×',
'Ø',
'Ù',
'Ú',
'Û',
'Ü',
'Ý',
'Þ',
'ß',
'à',
'á',
'â',
'ã',
'ä',
'å',
'æ',
'ç',
'è',
'é',
'ê',
'ë',
'ì',
'í',
'î',
'ï',
'ð',
'ñ',
'ò',
'ó',
'ô',
'õ',
'ö',
'÷',
'ø',
'ù',
'ú',
'û',
'ü',
'ý',
'þ',
'ÿ']



def ascii(x, allow_error = False, extended= False, default_error_char = '§', allow_control_values = False):
    '''


    Args:
        x (int): Index in ASCII Table
        x (str): One character string represented in ASCII table
        allow_error (bool, optional): Function is not going to generate an error if character is not in ASCII table or index greater than ASCII table range
            defalut : False
        extended (bool, optional): Function will use ASCII-Extended version of table (range : 0-255)
        allow_control_values (bool, optional): Function return control value. Ex : DEL, NULL, EXT
        default_error_char (str, optional): what char is returned when value has error

    Returns
        ascii(x:int) -> str
        Returns the str character corresponding to that index in ASCII table

        ascii(x:str) -> int
        Returns the index value of some character valid in ASCII table

    Raises:
        ValueError : Is raised when integer is out of range (0:127 or 0:255 if exteded) or is not a valid ASCII character

    Exemplos:
        ascii(99) -> "c"
        ascii("c") -> 99
        ascii(500) -> ValueError
        ascii("₢") -> ValueError
        ascii(500,  allow_error=True) -> "§" (sem sinal)
        ascii("₢", allow_error=True) -> -1
    '''
    if type(x) == str:
        try:
            if extended:
                return list_ascii.index(x)
            else:
                return list_ascii[:128].index(x)
        except:
            if allow_error:
                return -1
            else:
                raise ValueError(f'Caracter {x} não existe na tabela ascii padrão')
    if type(x) == int:
        if extended:
            if x > 255:
                if allow_error:
                    return default_error_char
                else:
                    raise ValueError(f'Valor {x} está fora do range da tabela ascci')
            if not(allow_control_values):
                if len(list_ascii[x]) > 1:
                    return default_error_char
                else:
                    return list_ascii[x]
            else:
                return list_ascii[x]
        else:
            if x >= 128:
                if allow_error:
                    return default_error_char
                else:
                    raise ValueError(f'Valor {x} está fora do range da tabela ascci')
            if not(allow_control_values):
                if len(list_ascii[x]) > 1:
                    return default_error_char
                else:
                    return list_ascii[x]
            else:
                return list_ascii[x]