#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define LOOP 10

#define RAND "rdrand %0\n\t"
#define SEED "rdseed %0\n\t"

#define RD(i)                                                                  \
  asm volatile("mov %1, %%ecx\n\t"                                             \
               "1:\n\t" i "jc 2f\n\t"                                          \
               "loop 1b\n\t"                                                   \
               "xor %0, %0\n\t"                                                \
               "2:"                                                            \
               : "=r"(v)                                                       \
               : "n"(LOOP)                                                     \
               : "rcx", "cc")

static PyObject *method_rand64(PyObject *self) {
  register unsigned long v asm("rdi");

  RD(RAND);
  return PyLong_FromUnsignedLong(v);
}

static PyObject *method_rand32(PyObject *self) {
  register unsigned v asm("edi");

  RD(RAND);
  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_rand16(PyObject *self) {
  register unsigned short v asm("di");

  RD(RAND);
  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_seed64(PyObject *self) {
  register unsigned long v asm("rdi");

  RD(SEED);
  return PyLong_FromUnsignedLong(v);
}

static PyObject *method_seed32(PyObject *self) {
  register unsigned v asm("edi");

  RD(SEED);
  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_seed16(PyObject *self) {
  register unsigned short v asm("di");

  RD(SEED);
  return PyLong_FromUnsignedLong((unsigned long)v);
}
/* Return value:
    - appropriate random number
    - 0    -> if rdrand fails
    - NULL -> if PyLong_FromUnsignedLong fails
*/
static PyMethodDef RdrandMethods[] = {
    {"rand64", (PyCFunction)method_rand64, METH_NOARGS, "rdrand 64 bit RNG"},
    {"rand32", (PyCFunction)method_rand32, METH_NOARGS, "rdrand 32 bit RNG"},
    {"rand16", (PyCFunction)method_rand16, METH_NOARGS, "rdrand 16 bit RNG"},
    {"seed64", (PyCFunction)method_seed64, METH_NOARGS, "rdseed 64 bit seed"},
    {"seed32", (PyCFunction)method_seed32, METH_NOARGS, "rdseed 32 bit seed"},
    {"seed16", (PyCFunction)method_seed16, METH_NOARGS, "rdseed 16 bit seed"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef rdrandmodule = {PyModuleDef_HEAD_INIT, "rdrand",
                                          "Python interface for rdrand", -1,
                                          RdrandMethods};

PyMODINIT_FUNC PyInit_rdrand(void) { return PyModule_Create(&rdrandmodule); }
