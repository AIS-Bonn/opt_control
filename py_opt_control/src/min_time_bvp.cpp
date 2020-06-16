#include "rt_nonfinite.h"
#include "opt_control_lib.h"
#include "opt_control_lib_terminate.h"
#include "opt_control_lib_emxAPI.h"
#include "opt_control_lib_initialize.h"
#include <iostream>

/* Function Declarations */
static emxArray_boolean_T *argInit_1xUnbounded_boolean_T();
static emxArray_real_T *argInit_Unboundedx1_real_T();
static emxArray_real_T *argInit_Unboundedx3_real_T();
static emxArray_int16_T *c_argInit_Unboundedx2xUnbounded();
static emxArray_real_T *c_argInit_Unboundedx5xUnbounded();
static emxArray_boolean_T *c_argInit_UnboundedxUnbounded_b();
static emxArray_real_T *c_argInit_UnboundedxUnbounded_r();

#define num_traj 1
#define out_stride 32

bool b_sync_V = true;
bool b_sync_A = true;
bool b_sync_J = false;
bool b_sync_W = true;

bool b_comp_global = false;
bool b_rotate = false;
bool b_best_solution = true;
bool b_hard_vel_limit = false;
bool b_catch_up = true;

double ts_rollout = 0.1;


/* Function Definitions */
static emxArray_boolean_T *argInit_1xUnbounded_boolean_T()
{
  emxArray_boolean_T *result;
  static int iv182[2] = { 1, num_traj };
  int idx1;
  result = emxCreateND_boolean_T(2, iv182);
  for (idx1 = 0; idx1 < result->size[1U]; idx1++) {
    result->data[result->size[0] * idx1] = false;
  }
  return result;
}

static emxArray_real_T *argInit_Unboundedx1_real_T(int num_axes)
{
  emxArray_real_T *result;
  static int iv180[1] = { num_axes };
  int idx0;
  result = emxCreateND_real_T(1, iv180);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    result->data[idx0] = 0.0;
  }
  return result;
}

static emxArray_real_T *argInit_Unboundedx3_real_T(int num_axes)
{
  emxArray_real_T *result;
  static int iv177[2] = { num_axes, 3 };
  int idx0;
  int idx1;
  result = emxCreateND_real_T(2, iv177);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    for (idx1 = 0; idx1 < 3; idx1++) {
      result->data[idx0 + result->size[0] * idx1] = 0.0;
    }
  }
  return result;
}

static emxArray_int16_T *c_argInit_Unboundedx2xUnbounded(int num_axes)
{
  emxArray_int16_T *result;
  static int iv183[3] = { num_axes, 2, num_traj };
  int idx0;
  int idx1;
  int idx2;
  result = emxCreateND_int16_T(3, iv183);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    for (idx1 = 0; idx1 < 2; idx1++) {
      for (idx2 = 0; idx2 < result->size[2U]; idx2++) {
        result->data[(idx0 + result->size[0] * idx1) + result->size[0] * result->size[1] * idx2] = 0;
      }
    }
  }
  return result;
}

static emxArray_real_T *c_argInit_Unboundedx5xUnbounded(int num_axes)
{
  emxArray_real_T *result;
  static int iv178[3] = { num_axes, 5, num_traj };
  int idx0;
  int idx1;
  int idx2;
  result = emxCreateND_real_T(3, iv178);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    for (idx1 = 0; idx1 < 5; idx1++) {
      for (idx2 = 0; idx2 < result->size[2U]; idx2++) {
        result->data[(idx0 + result->size[0] * idx1) + result->size[0] * result->size[1] * idx2] = 0.0;
      }
    }
  }
  return result;
}

static emxArray_boolean_T *c_argInit_UnboundedxUnbounded_b(int num_axes)
{
  emxArray_boolean_T *result;
  static int iv181[2] = { num_axes, num_traj };
  int idx0;
  int idx1;
  result = emxCreateND_boolean_T(2, iv181);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    for (idx1 = 0; idx1 < result->size[1U]; idx1++) {
      result->data[idx0 + result->size[0] * idx1] = false;
    }
  }
  return result;
}

