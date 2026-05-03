#include "lvgl.h"

void lvgl_init() {
    static bool init;
    if (init) return;
    init = true;

    lv_init();
    lv_display_create(0, 0);
}

static PyObject *load(PyObject *self, PyObject *args) {
    const char *data;
    Py_ssize_t len;

    if (!PyArg_ParseTuple(args, "y#", &data, &len))
        return NULL;

    lvgl_init();
    lv_image_decoder_dsc_t dsc;
    lv_image_dsc_t img_dsc = {
        .data_size = len,
        .data = (uint8_t*)data,
    };
    lv_image_decoder_args_t dec_args = { 0 };
    lv_image_decoder_open(&dsc, &img_dsc, &dec_args);

    CanvasObject *canvas = PyObject_New(CanvasObject, &CanvasType);
    canvas->w = dsc.header.w;
    canvas->h = dsc.header.h;

    switch (dsc.header.cf) {
    case LV_COLOR_FORMAT_RGB888:
        canvas->size = canvas->w * canvas->h * 3;
        break;
    case LV_COLOR_FORMAT_ARGB8888:
        canvas->size = canvas->w * canvas->h * 4;
        break;
    }
    canvas->buf = lv_malloc(canvas->size);
    if (!canvas->buf) {
        PyErr_NoMemory();
        return NULL;
    }

    memcpy(canvas->buf, dsc.decoded->data, canvas->size);
    lv_image_decoder_close(&dsc);

    canvas->canvas = lv_canvas_create(lv_screen_active());
    lv_canvas_set_buffer(canvas->canvas, canvas->buf, canvas->w, canvas->h, dsc.header.cf);

    return (PyObject*)canvas;
}

static PyObject *rectangle(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x1, y1, x2, y2, fill, outline, width, radius;

    if (!PyArg_ParseTuple(args, "O!(iiii)iiii", &CanvasType, &canvas,
        &x1, &y1, &x2, &y2, &fill, &outline, &width, &radius))
        return NULL;

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_rect_dsc_t dsc;
    lv_draw_rect_dsc_init(&dsc);
    if (fill >= 0) {
        dsc.bg_color = lv_color_hex(fill);
    } else {
        dsc.bg_opa = LV_OPA_TRANSP;
    }
    if (outline >= 0) {
        dsc.border_color = lv_color_hex(outline);
        dsc.border_width = width;
    } else {
        dsc.border_opa = LV_OPA_TRANSP;
    }
    dsc.radius = radius;

    lv_area_t coords = {x1, y1, x2 - 1, y2 - 1};
    lv_draw_rect(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);

    Py_RETURN_NONE;
}

static PyObject *line(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x1, y1, x2, y2, fill;

    if (!PyArg_ParseTuple(args, "O!(iiii)i", &CanvasType, &canvas,
        &x1, &y1, &x2, &y2, &fill))
        return NULL;

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_line_dsc_t dsc;
    lv_draw_line_dsc_init(&dsc);
    dsc.color = lv_color_hex(fill);
    dsc.width = 1;
    dsc.p1.x = x1;
    dsc.p1.y = y1;
    dsc.p2.x = x2;
    dsc.p2.y = y2;

    lv_draw_line(&layer, &dsc);
    lv_canvas_finish_layer(canvas->canvas, &layer);

    Py_RETURN_NONE;
}

static PyObject *text(PyObject *self, PyObject *args) {
    CanvasObject *canvas;
    int x, y, fill;
    const char *text, *anchor;

    if (!PyArg_ParseTuple(args, "O!(ii)sis", &CanvasType, &canvas,
        &x, &y, &text, &fill, &anchor))
        return NULL;

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_label_dsc_t dsc;
    lv_draw_label_dsc_init(&dsc);
    dsc.color = lv_color_hex(fill);
    dsc.font = LV_FONT_DEFAULT;
    dsc.text = text;

    lv_point_t size;
    lv_text_get_size(&size, text, dsc.font, 0, 0, LV_COORD_MAX, LV_TEXT_FLAG_NONE);

    switch (anchor[0]) {
    case 'm':
        x -= size.x / 2;
        break;
    }

    switch (anchor[1]) {
    case 's':
        y -= size.y - (size.y + 3) / 4;
        break;
    }

    lv_area_t coords = {x, y, LV_COORD_MAX, LV_COORD_MAX};
    lv_draw_label(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);

    return PyTuple_Pack(2, PyLong_FromLong(size.x), PyLong_FromLong(size.y));
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

extern PyTypeObject CanvasType;

PyMODINIT_FUNC PyInit_lvgl(void) {
    if (PyType_Ready(&CanvasType) < 0)
        return NULL;

    PyObject *m = PyModule_Create(&module);
    if (!m) return NULL;

    Py_INCREF(&CanvasType);
    PyModule_AddObject(m, "Canvas", (PyObject*)&CanvasType);

    return m;
}
