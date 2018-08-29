//------------------------------------------------------------------------
// File:       opt_control_lib_rtwutil.h
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

#ifndef OPT_CONTROL_LIB_RTWUTIL_H
#define OPT_CONTROL_LIB_RTWUTIL_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern short _s16_s32_(int b);
extern void b_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void c_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void d_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void e_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void f_rtErrorWithMessageID(const int b, const char *c, const
  rtRunTimeErrorInfo *aInfo);
extern void g_rtErrorWithMessageID(const int b, const char *c, const
  rtRunTimeErrorInfo *aInfo);
extern void h_rtErrorWithMessageID(const int b, const char *c, const
  rtRunTimeErrorInfo *aInfo);
extern void i_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void j_rtErrorWithMessageID(const int b, const char *c, const
  rtRunTimeErrorInfo *aInfo);
extern void k_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void l_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void m_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void n_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void o_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void p_rtErrorWithMessageID(const int b, const char *c, const
  rtRunTimeErrorInfo *aInfo);
extern void q_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void r_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void rtDimSizeEqError(const int aDim1, const int aDim2, const
  rtEqualityCheckInfo *aInfo);
extern void rtDynamicBoundsError(int aIndexValue, int aLoBound, int aHiBound,
  const rtBoundsCheckInfo *aInfo);
extern void rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void rtIntegerError(const double aInteger, const rtDoubleCheckInfo *aInfo);
extern void rtIntegerOverflowError(const rtRunTimeErrorInfo *aInfo);
extern void rtNonNegativeError(const double aPositive, const rtDoubleCheckInfo
  *aInfo);
extern void rtSizeEq1DError(const int aDim1, const int aDim2, const
  rtEqualityCheckInfo *aInfo);
extern void rtSizeEqNDCheck(const int *aDims1, const int *aDims2, const
  rtEqualityCheckInfo *aInfo);
extern void rtSubAssignSizeCheck(const int *aDims1, const int aNDims1, const int
  *aDims2, const int aNDims2, const rtEqualityCheckInfo *aInfo);
extern double rt_atan2d_snf(double u0, double u1);
extern double rt_hypotd_snf(double u0, double u1);
extern double rt_powd_snf(double u0, double u1);
extern void s_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void t_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void u_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void v_rtErrorWithMessageID(const rtRunTimeErrorInfo *aInfo);
extern void w_rtErrorWithMessageID(const int b, const int c, const
  rtRunTimeErrorInfo *aInfo);

#endif
