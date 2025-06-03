import torch
import cv2
import mediapipe as mp
import numpy as np

class FullBodyDetection:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("BOOLEAN","FLOAT","FLOAT")
    RETURN_NAMES = ("is_full", "eye_to_edge", "foot_to_edge")
    FUNCTION = "full_body_detection"
    CATEGORY = "NVVS/image processing"


    def full_body_detection(self, image):
        """
        执行人体完整性判断
        
        参数:
            image (torch.Tensor): 输入图像张量 [H, W, 3]，范围 [0, 1]
            threshold_visibility (float): 关键点可见性阈值
            
        返回:
            tuple: (是否为完整人体, 眼睛与边缘距离, 脚部与边缘距离)
        """
        # 初始化 MediaPipe 姿态检测模块
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        
        # 检查输入张量形状（允许 [1, H, W, 3] 或 [H, W, 3]）
        if image.dim() == 4 and image.shape[0] == 1 and image.shape[-1] == 3:
            pass
        elif image.dim() == 3 and image.shape[-1] == 3:
            image = image.unsqueeze(0)
        else:
            raise ValueError(f"输入张量必须是 [1, H, W, 3] 或 [H, W, 3] 格式，当前形状: {image.shape}")

        # 将张量转换为 [1, 3, H, W] 格式（即 NCHW）
        image = image.permute(0, 3, 1, 2)  # [1, H, W, 3] → [1, 3, H, W]

        # 将 PyTorch 张量转换为 NumPy 数组（HWC 格式，像素值 [0, 255]）
        image_np = image.squeeze(0).detach().cpu().numpy()  # 移除批次维度 [1, 3, H, W] → [3, H, W]
        image_np = np.transpose(image_np, (1, 2, 0))  # [3, H, W] → [H, W, 3]
        image_np = (np.clip(image_np, 0.0, 1.0) * 255).astype(np.uint8)  # [0-1] → [0-255]

        # 假设输入张量是 RGB 格式，直接使用 cv2.cvtColor 转换为 BGR（如需）
        bgr_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # 执行姿态检测
        pose_result = pose.process(cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB))

        # 检查是否检测到关键点
        if pose_result.pose_landmarks:
            landmarks = pose_result.pose_landmarks.landmark
            print(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX])
            print(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].visibility)

            left_eye_y = landmarks[mp_pose.PoseLandmark.LEFT_EYE].y
            right_eye_y = landmarks[mp_pose.PoseLandmark.RIGHT_EYE].y
            left_foot_y = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y
            right_foot_y = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y

            eye_to_edge = 0
            foot_to_edge = 0

            if (left_eye_y > 0 and right_eye_y > 0 and left_foot_y < 1 and right_foot_y < 1):
                is_full = True

            if (left_eye_y <= 0 or right_eye_y <= 0):
                is_full = False
                eye_to_edge = max(0-left_eye_y, 0-right_eye_y)

            if (left_foot_y >= 1 or right_foot_y >= 1):
                is_full = False
                foot_to_edge = max(left_foot_y-1, right_foot_y-1)
        else:
            is_full = False

        return (is_full, round(eye_to_edge, 4), round(foot_to_edge, 4))
