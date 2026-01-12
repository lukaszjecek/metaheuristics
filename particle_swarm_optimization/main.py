from __future__ import annotations

import sys
from pathlib import Path

from src.cli import build_main_parser
from src.config import PSOConfig, RunConfig
from src.objectives.registry import get_objective
from src.core.solver import PSOSolver
from src.results.layout import make_single_run_output_dir
from src.results.writer import ResultsWriter
from src.plotting.convergence import plot_convergence_all_runs
from src.plotting.swarm_snapshots import plot_swarm_snapshots_0_mid_end

def main(argv: list[str]) -> int:
    parser = build_main_parser()
    args = parser.parse_args(argv)

    objective = get_objective(args.objective)
    mode = args.mode

    pso = PSOConfig(
        n_particles=args.n_particles,
        n_iterations=args.n_iterations,
        w=args.w,
        c1=args.c1,
        c2=args.c2,
        mode=mode,
    )

    run_cfg = RunConfig(
        objective_name=objective.name,
        bounds=objective.bounds,
        mode=mode,
        pso=pso,
        seed=args.seed,
        output_root=Path(args.output_root) if args.output_root else Path("outputs"),
        tag=args.tag,
    )

    output_dir = make_single_run_output_dir(run_cfg)
    output_dir.mkdir(parents=True, exist_ok=True)

    solver = PSOSolver(objective=objective, pso=pso)
    result = solver.run(seed=run_cfg.seed)

    writer = ResultsWriter(output_dir=output_dir)
    writer.write_meta_config_single(run_cfg=run_cfg, result=result)
    writer.write_raw_runs(run_cfg=run_cfg, run_results=[result])
    writer.write_raw_history(run_cfg=run_cfg, run_results=[result])

    plots_dir = output_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    plot_convergence_all_runs(
        raw_history_csv=output_dir / "raw_history.csv",
        out_path=plots_dir / "convergence_all_runs.png",
        title=f"Convergence (all runs) | {objective.name} | mode={mode}",
    )

    plot_swarm_snapshots_0_mid_end(
        objective=objective,
        bounds=objective.bounds,
        snapshots=result.snapshots,
        n_iterations=pso.n_iterations,
        out_path=plots_dir / "swarm_positions_0_mid_end.png",
        title=f"Swarm positions (0, mid, end) | {objective.name} | mode={mode}",
    )

    print("DONE")
    print(f"Output: {output_dir}")
    print(f"Best value: {result.final_gbest_val}")
    print(f"Best position: ({result.final_gbest_x}, {result.final_gbest_y})")
    print(f"Elapsed [s]: {result.elapsed_s:.6f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))