from __future__ import annotations

import itertools
import sys
from pathlib import Path

from src.cli import build_experiment_parser
from src.config import PSOConfig, RunConfig
from src.core.solver import PSOSolver
from src.objectives.registry import get_objective, list_objectives
from src.plotting.convergence import (
    plot_convergence_all_runs,
    plot_convergence_single_run,
)
from src.plotting.parameter_influence import plot_parameter_influence
from src.plotting.swarm_snapshots import plot_swarm_snapshots_0_mid_end
from src.results.layout import make_config_dir_name, make_experiment_output_dir
from src.results.stats import aggregate_config_results
from src.results.writer import ResultsWriter


def build_grid_plan(args) -> list[PSOConfig]:
    plan: list[PSOConfig] = []
    for n_particles, n_iterations, w, c1, c2 in itertools.product(
        args.n_particles_list,
        args.n_iterations_list,
        args.w_list,
        args.c1_list,
        args.c2_list,
    ):
        plan.append(
            PSOConfig(
                n_particles=int(n_particles),
                n_iterations=int(n_iterations),
                w=float(w),
                c1=float(c1),
                c2=float(c2),
                mode=args.mode,
            )
        )

    uniq = {}
    for c in plan:
        key = (c.n_particles, c.n_iterations, c.w, c.c1, c.c2, c.mode)
        uniq[key] = c
    return list(uniq.values())


def main(argv: list[str]) -> int:
    parser = build_experiment_parser()
    args = parser.parse_args(argv)

    if args.n_runs < 5:
        raise SystemExit("ERROR: n_runs must be >= 5.")

    objectives: list[str]
    if args.objective == "all":
        objectives = list_objectives()
    else:
        objectives = [args.objective]

    output_root = Path(args.output_root) if args.output_root else Path("outputs")
    exp_root = make_experiment_output_dir(output_root=output_root, tag=args.tag)
    exp_root.mkdir(parents=True, exist_ok=True)

    all_agg_rows: list[dict] = []
    writer_root = ResultsWriter(output_dir=exp_root)

    plan = build_grid_plan(args)

    for obj_name in objectives:
        objective = get_objective(obj_name)

        for pso_cfg in plan:
            solver = PSOSolver(objective=objective, pso=pso_cfg)

            run_cfg = RunConfig(
                objective_name=objective.name,
                bounds=objective.bounds,
                mode=pso_cfg.mode,
                pso=pso_cfg,
                seed=args.seed,
                output_root=exp_root,
                tag=args.tag,
            )

            cfg_dir_name = make_config_dir_name(
                objective_name=objective.name,
                mode=pso_cfg.mode,
                n_particles=pso_cfg.n_particles,
                n_iterations=pso_cfg.n_iterations,
                w=pso_cfg.w,
                c1=pso_cfg.c1,
                c2=pso_cfg.c2,
            )
            cfg_dir = exp_root / "configs" / cfg_dir_name
            cfg_dir.mkdir(parents=True, exist_ok=True)
            (cfg_dir / "plots").mkdir(parents=True, exist_ok=True)
            (cfg_dir / "plots" / "runs").mkdir(parents=True, exist_ok=True)

            writer = ResultsWriter(output_dir=cfg_dir)

            run_results = solver.run_multiple(
                n_runs=args.n_runs,
                master_seed=run_cfg.seed,
            )

            writer.write_meta_config_experiment(run_cfg=run_cfg, run_results=run_results)
            writer.write_raw_runs(run_cfg=run_cfg, run_results=run_results)
            writer.write_raw_history(run_cfg=run_cfg, run_results=run_results)

            agg = aggregate_config_results(run_cfg=run_cfg, run_results=run_results)
            writer.write_agg_summary(agg_row=agg)

            plot_convergence_all_runs(
                raw_history_csv=cfg_dir / "raw_history.csv",
                out_path=cfg_dir / "plots" / "convergence_all_runs.png",
                title=f"Convergence (all runs) | {objective.name} | mode={pso_cfg.mode} | {cfg_dir_name}",
            )

            for rr in run_results:
                run_plot_dir = cfg_dir / "plots" / "runs" / f"run_{rr.run_id}"
                run_plot_dir.mkdir(parents=True, exist_ok=True)

                plot_convergence_single_run(
                    raw_history_csv=cfg_dir / "raw_history.csv",
                    run_id=rr.run_id,
                    out_path=run_plot_dir / "convergence.png",
                    title=(
                        f"Convergence | {objective.name} | mode={pso_cfg.mode} | "
                        f"{cfg_dir_name} | run_id={rr.run_id}"
                    ),
                )

                plot_swarm_snapshots_0_mid_end(
                    objective=objective,
                    bounds=objective.bounds,
                    snapshots=rr.snapshots,
                    n_iterations=pso_cfg.n_iterations,
                    out_path=run_plot_dir / "swarm_positions_0_mid_end.png",
                    title=(
                        f"Swarm positions (0, mid, end) | {objective.name} | mode={pso_cfg.mode} | "
                        f"{cfg_dir_name} | run_id={rr.run_id}"
                    ),
                )

            all_agg_rows.append(agg)

    plots_dir = exp_root / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    plot_parameter_influence(
        agg_rows=all_agg_rows,
        out_dir=plots_dir,
        mode=args.mode,
    )

    writer_root.write_agg_summary_all(
        agg_rows=all_agg_rows,
        out_path=exp_root / "agg_summary_all.csv",
    )

    print("DONE")
    print(f"Experiment output: {exp_root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))