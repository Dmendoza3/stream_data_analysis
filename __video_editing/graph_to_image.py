import matplotlib.pyplot as plt
import numpy as np

def plot_to_img(values, filename="plot.png"):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    data = np.array(values)
    x, y = data.T
    ax.plot(x, y)
    fig.set_size_inches(30.5, 10.5, forward=True)
    fig.set_dpi(100)
    fig.savefig(filename)   
    plt.close(fig)
    #plt.show()

if __name__=="__main__":
    plot_to_img([])