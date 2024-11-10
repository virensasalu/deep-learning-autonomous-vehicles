# deep-learning-autonomous-vehicles

his project focuses on object detection and classification in real-time for autonomous vehicles. 

## Tech Stack
- YOLO, SSD, Faster R-CNN
- OpenCV, KITTI dataset, TensorFlow

## Project Structure
├── README.md                       # Overview of the project, setup instructions
├── data/                            # Directory to store datasets
│   └── kitti/                       # KITTI dataset subdirectory
├── notebooks/                       # Jupyter notebooks for exploratory analysis, EDA
│   └── data_preprocessing.ipynb     # Example notebook for data exploration and preprocessing
├── src/                             # Source code for the project
│   ├── data_loader.py               # Script to load and preprocess data
│   ├── yolo_model.py                # YOLO model code
│   ├── ssd_model.py                 # SSD model code
│   ├── faster_rcnn_model.py         # Faster R-CNN model code
│   ├── object_detection.py          # Script to handle object detection pipeline
│   └── utils.py                     # Utility functions (e.g., visualization)
├── experiments/                     # Experimental results, model versions
│   └── model_v1/                    # Folder for model version 1 (weights, configurations)
│       ├── config.json
│       └── best_weights.h5
├── tests/                           # Unit tests for your code
│   ├── test_data_loader.py          # Tests for data loader
│   ├── test_yolo_model.py           # Tests for YOLO model
│   └── test_object_detection.py     # Tests for object detection pipeline
├── requirements.txt                 # Python package dependencies
└── setup.py                         # For packaging the project (optional, if using as a module)


