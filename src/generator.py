from . import types
from . import util

def build_arg_unpackers(proto):
    encoders = []
    for a in proto['args']:
        ifc = types.get_interface(a['type'])
        if ifc:
            pos = a['position']
            argname = f"argv[{pos}]"
            encoders.append(ifc.atom_to_c(a['type'], a['argname'], argname))
        else:
            util.warn(f"no handler for {a['type']}")
    return ''.join(encoders)

def build_exec(proto):
    args = ", ".join([a['argname'] for a in proto['args']])
    if proto['returns'] == 'void':
        return f"""
        {proto['func']}({args});"""
    else:
        return f"""
        {proto['returns']} func_result = {proto['func']}({args});"""

def build_return_value(proto):
    if proto['returns'] == 'void':
        return """
        return ATOM_OK;""";
    else:
        ifc = types.get_interface(proto['returns'])
        if ifc:
            make_retval = ifc.c_to_atom('atom_val', 'func_result')
            return f"""
        {make_retval}
        return atom_val;"""
        else:
            util.warn(f"no handler for {proto['returns']}")
            return f"""
        // no handler found for {proto['returns']}
            """
    
def build_nif_skeleton(proto, modname):
    if proto is None: return ''
    proto.update({
        'modname': modname,
        'unpack_args': build_arg_unpackers(proto),
        'exec': build_exec(proto),
        'make_ret_val': build_return_value(proto)
    })
    r = """
    static term nif_{modname}_{func}(Context *ctx, int argc, term argv[]) {{
        printf("entering {modname}:{func}/%d", argc); 
        if (argc != {arity}) {{
            printf("{modname}:{func}/%d - expected %d args, got %d", {arity}, {arity}, argc);
            return BADARG_ATOM;
        }}
        {unpack_args}{exec}{make_ret_val}
    }}
    static const struct Nif {modname}_{func}_nif_info = 
    {{
        .base.type = NIFFunctionType,
        .nif_ptr = nif_{modname}_{func}
    }};"""
    return r.format(**proto)

def build_nif_implementations(protos, modname):
    return [build_nif_skeleton(p, modname) for p in protos]

def build_nif_matchers(protos, modname):
    proto_matches = []

    for p in protos: 
        if p is None: continue
        proto_matches.append(f"""
        if (strcmp("{modname}:{p['func']}/{p['arity']}", nifname) == 0) {{
            return &{modname}_{p['func']}_nif_info;
        }}""")

    return proto_matches

def generate_enclosure(protos, modname):
    
    nifs = build_nif_implementations(protos, modname)
    nif_impls = "\n".join(nifs).strip()
    proto_matches = build_nif_matchers(protos, modname)
    proto_dispatcher = "\n".join(proto_matches)

    return f"""
    #include "freertos/FreeRTOS.h"
    #include "freertos/task.h"
    #include <esp_log.h>
    #include <stdlib.h>
    #include <defaultatoms.h>
    #include <interop.h>
    #include <nifs.h>
    #include <port.h>
    #include <term.h>

    {nif_impls}
    const struct Nif *{modname}_get_nif(const char *nifname)
    {{
        {proto_dispatcher}
        return NULL;
    }}
    """

