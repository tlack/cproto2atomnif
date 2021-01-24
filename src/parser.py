import re

RE_OPTS = re.VERBOSE | re.IGNORECASE  # | re.DOTALL

def resolve_re(re_str):
    x = re_str
    access = '(static|const)';
    identifier = '[a-z0-9:_.]+';
    pats = {
        'access': access,
        'identifier': identifier,
        # 'modifiers': '((\[\]|\*)+)'     # ex. []
    }
    pats['types'] = f'( {access}? \s? (&|\*)? \s* {identifier} )'
    for code, pat in pats.items():
        x = x.replace('{'+code+'}', pat)
    return x

def parse_return_and_func(line):
    r = {}
    line = line.strip()

    '''
    mod_re_str = resolve_re('.+(?P<modifiers> {modifiers})$')
    print(f'mod_re_str\n{line}\n{mod_re_str}\n')
    mod_re = re.compile(mod_re_str)
    m = mod_re.match(line)
    if m:
        print('got modifier', m)
        r['modifiers'] = m.groupdict()['modifiers']
        line = line.replace(m.match[0])
    '''

    words = re.split('\s', line)
    r['returns'] = ' '.join(words[:-1])
    r['func'] = words[-1]
    return r

def parse_args(n, args_str):
    arg_re_str = '''
        ((?P<access>{access}) \s+)?   # ex. static
        (?P<type>.+)                  # ex. int
        \s+
        (?P<argname>{identifier})     # ex. age
        \s?
        (?P<modifiers>(\[\]|\*)+)?     # ex. []
    '''
    arg_re_str_final = resolve_re(arg_re_str)
    arg_re = re.compile(arg_re_str_final, RE_OPTS)
    args_parsed = []
    if args_str:
        arg_parts = args_str.split(",")
        for i, p in enumerate(arg_parts):
            am = arg_re.match((p or '').strip())
            if am:
                arg_info = {k: v.strip() if not v is None else '' for k, v in am.groupdict().items()}
                arg_info['position'] = i
                args_parsed.append(arg_info)
            else:
                print(f'WARNING: line {n}: could not parse argument "{p}"')
    return args_parsed

def parse_line(n, line, modname):

    line = line.strip()
    if line == '': return None

    print(f'parsing line #{n}: {line}')
    proto_re_str = '''
        \s*
        # get the return type
        (?P<ret_and_func> .+) 
        \s?
        \s? \( \s? 
        (?P<args_raw>     # ie int age, char* name
            .+
        )?
        \s? \) \s? 
        # optional semicolon, EOL 
        ;? \s? $
    '''
    proto_re_str_final = resolve_re(proto_re_str)
    proto_re = re.compile(proto_re_str_final, RE_OPTS)

    m = proto_re.match(line)
    if m:
        g = m.groupdict()
        g['modname'] = modname

        # expand 'void print' into 'ret' -> 'void', 'func' -> 'print'
        ret_and_func = g['ret_and_func']
        del g['ret_and_func']
        g.update(parse_return_and_func(ret_and_func))

        # expand arguments
        args_str = (g['args_raw'] or '').strip()
        g['args'] = parse_args(n, args_str)
        g['arity'] = len(g['args'])

        print('// ->', line, '\n<-', g)
        return g
    else:
        print(f'WARNING: line {n}: could not parse prototype at all: "{line}"')
        return None

def load_protos(fn, modname):
    return [parse_line(i, x, modname) for i, x in enumerate(open(fn, 'r').read().split('\n'))]

