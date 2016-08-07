#!/usr/bin/env python3

# Charles McEachern

# Spring 2016

# ######################################################################
# ############################################################# Synopsis
# ######################################################################

# WIP...

# ######################################################################
# ################################################## Import Dependencies
# ######################################################################

import numpy as np

import random

from urllib.request import urlretrieve

## For conveniently parsing HTML. 
#from bs4 import BeautifulSoup

# We use Matplotlib's image library to display images. 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# For navigating between directories. 
import os

## For choosing randomly from a list. 
#from random import choice

## For grabbing HTML and images from online. 
#from urllib2 import urlopen

# ######################################################################
# ############################################## Double Faced Card Class
# ######################################################################

class dfc(object):

    url_root = 'http://mtg.wtf/cards/'

    abbr, num = None, None

    front, back, flip = None, None, None

    # ==================================================================
    # ========================================== Initialize Pixel Arrays
    # ==================================================================

    def __init__(self, abbr, num):

        self.abbr, self.num = abbr, str(num)

        # Check if we already have images for this card. If not,
        # download them. 
        for side in ('a', 'b'):
            if os.path.exists( self.path(side) ):
                print( 'already have ', self.path(side) )
            else:
                print( 'getting ', self.path(side) )
                urlretrieve( self.url(side), self.path(side) )

        # Load the front and back images into arrays.
        self.front = mpimg.imread( self.path('a') )[:, :, :3]
        self.back = mpimg.imread( self.path('b') )[:, :, :3]
        # Sanity check: are the pixel arrays the same shape?
        assert self.front.shape == self.back.shape
        # Create a third array. We'll squish the front and back onto it,
        # shaped like a flip card. 
        self.flip = np.zeros(self.front.shape)
        return

    # ------------------------------------------------------------------

    def path(self, side):
        return self.abbr + self.num + side + '.png'

    # ------------------------------------------------------------------

    def url(self, side):
        return self.url_root + self.abbr + '/' + self.num + side + '.png'



    def flip_flip(self):
        # It's easier to flip the canvas than it is to rearrange all the
        # little pieces we're putting onto it.
        self.flip = self.flip[::-1, ::-1]








# ######################################################################
# ################################################################# Main
# ######################################################################

'''
def path(abbr, num, side=None):
    return abbr + str(num) + ( '' if side is None else side ) + '.png'

def url(abbr, num, side=None):
    return 'http://mtg.wtf/cards/' + abbr + '/' + str(num) + ( '' if side is None else side ) + '.png'
'''

def main():

    prowler = dfc('emn', 163)

    '''
    # List the flip cards we care about. 
    abbr_num = ( ('soi', 203), ('soi', 209), ('soi', 215), ('emn', 163) )

    # Also a blank card of each color, so we can get rid of the divot in
    # the frame just above the power/toughness box. 
    blanks = ( ('emn', 164), ('emn', 164), ('emn', 164), ('emn', 164), ('emn', 164) )

    # Grab the image for any flip card we're missing. 
    for abbr, num in abbr_num:
        for side in ('a', 'b'):
            if not os.path.exists( path(abbr, num, side) ):
                print( 'getting', path(abbr, num, side) )
                urllib.request.urlretrieve( url(abbr, num, side), path(abbr, num, side) )
            else:
                print( 'already have', path(abbr, num, side) )

    # Grab any blanks we're missing. 
    for color, (abbr, num) in zip('wubrg', blanks):
        if os.path.exists(color + '.png'):
            print('already have ' + color + '.png')
        else:
            print('getting ' + color + '.png')
            urllib.request.urlretrieve(url(abbr, num), color + '.png')

    # Read in an array of pixels. Chop off the alpha channel. 
    abbr, num = abbr_num[-1]
    patha, pathb = path(abbr, num, 'a'), path(abbr, num, 'b')

    imga = mpimg.imread(patha)[:, :, :3]
    imgb = mpimg.imread(pathb)[:, :, :3]
    img_ = mpimg.imread('g.png')[:, :, :3]

    # Sanity check. 
    assert imga.shape == imgb.shape
    assert imga.shape == img_.shape

    '''

    # Flip the back upside down. 
    imga = prowler.front
    imgb = prowler.back

    # Canvas for assembling the flip version. 
    imgc = np.zeros(imga.shape)

    # Where are the art box, the text box, and the power/toughness box?
    art_t, art_b = 35, 173
    art_l, art_r = 17, 205
    txt_t, txt_b = 195, 275
    txt_l, txt_r = art_l, art_r
    clr_t, clr_b = 286, 290
    pow_t, pow_b = txt_b, 296
    pow_l = imga.shape[1]//2

    # Title line. 
    titlea = imga[:art_t, :]
    imgc[:art_t, :] = titlea
    titleb = imgb[:art_t, :]
    imgc[-art_t:, :] = titleb[::-1, ::-1]

    # Art framing. 
