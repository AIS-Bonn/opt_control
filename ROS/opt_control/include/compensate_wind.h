/*
 * Student License - for use by students to meet course requirements and
 * perform academic research at degree granting institutions only.  Not
 * for government, commercial, or other organizational use.
 *
 * compensate_wind.h
 *
 * Code generation for function 'compensate_wind'
 *
 */

#ifndef COMPENSATE_WIND_H
#define COMPENSATE_WIND_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern void compensate_wind(const emxArray_real_T *State_in, const
  emxArray_real_T *A_wind, const emxArray_real_T *A_max_in, const
  emxArray_real_T *A_min_in, emxArray_real_T *State_out, emxArray_real_T
  *A_max_out, emxArray_real_T *A_min_out);

#endif

/* End of code generation (compensate_wind.h) */
