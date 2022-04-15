import os
flag0=flag1=flag2=flag3=flag4=flag5=flag6=flag7=flag8=0
def Make():
	global flag0
	if(flag0==1):return
	else: flag0=1
	print( "Running: Make")
	func_path = "python3 logs_format_to_dataset.py"
	input_file = ""
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def ModelTraining(GPUTrace_csv, dataset_csv):
	global flag1
	if(flag1==1):return
	else: flag1=1
	print( "Running: ModelTraining")
	func_path = "cd ~/optimization_unified_memory/rodinia_3.1/cuda/cfd && python3 $PATH_TO_PROJECT/scripts/merger.py"
	input_file = "/Users/mdave2/Documents/HISyn/Files/GPUTrace.csv /Users/mdave2/Documents/HISyn/Files/dataset.csv "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def RunProgramVarient(fvcorr):
	global flag2
	if(flag2==1):return
	else: flag2=1
	print( "Running: RunProgramVarient")
	func_path = "./rodinia_3.1/cuda/cfd/baseline-kernel-features.sh"
	input_file = "/Users/mdave2/Documents/HISyn/Files/fvcorr "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def ModelEvaluation(kernel_data_best_csv, mergedDataSet_csv):
	global flag3
	if(flag3==1):return
	else: flag3=1
	print( "Running: ModelEvaluation")
	func_path = "cd $PATH_TO_PROJET/optimization_unified_memory/rodinia_3.1/cuda/cfd && python3 $PATH_TO_PROJET/scripts/labeler.py"
	input_file = "/Users/mdave2/Documents/HISyn/Files/kernel_data_best.csv /Users/mdave2/Documents/HISyn/Files/mergedDataSet.csv "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def BuildingDataset(output_log):
	global flag4
	if(flag4==1):return
	else: flag4=1
	print( "Running: BuildingDataset")
	func_path = "python3 $PATH_TO_PROJECT/scripts/extractData.py"
	input_file = "/Users/mdave2/Documents/HISyn/Files/output.log "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def DataFeature():
	global flag5
	if(flag5==1):return
	else: flag5=1
	print( "Running: DataFeature")
	func_path = "./rodinia_3.1/cuda/cfd/baseline-data-features.sh"
	input_file = ""
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def KernelRun(fvcorr):
	global flag6
	if(flag6==1):return
	else: flag6=1
	print( "Running: KernelRun")
	func_path = "./rodinia_3.1/cuda/cfd/run_variants.sh"
	input_file = "/Users/mdave2/Documents/HISyn/Files/fvcorr "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def DataPreProcessing(GPUTraceOutput_log):
	global flag7
	if(flag7==1):return
	else: flag7=1
	print( "Running: DataPreProcessing")
	func_path = "cd data-level-measurement && python3 $PATH_TO_PROJET/scripts/extractGPUTrace.py"
	input_file = "/Users/mdave2/Documents/HISyn/Files/GPUTraceOutput.log "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


def DataCollection(insight_log):
	global flag8
	if(flag8==1):return
	else: flag8=1
	print( "Running: DataCollection")
	func_path = "cd kernel-level-measureent && python3 $PROJECT_HOME/prototype/logs_format_to_dataset.py"
	input_file = "/Users/mdave2/Documents/HISyn/Files/insight.log "
	os.chdir('/Users/mdave2/')
	os.system (func_path+' '+input_file) 