#    new_art_h = (art_b - art_t)//3
    new_art_h = 45

    print('New art height:', new_art_h)

    new_art_b = art_t + new_art_h
    larta = imga[art_b - new_art_h:art_b, :art_l]
    imgc[art_t:art_t + new_art_h, :art_l] = larta
    rarta = imga[art_b - new_art_h:art_b, art_r:]
    imgc[art_t:new_art_b, art_r:] = rarta
    # Flipping the template is easier than flipping the chunks. 
    imgc = imgc[::-1, ::-1]
    # Same as above. 
    lartb = imgb[art_b - new_art_h:art_b, :art_l]
    imgc[art_t:new_art_b, :art_l] = lartb
    rartb = imgb[art_b - new_art_h:art_b, art_r:]
    imgc[art_t:new_art_b, art_r:] = rartb
    # Flip the canvas back. 
    imgc = imgc[::-1, ::-1]

    # Type line. 
    type_h = txt_t - art_b
    new_txt_t = new_art_b + type_h
    typea = imga[art_b:txt_t, :]
    imgc[new_art_b:new_txt_t, :] = typea
    # Flip the canvas, do the back side, flip it back. 
    imgc = imgc[::-1, ::-1]
    typeb = imgb[art_b:txt_t, :]
    imgc[new_art_b:new_txt_t, :] = typeb
    imgc = imgc[::-1, ::-1]

    # Text box framing. 
#    new_txt_h = (txt_b - txt_t)//2
    new_txt_h = 34

    apparent_new_txt_h = new_txt_h + (clr_t - txt_b)

    print('New text box height:', new_txt_h, '(but looks like', apparent_new_txt_h, ')')

    new_txt_b = new_txt_t + new_txt_h
    ltxta = imga[txt_b - new_txt_h:txt_b, :art_l]
    imgc[new_txt_t:new_txt_b, :art_l] = ltxta

    rtxta = imga[txt_b - new_txt_h:txt_b, art_r:]

    imgc[new_txt_t:new_txt_b, art_r:] = rtxta
    # Flip the canvas, do the back side, flip it back. 
    imgc = imgc[::-1, ::-1]
    ltxtb = imgb[txt_b - new_txt_h:txt_b, :art_l]
    imgc[new_txt_t:new_txt_b, :art_l] = ltxtb
    rtxtb = imgb[txt_b - new_txt_h:txt_b, art_r:]
    imgc[new_txt_t:new_txt_b, art_r:] = rtxtb
    imgc = imgc[::-1, ::-1]

    # Colored line at the bottom of the text box. 
    new_clr_b = new_txt_b + (clr_b - txt_b)
    clra = imga[txt_b:clr_b, :]
    imgc[new_txt_b:new_clr_b] = clra
    # Flip the canvas, do the back side, flip it back. 
    imgc = imgc[::-1, ::-1]
    clrb = imgb[txt_b:clr_b, :]
    imgc[new_txt_b:new_clr_b] = clrb
    imgc = imgc[::-1, ::-1]

    # Fill in the space between with border color. 
    border_color = imga[3, 20]
