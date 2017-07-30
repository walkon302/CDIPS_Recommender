
import numpy as np
from IPython.core.debugger import Tracer
import pandas as pd


def dot(K, L):
    if len(K) != len(L): return 0
    return sum(i[0]*i[1] for i in zip(K, L))

def similarity(item_1, item_2):
        return dot(item_1, item_2) / np.sqrt(dot(item_1, item_1)*dot(item_2, item_2))


def get_user_buy_spu(user_id,user_profile):
    '''Returns the FIRST buy_spu for each user'''
    trajectory = user_profile.loc[user_profile.user_id==user_id,]
    return(trajectory.buy_spu.as_matrix()[0])


def rank_candidates(user_id,user_profile,spu_fea,method='AverageFeatureSim',extra_inputs={},randomize_scores=False):
        '''
        Parameters:
        -----------
        user_id: str
        user_profile: DataFrame
            Can be sub-sampled

        Changes:
        ---------
        - migth use the buy item as the input.

        Return:
        -------
        ranked_candidates: DataFrame
            Returns a dictionary with (spu; rank) for each item in the candidate list
        '''
        # get bought item
        buy_spu = get_user_buy_spu(user_id,user_profile)

        # find buy item categoriy
        buy_sn = user_profile.loc[user_profile['buy_spu']==buy_spu,'buy_sn'].as_matrix()[0] # should assert they are all the same

        # find all other items in the category: CAREFUL THIS IS A SUBSET
        spus_in_category_b = user_profile.loc[user_profile.buy_sn==buy_sn,'buy_spu'].unique()
        spus_in_category_v = user_profile.loc[user_profile.view_sn==buy_sn,'view_spu'].unique()
        spus_in_category = list(set(list(spus_in_category_b)+list(spus_in_category_v))) # take intersection

        # make sure buy item is in list
        assert buy_spu in spus_in_category

        item_score_in_category = pd.DataFrame(data = spus_in_category,columns=['spu'])


        if randomize_scores:
            item_score_in_category['score'] = np.random.randn(len(item_score_in_category))
            #Tracer()()
        else:
            # for each item calculate the recommendation score (this might be similarity or some other)
            for candidate_spu in spus_in_category:
                 item_score_in_category.loc[item_score_in_category['spu']==candidate_spu,'score'] = recommendation_score(user_id,candidate_spu,user_profile,spu_fea,method=method,extra_inputs=extra_inputs)

        # rank candidates by score
        item_score_in_category['rank']=item_score_in_category['score'].rank()

        # put bought or not
        item_score_in_category['buy']=np.zeros(len(item_score_in_category))
        item_score_in_category.loc[item_score_in_category.spu==buy_spu,'buy']=1
        assert len(item_score_in_category.loc[item_score_in_category.buy==1,'rank'].as_matrix())==1 # make sure buy item is only in there once

        return(item_score_in_category)




def recommendation_score(user_id,candidate_spu,user_profile,spu_fea,method='AverageFeatureSim',extra_inputs={}):
    # Actually maybe don't do this per item.
    '''TO-DO: load each item out of database?'''

    if method=='AverageFeatureSim':

        # could just calculate the average features here instead of generating them #
        average_features = get_user_average_features(user_id,user_profile,spu_fea)

        # load nn features for candidate item
        try:
            features_other = spu_fea.loc[spu_fea.spu_id==candidate_spu,'features'].as_matrix()[0] # return a 1-D np array
        except:
            features_other = np.ones(len(average_features))
            print('missing a candidates features ui:'+str(user_id)+' spu:'+str(candidate_spu))

        return(similarity(average_features,features_other))


    if method=='LastItemSim':

        # get his trajectory
        trajectory = user_profile.loc[user_profile.user_id==user_id,]

        # remove buy item
        trajectory = trajectory.loc[trajectory.view_spu!=trajectory.buy_spu.as_matrix()[0]]

        # get last item and its features
        lastitem_spu = trajectory.loc[trajectory.time_interval==np.min(trajectory.time_interval),'view_spu'].as_matrix()[0]
        features_lastitem = spu_fea.loc[spu_fea.spu_id==lastitem_spu,'features'].as_matrix()[0] # return a 1-D np array

        # get candidate item features
        try:
            features_candidate = spu_fea.loc[spu_fea.spu_id==candidate_spu,'features'].as_matrix()[0] # return a 1-D np array
        except:
            features_candidate = np.ones(len(features_lastitem))
            print('missing a candidates features ui:'+str(user_id)+' spu:'+str(candidate_spu))
        # return similarity
        return(similarity(features_lastitem,features_candidate))


    #if method=='AverageFeatureSim_Weighted':

        # load user's average features that are weighted by classification problems weights (striped v not)

        # load candidates average features that are weighted by classification problem weights

    #if method=='Popularity':
        # return item based on popularity #


    #if method=='Classify_User'



###### NATHAN's METHOD

def get_user_average_features(user_id,user_profile,spu_fea):

    # calculates the average feature from each user #
    average_viewed_features_dict = {}

    # get his trajectory
    trajectory = user_profile.loc[user_profile.user_id==user_id,]

    # remove buy item
    trajectory = trajectory.loc[trajectory.view_spu!=trajectory.buy_spu.as_matrix()[0]]

    n_features = len(spu_fea.features.as_matrix()[0])
    n_views = len(trajectory)

    # loop through sequence of views and store feature vect into matrix
    features_items = np.empty((n_features,n_views))
    for vi,view_spu in enumerate(trajectory.view_spu):
            # load features for image
            features_items[:,vi] = spu_fea.loc[spu_fea.spu_id==view_spu,'features'].as_matrix()[0] # return a 1-D np array
    avg_feature_vec = np.mean(features_items,axis=1)

    return(avg_feature_vec)

#def gener
