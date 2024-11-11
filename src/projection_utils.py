import numpy as np
import cv2
from data_loader import load_calib_velo_to_cam, load_calib_cam_to_cam

def project_velodyne_to_image(velodyne_points, calib_velo, calib_cam):
    """
    Project 3D Velodyne points onto the 2D image plane.
    """
    # Step 1: Transform Velodyne points to the camera coordinate system
    Tr_velo_to_cam = calib_velo['Tr_velo_to_cam']
    points_cam = velodyne_points @ Tr_velo_to_cam[:, :3].T + Tr_velo_to_cam[:, 3]

    # Debug: Print transformed points in the camera coordinate system
    print("Transformed 3D points in camera coordinates:", points_cam)

    # Step 2: Filter points to keep only those in front of the camera
    points_cam = points_cam[points_cam[:, 2] > 0]

    # Step 3: Convert to homogeneous coordinates
    ones_column = np.ones((points_cam.shape[0], 1))
    points_cam_homogeneous = np.hstack((points_cam, ones_column))

    # Step 4: Project points to 2D using P2 matrix
    P2 = calib_cam['P2']
    points_2d_homogeneous = points_cam_homogeneous @ P2.T
    points_2d = points_2d_homogeneous[:, :2] / points_2d_homogeneous[:, 2, np.newaxis]  # Normalize by depth

    # Debug: Print projected 2D points
    print("Projected 2D points after normalization:", points_2d)

    return points_2d

def overlay_points_on_image(image, points_2d):
    """
    Overlay projected 2D points on the image.

    Parameters:
        image (np.ndarray): Image on which to overlay points.
        points_2d (np.ndarray): 2D points projected onto the image.

    Returns:
        np.ndarray: Image with points overlayed.
    """
    for point in points_2d:
        x, y = int(point[0]), int(point[1])
        if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:  # Check if point is within image bounds
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)  # Draw point in red
    return image

if __name__ == "__main__":
    # Example paths for calibration files
    cam_to_cam_path = './data/calib/calib_cam_to_cam.txt'
    velo_to_cam_path = './data/calib/calib_velo_to_cam.txt'

    # Load calibration data
    calib_cam = load_calib_cam_to_cam(cam_to_cam_path)
    calib_velo = load_calib_velo_to_cam(velo_to_cam_path)

    # Sample 3D points (Replace with actual Velodyne points)
    velodyne_points = np.array([[10, 10, 10], [15, 20, 15], [5, -5, 10]])

    # Project points onto the image
    points_2d = project_velodyne_to_image(velodyne_points, calib_velo, calib_cam)
    print("Projected 2D points:", points_2d)

    # Load a test image (replace this with an actual image from image_02)
    image = np.ones((375, 1242, 3), dtype=np.uint8) * 255

    # Overlay points on the image
    image_with_points = overlay_points_on_image(image, points_2d)

    # Display the image
    import matplotlib.pyplot as plt
    plt.imshow(image_with_points)
    plt.axis('off')
    plt.show()