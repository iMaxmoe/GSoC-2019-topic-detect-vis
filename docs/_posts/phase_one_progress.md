---

layout: post
title: "Phase 1 Progress"
---

It feels great to work on the topic detection visualization project. This post includes all my work which will be done during the Phase 1 evaluation.This phase is directly headed towards the coding part of the project.

## :ballot_box_with_check: Task List 

The main job in this phase is to establish a robust pipeline to effectively fetch and process data from Cartago, getting them ready for visualization.

#### 1. Document Dr. Weixin's data processing pipeline 

Skim through Dr. Weixin's data processing code, make brief documentation for latter programmers, pick up the reusable code. Also learn something from it LOL.

__- Segmentation__

- [x] cleansing.py
- [x] collect_program_names.py
- [x] combine_agenda_week.py
- [x] get_pair_data.py
- [x] read_data.py
- [ ] readingfiles.py

__- Clustering__

- [ ] generate_chunk_ner_struc.py
- [ ] save_clusters.py
- [ ] save_clusters_v2.py
- [ ] save_week_top_topics.py
- [ ] sw.py
- [ ] topic_clustering.py
- [ ] topic_clustering_v2.py

__- Tracking__

- [ ] tracking.py
- [ ] tracking_v2.py
- [ ] track_gun_violence_by_week.py

__- Miscellaneous__

- [x] candidates.py

- [x] document.py

- [x] graph_cycle.py

- [ ] image.py

- [ ] new_topic_model_final_with_image.py

- [ ] probability.py

- [x] process.py

- [x] process2015.py

- [x] process_other_year_data.py

- [ ] run_CNN_out.py

- [ ] run_previous_topic.py

- [ ] run_week_topics.py

- [ ] sort.py

- [ ] sort_old.py

- [ ] topic_model_v2.py

- [ ] vocabulary.py

  

#### 2. Build textual data processing pipeline for topic detection

- Enable data query given keywords and a random time range, say one week, one month, one year.

  - [ ] Given a keyword, count its occurrences in a <u>certain time interval</u> at a <u>given region</u>
  - [ ] Detect the high frequency topics in a <u>certain time interval</u> at a <u>given region</u>

- Data formatted in JSON and return to front end

  


#### 3. Visual Module I: Topic Frequency Detection

The front end part is relatively easy here. (? implementation of filter)

- Plot the frequency trend of a given keyword

- Visualize high frequency topics using word cloud (Only for experiment, novel and interactive features will be added in phase II)

  


##:film_projector: ​ Problem Box

This section lists the problems I met&fixed /predicted. Hope it could be helpful for buddies. 

**1. Searching over a big time range may require long time, which leads to long waiting time of users.**

