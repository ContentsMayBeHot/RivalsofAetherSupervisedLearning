import enum
import numpy as np
import os


class Actions(enum.Enum):
    LEFT = 0
    LEFT_TAP = 1
    RIGHT = 2
    RIGHT_TAP = 3
    UP = 4
    UP_TAP = 5
    DOWN = 6
    DOWN_TAP = 7
    ATTACK = 8
    SPECIAL = 9
    JUMP = 10
    DODGE = 11
    STRONG = 12
    STRONG_LEFT = 13
    STRONG_RIGHT = 14
    STRONG_UP = 15
    STRONG_DOWN = 16
    ANG_RIGHT = 17
    ANG_UP_RIGHT = 18
    ANG_UP = 19
    ANG_UP_LEFT = 20
    ANG_LEFT = 21
    ANG_DOWN_LEFT = 22
    ANG_DOWN = 23
    ANG_DOWN_RIGHT = 24
    ANG_TOGGLE = 25


class Classes(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    ATTACK = 4
    SPECIAL = 5
    JUMP = 6
    DODGE = 7
    STRONG = 8


def rgb2gray(rgb):
    # https://stackoverflow.com/a/12201744
    # Reduces dimensions from (135, 240, 3) to (135, 240, 1)
    gray = np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
    return gray.reshape(135, 240, 1)


def downscale_img(img):
    return None


def pad_clip(x_clip, x_clip_shape, y_clip, y_clip_shape):
    padded_x = np.zeros(x_clip_shape, dtype=np.int32)
    padded_y = np.zeros(y_clip_shape, dtype=np.int32)
    padded_x[:x_clip[0],:x_clip[1],:x_clip[2],:x_clip[3]] = x_clip
    padded_y[:y_clip[0],:y_clip[1]] = y_clip
    return padded_x, padded_y


def reduce_classes(y):
    labels = np.zeros(9).tolist()
    if (y[Actions.LEFT.value]
        or y[Actions.LEFT_TAP.value] == 1
        or y[Actions.STRONG_LEFT.value] == 1
        or y[Actions.ANG_UP_LEFT.value] == 1
            or y[Actions.ANG_DOWN_LEFT.value] == 1):
        labels[Classes.LEFT.value] = 1
    if (y[Actions.RIGHT.value] == 1
        or y[Actions.RIGHT_TAP.value] == 1
        or y[Actions.STRONG_RIGHT.value] == 1
        or y[Actions.ANG_UP_RIGHT.value] == 1
            or y[Actions.ANG_DOWN_RIGHT.value] == 1):
        # Press right
        labels[Classes.RIGHT.value] = 1
    if (y[Actions.UP.value]
        or y[Actions.UP_TAP.value] == 1
        or y[Actions.STRONG_UP.value] == 1
        or y[Actions.ANG_UP_RIGHT.value] == 1
            or y[Actions.ANG_UP_LEFT.value] == 1):
        # Press up
        labels[Classes.UP.value] = 1
    if (y[Actions.DOWN.value]
        or y[Actions.DOWN_TAP.value] == 1
        or y[Actions.STRONG_DOWN.value] == 1
        or y[Actions.ANG_DOWN_RIGHT.value] == 1
            or y[Actions.ANG_DOWN_LEFT.value] == 1):
        # Press down
        labels[Classes.DOWN.value] = 1
    if (y[Actions.ATTACK.value] == 1):
        # Press attack
        labels[Classes.ATTACK.value] = 1
    if (y[Actions.SPECIAL.value] == 1):
        # Press special
        labels[Classes.SPECIAL.value] = 1
    if (y[Actions.JUMP.value] == 1):
        # Press jump
        labels[Classes.JUMP.value] = 1
    if (y[Actions.DODGE.value] == 1):
        # Press dodge
        labels[Classes.DODGE.value] = 1
    if (y[Actions.STRONG.value] == 1
        or y[Actions.STRONG_LEFT.value] == 1
        or y[Actions.STRONG_RIGHT.value] == 1
        or y[Actions.STRONG_UP.value] == 1
            or y[Actions.STRONG_DOWN.value] == 1):
        # Press STRONG
        labels[Classes.STRONG.value] = 1
    return np.array(labels, dtype=np.int32)


def listdir_subdir_only(apath):
    '''listdir filtered to only get folders'''
    return [
        dirent for dirent in os.listdir(apath)
        if os.path.isdir(os.path.join(apath, dirent))
    ]


def listdir_np_only(apath):
    '''listdir filtered to only get numpy pickles'''
    return [
        dirent for dirent in os.listdir(apath)
        if os.path.isfile(os.path.join(apath, dirent))
        and (dirent.endswith('np') or dirent.endswith('npy'))
    ]


def generate_clips(x_data, y_data, x_clip_shape, y_clip_shape, clip_length, reshape_clips=True):  # noqa
    '''
        generate clips from a given video / label pair
        PRE:
            x_data : frames of a video
            y_data : labels of a video
            x_clip_shape : final shape of clip x_data (tuple)
            y_clip_shape : final shape of clip y_data (tuple)
            clip_length : number of frames in a clip
    '''
    clips = []
    for index in range(0, x_data.shape[0], clip_length):
        x_clip = batch_x[index:index + clip_length]
        y_clip = batch_y[index:index + clip_length]

        if(x_clip.shape[0] < CLIP_LENGTH):
            clips.append((x_clip, y_clip))
            continue

    if(reshape_clips):
        for clip in clips:
            clip[0] = clip[0].reshape(x_clip_shape)
            clip[1] = clip[1].reshape(y_clip_shape)

    return clips


def print_matrics(scalars):
    print('Loss: {0:.2f}'.format(scalars[0]), end='\t')
    print('Accuracy: {0:.2f}'.format(scalar[1]))
