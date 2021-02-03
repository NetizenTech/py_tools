/*
Python interface for RNG (Cryptographic Co-Processor). Coded by Wojciech Lawren.

Copyright (C) 2021, Wojciech Lawren, All rights reserved.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

References:
  https://www.amd.com/system/files/TechDocs/amd-random-number-generator.pdf
  https://software.intel.com/content/www/us/en/develop/articles/intel-digital-random-number-generator-drng-software-implementation-guide.html

Compilation:
  /opt/AMD/aocc-compiler-2.x.x/bin/clang -march=native -O3 -fPIC -c -fwrapv rdrand.c -o rdrand.o
  /opt/AMD/aocc-compiler-2.x.x/bin/clang -flto -shared -nostdlib rdrand.o -o rdrand.so

Return value:
  - appropriate random number
  - 0    -> if rdrand fails
  - NULL -> if PyLong_FromUnsignedLong fails
*/
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define LOOP 10

static PyObject *method_rand64(PyObject *self) {
  register unsigned long v asm("rdi");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdrandq %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncq %%rcx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong(v);
}

static PyObject *method_rand32(PyObject *self) {
  register unsigned v asm("edi");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdrandl %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncl %%ecx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_rand16(PyObject *self) {
  register unsigned short v asm("di");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdrandw %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncw %%cx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_seed64(PyObject *self) {
  register unsigned long v asm("rdi");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdseedq %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncq %%rcx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong(v);
}

static PyObject *method_seed32(PyObject *self) {
  register unsigned v asm("edi");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdseedl %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncl %%ecx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong((unsigned long)v);
}

static PyObject *method_seed16(PyObject *self) {
  register unsigned short v asm("di");

  asm volatile("movl %1, %%ecx\n\t"
               "1:\n\t"
               "rdseedw %0\n\t"
               "jc 2f\n\t"
               "loop 1b\n\t"
               "cmovncw %%cx, %0\n\t"
               "2:"
               : "=r"(v)
               : "n"(LOOP)
               : "rcx", "cc");

  return PyLong_FromUnsignedLong((unsigned long)v);
}
/* module definition */
static PyMethodDef RdrandMethods[] = {{"rand64", (PyCFunction)method_rand64, METH_NOARGS, "rdrand 64 bit RNG"},
                                      {"rand32", (PyCFunction)method_rand32, METH_NOARGS, "rdrand 32 bit RNG"},
                                      {"rand16", (PyCFunction)method_rand16, METH_NOARGS, "rdrand 16 bit RNG"},
                                      {"seed64", (PyCFunction)method_seed64, METH_NOARGS, "rdseed 64 bit seed"},
                                      {"seed32", (PyCFunction)method_seed32, METH_NOARGS, "rdseed 32 bit seed"},
                                      {"seed16", (PyCFunction)method_seed16, METH_NOARGS, "rdseed 16 bit seed"},
                                      {NULL, NULL, 0, NULL}};

static struct PyModuleDef rdrandmodule = {PyModuleDef_HEAD_INIT, "rdrand", "Python interface for RNG", -1,
                                          RdrandMethods};

PyMODINIT_FUNC PyInit_rdrand(void) { return PyModule_Create(&rdrandmodule); }
