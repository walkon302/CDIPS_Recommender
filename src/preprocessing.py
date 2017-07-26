def br_grabcut(input_folder='test_img', output_folder='br_img'):
    '''
    Parameters:
    -----------
    input_folder: str
        The path of input folder
    output_folder: str
        The path of output folder

    Returns:
    --------
        Generate imags with background removed with grabcut algorithm.
    '''
    file_in_list = file_loader(input_folder, 'jpg')
    try:
        os.makedirs(output_folder)
    except OSError:
        if not os.path.isdir(output_folder):
            raise

    for img_in_path in file_in_list:
        img = cv2.imread(img_in_path)
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (35,50,165,250)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        cv2.imwrite(output_folder + '/' +
                    img_in_path[len(input_folder)+1:], img)
