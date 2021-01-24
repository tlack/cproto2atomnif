// line #0
// proto void nothing();
// parsed: {'args_raw': None, 'modname': 'testlib', 'returns': 'void', 'func': 'nothing', 'args': [], 'arity': 0}

// line #1
// proto void nothing2(int a);
// parsed: {'args_raw': 'int a', 'modname': 'testlib', 'returns': 'void', 'func': 'nothing2', 'args': [{'access': '', 'type': 'int', 'argname': 'a', 'modifiers': '', 'position': 0}], 'arity': 1}

// line #2
// proto int add(int a, int b);
// parsed: {'args_raw': 'int a, int b', 'modname': 'testlib', 'returns': 'int', 'func': 'add', 'args': [{'access': '', 'type': 'int', 'argname': 'a', 'modifiers': '', 'position': 0}, {'access': '', 'type': 'int', 'argname': 'b', 'modifiers': '', 'position': 1}], 'arity': 2}

// line #3
// proto float addf(float a, float b);
// parsed: {'args_raw': 'float a, float b', 'modname': 'testlib', 'returns': 'float', 'func': 'addf', 'args': [{'access': '', 'type': 'float', 'argname': 'a', 'modifiers': '', 'position': 0}, {'access': '', 'type': 'float', 'argname': 'b', 'modifiers': '', 'position': 1}], 'arity': 2}

// line #4
// proto char* reverse(char* blah);
// parsed: {'args_raw': 'char* blah', 'modname': 'testlib', 'returns': 'char*', 'func': 'reverse', 'args': [{'access': '', 'type': 'char*', 'argname': 'blah', 'modifiers': '', 'position': 0}], 'arity': 1}


    #include "freertos/FreeRTOS.h"
    #include "freertos/task.h"
    #include <esp_log.h>
    #include <stdlib.h>
    #include <defaultatoms.h>
    #include <interop.h>
    #include <nifs.h>
    #include <port.h>
    #include <term.h>

    static term nif_testlib_nothing(Context *ctx, int argc, term argv[]) {
        printf("entering testlib:nothing/%d", argc); 
        if (argc != 0) {
            printf("testlib:nothing/%d - expected %d args, got %d", 0, 0, argc);
            return BADARG_ATOM;
        }
        
        nothing();
        return ATOM_OK;
    }
    static const struct Nif testlib_nothing_nif_info = 
    {
        .base.type = NIFFunctionType,
        .nif_ptr = nif_testlib_nothing
    };

    static term nif_testlib_nothing2(Context *ctx, int argc, term argv[]) {
        printf("entering testlib:nothing2/%d", argc); 
        if (argc != 1) {
            printf("testlib:nothing2/%d - expected %d args, got %d", 1, 1, argc);
            return BADARG_ATOM;
        }
        
        int a = (int)term_to_int(argv[0]);
        nothing2(a);
        return ATOM_OK;
    }
    static const struct Nif testlib_nothing2_nif_info = 
    {
        .base.type = NIFFunctionType,
        .nif_ptr = nif_testlib_nothing2
    };

    static term nif_testlib_add(Context *ctx, int argc, term argv[]) {
        printf("entering testlib:add/%d", argc); 
        if (argc != 2) {
            printf("testlib:add/%d - expected %d args, got %d", 2, 2, argc);
            return BADARG_ATOM;
        }
        
        int a = (int)term_to_int(argv[0]);
        int b = (int)term_to_int(argv[1]);
        int func_result = add(a, b);
        
	term atom_val = term_from_int32(func_result);
        VALIDATE_VALUE(atom_val, term_is_integer);
        return atom_val;
    }
    static const struct Nif testlib_add_nif_info = 
    {
        .base.type = NIFFunctionType,
        .nif_ptr = nif_testlib_add
    };

    static term nif_testlib_addf(Context *ctx, int argc, term argv[]) {
        printf("entering testlib:addf/%d", argc); 
        if (argc != 2) {
            printf("testlib:addf/%d - expected %d args, got %d", 2, 2, argc);
            return BADARG_ATOM;
        }
        
        float a = (float)term_to_float(argv[0]);
        float b = (float)term_to_float(argv[1]);
        float func_result = addf(a, b);
        
	term atom_val = term_from_float(func_result);
        VALIDATE_VALUE(atom_val, term_is_float);
        return atom_val;
    }
    static const struct Nif testlib_addf_nif_info = 
    {
        .base.type = NIFFunctionType,
        .nif_ptr = nif_testlib_addf
    };

    static term nif_testlib_reverse(Context *ctx, int argc, term argv[]) {
        printf("entering testlib:reverse/%d", argc); 
        if (argc != 1) {
            printf("testlib:reverse/%d - expected %d args, got %d", 1, 1, argc);
            return BADARG_ATOM;
        }
        
        char* blah = (char*)term_binary_data(argv[0]);
        char* func_result = reverse(blah);
        
	term atom_val = term_from_literal_binary(func_result, strlen(func_result));
        VALIDATE_VALUE(atom_val, term_is_binary)
        return atom_val;
    }
    static const struct Nif testlib_reverse_nif_info = 
    {
        .base.type = NIFFunctionType,
        .nif_ptr = nif_testlib_reverse
    };
    const struct Nif *testlib_get_nif(const char *nifname)
    {
        
        if (strcmp("testlib:nothing/0", nifname) == 0) {
            return &testlib_nothing_nif_info;
        }

        if (strcmp("testlib:nothing2/1", nifname) == 0) {
            return &testlib_nothing2_nif_info;
        }

        if (strcmp("testlib:add/2", nifname) == 0) {
            return &testlib_add_nif_info;
        }

        if (strcmp("testlib:addf/2", nifname) == 0) {
            return &testlib_addf_nif_info;
        }

        if (strcmp("testlib:reverse/1", nifname) == 0) {
            return &testlib_reverse_nif_info;
        }
        return NULL;
    }
    
