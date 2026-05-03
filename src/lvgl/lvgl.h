#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "lvgl/lvgl.h"

void lvgl_init();

typedef struct {
    PyObject_HEAD
    uint8_t *buf;
    size_t size;
    int32_t w, h;
    lv_obj_t *canvas;
} CanvasObject;

extern PyTypeObject CanvasType;
