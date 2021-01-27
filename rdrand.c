#include <Python.h>

static PyObject *method_rand64(PyObject *self)
{
    unsigned long v;

    asm volatile ( "movl $10, %%ecx\n\t"
                   ".rd_start:\n\t"
                       "rdrand %0\n\t"
                       "jc .rd_end\n\t"
                       "loop .rd_start\n\t"
                       "cmovnc %%rcx, %0\n\t"
                   ".rd_end:"
                   :"=r"(v) : : "rcx", "cc" );

    return PyLong_FromUnsignedLong(v);
}

static PyMethodDef RdrandMethods[] = {
    {"rand64", (PyCFunction)method_rand64, METH_NOARGS, "Python interface for rdrand"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef rdrandmodule = {
    PyModuleDef_HEAD_INIT,
    "rdrand",
    "Python interface for rdrand",
    -1,
    RdrandMethods
};

PyMODINIT_FUNC PyInit_rdrand(void)
{
    return PyModule_Create(&rdrandmodule);
}
