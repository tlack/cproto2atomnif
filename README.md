cproto2atomnif
==============

Plug existing C code into your [AtomVM](https://github.com/bettio/AtomVM) 
applications quickly and easily.

cproto2atomnif is a Python script that reads C prototype header files and spits
out code to use them from inside Erlang or Elixir on AtomVM.

The process of creating these AtomVM nifs is very straightforward, but there 
is a lot of boilerplate involved. This script automates that by creating the 
C source code for the AtomVM nif component.

You still need to edit the resulting code to add your specific validation
logic, etc.

# example

```
$ cat test-library.c
int add(int a, int b) {
	        return a+b;
}
$ cat test-library.h
int add(int a, int b);
$ cproto2atomnif test-library.h testlib > testlib.c
$ cat testlib.c

    #include "freertos/FreeRTOS.h"
    #include "freertos/task.h"
    #include <esp_log.h>
    #include <stdlib.h>
    #include <defaultatoms.h>
    #include <interop.h>
    #include <nifs.h>
    #include <port.h>
    #include <term.h>

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

    const struct Nif *testlib_get_nif(const char *nifname)
    {
        if (strcmp("testlib:add/2", nifname) == 0) {
            return &testlib_add_nif_info;
        }

        return NULL;
    }

```

# status

- Does NOT support precompiler macros, or real `.h` files. You must simplify your prototypes before use!
- Rough, barbarian-style first draft
- Supports only `int` (of various kinds), `float`/`double`, and `char*`/`uint8_t*` (as beam binaries).
- Very crude regular expression-based parser; should switch to `pyclanguage`
- Would be cool to have more config options, or any config options.

# motivation

There is a lot of existing Arduino code that I need to call from Erlang code
running in AtomVM!


