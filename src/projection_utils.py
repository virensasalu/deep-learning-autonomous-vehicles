import numpy as np
import cv2


# Projection functions
def project_velodyne_to_image(velodyne_points, calib_velo, calib_cam):
    Tr_velo_to_cam = calib_velo['Tr_velo_to_cam']
    points_cam = velodyne_points @ Tr_velo_to_cam[:, :3].T + Tr_velo_to_cam[:, 3]
    points_cam = points_cam[points_cam[:, 2] > 0]

    ones_column = np.ones((points_cam.shape[0], 1))
    points_cam_homogeneous = np.hstack((points_cam, ones_column))

    P2 = calib_cam['P2']
    points_2d_homogeneous = points_cam_homogeneous @ P2.T
    points_2d = points_2d_homogeneous[:, :2] / points_2d_homogeneous[:, 2, np.newaxis]
    return points_2d

def overlay_points_on_image(image, points_2d):
    for point in points_2d:
        x, y = int(point[0]), int(point[1])
        if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)
    return image

if __name__ == "__main__":
    velodyne_points = np.array([[10, 10, 10], [15, 20, 15], [5, -5, 10]])
    calib_velo = {
        'Tr_velo_to_cam': np.array([
            [7.533745e-03, -9.999714e-01, -6.166020e-04, -4.069766e-03],
            [1.480249e-02, 7.280733e-04, -9.998902e-01, -7.631618e-02],
            [9.998621e-01, 7.523790e-03, 1.480755e-02, -2.717806e-01]
        ])
    }
    calib_cam = {
        'P2': np.array([
            [7.215377e+02, 0.000000e+00, 6.095593e+02, 4.485728e+01],
            [0.000000e+00, 7.215377e+02, 1.728540e+02, 2.163791e-01],
            [0.000000e+00, 0.000000e+00, 1.000000e+00, 2.745884e-03]
        ])
    }
    
    image = np.ones((375, 1242, 3), dtype=np.uint8) * 255
    
    # Project points and print to debug
    points_2d = project_velodyne_to_image(velodyne_points, calib_velo, calib_cam)
    print("Projected 2D points:", points_2d)  # Debugging line to check projected points

    image_with_points = overlay_points_on_image(image, points_2d)

    import matplotlib.pyplot as plt
    plt.imshow(image_with_points)
    plt.axis('off')
    plt.show()
    