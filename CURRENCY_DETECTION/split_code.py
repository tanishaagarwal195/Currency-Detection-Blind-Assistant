import os
import shutil
import random

def create_directory(path):
    """
    Creates a directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)

def split_data(class_folder, images_src, labels_src, images_dest, labels_dest, split_ratio=(0.7, 0.2, 0.1)):
    """
    Splits the data into train, val, and test sets and copies them to the destination directories.
    
    Parameters:
    - class_folder: Name of the class (e.g., '10', '20', etc.)
    - images_src: Source directory for images
    - labels_src: Source directory for labels
    - images_dest: Destination directory for images
    - labels_dest: Destination directory for labels
    - split_ratio: Tuple representing the split ratio for train, val, and test
    """
    # List all image files in the class folder
    image_files = [f for f in os.listdir(images_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print(f"No image files found in {images_src}. Skipping class '{class_folder}'.")
        return
    
    # Shuffle the image files for random splitting
    random.shuffle(image_files)
    
    # Calculate split indices
    total = len(image_files)
    train_end = int(total * split_ratio[0])
    val_end = train_end + int(total * split_ratio[1])
    
    # Split the data
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]
    
    # Function to copy files
    def copy_files(file_list, subset):
        for img_file in file_list:
            # Define source and destination for images
            src_img_path = os.path.join(images_src, img_file)
            dest_img_path = os.path.join(images_dest, subset, class_folder, img_file)
            shutil.copy2(src_img_path, dest_img_path)
            
            # Define corresponding label file
            label_file = os.path.splitext(img_file)[0] + '.txt'
            src_label_path = os.path.join(labels_src, label_file)
            dest_label_path = os.path.join(labels_dest, subset, class_folder, label_file)
            
            # Check if the label file exists
            if os.path.exists(src_label_path):
                shutil.copy2(src_label_path, dest_label_path)
            else:
                print(f"Warning: Label file {src_label_path} does not exist for image {img_file}.")
    
    # Copy train, val, and test files
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    copy_files(test_files, 'test')

def organize_dataset(source_root, dest_root, class_names, split_ratio=(0.7, 0.2, 0.1)):
    """
    Organizes the dataset into the desired directory structure.
    
    Parameters:
    - source_root: Root directory of the source dataset containing class folders
    - dest_root: Root directory where the organized dataset will be stored
    - class_names: List of class names
    - split_ratio: Tuple representing the split ratio for train, val, and test
    """
    # Define destination images and labels directories
    images_dest_root = os.path.join(dest_root, 'images')
    labels_dest_root = os.path.join(dest_root, 'labels')
    
    # Create destination directories
    for subset in ['train', 'val', 'test']:
        for cls in class_names:
            create_directory(os.path.join(images_dest_root, subset, cls))
            create_directory(os.path.join(labels_dest_root, subset, cls))
    
    # Process each class
    for cls in class_names:
        print(f"Processing class: {cls}")
        
        # Define source directories for images and labels
        # Assuming that images and labels are stored in separate subdirectories within each class folder
        # e.g., D:\IOT_PROJECT\source_dir\10\images and D:\IOT_PROJECT\source_dir\10\labels
        class_src_dir = os.path.join(source_root, cls)
        images_src = os.path.join(class_src_dir, 'images')
        labels_src = os.path.join(class_src_dir, 'labels')
        
        # Check if the source directories exist
        if not os.path.exists(images_src):
            print(f"Images source directory {images_src} does not exist. Skipping class '{cls}'.")
            continue
        if not os.path.exists(labels_src):
            print(f"Labels source directory {labels_src} does not exist. Skipping class '{cls}'.")
            continue
        
        split_data(
            class_folder=cls,
            images_src=images_src,
            labels_src=labels_src,
            images_dest=images_dest_root,
            labels_dest=labels_dest_root,
            split_ratio=split_ratio
        )
    print("Dataset organization complete!")

if __name__ == "__main__":
    # Define class names
    class_names = ['10', '20', '50', '100', '200', '500', '2000']
    
    # Define source and destination directories
    # Use raw strings (prefix with 'r') to handle backslashes in Windows paths
    SOURCE_DIR = r'D:\IOT_PROJECT\source_dir'       # Replace with your actual source directory
    DEST_DIR = r'D:\IOT_PROJECT\currency_dataset'   # Replace with your desired destination directory
    
    # Verify that the source directory exists
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} does not exist. Please check the path.")
    else:
        # Organize the dataset
        organize_dataset(
            source_root=SOURCE_DIR,
            dest_root=DEST_DIR,
            class_names=class_names,
            split_ratio=(0.7, 0.2, 0.1)  # 70% train, 20% val, 10% test
        )
