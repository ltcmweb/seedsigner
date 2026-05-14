#include "lvgl.h"

typedef struct {
    uint8_t *buf;
    size_t size;
    int32_t w, h;
    lv_obj_t *canvas;
} Canvas;

bool mod_lvgl_load(Canvas *canvas, const uint8_t *data, size_t len);
void mod_lvgl_rect(Canvas *canvas, int x1, int y1, int x2, int y2,
    uint32_t fill, uint32_t outline, int width, int radius);
void mod_lvgl_line(Canvas *canvas, int x1, int y1, int x2, int y2, uint32_t fill);
void mod_lvgl_arc(Canvas *canvas, int x1, int y1, int x2, int y2,
    int start, int end, uint32_t fill, int width);
void mod_lvgl_text(Canvas *canvas, int x, int y, uint32_t fill,
    const char *text, const char *font, const char *anchor,
    int stroke_width, uint32_t stroke_fill, lv_area_t *box);
void mod_lvgl_putalpha(Canvas *canvas, int alpha);
bool mod_lvgl_canvas_init(Canvas *canvas, const char *mode, int w, int h, bool visible);
void mod_lvgl_canvas_del(Canvas *canvas);
void mod_lvgl_canvas_copyto(Canvas *canvas, Canvas *src, int x, int y);

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
