---
layout: post
title: "Phase 1 Progress"
---

It is a great feeling to work on the Red Hen Rapid Annotator-2.0 Project and adding production level code in the project. This post includes all my work which will be done during the Phase 1 evaluation.This phase is directly headed towards the coding part of the project.

# [](#header-1)Decisions made post community bonding period

After the community bonding period several changes has been redefined and there has been addition of two taks. The following things is decided on several deliberation with the mentors:
1. There should a admin CRUD in the project. Admins should be able to see and access all experiments.
2. It would be perfect to have an "export to Rapid Annotator" button in CQPweb. -&gt; Waiting for the feedback from Andrew Hardie to implement this feature.
3. Add support for tagging Scheme is redefined. Now in the tagging scheme the annotation labels can be reused bu the user for other experiment as well. This will save user's time a lot and provide a more comprehensible way for the annotations.


# [](#header-2) Progress made so far

The following features has been implemented till so far:

* Addition of Admin in the experiment. Now, Admins should be able to see and access all others experiments.
* When starting not logged in at an address such as cluos.ikw.uos.de:8000/home, the green warning is over the login and sign up buttons, so these are not accessible. Now these buttons are made accessible and the green warning now automatically fades out after some time.
* Added "Undo" functionality for the last element in the set of annotations.
* Include Video link and captions in the result export.
* Added functionality of pausing the video with the space and again play it using the space key.