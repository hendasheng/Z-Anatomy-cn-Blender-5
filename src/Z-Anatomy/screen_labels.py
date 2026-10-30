bl_info = {'name': 'Z-Anatomy UI 文字', 'author': 'hendasheng', 'version': (1, 0, 1), 'blender': (5, 0, 0), 'category': '3D View'}

import bpy
import blf
import re
import os
import tempfile
from mathutils import Vector, Matrix
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.app.handlers import persistent

_handle = None
_hidden = []  # (text datablock, last non-empty body); visibility is never changed.
_font = 0
_font_path = None
_labels = []
_dirty = True
_BODY_KEY = '_zanatomy_ui_body'
_lines_hidden = []
_leader_objects = []


def is_leader_line(obj):
    # Localized duplicate names often lose their .j suffix. Identify actual
    # two-point leaders by geometry; keep four-point cross-section helpers.
    return (obj.type == 'MESH' and len(obj.data.vertices) == 2
            and len(obj.data.edges) == 1 and len(obj.data.polygons) == 0)


def sync_leader_lines():
    if bpy.context.window_manager.za_show_names:
        for obj, was_hidden in _lines_hidden:
            try:
                obj.hide_viewport = was_hidden
            except ReferenceError:
                pass
        _lines_hidden.clear()
        return
    known = set()
    for obj, _ in _lines_hidden:
        try:
            known.add(obj.as_pointer())
            if not obj.hide_viewport:
                obj.hide_viewport = True
        except ReferenceError:
            pass
    for obj in _leader_objects:
        if is_leader_line(obj):
            if obj.as_pointer() not in known:
                _lines_hidden.append((obj, obj.hide_viewport))
                obj.hide_viewport = True


def names_changed(self, context):
    sync_leader_lines()
    redraw()

def is_label(obj):
    return obj.type == 'FONT' and '\x00' not in obj.data.body


def redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def stop():
    global _handle, _font, _font_path
    if _handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
        _handle = None
    if bpy.app.timers.is_registered(maintain_hidden):
        bpy.app.timers.unregister(maintain_hidden)
    for data, body in _hidden:
        try:
            if not data.body:
                data.body = data.get(_BODY_KEY, body)
            if _BODY_KEY in data:
                del data[_BODY_KEY]
        except ReferenceError:
            pass
    _hidden.clear()
    _labels.clear()
    for obj, was_hidden in _lines_hidden:
        try:
            obj.hide_viewport = was_hidden
        except ReferenceError:
            pass
    _lines_hidden.clear()
    if _font_path:
        blf.unload(_font_path)
        os.unlink(_font_path)
        _font_path = None
    _font = 0
    redraw()


def maintain_hidden():
    global _dirty
    # Keep actual objects and all visibility flags intact for atlas operators.
    if _handle is None:
        return None
    sync_leader_lines()
    if not _dirty:
        return 0.3
    _dirty = False
    live = []
    for data, body in _hidden:
        try:
            data.as_pointer()
            if data.name in bpy.data.curves:
                live.append((data, body))
        except ReferenceError:
            pass
    _hidden[:] = live
    known = {data.as_pointer(): index for index, (data, _) in enumerate(_hidden)}
    _labels.clear()
    _leader_objects[:] = [o for o in bpy.context.scene.objects if is_leader_line(o)]
    for obj in bpy.context.scene.objects:
        if is_label(obj):
            _labels.append(obj)
            data = obj.data
            index = known.get(data.as_pointer())
            if index is None:
                known[data.as_pointer()] = len(_hidden)
                body = data.body or data.get(_BODY_KEY, '')
                _hidden.append((data, body))
                data[_BODY_KEY] = body
            elif data.body:
                # Language operators continue writing to the original text data.
                _hidden[index] = (data, data.body)
                data[_BODY_KEY] = data.body
            if data.body:
                data.body = ''
    redraw()
    return 0.3


def start():
    global _handle, _font, _font_path, _dirty
    stop()
    # Reuse the packed atlas font rather than the default font without CJK glyphs.
    _font = 0
    for font in bpy.data.fonts:
        if font.packed_file or 'SourceHan' in font.name or 'CJK' in font.name:
            try:
                path = bpy.path.abspath(font.filepath)
                if font.packed_file:
                    with tempfile.NamedTemporaryFile(suffix='.otf', delete=False) as output:
                        output.write(font.packed_file.data)
                        path = output.name
                    _font_path = path
                _font = blf.load(path)
                if _font >= 0:
                    break
            except RuntimeError:
                _font = 0
    _handle = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')
    _dirty = True
    maintain_hidden()
    bpy.app.timers.register(maintain_hidden, first_interval=0.3)


