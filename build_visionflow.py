#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VisionFlow PyInstaller build script — Cross-platform (Linux / Windows / macOS)
Usage:
    Linux/macOS:   python3 build_visionflow.py
    Windows:       python build_visionflow.py
"""
import io
import sys
# Force UTF-8 on Windows to avoid cp1252 codec errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import os
import platform

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SRC_DIR)

# PyInstaller --add-data 的分隔符：Windows 用 ; ，其他用 :
SEP = ";" if platform.system() == "Windows" else ":"

# ------------------------------------------------------------------
# 1. 收集所有需要显式包含的 hidden imports（importlib 动态导入）
# ------------------------------------------------------------------
HIDDEN_IMPORTS = [
    # core 模块
    'core',
    'core.commands', 'core.conditions', 'core.constants', 'core.data_packet',
    'core.events', 'core.interfaces', 'core.ioc', 'core.node_base',
    'core.node_condition', 'core.node_group', 'core.node_roi',
    'core.node_selectable', 'core.node_vision', 'core.project',
    'core.registry', 'core.result_presenter', 'core.workflow',
    # services
    'services', 'services.app_context', 'services.node_service',
    'services.workflow_runner',
    # gui
    'gui', 'gui.caption_bar', 'gui.color_picker', 'gui.condition_editor',
    'gui.crop_dialog', 'gui.diagram_tab_header', 'gui.flow_resource_panel',
    'gui.font_icons', 'gui.guide_overlay', 'gui.help_panel',
    'gui.image_viewer', 'gui.img_template_manager', 'gui.main_window',
    'gui.node_property_dialog', 'gui.property_panel', 'gui.result_panel',
    'gui.roi_editor', 'gui.settings_dialog', 'gui.template_dialog',
    'gui.theme', 'gui.theme_data', 'gui.toolbox_panel', 'gui.widget_utils',
    'gui.node_editor', 'gui.node_editor.edge_item', 'gui.node_editor.editor_widget',
    'gui.node_editor.link_drawer', 'gui.node_editor.node_item',
    'gui.node_editor.scene', 'gui.node_editor.socket_item',
    'gui.widgets', 'gui.widgets.grid_splitter_box', 'gui.widgets.inline_status_strip',
    # 14 个节点包
    'nodes',
    'nodes.sources', 'nodes.sources.camera_source', 'nodes.sources.image_file_source',
    'nodes.sources.video_file_source', 'nodes.sources.zoo_sources',
    'nodes.preprocessings', 'nodes.preprocessings.arithmetic',
    'nodes.preprocessings.bitwise_not', 'nodes.preprocessings.cvt_color',
    'nodes.preprocessings.flip', 'nodes.preprocessings.normalize',
    'nodes.preprocessings.repeat', 'nodes.preprocessings.resize',
    'nodes.preprocessings.rotate', 'nodes.preprocessings.split_bgr',
    'nodes.preprocessings.threshold',
    'nodes.blurs', 'nodes.blurs.blur', 'nodes.blurs.detail_enhance',
    'nodes.blurs.edge_blur', 'nodes.blurs.gaussian_blur', 'nodes.blurs.pencil_sketch',
    'nodes.takeoffs', 'nodes.takeoffs.bitwise_and', 'nodes.takeoffs.crop',
    'nodes.takeoffs.draw_contours', 'nodes.takeoffs.hsv_inrange',
    'nodes.takeoffs.roi_map_back', 'nodes.takeoffs.seamless_clone_bg',
    'nodes.morphology', 'nodes.morphology.black_hat', 'nodes.morphology.close',
    'nodes.morphology.dilate', 'nodes.morphology.erode',
    'nodes.morphology.gradient', 'nodes.morphology.morph_base',
    'nodes.morphology.open', 'nodes.morphology.top_hat',
    'nodes.conditions', 'nodes.conditions.condition_branch',
    'nodes.conditions.data_collector', 'nodes.conditions.pixel_threshold',
    'nodes.template_matchings', 'nodes.template_matchings.chamfer_matching',
    'nodes.template_matchings.edge_matching', 'nodes.template_matchings.hsv_blob',
    'nodes.template_matchings.ncc_matching', 'nodes.template_matchings.orb_matching',
    'nodes.template_matchings.sad_matching', 'nodes.template_matchings.shape_context_matching',
    'nodes.template_matchings.sift_matching', 'nodes.template_matchings.surf_matching',
    'nodes.template_matchings.template_base', 'nodes.template_matchings.template_matching',
    'nodes.template_matchings.xfeat_match',
    'nodes.detectors', 'nodes.detectors.blob_detector', 'nodes.detectors.canny',
    'nodes.detectors.detector_base', 'nodes.detectors.find_contours',
    'nodes.detectors.hough_lines', 'nodes.detectors.hough_lines_p',
    'nodes.detectors.qr_code', 'nodes.detectors.render_blobs',
    'nodes.features', 'nodes.features.akaze', 'nodes.features.brisk',
    'nodes.features.fast', 'nodes.features.feature_base', 'nodes.features.freak',
    'nodes.features.homography', 'nodes.features.kaze', 'nodes.features.mser',
    'nodes.features.star',
    'nodes.others', 'nodes.others.dnn_superres', 'nodes.others.haar_cascade',
    'nodes.others.histogram', 'nodes.others.hog', 'nodes.others.lbp_cascade',
    'nodes.others.seamless_clone', 'nodes.others.stitching',
    'nodes.others.subdiv2d', 'nodes.others.svm', 'nodes.others.warp_affine',
    'nodes.others.warp_perspective',
    'nodes.video', 'nodes.video.video_nodes',
    'nodes.outputs', 'nodes.outputs.output_base', 'nodes.outputs.show_outputs',
    'nodes.onnx', 'nodes.onnx.age_infer', 'nodes.onnx.defect_box',
    'nodes.onnx.detection_utils', 'nodes.onnx.dnn_interface',
    'nodes.onnx.gender_cls', 'nodes.onnx.human_semseg',
    'nodes.onnx.onnx_base', 'nodes.onnx.onnx_bbox', 'nodes.onnx.onnx_cls',
    'nodes.onnx.onnx_infer', 'nodes.onnx.onnx_seg', 'nodes.onnx.yolov5',
    'nodes.onnx.yolov5_face', 'nodes.onnx.yolov8_detect',
    'nodes.network', 'nodes.network.modbus_base', 'nodes.network.modbus_coil_read',
    'nodes.network.modbus_coil_write', 'nodes.network.modbus_discrete_input',
    'nodes.network.modbus_input_register', 'nodes.network.modbus_multi_write',
    'nodes.network.modbus_read', 'nodes.network.modbus_write',
    'nodes.dll', 'nodes.dll.vision_dll',
    'nodes.third_party', 'nodes.third_party.alike_wrapper',
    # PyQt5 内部模块
    'PyQt5.sip',
    'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
    'PyQt5.QtNetwork', 'PyQt5.QtOpenGL',
    # OpenCV
    'cv2',
    # ONNX
    'onnxruntime',
    'onnxruntime.capi.onnxruntime_pybind11_state',
    # 其他
    'PIL', 'PIL.Image', 'PIL.ImageOps', 'PIL.ImageFilter',
    'pymodbus', 'pymodbus.client', 'pymodbus.server',
    # numpy
    'numpy.core._dtype_ctypes',
]

# ------------------------------------------------------------------
# 2. 收集数据文件
# ------------------------------------------------------------------
data_files = []

# assets/ 目录
assets_root = os.path.join(SRC_DIR, 'assets')
if os.path.exists(assets_root):
    for root, dirs, files in os.walk(assets_root):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.relpath(root, SRC_DIR)
            data_files.append((src, dst))

# nodes/dll/ 目录下的 DLL / SO
dll_dir = os.path.join(SRC_DIR, 'nodes', 'dll')
if os.path.exists(dll_dir):
    for f in os.listdir(dll_dir):
        if f.lower().endswith('.dll') or f.lower().endswith('.so'):
            data_files.append((os.path.join(dll_dir, f), 'nodes/dll'))

# nodes/modules/ 下的训练模块文件
modules_dir = os.path.join(SRC_DIR, 'nodes', 'modules')
if os.path.exists(modules_dir):
    for root, dirs, files in os.walk(modules_dir):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.relpath(root, SRC_DIR)
            data_files.append((src, dst))

# 根目录配置文件
for cfg in ['app_config.json', 'theme_config.json', 'templates.json']:
    cfg_path = os.path.join(SRC_DIR, cfg)
    if os.path.exists(cfg_path):
        data_files.append((cfg_path, '.'))

# 项目模板文件
templates_dir = os.path.join(SRC_DIR, 'templates')
if os.path.exists(templates_dir):
    for f in os.listdir(templates_dir):
        if f.endswith('.json'):
            data_files.append((os.path.join(templates_dir, f), 'templates'))

# ------------------------------------------------------------------
# 3. 构建 PyInstaller 参数
# ------------------------------------------------------------------
import PyInstaller.__main__

args = [
    'main.py',
    '--name', 'VisionFlow',
    '--onefile',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--noconsole',
    '--workpath', os.path.join(SRC_DIR, 'build'),
    '--distpath', os.path.join(SRC_DIR, 'dist'),
    '--paths', SRC_DIR,
]

# 图标（Windows 和 macOS 支持 .ico，Linux 忽略）
ico_path = os.path.join(SRC_DIR, 'assets', 'icons', 'logo.ico')
if os.path.exists(ico_path):
    args.extend(['--icon', ico_path])

# hidden imports
for mod in HIDDEN_IMPORTS:
    args.extend(['--hidden-import', mod])

# 数据文件 — 使用平台正确的分隔符
for src, dst in data_files:
    args.extend(['--add-data', f'{src}{SEP}{dst}'])

# PyQt5 全量收集
args.extend([
    '--collect-all', 'PyQt5',
    '--collect-all', 'PyQt5-Qt5',
])

# ------------------------------------------------------------------
# 4. 运行打包
# ------------------------------------------------------------------
print("=" * 60)
print("VisionFlow PyInstaller Build")
print(f"Platform: {platform.system()} {platform.machine()}")
print(f"Python: {platform.python_version()}")
print("=" * 60)
print(f"Working dir: {SRC_DIR}")
print(f"Data files: {len(data_files)}")
print(f"Hidden imports: {len(HIDDEN_IMPORTS)}")
print(f"Separator: '{SEP}'")
print("-" * 60)

PyInstaller.__main__.run(args)

exe_name = "VisionFlow.exe" if platform.system() == "Windows" else "VisionFlow"
output_path = os.path.join(SRC_DIR, 'dist', exe_name)

print("=" * 60)
print("Build complete!")
print(f"Output: {output_path}")
if os.path.exists(output_path):
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Size: {size_mb:.1f} MB")
print("=" * 60)
