#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "mod_lvgl.h"

typedef struct {
    PyObject_HEAD
    Canvas canvas;
} CanvasObject;

extern PyTypeObject CanvasType;

static PyObject *Canvas_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    CanvasObject *self = (CanvasObject*)type->tp_alloc(type, 0);
    if (self) {
        self->canvas.buf = NULL;
        self->canvas.canvas = NULL;
    }
    return (PyObject*)self;
}

static int Canvas_init(CanvasObject *self, PyObject *args, PyObject *kwds) {
    const char *mode;
    int w, h;
    if (!PyArg_ParseTuple(args, "s(ii)", &mode, &w, &h))
        return -1;

    if (!mod_lvgl_canvas_init(&self->canvas, mode, w, h)) {
        PyErr_NoMemory();
        return -1;
    }

    return 0;
}

static void Canvas_dealloc(CanvasObject *self) {
    lv_free(self->canvas.buf);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *Canvas_size(CanvasObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    return PyTuple_Pack(2, PyLong_FromLong(self->canvas.w), PyLong_FromLong(self->canvas.h));
}

static PyObject *Canvas_tobytes(CanvasObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    return PyBytes_FromStringAndSize((char*)self->canvas.buf, self->canvas.size);
}

static PyObject *Canvas_setbytes(CanvasObject *self, PyObject *args) {
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "y*", &view))
        return NULL;

    memcpy(self->canvas.buf, view.buf, self->canvas.size);

    PyBuffer_Release(&view);
    Py_RETURN_NONE;
}

static PyObject *Canvas_copyto(CanvasObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x, y;
    if (!PyArg_ParseTuple(args, "O!(ii)", &CanvasType, &canvas, &x, &y))
        return NULL;

    mod_lvgl_canvas_copyto(&canvas->canvas, &self->canvas, x, y);

    Py_RETURN_NONE;
}

static PyMethodDef Canvas_methods[] = {
    {"size", (PyCFunction)Canvas_size, METH_VARARGS, "Get size"},
    {"tobytes", (PyCFunction)Canvas_tobytes, METH_VARARGS, "Get bytes"},
    {"setbytes", (PyCFunction)Canvas_setbytes, METH_VARARGS, "Set bytes"},
    {"copyto", (PyCFunction)Canvas_copyto, METH_VARARGS, "Copy to"},
    {NULL}
};

PyTypeObject CanvasType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "lvgl.Canvas",
    .tp_basicsize = sizeof(CanvasObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor)Canvas_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Canvas object",
    .tp_methods = Canvas_methods,
    .tp_init = (initproc)Canvas_init,
    .tp_new = Canvas_new,
};
