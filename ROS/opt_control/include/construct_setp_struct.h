//------------------------------------------------------------------------
// File:       construct_setp_struct.h
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

#ifndef CONSTRUCT_SETP_STRUCT_H
#define CONSTRUCT_SETP_STRUCT_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern void b_construct_setp_struct(const cell_wrap_11 t_in2[1], const
  cell_wrap_11 J_in2[1], emxArray_real_T *J_setp_struct_time, emxArray_real_T
  *J_setp_struct_signals_values);
extern void c_construct_setp_struct(const double t_in2[1], emxArray_real_T
  *J_setp_struct_time, emxArray_real_T *J_setp_struct_signals_values);
extern void construct_setp_struct(const double t_in2[1], const double J_in2[1],
  double J_setp_struct_time_data[], int J_setp_struct_time_size[1], double
  c_J_setp_struct_signals_values_[], int d_J_setp_struct_signals_values_[2]);
extern void d_construct_setp_struct(const cell_wrap_16 t_in2[1], const
  cell_wrap_16 J_in2[1], double J_setp_struct_time_data[], int
  J_setp_struct_time_size[1], double c_J_setp_struct_signals_values_[], int
  d_J_setp_struct_signals_values_[2]);
extern void e_construct_setp_struct(const emxArray_cell_wrap_0 *t_in2, const
  emxArray_cell_wrap_0 *J_in2, emxArray_struct0_T *J_setp_struct);

#endif
