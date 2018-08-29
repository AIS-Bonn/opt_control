//------------------------------------------------------------------------
// File:       evaluate_to_time.h
// Version:    2018-08-29 12:42:43
// Maintainer: Marius Beul (mbeul@ais.uni-bonn.de)
// Package:    opt_control (https://github.com/AIS-Bonn/opt_control)
// License:    BSD
//------------------------------------------------------------------------

// Software License Agreement (BSD License)
// Copyright (c) 2018, Computer Science Institute VI, University of Bonn
// All rights reserved.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 
// * Redistributions of source code must retain the above copyright
//   notice, this list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above
//   copyright notice, this list of conditions and the following
//   disclaimer in the documentation and/or other materials provided
//   with the distribution.
// * Neither the name of University of Bonn, Computer Science Institute
//   VI nor the names of its contributors may be used to endorse or
//   promote products derived from this software without specific
//   prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
// FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
// COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
// BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
// ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//------------------------------------------------------------------------

#ifndef EVALUATE_TO_TIME_H
#define EVALUATE_TO_TIME_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern void b_evaluate_to_time(double P_init, double V_init, double A_init,
  const emxArray_real_T *J_setp_struct_time, const emxArray_real_T
  *J_setp_struct_signals_values, double *P, double *V, double *A);
extern void c_evaluate_to_time(double P_init, double V_init, double A_init,
  emxArray_real_T *J_setp_struct_time, emxArray_real_T
  *J_setp_struct_signals_values, double T_in, double *P, double *V, double *A);
extern void d_evaluate_to_time(double P_init, double V_init, emxArray_real_T
  *J_setp_struct_time, emxArray_real_T *J_setp_struct_signals_values, double
  T_in, double *P, double *V, double *A, double *J);
extern void e_evaluate_to_time(const emxArray_real_T *P_init, const
  emxArray_real_T *V_init, const emxArray_real_T *A_init, emxArray_struct0_T
  *J_setp_struct, const emxArray_real_T *T_in, emxArray_real_T *P,
  emxArray_real_T *V, emxArray_real_T *A, emxArray_real_T *J);
extern void evaluate_to_time(double P_init, double V_init, double A_init, double
  J_setp_struct_time_data[], int J_setp_struct_time_size[1], double
  c_J_setp_struct_signals_values_[], int d_J_setp_struct_signals_values_[2],
  double T_in, double *P, double *V, double *A);

#endif
