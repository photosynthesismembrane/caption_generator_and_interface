#!/bin/bash
#SBATCH --time=0-23:59:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=a100:2
#SBATCH --job-name=autocap
#SBATCH --mem=100G

module purge
module load CUDA/12.1.1
module load Python/3.11.3-GCCcore-12.3.0
module load GCCcore/12.3.0

source venv/bin/activate

export HF_DATASETS_CACHE="/scratch/$USER/.cache/huggingface/datasets"
export TRANSFORMERS_CACHE="/scratch/$USER/.cache/huggingface/transformers"

python answer_questions.py --image_folder="images" --questions_file_path="questions.js" --json_file_path="reformatted_image_data.js"

deactivate
