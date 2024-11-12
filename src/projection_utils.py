import numpy as np
import cv2
from data_loader import load_all_calibration

def project_velodyne_to_image(velodyne_points, calib_data, scale_factor=0.01, y_offset=200):
    # Step 1: Transform Velodyne points to the camera coordinate system
    Tr_velo_to_cam = calib_data['Tr_velo_to_cam']
    points_cam = velodyne_points @ Tr_velo_to_cam[:, :3].T + Tr_velo_to_cam[:, 3]
    points_cam = points_cam[points_cam[:, 2] > 0]

    # Step 2: Apply rectification
    R_rect_02 = calib_data['R0_rect']
    points_cam = points_cam @ R_rect_02.T

    # Step 3: Convert to homogeneous coordinates
    ones_column = np.ones((points_cam.shape[0], 1))
    points_cam_homogeneous = np.hstack((points_cam, ones_column))

    # Step 4: Project points to 2D using P_rect_02
    P_rect_02 = calib_data['P2']
    points_2d_homogeneous = points_cam_homogeneous @ P_rect_02.T

    # Step 5: Normalize and apply scaling factor
    points_2d = (points_2d_homogeneous[:, :2] / points_2d_homogeneous[:, 2, np.newaxis]) * scale_factor

    # Step 6: Add y_offset to improve visibility
    points_2d[:, 1] += y_offset

    # Clip points to image bounds
    points_2d_clipped = np.clip(points_2d, [0, 0], [1242 - 1, 375 - 1])

    return points_2d_clipped

# Testing code
if __name__ == "__main__":
    # Load calibration data
    velo_to_cam_path = './data/calib/calib_velo_to_cam.txt'
    cam_to_cam_path = './data/calib/calib_cam_to_cam.txt'
    calib_data = load_all_calibration(velo_to_cam_path, cam_to_cam_path)

    # Test with smaller scale and offset
    velodyne_points = np.array([[0.5, 0.5, 10], [1, 1, 12], [0.2, -0.5, 8]])
    points_2d = project_velodyne_to_image(velodyne_points, calib_data, scale_factor=0.01, y_offset=200)
    print("Projected 2D points:", points_2d)