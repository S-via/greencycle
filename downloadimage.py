from icrawler.builtin import BingImageCrawler
import os
import random
import shutil

def download(keyword, max_images=100, out_dir="dataset/datasrc"):
    crawler = BingImageCrawler(storage={"root_dir": f"{out_dir}/{keyword}"})
    crawler.crawl(keyword=keyword, max_num=max_images)

def split_dataset(src_folder, train_folder="dataset/train", val_folder="dataset/validation", val_ratio=0.2):
    # create folder if not exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    
    # shuffle images
    files = [f for f in os.listdir(src_folder) if f.endswith(('.jpg', '.png'))]
    random.shuffle(files)
    
    # split between validation files and trained files
    val_size = int(len(files) * val_ratio)
    val_files = files[:val_size]
    train_files = files[val_size:]
    
    # move files to their folder
    for f in train_files:
        shutil.move(os.path.join(src_folder, f), os.path.join(train_folder, f))
    for f in val_files:
        shutil.move(os.path.join(src_folder, f), os.path.join(val_folder, f))

"""
download("battery")
split_dataset("dataset/datasrc/battery", "dataset/train/battery","dataset/validation/battery")
download("cardboard")
split_dataset("dataset/datasrc/cardboard", "dataset/train/cardboard","dataset/validation/cardboard")
download("cigarette")
split_dataset("dataset/datasrc/cigarette", "dataset/train/cigarette","dataset/validation/cigarette")
download("diaper")
split_dataset("dataset/datasrc/diaper", "dataset/train/diaper","dataset/validation/diaper")
download("electronics")
split_dataset("dataset/datasrc/electronics", "dataset/train/electronics","dataset/validation/electronics")
download("food_waste")
split_dataset("dataset/datasrc/food_waste", "dataset/train/food_waste","dataset/validation/food_waste")
download("glass")
split_dataset("dataset/datasrc/glass", "dataset/train/glass","dataset/validation/glass")
download("light_bulb")
split_dataset("dataset/datasrc/light_bulb", "dataset/train/light_bulb","dataset/validation/light_bulb")
download("medicine")
split_dataset("dataset/datasrc/medicine", "dataset/train/medicine","dataset/validation/medicine")
download("metal")
split_dataset("dataset/datasrc/metal", "dataset/train/metal","dataset/validation/metal")
download("paper")
split_dataset("dataset/datasrc/paper", "dataset/train/paper","dataset/validation/paper")
download("plastic")
split_dataset("dataset/datasrc/plastic", "dataset/train/plastic","dataset/validation/plastic")
download("styrofoam")
split_dataset("dataset/datasrc/styrofoam", "dataset/train/styrofoam","dataset/validation/styrofoam")
"""