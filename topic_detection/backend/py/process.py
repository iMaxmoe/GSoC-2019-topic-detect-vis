#!/usr/bin/env python

import datetime
import subprocess
import glob
import generate_chunk_ner_struc
from multiprocessing import Pool
import read_data
import get_pair_data

import topic_clustering
import os
import nltk
import ner
import shutil

import save_clusters

import sort
import sys
import pickle
import tracking_v2

import subprocess
import shutil
#sys.path.append('/home/vcla/Desktop/VCLA/cartago_news/election_related/')
#sys.path.append('/home/weixin/Desktop/VCLA/cartago_news/election_related/')
#import generate_candidate_sentence_file
#import issue_classify
#import combine_agenda_week
#import run_week_topics
import topic_clustering_v2
import save_clusters_v2 

### make sure you have access to cartago: csa@164.67.183.179
### start the ner server: java -mx1000m -cp stanford-ner-3.4.jar:stanford-corenlp-caseless-2014-02-25-models.jar edu.stanford.nlp.ie.NERServer -loadClassifier edu/stanford/nlp/models/ner/english.muc.7class.caseless.distsim.crf.ser.gz -port 8080 -outputFormat inlineXML
def main():
    
    # get the date of yesterday
    yesterday = datetime.date.today()-datetime.timedelta(1)
    year = str(yesterday.year).zfill(4)
    month = str(yesterday.month).zfill(2)
    day = str(yesterday.day).zfill(2)
    
    #pickle.dump(day, open('/home/vcla/Desktop/VCLA/cartago_news/yesterday','w'))    
    #paras = sys.argv
    #year = paras[1]
    #month = paras[2]
    #day = paras[3]
    
    #year = '2016'
    #month = '03'
    #day = '26'
    
    process(year, month, day)
    

    
    #year = '2015'
    #month = '12'
    #for dd in range(12, 16):
    #    day = str(dd).zfill(2)
    #    process(year, month, day)

    #month = '09'

    #for dd in range(1, 31):
    #    day = str(dd).zfill(2)
    #    process(year, month, day)



