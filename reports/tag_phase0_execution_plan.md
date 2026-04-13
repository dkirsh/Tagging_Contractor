# Phase 0 Image-Only Execution Plan

## Tags and extraction rules
- `env.ae.hard_reflective_surfaces` | material_reflectance | specular_area>=0.20 OR glossy_surface_area>=0.25 | abstain: low light, strong glare bloom, heavy occlusion, low resolution
- `env.ae.hard_seating` | object_detection+material | seats>=1 AND hard_material_ratio>=0.6 | abstain: seating occluded or material uncertain
- `env.ae.high_texture_complexity` | texture_analysis | entropy>=P75 AND edge_density>=P75 | abstain: motion blur or low-res imagery
- `env.ae.home-like_decor` | style_classification | style_confidence>=0.6 | abstain: mixed-use or staged commercial settings
- `env.ae.indoor-outdoor_continuity` | scene_layout | opening_width_ratio>=0.25 AND exterior_view_present | abstain: single narrow window only
- `env.ae.institutional_decor` | style_classification | style_confidence>=0.6 | abstain: small sample or ambiguous setting
- `env.ae.low_texture_complexity` | texture_analysis | entropy<=P25 AND edge_density<=P25 | abstain: overexposed or heavily compressed images
- `env.ae.metal_prominent` | material_classification | metal_area>=0.20 | abstain: specular ambiguity vs glass
- `env.ae.monochrome/minimal_palette` | color_analysis | palette_entropy<=P25 | abstain: color cast or white balance failure
- `env.ae.natural/earthy_palette` | color_analysis | earth_tone_ratio>=0.35 | abstain: mixed lighting or strong color filters
- `env.ae.nature_imagery` | object_detection+scene | nature_artwork_count>=1 | abstain: actual windows to nature (not imagery)
- `env.ae.open_plan` | layout_estimation | partition_density<=P25 AND visible_area_span>=P75 | abstain: cropped views or narrow FOV
- `env.ae.open_windows` | object_detection | open_window_count>=1 | abstain: reflections or curtains obscure state
- `env.ae.soft_seating` | object_detection+material | seats>=1 AND soft_material_ratio>=0.6 | abstain: seating occluded or material uncertain
- `env.ae.sparse_occupancy` | people_detection | people_count<=1 OR people_density<=0.02 per m^2 | abstain: crowd occlusion or limited FOV
- `env.ae.stone/marble_prominent` | material_classification | stone_area>=0.20 | abstain: patterned porcelain vs stone ambiguity
- `env.ae.strong_verticality` | geometry_lines | vertical_line_ratio>=0.6 | abstain: tilted camera or strong perspective skew
- `env.ae.surveillance_/_cameras_visible` | object_detection | camera_count>=1 | abstain: small/low-res ceiling fixtures ambiguous
- `env.ae.textiles/soft_furnishings` | material_classification | textile_area>=0.15 | abstain: small accents only
- `env.ae.visible_dirt/decay` | defect_detection | defect_score>=0.6 | abstain: low resolution or compression artifacts
- `env.ae.visible_windows` | object_detection | window_count>=1 | abstain: ambiguous openings or mirrors
- `env.ae.warm_color_palette` | color_analysis | warm_ratio>=0.35 | abstain: mixed lighting or white balance drift
- `env.ae.well_maintained` | defect_detection | defect_score<=0.2 | abstain: insufficient visible surfaces
- `env.ae.wood_prominent` | material_classification | wood_area>=0.20 | abstain: strong color cast or low resolution
- `env.ae.work_surfaces_present` | object_detection | work_surfaces>=1 | abstain: partial views with ambiguous surfaces
- `env.ae.worn/degraded` | defect_detection | wear_score>=0.6 | abstain: low lighting or extreme filters
