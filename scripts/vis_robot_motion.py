from general_motion_retargeting import RobotMotionViewer, load_robot_motion
import argparse
import os
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default="unitree_g1")
                        
    parser.add_argument("--robot_motion_path", type=str, required=True)

    parser.add_argument("--record_video", action="store_true")
    parser.add_argument("--video_path", type=str, 
                        default="videos/example.mp4")
    parser.add_argument(
        "--step",
        action="store_true",
        help="逐帧播放模式（空格/回车播放下一帧）",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="倒放（从最后一帧往第一帧播放）",
    )
                        
    args = parser.parse_args()
    
    robot_type = args.robot
    robot_motion_path = args.robot_motion_path
    
    if not os.path.exists(robot_motion_path):
        raise FileNotFoundError(f"Motion file {robot_motion_path} not found")
    
    motion_data, motion_fps, motion_root_pos, motion_root_rot, motion_dof_pos, motion_local_body_pos, motion_link_body_list = load_robot_motion(robot_motion_path)
    
    env = RobotMotionViewer(robot_type=robot_type,
                            motion_fps=motion_fps,
                            camera_follow=False,
                            record_video=args.record_video, video_path=args.video_path)
    
    num_frames = len(motion_root_pos)
    # 倒放时从最后一帧开始，否则从第 0 帧开始
    frame_idx = (num_frames - 1) if args.reverse else 0
    step = -1 if args.reverse else 1

    if args.step:
        direction = "上一帧" if args.reverse else "下一帧"
        print(f"逐帧模式：按空格 + 回车 播放{direction}，输入 q + 回车 退出。")

        while True:
            cmd = input(f"[{frame_idx+1}/{num_frames}] 按空格继续，q 退出: ").strip()

            if cmd.lower() == "q":
                break

            # 允许直接回车或输入空格代表下一帧/上一帧
            if cmd in ("", " "):
                env.step(
                    motion_root_pos[frame_idx],
                    motion_root_rot[frame_idx],
                    motion_dof_pos[frame_idx],
                    rate_limit=True,
                )
                frame_idx += step
                if frame_idx >= num_frames:
                    frame_idx = 0
                elif frame_idx < 0:
                    frame_idx = num_frames - 1
    else:
        # 自动循环播放（正放或倒放）
        while True:
            env.step(
                motion_root_pos[frame_idx],
                motion_root_rot[frame_idx],
                motion_dof_pos[frame_idx],
                rate_limit=True,
            )
            frame_idx += step
            if frame_idx >= num_frames:
                frame_idx = 0
            elif frame_idx < 0:
                frame_idx = num_frames - 1

    env.close()

#old file
# 85 140
# 225 310

#new file
# 30 140
# 225 340

# kcrawl_edit3
# 120

# omni 7dof 
# 120