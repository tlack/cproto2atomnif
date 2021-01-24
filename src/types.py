class TypeInterface:
    def can_handle(self, type_):
        for t in self.types:
            if t in type_:
                return True
        return False
    def c_to_atom(self, type_, name, expr):
        return "// not yet implemented"
    def atom_to_c(self, type_, name, expr):
        return "// not yet implemented"

class IntInterface(TypeInterface):
    types = [
        "int",
        "long",
        "long long",
        "int8_t",
        "int16_t"
    ]

    def c_to_atom(self, name, expr):
        s = f"""
	term {name} = term_from_int32({expr});
        VALIDATE_VALUE({name}, term_is_integer);""";
        return s

    def atom_to_c(self, type_, name, expr):
        if type_ == "void":
            type_b = ""
        else:
            type_b = type_ + " "
        s = f"""
        {type_b}{name} = ({type_})term_to_int({expr});"""
        return s

class FloatInterface(TypeInterface):
    types = [
        "float",
        "double"
    ]

    def c_to_atom(self, name, expr):
        s = f"""
	term {name} = term_from_float({expr});
        VALIDATE_VALUE({name}, term_is_float);""";
        return s

    def atom_to_c(self, type_, name, expr):
        if type_ == "void":
            type_b = ""
        else:
            type_b = type_ + " "
        s = f"""
        {type_b}{name} = ({type_})term_to_float({expr});"""
        return s

class StringInterface(TypeInterface):
    types = [
        "char*",
        "uint8_t*"
    ]

    def c_to_atom(self, name, expr):
        s = f"""
	term {name} = term_from_literal_binary({expr}, strlen({expr}));
        VALIDATE_VALUE({name}, term_is_binary)""";
        return s

    def atom_to_c(self, type_, name, expr):
        type_b = type_ + " "
        s = f"""
        {type_b}{name} = ({type_})term_binary_data({expr});"""
        return s

INTERFACES = [
    IntInterface(),
    FloatInterface(),
    StringInterface()
]

def get_interface(type_):
    for i in INTERFACES:
        if i.can_handle(type_):
            return i
    return None
