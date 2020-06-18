build/lib_min_time_bvp.so : build/min_time_bvp.o
	g++ -shared -Wl,-soname,lib_min_time_bvp.so -o build/lib_min_time_bvp.so build/min_time_bvp.o lib/opt_control_lib.a

build/min_time_bvp.o : py_opt_control/min_time_bvp.cpp include/rt_nonfinite.h
	g++ -c -fPIC py_opt_control/min_time_bvp.cpp -llib/opt_control_lib.a -iquote include -o build/min_time_bvp.o

clean :
	-rm -vf build/lib_min_time_bvp.so min_time_bvp.o build/min_time_bvp.pyc

m.PHONY : clean
