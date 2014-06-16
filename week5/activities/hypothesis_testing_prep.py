
import astropy.io.fits as pf
from astropy import wcs

# http://www.mpia-hd.mpg.de/homes/ianc/python/phot.html

data, header = pf.getdata('data/star_field.fits', header=True)

wcs_header = wcs.WCS('data/star_field.fits')

center_pix = wcs_header.wcs_world2pix(0, 0, 0)

bg_box = (117, 82, 134, 103)

x_axis = np.linspace(0, data.shape[0]-1, data.shape[0])
y_axis = np.linspace(0, data.shape[1]-1, data.shape[1])

x, y = np.meshgrid(x_axis, y_axis)

def get_box_pix(data, box):
    box_data = data[(x > box[1]) & \
                    (x < box[3]) & \
                    (y > box[0]) & \
                    (y < box[2])]
    return box_data

bg_pix = get_box_pix(data, bg_box)

star_box = (110, 106, 117, 114)

star_pix = get_box_pix(data, star_box)

plt.hist(bg_pix)
plt.hist(star_pix, bins=50)
plt.show()







