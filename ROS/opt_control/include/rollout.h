/*
 * Student License - for use by students to meet course requirements and
 * perform academic research at degree granting institutions only.  Not
 * for government, commercial, or other organizational use.
 *
 * rollout.h
 *
 * Code generation for function 'rollout'
 *
 */

#ifndef ROLLOUT_H
#define ROLLOUT_H

/* Include files */
#include <stddef.h>
#include <stdlib.h>
#include "rtwtypes.h"
#include "opt_control_lib_types.h"

/* Function Declarations */
extern void rollout(const emxArray_real_T *P_init, const emxArray_real_T *V_init,
                    const emxArray_real_T *A_init, const emxArray_struct0_T
                    *J_setp_struct, double T, double ts, emxArray_struct2_T *P,
                    emxArray_struct2_T *V, emxArray_struct2_T *A,
                    emxArray_struct2_T *J);

#endif

/* End of code generation (rollout.h) */
