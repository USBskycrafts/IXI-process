# How to use the toolchain for IXI dataset

## 0. Install the fsl and freesurfer

Please follow the install instruction on the web of FSL and Freesufer tools.

## 1. Group the different modals into a folder
The IXI dataset contains different modalities (e.g. T1, T2, PD, MRA, DTI). In order to use the toolchain, all these modalities need to be grouped into a single folder. This can be done using the following command:

```bash
python dataset_normlization.py --input_dir <path_to_ixi_dataset> --output_dir <path_to_output_folder>
```

## 2. reorient the MRI images
The IXI dataset contains MRI images that are not aligned in the same orientation. In order to use the toolchain, the MRI images need to be reoriented to the same orientation. This can be done using the following command:

```bash
python reorient.py --input_dir <path_to_output_folder> --output_dir <path_to_output_folder>
```
## 3. remove the skull from the MRI images
The IXI dataset contains MRI images that have a skull. In order to use the toolchain, the skull needs to be removed from the MRI images. This can be done using the following command:

```bash
python brain_extraction.py --input_dir <path_to_output_folder> --output_dir <path_to_output_folder>
```
## 4. registration

all modals will be registered to a template (e.g.  MNI152_T1_1mm_brain.nii.gz). This can be done using the following command:

```bash
python registration.py --input_dir <path_to_output_folder> --output_dir <path_to_output_folder> -ref_path <path_to_MNI152_T1_1mm_brain.nii.gz>
```