def draw():
    ctx = bpy.context
    if not ctx.window_manager.za_show_names:
        return
    if not ctx.region or not ctx.region_data or not ctx.space_data.overlay.show_overlays:
        return
    blf.size(_font, ctx.window_manager.za_screen_font_size)
    blf.enable(_font, blf.SHADOW)
    blf.shadow(_font, 3, 0, 0, 0, 1)
    blf.shadow_offset(_font, 1, -1)
    bodies = {}
    for data, body in _hidden:
        try:
            bodies[data.as_pointer()] = body
        except ReferenceError:
            continue
    try:
        # Draw the original visible text objects, regardless of selection.
        for obj in tuple(_labels):
            try:
                obj.name
            except ReferenceError:
                continue
            if not is_label(obj):
                continue
            if not obj.visible_get(view_layer=ctx.view_layer, viewport=ctx.space_data):
                continue
            center = obj.matrix_world.translation
            point = location_3d_to_region_2d(ctx.region, ctx.region_data, center)
            if point is None:
                continue
            clip = ctx.region_data.perspective_matrix @ center.to_4d()
            if clip.w <= 0:
                continue
            depth = clip.z / clip.w
            if not -1 <= depth <= 1:
                continue
            size = ctx.window_manager.za_screen_font_size
            # Project the original text's em height, including object/parent scale.
            # Screen-aligned view-up avoids shrinking letters when viewed edge-on.
            scale = obj.matrix_world.to_scale()
            height_world = obj.data.size * max(abs(scale.x), abs(scale.y))
            up = ctx.region_data.view_rotation @ Vector((0, 1, 0))
            top = location_3d_to_region_2d(ctx.region, ctx.region_data, center + up * height_world)
            if top is None:
                continue
            size = max(1, min(size, round((top - point).length)))
            blf.size(_font, size)
            text = obj.data.body or bodies.get(obj.data.as_pointer(), '')
            for line_index, line in enumerate(text.splitlines()):
                width, height = blf.dimensions(_font, line)
                x, y = point.x, point.y - line_index * size * obj.data.space_line
                if obj.data.align_x == 'CENTER':
                    x -= width / 2
                elif obj.data.align_x == 'RIGHT':
                    x -= width
                blf.position(_font, x, y, 0)
                blf.color(_font, 1, 1, 1, 1)
                blf.draw(_font, line)
    finally:
        blf.disable(_font, blf.SHADOW)


class ZA_OT_screen_labels(bpy.types.Operator):
    bl_idname = 'zanatomy.screen_labels'
    bl_label = '切换屏幕名称'

    def execute(self, context):
        if _handle is None:
            start()
        else:
            stop()
        return {'FINISHED'}


class ZA_PT_screen_labels(bpy.types.Panel):
    bl_label = '名称文字'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Z-Anatomy'

    def draw(self, context):
        self.layout.prop(context.window_manager, 'za_show_names')
        self.layout.prop(context.window_manager, 'za_screen_font_size')


@persistent
def before_load(_):
    stop()


@persistent
def geometry_changed(scene=None, depsgraph=None):
    global _dirty
    if depsgraph is None or any(
        isinstance(update.id, bpy.types.Curve)
        or (isinstance(update.id, bpy.types.Object) and update.id.type == 'FONT'
            and update.is_updated_geometry)
        for update in depsgraph.updates
    ):
        _dirty = True


@persistent
def restore_before_undo(_):
    if _handle is not None:
        stop()


def add_about_text():
    text = bpy.data.texts.get('关于 Z-Anatomy · v1.0.1')
    if text is None:
        text = bpy.data.texts.new('关于 Z-Anatomy · v1.0.1')
    text.clear()
    text.write('Z-Anatomy 中文版 — Blender 5.0+ 适配与优化\n\n当前版本 / Version: v1.0.1\n仓库 / Repository:\nhttps://github.com/hendasheng/Z-Anatomy-cn-Blender-5\n\n版本记录 / Changelog:\nhttps://github.com/hendasheng/Z-Anatomy-cn-Blender-5/blob/main/CHANGELOG.md\n\n原始项目: Z-Anatomy\n中文翻译: Dean Song (@Dean-Song-1)\n适配与优化: @hendasheng\n')


def enable_on_load():
    add_about_text()
    start()
    return None


@persistent
def after_load(_):
    if not bpy.app.background and not bpy.app.timers.is_registered(enable_on_load):
        bpy.app.timers.register(enable_on_load, first_interval=1.0)


_resume_after_save = False


@persistent
def before_save(_):
    global _resume_after_save
    _resume_after_save = _handle is not None
    if _resume_after_save:
        stop()


@persistent
def after_save(_):
    global _resume_after_save
    if _resume_after_save:
        _resume_after_save = False
        start()


def register():
    bpy.types.WindowManager.za_show_names = bpy.props.BoolProperty(name='显示名称', default=True, update=names_changed)
    bpy.types.WindowManager.za_screen_font_size = bpy.props.IntProperty(name='最大字号', default=20, min=8, max=48)
    for cls in (ZA_OT_screen_labels, ZA_PT_screen_labels):
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_pre.append(before_load)
    bpy.app.handlers.load_post.append(after_load)
    bpy.app.handlers.save_pre.append(before_save)
    bpy.app.handlers.save_post.append(after_save)
    bpy.app.handlers.render_pre.append(before_save)
    bpy.app.handlers.render_post.append(after_save)
    bpy.app.handlers.render_cancel.append(after_save)
    bpy.app.handlers.depsgraph_update_post.append(geometry_changed)
    bpy.app.handlers.undo_pre.append(restore_before_undo)
    bpy.app.handlers.redo_pre.append(restore_before_undo)
    bpy.app.handlers.undo_post.append(after_load)
    bpy.app.handlers.redo_post.append(after_load)


def unregister():
    stop()
    bpy.app.handlers.load_pre.remove(before_load)
    bpy.app.handlers.load_post.remove(after_load)
    if bpy.app.timers.is_registered(enable_on_load):
        bpy.app.timers.unregister(enable_on_load)
    bpy.app.handlers.save_pre.remove(before_save)
    bpy.app.handlers.save_post.remove(after_save)
    bpy.app.handlers.render_pre.remove(before_save)
    bpy.app.handlers.render_post.remove(after_save)
    bpy.app.handlers.render_cancel.remove(after_save)
    bpy.app.handlers.depsgraph_update_post.remove(geometry_changed)
    bpy.app.handlers.undo_pre.remove(restore_before_undo)
    bpy.app.handlers.redo_pre.remove(restore_before_undo)
    bpy.app.handlers.undo_post.remove(after_load)
    bpy.app.handlers.redo_post.remove(after_load)
    for cls in (ZA_PT_screen_labels, ZA_OT_screen_labels):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.za_screen_font_size
    del bpy.types.WindowManager.za_show_names



