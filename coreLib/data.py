# -*-coding: utf-8 -
'''
    @author: Mobassir
'''
#--------------------
# imports
#--------------------
import random
from .config import config
from .text import *
from .textimage import createPrintedWords,gp
import numpy as np
import cv2
import PIL
import PIL.Image , PIL.ImageDraw , PIL.ImageFont 



def create_marked_word(ds,lang,iden,font_path=None,font_size=None):
    '''
        creates a marked word
        args:
            ds       :   dataset resource
            lang     :   language to use
            iden     :   word identifier start
            font_path:   the specific font to usefor line in para_data:
            print(line)
        
            font_size:   the specific size to use
    '''
    
    # gen image
    if font_path is None:
        # string to dict lang object
        lang=languages[lang]
        if lang.iden=="bangla":
            font_path=random.choice(ds.fonts.bangla)
        else:
            font_path=random.choice(ds.fonts.english)
    
    if font_size is None:
        font_size=random.randint(config.font_size_min,config.font_size_max)

    # generate text
    text=generate_single_word_text(lang.valid)
    # un-processed image
    image,iden=createPrintedWords(iden,text,font_path,font_size)
    return image,iden

def create_text_line(ds,lang,iden,font_path=None):
    '''
        creates a marked line
        args:
            ds       :   dataset resource
            lang     :   language to use
            iden     :   word identifier start
    '''
    # string to dict lang object
    if font_path is None:
        lang=languages[lang]
    
        if lang.iden=="bangla":
            font_path=random.choice(ds.fonts.bangla)
        else:
            font_path=random.choice(ds.fonts.english)
    font_size=config.font_size_max
    
    num_words=random.randint(config.min_word_in_line,config.max_word_in_line)

    words=[]
    for i in range(num_words):
        text=generate_single_word_text(lang.valid)
        
        if i<num_words-1:
            text+=" "
        word,iden=createPrintedWords(iden,text,font_path,font_size)
        if word is not None:
            words.append(word)
    
    # fix height
    max_h=0
    for word in words:
        h,w=word.shape
        max_h=max(h,max_h)
    # resize
    resized_words=[]
    for word in words:
        h,w=word.shape
        new_width=int(max_h*(w/h))
        word=cv2.resize(word,(new_width,max_h),fx=0,fy=0,interpolation = cv2.INTER_NEAREST)
        resized_words.append(word)
    image=np.concatenate(resized_words,axis=1)
    return image,iden


def create_text_line_from_text(ds,lang,iden,text,font_path=None):
    '''
        creates a marked line
        args:
            ds       :   dataset resource
            lang     :   language to use
            iden     :   word identifier start
            text     :   line text
    '''
    # words
    words=text.split()
    # string to dict lang object
    if font_path is None:
        lang=languages[lang]
    
        if lang.iden=="bangla":
            font_path=random.choice(ds.fonts.bangla)
        else:
            font_path=random.choice(ds.fonts.english)
    font_size=config.font_size_max
    
    
    word_imgs=[]
    for i in range(len(words)):
        word_text=words[i]
        
        if i<len(words)-1:
            word_text+=" "
        word,iden=createPrintedWords(iden,word_text,font_path,font_size)
        if word is not None:
            word_imgs.append(word)
    # fix height
    max_h=0
    for word in word_imgs:
        h,w=word.shape
        max_h=max(h,max_h)
    # resize
    resized_words=[]
    for word in word_imgs:
        h,w=word.shape
        new_width=int(max_h*(w/h))
        word=cv2.resize(word,(new_width,max_h),fx=0,fy=0,interpolation = cv2.INTER_NEAREST)
        resized_words.append(word)
    image=np.concatenate(resized_words,axis=1)
    return image,iden

def fix_alignment(img,max_width,alignment):
    '''
        fixes alignment
        args:
            img         :   image to align
            max_width   :   width to fix text
            alignment   :   the alignment to set the image
    '''
    h,w=img.shape
    if w<max_width:
        if alignment=="center":
            left_w=(max_width-w)//2
            right_w=max_width-w-left_w
            left_pad=np.zeros((h,left_w))
            right_pad=np.zeros((h,right_w))
            img=np.concatenate([left_pad,img,right_pad],axis=1)
        else:
            pad_w=max_width-w
            pad=np.zeros((h,pad_w))
            if alignment=="left":
                img=np.concatenate([img,pad],axis=1)
            else:
                img=np.concatenate([pad,img],axis=1)
    return img

def create_paragraph(ds,lang,iden,alignment):
    '''
        creates a marked line
        args:
            ds       :   dataset resource
            lang     :   language to use
            iden     :   word identifier start
            alignment:   left,right,center,middle
    
    '''
    # string to dict lang object
    lang=languages[lang]
    
    if lang.iden=="bangla":
        font_path=random.choice(ds.fonts.bangla)
    else:
        font_path=random.choice(ds.fonts.english)
    
    num_lines=random.randint(config.min_line_in_para,config.max_line_in_para)
    if alignment!="middle":
        lines=[]
        for _ in range(num_lines):
            line_img,iden=create_text_line(ds,lang,iden,font_path)
            lines.append(line_img)
        # padding
        max_w=0
        for line in lines:
            h,w=line.shape
            max_w=max(max_w,w)
        # correcting alignment
        paded_lines=[]
        for line in lines:
            line=fix_alignment(line,max_w,alignment)
            paded_lines.append(line)
        para=np.concatenate(paded_lines,axis=0)
    else:
        para=[]
        # 1st line text
        num_words=random.randint(config.min_word_in_line,config.max_word_in_line)
        line=generate_single_line_text(lang.valid,num_words)
        para.append(line)
        # rest line text
        len_line=len(line)
        for _ in range(num_lines-1):
            line=generate_single_line_text_by_lenght(lang.valid,len_line)
            para.append(line)
        # reset len
        para_data=[]
        font_size=config.font_size_max
        font=PIL.ImageFont.truetype(font_path, size=font_size)
        min_size=min([font.getsize(line)[0] for line in para])
        for line in para:
            
            while font.getsize(line)[0]>min_size:
                comps=gp.process(line,return_graphemes=True)
                line="".join(comps[:-1])
            para_data.append(line)
            
        # create text line
        para_images=[]
        for line in para_data:
            line,iden=create_text_line_from_text(ds,lang,iden,line,font_path)
            para_images.append(line)
        
        # padding
        max_w=0
        for line in para_images:
            h,w=line.shape
            max_w=max(max_w,w)
        # correcting alignment
        paded_lines=[]
        for line in para_images:
            line=fix_alignment(line,max_w,"left")
            paded_lines.append(line)
        
        para=np.concatenate(paded_lines,axis=0)

    return para,iden



