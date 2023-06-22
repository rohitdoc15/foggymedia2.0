# import numpy as np
# import matplotlib.cbook as cbook
# import matplotlib.image as image
# import matplotlib.pyplot as plt
# import datetime;
# ct = datetime.datetime.now()
#
# with cbook.Path('sp.png') as file:
#     im = image.imread(file)
#
# fig, ax = plt.text(-5, 60, 'Parabola $Y = x^2$', fontsize = 22)
#
# # ax.plot(np.sin(10 * np.linspace(0, 1)), '-o', ms=20, alpha=0.7, mfc='orange')
# plt.text(-5, 60, 'Parabola $Y = x^2$', fontsize = 22)
# fig.figimage(im ,100, 100, zorder=2, alpha=.5)
#
# plt.show()


import matplotlib

# Enabling interactive backend ipympl in
# jupyter notebook or you can use
# any other backend


import matplotlib

# changing backend

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import datetime;
import matplotlib.image as image
ct = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")

fig = plt.figure(figsize=(10, 10))
COLOR = 'white'
plt.rcParams['text.color'] = COLOR
plt.text(0.1, 0.35, "hi from python", bbox=dict(facecolor='None', alpha=1))
plt.axis('off')
# with cbook.Path('sp.png') as file:
#     im = image.imread(file)
# fig.figimage(im ,100, 100, zorder=2, alpha=.5)
# displaying the figure
plt.show()
