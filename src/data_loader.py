import os
import numpy as np


def load_velodyne_points_bin(file_path):
    """
    Load 3D point cloud data from a .bin file.

    Parameters:
        file_path (str): Path to the Velodyne .bin file.

    Returns:
    
        np.ndarray: Array of points with each row as [x, y, z, intensity].
    """
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    return point_cloud

def load_all_velodyne_data(folder_path):
    """
    Load all Velodyne point cloud data from a specified folder.

    Parameters:
        folder_path (str): Path to the folder containing Velodyne .bin files.

    Returns:
        dict: A dictionary where each key is a filename and each value is the loaded point cloud data.
    """
    velodyne_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".bin"):
            file_path = os.path.join(folder_path, filename)
            velodyne_data[filename] = load_velodyne_points_bin(file_path)
    return velodyne_data

# if __name__ == "__main__":
#     # Example usage for testing
#     folder_path = './data/velodyne_points/data'  
#     all_points = load_all_velodyne_data(folder_path)
#     print(f"Loaded {len(all_points)} files.")
#     print("Sample data from the first file:", list(all_points.items())[0])



def load_calib_cam_to_cam(file_path):
    calib_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if 'P_rect_02:' in line:
                calib_data['P2'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 4)
                print("Loaded P_rect_02:", calib_data['P2'])  # Debugging print
            if 'R_rect_02:' in line:
                calib_data['R0_rect'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
                print("Loaded R_rect_02:", calib_data['R0_rect'])  # Debugging print
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
    calib_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('R:'):
                R = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
            elif line.startswith('T:'):
                T = np.array([float(x) for x in line.split()[1:]]).reshape(3, 1)

    if R is not None and T is not None:
        Tr_velo_to_cam = np.hstack((R, T))
        print("Loaded Tr_velo_to_cam:", Tr_velo_to_cam)  # Debugging print
        calib_data['Tr_velo_to_cam'] = Tr_velo_to_cam
    return calib_data
    

# Wrapper function to load all calibration data
def load_all_calibration(velo_to_cam_path, cam_to_cam_path):
    calib_velo = load_calib_velo_to_cam(velo_to_cam_path)
    calib_cam = load_calib_cam_to_cam(cam_to_cam_path)
    
    # Combine all calibration data into a single dictionary
    calib_data = {**calib_velo, **calib_cam}
    return calib_data

# Testing the function in __main__ (Optional for verification)
if __name__ == "__main__":
    velo_to_cam_path = './data/calib/calib_velo_to_cam.txt'
    cam_to_cam_path = './data/calib/calib_cam_to_cam.txt'
    calib_data = load_all_calibration(velo_to_cam_path, cam_to_cam_path)
    print("Calibration data:", calib_data)