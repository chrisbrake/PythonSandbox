from importFail.protectedImports import not_special

unavailable_libs = list()
desired_libs = ['sys', 'itertools', 'functions', 'not_a_real_thing']

for lib in desired_libs:
    try:
        __import__(lib)
    except ImportError:
        unavailable_libs.append(lib)

if not {'sys', 'itertools'}.issubset(unavailable_libs):
    from importFail.protectedImports import special
else:
    from importFail.protectedImports import bomb as special

if 'not_a_real_thing' not in unavailable_libs:
    from importFail.protectedImports import impossible
else:
    from importFail.protectedImports import bomb as impossible