#    imgc[new_clr_b:-new_clr_b, :] = border_color

    # Power and toughness box. Only do this on the right side, so the
    # top and bottom boxes can stagger a bit. 
    new_pow_b = new_clr_b + (pow_b - clr_b)
    powa = imga[clr_b:pow_b, pow_l:]
    imgc[new_clr_b:new_pow_b, pow_l:] = powa
    # Flip the canvas, do the back side, flip it back. 
    imgc = imgc[::-1, ::-1]
    powb = imgb[clr_b:pow_b, pow_l:]
    imgc[new_clr_b:new_pow_b, pow_l:] = powb
    imgc = imgc[::-1, ::-1]









    # We'll plot a triple-wide image: front, back, and flip. 
    new_img_shape = np.array(imga.shape)*(1, 3, 1)
    new_img = np.zeros(new_img_shape)

    # Put the front in the first slot and the back in the second slot.
    # We'll stitch them together in the third slot. 
    card_width = imga.shape[1]
    new_img[:, :card_width] = imga
    new_img[:, card_width:2*card_width] = imgb
    new_img[:, 2*card_width:] = imgc






#    # Fuzz the borders a bit. Maybe not necessary?
#    avg_t = np.mean(imga[art_t, art_l:art_r+1], axis=0)
#    avg_b = np.mean(imga[art_b, art_l:art_r+1], axis=0)
#    avg_l = np.mean(imga[art_t:art_b+1, art_l], axis=0)
#    avg_r = np.mean(imga[art_t:art_b+1, art_r], axis=0)
#    new_img[art_t, art_l:art_r+1] = avg_t
#    new_img[art_b, art_l:art_r+1] = avg_b
#    new_img[art_t:art_b+1, art_l] = avg_l
#    new_img[art_t:art_b+1, art_r] = avg_r

    red = np.array( [1, 0, 0] )

    # We'll cut the height of the art in half. 
    new_art_h = (art_b - art_t)//3
    # Set the top and bottom of the new art. 
    new_art_t = art_t + 10
    new_art_b = new_art_t + new_art_h
    # Paint the part of the art we're not using red. 
    new_img[art_t:new_art_t, art_l:art_r+1] = red
    new_img[new_art_b:art_b, art_l:art_r+1] = red
    # Cut the margins in a different place to reduce the number of seams. 
    cut = (art_b - art_t) - (new_art_b - new_art_t)
    new_img[art_t:art_t+cut, :art_l] = red
    new_img[art_t:art_t+cut, art_r:card_width] = red

    # Keep half of the text box. 
    new_txt_h = (txt_b - txt_t)//2

    new_txt_t = txt_t + 12
    new_txt_b = new_txt_t + new_txt_h

    new_img[txt_t:new_txt_t, art_l:art_r+1] = red
    new_img[new_txt_b:txt_b, art_l:art_r+1] = red

    cut = (txt_b - txt_t) - (new_txt_b - new_txt_t)

    new_img[txt_t:txt_t+cut, :art_l] = red
    new_img[txt_t:txt_t+cut, art_r:card_width] = red


    # Chunks need to be cut out of the text box and margins in different places to preserve the curvature at the bottom. 


    # Where's the text box?
#    new_img[txt_t, art_l:art_r+1] = red
#    new_img[txt_b, art_l:art_r+1] = red

    new_img[286, art_l:art_r+1] = red
    new_img[290, art_l:art_r+1] = red
    new_img[295, art_l:art_r+1] = red



#    # Left side of the art. 
#    img[:, 18] = 255

#    # Right side of the art.
#    img[:, -19] = 255

#    # Top of the art. 
#    img[36, :] = 255

#    # Bottom of the art. 
#    img[172, :] = 255

    # Fire up a plot figure in the proportions of three cards.
    plt.figure( figsize=(15, 7) )
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)


    # Turn those pixels into a plot. 
    plt.imshow(new_img)

    plt.show()

    return

# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()
