lib_min_time_bvp.so : min_time_bvp.o
	g++ -shared -Wl,-soname,lib_min_time_bvp.so -o lib_min_time_bvp.so min_time_bvp.o lib/opt_control_lib.a

min_time_bvp.o : src/min_time_bvp.cpp include/rt_nonfinite.h
	g++ -c -fPIC src/min_time_bvp.cpp -llib/opt_control_lib.a -iquote include -o min_time_bvp.o

clean :
	-rm -vf lib_min_time_bvp.so min_time_bvp.o min_time_bvp.pyc

m.PHONY : clean
