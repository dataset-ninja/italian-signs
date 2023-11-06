import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil
import json
from tqdm import tqdm
from glob import glob
import imagesize
import csv


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    def create_ann(image_path):
        labels = []
        bbox = img_ann_dict.get(sly.fs.get_file_name_with_ext(image_path))
    
        x_min, y_min, x_max, y_max, tag_value = bbox
    
        rectangle = sly.Rectangle(top=int(y_min), left=int(x_min), bottom=int(y_max), right=int(x_max))
        tag = sly.Tag(tm_sl, int(tag_value))
    
        label = sly.Label(rectangle, obj_class, tags=[tag])
        labels.append(label)
    
        img_width, img_height = imagesize.get(image_path)
        return sly.Annotation(img_size=(img_height, img_width), labels=labels)
    
    
    obj_class = sly.ObjClass("sign", sly.Rectangle, color=[255, 0, 0])
    
    tm_sl = sly.TagMeta("speed limit", sly.TagValueType.ANY_NUMBER)
    
    with open('/mnt/c/users/german/documents/ItalianSigns/labels/ItalianSigns.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        img_ann_dict = {row[0]: row[1:6] for row in csv_reader if len(row)!=0}

    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[tm_sl],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset_path = "/mnt/c/users/german/documents/ItalianSigns"
    dataset = api.dataset.create(project.id, "ds0", change_name_if_conflict=True)

    images_pathes = glob(dataset_path + "/images/*.jpg")

    batch_size = 31
    progress = sly.Progress("Create dataset {}".format("ds0"), len(images_pathes))
    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [sly.fs.get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)
    return project
