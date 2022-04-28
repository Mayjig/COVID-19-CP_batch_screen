# COVID-19-CP batch screening
This repository contains k-nearest neighbor machine learning models for predicting anti-SARS-CoV-2 activities of screening compounds. Nine assays are included in the prediction:
assay1 3CL_enzymatic_activity
assay2 ACE2_enzymatic_activity
assay3 HEK293_cell_line_toxicity
assay4 Human_fibroblast_toxicity
assay5 SARS-CoV-2_cytopathic_effect_CPE
assay6 SARS-CoV-2_cytopathic_effect_host_tox_counterscreen
assay7 Spike-ACE2_protein-protein_interaction_AlphaLISA
assay8 Spike-ACE2_protein-protein_interaction_TruHit_Counterscreen
assay9 TMPRSS2_enzymatic_activity

##Workflow
1. Install Anaconda and python3 for your operating system.
2. For python program, install scikit-learn with version higher than 0.24
3. git clone this repo
4. Input molecules file(s) into "input_smi" or "input_sdfmol" folder according to the molecular formats. (There are template input files in the folders.)
5. Run "convert_sdfmol.sh" or "convert_smi.sh" based on input files.
6. Run python file "prediction.py"
7. The prediction results are saved in "classification_results.csv" file.

##Citation
Please cite: Beihong Ji, Yuhui Wu, Elena N Thomas, Jocelyn N Edwards, Xibing He, Junmei Wang. Development of Machine Learning Models to Predict A Chemical’s Anti-SARS-CoV-2 Activities.
