# Event-Related Bias Removal for Real-time Disaster Events

### Evangelia Spiliopoulou, Salvador Medina, Eduard Hovy, Alexander Hauptmann
#### Findings of EMNLP 2020

Social  media  has  become  an  important  toolto share information about crisis events suchas natural disasters and mass attacks.  Detect-ing actionable posts that contain useful infor-mation  requires  rapid  analysis  of  huge  vol-umes of data in real-time.  This poses a com-plex problem due to the large amount of poststhat do not contain any actionable information.Furthermore, the classification of informationin real-time systems requires training on out-of-domain  data,  as  we  do  not  have  any  datafrom  a  new  emerging  crisis.   Prior  work  fo-cuses on models pre-trained on similar eventtypes.  However, those models capture unnec-essary event-specific biases,  like the locationof the event, which affect the generalizabilityand performance of the classifiers on new un-seen  data  from  an  emerging  new  event.    Inour work, we train an adversarial neural modelto remove latent event-specific biases and im-prove  the  performance  on  tweet  importanceclassification.

[\Paper[\]]() [\[Code\]]()