def process(year, month, day):
    
    #############################################################################
    # download the data for yesterday
    hierarchy = year+'/'+year+'-'+month+'/'+year+'-'+month+'-'+day+'/'
    print hierarchy

    path_pre = '/home/csa/CAS2/weixin/cartago_news_process_TDT_StorySeg/'
    
    #cartago_path = 'csa@164.67.183.179:/sweep/'+ hierarchy #'liweixin@164.67.183.182:/sweep/'+ hierarchy #'csa@164.67.183.179:/sweep/'+ hierarchy #'csa@164.67.183.179:/tvspare/tv/'+ hierarchy
    #local_path = '/home/weixin/Desktop/VCLA/cartago_news/tv/' + hierarchy #'/home/vcla/Desktop/VCLA/cartago_news/tv/' + hierarchy
    
    cartago_path = '/sweep/' + hierarchy
    local_path = path_pre + 'tv/' + hierarchy
    if not os.path.exists(local_path):
        os.makedirs(local_path, 0777)
    
    
    #cnn_delete_names = ['US_CNN_CNN_Special_Report', 'US_CNN_Piers_Morgan_Tonight', 'US_CNN_CNN_Presents', 'US_CNN_Reliable_Sources', 'US_CNN_State_of_the_Union', 'US_CNN_Fareed_Zakaria_GPS']
    #fox_delete_names = ['US_FOX-News_The_OReilly_Factor', 'US_FOX-News_Hannity', 'US_FOX-News_Journal_Editorial_Report', 'US_FOX-News_Special_Report_with_', 'US_FOX-News_Fox_and_Friends', 'US_FOX-News_Fox_News_Watch']
    #msnbc_delete_names = ['US_MSNBC_Up_with_', 'US_MSNBC_Melissa_Harris-Perry', 'US_MSNBC_Meet_the_Press', 'US_MSNBC_The_Daily_Rundown', 'US_MSNBC_Martin_Bashir', 'US_MSNBC_Hardball_with_Chris_Matthews', 'US_MSNBC_Politics_Nation_With_', 'US_MSNBC_All_In_With_']
    #abc_delete_names = ['US_KABC_Jimmy_Kimmel_Live', 'US_KABC_Good_Morning_America_Sunday', 'US_KABC_This_Week', 'US_KABC_Good_Morning_America', 'US_KABC_Live_With_', 'US_KABC_The_View', 'US_KABC_The_Doctor_Oz_Show', 'US_KABC_20-20']
    #cbs_delete_names = ['US_KCBS_Entertainment_Tonight', 'US_KCBS_The_Insider', 'US_KCBS_Late_Show_with_Dave_Letterman', 'US_KCBS_Late_Late_Show_with_', 'US_KCBS_What_America_Thinks_with', 'US_KCBS_Face_the_Nation', 'US_KCBS_60_Minutes', 'US_KCBS_48_Hours', 'US_KCBS_Brooklyn_DA']
    #nbc_delete_names = ['US_KNBC_EXTRA', 'US_KNBC_Access_Hollywood', 'US_KNBC_Dateline_NBC', 'US_KNBC_Rock_Center_with_', 'US_KNBC_Tonight_Show_with_', 'US_KNBC_Late_Night_with_', 'US_KNBC_Saturday_Night_Live', 'US_KNBC_KNBC_News_Conference', 'US_KNBC_The_Ellen_DeGeneres_Show']

    #local_news_name = ['US_KABC_Eyewitness_News', 'US_KABC_KABC_7_News', 'US_KABC_KABC_Eyewitness_News', 'US_KABC_Today_in_LA', 'US_KCBS_CBS_2_News', 'US_KCBS_KCBS_2_News', 'US_KNBC_Channel_4_News', 'US_KNBC_KNBC_4_News', 'US_KNBC_Today_in_LA', 'US_KTTV-FOX_Morning_News', 'US_KTTV-FOX_Ten_OClock_News', 'US_KCAL_KCAL_9_News', 'US_KTLA_KTLA_News']
    #national_news_name = ['US_KABC_20-20', 'US_KABC_ABC_World_News', 'US_KABC_Good_Morning_America', 'US_KABC_Nightline', 'US_KABC_This_Week', 'US_KABC_World_News_Tonight_With_David_Muir', 'US_KCBS_48_Hours', 'US_KCBS_60_Minutes', 'US_KCBS_CBS_Evening_News', 'US_KCBS_CBS_News_Sunday_Morning', 'US_KCBS_Face_the_Nation', 'US_KCBS_This_Morning', 'US_KNBC_NBC_Nightly_News', 'US_KNBC_Today_Show', 'US_KNBC_Today_Weekend', 'US_KNBC_KNBC_Early_Today']    
    
    
    #subprocess.call(['scp', cartago_path + '*_US_*.txt', local_path])
    #print 'Finish downloading'
    ##subprocess.call(['scp', cartago_path + '*_US_CNN_*.txt', local_path])
    ##subprocess.call(['scp', cartago_path + '*_US_FOX-News_*.txt', local_path])
    ##subprocess.call(['scp', cartago_path + '*_US_MSNBC_*.txt', local_path])
    ##subprocess.call(['scp', cartago_path + '*_US_KABC_*.txt', local_path])
    ##subprocess.call(['scp', cartago_path + '*_US_KCBS_*.txt', local_path])
    ##subprocess.call(['scp', cartago_path + '*_US_KNBC_*.txt', local_path])
    file_list = glob.glob(cartago_path+'*_US_CNN_*.txt')
    for fname in file_list:
        shutil.copy(fname, local_path)
    print 'Finish downloading'


    #delete_path = local_path + 'other_networks/'
    #if not os.path.exists(delete_path):
    #    os.makedirs(delete_path, 0777)
    #all_files = glob.glob(local_path + '*.txt')
    #for fname in all_files:
    #    if '_US_CNN_' in fname or '_US_FOX-News_' in fname or '_US_MSNBC_' in fname:
    #        continue
    #    shutil.move(fname, delete_path)
    #local_program_path = local_path + 'local_news/'
    #if not os.path.exists(local_program_path):
    #    os.makedirs(local_program_path, 0777)
    #all_files = glob.glob(local_path + '*.txt')
    #for fname in all_files:
    #    if '_US_CNN_' in fname or '_US_FOX-News_' in fname or '_US_MSNBC_' in fname:
    #        continue
    #    isnational = False
    #    islocal = False
    #    # move to national news
    #    for nnn in national_news_name:
    #        if nnn in fname:
    #            isnational = True
    #            break    
    #    # move to local news
    #    if isnational:
    #        continue
    #    else:
    #        for lnn in local_news_name:
    #            if lnn in fname:
    #                islocal = True
    #                break
    #        if islocal:
    #            shutil.move(fname, local_program_path)
    #        else:
    #            shutil.move(fname, delete_path)

    print 'Segmenting ...'
    #subprocess.call(['/home/vcla/Desktop/VCLA/cartago_news/storyseg/storyseg', local_path])
    #subprocess.call(['/home/vcla/Desktop/VCLA/cartago_news/storyseg/storyseg', local_program_path])
    subprocess.call([path_pre + 'storyseg/storyseg', local_path])
    ##subprocess.call([path_pre+'storyseg/storyseg', local_program_path])

     
    #############################################################################
    # preprocessing
    # process data
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    tagger = ner.SocketNER(host='localhost', port=8080)
    pool = Pool(processes = 8)
    filenames = glob.glob(local_path + '*.out')
    #filenames = glob.glob(local_path + '*_US_CNN_*.out')
    #filenames.extend(glob.glob(local_path + '*_US_FOX-News_*.out'))
    #filenames.extend(glob.glob(local_path + '*_US_MSNBC_*.out'))
    #filenames.extend(glob.glob(local_path + '*_US_KABC_*.out'))
    #filenames.extend(glob.glob(local_path + '*_US_KCBS_*.out'))
    #filenames.extend(glob.glob(local_path + '*_US_KNBC_*.out'))
    filenames.sort()


    data_needed = []
    for fname in filenames:
        data_needed.append([fname, local_path, sent_detector, tagger])
    #for data in data_needed:
    #    generate_chunk_ner_struc.generate_chunk_ner(data)
    
    #filenames_local = glob.glob(local_path + 'local_news/*.out')
    #for fname in filenames_local:
    #    data_needed.append([fname, local_path + 'local_news/', sent_detector, tagger])

    pool = Pool(processes = 8)
    pool.map(generate_chunk_ner_struc.generate_chunk_ner, data_needed)
    pool.close()
    pool.join()
    print 'Finish generating .chk file'
    

    
    # chk to docu_struc
    #input_files_ori = glob.glob(local_path + '*.chk')
    input_files = glob.glob(local_path + '*.chk')
    #for fname in input_files_ori:
    #    delete = False
    #    for dn in cnn_delete_names:
    #        if dn in fname:
    #            delete = True
    #            break
    #    if not delete:
    #        input_files.append(fname)
    input_files.sort()
    data_needed = []
    for j, fname in enumerate(input_files):
        data_needed.append([j, fname, local_path])

    #input_files2 = glob.glob(local_path + 'local_news/*.chk')
    #for j, fname in enumerate(input_files2):
    #    data_needed.append([j, fname, local_path + 'local_news/'])

    pool = Pool(processes=8)
    pool.map(read_data.read_doc, data_needed)
    pool.close()
    pool.join()
    print 'Finish generating .docu_struc file'

    # get the pair data
    data_needed = []
    filenames = glob.glob(local_path + '*.docu_struc')
    for fname in filenames:
        data_needed.append([fname, local_path])
    
    #filenames2 = glob.glob(local_path + 'local_news/*.docu_struc')
    #for fname in filenames2:
    #    data_needed.append([fname, local_path + 'local_news/'])    
 
    pool = Pool(processes=8)
    pool.map(get_pair_data.get_pair, data_needed)
    pool.close()
    pool.join()
    print 'Finish generating .pair file'
     
   
    #############################################################################
    # clustering
    #filenames = glob.glob(local_path + '*_US_CNN_*.docu_struc')
    #filenames.sort()
    #topic_clustering.do_clustering([year+month+day, filenames, local_path])
    #save_clusters.save_data(local_path + 'swc_clustering_result_' + year+month+day + '.topic', local_path)
    filenames = glob.glob(local_path + '*.docu_struc')
    #filenames.extend(glob.glob(local_path + 'local_news/*.docu_struc'))
    filenames.sort()
    flag = 1
    topic_clustering_v2.do_clustering([year+month+day, filenames, local_path, flag])
    save_clusters_v2.save_data(local_path + 'swc_clustering_result_' + year+month+day + '_all_day.topic', local_path, flag, path_pre)
    print 'Finish clustering' #results saved in 'swc_clustering_result_' + year+month+day + '_all_day.topic'
    
    
    
    #############################################################################
    # tracking
    tracking_v2.do_tracking(path_pre) #results saved in trajectory_all_day.csv
    #sort.sort_circles()
    
    """
    #############################################################################
    # finish all processing, upload to the server
    subprocess.call(['scp', '/home/weixin/Desktop/VCLA/cartago_news/event-tracking_data_all_day.json', 'election@128.97.229.75:~/viz2016/website/static/data/'])
    
    
    #local_program_path = local_path + 'local_news/'
    #############################################################################
    # extract election chunk 
    print 'Extract election chunk ...'
    #filenames = glob.glob(local_path + '*_US_CNN_*.txt')
    #filenames.extend(glob.glob(local_path + '*_US_FOX-News_*.out'))
    #filenames.extend(glob.glob(local_path + '*_US_MSNBC_*.out'))
    #filenames_tmp = glob.glob(local_path + '*.out')
    filenames = glob.glob(local_path + '*.out')
    
    #for fname in filenames_tmp:
    #    if '_US_CNN_' in fname:
    #        continue
    #    else:
    #        filenames.append(fname)
    #filenames.sort()
    
    for j, fname in enumerate(filenames):
        print j, '/', len(filenames)
        generate_candidate_sentence_file.get_sentence_with_time([fname, local_path])
    


    filenames = glob.glob(local_program_path + '*.out')
    filenames.sort()
    for j, fname in enumerate(filenames):
        print j, '/', len(filenames)
        generate_candidate_sentence_file.get_sentence_with_time([fname, local_program_path])
    

    
    #subprocess.call(['python', '/home/vcla/Desktop/VCLA/news_proc/proc.py'])
    subprocess.call(['python', '/home/weixin/Desktop/VCLA/news_proc/proc.py'])
    
    issue_classify.process_each_day(local_path, local_path, year+month+day)

     
    ddd = datetime.date.today()
    print ddd
    if ddd.isoweekday() == 1: # Monday
        print 'Monday, combine agenda result'
        last_week = []
        for k in range(1, 8):        
            dif = 8-k
            d_tmp = ddd - datetime.timedelta(days=dif)
            last_week.append([str(d_tmp.year).zfill(4), str(d_tmp.month).zfill(2), str(d_tmp.day).zfill(2)])
        combine_agenda_week.combine_week_agenda(last_week)
        run_week_topics.get_week_topics(last_week)
        subprocess.call(['scp', '/home/weixin/Desktop/VCLA/cartago_news/week_topics.json', 'election@128.97.229.75:~/viz2016/website/static/data/'])
    """
    

if __name__ == '__main__':
    main()
