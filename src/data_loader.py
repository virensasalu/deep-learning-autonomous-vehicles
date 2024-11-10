import os
import numpy as np

def load_velodyne_points_txt(file_path):
    """
    Load 3D point cloud data from a .txt file.

    Parameters:
        file_path (str): Path to the Velodyne .txt file.

    Returns:
        np.ndarray: Array of points with each row as [x, y, z, intensity].
    """
    point_cloud = np.loadtxt(file_path, dtype=np.float32)
    return point_cloud

def load_all_velodyne_data(folder_path):
    """
    Load all Velodyne point cloud data from a specified folder.

    Parameters:
        folder_path (str): Path to the folder containing Velodyne .txt files.

    Returns:
        dict: A dictionary where each key is a filename and each value is the loaded point cloud data.
    """
    velodyne_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            velodyne_data[filename] = load_velodyne_points_txt(file_path)
    return velodyne_data

if __name__ == "__main__":
    # Example usage for testing
    folder_path = './data/velodyne_points/data'  
    all_points = load_all_velodyne_data(folder_path)
    print(f"Loaded {len(all_points)} files.")
    print("Sample data from the first file:", list(all_points.items())[0])





def load_calib_cam_to_cam(file_path):
    """
    Load camera calibration from calib_cam_to_cam.txt.
    Returns P_rect_02 (projection matrix) and R_rect_02 (rectification matrix).
    """
    calib_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if 'P_rect_02:' in line:
                calib_data['P2'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 4)
            if 'R_rect_02:' in line:
                calib_data['R0_rect'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
    return calib_data


def load_calib_imu_to_velo(file_path):
    """
    Load IMU to Velodyne transformation from calib_imu_to_velo.txt.
    Returns a dictionary with 'R' (rotation matrix) and 'T' (translation vector).
    """
    calib_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('R:'):
                calib_data['R'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
            elif line.startswith('T:'):
                calib_data['T'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 1)
    return calib_data


def load_calib_velo_to_cam(file_path):
    """
    Load Velodyne to Camera transformation from calib_velo_to_cam.txt.
    Returns Tr_velo_to_cam, a 3x4 transformation matrix.
    """
    R = None
    T = None
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('R:'):
                R = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
            elif line.startswith('T:'):
                T = np.array([float(x) for x in line.split()[1:]]).reshape(3, 1)
    
    if R is not None and T is not None:
        # Combine R and T into a 3x4 transformation matrix
        Tr_velo_to_cam = np.hstack((R, T))
        return {'Tr_velo_to_cam': Tr_velo_to_cam}
    else:
        raise ValueError("R or T matrix not found in the calibration file.")
    
    
if __name__ == "__main__":
    # Paths to calibration files
    cam_to_cam_path = './data/calib/calib_cam_to_cam.txt'
    velo_to_cam_path = './data/calib/calib_velo_to_cam.txt'
    imu_to_velo_path = './data/calib/calib_imu_to_velo.txt'  # Optional for IMU data

    # Load calibration data
    calib_cam = load_calib_cam_to_cam(cam_to_cam_path)
    calib_velo = load_calib_velo_to_cam(velo_to_cam_path)

    # Load IMU to Velodyne calibration only if available
    calib_imu = None
    try:
        calib_imu = load_calib_imu_to_velo(imu_to_velo_path)
    except FileNotFoundError:
        print("IMU to Velodyne calibration file not found; skipping.")

    # Print loaded calibration data for verification
    print("Camera Calibration (P2 and R0_rect):", calib_cam)
    print("Velodyne to Camera Transformation (Tr_velo_to_cam):", calib_velo)
    if calib_imu:
        print("IMU to Velodyne Transformation (Tr_imu_to_velo):", calib_imu)