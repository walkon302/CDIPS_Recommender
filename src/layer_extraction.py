def layer_feature_extraction(input_folder='br_img',
                             model_name='ResNet50', layer_name='avg_pool'):
    '''
    Parameters:
    -----------
    input_folder: str
        The path of input folder
    model: str
        The name of pre-trained CNN model
    layer_name: str
        The name of layer which we want to extract features from

    Returns:
    --------
    feature_list: dict
        key: The name of image file
        value: The list of extracted features of images within input folder
    '''
    if model_name == 'ResNet50':
        base_model = ResNet50(include_top=False, weights='imagenet')
    elif model_name == 'VGG16':
        base_model = VGG16(include_top=False, weights='imagenet')
        target_size
    else:
        base_model = VGG19(include_top=False, weights='imagenet')
    model = Model(input=base_model.input,
                  output=base_model.get_layer(layer_name).output)

    feature_list = {}

    file_in_list = file_loader(input_folder, 'jpg')
    for img_in_path in file_in_list:
        img = image.load_img(img_in_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        layer_features = model.predict(x)
        flattened_list  = list(itertools.chain(*layer_features.tolist()[0][0]))
        feature_list[img_in_path] = flattened_list
    return feature_list
