#include <string.h>
#include "lvgl.h"

static PyObject *Canvas_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    CanvasObject *self = (CanvasObject*)type->tp_alloc(type, 0);
    if (self) {
        self->buf = NULL;
        self->canvas = NULL;
    }
    return (PyObject*)self;
}

static int Canvas_init(CanvasObject *self, PyObject *args, PyObject *kwds) {
    const char *mode;
    int w, h;
    if (!PyArg_ParseTuple(args, "s(ii)", &mode, &w, &h))
        return -1;

    lv_color_format_t cf = LV_COLOR_FORMAT_RGB565;
    if (!strcmp(mode, "RGB")) {
        cf = LV_COLOR_FORMAT_RGB888;
        self->size = w * h * 3;
    } else if (!strcmp(mode, "RGBA")) {
        cf = LV_COLOR_FORMAT_ARGB8888;
        self->size = w * h * 4;
    } else {
        self->size = w * h * 2;
    }

    lvgl_init();
    self->buf = lv_malloc(self->size);
    if (!self->buf) {
        PyErr_NoMemory();
        return -1;
    }

    self->w = w;
    self->h = h;
    self->canvas = lv_canvas_create(lv_screen_active());
    lv_canvas_set_buffer(self->canvas, self->buf, w, h, cf);
    return 0;
}

static void Canvas_dealloc(CanvasObject *self) {
    lv_free(self->buf);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *Canvas_size(CanvasObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    return PyTuple_Pack(2, PyLong_FromLong(self->w), PyLong_FromLong(self->h));
}

static PyObject *Canvas_tobytes(CanvasObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    return PyBytes_FromStringAndSize((char*)self->buf, self->size);
}

static PyObject *Canvas_setbytes(CanvasObject *self, PyObject *args) {
    Py_buffer view;
    if (!PyArg_ParseTuple(args, "y*", &view))
        return NULL;

    memcpy(self->buf, view.buf, self->size);

    PyBuffer_Release(&view);
    Py_RETURN_NONE;
}

static PyObject *Canvas_copyto(CanvasObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x, y;
    if (!PyArg_ParseTuple(args, "O!(ii)", &CanvasType, &canvas, &x, &y))
        return NULL;

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_image_dsc_t dsc;
    lv_draw_image_dsc_init(&dsc);
    dsc.src = lv_canvas_get_image(self->canvas);

    lv_area_t coords = {x, y, x + self->w - 1, y + self->h - 1};
    lv_draw_image(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);

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
