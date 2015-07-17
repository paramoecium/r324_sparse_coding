# bracketing 
codeDir=~/r324_sparse_coding/
rawData=merge-2014-11-02_to_2014-11-03.dat
baseName=allSound_allPIR_allLight_20141102_to_20141103_
#allSound_allPIR_allLight_20141102_to_20141103_PCA_Dimension3_weka.cache
for ReductionType in SC
do
	for dim in $(seq 1 10)
	do
		echo ${ReductionType} Reduced Dimensionality = $dim	
		python ${codeDir}dimReduction.py $rawData $ReductionType $dim SPL ./
		mkdir hdp_output_${ReductionType}_dim_${dim}
		python ${codeDir}DPGMM_wordConstruction.py ${baseName}${ReductionType}_Dimension${dim}_weka.cache timestamp hdp_output_${ReductionType}_dim_${dim}/
		python ${codeDir}evaluate.py hdp_output_${ReductionType}_dim_${dim}/hdp_topic truth_data-2014-11-02_to_2014-11-03.txt
	done
done
