# -*-coding: utf-8 -
'''
    @author: MD. Nazmuddoha Ansary
'''
import numpy as np
import PIL
import PIL.Image , PIL.ImageDraw , PIL.ImageFont 
from .utils import GraphemeParser

#----------------------------------------------------------------
gp=GraphemeParser()


def createPrintedWords(iden,text,font_path,font_size):
    '''
        creates printed word image
        args:
            iden     :       iden to mark the word
            text     :       the text to create the word image
            font_path:       font path to use 
            font_size:       font size of the text
        returns:
            img     :       word image(np.array)
            iden    :       next word identifier
    '''
    # decomp
    comps=gp.process(text,return_graphemes=True)
    if comps is not None:
        # font 
        font=PIL.ImageFont.truetype(font_path, size=font_size)
        
        # construct labels
        imgs=[]
        comp_str=''
        for comp in comps:
            comp_str+=comp
            # draw
            image = PIL.Image.new(mode='L', size=font.getsize("".join(comps)))
            draw = PIL.ImageDraw.Draw(image)
            draw.text(xy=(0, 0), text=comp_str, fill=1, font=font)
            imgs.append(np.array(image))
            
            
        # add images
        img=sum(imgs)
        # offset
        vals=list(np.unique(img))
        vals=sorted(vals,reverse=True)
        vals=vals[:-1]
        
        _img=np.zeros(img.shape)
        for v in vals:
            _img[img==v]=iden
            iden+=1
        return _img,iden
    else:
        return None,None