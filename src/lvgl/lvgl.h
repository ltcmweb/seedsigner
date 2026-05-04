#include "lvgl/lvgl.h"

typedef struct {
    uint8_t *buf;
    size_t size;
    int32_t w, h;
    lv_obj_t *canvas;
} Canvas;

void lvgl_init();
bool lvgl_load(Canvas *canvas, const uint8_t *data, size_t len);
void lvgl_rect(Canvas *canvas, int x1, int y1, int x2, int y2,
    int fill, int outline, int width, int radius);
void lvgl_line(Canvas *canvas, int x1, int y1, int x2, int y2, int fill);
void lvgl_text(Canvas *canvas, int x, int y, int fill,
    const char *text, const char *font, const char *anchor, lv_area_t *box);
bool canvas_init(Canvas *canvas, const char *mode, int w, int h);
void canvas_copyto(Canvas *canvas, Canvas *src, int x, int y);

LV_FONT_DECLARE(opensans_regular_17_4bpp);
LV_FONT_DECLARE(opensans_regular_17_4bpp_125x);
LV_FONT_DECLARE(opensans_regular_17_4bpp_150x);
LV_FONT_DECLARE(opensans_regular_17_4bpp_200x);
LV_FONT_DECLARE(opensans_semibold_18_4bpp);
LV_FONT_DECLARE(opensans_semibold_20_4bpp);
LV_FONT_DECLARE(opensans_semibold_26_4bpp);
LV_FONT_DECLARE(Inconsolata_SemiBold);
LV_FONT_DECLARE(seedsigner_icons_24_4bpp);
LV_FONT_DECLARE(seedsigner_icons_36_4bpp);
LV_FONT_DECLARE(seedsigner_icons_48_4bpp);
LV_FONT_DECLARE(Font_Awesome_6_Free_24);
LV_FONT_DECLARE(Font_Awesome_6_Free_36);
