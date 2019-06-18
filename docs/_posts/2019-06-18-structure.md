---
layout: post
title: "Topic Detection Dashboard Project Framework"
---

### 1. Background

This framework is devised with the goal of establishing a reusable and scalable dashboard. It is designed with reference to the frameworks of [Viz2016](http://128.97.229.75), [NewsSCOPE](http://newsscape.library.ucla.edu/~broadwell/newsscope/). Special thanks to Dr. Peter Broadwell and Dr. Weixin Li for generously sharing their code. Thanks Professor Steen for his consistent assistance and coordination. Also, thanks Leo for providing me with professional and useful suggestions.

### 2. Overview

**Front End Interface**

- React.js: manage front-end layout and menu logic (say goodbye to jquery)
- D3.js: visualization kernel, supporting layer for higher-level visualization tools
- Vega-Lite (and others): high-level toolkit (do not rebuild visual wheels!)
- Altair: play around with data in jupyter notebook (in later stages)

**Back End**

- Stanford NER: extract named entity from script file
- MongoDB: in this project, we no longer store .json files statically on the server; instead, we takes advantage of NoSQL database, which enables the scaling of data and increases automation. It allows us to add attributes to each tuple without the need of regenerating all the files (considering the amount of data, the re-generation work will be awful...). This will be especially beneficial to further data mining and future work.

### 3. Current Work and Future Plan

The project is now on the right track. After talking with Leo, we both agree that at the first stage(~ late July), I should focus the project part, i.e. the dashboard, as has been described in the proposal. This is a conventional visualization job but this is the right thing I should deliver to GSoC. After that, we will work towards the goal of publication, devising novel visualization schemes and conducting further data mining tasks based on .seg files. 

I talked with several PhD students from HKUST vis lab and they all expressed great interest in this project. I will talk with them recently and discuss about how to conduct visualization research with those wonderful data. Leo suggested the nearest conference:  [*The ACM CHI Conference on Human Factors in Computing Systems*]() (deadline on Sept 14). I will also look into other conferences and read related papers during the summer. If everything goes on well, the following stages, say further developing and paper writing will continue after the GSoC period. 
