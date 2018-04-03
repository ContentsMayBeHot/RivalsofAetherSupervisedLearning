import os
import time
import numpy as np
from operator import itemgetter
import skimage.io


class SyncedFrame:
    def __init__(self, frame, action_matrix):
        self.frame = frame
        self.actions = action_matrix

    def normalize(self):
        if self.actions is None:
            self.actions = np.zeros(26)


class SyncedReplay:
    def __init__(self):
        self.list = []
        self.synced_frames = []

    def create_sync_from_npys(self, frame_dirpath, numpy_path):
        self.initialize_frames(frame_dirpath)
        self.initialize_actions_from_npy(numpy_path)
        self.sync_actions()

    def initialize_frames(self, frame_dirpath):
        for numpy_fname in os.listdir(frame_dirpath):
            if numpy_fname.endswith(".np") or numpy_fname.endswith(".npy"):
                f_out = open(os.path.join(frame_dirpath, numpy_fname), "rb")
                frame_num = 0
                if numpy_fname.endswith(".np"):
                    frame_num = int(numpy_fname[:-3])
                else:
                    frame_num = int(numpy_fname[:-4])
                data = np.load(f_out)
                f_out.close()
                self.list.append((frame_num, data, True))

    def initialize_actions_from_npy(self, action_numpypath):
        actions = np.load(action_numpypath)
        for action in actions:
            self.list.append((action[0], action[1], False))

    def sync_actions(self):
        self.list.sort(key=itemgetter(0))

        temp_actions = None

        for item in self.list:
            if item[2]:
                self.synced_frames.append(SyncedFrame(item[1], temp_actions))
                self.synced_frames[-1].normalize()
                temp_actions = None

            else:
                if temp_actions is None:
                    temp_actions = item[1]

                else:
                    temp_actions = np.add(temp_actions, item[1])

    def normalize(self):
        for synced in self.synced_frames:
            synced.normalize()


if __name__ == "__main__":

    synced = SyncedReplay()
    synced.create_sync_from_npys("data/frames/", "data/labels/roa_0.np")

    for s_frame in synced.synced_frames:

        action_str = ""
        if s_frame.actions is not None:
            action_str = str(s_frame.actions)

        f_out = open("output/action.txt", "w+")
        f_out.write(action_str)
        f_out.close()
        skimage.io.imsave('output/frame.png', s_frame.frame)
        input("Press Enter to Progress Frame...")

    print("OWO: It Doesn't Error")
