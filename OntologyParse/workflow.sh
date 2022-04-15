#!/bin/bash
#Enter Path to your project in below line. (eg PATH_TO_PROJECT=/Users/mdave2 )
PATH_TO_PROJECT=/Users/mdave2
### build adapter
cd $PATH_TO_PROJECT/rodinia_3.1/cuda-adapter && make

## (Kernel Run)
bash $PATH_TO_PROJECT/rodinia_3.1/cuda/cfd/run_variants.sh $PATH_TO_PROJECT/Files/fvcorr

# (Building Dataset)
python3 $PATH_TO_PROJECT/scripts/extractData.py $PATH_TO_PROJECT/Files/GPUTrace.csv $PATH_TO_PROJECT/Files/dataset.csv

## (DataFeature)
bash $PATH_TO_PROJECT/rodinia_3.1/cuda/cfd/baseline-data-features.sh

## (DataPreprocessing)
cd $PATH_TO_PROJECT/data-level-measurement && python3 $PATH_TO_PROJECT/scripts/extractGPUTrace.py $PATH_TO_PROJECT/Files/GPUTraceOutput.log

## (RunProgramVarient)
bash $PATH_TO_PROJECT/rodinia_3.1/cuda/cfd/baseline-kernel-features.sh $PATH_TO_PROJECT/Files/fvcorr

## (Data Collection)
cd $PATH_TO_PROJECT/kernel-level-measureent && python3 $PATH_TO_PROJECT/prototype/logs_format_to_dataset.py $PATH_TO_PROJECT/Files/insight.log

# (Model Training)
cd $PATH_TO_PROJECT/optimization_unified_memory/rodinia_3.1/cuda/cfd && python3 $PATH_TO_PROJECT/scripts/merger.py $PATH_TO_PROJECT/Files/output.log


# (Model Evaluation)
cd $PATH_TO_PROJECT/optimization_unified_memory/rodinia_3.1/cuda/cfd && python3 $PATH_TO_PROJECT/scripts/labeler.py $PATH_TO_PROJECT/Files/kernel_data_best.csv $PATH_TO_PROJECT/Files/mergedDataSet.csv
