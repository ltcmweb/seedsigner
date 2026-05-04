#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "lvgl.h"

typedef struct {
    PyObject_HEAD
    Canvas canvas;
} CanvasObject;

extern PyTypeObject CanvasType;

static PyObject *load(PyObject *self, PyObject *args) {
    const char *data;
    Py_ssize_t len;

    if (!PyArg_ParseTuple(args, "y#", &data, &len))
        return NULL;

    CanvasObject *canvas = PyObject_New(CanvasObject, &CanvasType);
    if (!lvgl_load(&canvas->canvas, (const uint8_t*)data, len)) {
        PyErr_NoMemory();
        return NULL;
    }

    return (PyObject*)canvas;
}

static PyObject *rectangle(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x1, y1, x2, y2, fill, outline, width, radius;

    if (!PyArg_ParseTuple(args, "O!(iiii)iiii", &CanvasType, &canvas,
        &x1, &y1, &x2, &y2, &fill, &outline, &width, &radius))
        return NULL;

    lvgl_rect(&canvas->canvas, x1, y1, x2, y2, fill, outline, width, radius);

    Py_RETURN_NONE;
}

static PyObject *line(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x1, y1, x2, y2, fill;

    if (!PyArg_ParseTuple(args, "O!(iiii)i", &CanvasType, &canvas,
        &x1, &y1, &x2, &y2, &fill))
        return NULL;

    lvgl_line(&canvas->canvas, x1, y1, x2, y2, fill);

    Py_RETURN_NONE;
}

static PyObject *text(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x, y, fill;
    const char *text, *font, *anchor;

    if (!PyArg_ParseTuple(args, "O!(ii)ssis", &CanvasType, &canvas,
        &x, &y, &text, &font, &fill, &anchor))
        return NULL;

    lv_area_t box;
    lvgl_text(&canvas->canvas, x, y, fill, text, font, anchor, &box);

    return PyTuple_Pack(4, PyLong_FromLong(box.x1), PyLong_FromLong(box.y1),
                           PyLong_FromLong(box.x2), PyLong_FromLong(box.y2));
}

static PyMethodDef Methods[] = {
    {"load", load, METH_VARARGS, "Load image"},
    {"rectangle", rectangle, METH_VARARGS, "Draw rectangle"},
    {"line", line, METH_VARARGS, "Draw line"},
    {"text", text, METH_VARARGS, "Draw text"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "lvgl",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_lvgl(void) {
    if (PyType_Ready(&CanvasType) < 0)
        return NULL;

    PyObject *m = PyModule_Create(&module);
    if (!m) return NULL;

    Py_INCREF(&CanvasType);
    PyModule_AddObject(m, "Canvas", (PyObject*)&CanvasType);

    return m;
}
