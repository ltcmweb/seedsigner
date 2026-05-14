#include <string.h>
#include "mod_lvgl.h"

bool mod_lvgl_load(Canvas *canvas, const uint8_t *data, size_t len) {
    lv_image_decoder_dsc_t dsc;
    lv_image_dsc_t img_dsc = {
        .data_size = len,
        .data = data,
    };
    lv_image_decoder_args_t dec_args = { 0 };
    lv_image_decoder_open(&dsc, &img_dsc, &dec_args);

    canvas->w = dsc.header.w;
    canvas->h = dsc.header.h;
    canvas->canvas = NULL;

    switch (dsc.header.cf) {
    case LV_COLOR_FORMAT_RGB888:
        canvas->size = canvas->w * canvas->h * 3;
        break;
    case LV_COLOR_FORMAT_ARGB8888:
        canvas->size = canvas->w * canvas->h * 4;
        break;
    }

    canvas->buf = lv_malloc(canvas->size);
    if (!canvas->buf) return false;

    memcpy(canvas->buf, dsc.decoded->data, canvas->size);
    lv_image_decoder_close(&dsc);

    canvas->canvas = lv_canvas_create(lv_screen_active());
    if (!canvas->canvas) return false;

    lv_obj_add_flag(canvas->canvas, LV_OBJ_FLAG_HIDDEN);
    lv_canvas_set_buffer(canvas->canvas, canvas->buf, canvas->w, canvas->h, dsc.header.cf);

    return true;
}

void mod_lvgl_rect(Canvas *canvas, int x1, int y1, int x2, int y2,
    uint32_t fill, uint32_t outline, int width, int radius) {

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_rect_dsc_t dsc;
    lv_draw_rect_dsc_init(&dsc);
    dsc.bg_color = lv_color_hex(fill);
    dsc.bg_opa = fill >> 24;
    dsc.border_color = lv_color_hex(outline);
    dsc.border_opa = outline >> 24;
    dsc.border_width = width;
    dsc.radius = radius;

    lv_area_t coords = {x1, y1, x2, y2};
    lv_draw_rect(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);
}

void mod_lvgl_line(Canvas *canvas, int x1, int y1, int x2, int y2, uint32_t fill) {
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
}

void mod_lvgl_arc(Canvas *canvas, int x1, int y1, int x2, int y2,
    int start, int end, uint32_t fill, int width) {

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_arc_dsc_t dsc;
    lv_draw_arc_dsc_init(&dsc);
    dsc.color = lv_color_hex(fill);
    dsc.width = width;
    dsc.start_angle = start;
    dsc.end_angle = end;
    dsc.center.x = (x1 + x2) / 2;
    dsc.center.y = (y1 + y2) / 2;
    dsc.radius = (x2 - x1) / 2;

    lv_draw_arc(&layer, &dsc);
    lv_canvas_finish_layer(canvas->canvas, &layer);
}

void mod_lvgl_text(Canvas *canvas, int x, int y, uint32_t fill,
    const char *text, const char *font, const char *anchor,
    int stroke_width, uint32_t stroke_fill, lv_area_t *box) {

    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_label_dsc_t dsc;
    lv_draw_label_dsc_init(&dsc);
    dsc.color = lv_color_hex(fill);
    dsc.opa = fill >> 24;
    dsc.text = text;
    dsc.outline_stroke_color = lv_color_hex(stroke_fill);
    dsc.outline_stroke_opa = stroke_fill >> 24;
    dsc.outline_stroke_width = stroke_width;

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
    } else if (!strcmp(font, "OpenSans-Regular-24")) {
        dsc.font = &opensans_regular_17_4bpp_150x;
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
    } else if (!strcmp(font, "Inconsolata-Regular-23")) {
        dsc.font = &Inconsolata_SemiBold;
    } else if (!strcmp(font, "Inconsolata-Regular-24")) {
        dsc.font = &Inconsolata_SemiBold;
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
    case 'r':
        x -= size.x;
        break;
    }

    switch (anchor[1]) {
    case 'm':
        y -= size.y / 2;
        break;
    case 's':
        y -= size.y - dsc.font->base_line;
        size.y = 0;
        for (const char *p = text; *p; p++)
            for (char *q = "gjpqyQ()"; *q; q++)
                if (*p == *q)
                    size.y = dsc.font->base_line;
        break;
    }

    lv_area_t coords = {x, y, LV_COORD_MAX, LV_COORD_MAX};
    lv_draw_label(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);

    box->x1 = x;
    box->y1 = y;
    box->x2 = size.x;
    box->y2 = size.y;
}

void mod_lvgl_putalpha(Canvas *canvas, int alpha) {
    uint8_t *p = canvas->buf + 3;
    for (; p < canvas->buf + canvas->size; p += 4)
        *p = alpha;
}

bool mod_lvgl_canvas_init(Canvas *canvas, const char *mode, int w, int h, bool visible) {
    lv_color_format_t cf = LV_COLOR_FORMAT_RGB565;
    if (!strcmp(mode, "RGB")) {
        cf = LV_COLOR_FORMAT_RGB888;
        canvas->size = w * h * 3;
    } else if (!strcmp(mode, "RGBA")) {
        cf = LV_COLOR_FORMAT_ARGB8888;
        canvas->size = w * h * 4;
    } else {
        canvas->size = w * h * 2;
    }

    canvas->w = w;
    canvas->h = h;
    canvas->canvas = NULL;

    canvas->buf = lv_malloc_zeroed(canvas->size);
    if (!canvas->buf) return false;

    canvas->canvas = lv_canvas_create(lv_screen_active());
    if (!canvas->canvas) return false;

    if (!visible) lv_obj_add_flag(canvas->canvas, LV_OBJ_FLAG_HIDDEN);
    lv_canvas_set_buffer(canvas->canvas, canvas->buf, w, h, cf);
    return true;
}

void mod_lvgl_canvas_del(Canvas *canvas) {
    if (canvas->canvas) {
        lv_obj_delete(canvas->canvas);
        canvas->canvas = NULL;
    }
    if (canvas->buf) {
        lv_free(canvas->buf);
        canvas->buf = NULL;
    }
}

void mod_lvgl_canvas_copyto(Canvas *canvas, Canvas *src, int x, int y) {
    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_image_dsc_t dsc;
    lv_draw_image_dsc_init(&dsc);
    dsc.src = lv_canvas_get_image(src->canvas);

    lv_area_t coords = {x, y, x + src->w - 1, y + src->h - 1};
    lv_draw_image(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);
}
