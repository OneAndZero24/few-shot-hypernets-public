#!/bin/bash
#SBATCH --job-name=experiment
#SBATCH --qos=test
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --partition=student

BASEPATH="path_to_directory_with_best_model_and_args"

cd $HOME/fork/miksa/few-shot-hypernets-public

source activate few-shot-learning

sh ./hypershot_uncertainty.sh "$BASEPATH"