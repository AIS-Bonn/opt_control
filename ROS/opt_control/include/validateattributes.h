//------------------------------------------------------------------------
// File:       validateattributes.h
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

#ifndef VALIDATEATTRIBUTES_H
#define VALIDATEATTRIBUTES_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern void b_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[3]);
extern void c_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void d_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void e_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void f_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void g_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void h_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void i_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void j_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void k_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void l_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void m_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void n_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void o_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void p_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void q_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void r_validateattributes(const emxArray_boolean_T *a, const double
  attributes_f2[2]);
extern void s_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[3]);
extern void t_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void u_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void v_validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void validateattributes(const emxArray_real_T *a, const double
  attributes_f2[2]);
extern void w_validateattributes(const emxArray_int16_T *a, const double
  attributes_f2[3]);

#endif
