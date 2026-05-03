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

LV_FONT_DECLARE(opensans_regular_17_4bpp);
LV_FONT_DECLARE(opensans_regular_17_4bpp_125x);
LV_FONT_DECLARE(opensans_regular_17_4bpp_150x);
LV_FONT_DECLARE(opensans_regular_17_4bpp_200x);
LV_FONT_DECLARE(opensans_semibold_18_4bpp);
LV_FONT_DECLARE(opensans_semibold_20_4bpp);
LV_FONT_DECLARE(opensans_semibold_26_4bpp);
LV_FONT_DECLARE(seedsigner_icons_24_4bpp);
LV_FONT_DECLARE(seedsigner_icons_36_4bpp);
LV_FONT_DECLARE(seedsigner_icons_48_4bpp);