static emxArray_real_T *c_argInit_UnboundedxUnbounded_r(int num_axes)
{
  emxArray_real_T *result;
  static int iv179[2] = { num_axes, num_traj };
  int idx0;
  int idx1;
  result = emxCreateND_real_T(2, iv179);
  for (idx0 = 0; idx0 < result->size[0U]; idx0++) {
    for (idx1 = 0; idx1 < result->size[1U]; idx1++) {
      result->data[idx0 + result->size[0] * idx1] = 0.0;
    }
  }
  return result;
}

extern "C"
void min_time_bvp(
    int num_axes,
    double* p0, double* v0, double* a0,
    double* p1, double* v1, double* a1,
    double V_min, double V_max,
    double A_min, double A_max,
    double J_min, double J_max,
    double* t,
    double* j){

  opt_control_lib_initialize();

  //Inputs
  emxArray_real_T *State_start_in;
  emxArray_real_T *Waypoints_in;
  emxArray_real_T *V_max_in;
  emxArray_real_T *V_min_in;
  emxArray_real_T *A_max_in;
  emxArray_real_T *A_min_in;
  emxArray_real_T *J_max_in;
  emxArray_real_T *J_min_in;
  emxArray_real_T *A_global_in;
  emxArray_boolean_T *b_sync_V_in;
  emxArray_boolean_T *b_sync_A_in;
  emxArray_boolean_T *b_sync_J_in;
  emxArray_boolean_T *b_sync_W_in;
  emxArray_boolean_T *b_rotate_in;
  emxArray_boolean_T *b_best_solution_in;
  emxArray_boolean_T *b_hard_vel_limit_in;
  emxArray_boolean_T *b_catch_up_in;
  bool b_comp_global_in;
  emxArray_int16_T *solution_in;

  //Outputs
  emxArray_struct0_T *J_setp_struct;
  emxArray_int16_T *solution_out;
  emxArray_real_T *T_waypoints;
  emxArray_real_T *P_rollout;
  emxArray_real_T *V_rollout;
  emxArray_real_T *A_rollout;
  emxArray_real_T *J_rollout;
  emxArray_real_T *t_rollout;
  emxInitArray_struct0_T(&J_setp_struct, 2);
  emxInitArray_int16_T(&solution_out, 3);
  emxInitArray_real_T(&T_waypoints, 2);
  emxInitArray_real_T(&P_rollout, 2);
  emxInitArray_real_T(&V_rollout, 2);
  emxInitArray_real_T(&A_rollout, 2);
  emxInitArray_real_T(&J_rollout, 2);
  emxInitArray_real_T(&t_rollout, 2);


  State_start_in = argInit_Unboundedx3_real_T(num_axes);
  Waypoints_in = c_argInit_Unboundedx5xUnbounded(num_axes);
  V_max_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  V_min_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  A_max_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  A_min_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  J_max_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  J_min_in = c_argInit_UnboundedxUnbounded_r(num_axes);
  A_global_in = argInit_Unboundedx1_real_T(num_axes);
  b_sync_V_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_sync_A_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_sync_J_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_sync_W_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_rotate_in = argInit_1xUnbounded_boolean_T();
  b_best_solution_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_hard_vel_limit_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  b_catch_up_in = c_argInit_UnboundedxUnbounded_b(num_axes);
  solution_in = c_argInit_Unboundedx2xUnbounded(num_axes);

  for (int idx_axis = 0; idx_axis < num_axes; idx_axis++) {

      State_start_in->data[idx_axis + State_start_in->size[0] * 0] = p0[idx_axis];
      State_start_in->data[idx_axis + State_start_in->size[0] * 1] = v0[idx_axis];
      State_start_in->data[idx_axis + State_start_in->size[0] * 2] = a0[idx_axis];

      Waypoints_in->data[(idx_axis + Waypoints_in->size[0] * 0)] = p1[idx_axis];
      Waypoints_in->data[(idx_axis + Waypoints_in->size[0] * 1)] = v1[idx_axis];
      Waypoints_in->data[(idx_axis + Waypoints_in->size[0] * 2)] = a1[idx_axis];

      V_max_in->data[idx_axis] = V_max;
      V_min_in->data[idx_axis] = V_min;
      A_max_in->data[idx_axis] = A_max;
      A_min_in->data[idx_axis] = A_min;
      J_max_in->data[idx_axis] = J_max;
      J_min_in->data[idx_axis] = J_min;

      A_global_in->data[idx_axis]  = 0;
      b_comp_global_in             = b_comp_global;
      b_sync_V_in->data[idx_axis] = b_sync_V;
      b_sync_A_in->data[idx_axis] = b_sync_A;
      b_sync_J_in->data[idx_axis] = b_sync_J;
      b_sync_W_in->data[idx_axis] = b_sync_W;
      b_rotate_in->data[b_rotate_in->size[0] * idx_axis]  = b_rotate;
      b_best_solution_in->data[idx_axis]   = b_best_solution;
      b_hard_vel_limit_in->data[idx_axis] = b_hard_vel_limit;
      b_catch_up_in->data[idx_axis]             = b_catch_up;
  }

  // State_start_in->data[0 + State_start_in->size[0] * 0] = 0.6;
  // State_start_in->data[1 + State_start_in->size[0] * 0] = 0.9;
  // std::cout << State_start_in->data[3];

    opt_control_lib(
        State_start_in,
        Waypoints_in,
        V_max_in, V_min_in, A_max_in,
        A_min_in, J_max_in, J_min_in,
        A_global_in,
        b_comp_global_in,
        b_sync_V_in,
        b_sync_A_in,
        b_sync_J_in,
        b_sync_W_in,
        b_rotate_in,
        b_best_solution_in,
        b_hard_vel_limit_in,
        b_catch_up_in,
        solution_in,
        ts_rollout,
        J_setp_struct,
        solution_out,
        T_waypoints,
        P_rollout,
        V_rollout,
        A_rollout,
        J_rollout,
        t_rollout);

  for (int idx_axis = 0; idx_axis < num_axes; idx_axis++) {
    int pts = *(J_setp_struct[0].data[idx_axis].time->size);
    for (int i=0; i < pts; i++) {
       t[i+idx_axis*out_stride] = J_setp_struct[0].data[idx_axis].time->data[i];
       j[i+idx_axis*out_stride] = J_setp_struct[0].data[idx_axis].signals.values->data[i];
    }
  }

  emxDestroyArray_real_T(J_rollout);
  emxDestroyArray_real_T(A_rollout);
  emxDestroyArray_real_T(V_rollout);
  emxDestroyArray_real_T(P_rollout);
  emxDestroyArray_real_T(t_rollout);
  emxDestroyArray_real_T(T_waypoints);
  emxDestroyArray_int16_T(solution_out);
  emxDestroyArray_struct0_T(J_setp_struct);
  emxDestroyArray_int16_T(solution_in);
  emxDestroyArray_boolean_T(b_catch_up_in);
  emxDestroyArray_boolean_T(b_hard_vel_limit_in);
  emxDestroyArray_boolean_T(b_best_solution_in);
  emxDestroyArray_boolean_T(b_rotate_in);
  emxDestroyArray_boolean_T(b_sync_W_in);
  emxDestroyArray_boolean_T(b_sync_J_in);
  emxDestroyArray_boolean_T(b_sync_A_in);
  emxDestroyArray_boolean_T(b_sync_V_in);
  emxDestroyArray_real_T(A_global_in);
  emxDestroyArray_real_T(J_min_in);
  emxDestroyArray_real_T(J_max_in);
  emxDestroyArray_real_T(A_min_in);
  emxDestroyArray_real_T(A_max_in);
  emxDestroyArray_real_T(V_min_in);
  emxDestroyArray_real_T(V_max_in);
  emxDestroyArray_real_T(Waypoints_in);
  emxDestroyArray_real_T(State_start_in);

  opt_control_lib_terminate();

}
