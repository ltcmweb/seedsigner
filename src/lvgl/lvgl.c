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
    const char *text, *font, *anchor;

    if (!PyArg_ParseTuple(args, "O!(ii)ssis", &CanvasType, &canvas,
        &x, &y, &text, &font, &fill, &anchor))
        return NULL;

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_label_dsc_t dsc;
    lv_draw_label_dsc_init(&dsc);
    dsc.color = lv_color_hex(fill);
    dsc.text = text;

    if (!strcmp(font, "OpenSans-Regular-15")) {
        dsc.font = &opensans_regular_17_4bpp;
    } else if (!strcmp(font, "OpenSans-Regular-17")) {
        dsc.font = &opensans_regular_17_4bpp;
    } else if (!strcmp(font, "OpenSans-Regular-18")) {
        dsc.font = &opensans_regular_17_4bpp;
    } else if (!strcmp(font, "OpenSans-Regular-19")) {
        dsc.font = &opensans_regular_17_4bpp_125x;
    } else if (!strcmp(font, "OpenSans-Regular-20")) {
        dsc.font = &opensans_regular_17_4bpp_125x;
    } else if (!strcmp(font, "OpenSans-Regular-22")) {
        dsc.font = &opensans_regular_17_4bpp_125x;
    } else if (!strcmp(font, "OpenSans-Regular-26")) {
        dsc.font = &opensans_regular_17_4bpp_150x;
    } else if (!strcmp(font, "OpenSans-SemiBold-17")) {
        dsc.font = &opensans_semibold_18_4bpp;
    } else if (!strcmp(font, "OpenSans-SemiBold-18")) {
        dsc.font = &opensans_semibold_18_4bpp;
    } else if (!strcmp(font, "OpenSans-SemiBold-20")) {
        dsc.font = &opensans_semibold_20_4bpp;
    } else if (!strcmp(font, "OpenSans-SemiBold-26")) {
        dsc.font = &opensans_semibold_26_4bpp;
    } else if (!strcmp(font, "Inconsolata-Regular-26")) {
        dsc.font = &Inconsolata_SemiBold;
    } else if (!strcmp(font, "Inconsolata-SemiBold-20")) {
        dsc.font = &Inconsolata_SemiBold;
    } else if (!strcmp(font, "Inconsolata-SemiBold-22")) {
        dsc.font = &Inconsolata_SemiBold;
    } else if (!strcmp(font, "Inconsolata-SemiBold-24")) {
        dsc.font = &Inconsolata_SemiBold;
    } else if (!strcmp(font, "seedsigner-icons-17")) {
        dsc.font = &seedsigner_icons_24_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-22")) {
        dsc.font = &seedsigner_icons_24_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-24")) {
        dsc.font = &seedsigner_icons_24_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-26")) {
        dsc.font = &seedsigner_icons_24_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-30")) {
        dsc.font = &seedsigner_icons_36_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-34")) {
        dsc.font = &seedsigner_icons_36_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-48")) {
        dsc.font = &seedsigner_icons_48_4bpp;
    } else if (!strcmp(font, "seedsigner-icons-50")) {
        dsc.font = &seedsigner_icons_48_4bpp;
    } else if (!strcmp(font, "Font_Awesome_6_Free-Solid-900-24")) {
        dsc.font = &Font_Awesome_6_Free_24;
    } else if (!strcmp(font, "Font_Awesome_6_Free-Solid-900-26")) {
        dsc.font = &Font_Awesome_6_Free_24;
    } else if (!strcmp(font, "Font_Awesome_6_Free-Solid-900-36")) {
        dsc.font = &Font_Awesome_6_Free_36;
    }

    lv_point_t size;
    lv_text_get_size(&size, text, dsc.font, 0, 0, LV_COORD_MAX, LV_TEXT_FLAG_NONE);

    switch (anchor[0]) {
    case 'm':
        x -= size.x / 2;
        break;
    }

    switch (anchor[1]) {
    case 's':
        y -= size.y - dsc.font->base_line;
        size.y = 0;
        for (char *p = text; *p; p++)
            for (char *q = "gjpqyQ()"; *q; q++)
                if (*p == *q)
                    size.y = dsc.font->base_line;
        break;
    }

    lv_area_t coords = {x, y, LV_COORD_MAX, LV_COORD_MAX};
    lv_draw_label(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);

    return PyTuple_Pack(4, PyLong_FromLong(x), PyLong_FromLong(y),
                           PyLong_FromLong(size.x), PyLong_FromLong(size.y));
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
