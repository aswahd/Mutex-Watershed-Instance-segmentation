from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

# Instance segmentation label
img_path = "cable.png"  # "plant017_label.png" or "cable.png"

img = np.array(Image.open(img_path))[np.newaxis]  # (1, h, w)
## Generate affinity
import numpy as np
from affogato.affinities import compute_affinities


def generate_offsets():
    out = []
    D = [1, 2, 4, 8, 16, 32, 64]
    offset = [[0, -1, 0], [0, 0, -1], [0, 1, 0], [0, 0, 1]]
    for stride in D:
        out.extend([[stride * z, stride * y, stride * x] for z, y, x in offset])
    return out


offsets = generate_offsets()
# Alternative offsets
# offsets = [
#     [0, -1, 0], [0, 0, -1],
#     [0, -1, -1], [0, 1, 1], [0, -1, 1], [0, 1, -1],
#     [0, -9, 0], [0, 0, -9],
#     [0, -9, -9], [0, 9, -9], [0, -9, -4],
#     [0, -4, -9], [0, 4, -9], [0, 9, -4],
#     [0, -27, 0], [0, 0, -27], [0, -27, 27]
# ]

# Affinities
affs, _ = compute_affinities(img.astype(np.uint64), offsets)

## Mutex Watershed
from elf.segmentation.mutex_watershed import mutex_watershed

pred_seg = mutex_watershed(1 - affs, offsets=offsets, strides=[1, 1, 1], mask=np.greater(img, 0).astype(np.int16)).astype(np.uint16)
# fig, axes = plt.subplots(1, 2)
# axes[0].imshow(img[0])
# axes[1].imshow(pred_seg[0])
# fig.show()
#
plt.imshow(pred_seg[0])
# plt.savefig('plant017_output.png', bbox_inches='tight')
print("End")
