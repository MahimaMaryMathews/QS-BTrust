# run_all.py
import argparse
import numpy as np

np.random.seed(42)

from simulation.node import Node
from core.hashgraph import Hashgraph

def run_protocol_test(num_nodes=5):
    print("\n[+] Running QS-BTrust Protocol Test")

    try:
        nodes = [Node(f"Node{i}".encode()) for i in range(num_nodes)]
        hg = Hashgraph()

        for n in nodes:
            piid, taghash = n.generate_tag()
            hg.add(piid, taghash)

        print(f"    Registered {num_nodes} nodes")

        sender = nodes[0]
        receiver = nodes[1]

        pkt = sender.broadcast("Safety Message")
        result = receiver.verify(pkt, hg)

        if result:
            print("    [SUCCESS] Verification passed")
        else:
            print("    [FAIL] Verification failed")

    except Exception as e:
        print(f"    [ERROR] Protocol test failed: {e}")


def run_performance_evaluation():
    print("\n[+] Running Performance Evaluation")

    try:
        from evaluation.plot_results import run_plot
        run_plot()
        print("    Latency vs Vehicle Density plotted")
    except Exception as e:
        print(f"    [ERROR] Evaluation failed: {e}")


def run_visualization():
    print("\n[+] Running Traffic Visualization")

    try:
        from evaluation.traffic_visualization import run_simulation

        print("    Opening visualization (interactive window)...")
        run_simulation(2500)

    except Exception as e:
        print(f"    [ERROR] Visualization failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="QS-BTrust Reproducibility Runner"
    )

    parser.add_argument("--protocol", action="store_true")
    parser.add_argument("--eval", action="store_true")
    parser.add_argument("--viz", action="store_true")
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    print("\n=== QS-BTrust Execution Framework ===")

    if args.all or args.protocol:
        run_protocol_test()

    if args.all or args.eval:
        run_performance_evaluation()

    if args.all or args.viz:
        run_visualization()

    if not any(vars(args).values()):
        print("\n[!] No option selected. Running protocol test by default.")
        run_protocol_test()

if __name__ == "__main__":
    main()