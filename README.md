# Social Media Analysis

Code repository for Cluster and Cloud Computing 2018 project in Uni Melbourne.

Our system is built in virtual machines powered by Nectar Research Cloud.

### Technoloyies used
* Python
* Javasrcipt
* Docker
* MongoDB
* MapReduce
* TensorFlow
* Boto (auto-deployment)
* Ansible (auto-deployment)

### How it works
We collect twitter data from twitter offical API, then do sentiment analysis on tweets gathered. We analyze these data in combination with AURIN database. Final results are shown in a form of web application.

### System Architecture
<img src="/images/system_architecture.png" width="400" height="380"/>

Our system architecture is shown as above. Three instances are in charge of harvesting tweets, sentiment analysis and data storage. Last instance is resposible for web app.

### Final delivery
<img src="/images/page1.png" width="650" height="300"/>

<img src="/images/page2.png" width="650" height="300"/>

<img src="/images/page3.png" width="650" height="300"/>
