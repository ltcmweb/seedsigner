#include <string.h>
#include "lvgl.h"

void lvgl_init() {
    static bool init;
    if (init) return;
    init = true;

    lv_init();
    lv_display_create(0, 0);
}

bool lvgl_load(Canvas *canvas, const uint8_t *data, size_t len) {
    lvgl_init();
    lv_image_decoder_dsc_t dsc;
    lv_image_dsc_t img_dsc = {
        .data_size = len,
        .data = data,
    };
    lv_image_decoder_args_t dec_args = { 0 };
    lv_image_decoder_open(&dsc, &img_dsc, &dec_args);

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
    if (!canvas->buf) return false;

    memcpy(canvas->buf, dsc.decoded->data, canvas->size);
    lv_image_decoder_close(&dsc);

    canvas->canvas = lv_canvas_create(lv_screen_active());
    lv_canvas_set_buffer(canvas->canvas, canvas->buf, canvas->w, canvas->h, dsc.header.cf);

    return true;
}

void lvgl_rect(Canvas *canvas, int x1, int y1, int x2, int y2,
    int fill, int outline, int width, int radius) {

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
}

void lvgl_line(Canvas *canvas, int x1, int y1, int x2, int y2, int fill) {
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

void lvgl_text(Canvas *canvas, int x, int y, int fill,
    const char *text, const char *font, const char *anchor, lv_area_t *box) {

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

bool canvas_init(Canvas *canvas, const char *mode, int w, int h) {
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

    lvgl_init();
    canvas->buf = lv_malloc(canvas->size);
    if (!canvas->buf) return false;

    canvas->w = w;
    canvas->h = h;
    canvas->canvas = lv_canvas_create(lv_screen_active());
    lv_canvas_set_buffer(canvas->canvas, canvas->buf, w, h, cf);
    return true;
}

void canvas_copyto(Canvas *canvas, Canvas *src, int x, int y) {
    lv_layer_t layer;
    lv_canvas_init_layer(canvas->canvas, &layer);

    lv_draw_image_dsc_t dsc;
    lv_draw_image_dsc_init(&dsc);
    dsc.src = lv_canvas_get_image(src->canvas);

    lv_area_t coords = {x, y, x + src->w - 1, y + src->h - 1};
    lv_draw_image(&layer, &dsc, &coords);
    lv_canvas_finish_layer(canvas->canvas, &layer);
}
