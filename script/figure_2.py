import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_root)
from utils.file_system import load_sequences
from model.F_k_function import *

import yaml
import matplotlib.pyplot as plt
from easydict import EasyDict

def main():
    config_path = "../config/run_fig_2.yaml"
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    args = EasyDict(config)

    data_path = args.get("data_path", "../dataset/test.fasta")
    figure_output_path = args.get("figure_output_path", "../result/figure/")

    seq_list = load_sequences(data_path)

    F_k_v1 = F_k_function_v1(seq_list[0], seq_list[1], "basic_kmer_matches", args).get_F_k()
    F_k_v2 = F_k_function_v2(seq_list[0], seq_list[1], "start_ry_matches", args).get_F_k()
    F_k_paper = F_k_function_paper(seq_list[0], seq_list[1], "basic_kmer_matches", args).get_F_k()

    # k_values = list(range(1, 25))
    k_values = list(range(2, 25))

    plt.figure(figsize=(10, 6))
    plt.plot(k_values[:len(F_k_v2)], F_k_v2, marker='o', linestyle='-', color='b', label='F_k_v2')
    plt.plot(k_values[:len(F_k_paper)], F_k_paper, marker='s', linestyle='-', color='r', label='F_k_paper')
    plt.plot(k_values[:len(F_k_v1)], F_k_v1, marker='^', linestyle='-', color='y', label='F_k_v1')

    plt.xlabel('Word Length (k)')
    plt.ylabel('Number of Matches F(k)')
    plt.title('Relationship between F(k) and Word Length (k)')
    plt.grid(True)
    plt.legend()
    plt.savefig(figure_output_path + 'F_k_vs_k.png') 
    plt.show()

if __name__ == "__main__":
    main()