# vim: set ft=python:

from vapoursynth import core
clip = video_in
dst_fps = 48

# Skip interpolation for 60 Hz content
if not (container_fps > 47):
    src_fps_num = int(container_fps * 1e8)
    src_fps_den = int(1e8)
    dst_fps_num = int(dst_fps * 1e4)
    dst_fps_den = int(1e4)
    # Needed because clip FPS is missing
    clip = core.std.AssumeFPS(clip, fpsnum = src_fps_num, fpsden = src_fps_den)
    print("Reflowing from ",src_fps_num/src_fps_den," fps to ",dst_fps_num/dst_fps_den," fps.")
    
    sup  = core.mv.Super(clip, pel=1, hpad=8, vpad=8)
    bvec = core.mv.Analyse(sup, blksize=8, isb=True , chroma=True, search=3, searchparam=1)
    fvec = core.mv.Analyse(sup, blksize=8, isb=False, chroma=True, search=3, searchparam=1)
    clip = core.mv.BlockFPS(clip, sup, bvec, fvec, num=dst_fps_num, den=dst_fps_den, mode=3, thscd2=12)

clip.set_output()
