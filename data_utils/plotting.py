from typing import List
import os
import matplotlib.pyplot as plt
import numpy as np


def plot_curves(values: List[np.ndarray], titles: List[str], plot_title: str,
                x=None, x_label="Epoch", show=True, save=False, save_path=None):
    
    if save: assert save_path is not None

    if x is None:
        x = np.arange(len(values[0]))

    f1 = plt.figure(dpi=200)
    plots = []
    for plot_values in values:
        plot, = plt.plot(x, plot_values)
        plots.append(plot)
    plt.legend(tuple(plots), tuple(titles))
    plt.xlabel(x_label)
    plt.title(plot_title)

    if save:
        plt.savefig(os.path.join(save_path, "loss.png"), bbox_inches="tight", pad_inches=0.1)

    if show:
        plt.show()