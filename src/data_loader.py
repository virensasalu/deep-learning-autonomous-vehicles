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
    folder_path = '/Users/virensasalu/Desktop/2011_09_26_drive_0009_extract/velodyne_points/data/'  
    all_points = load_all_velodyne_data(folder_path)
    print(f"Loaded {len(all_points)} files.")
    print("Sample data from the first file:", list(all_points.items())[0])




def load_calib_cam_to_cam(file_path):
    """
    Load camera calibration from calib_cam_to_cam.txt.
    Returns P2 (projection matrix) and R0_rect (rectification matrix).
    """
    calib_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if 'P2:' in line:
                calib_data['P2'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 4)
            if 'R0_rect:' in line:
                calib_data['R0_rect'] = np.array([float(x) for x in line.split()[1:]]).reshape(3, 3)
    return calib_data

def load_calib_velo_to_cam(file_path):
    """
    Load LiDAR to camera transformation from calib_velo_to_cam.txt.
    Returns Tr_velo_to_cam matrix.
    """
    with open(file_path, 'r') as f:
        for line in f:
            if 'Tr_velo_to_cam:' in line:
                Tr_velo_to_cam = np.array([float(x) for x in line.split()[1:]]).reshape(3, 4)
                return {'Tr_velo_to_cam': Tr_velo_to_cam}

# Optional: Load IMU to Velodyne transformation if you need IMU data
def load_calib_imu_to_velo(file_path):
    """
    Load IMU to Velodyne transformation from calib_imu_to_velo.txt.
    Returns Tr_imu_to_velo matrix.
    """
    with open(file_path, 'r') as f:
        for line in f:
            if 'Tr_imu_to_velo:' in line:
                Tr_imu_to_velo = np.array([float(x) for x in line.split()[1:]]).reshape(3, 4)
                return {'Tr_imu_to_velo': Tr_imu_to_velo}
            

cam_to_cam_path = '/Users/virensasalu/Desktop/2011_09_26-10/calib_cam_to_cam.txt'
velo_to_cam_path = '/Users/virensasalu/Desktop/2011_09_26-10/calib_velo_to_cam.txt'
imu_to_velo_path = '/Users/virensasalu/Desktop/2011_09_26-10/calib_imu_to_velo.txt'  # Only if needed

calib_cam = load_calib_cam_to_cam(cam_to_cam_path)
calib_velo = load_calib_velo_to_cam(velo_to_cam_path)           