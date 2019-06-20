---
layout: post
title: "Phase 1 Progress"
font: "Noto Sans"
---

It feels great to work on the topic detection visualization project. This post includes all my work which will be done during the Phase 1 evaluation.This phase is directly headed towards the coding part of the project.

## :ballot_box_with_check: Task List 

The main job in this phase is to establish a robust pipeline to effectively fetch and process data from Cartago, getting them ready for visualization.

#### 1. Document Dr. Weixin's data processing pipeline 

Skim through Dr. Weixin's data processing code, make brief documentation for latter programmers, pick up the reusable code. Also learn something from it LOL.

- __Segmentation__

- [x] cleansing.py
- [x] collect_program_names.py
- [x] combine_agenda_week.py
- [x] get_pair_data.py
- [x] read_data.py
- [x] readingfiles.py

__- Clustering__

- [x] generate_chunk_ner_struc.py
- [x] save_clusters.py
- [x] save_clusters_v2.py
- [x] save_week_top_topics.py
- [x] sw.py
- [x] topic_clustering.py
- [x] topic_clustering_v2.py

__- Tracking__

- [x] tracking.py
- [x] tracking_v2.py
- [x] track_gun_violence_by_week.py

__- Miscellaneous__

- [x] candidates.py

- [x] document.py

- [x] graph_cycle.py

- [x] image.py

- [x] new_topic_model_final_with_image.py

- [x] probability.py

- [x] process.py

- [x] process2015.py

- [x] process_other_year_data.py

- [x] run_CNN_out.py

- [x] run_previous_topic.py

- [x] run_week_topics.py

- [x] sort.py

- [x] sort_old.py

- [x] topic_model_v2.py

- [x] vocabulary.py

  

#### 2. Build textual data processing pipeline for topic detection

- Enable data query given keywords and a random time range, say one week, one month, one year.

  - [x] Detect the high frequency topics in a <u>certain time interval</u> at a <u>given region</u>
  - [ ] Given a keyword, count its occurrences in a <u>certain time interval</u> at a <u>given region</u>

- Data formatted in JSON and return to front end

  


#### 3. Visual Module I: Topic Frequency Detection

The front end part is relatively easy here. (? implementation of filter)

- Plot the frequency trend of a given keyword

- Visualize high frequency topics using word cloud (Only for experiment, novel and interactive features will be added in phase II)

  


## :film_projector: ​ Problem Box

This section lists the problems I met&fixed /predicted. Hope it could be helpful for buddies. 

**1. Searching over a big time range may require long time, which leads to long waiting time of users.**

