# Original repo: https://github.com/Prodesire/face-mask

import numpy as np
from PIL import Image, ImageFile
import glob
import os
import face_recognition

from utils import paths

class FaceMasker:
    KEY_FACIAL_FEATURES = ('nose_bridge', 'chin')

    def __init__(self, src_path, mask_colors, dst_path, show=False, model='hog'):
        self.src_path = src_path
        self.dst_path = dst_path
        self.show = show
        self.model = model
        self._face_img: ImageFile = None
        self.mask_colors = mask_colors



    def mask(self):

        face_image_np = face_recognition.load_image_file(self.src_path)
        face_locations = face_recognition.face_locations(face_image_np, model=self.model)
        face_landmarks = face_recognition.face_landmarks(face_image_np, face_locations)
        self._face_img = Image.fromarray(face_image_np)


        found_face = False
        for face_landmark in face_landmarks:
            # check whether facial features meet requirement
            skip = False
            for facial_feature in self.KEY_FACIAL_FEATURES:
                if facial_feature not in face_landmark:
                    skip = True
                    break
            if skip:
                continue

            # mask face
            found_face = True
            self._mask_face(face_landmark)

        if found_face:
            if self.show:
                self._face_img.show()

        else:
            print('Found no face.')

    def _mask_face(self, face_landmark: dict):
        nose_bridge = face_landmark['nose_bridge']
        nose_point = nose_bridge[len(nose_bridge) * 1 // 4]
        nose_v = np.array(nose_point)

        chin = face_landmark['chin']
        chin_len = len(chin)
        chin_bottom_point = chin[chin_len // 2]
        chin_bottom_v = np.array(chin_bottom_point)
        chin_left_point = chin[chin_len // 8]
        chin_right_point = chin[chin_len * 7 // 8]

        for name in self.mask_colors:
            for dir_ in glob.iglob(str(paths.MASKS_DIR / "*.png")):
                if name == dir_.split("/")[-1].strip(".png"):
                    mask=Image.open(dir_)
                    # split mask and resize
                    width = mask.width
                    height = mask.height
                    width_ratio = 1.2
                    new_height = int(np.linalg.norm(nose_v - chin_bottom_v))

                    # left
                    mask_left_img = mask.crop((0, 0, width // 2, height))
                    mask_left_width = self.get_distance_from_point_to_line(chin_left_point, nose_point, chin_bottom_point)
                    mask_left_width = int(mask_left_width * width_ratio)
                    mask_left_img = mask_left_img.resize((mask_left_width, new_height))

                    # right
                    mask_right_img = mask.crop((width // 2, 0, width, height))
                    mask_right_width = self.get_distance_from_point_to_line(chin_right_point, nose_point, chin_bottom_point)
                    mask_right_width = int(mask_right_width * width_ratio)
                    mask_right_img = mask_right_img.resize((mask_right_width, new_height))

                    # merge mask
                    size = (mask_left_img.width + mask_right_img.width, new_height)
                    mask_img = Image.new('RGBA', size)
                    mask_img.paste(mask_left_img, (0, 0), mask_left_img)
                    mask_img.paste(mask_right_img, (mask_left_img.width, 0), mask_right_img)

                    # rotate mask
                    angle = np.arctan2(chin_bottom_point[1] - nose_point[1], chin_bottom_point[0] - nose_point[0])
                    rotated_mask_img = mask_img.rotate(angle, expand=True)

                    # calculate mask location
                    center_x = (nose_point[0] + chin_bottom_point[0]) // 2
                    center_y = (nose_point[1] + chin_bottom_point[1]) // 2

                    offset = mask_img.width // 2 - mask_left_img.width
                    radian = angle * np.pi / 180
                    box_x = center_x + int(offset * np.cos(radian)) - rotated_mask_img.width // 2
                    box_y = center_y + int(offset * np.sin(radian)) - rotated_mask_img.height // 2

                    # add mask
                    tmp = self._face_img.copy()
                    tmp.paste(mask_img, (box_x, box_y), mask_img)
                    path_splits = os.path.splitext(self.src_path)
                    tmp.save(self.dst_path+"/"+self.src_path.split("/")[-1].strip(".jpg") + "__"+name+"-mask"+"__"+ ".jpg")


    @staticmethod
    def get_distance_from_point_to_line(point, line_point1, line_point2):
        distance = np.abs((line_point2[1] - line_point1[1]) * point[0] +
                          (line_point1[0] - line_point2[0]) * point[1] +
                          (line_point2[0] - line_point1[0]) * line_point1[1] +
                          (line_point1[1] - line_point2[1]) * line_point1[0]) / \
                   np.sqrt((line_point2[1] - line_point1[1]) * (line_point2[1] - line_point1[1]) +
                           (line_point1[0] - line_point2[0]) * (line_point1[0] - line_point2[0]))
        return int(distance)
